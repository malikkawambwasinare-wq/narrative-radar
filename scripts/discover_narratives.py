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
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from channel_sweep import best_topic, corpus_titles, topic_vocab   # one definition of "belongs to this narrative"

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv
MIN_CHANNELS, MIN_MONTHS, MIN_VIDEOS = 3, 2, 4
MAX_DF = 0.02          # a phrase needs one word used in 2% of titles or fewer
POOL_MIN_CHANNELS = 4  # material from the open pool has to clear a higher bar than a curated corpus
NGRAM = (2, 4)

STOP = set("""a an the and or but if then than that this these those of in on at to for from by with without
about into over after before under again further once here there all any both each few more most other some such
no nor not only own same so too very can will just should now what why how when who whom which is are was were be
been being do does did doing have has had having i you he she it we they them his her its our your their my me
new best top vs video watch full episode part live today tomorrow yesterday week month year years ep podcast
subscribe channel please like comment share""".split())

from _lexicon import CLAIM_MARK, RHETORIC, has_content

TRACKED_VOCAB = {}
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
    # The pool: claim-carrying videos found by search that belong to no tracked
    # narrative. New narratives come from here, so discovery must read it.
    pf = ROOT / "discovery-pool.json"
    if pf.exists():
        for v in json.loads(pf.read_text()).get("videos", []):
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v.get("published") or ""):
                continue
            vids.append({**v, "_topic": "(pool)", "_industry": v.get("industry", "Unsorted"),
                         "_month": v["published"][:7], "first_seen": v.get("found")})
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
    global TRACKED_VOCAB
    vids, wl, inds = load()
    TRACKED_VOCAB = topic_vocab(wl, corpus_titles())
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
    def content(ph):
        """Words that say what the claim is about, once rhetoric is removed."""
        return [w for w in ph.split()
                if w not in RHETORIC and not CLAIM_MARK.fullmatch(w)]
    assert has_content("dollar collapse") and not has_content("shocking truth")

    def distinctive(ph):
        c = content(ph)
        return bool(c) and any(df[w] / N <= MAX_DF for w in c)

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
        pooled = [x for x in h["v"] if x["_topic"] == "(pool)"]
        if top == "(pool)":
            if len(h["ch"]) < POOL_MIN_CHANNELS:
                continue
            # A pool phrase often just restates something we already track. Ask the
            # channel sweep's matcher, which knows each narrative's learned wording.
            votes = Counter(filter(None, (best_topic(x["title"], "", TRACKED_VOCAB)[0] for x in h["v"])))
            if votes and votes.most_common(1)[0][1] >= len(h["v"]) / 2:
                top = votes.most_common(1)[0][0]
                share = votes.most_common(1)[0][1] / len(h["v"])
                pooled = []
        pw = set(ph.split())
        overlap = len(pw & tracked.get(top, set())) / max(1, len(pw))
        cands.append({
            "phrase": ph, "videos": len(h["v"]), "channels": len(h["ch"]),
            "months": len(h["mo"]), "span": f"{min(h['mo'])} → {max(h['mo'])}",
            "industry": (Counter(x.get("_industry", "Unsorted") for x in pooled).most_common(1)[0][0]
                         if top == "(pool)" and pooled else industry_of.get(top, "Unsorted")),
            "home": top, "home_share": round(share, 2),
            "kind": "new candidate" if top == "(pool)" else
                    "sub-claim" if (share >= 0.8 and overlap >= 0.5) else
                    ("cross-narrative" if share < 0.6 else "new candidate"),
            "examples": [x["title"] for x in sorted(h["v"], key=lambda x: x["_month"])[:3]],
            "ids": sorted({x["videoId"] for x in h["v"]}),
        })

    # Cluster: phrases carried by the same videos are one candidate. The longest
    # phrase names it, and its evidence is the union.
    cands.sort(key=lambda c: (-c["videos"], -len(c["phrase"])))
    kept, bags = [], {}
    for c in cands:
        bag = frozenset(content(c["phrase"]))
        if bag and bag in bags:
            bags[bag].setdefault("also", []).append(c["phrase"])
            continue
        ids = set(c["ids"])
        home = next((k for k in kept if len(ids & set(k["ids"])) / max(1, min(len(ids), len(k["ids"]))) >= 0.5), None)
        if home:
            home.setdefault("also", []).append(c["phrase"])
            if len(c["phrase"]) > len(home["phrase"]) and c["videos"] >= home["videos"] * 0.8:
                home["phrase"], c["phrase"] = c["phrase"], home["phrase"]
            continue
        kept.append(c)
        if bag:
            bags[bag] = c

    for c in kept:
        c["specificity"] = round(min((df[w] / N for w in content(c["phrase"])), default=1), 4)
        c["rank"] = round(c["channels"] * c["months"] / max(c["specificity"], 0.0005) / 1000, 1)
    kept.sort(key=lambda c: -c["rank"])

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
