#!/usr/bin/env python3
"""Narrative Radar — keep every hook title true as the corpus grows.

    python3 scripts/title_check.py            # check them
    python3 scripts/title_check.py --strict   # exit non-zero if any fails

A title built on a number goes stale the moment the number moves. "566 Videos
Called the 2023 Crash" is a finding today and a lie in a month if the count
changes and nobody looks. So the numbers in every title are re-derived from the
corpus on each run, and a title whose figures have drifted is reported for
rewriting.

It also enforces the shape rules, which are easy to state and easy to forget:

  ≤ 60 characters · no em dash · no fear word beside an urgency word · not
  shouty · no colon followed by a coy question · a number in the title must
  exist in the corpus · a year in the title must be one the corpus knows.

Shapes, in order of preference (briefs/narratives/SYSTEM.md §3):
  tally  — a count that lands            "Nearly 1 in 3 Videos Sells Something"
  clock  — a date that moved, or passed  "7 Collapse Deadlines Have Passed"
  split  — how the sides divide          "43 Channels Say Your Gut Explains Everything"
  scale  — the sheer volume being pushed "1,541 Videos, 155 Channels"
  question — only where nothing is provable yet
"""
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRICT = "--strict" in sys.argv
MAX_LEN = 60
DRIFT = 0.15            # a stated count may drift this far before it needs a rewrite

CRISIS = re.compile(r"\b(warn\w*|collaps\w*|crash\w*|bubble|burst|crisis|shock\w*|panic|survive|protect|"
                    r"final|massive|expos\w*|hidden|doom|toxic|poison\w*|kill\w*|destroy\w*|danger\w*|"
                    r"deadly|worst|secret|lie(?:s|d)?)\b", re.I)
URGENT = re.compile(r"\b(just|now|already|about to|soon|immediately|urgent\w*|today|right now|"
                    r"before it'?s too late|stop)\b", re.I)


def facts(tid):
    """What the corpus can actually prove about this narrative right now."""
    try:
        vids = json.loads((ROOT / "corpus" / tid / "videos.json").read_text())["videos"]
    except Exception:
        return None
    named = Counter()
    for v in vids:
        for y in re.findall(r"\b(20[2-3]\d)\b", v.get("title") or ""):
            named[y] += 1
    graded = [v for v in vids if v.get("verdict") and v["verdict"] != "UNREVIEWED"]
    # The prediction ledger is a source of title numbers too: "14 deadlines on
    # the clock", "7 have passed". Without it the checker calls a true number false.
    led, resolved = [], 0
    lf = ROOT / "corpus" / tid / "predictions.json"
    if lf.exists():
        led = json.loads(lf.read_text()).get("entries", [])
        resolved = sum(1 for e in led if e.get("status") in ("SUPPORTED", "REFUTED", "AMBIGUOUS", "UPDATED"))
    return {
        "ledger": len(led), "ledger_resolved": resolved,
        "ledger_pending": sum(1 for e in led if e.get("status") == "PENDING"),
        "videos": len(vids),
        "channels": len({v.get("channel") for v in vids}),
        "graded": len(graded),
        "pitch": sum(1 for v in vids if (v.get("review") or {}).get("pitch")),
        "years_named": named,
        "years_seen": {(v.get("published") or "")[:4] for v in vids if (v.get("published") or "")[:4].isdigit()},
    }


def main():
    topics = json.loads((ROOT / "watchlist.json").read_text())["topics"]
    problems = 0
    for t in topics:
        title, tid = t.get("name", ""), t["id"]
        f = facts(tid)
        bad = []
        if len(title) > MAX_LEN:
            bad.append(f"{len(title)} characters, over {MAX_LEN}")
        if "—" in title or "–" in title:
            bad.append("em dash: a title is one line, not a line with a tail")
        if CRISIS.search(title) and URGENT.search(title):
            bad.append("a fear word beside an urgency word — the pattern we flag on other people's videos")
        if len([w for w in re.findall(r"[A-Za-z]{3,}", title) if w.isupper()]) >= 3:
            bad.append("shouty")
        if re.search(r":.*\?$", title):
            bad.append("colon then a question: the formula that says nothing")
        if not t.get("title_basis"):
            bad.append("no title_basis recorded, so the claim in the title cannot be checked")

        if f:
            # Every number in the title has to be a number the corpus still shows.
            for num in {int(n.replace(",", "")) for n in re.findall(r"\b\d[\d,]{1,6}\b", title)}:
                if 1900 < num < 2100:                       # that is a year, checked below
                    continue
                near = [v for v in (f["videos"], f["channels"], f["graded"], f["pitch"],
                                    f["ledger"], f["ledger_resolved"], f["ledger_pending"],
                                    *f["years_named"].values()) if v]
                if not any(abs(num - v) <= max(1, v * DRIFT) for v in near):
                    bad.append(f"the number {num:,} matches nothing in the corpus any more")
            for y in {int(y) for y in re.findall(r"\b(20[0-3]\d)\b", title)}:
                if str(y) not in f["years_seen"] and not f["years_named"].get(str(y)) and y > 2015:
                    bad.append(f"the year {y} appears in no video we hold")

        mark = "ok  " if not bad else "FAIL"
        print(f"{mark} {t.get('title_shape', '—'):9} {title}")
        for b in bad:
            print(f"       ↳ {b}")
        problems += len(bad)
    print(f"\n{len(topics)} titles · {problems} problem{'' if problems == 1 else 's'}")
    if problems and STRICT:
        sys.exit(1)


if __name__ == "__main__":
    main()
