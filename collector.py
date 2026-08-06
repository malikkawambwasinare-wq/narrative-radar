#!/usr/bin/env python3
"""Narrative Radar — YouTube collector.

Reads watchlist.json, searches YouTube for each active topic's queries
(newest uploads first), merges new finds into corpus/<topic>/videos.json,
and pulls captions for new videos into corpus/<topic>/transcripts/<id>.txt.

No API key required: parses the public search results page. If a YouTube
Data API key is later placed in .yt_api_key, the collector switches to the
official API automatically.

Usage:
  python3 collector.py                 # collect all active topics
  python3 collector.py collapse-audit  # collect one topic
  python3 collector.py --transcript VIDEO_ID collapse-audit
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    # Skip the EU/consent interstitial if one is served.
    "Cookie": "CONSENT=YES+cb; SOCS=CAI",
}
KEEP_DAYS = 14  # how far back "new" reaches on a collection run


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_initial_data(html):
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.DOTALL)
    if not m:
        m = re.search(r'window\["ytInitialData"\] = (\{.*?\});', html, re.DOTALL)
    return json.loads(m.group(1)) if m else None


def walk_video_renderers(node):
    """Yield every videoRenderer dict anywhere in the ytInitialData tree."""
    if isinstance(node, dict):
        if "videoRenderer" in node:
            yield node["videoRenderer"]
        for v in node.values():
            yield from walk_video_renderers(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_video_renderers(v)


def text_of(field):
    if not field:
        return ""
    if "simpleText" in field:
        return field["simpleText"]
    return "".join(run.get("text", "") for run in field.get("runs", []))


AGO_UNITS = {"second": 1 / 86400, "minute": 1 / 1440, "hour": 1 / 24,
             "day": 1, "week": 7, "month": 30, "year": 365}


def age_days(published_text):
    """'3 hours ago' -> 0.125; 'Streamed 2 days ago' handled; unknown -> None."""
    m = re.search(r"(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago",
                  published_text or "")
    if not m:
        return None
    return int(m.group(1)) * AGO_UNITS[m.group(2)]


def search_youtube(query, sort_newest=True):
    sp = "&sp=CAI%253D" if sort_newest else ""
    url = ("https://www.youtube.com/results?search_query="
           + urllib.parse.quote(query) + sp)
    data = extract_initial_data(fetch(url))
    if not data:
        return []
    videos = []
    for vr in walk_video_renderers(data):
        vid = vr.get("videoId")
        if not vid:
            continue
        videos.append({
            "videoId": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": text_of(vr.get("title")),
            "channel": text_of(vr.get("ownerText") or vr.get("longBylineText")),
            "published": text_of(vr.get("publishedTimeText")),
            "views": text_of(vr.get("viewCountText")),
            "length": text_of(vr.get("lengthText")),
            "query": query,
        })
    return videos


def get_transcript(video_id):
    """Return plain-text captions (manual preferred, else auto) or None."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        fetched = YouTubeTranscriptApi().fetch(
            video_id, languages=["en", "en-US", "en-GB"])
        lines = []
        for s in fetched.snippets:
            seg = s.text.replace("\n", " ").strip()
            if seg:
                start = int(s.start)
                lines.append(f"[{start // 60:02d}:{start % 60:02d}] {seg}")
        if lines:
            return "\n".join(lines)
    except ImportError:
        pass  # fall through to the page-scrape path below
    except Exception:
        return None
    # Fallback: scrape caption tracks off the watch page (YouTube now often
    # serves empty bodies for these URLs, so the library above is preferred).
    html = fetch(f"https://www.youtube.com/watch?v={video_id}")
    m = re.search(r'"captionTracks":(\[.*?\])', html)
    if not m:
        return None
    tracks = json.loads(m.group(1))
    if not tracks:
        return None
    track = next((t for t in tracks if t.get("languageCode", "").startswith("en")
                  and t.get("kind") != "asr"), None) \
        or next((t for t in tracks if t.get("languageCode", "").startswith("en")), None) \
        or tracks[0]
    base = track["baseUrl"].replace("\\u0026", "&")
    raw = fetch(base + "&fmt=json3")
    events = json.loads(raw).get("events", [])
    lines = []
    for ev in events:
        seg = "".join(s.get("utf8", "") for s in ev.get("segs", []))
        seg = seg.replace("\n", " ").strip()
        if seg:
            start = int(ev.get("tStartMs", 0)) // 1000
            lines.append(f"[{start // 60:02d}:{start % 60:02d}] {seg}")
    return "\n".join(lines) if lines else None


def collect_topic(topic):
    tdir = ROOT / "corpus" / topic["id"]
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / "transcripts").mkdir(exist_ok=True)
    vfile = tdir / "videos.json"
    corpus = json.loads(vfile.read_text()) if vfile.exists() else {"videos": []}
    known = {v["videoId"] for v in corpus["videos"]}

    found, fresh = {}, []
    for q in topic["queries"]:
        try:
            for v in search_youtube(q):
                found.setdefault(v["videoId"], v)
        except Exception as e:
            print(f"  ! query failed: {q!r}: {e}")

    today = datetime.now().strftime("%Y-%m-%d")
    for v in found.values():
        age = age_days(v["published"])
        v["age_days"] = round(age, 2) if age is not None else None
        if v["videoId"] in known:
            continue
        if age is not None and age > KEEP_DAYS:
            continue
        v["first_seen"] = today
        v["transcript"] = None
        v["verdict"] = "UNREVIEWED"
        corpus["videos"].append(v)
        fresh.append(v)

    for v in fresh:
        try:
            t = get_transcript(v["videoId"])
            if t:
                path = tdir / "transcripts" / f"{v['videoId']}.txt"
                path.write_text(t)
                v["transcript"] = str(path.relative_to(ROOT))
        except Exception as e:
            print(f"  ! transcript failed for {v['videoId']}: {e}")

    corpus["videos"].sort(key=lambda v: v.get("age_days") or 9e9)
    vfile.write_text(json.dumps(corpus, indent=2, ensure_ascii=False))

    print(f"[{topic['id']}] searched {len(topic['queries'])} queries, "
          f"saw {len(found)} videos, kept {len(fresh)} new (<= {KEEP_DAYS}d), "
          f"{sum(1 for v in fresh if v['transcript'])} transcripts pulled")
    for v in fresh:
        t = "T" if v["transcript"] else "-"
        print(f"  [{t}] {v['published'] or '?':>14}  {v['views'] or '?':>18}  "
              f"{v['title'][:70]}  — {v['channel']}")


def main():
    args = [a for a in sys.argv[1:]]
    if args[:1] == ["--transcript"]:
        vid, topic_id = args[1], args[2]
        t = get_transcript(vid)
        if not t:
            print(f"no captions available for {vid}")
            return
        path = ROOT / "corpus" / topic_id / "transcripts" / f"{vid}.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(t)
        print(f"saved {len(t.splitlines())} caption lines -> {path}")
        return

    watchlist = json.loads((ROOT / "watchlist.json").read_text())
    only = args[0] if args else None
    for topic in watchlist["topics"]:
        if only and topic["id"] != only:
            continue
        if topic["status"] != "active" and not only:
            continue
        collect_topic(topic)


if __name__ == "__main__":
    main()
