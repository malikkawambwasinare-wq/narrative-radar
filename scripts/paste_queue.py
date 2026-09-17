#!/usr/bin/env python3
"""Narrative Radar — turn pasted misses into collection work.

    python3 scripts/paste_queue.py                 # report
    python3 scripts/paste_queue.py --write         # queue the missed channels

Pastes are the demand signal. A link that lands in a narrative we hold is a hit.
A link that does not is a miss, and the channel it names is a channel real people
watch and we do not collect. Those channels enter the ledger as candidates, so
what gets collected next is decided by interest rather than by our heuristics.

Reads the engine's paste log (GET /api/paste-log) and writes the missed channels
into channel-candidates.json, which scripts/channel_ledger.py merges at tier B.
It also prints the hit rate, the number the collection plan turns on:

    above 75%   the library covers what people watch; stop growing it
    40 to 75%   keep collecting; the misses name what to add
    below 40%   collect only what pastes ask for
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = os.environ.get("NR_API", "https://lambent-salmiakki-6ea854.netlify.app")
WRITE = "--write" in sys.argv
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def main():
    try:
        with urllib.request.urlopen(f"{API}/api/paste-log", timeout=20) as r:
            log = json.loads(r.read().decode())
    except Exception as e:
        print(f"paste queue: the engine's paste log is unreachable ({e}).")
        print("  Nothing queued. The page keeps its own tally and flushes when the engine is back.")
        return

    rate = log.get("rate")
    verdict = ("no pastes yet" if not log.get("pastes") else
               "library covers what people watch" if rate and rate >= 0.75 else
               "keep collecting; the misses name what to add" if rate and rate >= 0.40 else
               "collect only what pastes ask for")
    print(f"paste log since {log.get('since') or '—'}: {log.get('pastes', 0)} pastes · "
          f"{log.get('hits', 0)} hits · {log.get('misses', 0)} misses · "
          f"hit rate {f'{rate * 100:.0f}%' if rate is not None else '—'} · {verdict}")

    missed = [m for m in log.get("missedChannels", []) if m.get("channelId")]
    if not missed:
        print("  no missed channels named yet")
        return

    f = ROOT / "channel-candidates.json"
    doc = json.loads(f.read_text()) if f.exists() else {"generated": TODAY, "channels": []}
    have = {c.get("channelId") for c in doc["channels"]}
    added = 0
    for m in missed:
        if m["channelId"] in have:
            continue
        doc["channels"].append({
            "channelId": m["channelId"], "channel": m.get("channel", ""),
            "found": TODAY, "found_by": f"pasted {m['pastes']}x and not held",
            "industry": "Unsorted", "basis": "paste",
        })
        added += 1
        print(f"  + {m.get('channel', '')[:40]:42} pasted {m['pastes']}x")
    doc["generated"] = TODAY
    if WRITE and added:
        f.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"+{added} channels queued for screening{'' if WRITE else ' (dry run)'}")


if __name__ == "__main__":
    main()
