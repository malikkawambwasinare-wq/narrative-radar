#!/usr/bin/env python3
"""Narrative Radar — pull every filterable signal YouTube exposes for a video and its channel.

    python3 scripts/enrich_youtube.py                    # every narrative, dry run
    python3 scripts/enrich_youtube.py collapse-audit     # one narrative
    python3 scripts/enrich_youtube.py --write            # save into videos.json
    python3 scripts/enrich_youtube.py --write --refresh  # re-pull even if already enriched

Why this exists
  The Series page lets the viewer decide what counts as relevant: how many people
  watched, whether the channel is verified, what kind of channel it is, where it
  is based, how old it is. None of that is in videos.json today — only the title,
  channel name and a view string. This script pulls the rest off YouTube's own
  pages (the watch page's ytInitialPlayerResponse / ytInitialData and the channel
  About page) and stores it under `yt` on each video.

Storage rule
  Only identifiers, dates, counts and category labels are stored. No description
  text, no comments, no keyword lists — third-party text stays out of the repo.

What it writes (per video, under "yt")
  category, channelId, handle, verified, unlisted, familySafe, regionsAvailable,
  likes, comments, subscribers, channelCountry, channelJoined, channelViews,
  channelVideos, enrichedOn
"""
import json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITE = "--write" in sys.argv
REFRESH = "--refresh" in sys.argv
ONLY = [a for a in sys.argv[1:] if not a.startswith("--")]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PAUSE = 1.2   # seconds between page fetches; polite, and well under YouTube's tolerance


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9",
                                               "Cookie": "CONSENT=YES+cb; SOCS=CAI"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def ytjson(html, var):
    m = re.search(var + r"\s*=\s*(\{.*?\});\s*(?:</script>|var |window)", html, re.S)
    return json.loads(m.group(1)) if m else {}


def walk(o, key, out):
    if isinstance(o, dict):
        if key in o:
            out.append(o[key])
        for v in o.values():
            walk(v, key, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, key, out)
    return out


def text(o):
    if not isinstance(o, dict):
        return o
    return o.get("simpleText") or o.get("content") or "".join(r.get("text", "") for r in o.get("runs", []))


def to_int(s):
    """'19.6M subscribers' → 19600000; '114,261' → 114261; None on no number."""
    if not s:
        return None
    m = re.search(r"([\d.,]+)\s*([KMB])?", str(s))
    if not m:
        return None
    n = float(m.group(1).replace(",", ""))
    return int(n * {"K": 1e3, "M": 1e6, "B": 1e9, None: 1}[m.group(2)])


def video_signals(video_id):
    html = fetch(f"https://www.youtube.com/watch?v={video_id}")
    pr = ytjson(html, "ytInitialPlayerResponse")
    d = ytjson(html, "ytInitialData")
    vd = pr.get("videoDetails", {})
    mf = pr.get("microformat", {}).get("playerMicroformatRenderer", {})
    owner = (walk(d, "videoOwnerRenderer", []) or [{}])[0]
    verified = any(b.get("metadataBadgeRenderer", {}).get("style") in
                   ("BADGE_STYLE_TYPE_VERIFIED", "BADGE_STYLE_TYPE_VERIFIED_ARTIST")
                   for b in owner.get("badges", []))
    handle = None
    for u in walk(owner, "canonicalBaseUrl", []):
        if isinstance(u, str) and u.startswith("/@"):
            handle = u[1:]
            break
    likes = None
    for s in walk(d, "accessibilityText", []):
        if isinstance(s, str) and "like this video" in s:
            likes = to_int(re.search(r"([\d,]+) other people", s).group(1)) if "other people" in s else None
            break
    comments = None
    for c in walk(d, "commentCount", []):
        comments = to_int(text(c))
        if comments is not None:
            break
    out = {
        "category": mf.get("category"),
        "channelId": vd.get("channelId"),
        "handle": handle,
        "verified": verified,
        "unlisted": bool(mf.get("isUnlisted")),
        "familySafe": bool(mf.get("isFamilySafe", True)),
        "regionsAvailable": len(mf.get("availableCountries") or []) or None,
        "likes": likes,
        "comments": comments,
        "subscribers": to_int(text(owner.get("subscriberCountText"))),
    }
    # Fresh view count and publish date come along for free; keep them current.
    if vd.get("viewCount", "").isdigit():
        out["_views"] = f"{int(vd['viewCount']):,} views"
    if mf.get("publishDate"):
        out["_published"] = mf["publishDate"][:10]
    return out


def channel_signals(channel_id):
    html = fetch(f"https://www.youtube.com/channel/{channel_id}/about")
    d = ytjson(html, "ytInitialData")
    about = (walk(d, "aboutChannelViewModel", []) or [{}])[0]
    joined = text(about.get("joinedDateText")) or ""
    m = re.search(r"([A-Z][a-z]{2}) (\d{1,2}), (\d{4})", joined)
    joined_iso = None
    if m:
        months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
        joined_iso = f"{m.group(3)}-{months.index(m.group(1)) + 1:02d}-{int(m.group(2)):02d}"
    return {
        "channelCountry": text(about.get("country")) or None,
        "channelJoined": joined_iso,
        "channelViews": to_int(text(about.get("viewCountText"))),
        "channelVideos": to_int(text(about.get("videoCountText"))),
        "subscribers": to_int(text(about.get("subscriberCountText"))),
    }


def main():
    topics = [p for p in sorted((ROOT / "corpus").iterdir()) if (p / "videos.json").exists()]
    if ONLY:
        topics = [t for t in topics if t.name in ONLY]
    today = time.strftime("%Y-%m-%d")
    channel_cache = {}
    total_v = total_c = 0
    for t in topics:
        f = t / "videos.json"
        data = json.loads(f.read_text())
        print(f"\n{t.name}")
        for v in data["videos"]:
            if v.get("yt") and not REFRESH:
                continue
            try:
                sig = video_signals(v["videoId"])
                time.sleep(PAUSE)
            except Exception as e:
                print(f"  ! {v['videoId']}: {e}")
                continue
            views, pub = sig.pop("_views", None), sig.pop("_published", None)
            if views:
                v["views"] = views
            if pub and not re.match(r"^\d{4}-\d{2}-\d{2}$", v.get("published") or ""):
                v["published"] = pub
            cid = sig.get("channelId")
            if cid:
                if cid not in channel_cache:
                    try:
                        channel_cache[cid] = channel_signals(cid)
                        total_c += 1
                        time.sleep(PAUSE)
                    except Exception as e:
                        print(f"  ! channel {cid}: {e}")
                        channel_cache[cid] = {}
                ch = dict(channel_cache[cid])
                if sig.get("subscribers") is None:
                    sig["subscribers"] = ch.pop("subscribers", None)
                else:
                    ch.pop("subscribers", None)
                sig.update(ch)
            sig["enrichedOn"] = today
            v["yt"] = sig
            total_v += 1
            print(f"  + {v['videoId']}  {sig.get('category') or '?':18s} {'✓' if sig['verified'] else ' '} "
                  f"{(sig.get('channelCountry') or '—'):16s} subs {sig.get('subscribers') or '—'}  likes {sig.get('likes') or '—'}")
        if WRITE:
            f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"\n{total_v} videos enriched, {total_c} channels fetched{' · written' if WRITE else ' · dry run (add --write)'}")


if __name__ == "__main__":
    main()
