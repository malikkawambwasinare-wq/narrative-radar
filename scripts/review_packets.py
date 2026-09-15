#!/usr/bin/env python3
"""Narrative Radar — cut a corpus into review packets for the transcript graders.

    python3 scripts/review_packets.py housing-crash-watch            # packets of <= 27 videos
    python3 scripts/review_packets.py housing-crash-watch --per=20

Selects videos that still need a proper verdict: UNREVIEWED ones, and ones whose
verdict was guessed from title and metadata where a transcript now exists.
Each packet carries the narrative's context (claim, industry, current camps)
and, per video, its metadata plus a transcript excerpt (first ~600 and last
~220 words). Packets are written to corpus/<topic>/review/ — gitignored,
because excerpts are third-party text.
"""
import json, os, re, sys, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
TOPIC = args[0]
PER = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--per=")), 27))
base = ROOT / "corpus" / TOPIC
rd = lambda f: json.loads((base / f).read_text()) if (base / f).exists() else None
watch = json.loads((ROOT / "watchlist.json").read_text())
topic = next(t for t in watch["topics"] if t["id"] == TOPIC)
narr = rd("narrative.json") or {}
claims = (rd("claims.json") or {}).get("claims", [])
vids = rd("videos.json")["videos"]

has_t = lambda v: bool(v.get("transcript")) and (ROOT / v["transcript"]).exists()
todo = [v for v in vids if v.get("verdict") == "UNREVIEWED" or (v.get("verdict_basis") != "transcript" and has_t(v))]
todo.sort(key=lambda v: v.get("published") or "")

def excerpt(path, head=600, tail=220):
    words = re.sub(r"\[\d+:\d+(?::\d+)?\]\s*", " ", (ROOT / path).read_text()).split()
    if len(words) <= head + tail:
        return " ".join(words), len(words)
    return " ".join(words[:head]) + " […middle omitted…] " + " ".join(words[-tail:]), len(words)

camps = [f"- {c['statement']}: " + " / ".join(k.get("position", "") for k in c.get("camps") or []) for c in claims if c.get("camps")]
header = "\n".join([
    f"# Narrative: {topic['name']}",
    f"industry: {topic.get('industry')}",
    f"core claim: {narr.get('claim') or topic.get('notes', '')}",
    "known contested questions and camps:" if camps else "known contested questions: none recorded yet",
    *camps, ""])

(base / "review").mkdir(exist_ok=True)
for old in (base / "review").glob("packet-*.md"):
    old.unlink()
packets = [todo[i:i + PER] for i in range(0, len(todo), PER)]
for i, pk in enumerate(packets):
    out = [header]
    for v in pk:
        y = v.get("yt") or {}
        ex = excerpt(v["transcript"]) if has_t(v) else None
        out.append(f"### {v['videoId']}\ntitle: {v['title']}\nchannel: {v['channel']} | published: {v.get('published')} | {v.get('views')} | length {v.get('length')} | YouTube paid-promotion flag: {y.get('paidPromotion')}\n"
                   + (f"transcript ({ex[1]} words total), excerpt:\n" + "\n".join(textwrap.wrap(ex[0], 110)) if ex else "transcript: NONE (grade from title/channel only)") + "\n")
    (base / "review" / f"packet-{i}.md").write_text("\n".join(out))
print(f"{TOPIC}: {len(todo)} videos to grade ({sum(1 for v in todo if has_t(v))} with transcript) → {len(packets)} packet(s)")
