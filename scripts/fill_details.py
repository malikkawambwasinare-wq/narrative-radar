#!/usr/bin/env python3
"""Narrative Radar — fill in the details of videos we hold but never looked up.

    python3 scripts/fill_details.py                  # report what is missing
    python3 scripts/fill_details.py --write          # fetch and fill
    python3 scripts/fill_details.py --write --max=5000

A video can enter a corpus from three places: a channel's uploads, a search
result, or the discovery pool. Only the first arrives with a runtime. The others
carry a title and a date, which is enough to file a claim and useless for a set:
the evening set needs runtimes to fit a time budget, so a narrative built from
refiled videos could not produce a single set until this ran.

videos.list returns duration, views, likes, comments, category and whether
captions exist, fifty videos per quota unit — so filling ten thousand videos
costs 200 units, a fiftieth of a day.

Official API only (decision 2026-09-16).
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://www.googleapis.com/youtube/v3/videos"
KEY = os.environ.get("YT_API_KEY", "").strip()
WRITE = "--write" in sys.argv
arg = lambda n, d: next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{n}=")), d)
MAX = int(arg("max", 20000))
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
units = 0


class QuotaGone(Exception):
    """The day's allowance is spent. What is already filled still counts."""


def fetch(ids):
    global units
    url = API + "?" + urllib.parse.urlencode({
        "key": KEY, "part": "contentDetails,statistics,snippet", "id": ",".join(ids), "maxResults": 50})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                units += 1
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 403:
                raise QuotaGone()      # the day's allowance is spent; keep what is filled
            if e.code == 400:
                raise
        except Exception:
            pass
        time.sleep(1.5 * (3 ** attempt))
    return {"items": []}


def duration(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    h, mi, se = (int(x or 0) for x in (m.groups() if m else (0, 0, 0)))
    return f"{h}:{mi:02d}:{se:02d}" if h else f"{mi}:{se:02d}"


def main():
    if not KEY:
        print("fill details: no YT_API_KEY. Official API only (decision 2026-09-16); nothing fetched.")
        return
    todo, docs = [], {}
    for f in sorted((ROOT / "corpus").glob("*/videos.json")):
        doc = json.loads(f.read_text())
        docs[f] = doc
        for v in doc["videos"]:
            if not v.get("length") and v.get("videoId"):
                todo.append(v)
    print(f"{sum(len(d['videos']) for d in docs.values()):,} videos held · {len(todo):,} without a runtime")
    todo = todo[:MAX]
    if not todo:
        return

    by_id = {v["videoId"]: [] for v in todo}
    for v in todo:
        by_id[v["videoId"]].append(v)
    ids = list(by_id)
    filled, gone = 0, 0
    stopped = None
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        try:
            got = {it["id"]: it for it in fetch(batch).get("items", [])}
        except QuotaGone:
            stopped = "daily quota reached"
            break
        for vid in batch:
            it = got.get(vid)
            if not it:
                gone += 1
                for v in by_id[vid]:
                    v["unavailable"] = TODAY      # deleted or private: recorded, not deleted
                continue
            cd, st, sn = it.get("contentDetails", {}), it.get("statistics", {}), it.get("snippet", {})
            for v in by_id[vid]:
                v["length"] = duration(cd.get("duration"))
                v["views"] = int(st.get("viewCount", 0) or 0)
                if not v.get("published") and sn.get("publishedAt"):
                    v["published"] = sn["publishedAt"][:10]
                yt = v.get("yt") or {}
                yt.update({"category": sn.get("categoryId"), "channelId": sn.get("channelId") or yt.get("channelId"),
                           "language": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage"),
                           "captions": cd.get("caption") == "true",
                           "live": sn.get("liveBroadcastContent") not in (None, "none"),
                           "likes": int(st.get("likeCount", 0) or 0) or None,
                           "comments": int(st.get("commentCount", 0) or 0) or None,
                           "enrichedOn": TODAY})
                v["yt"] = yt
                filled += 1
        if i and i % 1000 == 0:
            print(f"  {i}/{len(ids)}…")
    if WRITE:
        for f, doc in docs.items():
            doc["updated"] = TODAY
            f.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    if stopped:
        print(f"  STOPPED: {stopped} — {len(ids) - i:,} videos left for the next run")
    print(f"filled {filled:,} · {gone:,} no longer available · {units} quota units{'' if WRITE else ' (dry run)'}")


if __name__ == "__main__":
    main()
