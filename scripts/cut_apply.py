#!/usr/bin/env python3
"""Apply the cut check's corrections to an evening.

    python3 scripts/cut_apply.py <page.html> <series-id> [--write]

Only a check made against the cut as it stands now is used. A correction is
taken when it is small enough to be the same point (within 45 s of the old
time) and leaves a real clip. Prints every change with the line it now starts
or ends on; without --write it only shows what it would do.
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
mm = lambda s: f"{s // 60}:{s % 60:02d}"


def t(x):
    try:
        p = [int(v) for v in str(x).strip().split(":")]
        return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]
    except Exception:
        return None


def main():
    page, sid, write = Path(sys.argv[1]), sys.argv[2], "--write" in sys.argv
    s = page.read_text(); i = s.find('{"id": "%s"' % sid)
    obj, end = json.JSONDecoder().raw_decode(s, i)
    n = stale = 0; off = []
    for e in obj["eps"]:
        for v in e["videos"]:
            L = t(v["length"]); a, b = v.get("start", 0), v.get("end") or L
            f = ROOT / "watch" / "cuts" / sid / f"{v['id']}_{a}.json"
            if not f.exists():
                f = ROOT / "watch" / "cuts" / sid / f"{v['id']}.json"
            if not f.exists():
                print(f"  not checked   {v['channel'][:20]}"); stale += 1; continue
            d = json.loads(f.read_text()); c = d["check"]
            if d["cut"] != [a, b]:
                print(f"  check is for an older cut   {v['channel'][:20]}"); stale += 1; continue
            if c.get("on_subject") in ("no", "partly"):
                off.append((c["on_subject"], v.get("name") or v["title"][:60], v["channel"]))
            na, nb = a, b
            if not c["start_clean"]:
                x = t(c["better_start"])
                if x is not None and abs(x - a) <= 45: na = x
            if not c["end_clean"]:
                x = t(c["better_end"])
                if x is not None and abs(x - b) <= 45: nb = min(L, x)
            if nb - na < 15:
                print(f"  SKIPPED (would leave {nb - na}s)   {v['channel'][:20]}"); continue
            if (na, nb) != (a, b):
                n += 1
                print(f"  {v['channel'][:18]:18} {mm(a)}-{mm(b)} -> {mm(na)}-{mm(nb)}")
                if na != a: print(f"       opens: {c['first_words'][:90]}" if c['start_clean'] else f"       opens at {mm(na)}")
                if nb != b: print(f"       closes: {c['better_end_line'][:100]}")
                v["start"] = na
                if L - nb < 3: v.pop("end", None)
                else: v["end"] = nb
    for kind, name, ch in off:
        print(f"  ** OFF SUBJECT ({kind}): {name} [{ch}] — remove it, or move it to the story it belongs to")
    print(f"{sid}: {n} cuts corrected, {stale} not yet checked")
    if write:
        page.write_text(s[:i] + json.dumps(obj, ensure_ascii=False) + s[end:])


if __name__ == "__main__":
    main()
