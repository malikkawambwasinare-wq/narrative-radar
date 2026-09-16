#!/usr/bin/env python3
"""Narrative Radar — collect new uploads from the channels in the ledger.

    python3 scripts/channel_sweep.py                      # dry run, tier A
    python3 scripts/channel_sweep.py --write              # append to the corpora
    python3 scripts/channel_sweep.py --tiers=AB --days=14 --write

Why this exists
  The daily sweep searches each narrative's queries, which spends about half of
  the 100 daily search calls — the one bucket that cannot be topped up and the
  only way to find channels and narratives we do not yet know. Reading a known
  channel's uploads costs 1 unit per 50 videos from the 10,000 bucket instead,
  so this route collects more for a fraction of the scarce resource and leaves
  search free for discovery.

How it works
  For every channel in channels.json at the chosen tiers, it walks the uploads
  playlist back `--days`, keeps videos not already in a corpus, scores each
  title and description against every narrative's query vocabulary, and files
  the ones that clearly belong. Everything else is reported and dropped, since
  a channel we follow also posts about other things.

  Requires YT_API_KEY. Official API only (decision 2026-09-16).
"""
import json, os, re, sys, urllib.parse, urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://www.googleapis.com/youtube/v3/"
KEY = os.environ.get("YT_API_KEY", "").strip()
WRITE = "--write" in sys.argv
arg = lambda name, dflt: next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{name}=")), dflt)
DAYS = int(arg("days", 7))
TIERS = set(arg("tiers", "A").upper())
MAX_CHANNELS = int(arg("max", 400))
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
CUTOFF = datetime.now(timezone.utc) - timedelta(days=DAYS)

STOP = set("""the and for with that this from what how why your you are was were will has have not but all any
about into over more most just now new best top vs video watch full episode part live""".split())
units = 0


def call(endpoint, **params):
    global units
    params["key"] = KEY
    url = API + endpoint + "?" + urllib.parse.urlencode(params, doseq=True)
    with urllib.request.urlopen(url, timeout=30) as r:
        units += 1
        return json.loads(r.read().decode())


def words(s):
    s = re.sub(r"[^a-z0-9'\s-]", " ", (s or "").lower())
    return [w for w in s.split() if len(w) > 2 and w not in STOP]


def topic_vocab(topics):
    """Each narrative's search vocabulary: the phrases it is collected by."""
    vocab = {}
    for t in topics:
        grams, singles = set(), set()
        for q in t.get("queries", []):
            ws = words(q)
            singles |= set(ws)
            grams |= {" ".join(ws[i:i + 2]) for i in range(len(ws) - 1)}
        vocab[t["id"]] = (grams, singles)
    return vocab


def best_topic(text, vocab):
    """A video belongs to the narrative whose vocabulary it clearly carries:
    a two-word phrase from a query, or three distinct query words."""
    t = " ".join(words(text))
    tw = set(t.split())
    best, score = None, 0
    for tid, (grams, singles) in vocab.items():
        g = sum(1 for gm in grams if gm in t)
        s = len(tw & singles)
        sc = g * 3 + s
        if (g >= 1 or s >= 3) and sc > score:
            best, score = tid, sc
    return best, score


def uploads_items(playlist_id):
    """Videos from an uploads playlist, newest first, back to the cutoff."""
    out, page = [], None
    for _ in range(10):                       # 500 videos per channel per run, hard stop
        r = call("playlistItems", part="snippet,contentDetails", playlistId=playlist_id,
                 maxResults=50, **({"pageToken": page} if page else {}))
        stop = False
        for it in r.get("items", []):
            pub = it["contentDetails"].get("videoPublishedAt") or it["snippet"].get("publishedAt")
            if not pub:
                continue
            when = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            if when < CUTOFF:
                stop = True
                continue
            sn = it["snippet"]
            out.append({"videoId": it["contentDetails"]["videoId"], "title": sn.get("title", ""),
                        "description": (sn.get("description") or "")[:1200],
                        "published": when.strftime("%Y-%m-%d"), "channel": sn.get("channelTitle", ""),
                        "channelId": sn.get("videoOwnerChannelId") or sn.get("channelId")})
        page = r.get("nextPageToken")
        if stop or not page:
            break
    return out


def hydrate(ids):
    """Duration, views and the rest, 50 at a time."""
    meta = {}
    for i in range(0, len(ids), 50):
        r = call("videos", part="contentDetails,statistics,snippet", id=",".join(ids[i:i + 50]), maxResults=50)
        for it in r.get("items", []):
            cd, st, sn = it.get("contentDetails", {}), it.get("statistics", {}), it.get("snippet", {})
            m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", cd.get("duration", "") or "")
            h, mi, se = (int(x or 0) for x in (m.groups() if m else (0, 0, 0)))
            meta[it["id"]] = {
                "length": (f"{h}:{mi:02d}:{se:02d}" if h else f"{mi}:{se:02d}"),
                "views": int(st.get("viewCount", 0) or 0),
                "yt": {"category": sn.get("categoryId"), "channelId": sn.get("channelId"),
                       "language": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage"),
                       "captions": cd.get("caption") == "true", "live": sn.get("liveBroadcastContent") not in (None, "none"),
                       "likes": int(st.get("likeCount", 0) or 0) or None,
                       "comments": int(st.get("commentCount", 0) or 0) or None,
                       "enrichedOn": TODAY},
            }
    return meta


def main():
    if not KEY:
        print("channel sweep: no YT_API_KEY. Official API only (decision 2026-09-16); nothing collected.")
        return
    ledger = json.loads((ROOT / "channels.json").read_text())["channels"]
    rows = [r for r in ledger if r["tier"] in TIERS and r.get("channelId")][:MAX_CHANNELS]
    wl = json.loads((ROOT / "watchlist.json").read_text())["topics"]
    vocab = topic_vocab(wl)

    corpora, known = {}, set()
    for t in wl:
        f = ROOT / "corpus" / t["id"] / "videos.json"
        if f.exists():
            corpora[t["id"]] = json.loads(f.read_text())
            known |= {v["videoId"] for v in corpora[t["id"]]["videos"]}

    print(f"channel sweep {TODAY} · tier {''.join(sorted(TIERS))} · {len(rows)} channels · last {DAYS} days")
    seen, matched, off_topic = 0, defaultdict(list), 0
    for r in rows:
        try:
            items = uploads_items("UU" + r["channelId"][2:])
        except Exception as e:
            print(f"  ! {r['channel'][:34]}: {e}")
            continue
        for v in items:
            seen += 1
            if v["videoId"] in known:
                continue
            tid, score = best_topic(v["title"] + " " + v["description"], vocab)
            if not tid:
                off_topic += 1
                continue
            v["_score"] = score
            matched[tid].append(v)

    ids = [v["videoId"] for vs in matched.values() for v in vs]
    meta = hydrate(ids) if ids else {}

    total = 0
    for tid, vs in sorted(matched.items()):
        doc = corpora.get(tid)
        if not doc:
            continue
        add = []
        for v in sorted(vs, key=lambda x: x["published"], reverse=True):
            m = meta.get(v["videoId"], {})
            if m.get("yt", {}).get("live"):
                continue
            add.append({
                "videoId": v["videoId"], "title": v["title"], "channel": v["channel"],
                "url": f"https://www.youtube.com/watch?v={v['videoId']}",
                "published": v["published"], "first_seen": TODAY,
                "views": m.get("views"), "length": m.get("length"),
                "age_days": (datetime.now(timezone.utc) - datetime.fromisoformat(v["published"] + "T00:00:00+00:00")).days,
                "query": f"channel sweep: {v['channel']}", "transcript": None,
                "verdict": "UNREVIEWED", "verdict_basis": "metadata", "yt": m.get("yt", {}),
            })
        print(f"  {tid:28s} +{len(add)}")
        for v in add[:4]:
            print(f"      {v['published']}  {v['title'][:74]}")
        if add and WRITE:
            doc["videos"].extend(add)
            (ROOT / "corpus" / tid / "videos.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        total += len(add)

    print(f"  {seen} uploads read · {off_topic} off-topic for these narratives · {units} quota units")
    print(f"+{total} new videos across {len(matched)} narratives (channel uploads)")


if __name__ == "__main__":
    main()
