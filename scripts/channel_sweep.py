#!/usr/bin/env python3
"""Narrative Radar — collect new uploads from the channels in the ledger.

    python3 scripts/channel_sweep.py                      # dry run, tier A
    python3 scripts/channel_sweep.py --write              # append to the corpora
    python3 scripts/channel_sweep.py --tiers=AB --days=14 --write

Why this exists
  The daily sweep searches each narrative's queries, which spends about half of
  the 100 daily search calls — the one bucket that cannot be topped up and the
  only way to find channels and narratives we do not yet know. Reading a known
  channel's uploads costs 1 unit per 50 videos from the 10,000 bucket instead,
  so this route collects more for a fraction of the scarce resource and leaves
  search free for discovery.

How it works
  For every channel in channels.json at the chosen tiers, it walks the uploads
  playlist back `--days`, keeps videos not already in a corpus, scores each
  title and description against every narrative's query vocabulary, and files
  the ones that clearly belong. Everything else is reported and dropped, since
  a channel we follow also posts about other things.

  Requires YT_API_KEY. Official API only (decision 2026-09-16).
"""
import json, os, re, sys, urllib.parse, urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://www.googleapis.com/youtube/v3/"
KEY = os.environ.get("YT_API_KEY", "").strip()
WRITE = "--write" in sys.argv
arg = lambda name, dflt: next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{name}=")), dflt)
DAYS = int(arg("days", 7))
TIERS = set(arg("tiers", "A").upper())
MAX_CHANNELS = int(arg("max", 400))
SCORE_MIN = float(arg("min-score", 6))   # tuned offline: 74% recall on filed videos, no known false positives
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
CUTOFF = datetime.now(timezone.utc) - timedelta(days=DAYS)

STOP = set("""the and for with that this from what how why your you are was were will has have not but all any
about into over more most just now new best top vs video watch full episode part live""".split())
units = 0


def call(endpoint, **params):
    global units
    params["key"] = KEY
    url = API + endpoint + "?" + urllib.parse.urlencode(params, doseq=True)
    with urllib.request.urlopen(url, timeout=30) as r:
        units += 1
        return json.loads(r.read().decode())


def words(s):
    s = re.sub(r"[^a-z0-9'\s-]", " ", (s or "").lower())
    return [w for w in s.split() if len(w) > 2 and w not in STOP]


def topic_vocab(topics, corpora=None):
    """Each narrative's DISTINCTIVE vocabulary, learned from its own corpus.

    Two sources. The six search queries say what we went looking for. The titles
    already filed under the narrative say what it actually sounds like, which is
    far richer: "halving", "bull run", "yield curve", "remote viewing".

    A term counts only where it is distinctive. A word used across several
    narratives — "market", "2026", "crash" — identifies none of them, and
    matching on it files the Federal Reserve's rate decision as a housing story.
    So a term is kept for a narrative when that narrative uses it at least three
    times AND uses it at least three times more densely than the rest do.
    """
    MIN_N, RATIO = 3, 3.0
    q_terms, c_counts, totals = {}, {}, defaultdict(int)
    for t in topics:
        grams, singles = set(), set()
        for q in t.get("queries", []):
            ws = words(q)
            singles |= set(ws)
            grams |= {" ".join(ws[i:i + 2]) for i in range(len(ws) - 1)}
        q_terms[t["id"]] = (grams, singles)
        counts = defaultdict(int)
        for title in (corpora or {}).get(t["id"], []):
            ws = words(title)
            for term in set(ws) | {" ".join(ws[i:i + 2]) for i in range(len(ws) - 1)}:
                counts[term] += 1
                totals[term] += 1
        c_counts[t["id"]] = counts

    sizes = {tid: max(1, sum(1 for _ in (corpora or {}).get(tid, []))) for tid in c_counts}
    grand = max(1, sum(sizes.values()))
    owners = defaultdict(set)
    for tid, (grams, singles) in q_terms.items():
        for term in grams | singles:
            owners[term].add(tid)

    vocab = {}
    for tid, (grams, singles) in q_terms.items():
        g = {t for t in grams if len(owners[t]) == 1}
        u = {t for t in singles if len(owners[t]) == 1}
        for term, n in c_counts.get(tid, {}).items():
            if n < MIN_N:
                continue
            mine = n / sizes[tid]
            rest = (totals[term] - n) / max(1, grand - sizes[tid])
            if mine < rest * RATIO:
                continue
            (g if " " in term else u).add(term)
        vocab[tid] = (g, u)
    return vocab


def corpus_titles():
    out = {}
    for f in sorted((ROOT / "corpus").glob("*/videos.json")):
        out[f.parent.name] = [v.get("title", "") for v in json.loads(f.read_text())["videos"]]
    return out


def best_topic(title, description, vocab):
    """A video belongs to a narrative when its TITLE carries that narrative's
    own wording: one distinctive two-word phrase, or two distinctive words with
    support. The description can support a match but never make one, because
    descriptions carry sponsor text, link lists and channel boilerplate."""
    t = " ".join(words(title))
    tw = set(t.split())
    d = " ".join(words(description))
    best, score = None, 0
    for tid, (grams, singles) in vocab.items():
        tg = sum(1 for g in grams if g in t)
        tu = len(tw & singles)
        dg = sum(1 for g in grams if g in d)
        sc = tg * 4 + tu * 1.5 + min(dg, 2)
        if (tg >= 1 or tu >= 2) and sc >= SCORE_MIN and sc > score:
            best, score = tid, sc
    return best, score


def uploads_items(playlist_id):
    """Videos from an uploads playlist, newest first, back to the cutoff."""
    out, page = [], None
    for _ in range(10):                       # 500 videos per channel per run, hard stop
        r = call("playlistItems", part="snippet,contentDetails", playlistId=playlist_id,
                 maxResults=50, **({"pageToken": page} if page else {}))
        stop = False
        for it in r.get("items", []):
            pub = it["contentDetails"].get("videoPublishedAt") or it["snippet"].get("publishedAt")
            if not pub:
                continue
            when = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            if when < CUTOFF:
                stop = True
                continue
            sn = it["snippet"]
            out.append({"videoId": it["contentDetails"]["videoId"], "title": sn.get("title", ""),
                        "description": (sn.get("description") or "")[:1200],
                        "published": when.strftime("%Y-%m-%d"), "channel": sn.get("channelTitle", ""),
                        "channelId": sn.get("videoOwnerChannelId") or sn.get("channelId")})
        page = r.get("nextPageToken")
        if stop or not page:
            break
    return out


def hydrate(ids):
    """Duration, views and the rest, 50 at a time."""
    meta = {}
    for i in range(0, len(ids), 50):
        r = call("videos", part="contentDetails,statistics,snippet", id=",".join(ids[i:i + 50]), maxResults=50)
        for it in r.get("items", []):
            cd, st, sn = it.get("contentDetails", {}), it.get("statistics", {}), it.get("snippet", {})
            m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", cd.get("duration", "") or "")
            h, mi, se = (int(x or 0) for x in (m.groups() if m else (0, 0, 0)))
            meta[it["id"]] = {
                "length": (f"{h}:{mi:02d}:{se:02d}" if h else f"{mi}:{se:02d}"),
                "views": int(st.get("viewCount", 0) or 0),
                "yt": {"category": sn.get("categoryId"), "channelId": sn.get("channelId"),
                       "language": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage"),
                       "captions": cd.get("caption") == "true", "live": sn.get("liveBroadcastContent") not in (None, "none"),
                       "likes": int(st.get("likeCount", 0) or 0) or None,
                       "comments": int(st.get("commentCount", 0) or 0) or None,
                       "enrichedOn": TODAY},
            }
    return meta


def selftest():
    """Measure the matcher without touching the API: recall against every video
    already filed under a narrative, precision against uploads the first dry run
    wrongly matched."""
    wl = json.loads((ROOT / "watchlist.json").read_text())["topics"]
    vocab = topic_vocab(wl, corpus_titles())
    hit = miss = 0
    for t in wl:
        f = ROOT / "corpus" / t["id"] / "videos.json"
        if not f.exists():
            continue
        for v in json.loads(f.read_text())["videos"]:
            tid, _ = best_topic(v["title"], "", vocab)
            if tid == t["id"]:
                hit += 1
            else:
                miss += 1
    wrong = [
        "Fed Hikes Rates for the First Time Since 2023",
        "Houthi Conflict Threatens Saudi Arabia's Economy",
        "KFC is Crashing Hard, Over 700 Stores Have CLOSED",
        "The Bond Market Is Breaking",
        "Claude + Obsidian is Absolutely WILD!",
        "Orca ADE: New FREE AI Coding Agent!",
        "Grok Bot Manages My Inbox (and has its own)",
        "Do Proton Pump Inhibitors Work for Acid Reflux (GERD)?",
        "The #1 Best Food to Reverse Fatty Liver",
        "Angie Nixon's old education post IGNITES new debate",
        "EU Proposes Canada to Become First 'Associate Member'; Fed Decision on December",
        "Rep. Josh Gottheimer: You can't get rid of data centers, but put them only where useful",
        "Market Close: Fed Raises Rates, Signals More Hikes Ahead; Stocks Fall",
        "Stop Having Nightmares!",
        "China Is Turning America's AI Advantage Against It",
    ]
    still = [(w, best_topic(w, "", vocab)) for w in wrong]
    caught = [(w, r) for w, r in still if r[0]]
    print(f"recall on filed videos: {hit}/{hit + miss} ({hit / max(1, hit + miss) * 100:.0f}%)")
    print(f"known false positives still matching: {len(caught)}/{len(wrong)}")
    for w, (tid, sc) in caught:
        print(f"    {tid} ({sc}) ← {w[:66]}")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if not KEY:
        print("channel sweep: no YT_API_KEY. Official API only (decision 2026-09-16); nothing collected.")
        return
    ledger = json.loads((ROOT / "channels.json").read_text())["channels"]
    rows = [r for r in ledger if r["tier"] in TIERS and r.get("channelId")][:MAX_CHANNELS]
    wl = json.loads((ROOT / "watchlist.json").read_text())["topics"]
    vocab = topic_vocab(wl, corpus_titles())

    corpora, known = {}, set()
    for t in wl:
        f = ROOT / "corpus" / t["id"] / "videos.json"
        if f.exists():
            corpora[t["id"]] = json.loads(f.read_text())
            known |= {v["videoId"] for v in corpora[t["id"]]["videos"]}

    print(f"channel sweep {TODAY} · tier {''.join(sorted(TIERS))} · {len(rows)} channels · last {DAYS} days")
    seen, matched, off_topic = 0, defaultdict(list), 0
    for r in rows:
        try:
            items = uploads_items("UU" + r["channelId"][2:])
        except Exception as e:
            print(f"  ! {r['channel'][:34]}: {e}")
            continue
        for v in items:
            seen += 1
            if v["videoId"] in known:
                continue
            tid, score = best_topic(v["title"], v["description"], vocab)
            if not tid:
                off_topic += 1
                continue
            v["_score"] = score
            matched[tid].append(v)

    ids = [v["videoId"] for vs in matched.values() for v in vs]
    meta = hydrate(ids) if ids else {}

    total = 0
    for tid, vs in sorted(matched.items()):
        doc = corpora.get(tid)
        if not doc:
            continue
        add = []
        for v in sorted(vs, key=lambda x: x["published"], reverse=True):
            m = meta.get(v["videoId"], {})
            if m.get("yt", {}).get("live"):
                continue
            add.append({
                "videoId": v["videoId"], "title": v["title"], "channel": v["channel"],
                "url": f"https://www.youtube.com/watch?v={v['videoId']}",
                "published": v["published"], "first_seen": TODAY,
                "views": m.get("views"), "length": m.get("length"),
                "age_days": (datetime.now(timezone.utc) - datetime.fromisoformat(v["published"] + "T00:00:00+00:00")).days,
                "query": f"channel sweep: {v['channel']}", "transcript": None,
                "verdict": "UNREVIEWED", "verdict_basis": "metadata", "yt": m.get("yt", {}),
            })
        print(f"  {tid:28s} +{len(add)}")
        for v in add[:4]:
            print(f"      {v['published']}  {v['title'][:74]}")
        if add and WRITE:
            doc["videos"].extend(add)
            (ROOT / "corpus" / tid / "videos.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        total += len(add)

    print(f"  {seen} uploads read · {off_topic} off-topic for these narratives · {units} quota units")
    print(f"+{total} new videos across {len(matched)} narratives (channel uploads)")


if __name__ == "__main__":
    main()
