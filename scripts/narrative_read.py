#!/usr/bin/env python3
"""Narrative Radar — what claim do the videos in a narrative actually converge on?

    python3 scripts/narrative_read.py --topic housing-crash-watch --n 24
    python3 scripts/narrative_read.py --all --n 24 --write
    python3 scripts/narrative_read.py --topic housing-crash-watch --synthesize-only
    python3 scripts/narrative_read.py --topic the-2026-setup --write --apply   # fill turns and camps where the corpus has none

Two passes.

  1. Read a stratified sample of the narrative's videos with Gemini and take the
     claims each one asserts.
  2. Hand all those claims back and ask what they converge on — the one claim
     the narrative is really making, its variants, and what it is not about.

Why a sample and not the corpus
  Reading 72,437 videos costs about $2,276 and answers a question nobody asked.
  A narrative's claim is a property of the narrative, not of each video, so 24
  well-spread videos establish it for roughly a dollar. The corpus stays the
  evidence; the sample is how we learn what to look for in it.

Why the sample is stratified
  "The videos in this narrative focus on this claim" is a measurement, and it is
  only as honest as the draw. Sorting by views would measure what YouTube
  promotes. So the sample takes at most two videos per channel and spreads them
  across the months the narrative spans, which is the same discipline the
  channel ledger uses (briefs/collection-engine/AUDIT.md).

Why it can refuse to answer
  A claim of convergence needs enough reads to mean anything. Under MIN_READS
  videos, or under MIN_SHARE agreement, the result is filed inconclusive rather
  than dressed up. An engine that always finds a pattern is not measuring one.

What it writes
  .cache/narrative-read/<topic>/<videoId>.json   per-video claims (gitignored —
                                                 derived third-party text is local)
  corpus/<topic>/claim-analysis.json             the synthesis, which is ours
"""
import json, random, sys, time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gemini import (ROOT, ApiError, Budget, DailyLimit, ask, key, payload, spend, video_tokens)

CACHE = ROOT / ".cache" / "narrative-read"
MIN_READS = 12      # below this, convergence is anecdote
MIN_SHARE = 0.40    # below this, the narrative has no centre worth naming
PER_CHANNEL = 2     # no channel may dominate the sample

WRITE = "--write" in sys.argv
SYNTH_ONLY = "--synthesize-only" in sys.argv
ALL = "--all" in sys.argv
APPLY = "--apply" in sys.argv     # fill narrative.json / claims.json where they are empty; never overwrite


def flag(name, default):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


N = int(flag("--n", 24))
ONLY = flag("--topic", None)
# Each model carries its own free-tier request-per-day allowance, so a run that
# has exhausted one can often still finish on another.
MODEL = flag("--model", "gemini-3.8-flash")

# ---------------------------------------------------------------- pass one

CLAIM_SCHEMA = {
    "type": "object",
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The claim as a flat proposition"},
                    "timestamp": {"type": "string", "description": "MM:SS where the speaker says it"},
                    "is_the_channels_own": {"type": "boolean", "description": "True if the channel asserts it, false if they are reporting what someone else said"},
                    "hedged": {"type": "boolean"},
                    "is_prediction": {"type": "boolean"},
                    "deadline": {"type": "string", "description": "Only if the speaker states or clearly implies one. Empty otherwise. Never infer a date from context."},
                    "deadline_stated_aloud": {"type": "boolean", "description": "True only if the speaker actually says the timeframe"},
                },
                "required": ["text", "timestamp", "is_the_channels_own", "hedged", "is_prediction"],
            },
        },
        "sells_something": {"type": "boolean"},
        "one_line": {"type": "string", "description": "What this video argues, in one sentence"},
    },
    "required": ["claims", "sells_something", "one_line"],
}

CLAIM_PROMPT = """Extract the claims this video makes.

A claim is an assertion that could later turn out to be true or false. What we
want is what THIS CHANNEL is arguing, so:

- Set is_the_channels_own false for background they are merely reporting
  ("Biden nominated Powell", "Musk co-founded OpenAI in 2015"). Include it, but
  mark it, because it is context and not their position.
- Set is_the_channels_own true for what they assert, predict, or push.
- Skip greetings, sponsor reads and calls to subscribe.

On deadlines, be strict. Give a deadline ONLY if the speaker states or clearly
implies a timeframe out loud, and set deadline_stated_aloud accordingly. Do not
date a claim from the video's context, the publication date, or your own
knowledge. A wrong date is worse to us than no date.

A video that asserts nothing checkable returns an empty claims list. That is a
valid answer."""


def when(v):
    """A sortable date for every video.

    71 records still carry a relative date ("2 weeks ago") from the scraper era.
    Left alone they each became their own bucket, which pushed an entire sample
    into the two oldest years. first_seen minus age_days recovers the real one."""
    p = v.get("published") or ""
    if len(p) == 10 and p[4] == "-" and p[7] == "-":
        return p
    seen, age = v.get("first_seen"), v.get("age_days")
    if seen and age is not None:
        try:
            t = time.mktime(time.strptime(seen, "%Y-%m-%d")) - float(age) * 86400
            return time.strftime("%Y-%m-%d", time.localtime(t))
        except Exception:
            pass
    return seen or ""


def sample(topic, n):
    """n videos spread evenly across the narrative's whole life.

    Slicing the corpus into n equal-sized windows by date and drawing one from
    each gives the same weight to a quiet year as a loud one, which is what the
    question needs: does this claim hold across the span, or only in the months
    the topic was hot? A draw weighted by volume, or by views, would answer a
    different question — what YouTube pushed."""
    f = ROOT / "corpus" / topic / "videos.json"
    if not f.exists():
        return []
    vids = [v for v in json.loads(f.read_text())["videos"]
            if v.get("title") and v.get("url") and not v.get("unavailable")]
    vids = [v for v in vids if when(v)]
    if not vids:
        return []
    vids.sort(key=when)
    picked, seen = [], Counter()
    size = max(len(vids) // n, 1)
    for i in range(min(n, len(vids))):
        window = vids[i * size: (i + 1) * size] if i < n - 1 else vids[i * size:]
        random.shuffle(window)
        for v in window:
            ch = v.get("channel")
            if seen[ch] >= PER_CHANNEL:
                continue
            seen[ch] += 1
            picked.append(v)
            break
    return picked


def read_videos(topic, vids, k, budget):
    out_dir = CACHE / topic
    out_dir.mkdir(parents=True, exist_ok=True)
    reads, cost, skipped = [], 0.0, 0
    for i, v in enumerate(vids, 1):
        cached = out_dir / f"{v['videoId']}.json"
        if cached.exists():
            reads.append(json.loads(cached.read_text()))
            print(f"  [{i}/{len(vids)}] cached   {v['title'][:62]}")
            continue
        est = video_tokens(v.get("length"))
        if est and budget.too_big(est):
            print(f"  [{i}/{len(vids)}] too long {v.get('length')}  {v['title'][:52]}")
            skipped += 1
            continue
        print(f"  [{i}/{len(vids)}] reading  {v['title'][:62]}")
        try:
            r = ask(MODEL, [{"type": "text", "text": CLAIM_PROMPT},
                            {"type": "video", "uri": v["url"]}],
                    CLAIM_SCHEMA, k, budget=budget, est_tokens=est)
        except DailyLimit:
            print(f"      out of requests for today. {len(reads)} read and cached.")
            raise
        except ApiError as e:
            print(f"      skipped ({e.code}): {e.detail[:100]}")
            skipped += 1
            continue
        data = payload(r)
        if not data:
            print("      unparsed")
            skipped += 1
            continue
        cost += spend(r)
        rec = {"videoId": v["videoId"], "title": v["title"], "channel": v.get("channel"),
               "published": v.get("published"), "read": data}
        cached.write_text(json.dumps(rec, indent=1))
        reads.append(rec)
        own = sum(1 for c in data.get("claims", []) if c.get("is_the_channels_own"))
        print(f"      {own} of its own, {len(data.get('claims',[]))} total")
    return reads, cost, skipped


# ---------------------------------------------------------------- pass two

SYNTH_SCHEMA = {
    "type": "object",
    "properties": {
        "central_claim": {"type": "string", "description": "The one claim these videos converge on, as a flat proposition. No hedging, no rhetoric."},
        "videos_asserting_it": {"type": "integer", "description": "How many of the videos listed assert it, including in paraphrase"},
        "variants": {
            "type": "array",
            "description": "Distinct versions of the claim, strongest first",
            "items": {"type": "object", "properties": {
                "claim": {"type": "string"},
                "count": {"type": "integer"}}, "required": ["claim", "count"]},
        },
        "not_about": {"type": "string", "description": "What a reader might wrongly assume this narrative covers, but it does not"},
        "claim_name": {"type": "string", "description": "A short neutral name for the claim itself. Never a question, never a number, under 8 words."},
        "hook_candidates": {"type": "array", "items": {"type": "string"},
                            "description": "Two or three title options, under 60 characters, never a question, no em dash"},
        "disagreement": {"type": "string", "description": "Where the videos contradict each other, if they do"},
        "is_one_narrative": {"type": "boolean", "description": "False if these claims are really two or more separate narratives filed together"},
        "split_into": {"type": "array", "items": {"type": "string"},
                       "description": "If is_one_narrative is false, the narratives this should split into"},
        # The two things a set is built from. Origin sets slice the corpus by
        # the years in `turns`; debate sets need two `camps` each holding videos.
        "born": {"type": "string", "description": "The earliest year the claim appears in these videos, YYYY. Empty if the sample cannot say."},
        "turns": {
            "type": "array",
            "description": "The turns the story took as these videos show it, oldest first. Only turns visible in the listed videos.",
            "items": {"type": "object", "properties": {
                "date": {"type": "string", "description": "YYYY or YYYY-MM, taken from the video dates shown"},
                "mechanism": {"type": "string", "description": "What changed, under 12 words"},
                "videoIds": {"type": "array", "items": {"type": "string"},
                             "description": "Ids from the list that show this turn"}},
                "required": ["date", "mechanism", "videoIds"]},
        },
        "camps": {
            "type": "array",
            "description": "The sides that disagree about the central claim, strongest first. Two minimum, or leave empty.",
            "items": {"type": "object", "properties": {
                "position": {"type": "string", "description": "This side's position, under 10 words"},
                "watch_for": {"type": "string", "description": "The tell: what a viewer should notice when this side argues"},
                "videoIds": {"type": "array", "items": {"type": "string"},
                             "description": "Ids from the list whose channel argues this side"}},
                "required": ["position", "watch_for", "videoIds"]},
        },
    },
    "required": ["central_claim", "videos_asserting_it", "variants", "not_about",
                 "claim_name", "hook_candidates", "is_one_narrative", "born", "turns", "camps"],
}

SYNTH_PROMPT = """Below are the claims extracted from videos we have grouped into one narrative.

Tell us what they converge on.

- central_claim is the proposition these videos are really asserting, written flat
  and checkable. Not a topic ("housing"), not a mood ("fear about housing") — a
  claim that could be shown right or wrong.
- Count honestly. videos_asserting_it must not exceed the number of videos listed,
  and paraphrases count but unrelated claims do not.
- Weight the claims marked as the channel's own. Background they were reporting
  tells you what they covered, not what they believe.
- not_about matters as much as the claim. It is what keeps the narrative from
  swallowing everything adjacent to it.
- If these are really two or more different narratives that have been filed
  together, say so with is_one_narrative false and name the split. Do not force
  a centre onto claims that have none.

For claim_name and hook_candidates: name the claim, not the topic. Never a
question. No em dashes. Hooks stay under 60 characters. Do not invent numbers —
if you want a count in a hook, use only counts present in this data.

Then the two things an evening's set is built from:

- turns: the story's timeline as THESE videos show it. Each turn is a date
  (from the dates listed, YYYY or YYYY-MM) and what changed, oldest first, with
  the ids that show it. born is the earliest year the claim appears here. If
  the sample does not reach back to a turn, do not invent one.
- camps: the sides that disagree about the central claim. Each camp has a
  position, a watch_for (the tell a viewer should notice when this side
  argues), and the ids of videos whose CHANNEL argues that side. Two camps
  minimum to be worth listing; one side is not a disagreement, so return an
  empty list rather than a single camp. A video goes in one camp only.

Cite only ids from the list above, exactly as written. An id you did not see
is worse than none: it would put a video that does not exist into someone's
evening."""


def synthesize(topic, reads, k, budget):
    lines = []
    for r in reads:
        cs = r["read"].get("claims", [])
        own = [c for c in cs if c.get("is_the_channels_own")]
        if not own:
            own = cs[:2]
        lines.append(f"\n[{r['videoId']}] {r['title'][:90]}  ({r.get('published','')})")
        lines.append(f"  argues: {r['read'].get('one_line','')}")
        for c in own[:6]:
            tag = "prediction" if c.get("is_prediction") else "claim"
            dl = f" by {c['deadline']}" if c.get("deadline") and c.get("deadline_stated_aloud") else ""
            lines.append(f"  - [{tag}] {c['text']}{dl}")
    blob = "\n".join(lines)
    print(f"  synthesising from {len(reads)} videos ({len(blob):,} chars)")
    r = ask(MODEL, [{"type": "text", "text": SYNTH_PROMPT + "\n\n" + blob}],
            SYNTH_SCHEMA, k, budget=budget, est_tokens=len(blob) // 3)
    return payload(r), spend(r)


def sanitize(synth, reads):
    """Every videoId the model cites must be one it was shown.

    Models produce plausible ids that do not exist, and an invented id here
    would put a video that does not exist into someone's evening. So drop any
    id we did not send. A camp with no surviving videos is dropped too, since a
    debate set needs sources; a turn survives on its date and mechanism alone,
    because the origin set slices the corpus by year and does not need ids."""
    have = {r["videoId"] for r in reads}
    keep = lambda ids: [i for i in (ids or []) if i in have]
    camps = [dict(c, videoIds=keep(c.get("videoIds"))) for c in synth.get("camps") or []]
    synth["camps"] = [c for c in camps if c.get("position") and c["videoIds"]]
    if len(synth["camps"]) < 2:              # one side is not a disagreement
        synth["camps"] = []
    turns = [dict(t, videoIds=keep(t.get("videoIds"))) for t in synth.get("turns") or []]
    synth["turns"] = [t for t in turns if t.get("date") and t.get("mechanism")]
    return synth


def apply_to_corpus(topic, synth, n_read):
    """Fill narrative.json and claims.json only where they are empty.

    The stories with hand-built turns and camps keep them: this never
    overwrites, and everything it adds says where it came from, so a later
    reviewer can tell a read from a graded judgement."""
    d = ROOT / "corpus" / topic
    changed = []
    stamp = time.strftime("%Y-%m-%d")

    npath = d / "narrative.json"
    nar = json.loads(npath.read_text()) if npath.exists() else {}
    if not (nar.get("mutations") or []) and synth.get("turns"):
        nar["mutations"] = [{"date": t["date"], "mechanism": t["mechanism"], "source": "gemini-read"}
                            for t in synth["turns"]]
        nar["mutations_note"] = (f"Turns read by {MODEL} from a {n_read}-video sample on {stamp}; "
                                 f"evidence in claim-analysis.json.")
        if not nar.get("born") and synth.get("born"):
            nar["born"] = str(synth["born"])[:4]
        npath.write_text(json.dumps(nar, indent=2, ensure_ascii=False) + "\n")
        changed.append(f"narrative.json: {len(nar['mutations'])} turns"
                       + (f", born {nar['born']}" if nar.get("born") else ""))

    cpath = d / "claims.json"
    cl = json.loads(cpath.read_text()) if cpath.exists() else {"note": "", "claims": []}
    has_contest = any(len(c.get("camps") or []) >= 2 for c in cl.get("claims", []))
    camps = synth.get("camps") or []
    if not has_contest and len(camps) >= 2:
        cl.setdefault("claims", []).append({
            "id": f"gemini-{stamp.replace('-', '')}",
            "type": "contested",
            "statement": synth.get("central_claim", ""),
            "note": synth.get("disagreement", ""),
            "source": "gemini-read",
            "camps": [{"position": c["position"], "watch_for": c.get("watch_for", ""),
                       "sources": [{"videoId": v} for v in c["videoIds"]]} for c in camps],
            "sources": [],
        })
        cl["updated"] = stamp
        cpath.write_text(json.dumps(cl, indent=2, ensure_ascii=False) + "\n")
        changed.append(f"claims.json: 1 contested claim, {len(camps)} camps")

    for c in changed:
        print(f"  applied      {c}")
    if not changed:
        print("  applied      nothing: the corpus already has turns and camps, or the read gave none")


def verdict(synth, n_read):
    """Is this strong enough to publish as a finding?"""
    if n_read < MIN_READS:
        return "inconclusive", f"only {n_read} videos read, need {MIN_READS}"
    if not synth.get("is_one_narrative"):
        return "split", "these are separate narratives filed together"
    share = synth.get("videos_asserting_it", 0) / max(n_read, 1)
    if share < MIN_SHARE:
        return "inconclusive", f"only {synth.get('videos_asserting_it',0)} of {n_read} assert it"
    return "established", f"{synth.get('videos_asserting_it')} of {n_read} videos"


def run(topic, k, budget):
    print(f"\n=== {topic}")
    reads = []
    if SYNTH_ONLY:
        d = CACHE / topic
        reads = [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))] if d.exists() else []
        print(f"  {len(reads)} cached reads")
        cost = skipped = 0
    else:
        vids = sample(topic, N)
        if not vids:
            print("  no videos")
            return 0.0
        print(f"  sampled {len(vids)} of the corpus, at most {PER_CHANNEL} per channel")
        try:
            reads, cost, skipped = read_videos(topic, vids, k, budget)
        except DailyLimit:
            # The reads are on disk. Synthesising needs one more request we do
            # not have, so stop here rather than lose the run to a failed call.
            print(f"\n  Daily request limit reached. Reads are cached in"
                  f" {(CACHE / topic).relative_to(ROOT)}/")
            print(f"  Resume with:  python3 scripts/narrative_read.py --topic {topic} --n {N} --write")
            print(f"  Or synthesise what we have:  ... --topic {topic} --synthesize-only --write")
            raise
    if not reads:
        print("  nothing read")
        return cost if not SYNTH_ONLY else 0.0
    synth, scost = synthesize(topic, reads, k, budget)
    if not synth:
        print("  synthesis unparsed")
        return cost
    synth = sanitize(synth, reads)
    total = (cost or 0) + scost
    state, why = verdict(synth, len(reads))

    print(f"\n  CLAIM        {synth['central_claim']}")
    print(f"  status       {state} ({why})")
    print(f"  name         {synth['claim_name']}")
    for h in synth.get("hook_candidates", [])[:3]:
        print(f"  hook         {h}  [{len(h)} chars]")
    print(f"  not about    {synth.get('not_about','')}")
    if synth.get("disagreement"):
        print(f"  they differ  {synth['disagreement']}")
    if not synth.get("is_one_narrative"):
        print(f"  SPLIT INTO   {', '.join(synth.get('split_into', []))}")
    for v in synth.get("variants", [])[:4]:
        print(f"    {v['count']:>3}x  {v['claim'][:74]}")
    if synth.get("born"):
        print(f"  born         {synth['born']}")
    for t in synth.get("turns", [])[:6]:
        print(f"  turn {t['date']:>7}  {t['mechanism'][:58]}  ({len(t.get('videoIds', []))} videos)")
    for c in synth.get("camps", [])[:3]:
        print(f"  camp         {c['position'][:56]}  ({len(c['videoIds'])} videos)")
    print(f"  cost         ${total:.3f}")

    if WRITE:
        out = {
            "topic": topic,
            "read_on": time.strftime("%Y-%m-%d"),
            "model": MODEL,
            "videos_read": len(reads),
            "sampled_from": len(json.loads((ROOT / "corpus" / topic / "videos.json").read_text())["videos"]),
            "sampling": f"at most {PER_CHANNEL} per channel, spread across months",
            "status": state,
            "status_reason": why,
            **{k2: synth[k2] for k2 in synth},
            "evidence": [r["videoId"] for r in reads],
        }
        p = ROOT / "corpus" / topic / "claim-analysis.json"
        p.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        print(f"  wrote        {p.relative_to(ROOT)}")
        # Only an established read may fill the corpus. An inconclusive one, or
        # a group that is really two narratives, has no centre to build a set on.
        if APPLY and state == "established":
            apply_to_corpus(topic, synth, len(reads))
        elif APPLY:
            print(f"  applied      nothing: status is {state}, and only an established read may fill the corpus")
    return total


def main():
    random.seed(11)
    k = key()
    budget = Budget()
    topics = [t["id"] for t in json.loads((ROOT / "watchlist.json").read_text())["topics"]]
    if ONLY:
        topics = [ONLY] if ONLY in topics else sys.exit(f"Unknown topic. Have: {', '.join(topics)}")
    elif not ALL:
        sys.exit("Pass --topic <id> or --all. Topics:\n  " + "\n  ".join(topics))
    spent = 0.0
    for t in topics:
        try:
            spent += run(t, k, budget)
        except DailyLimit:
            print("\nOut of free-tier requests for today (20 per model per day).")
            print("Either wait for the reset, pass --model with another model, or")
            print("enable billing — the whole library is about $12 at measured rates.")
            break
        except ApiError as e:
            if e.code in (401, 403):
                sys.exit(f"\nKey rejected ({e.code}).")
            print(f"  stopped: {e}")
    print(f"\ntotal ${spent:.3f}" + ("" if WRITE else "   (dry run — pass --write to save)"))


if __name__ == "__main__":
    main()
