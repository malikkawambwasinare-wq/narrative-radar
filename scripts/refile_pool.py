#!/usr/bin/env python3
"""Narrative Radar — re-file the pool against every narrative we now track.

    python3 scripts/refile_pool.py                 # report
    python3 scripts/refile_pool.py --write         # file what matches

Costs nothing: no API calls, no model calls. The pool holds claim-carrying
videos that matched no narrative AT THE TIME they were read. Every promotion
adds a narrative with its own vocabulary, so yesterday's unmatched video is
often today's match — a newly promoted narrative starts with the handful of
videos that evidenced it, and this hands it the rest of what we already hold.

Run it after any promotion, and after the vocabulary sharpens.
"""
import json, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from channel_sweep import best_topic, corpus_titles, topic_vocab

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv
TODAY = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%d")


def main():
    wl = json.loads((ROOT / "watchlist.json").read_text())["topics"]
    vocab = topic_vocab(wl, corpus_titles())
    pool_f = ROOT / "discovery-pool.json"
    pool_doc = json.loads(pool_f.read_text())
    pool = pool_doc.get("videos", [])

    corpora, known = {}, set()
    for t in wl:
        f = ROOT / "corpus" / t["id"] / "videos.json"
        if f.exists():
            corpora[t["id"]] = json.loads(f.read_text())
            known |= {v["videoId"] for v in corpora[t["id"]]["videos"]}

    matched, keep = defaultdict(list), []
    for v in pool:
        if v["videoId"] in known:
            continue
        # Pool material arrives without context, so it has to clear the higher
        # bar: a distinctive two-word phrase in the title, not two loose words.
        tid, score = best_topic(v.get("title", ""), "", vocab, min_score=7, require_gram=True)
        if tid and tid in corpora:
            matched[tid].append(v)
        else:
            keep.append(v)

    print(f"pool {len(pool):,} videos · {len(wl)} narratives")
    for tid, vs in sorted(matched.items(), key=lambda x: -len(x[1])):
        have = len(corpora[tid]["videos"])
        print(f"  {tid:32} +{len(vs):<6} ({have:,} → {have + len(vs):,})")
        for v in vs[:2]:
            print(f"      {v.get('published', '?')}  {v.get('title', '')[:72]}")
    total = sum(len(v) for v in matched.values())
    print(f"+{total:,} videos filed · pool left with {len(keep):,}{'' if WRITE else ' (dry run)'}")

    if not WRITE or not total:
        return
    for tid, vs in matched.items():
        doc = corpora[tid]
        for v in sorted(vs, key=lambda x: x.get("published") or ""):
            doc["videos"].append({
                "videoId": v["videoId"], "title": v.get("title", ""), "channel": v.get("channel", ""),
                "url": f"https://www.youtube.com/watch?v={v['videoId']}",
                "published": v.get("published"), "first_seen": v.get("found") or TODAY,
                "views": None, "length": None, "age_days": None,
                "query": f"refiled from the pool ({v.get('found_by', 'discovery')})",
                "transcript": None, "verdict": "UNREVIEWED", "verdict_basis": "metadata",
                "yt": {"channelId": v["channelId"]} if v.get("channelId") else {},
            })
        doc["updated"] = TODAY
        (ROOT / "corpus" / tid / "videos.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    pool_doc["videos"] = keep
    pool_doc["generated"] = TODAY
    pool_f.write_text(json.dumps(pool_doc, indent=1) + "\n")


if __name__ == "__main__":
    main()
