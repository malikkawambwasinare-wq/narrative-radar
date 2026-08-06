#!/usr/bin/env python3
"""Merge verdict files (analyst output) into videos.json.

Usage: python3 merge_verdicts.py <topic-id> <verdicts.json> [more.json ...]
Each verdicts file: [{"videoId", "verdict", "note", "claims": [...]}]
Verdicts land on the matching video; extracted claims accumulate in
corpus/<topic>/claims-extracted.json for later ledger review.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
topic = sys.argv[1]
tdir = ROOT / "corpus" / topic
vfile = tdir / "videos.json"
cfile = tdir / "claims-extracted.json"

corpus = json.loads(vfile.read_text())
by_id = {v["videoId"]: v for v in corpus["videos"]}
claims = json.loads(cfile.read_text()) if cfile.exists() else []
claim_keys = {(c["videoId"], c["claim"]) for c in claims}

applied = new_claims = 0
for path in sys.argv[2:]:
    for r in json.loads(Path(path).read_text()):
        v = by_id.get(r["videoId"])
        if not v:
            print(f"  ! unknown videoId {r['videoId']} in {path}")
            continue
        v["verdict"] = r["verdict"]
        v["verdict_note"] = r.get("note", "")
        applied += 1
        for c in r.get("claims", []):
            key = (r["videoId"], c["claim"])
            if key not in claim_keys:
                claim_keys.add(key)
                claims.append({"videoId": r["videoId"], "status": "UNREVIEWED", **c})
                new_claims += 1

vfile.write_text(json.dumps(corpus, indent=2, ensure_ascii=False))
cfile.write_text(json.dumps(claims, indent=2, ensure_ascii=False))
counts = {}
for v in corpus["videos"]:
    counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
print(f"applied {applied} verdicts, {new_claims} new claims extracted")
print("  " + ", ".join(f"{k}: {n}" for k, n in sorted(counts.items())))
