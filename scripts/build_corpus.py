#!/usr/bin/env python3
"""Narrative Radar — stock a corpus back through time, not just the last 14 days.

    python3 scripts/build_corpus.py anti-inflammatory-diet --years 5 --write

collector.py sweeps newest-first and keeps 14 days: right for a running
narrative, useless for founding one. This runs the topic's queries by
relevance, adds year-suffixed variants ("<query> 2022") so YouTube surfaces
older uploads, keeps anything published inside the window, and writes the
merged videos.json. Enrichment (exact dates, signals) and transcripts are
separate steps:

    python3 scripts/enrich_youtube.py <topic> --write
    python3 scripts/fetch_transcripts.py <topic> --write
"""
import json, sys, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import collector  # noqa: E402  (search_youtube, age_days)

WRITE = "--write" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
TOPIC = args[0]
def default_years(topic_id):
    """The narrative's whole life (from narrative.json `born`), never under 5."""
    f = ROOT / "corpus" / topic_id / "narrative.json"
    try:
        born = json.loads(f.read_text()).get("born", "")
        y = int(born[:4])
        return max(5, datetime.now().year - y + 1)
    except Exception:
        return 5
YEARS = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--years=")), 0)) or default_years(args[0])
PAUSE = 1.5

watch = json.loads((ROOT / "watchlist.json").read_text())
topic = next(t for t in watch["topics"] if t["id"] == TOPIC)
this_year = datetime.now().year
# Queries often carry the year they were written in ("crypto winter 2026").
# Strip it before adding each year, or "crypto winter 2026 2022" searches for nothing.
import re
def base(q):
    return re.sub(r"\s+", " ", re.sub(r"\b(19|20)\d\d\b", "", q)).strip()
queries, seen_q = [], set()
for q in topic["queries"]:
    if q.lower() not in seen_q:
        queries.append(q); seen_q.add(q.lower())
bases = []
for q in topic["queries"]:
    b = base(q)
    if b and b.lower() not in [x.lower() for x in bases]:
        bases.append(b)
for q in bases[:3]:
    for y in range(this_year - YEARS + 1, this_year + 1):
        yq = f"{q} {y}"
        if yq.lower() not in seen_q:
            queries.append(yq); seen_q.add(yq.lower())

tdir = ROOT / "corpus" / TOPIC
tdir.mkdir(parents=True, exist_ok=True)
vfile = tdir / "videos.json"
corpus = json.loads(vfile.read_text()) if vfile.exists() else {"videos": []}
known = {v["videoId"] for v in corpus["videos"]}

found = {}
for q in queries:
    try:
        hits = collector.search_youtube(q, sort_newest=False)
    except Exception as e:
        print(f"  ! {q!r}: {e}"); continue
    n = 0
    for v in hits:
        if v["videoId"] not in found:
            found[v["videoId"]] = v; n += 1
    print(f"  {len(hits):3d} hits, {n:3d} new  ← {q}")
    time.sleep(PAUSE)

today = datetime.now().strftime("%Y-%m-%d")
kept, too_old, undated = [], 0, 0
for v in found.values():
    age = collector.age_days(v["published"])
    v["age_days"] = round(age, 2) if age is not None else None
    if age is None:
        undated += 1
    elif age > YEARS * 365.25:
        too_old += 1; continue
    if v["videoId"] in known:
        continue
    v.update(first_seen=today, transcript=None, verdict="UNREVIEWED")
    kept.append(v)

by_year = {}
for v in kept:
    y = (datetime.now().timestamp() - (v["age_days"] or 0) * 86400)
    by_year[datetime.fromtimestamp(y).year] = by_year.get(datetime.fromtimestamp(y).year, 0) + 1
print(f"\n{len(found)} distinct videos seen · {len(kept)} new inside {YEARS} years · {too_old} older dropped · {undated} undated kept")
print("approx by year:", dict(sorted(by_year.items())))
if WRITE:
    corpus["videos"].extend(kept)
    corpus["videos"].sort(key=lambda v: v.get("age_days") or 9e9)
    vfile.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n")
    print(f"written → {vfile.relative_to(ROOT)} ({len(corpus['videos'])} videos)")
else:
    print("dry run — add --write")
