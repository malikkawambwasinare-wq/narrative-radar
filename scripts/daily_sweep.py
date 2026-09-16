#!/usr/bin/env python3
"""Narrative Radar — the daily sweep: add every narrative's new uploads to its corpus.

    python3 scripts/daily_sweep.py                      # every narrative, dry run
    python3 scripts/daily_sweep.py --write              # append new videos to videos.json
    python3 scripts/daily_sweep.py crypto-winter-watch --days=7 --write

Runs every morning in GitHub Actions (.github/workflows/corpus-daily.yml).
For each narrative it searches its queries for uploads from the last --days
(default 14, so a missed day or two is caught up), skips anything already in
the corpus, and appends the rest as UNREVIEWED with first_seen = today. It
never changes a video that is already there, never reorders the file, and
never touches verdicts.

Two routes, chosen automatically:
  * YT_API_KEY set → the official YouTube Data API: search.list (newest first,
    publishedAfter), then videos.list and channels.list for exact publish
    dates, views, likes, comments, duration, category and channel country/size.
    Works from any server. ~100 quota units per query per narrative per day;
    8 narratives x 6 queries is ~4,900 of the free 10,000.
  * no key → the sweep STOPS. Reading YouTube's search page is scraping, which
    the Terms forbid and which would put API access at risk. The old page route
    is kept below for reference only and runs solely with --allow-scraping,
    which nothing in this repo passes. Decision of 2026-09-16: API only.

Transcripts and reviews are not done here: YouTube withholds captions from
data-centre IPs, and verdicts are made with the transcript in hand.
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import collector  # search_youtube, age_days (no third-party imports)

WRITE = "--write" in sys.argv
DAYS = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--days=")), 14))
MAX_PER_TOPIC = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--max=")), 40))
ONLY = [a for a in sys.argv[1:] if not a.startswith("--")]
KEY = os.environ.get("YT_API_KEY", "").strip()
API = "https://www.googleapis.com/youtube/v3/"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def api(path, **params):
    params["key"] = KEY
    url = API + path + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/json"}), timeout=30) as r:
        return json.loads(r.read())


def iso_duration(d):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return None
    days, h, mi, s = (int(x or 0) for x in m.groups())
    h += days * 24
    return f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"


_categories = {}
def category_name(cid):
    if not _categories:
        try:
            for c in api("videoCategories", part="snippet", regionCode="US").get("items", []):
                _categories[c["id"]] = c["snippet"]["title"]
        except Exception:
            _categories["_"] = None
    return _categories.get(cid)


def via_api(queries, known):
    """New video entries from the Data API, with full details."""
    after = (datetime.now(timezone.utc) - timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    found = {}
    for q in queries:
        try:
            res = api("search", part="id", q=q, type="video", order="date", publishedAfter=after, maxResults=25)
        except Exception as e:
            print(f"    ! search {q!r}: {e}"); continue
        for it in res.get("items", []):
            vid = it["id"].get("videoId")
            if vid and vid not in known and vid not in found:
                found[vid] = q
    ids = list(found)[:MAX_PER_TOPIC]
    entries, chan_ids = [], set()
    for i in range(0, len(ids), 50):
        for v in api("videos", part="snippet,contentDetails,statistics", id=",".join(ids[i:i + 50])).get("items", []):
            sn, st, cd = v["snippet"], v.get("statistics", {}), v.get("contentDetails", {})
            chan_ids.add(sn["channelId"])
            views = st.get("viewCount")
            entries.append({
                "videoId": v["id"], "url": f"https://www.youtube.com/watch?v={v['id']}",
                "title": sn["title"], "channel": sn["channelTitle"],
                "published": sn["publishedAt"][:10],
                "views": f"{int(views):,} views" if views else "",
                "length": iso_duration(cd.get("duration")) or "",
                "query": found[v["id"]], "age_days": None, "first_seen": TODAY,
                "transcript": None, "verdict": "UNREVIEWED", "verdict_basis": "metadata",
                "yt": {
                    "category": category_name(sn.get("categoryId")), "channelId": sn["channelId"],
                    "likes": int(st["likeCount"]) if "likeCount" in st else None,
                    "comments": int(st["commentCount"]) if "commentCount" in st else None,
                    "captions": "manual" if cd.get("caption") == "true" else None,
                    "language": (sn.get("defaultAudioLanguage") or "").split("-")[0] or None,
                    "live": sn.get("liveBroadcastContent") not in (None, "none"),
                    "enrichedOn": TODAY, "source": "data-api",
                },
            })
    chans = {}
    ch_list = list(chan_ids)
    for i in range(0, len(ch_list), 50):
        for c in api("channels", part="snippet,statistics", id=",".join(ch_list[i:i + 50])).get("items", []):
            st = c.get("statistics", {})
            chans[c["id"]] = {
                "channelCountry": c["snippet"].get("country"),
                "channelJoined": c["snippet"].get("publishedAt", "")[:10] or None,
                "subscribers": None if st.get("hiddenSubscriberCount") else int(st.get("subscriberCount", 0)) or None,
                "channelViews": int(st["viewCount"]) if "viewCount" in st else None,
                "channelVideos": int(st["videoCount"]) if "videoCount" in st else None,
            }
    for e in entries:
        e["yt"].update(chans.get(e["yt"]["channelId"], {}))
    return entries


def via_search_page(queries, known):
    """New video entries from the public search page (no key): basic fields only."""
    found = {}
    for q in queries:
        try:
            hits = collector.search_youtube(q, sort_newest=True)
        except Exception as e:
            print(f"    ! search {q!r}: {str(e)[:80]}"); hits = []
        for v in hits:
            age = collector.age_days(v["published"])
            if v["videoId"] in known or v["videoId"] in found or age is None or age > DAYS:
                continue
            found[v["videoId"]] = {**v, "age_days": round(age, 2), "first_seen": TODAY,
                                   "transcript": None, "verdict": "UNREVIEWED", "verdict_basis": "metadata"}
        time.sleep(1.5)
    return list(found.values())[:MAX_PER_TOPIC]


def main():
    watch = json.loads((ROOT / "watchlist.json").read_text())
    if not KEY and "--allow-scraping" not in sys.argv:
        print("daily sweep: no YT_API_KEY, so nothing was collected.")
        print("  This project collects through the YouTube Data API only (decision 2026-09-16).")
        print("  Set the YT_API_KEY secret to resume. The corpus is unchanged.")
        print("+0 new videos across 0 narratives (no api key)")
        return
    route = "data-api" if KEY else "search-page (override)"
    total, touched = 0, []
    print(f"daily sweep {TODAY} · route: {route} · uploads from the last {DAYS} days")
    for t in watch["topics"]:
        if ONLY and t["id"] not in ONLY:
            continue
        f = ROOT / "corpus" / t["id"] / "videos.json"
        if not f.exists() or not t.get("queries"):
            continue
        doc = json.loads(f.read_text())
        known = {v["videoId"] for v in doc["videos"]}
        new = (via_api if KEY else via_search_page)(t["queries"], known)
        print(f"  {t['id']:28s} +{len(new)}")
        for v in new[:5]:
            print(f"      {v.get('published') or '?':>12}  {v['title'][:70]}")
        if new and WRITE:
            doc["videos"].extend(new)
            f.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        if new:
            total += len(new); touched.append(t["id"])
    # Last line is the commit summary the workflow reads.
    print(f"+{total} new videos across {len(touched)} narratives ({route})")


if __name__ == "__main__":
    main()
