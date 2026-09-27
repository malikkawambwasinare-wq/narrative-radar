#!/usr/bin/env python3
"""Narrative Radar — turn a bucket the reader filed "split" into its narratives.

    python3 scripts/story_split.py --bucket housing-crash-watch            # dry run
    python3 scripts/story_split.py --bucket housing-crash-watch --write
    python3 scripts/story_split.py --bucket the-2026-setup --write --no-ai # vocabulary only

Why this exists
  The two largest buckets in the corpus hold 43,000 videos between them and
  neither is a narrative. The reader said so: housing is three tellings under
  one name, the 2026 setup is five. A set built from a bucket mixes tellings of
  different things, so no story is offered an evening until it has been split.

How a video finds its narrative
  1. The reader's cached per-video reads (each with a one-line "what this video
     argues") are assigned to the split's children in one Gemini call. That is
     a few dozen labelled videos per child.
  2. From those labels and the child's name, a title vocabulary is learned the
     same way the sweep learns one (distinctive terms, content words only,
     scripts/_lexicon.py), and every video in the bucket is scored against
     each child. A video goes to its best child if it clears MIN_SCORE, and
     nowhere otherwise. Filing nothing is better than filing wrong.

What it writes
  stories.json                 the story's children, status "reading"
  watchlist.json               a topic per child, story set, status "forming"
  corpus/<child>/videos.json   the bucket's videos that clearly belong to it
  corpus/<child>/narrative.json  a skeleton: claim = the child's name, until read
  The bucket itself is left untouched; it stays as the story's evidence.
"""
import json, re, sys, time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lexicon import has_content
from _gemini import ROOT, ApiError, DailyLimit, ask, key, payload

WRITE = "--write" in sys.argv
NO_AI = "--no-ai" in sys.argv
MODEL = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--model"), "gemini-3.8-flash")
BUCKET = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--bucket"), None)
MIN_SCORE = 4.0      # a video needs this much distinctive vocabulary to be filed
MIN_LABELS = 3       # a child needs this many labelled reads to learn from

slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]
words = lambda s: [w for w in re.findall(r"[a-z0-9']{3,}", (s or "").lower()) if has_content(w)]


def assign_reads(children, reads, k):
    """One call: which child does each cached read belong to?"""
    schema = {"type": "object", "properties": {"assignments": {"type": "array", "items": {"type": "object",
              "properties": {"videoId": {"type": "string"}, "child": {"type": "string", "description": "One of the child names exactly, or NONE"}},
              "required": ["videoId", "child"]}}}, "required": ["assignments"]}
    lines = [f"[{r['videoId']}] {r['title'][:90]} — argues: {r['read'].get('one_line', '')[:160]}" for r in reads]
    prompt = ("These videos were filed under one name that turned out to hold several narratives:\n"
              + "\n".join(f"- {c}" for c in children)
              + "\n\nAssign each video to the ONE narrative it belongs to, by its name exactly, or NONE if it fits none. "
              "Use what the video argues, not its topic words.\n\n" + "\n".join(lines))
    r = ask(MODEL, [{"type": "text", "text": prompt}], schema, k)
    data = payload(r) or {}
    out = {}
    for a in data.get("assignments", []):
        if a.get("child") in children:
            out[a["videoId"]] = a["child"]
    return out


def vocab_for(children, labelled, reads_by_id):
    """Distinctive title terms per child, learned from its labelled reads and its name."""
    docs = {c: [] for c in children}
    for vid, c in labelled.items():
        r = reads_by_id.get(vid)
        if r:
            docs[c].append(" ".join(words(r["title"]) + words(r["read"].get("one_line", ""))))
    total = Counter()
    per = {}
    for c, ds in docs.items():
        cnt = Counter(w for d in ds for w in set(d.split()))
        per[c] = cnt
        total.update(cnt)
    vocab = {}
    for c in children:
        v = {w: 3.0 for w in words(c)}                         # the name is the strongest term
        n = max(len(docs[c]), 1)
        for w, k in per[c].items():
            share, elsewhere = k / n, (total[w] - k) / max(sum(len(d) for cc, d in docs.items() if cc != c), 1)
            if k >= 2 and share >= 3 * max(elsewhere, 0.02):
                v[w] = max(v.get(w, 0), min(2.0, share * 2))
        vocab[c] = v
    return vocab


def score(title, v):
    return sum(v.get(w, 0) for w in set(words(title)))


def main():
    if not BUCKET:
        sys.exit("Pass --bucket <narrative id> (one the reader filed split).")
    d = ROOT / "corpus" / BUCKET
    analysis = json.loads((d / "claim-analysis.json").read_text())
    # "split" is the gate's verdict; is_one_narrative false is the reader's own
    # judgement, which stands even when too few reads kept the status inconclusive.
    if analysis.get("status") != "split" and analysis.get("is_one_narrative") is not False:
        sys.exit(f"{BUCKET} is filed {analysis.get('status')} and read as one narrative. Nothing to split.")
    children = analysis["split_into"]
    stories = json.loads((ROOT / "stories.json").read_text())
    story = next((s for s in stories["stories"] if s.get("split_from") == BUCKET), None)
    if not story:
        sys.exit(f"No story in stories.json has split_from = {BUCKET}.")
    w = json.loads((ROOT / "watchlist.json").read_text())
    parent = next(t for t in w["topics"] if t["id"] == BUCKET)
    vids = json.loads((d / "videos.json").read_text())["videos"]
    cache = ROOT / ".cache" / "narrative-read" / BUCKET
    reads = [json.loads(p.read_text()) for p in sorted(cache.glob("*.json"))] if cache.exists() else []
    reads_by_id = {r["videoId"]: r for r in reads}
    print(f"{BUCKET}: {len(vids):,} videos · {len(reads)} cached reads · {len(children)} children")

    labelled = {}
    if reads and not NO_AI:
        try:
            labelled = assign_reads(children, reads, key())
            print(f"  reads assigned: {Counter(labelled.values())}")
        except DailyLimit:
            print("  out of Gemini requests today; falling back to name vocabulary only")
        except ApiError as e:
            print(f"  assignment failed ({e.code}); falling back to name vocabulary only")
    vocab = vocab_for(children, labelled, reads_by_id)

    filed, best_of = {c: [] for c in children}, Counter()
    for v in vids:
        scores = sorted(((score(v.get("title", ""), vocab[c]), c) for c in children), reverse=True)
        top, c = scores[0]
        if top >= MIN_SCORE and (len(scores) < 2 or top > scores[1][0] * 1.3):
            filed[c].append(v)
        else:
            best_of["unplaced"] += 1
    for c in children:
        print(f"  {len(filed[c]):6,}  {c}")
    print(f"  {best_of['unplaced']:6,}  left in the bucket (no clear home)")

    if not WRITE:
        print("\n(dry run — pass --write to create the children)")
        return
    stamp = time.strftime("%Y-%m-%d")
    for c in children:
        cid = f"{slug(c)}"
        cd = ROOT / "corpus" / cid
        cd.mkdir(exist_ok=True)
        (cd / "videos.json").write_text(json.dumps({"topic": cid, "updated": stamp, "source": f"split from {BUCKET}",
                                                     "videos": filed[c]}, indent=2, ensure_ascii=False) + "\n")
        if not (cd / "narrative.json").exists():
            (cd / "narrative.json").write_text(json.dumps({"name": c, "claim": c, "story": story["id"], "parent": BUCKET,
                                                            "status": "reading", "born": None, "mutations": [],
                                                            "note": "Skeleton from story_split.py; the reader fills born, turns and camps."},
                                                           indent=2, ensure_ascii=False) + "\n")
        if not any(t["id"] == cid for t in w["topics"]):
            w["topics"].append({"id": cid, "name": c, "industry": parent.get("industry"), "status": "forming",
                                "story": story["id"], "parent": BUCKET, "started": stamp,
                                "trigger": f"reader split of {BUCKET} on {analysis.get('read_on')}",
                                "queries": [c], "watched_predictors": [], "notes": "", "former_names": [],
                                "title_basis": "", "title_shape": "", "title_template": ""})
        if cid not in story["narratives"]:
            story["narratives"].append(cid)
    story["status"] = "reading"
    stories["updated"] = stamp
    (ROOT / "stories.json").write_text(json.dumps(stories, indent=1, ensure_ascii=False) + "\n")
    (ROOT / "watchlist.json").write_text(json.dumps(w, indent=1, ensure_ascii=False) + "\n")
    print(f"\nwrote {len(children)} children under story '{story['id']}'. Next: narrative_read.py --topic <child> for each.")


if __name__ == "__main__":
    main()
