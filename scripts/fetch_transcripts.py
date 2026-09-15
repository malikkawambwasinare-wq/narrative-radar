#!/usr/bin/env python3
"""Narrative Radar — pull transcripts and real publish dates for videos that lack them.

    python3 scripts/fetch_transcripts.py                 # every narrative, dry run
    python3 scripts/fetch_transcripts.py collapse-audit  # one narrative
    python3 scripts/fetch_transcripts.py --write         # save transcripts + update videos.json

Why this exists
  The live paste path (analyze.mjs) runs on datacenter IPs where YouTube serves
  empty caption bodies, so every live verdict is made from title + channel and
  stamped "[live analysis, metadata-only]". This script closes that gap from a
  machine YouTube does serve: it fetches the transcript with youtube_transcript_api
  (the same path collector.py used for the stocked corpus), pulls the true publish
  date, view count and length off the watch page, and records an explicit
  verdict_basis so the site can say which verdicts were read and which were guessed.

  It never changes a verdict. scripts/review-verdicts.mjs does that, with the
  transcript in hand.

What it writes
  corpus/<topic>/transcripts/<id>.txt   (gitignored — third-party text stays local)
  videos.json: transcript path, published (ISO), views, length, verdict_basis
"""
import json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv
ONLY = [a for a in sys.argv[1:] if not a.startswith("--")]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9",
                                               "Cookie": "CONSENT=YES+cb; SOCS=CAI"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def transcript(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    fetched = YouTubeTranscriptApi().fetch(video_id, languages=["en", "en-US", "en-GB"])
    lines = []
    for s in fetched.snippets:
        seg = s.text.replace("\n", " ").strip()
        if seg:
            start = int(s.start)
            lines.append(f"[{start // 60:02d}:{start % 60:02d}] {seg}")
    return "\n".join(lines) if lines else None

def watch_meta(video_id):
    """publishDate (ISO date), viewCount, lengthSeconds from the watch page."""
    html = fetch(f"https://www.youtube.com/watch?v={video_id}")
    g = lambda k: (re.search(r'"%s":"([^"]+)"' % k, html) or [None, None])[1]
    pub = g("publishDate")
    views = g("viewCount")
    secs = g("lengthSeconds")
    return {
        "published": pub[:10] if pub else None,
        "views": f"{int(views):,} views" if views and views.isdigit() else None,
        "length": (f"{int(secs) // 60}:{int(secs) % 60:02d}" if secs and secs.isdigit() else None),
    }

def basis_of(v):
    """Explicit record of how a verdict was made. Never upgrades a metadata verdict
    just because a transcript now exists — review-verdicts.mjs does that."""
    if v.get("verdict_basis"):
        return v["verdict_basis"]
    if "metadata-only" in (v.get("verdict_note") or ""):
        return "metadata"
    return "transcript" if v.get("transcript") else "metadata"

total_t = total_d = 0
for tdir in sorted((ROOT / "corpus").iterdir()):
    topic = tdir.name
    if ONLY and topic not in ONLY: continue
    vf = tdir / "videos.json"
    if not vf.exists(): continue
    doc = json.loads(vf.read_text())
    (tdir / "transcripts").mkdir(exist_ok=True)
    got_t = got_d = 0
    blocked_streak, blocked = 0, False
    print(f"\n{topic}")
    for v in doc.get("videos", []):
        vid = v["videoId"]
        v["verdict_basis"] = basis_of(v)
        tpath = tdir / "transcripts" / f"{vid}.txt"
        # transcript — skipped once YouTube starts blocking: hammering a block
        # only lengthens it. Re-run later; finished files are never re-fetched.
        no_captions = (v.get("yt") or {}).get("channelId") and not (v.get("yt") or {}).get("captions")
        if not tpath.exists() and not blocked and not no_captions:
            try:
                txt = transcript(vid)
                blocked_streak = 0
                if txt:
                    if WRITE: tpath.write_text(txt)
                    v["transcript"] = str(tpath.relative_to(ROOT))
                    got_t += 1
                    print(f"  + transcript  {vid}  {len(txt):6d} chars  {v.get('title','')[:50]}")
                else:
                    print(f"  - no captions {vid}")
            except Exception as e:
                name = type(e).__name__
                print(f"  ! {vid}: {name} {str(e).splitlines()[0][:60]}")
                if name in ("RequestBlocked", "IpBlocked", "TooManyRequests") or "429" in str(e):
                    blocked_streak += 1
                    if blocked_streak >= 3:
                        blocked = True
                        print("  ⏸ YouTube is blocking transcript requests from this IP — stopping; re-run later to resume.")
            time.sleep(3.0)
        elif not v.get("transcript"):
            v["transcript"] = str(tpath.relative_to(ROOT))
        # real dates for anything stored as a relative string ("10 days ago") or missing
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v.get("published") or ""):
            try:
                m = watch_meta(vid)
                if m["published"]:
                    v["published"] = m["published"]; got_d += 1
                    if m["views"]: v["views"] = m["views"]
                    if m["length"] and not v.get("length"): v["length"] = m["length"]
                    if v.get("age_days") is None and v.get("first_seen"):
                        from datetime import date
                        v["age_days"] = (date.fromisoformat(v["first_seen"][:10]) - date.fromisoformat(m["published"])).days
                    print(f"  ~ dated       {vid}  {m['published']}")
            except Exception as e:
                print(f"  ! date {vid}: {str(e).splitlines()[0][:60]}")
            time.sleep(0.8)
    if WRITE:
        vf.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    total_t += got_t; total_d += got_d
    bases = {}
    for v in doc.get("videos", []): bases[v["verdict_basis"]] = bases.get(v["verdict_basis"], 0) + 1
    print(f"  {got_t} transcripts pulled, {got_d} dates fixed · basis now {bases}")

print(f"\n{total_t} transcripts, {total_d} dates" + ("" if WRITE else " — dry run, pass --write"))
