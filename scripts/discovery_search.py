#!/usr/bin/env python3
"""Narrative Radar — spend the scarce search calls on what only search can do.

    python3 scripts/discovery_search.py                    # dry run
    python3 scripts/discovery_search.py --calls=40 --write

search.list is capped at 100 calls a day and cannot be topped up. Reading a
known channel's uploads costs a hundredth as much, so the daily collection runs
on channel uploads and search is reserved for the two jobs nothing else can do:
finding CHANNELS we have never seen, and finding CLAIMS that belong to no
narrative we track.

What it writes
  channel-candidates.json  channels seen for the first time, for the ledger to
                           screen at tier B
  discovery-pool.json      claim-carrying videos that match no tracked narrative.
                           This is the raw material new narratives come from:
                           discover_narratives.py reads it alongside the corpora.

Queries rotate by day, so every industry and every narrative comes round within
a few days, inside the ~20-day window in which search can still see an upload.
Official API only (decision 2026-09-16).
"""
import json, os, re, sys, urllib.parse, urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from discover_narratives import CLAIM_MARK, words           # one definition of "carries a claim"

ROOT = Path(__file__).resolve().parent.parent
API = "https://www.googleapis.com/youtube/v3/search"
KEY = os.environ.get("YT_API_KEY", "").strip()
WRITE = "--write" in sys.argv
arg = lambda n, d: next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{n}=")), d)
CALLS = int(arg("calls", 40))
DAYS = int(arg("days", 7))
TODAY = datetime.now(timezone.utc)
DAY_INDEX = int(TODAY.strftime("%j"))
POOL_CAP = 20000


def search(q, after):
    r = urllib.request.Request(API + "?" + urllib.parse.urlencode({
        "key": KEY, "part": "snippet", "type": "video", "order": "date",
        "publishedAfter": after, "maxResults": 50, "q": q}))
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode())


def rotation():
    """Today's slice of the query list: industry seeds and candidate narratives
    first, because those reach material no tracked corpus covers."""
    inds = json.loads((ROOT / "industries.json").read_text())["industries"]
    wl = json.loads((ROOT / "watchlist.json").read_text())["topics"]
    qs = []
    for i in inds:
        for c in i.get("candidates", []):
            for q in c.get("seed_queries", []):
                qs.append((q, i["name"], f"candidate:{c['id']}"))
        for term in i.get("seed_terms", []):
            qs.append((term, i["name"], "industry seed"))
    for t in wl:
        for q in t.get("queries", []):
            qs.append((q, t.get("industry", "Unsorted"), f"narrative:{t['id']}"))
    start = (DAY_INDEX * CALLS) % max(1, len(qs))
    return [qs[(start + k) % len(qs)] for k in range(min(CALLS, len(qs)))]


def main():
    if not KEY:
        print("discovery search: no YT_API_KEY. Official API only (decision 2026-09-16); nothing collected.")
        return
    known_videos, known_channels = set(), {}
    for f in (ROOT / "corpus").glob("*/videos.json"):
        for v in json.loads(f.read_text())["videos"]:
            known_videos.add(v["videoId"])
    led = ROOT / "channels.json"
    if led.exists():
        for r in json.loads(led.read_text())["channels"]:
            if r.get("channelId"):
                known_channels[r["channelId"]] = r["tier"]
    cand_f, pool_f = ROOT / "channel-candidates.json", ROOT / "discovery-pool.json"
    cands = json.loads(cand_f.read_text())["channels"] if cand_f.exists() else []
    pool = json.loads(pool_f.read_text())["videos"] if pool_f.exists() else []
    for c in cands:
        known_channels.setdefault(c["channelId"], "candidate")
    pool_ids = {v["videoId"] for v in pool} | known_videos

    after = (TODAY - timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    queries = rotation()
    print(f"discovery search {TODAY:%Y-%m-%d} · {len(queries)} of the 100 daily search calls · last {DAYS} days")
    new_ch, new_pool, seen, by_ind = 0, 0, 0, defaultdict(int)
    for q, industry, why in queries:
        try:
            r = search(q, after)
        except Exception as e:
            print(f"  ! {q[:40]}: {e}")
            continue
        for it in r.get("items", []):
            sn, vid = it["snippet"], it["id"].get("videoId")
            if not vid:
                continue
            seen += 1
            cid = sn.get("channelId")
            if cid and cid not in known_channels:
                known_channels[cid] = "candidate"
                cands.append({"channelId": cid, "channel": sn.get("channelTitle", ""),
                              "found": TODAY.strftime("%Y-%m-%d"), "found_by": q,
                              "industry": industry, "basis": "search"})
                new_ch += 1
            title = sn.get("title", "")
            if vid in pool_ids or not CLAIM_MARK.search(title):
                continue
            pool_ids.add(vid)
            pool.append({"videoId": vid, "title": title, "channel": sn.get("channelTitle", ""),
                         "channelId": cid, "published": (sn.get("publishedAt") or "")[:10],
                         "industry": industry, "found": TODAY.strftime("%Y-%m-%d"), "found_by": why})
            new_pool += 1
            by_ind[industry] += 1

    pool = pool[-POOL_CAP:]
    print(f"  {seen} results · {new_ch} channels never seen before · {new_pool} claim-carrying videos into the pool")
    for ind, n in sorted(by_ind.items(), key=lambda x: -x[1])[:8]:
        print(f"      {ind[:26]:28}+{n}")
    for v in pool[-6:]:
        print(f"      {v['published']}  {v['title'][:72]}")
    if WRITE:
        cand_f.write_text(json.dumps({"generated": TODAY.strftime("%Y-%m-%d"), "channels": cands}, indent=1) + "\n")
        pool_f.write_text(json.dumps({"generated": TODAY.strftime("%Y-%m-%d"),
                                      "note": "claim-carrying videos matching no tracked narrative; raw material for new ones",
                                      "videos": pool}, indent=1) + "\n")
    print(f"+{new_ch} channels · +{new_pool} pooled videos · pool holds {len(pool)} (discovery search)")


if __name__ == "__main__":
    main()
