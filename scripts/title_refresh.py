#!/usr/bin/env python3
"""Narrative Radar — keep the numbers in every title true, automatically.

    python3 scripts/title_refresh.py            # show what would change
    python3 scripts/title_refresh.py --write    # rewrite the titles

A title built on a count is a promise that the count is current. Every crawl
breaks that promise: one tier B run added 12,420 videos and eight titles went
stale in a single morning. Hand-editing them does not scale, so a title is
stored as a TEMPLATE bound to live quantities and re-rendered from the corpus.

    "{channels} Channels Say Your Gut Explains Everything"
    → "77 Channels Say Your Gut Explains Everything"

Placeholders, all derived from the corpus at render time:

    {videos}          videos filed under the narrative
    {channels}        distinct channels
    {graded}          videos carrying a verdict
    {pitch}           graded videos selling something
    {ledger}          dated claims on the prediction ledger
    {ledger_resolved} those whose deadline has passed
    {ledger_pending}  those still on the clock
    {named:2026}      titles naming that year as the year it happens

Wording never changes here — only numbers. A change of wording is an editorial
act and goes through the naming convention (briefs/narratives/SYSTEM.md §3),
which is why a pure number refresh does not touch former_names.
"""
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv


def facts(tid):
    try:
        vids = json.loads((ROOT / "corpus" / tid / "videos.json").read_text())["videos"]
    except Exception:
        return None
    named = Counter()
    for v in vids:
        for y in re.findall(r"\b(20[2-3]\d)\b", v.get("title") or ""):
            named[y] += 1
    graded = [v for v in vids if v.get("verdict") and v["verdict"] != "UNREVIEWED"]
    led = []
    lf = ROOT / "corpus" / tid / "predictions.json"
    if lf.exists():
        led = json.loads(lf.read_text()).get("entries", [])
    return {
        "videos": len(vids),
        "channels": len({v.get("channel") for v in vids}),
        "graded": len(graded),
        "pitch": sum(1 for v in vids if (v.get("review") or {}).get("pitch")),
        "ledger": len(led),
        "ledger_resolved": sum(1 for e in led if e.get("status") in ("SUPPORTED", "REFUTED", "AMBIGUOUS", "UPDATED")),
        "ledger_pending": sum(1 for e in led if e.get("status") == "PENDING"),
        "named": named,
    }


def render(template, f):
    def sub(m):
        key = m.group(1)
        if key.startswith("named:"):
            return f"{f['named'].get(key.split(':')[1], 0):,}"
        return f"{f.get(key, 0):,}"
    return re.sub(r"\{([a-z_]+(?::\d{4})?)\}", sub, template)


def main():
    w = json.loads((ROOT / "watchlist.json").read_text())
    changed = 0
    for t in w["topics"]:
        tpl = t.get("title_template")
        if not tpl:
            print(f"  —      {t['name'][:58]}   (no template: wording only, nothing to refresh)")
            continue
        f = facts(t["id"])
        if not f:
            continue
        new = render(tpl, f)
        if new == t["name"]:
            print(f"  ok     {new}")
            continue
        print(f"  UPDATE {t['name']}\n         → {new}")
        t["name"] = new
        changed += 1
    if changed and WRITE:
        (ROOT / "watchlist.json").write_text(json.dumps(w, indent=1, ensure_ascii=False) + "\n")
    print(f"\n{changed} title{'' if changed == 1 else 's'} refreshed{'' if WRITE else ' (dry run)'}")


if __name__ == "__main__":
    main()
