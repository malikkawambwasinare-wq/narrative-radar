#!/usr/bin/env python3
"""Story Evenings: keep tracked narratives up to date.

    python3 scripts/track.py            # every narrative in tracking/narratives.json
    python3 scripts/track.py hormuz-oil # just one

Once a day (the Track workflow) this searches YouTube for videos published since
the last run on each tracked narrative, keeps the ones whose title really is
about it, and adds them to tracking/<id>.json with the date they were found.
The page reads those files; whether a new video joins the narrative by itself
or waits for the viewer's yes is the viewer's choice, kept on their device.

Cost: one search (100 units) per query plus one details call per 50 videos.
Eight narratives with eleven queries is about 1,150 of the 10,000 daily units.
"""
import json, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from director import Quota, details, search, usable  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "tracking"
NOW = datetime.now(timezone.utc)
KEEP = 300   # videos kept per narrative, newest first

# Channels that re-upload other people's interviews under bait titles. The
# original is almost always findable; these never are the source.
REUPLOADS = re.compile(r"^(investor tv|crypto nutshell|everyday finance|savvy finance|joe blow|joegoatstory|comedy shorts|joe rogan hype|"
                       r"the rogan experience vau|jre vibes|podcast cringe|walk show|harjeetius takes|muhammad sudais studio|thepodbaydoors)", re.I)


def words(term):
    return re.compile(r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])")


def matches(n, title):
    t = title.lower()
    return all(any(words(term).search(t) for term in group) for group in n["match"])


def run(n, backfill_days, quota):
    f = DIR / f"{n['id']}.json"
    cur = json.loads(f.read_text()) if f.exists() else {"videos": []}
    have = {v["id"]: v for v in cur["videos"]}
    since = datetime.fromisoformat(cur["checked"]) - timedelta(hours=6) if cur.get("checked") else NOW - timedelta(days=backfill_days)
    ids = []
    for q in n["queries"]:
        ids += search(q, quota, after=since, order="date", why=n["name"])
    fresh = [i for i in dict.fromkeys(ids) if i not in have]
    added = 0
    for v in details(fresh, quota).values():
        if not usable(v) or REUPLOADS.search(v["channel"]) or not matches(n, v["title"]):
            continue
        have[v["id"]] = {k: v[k] for k in ("id", "title", "channel", "published", "length")} | {"found": NOW.strftime("%Y-%m-%dT%H:%M:%SZ")}
        added += 1
    vids = sorted(have.values(), key=lambda v: (v["published"], v["found"]), reverse=True)[:KEEP]
    out = {"id": n["id"], "name": n["name"], "line": n["line"], "cat": n.get("cat", ""), "checked": NOW.isoformat(), "videos": vids}
    f.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{n['name']}: {added} new · {len(vids)} tracked", flush=True)
    return out, added


def main():
    cfg = json.loads((DIR / "narratives.json").read_text())
    only = sys.argv[1:]
    quota = Quota(40)
    index = []
    for n in cfg["narratives"]:
        if only and n["id"] not in only:
            f = DIR / f"{n['id']}.json"
            out, added = (json.loads(f.read_text()), 0) if f.exists() else run(n, cfg["backfill_days"], quota)
        else:
            out, added = run(n, cfg["backfill_days"], quota)
        day = (NOW - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        index.append({"id": n["id"], "name": n["name"], "line": n["line"], "cat": n.get("cat", ""), "count": len(out["videos"]),
                      "new_today": sum(1 for v in out["videos"] if v["found"] >= day), "latest": out["videos"][0]["published"] if out["videos"] else "",
                      "faces": list(dict.fromkeys(v["channel"] for v in out["videos"]))[:4]})
    (DIR / "index.json").write_text(json.dumps({"updated": NOW.isoformat(), "narratives": index}, indent=1, ensure_ascii=False) + "\n")
    print(f"done · {quota.units} quota units")


if __name__ == "__main__":
    main()
