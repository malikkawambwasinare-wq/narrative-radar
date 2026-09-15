#!/usr/bin/env python3
"""Narrative Radar — apply transcript-review verdict files to a corpus.

    python3 scripts/merge_review.py anti-inflammatory-diet            # dry run
    python3 scripts/merge_review.py anti-inflammatory-diet --write

Reads corpus/<topic>/review/verdicts-*.json (gitignored working files written
by the reviewers) and, per video, sets our own analysis only:
  verdict, verdict_note, verdict_basis, reviewed_on,
  review: {pitch, evidence, stance}     — labels, never third-party text
Extracted claims (in our words) accumulate in claims-extracted.json; run
scripts/mark-horizons.mjs afterwards to stamp horizon_dated.
Refuses to write if any verdict file is malformed or a video is graded twice.
"""
import json, sys, collections
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv
topic = [a for a in sys.argv[1:] if not a.startswith("--")][0]
base = ROOT / "corpus" / topic
ENUM = {"verdict": {"ORIGINAL", "DERIVATIVE", "RECYCLED", "CLICKBAIT"},
        "verdict_basis": {"transcript", "metadata"},
        "stance": {"maximalist", "moderate", "skeptic", "none"},
        "evidence": {"outcome-trials", "biomarkers", "anecdote", "none"}}

rows = []
for f in sorted((base / "review").glob("verdicts-*.json")):
    rows += json.loads(f.read_text())
dupes = [k for k, c in collections.Counter(r["videoId"] for r in rows).items() if c > 1]
bad = [(r["videoId"], k, r.get(k)) for r in rows for k, ok in ENUM.items() if r.get(k) not in ok]
if dupes or bad:
    sys.exit(f"refusing: duplicates {dupes[:5]} bad values {bad[:5]}")

vf = base / "videos.json"
corpus = json.loads(vf.read_text())
by_id = {v["videoId"]: v for v in corpus["videos"]}
cf = base / "claims-extracted.json"
claims = json.loads(cf.read_text()) if cf.exists() else []
seen = {(c["videoId"], c["claim"]) for c in claims}
today = date.today().isoformat()
applied, new_claims, unknown = 0, 0, []
for r in rows:
    v = by_id.get(r["videoId"])
    if not v:
        unknown.append(r["videoId"]); continue
    v["verdict"] = r["verdict"]
    v["verdict_note"] = r["note"]
    v["verdict_basis"] = r["verdict_basis"]
    v["reviewed_on"] = today
    v["review"] = {"pitch": r.get("pitch"), "evidence": r["evidence"], "stance": r["stance"]}
    applied += 1
    for c in r.get("claims", []):
        if (r["videoId"], c["claim"]) not in seen:
            seen.add((r["videoId"], c["claim"]))
            claims.append({"videoId": r["videoId"], "status": "UNREVIEWED", **c})
            new_claims += 1

left = [v["videoId"] for v in corpus["videos"] if v.get("verdict") == "UNREVIEWED"]
print(f"{applied} verdicts applied, {new_claims} claims extracted, {len(unknown)} unknown ids, {len(left)} videos still unreviewed")
print("verdicts:", dict(collections.Counter(v["verdict"] for v in corpus["videos"])))
if WRITE:
    vf.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n")
    cf.write_text(json.dumps(claims, indent=2, ensure_ascii=False) + "\n")
    print("written")
else:
    print("dry run — add --write")
