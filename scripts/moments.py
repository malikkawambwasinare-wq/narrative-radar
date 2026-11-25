#!/usr/bin/env python3
"""Story Evenings: find the moments in tracked videos.

    GEMINI_API_KEY=... python3 scripts/moments.py              # every company track
    GEMINI_API_KEY=... python3 scripts/moments.py co-walmart   # one track
    python3 scripts/moments.py --per 3 --model gemini-3.6-flash

A moment is a stretch of one video where one person says one thing worth
hearing about something the viewer follows (briefs/MOMENTS-SPEC.md). Titles
only say a video *might* be about Walmart; this watches it and says where, and
what was said.

For each company track it picks the newest unwatched videos that mention the
company (from every file in tracking/, so a video found for "Anthropic goes
public" counts for Anthropic too), watches them with Gemini, and tags every
moment against ALL tracks: companies, ideas (tracking/ideas.json) and stories.
One watch therefore feeds several tracks.

Writes:
  watch/moments/<videoId>.json   one per watched video (local cache, never re-watched)
  tracking/moments.json          every moment, newest first, for the page
"""
import json, re, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gemini import ApiError, Budget, DailyLimit, ask, key, payload, spend, video_tokens  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TRK, CACHE = ROOT / "tracking", ROOT / "watch" / "moments"
arg = lambda f, d: next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == f), d)
MODEL, PER = arg("--model", "gemini-3.8-flash"), int(arg("--per", "4"))
ONLY = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (MODEL, str(PER))]

# Original outlets and the shows people already watch rank first; a re-upload never does.
OUTLETS = re.compile(r"bloomberg|cnbc|yahoo finance|reuters|wall street journal|wsj|financial times|schwab|fox business|bbc|"
                     r"the economist|new york times|marketwatch|barron|morningstar|all-in|prof g|diary of a ceo|lex|"
                     r"motley fool|seeking alpha|bnn|sky news|abc news|cbs|nbc", re.I)


def secs(mmss):
    p = [int(x) for x in str(mmss).split(":") if x.strip().isdigit()]
    return p[0] * 60 + p[1] if len(p) == 2 else (p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else 0)


def load_tracks():
    cfg = json.loads((TRK / "narratives.json").read_text())
    ideas = json.loads((TRK / "ideas.json").read_text())["ideas"] if (TRK / "ideas.json").exists() else []
    tracks = [n for n in cfg["narratives"] if n.get("kind") in ("company", "story") and not n.get("theme")] + ideas
    return tracks, ideas


def words(term):
    return re.compile(r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])")


def candidates(track):
    """Every tracked video whose title names this company, newest first."""
    seen, out = set(), []
    for f in TRK.glob("*.json"):
        if f.name in ("index.json", "narratives.json", "ideas.json", "moments.json"):
            continue
        for v in json.loads(f.read_text()).get("videos", []):
            if v["id"] in seen or not all(any(words(t).search(v["title"].lower()) for t in g) for g in track["match"]):
                continue
            s = secs(v.get("length", "0:00"))
            if not (120 <= s <= 45 * 60):      # free watching stops at about 45 minutes
                continue
            seen.add(v["id"]); out.append(v)
    return sorted(out, key=lambda v: (bool(OUTLETS.search(v["channel"])), v["published"]), reverse=True)


def schema(names):
    return {"type": "object", "properties": {
        "moments": {"type": "array", "items": {"type": "object", "properties": {
            "start": {"type": "string", "description": "MM:SS of the first word of the thought, exact to the second"},
            "end": {"type": "string", "description": "MM:SS just after the thought finishes"},
            "speaker": {"type": "string"},
            "credential": {"type": "string", "description": "Their job and firm as stated or shown; empty if never established"},
            "practises": {"type": "boolean", "description": "They work in this field (executive, investor, analyst, economist), rather than commenting on it"},
            "line": {"type": "string", "description": "The key sentence, word for word, under 30 words"},
            "gist": {"type": "string", "description": "What a viewer learns, in one plain sentence"},
            "kind": {"type": "string", "enum": ["fact", "data", "explanation", "view", "question"]},
            # Malik (2026-11-25): short term is noise ("investors are irrational"); the
            # 12-month view is where fundamentals decide. Every moment says which it is.
            "horizon": {"type": "string", "enum": ["today", "12 months", "years"],
                        "description": "today = price moves and reactions; 12 months = demand, supply, competition, financing; years = long-run shifts"},
            "tracks": {"type": "array", "items": {"type": "object", "properties": {
                "track": {"type": "string", "enum": names},
                "fit": {"type": "string", "enum": ["yes", "partly"]}}, "required": ["track", "fit"]}}},
            "required": ["start", "end", "speaker", "credential", "practises", "line", "gist", "kind", "horizon", "tracks"]}}},
        "required": ["moments"]}


def prompt(tracks, v):
    lines = []
    for t in tracks:
        if t["kind"] == "idea":
            lines.append(f"- {t['name']} (an idea: {t['question']} Example of a moment that fits: {t['seed']})")
        else:
            lines.append(f"- {t['name']} (a {t['kind']}: {t.get('line', '')})")
    return ("You are building a short morning briefing for someone who follows these tracks:\n" + "\n".join(lines) +
            f"\n\nWatch this video (“{v['title']}”, {v['channel']}). Find up to 6 MOMENTS worth their limited time: "
            "10 seconds to 3 minutes where one person says something they would want to hear about one of the tracks: "
            "a fact or number, how something works, what people in the business see, or a clear view with its reason. "
            "Skip intros, adverts, sponsor reads, repetition and vague hype. Start each moment on the first word of the "
            "thought and end it just after the thought finishes. Tag each moment with every track it fits: 'yes' if it "
            "is squarely about it, 'partly' if it touches it. A moment that fits no track is not a moment. If the video "
            "has nothing worth hearing, return no moments.")


def main():
    tracks, _ = load_tracks()
    names = [t["name"] for t in tracks]
    by_name = {t["name"]: t["id"] for t in tracks}
    CACHE.mkdir(parents=True, exist_ok=True)
    k, budget, cost = key(), Budget(), 0.0
    for t in [t for t in tracks if t["kind"] == "company" and (not ONLY or t["id"] in ONLY)]:
        todo = [v for v in candidates(t) if not (CACHE / f"{v['id']}.json").exists()][:PER]
        print(f"{t['name']}: watching {len(todo)} · model {MODEL}", flush=True)
        for v in todo:
            try:
                r = ask(MODEL, [{"type": "text", "text": prompt(tracks, v)},
                                {"type": "video", "uri": f"https://www.youtube.com/watch?v={v['id']}"}],
                        schema(names), k, budget=budget, est_tokens=video_tokens(v.get("length")))
            except DailyLimit:
                print("  out of requests for today on this model; run again with --model or tomorrow"); return write(by_name)
            except ApiError as ex:
                print(f"  skipped ({ex.code}): {ex.detail[:100]}"); continue
            d = payload(r)
            if not d:
                print("  unparsed"); continue
            cost += spend(r)
            ms = [m for m in d.get("moments", []) if m.get("tracks") and secs(m["end"]) > secs(m["start"])]
            (CACHE / f"{v['id']}.json").write_text(json.dumps({"video": v, "moments": ms, "model": MODEL,
                                                               "watched": datetime.now(timezone.utc).isoformat()}, indent=1, ensure_ascii=False))
            print(f"  {len(ms)} moments · {v['channel'][:24]} · {v['title'][:60]}", flush=True)
    print(f"cost ${cost:.3f}")
    write(by_name)


def write(by_name):
    """Every cached moment, as the page wants it."""
    out = []
    for f in CACHE.glob("*.json"):
        d = json.loads(f.read_text()); v = d["video"]
        for i, m in enumerate(d["moments"]):
            a, b = secs(m["start"]), secs(m["end"])
            tr = [{"id": by_name[x["track"]], "fit": x["fit"]} for x in m["tracks"] if x["track"] in by_name]
            if not tr or b - a < 8:
                continue
            out.append({"id": f"{v['id']}-{i}", "video": v["id"], "channel": v["channel"], "title": v["title"], "published": v["published"],
                        "start": max(0, a - 1), "end": b + 1, "speaker": m["speaker"], "credential": m["credential"],
                        "practises": m["practises"], "line": m["line"], "gist": m["gist"], "kind": m["kind"], "horizon": m.get("horizon", ""), "tracks": tr,
                        "found": d["watched"][:10]})
    out.sort(key=lambda m: (m["published"], m["found"]), reverse=True)
    (TRK / "moments.json").write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(), "moments": out}, indent=1, ensure_ascii=False) + "\n")
    print(f"tracking/moments.json · {len(out)} moments")


if __name__ == "__main__":
    main()
