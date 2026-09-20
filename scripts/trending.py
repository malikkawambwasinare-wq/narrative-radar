#!/usr/bin/env python3
"""Narrative Radar — what is being watched, and what is being argued about.

    python3 scripts/trending.py                  # dry run, both sources
    python3 scripts/trending.py --write          # save today's board
    python3 scripts/trending.py --youtube-only   # skip X (no token, or no spend)

Two sources, because they answer different questions.

  YouTube's own chart=mostPopular is what people are WATCHING. One quota unit
  per region-category slice, returning 50 videos each, from the same API and
  the same terms as everything else we do. Roughly 60 units a day of the 10,000.

  X's trends endpoint is what people are ARGUING ABOUT, and it usually knows
  first — a claim circulates as text long before anyone films a thirty minute
  video about it. Trends cost $0.010 per REQUEST, flat, so five locations a day
  is about $1.50 a month.

Why we never read the posts
  Reading X posts costs $0.005 per post, which is where a bill like this runs
  away: a thousand posts a day is $150 a month. We do not need the conversation,
  only the phrase. The phrase becomes a YouTube search against quota we already
  own, and the videos we get back are the evidence. X tells us where to look;
  YouTube is what we look at.

What this is not
  A trend is an EVENT. A narrative is a claim that recurs. Nothing here becomes
  a tracked narrative on the strength of one day's trending — that is what the
  recurrence test in promote_narratives.mjs is for, and rebuilding the tracked
  set daily would destroy the ledger, which is the only thing here that cannot
  be rebuilt. This script fills a candidate board, nothing more.

What it writes
  trending/<date>.json   the day's board, both sources, with what each phrase
                         already matches in the corpus
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "trending"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

WRITE = "--write" in sys.argv
YT_ONLY = "--youtube-only" in sys.argv
X_ONLY = "--x-only" in sys.argv

YT_KEY = os.environ.get("YT_API_KEY", "").strip()

# Where the claims we care about actually circulate. English-first because the
# corpus is, plus the two biggest non-US English markets and India, which drives
# a large share of the health and finance content we already track.
REGIONS = ["US", "GB", "CA", "AU", "IN"]

# The categories our industries live in. Entertainment and Music are excluded
# deliberately: they trend hardest and carry almost no checkable claims, so they
# would swamp the board with noise we would only have to filter back out.
CATEGORIES = {
    "25": "News & Politics",
    "28": "Science & Technology",
    "27": "Education",
    "26": "Howto & Style",
    "22": "People & Blogs",
}

# X wants a WOEID per location. 1 is worldwide.
X_LOCATIONS = {"1": "Worldwide", "23424977": "United States", "23424975": "United Kingdom"}


def x_token():
    t = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not t:
        f = ROOT / ".secrets" / "x-bearer-token"
        if f.exists():
            t = f.read_text().strip()
    return t


def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def youtube_trending():
    """chart=mostPopular, one unit per slice. Returns rows and units spent."""
    if not YT_KEY:
        print("  no YT_API_KEY in the environment — skipping YouTube")
        return [], 0
    rows, units = [], 0
    for region in REGIONS:
        for cat_id, cat in CATEGORIES.items():
            q = urllib.parse.urlencode({
                "part": "snippet,statistics", "chart": "mostPopular",
                "regionCode": region, "videoCategoryId": cat_id,
                "maxResults": 50, "key": YT_KEY})
            try:
                r = get(f"https://www.googleapis.com/youtube/v3/videos?{q}")
                units += 1
            except urllib.error.HTTPError as e:
                body = ""
                try:
                    body = e.read().decode()[:160]
                except Exception:
                    pass
                # A region that does not chart a category is a 400, not a fault.
                if e.code != 400:
                    print(f"  {region}/{cat}: HTTP {e.code} {body}")
                continue
            for it in r.get("items", []):
                sn, st = it.get("snippet", {}), it.get("statistics", {})
                rows.append({
                    "videoId": it["id"], "title": sn.get("title", ""),
                    "channel": sn.get("channelTitle", ""), "channelId": sn.get("channelId"),
                    "published": (sn.get("publishedAt") or "")[:10],
                    "views": int(st.get("viewCount", 0) or 0),
                    "region": region, "category": cat,
                })
            time.sleep(0.1)
    return rows, units


def x_trends():
    """Trends by location. $0.010 per request, charged per request not result."""
    tok = x_token()
    if not tok:
        print("  no X token (.secrets/x-bearer-token) — skipping X")
        return [], 0.0
    rows, spend = [], 0.0
    for woeid, place in X_LOCATIONS.items():
        try:
            r = get(f"https://api.x.com/2/trends/by/woeid/{woeid}",
                    {"Authorization": f"Bearer {tok}"})
            spend += 0.010
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode()[:200]
            except Exception:
                pass
            print(f"  X {place}: HTTP {e.code} {body}")
            continue
        for t in r.get("data", []):
            rows.append({"phrase": t.get("trend_name") or t.get("name"),
                         "posts": t.get("post_count") or t.get("tweet_volume"),
                         "place": place})
        time.sleep(0.5)
    return rows, spend


def corpus_index():
    """Channels and narrative vocabulary we already hold, so the board can say
    whether a trend is new to us or something we are already watching."""
    chans, titles = {}, []
    for f in (ROOT / "corpus").glob("*/videos.json"):
        topic = f.parent.name
        for v in json.loads(f.read_text())["videos"]:
            if v.get("channelId"):
                chans.setdefault(v["channelId"], topic)
            elif v.get("channel"):
                chans.setdefault(v["channel"], topic)
            titles.append((v.get("title") or "").lower())
    return chans, titles


def words(s):
    return {w for w in "".join(c if c.isalnum() else " " for c in (s or "").lower()).split()
            if len(w) > 3}


def main():
    print(f"trending board {TODAY}")
    yt, units = ([], 0) if X_ONLY else youtube_trending()
    xt, spend = ([], 0.0) if YT_ONLY else x_trends()
    chans, titles = corpus_index()

    # A trending video from a channel already in a corpus is confirmation. One
    # from a channel we have never seen is the interesting case: it is how the
    # ledger should grow, and it is invisible unless we say so.
    known = [v for v in yt if v.get("channelId") in chans or v.get("channel") in chans]
    fresh = [v for v in yt if v not in known]

    print(f"\nYouTube: {len(yt)} trending videos · {units} quota units")
    print(f"  {len(known)} from channels we hold · {len(fresh)} from channels we do not")
    seen_ch = {}
    for v in fresh:
        seen_ch.setdefault(v["channel"], []).append(v)
    for ch, vs in sorted(seen_ch.items(), key=lambda kv: -max(x["views"] for x in kv[1]))[:12]:
        top = max(vs, key=lambda x: x["views"])
        print(f"    {top['views']:>10,}  {ch[:26]:26} {top['title'][:52]}")

    print(f"\nX: {len(xt)} trends · ${spend:.2f}")
    # Which trending phrases overlap language already in the corpus? That is the
    # cheapest possible signal that a trend belongs to a story we track.
    for t in xt[:20]:
        w = words(t["phrase"])
        hits = sum(1 for tt in titles if w and w <= words(tt)) if w else 0
        mark = f"  ({hits} videos already)" if hits else "  NEW"
        vol = f"{t['posts']:,}" if t.get("posts") else "—"
        print(f"    {vol:>10}  {t['phrase'][:44]:44}{mark}")

    if WRITE:
        OUT.mkdir(exist_ok=True)
        p = OUT / f"{TODAY}.json"
        p.write_text(json.dumps({
            "date": TODAY,
            "note": "what is being watched and what is being argued about; candidates, not narratives",
            "youtube": {"units_spent": units, "regions": REGIONS,
                        "categories": list(CATEGORIES.values()),
                        "known_channels": len(known), "new_channels": len(seen_ch),
                        "videos": yt},
            "x": {"usd_spent": round(spend, 3), "locations": list(X_LOCATIONS.values()),
                  "trends": xt},
        }, indent=1, ensure_ascii=False) + "\n")
        print(f"\nwrote {p.relative_to(ROOT)}")
    else:
        print("\n(dry run — pass --write to save the board)")
    if spend:
        print(f"X spend today: ${spend:.2f}")


if __name__ == "__main__":
    main()
