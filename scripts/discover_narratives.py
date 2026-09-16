#!/usr/bin/env python3
"""Narrative Radar — find narrative candidates in collected videos, from titles alone.

    python3 scripts/discover_narratives.py                  # report
    python3 scripts/discover_narratives.py --write          # also write discovered.json

Why titles only
  Transcripts are the gate on grading, not on discovery. A narrative announces
  itself in how a claim is worded across many channels over months, and that is
  visible in titles and descriptions, which the API serves. So discovery can run
  at harvest scale today and grading can follow later.

The test (briefs/narratives/SYSTEM.md §1, briefs/collection-engine/CHANNELS.md)
  A phrase becomes a narrative candidate when it appears in videos from at least
  3 INDEPENDENT channels across at least 2 DISTINCT months, and the wording
  carries a claim rather than a subject. Phrases that simply restate a narrative
  we already track are reported as sub-claims of it, never as new narratives.

Output per candidate: the phrase, how many videos and channels carry it, the
month span, the industry it sits under, and example titles as evidence.
"""
import json, re, sys, unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv
MIN_CHANNELS, MIN_MONTHS, MIN_VIDEOS = 3, 2, 4
MAX_DF = 0.05          # a phrase needs one word used in 5% of titles or fewer
NGRAM = (2, 4)

STOP = set("""a an the and or but if then than that this these those of in on at to for from by with without
about into over after before under again further once here there all any both each few more most other some such
no nor not only own same so too very can will just should now what why how when who whom which is are was were be
been being do does did doing have has had having i you he she it we they them his her its our your their my me
new best top vs video watch full episode part live today tomorrow yesterday week month year years ep podcast
subscribe channel please like comment share""".split())

# A claim is a statement about the world that could be wrong. These markers are
# how claims announce themselves in a title; a title with none of them is
# usually a subject, a reaction or a tutorial.
CLAIM_MARK = re.compile(r"""\b(
 will|won'?t|going\ to|about\ to|coming|next\ year|by\ 20\d\d|soon|imminent|
 is|are|isn'?t|aren'?t|was|were|has|have|
 causes?|caused|cause|drives?|proves?|proven|shows?|means?|explains?|
 crash(?:es|ing)?|collaps(?:e|es|ing)|boom|bubble|burst|end(?:s|ing|ed)?|dead|dying|over|
 bans?|banned|wins?|beats?|replac(?:e|es|ing)|kills?|saves?|fix(?:es)?|
 should|must|why|truth|really|actually|myth|lie|scam|hoax
)\b""", re.X | re.I)

MONTH = lambda t: datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%Y-%m")


def published_ms(v):
    p = v.get("published") or ""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p):
        return datetime.fromisoformat(p + "+00:00").timestamp() * 1000
    fs = v.get("first_seen")
    if not fs:
        return None
    try:
        t = datetime.fromisoformat(fs.replace("Z", "+00:00")).timestamp() * 1000
    except ValueError:
        return None
    return t - (v.get("age_days") or 0) * 86400000


def words(title):
    s = unicodedata.normalize("NFKD", title or "").lower()
    s = re.sub(r"[^a-z0-9'\s-]", " ", s)
    return [w for w in s.split() if len(w) > 2 and w not in STOP]


def phrases(title):
    ws = words(title)
    out = set()
    for n in range(NGRAM[0], NGRAM[1] + 1):
        for i in range(len(ws) - n + 1):
            out.add(" ".join(ws[i:i + n]))
    return out


def load():
    vids = []
    for p in sorted((ROOT / "corpus").glob("*/videos.json")):
        topic = p.parent.name
        for v in json.loads(p.read_text())["videos"]:
            t = published_ms(v)
            if not t:
                continue
            v["_topic"], v["_month"] = topic, MONTH(t)
            vids.append(v)
    wl = json.loads((ROOT / "watchlist.json").read_text())["topics"]
    inds = json.loads((ROOT / "industries.json").read_text())["industries"]
    return vids, wl, inds


def main():
    vids, wl, inds = load()
    industry_of = {t["id"]: t.get("industry", "Unsorted") for t in wl}
    tracked = {t["id"]: set(w for q in t.get("queries", []) for w in words(q)) for t in wl}

    # Document frequency: a phrase built only from words everybody uses ("market
    # crash", "coming soon") is claim vocabulary, not a narrative. At least one
    # word has to be distinctive, or the phrase names a subject nobody can act on.
    df = defaultdict(int)
    for v in vids:
        for w in set(words(v.get("title") or "")):
            df[w] += 1
    N = max(1, len(vids))
    distinctive = lambda ph: any(df[w] / N <= MAX_DF for w in ph.split() if not CLAIM_MARK.fullmatch(w))

    hits = defaultdict(lambda: {"v": [], "ch": set(), "mo": set(), "tp": defaultdict(int)})
    for v in vids:
        if not CLAIM_MARK.search(v.get("title") or ""):
            continue
        for ph in phrases(v["title"]):
            h = hits[ph]
            h["v"].append(v); h["ch"].add(v.get("channel") or "?"); h["mo"].add(v["_month"])
            h["tp"][v["_topic"]] += 1

    cands = []
    for ph, h in hits.items():
        if len(h["v"]) < MIN_VIDEOS or len(h["ch"]) < MIN_CHANNELS or len(h["mo"]) < MIN_MONTHS:
            continue
        if not CLAIM_MARK.search(ph) or not distinctive(ph):
            continue
        top = max(h["tp"], key=h["tp"].get)
        share = h["tp"][top] / len(h["v"])
        pw = set(ph.split())
        overlap = len(pw & tracked.get(top, set())) / max(1, len(pw))
        cands.append({
            "phrase": ph, "videos": len(h["v"]), "channels": len(h["ch"]),
            "months": len(h["mo"]), "span": f"{min(h['mo'])} → {max(h['mo'])}",
            "industry": industry_of.get(top, "Unsorted"),
            "home": top, "home_share": round(share, 2),
            "kind": "sub-claim" if (share >= 0.8 and overlap >= 0.5) else
                    ("cross-narrative" if share < 0.6 else "new candidate"),
            "examples": [x["title"] for x in sorted(h["v"], key=lambda x: x["_month"])[:3]],
            "ids": sorted({x["videoId"] for x in h["v"]}),
        })

    # Cluster: phrases carried by the same videos are one candidate. The longest
    # phrase names it, and its evidence is the union.
    cands.sort(key=lambda c: (-c["videos"], -len(c["phrase"])))
    kept = []
    for c in cands:
        ids = set(c["ids"])
        home = next((k for k in kept if len(ids & set(k["ids"])) / max(1, min(len(ids), len(k["ids"]))) >= 0.5), None)
        if home:
            home.setdefault("also", []).append(c["phrase"])
            if len(c["phrase"]) > len(home["phrase"]) and c["videos"] >= home["videos"] * 0.8:
                home["phrase"], c["phrase"] = c["phrase"], home["phrase"]
            continue
        kept.append(c)

    claimy = sum(1 for v in vids if CLAIM_MARK.search(v.get("title") or ""))
    print(f"{len(vids)} videos · {claimy} carry claim wording")
    print(f"{len(kept)} candidates pass: {MIN_VIDEOS}+ videos, {MIN_CHANNELS}+ channels, {MIN_MONTHS}+ months, distinctive wording\n")
    for kind in ("new candidate", "cross-narrative", "sub-claim"):
        rows = [c for c in kept if c["kind"] == kind]
        if not rows:
            continue
        print(f"— {kind} ({len(rows)}) —")
        for c in rows[:12]:
            print(f"  {c['phrase'][:40]:42}{c['videos']:>4}v {c['channels']:>3}ch {c['months']:>3}mo  {c['span']}  {c['industry'][:17]}")
            print(f"      e.g. {c['examples'][0][:86]}")
        print()

    if WRITE:
        out = ROOT / "discovered.json"
        out.write_text(json.dumps({
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "method": "titles only; 4+ videos, 3+ independent channels, 2+ distinct months, claim wording in the phrase",
            "candidates": kept,
        }, indent=1) + "\n")
        print(f"wrote {out.name}: {len(kept)} candidates")


if __name__ == "__main__":
    main()
