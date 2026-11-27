#!/usr/bin/env python3
"""Story Evenings: does this person speak about the subject in this video, and where?

    GEMINI_API_KEY=... python3 scripts/find_mentions.py <name> "<subject>" <videoId> [<videoId> ...] [--model m]

A summary watch keeps a handful of claims and can drop a few minutes on a side
topic. So before saying "X never speaks about Y" (I said it about Jimi Wanjigi
and the infrastructure fund on the strength of six summaries; Malik believed
otherwise), ask the direct question of each full video.

Writes watch/mentions/<name>/<videoId>.json. A video already searched is skipped.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gemini import ApiError, Budget, DailyLimit, ask, key, payload  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODEL = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--model"), "gemini-3-flash-preview")
SCHEMA = {"type": "object", "properties": {
    "speaks_about_it": {"type": "boolean", "description": "The named person talks about the subject at least once in this video"},
    "stretches": {"type": "array", "description": "EVERY stretch where the named person talks about the subject, in order; empty if none",
        "items": {"type": "object", "properties": {
            "start": {"type": "string", "description": "MM:SS (or H:MM:SS) of the first word, ideally the question that prompts it"},
            "end": {"type": "string", "description": "MM:SS just after the sentence that ends the point"},
            "says": {"type": "string", "description": "What they say about the subject, in one or two plain sentences"},
            "quote": {"type": "string", "description": "Their key sentence, word for word"},
            "which": {"type": "string", "description": "Which part of the subject: the fund, the Safaricom sale, privatisation, the sovereign wealth fund, other"}},
            "required": ["start", "end", "says", "quote", "which"]}},
    "searched_whole_video": {"type": "boolean", "description": "You could watch the whole video, start to end"},
    "note": {"type": "string"}},
    "required": ["speaks_about_it", "stretches", "searched_whole_video", "note"]}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a != MODEL]
    name, subject, vids = args[0], args[1], args[2:]
    out = ROOT / "watch" / "mentions" / name.lower().replace(" ", "-"); out.mkdir(parents=True, exist_ok=True)
    k, budget = key(), Budget()
    for v in vids:
        f = out / f"{v}.json"
        if f.exists():
            continue
        prompt = (f"Watch this whole video carefully. Find every stretch where {name} talks about: {subject}. "
                  "Include passing remarks of a sentence or two as well as long answers. Give exact timestamps and their own words. "
                  "If they never talk about it, say so. Do not report what other people in the video say.")
        try:
            r = ask(MODEL, [{"type": "text", "text": prompt}, {"type": "video", "uri": f"https://www.youtube.com/watch?v={v}"}], SCHEMA, k, budget=budget, est_tokens=250000)
        except DailyLimit:
            print("out of requests on this model"); return
        except ApiError as ex:
            print(f"  {v} skipped ({ex.code}): {ex.detail[:90]}"); continue
        d = payload(r)
        if not d:
            print(f"  {v} unparsed"); continue
        f.write_text(json.dumps({"videoId": v, "person": name, "subject": subject, "found": d}, indent=1, ensure_ascii=False))
        print(f"  {v} {'YES' if d['speaks_about_it'] else 'no '} · {len(d['stretches'])} stretches · whole video: {d['searched_whole_video']}", flush=True)
        for s in d["stretches"]:
            print(f"      {s['start']}-{s['end']} [{s['which']}] {s['quote'][:110]}", flush=True)


if __name__ == "__main__":
    main()
