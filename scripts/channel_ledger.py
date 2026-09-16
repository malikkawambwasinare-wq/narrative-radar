#!/usr/bin/env python3
"""Narrative Radar — the channel ledger: who gets crawled, and why.

    python3 scripts/channel_ledger.py                 # report
    python3 scripts/channel_ledger.py --write         # also write channels.json

Implements briefs/collection-engine/CHANNELS.md from the corpus we already hold,
so it costs no quota. Every channel we have ever collected gets a row, a tier, a
reason and a date.

  A — crawl and watch: recurs across time in our corpora
  B — screen next: some evidence, not yet enough to crawl
  C — counted, not crawled: one appearance, no recurrence. Its videos still
      count as evidence that a claim travelled
  D — rejected, with a reason (not assigned here; set by hand)

Tier A here is the corpus-evidence form of the admission test. The API form,
which reads a channel's own last 100 uploads, runs once the screening pass
exists; a channel admitted from corpus evidence is marked basis "corpus".

Ranking inside a tier follows the spec: originator lead, original share, camp
coverage, persistence, cadence. Reach is recorded and never ranks.
"""
import json, math, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
THIN_CAMP = 0.25          # a camp holding under a quarter of a claim's videos is under-collected


def published_ms(v):
    p = v.get("published") or ""
    if len(p) == 10 and p[4] == "-":
        try:
            return datetime.fromisoformat(p + "T00:00:00+00:00").timestamp() * 1000
        except ValueError:
            pass
    fs = v.get("first_seen")
    if not fs:
        return None
    try:
        t = datetime.fromisoformat(fs.replace("Z", "+00:00")).timestamp() * 1000
    except ValueError:
        return None
    return t - (v.get("age_days") or 0) * 86400000


def load():
    topics, claims = {}, {}
    for f in sorted((ROOT / "corpus").glob("*/videos.json")):
        tid = f.parent.name
        topics[tid] = json.loads(f.read_text())["videos"]
        cf = f.parent / "claims.json"
        if cf.exists():
            claims[tid] = json.loads(cf.read_text()).get("claims", [])
    wl = {t["id"]: t for t in json.loads((ROOT / "watchlist.json").read_text())["topics"]}
    return topics, claims, wl


def main():
    topics, claims, wl = load()

    # Camp membership per video, and which camps are thin inside their claim.
    camp_of, thin_camps = {}, set()
    for tid, cl in claims.items():
        for c in cl:
            camps = c.get("camps") or []
            total = sum(len(k.get("sources") or []) for k in camps) or 1
            for k in camps:
                srcs = k.get("sources") or []
                name = k.get("name") or k.get("label") or (k.get("position") or "")[:40]
                key = (tid, c.get("id"), name)
                if len(srcs) / total < THIN_CAMP:
                    thin_camps.add(key)
                for s in srcs:
                    camp_of.setdefault(s.get("videoId"), []).append(key)

    ch = defaultdict(lambda: {
        "videos": 0, "topics": defaultdict(int), "months": set(), "first": None, "last": None,
        "graded": 0, "original": 0, "pitch": 0, "early": 0, "camps": set(), "thin": 0, "yt": {},
    })
    # Earliest three videos per narrative: posting a claim before the rest is the
    # originator signal, and it is what dates a mutation.
    early_ids = set()
    for tid, vids in topics.items():
        dated = sorted(((published_ms(v), v) for v in vids if published_ms(v)), key=lambda x: x[0])
        early_ids |= {v["videoId"] for _, v in dated[:3]}

    for tid, vids in topics.items():
        for v in vids:
            name = (v.get("channel") or "?").strip()
            c = ch[name]
            t = published_ms(v)
            c["videos"] += 1
            c["topics"][tid] += 1
            if t:
                mo = datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%Y-%m")
                c["months"].add(mo)
                c["first"] = mo if not c["first"] else min(c["first"], mo)
                c["last"] = mo if not c["last"] else max(c["last"], mo)
            if v.get("verdict") and v["verdict"] not in ("UNREVIEWED", "UNKNOWN"):
                c["graded"] += 1
                if v["verdict"] == "ORIGINAL":
                    c["original"] += 1
            if (v.get("review") or {}).get("pitch"):
                c["pitch"] += 1
            if v["videoId"] in early_ids:
                c["early"] += 1
            for key in camp_of.get(v["videoId"], []):
                c["camps"].add(key)
                if key in thin_camps:
                    c["thin"] += 1
            yt = v.get("yt") or {}
            if yt.get("channelId") and not c["yt"]:
                c["yt"] = {k: yt.get(k) for k in
                           ("channelId", "handle", "subscribers", "channelVideos", "channelJoined",
                            "channelCountry", "verified")}

    rows = []
    for name, c in ch.items():
        months, vids = len(c["months"]), c["videos"]
        # Tier, from corpus evidence. Recurrence over time is the test, never reach.
        if vids >= 3 and months >= 3:
            tier, reason = "A", f"{vids} videos across {months} months in {len(c['topics'])} narrative(s)"
        elif vids >= 3 or (vids >= 2 and months >= 2) or len(c["topics"]) >= 2:
            tier, reason = "B", f"{vids} videos, {months} month(s) — screen its own uploads next"
        else:
            tier, reason = "C", "one appearance, no recurrence yet — counted as spread"
        score = (c["early"] * 6
                 + (c["original"] / c["graded"] * 5 if c["graded"] else 0)
                 + c["thin"] * 4
                 + months * 1.5
                 + min(vids, 20) * 0.5
                 - (c["pitch"] / vids * 3 if vids else 0))
        uploads = c["yt"].get("channelVideos")
        rows.append({
            "channel": name, "tier": tier, "reason": reason, "assessed": TODAY, "basis": "corpus",
            "score": round(score, 2), "videos": vids, "months": months,
            "span": f"{c['first']} → {c['last']}" if c["first"] else "",
            "narratives": sorted(c["topics"], key=c["topics"].get, reverse=True),
            "graded": c["graded"], "original": c["original"],
            "originator_lead": c["early"], "thin_camp_videos": c["thin"],
            "pitch": c["pitch"],
            "channelId": c["yt"].get("channelId"), "handle": c["yt"].get("handle"),
            "subscribers": c["yt"].get("subscribers"), "uploads_total": uploads,
            "crawl_units": math.ceil(min(uploads or 500, 20000) / 50),
        })

    rows.sort(key=lambda r: (r["tier"], -r["score"]))
    by = defaultdict(list)
    for r in rows:
        by[r["tier"]].append(r)

    a_units = sum(r["crawl_units"] for r in by["A"])
    b_units = 3 * len(by["B"])
    print(f"{len(rows)} channels · A {len(by['A'])} · B {len(by['B'])} · C {len(by['C'])}")
    print(f"backfill of tier A: {a_units:,} quota units ({a_units / 10000:.1f} days) · "
          f"screening tier B: {b_units:,} units ({b_units / 10000:.1f} days)\n")
    for tier in ("A", "B"):
        print(f"— tier {tier}, top by what it adds —")
        for r in by[tier][:12]:
            flags = " ".join(filter(None, [
                f"lead×{r['originator_lead']}" if r["originator_lead"] else "",
                f"orig {r['original']}/{r['graded']}" if r["graded"] else "",
                f"thin-camp×{r['thin_camp_videos']}" if r["thin_camp_videos"] else "",
                f"pitch×{r['pitch']}" if r["pitch"] else "",
            ]))
            print(f"  {r['channel'][:30]:32}{r['score']:>6}  {r['videos']:>3}v {r['months']:>3}mo  "
                  f"{r['span']:>18}  {flags}")
        print()

    if WRITE:
        out = ROOT / "channels.json"
        out.write_text(json.dumps({
            "generated": TODAY,
            "method": "briefs/collection-engine/CHANNELS.md, corpus evidence only, no API calls",
            "tiers": {"A": "crawl and watch", "B": "screen next", "C": "counted, not crawled"},
            "channels": rows,
        }, indent=1) + "\n")
        print(f"wrote {out.name}: {len(rows)} channels")


if __name__ == "__main__":
    main()
