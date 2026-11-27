#!/usr/bin/env python3
"""Story Evenings: check every cut in an evening before it ships.

    GEMINI_API_KEY=... python3 scripts/cut_check.py <page.html> <series-id> [--model m]

The first watch says roughly where a point is made. That is not good enough to
cut on: clips opened on jingles and stopped mid-thought (Malik, 2026-11-27:
"the ending of this video was vague... poor curation/directing"). This is the
director's second look. For each cut it re-watches the video and reports the
exact first and last sentence of the window, whether each is a clean place to
start and stop, and a better time when it is not.

Writes watch/cuts/<series>/<videoId>.json; a cut already checked at the same
start/end is not checked again.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gemini import ApiError, Budget, DailyLimit, ask, key, payload, video_tokens  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODEL = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--model"), "gemini-3-flash-preview")
mm = lambda s: f"{s // 60}:{s % 60:02d}"
SCHEMA = {"type": "object", "properties": {
    "first_words": {"type": "string", "description": "The first full sentence spoken at or just after the start time, word for word"},
    "start_clean": {"type": "boolean", "description": "The start lands on the first word of a sentence or question, with no intro music, channel sting, greeting or half sentence"},
    "better_start": {"type": "string", "description": "MM:SS of the first word of the sentence where this point really begins, ideally a question being asked; same as the given start if it is already clean"},
    "last_words": {"type": "string", "description": "The last full sentence that finishes before the end time, word for word"},
    "end_clean": {"type": "boolean", "description": "The clip ends just after a sentence that concludes the point: a conclusion, a number, a verdict. Not a lead-in to the next topic, not mid-sentence, not a sign-off or 'thank you'"},
    "better_end": {"type": "string", "description": "MM:SS just after the last word of the strongest concluding sentence for this point, within about 30 seconds either side of the given end; same as the given end if it is already clean"},
    "better_end_line": {"type": "string", "description": "That concluding sentence, word for word"},
    # The relevance gate (Malik, 2026-11-27: "some of the Jimi Wanjigi interviews, he is
    # not at all talking about the infrastructure fund"). A famous name is not
    # relevance. The speaker must be talking about THIS story inside the window.
    "on_subject": {"type": "string", "enum": ["yes", "partly", "no"],
                   "description": "Inside this window, is the speaker talking about the evening's own subject (named below)? 'partly' = a neighbouring topic that only touches it; 'no' = a different subject, however related the speaker"},
    "subject_quote": {"type": "string", "description": "The words in the window that name or clearly refer to the subject, word for word; empty if there are none"},
    "note": {"type": "string", "description": "One short sentence on what was wrong, or empty"}},
    "required": ["first_words", "start_clean", "better_start", "last_words", "end_clean", "better_end", "better_end_line", "on_subject", "subject_quote", "note"]}


def secs(L):
    q = [int(x) for x in str(L).split(":")]
    return q[0] * 60 + q[1] if len(q) == 2 else q[0] * 3600 + q[1] * 60 + q[2]


def main():
    page, sid = Path(sys.argv[1]), sys.argv[2]
    s = page.read_text(); i = s.find('{"id": "%s"' % sid)
    obj, _ = json.JSONDecoder().raw_decode(s, i)
    out = ROOT / "watch" / "cuts" / sid; out.mkdir(parents=True, exist_ok=True)
    k, budget = key(), Budget()
    for e in obj["eps"]:
        for v in e["videos"]:
            a, b = v.get("start", 0), v.get("end") or secs(v["length"])
            # One source can give several pieces, so a check belongs to a piece (source + start).
            f = out / f"{v['id']}_{a}.json"
            old = out / f"{v['id']}.json"
            # Already checked at this cut, or this cut IS a correction a check produced:
            # either way do not watch it again. (Applying a correction used to make the
            # piece look new, so it was re-watched and nudged again: wasted watches.)
            done = False
            for cand in list(out.glob(f"{v['id']}*.json")):
                j = json.loads(cand.read_text())
                bs, be = j["check"].get("better_start"), j["check"].get("better_end")
                same = lambda q, sec: q and ":" in q and abs(sum(int(n) * m for n, m in zip(reversed(q.split(":")), (1, 60, 3600))) - sec) <= 3
                if j.get("cut") == [a, b] or j.get("applied") == [a, b] or (same(bs, a) and same(be, b)) or (j.get("cut", [None])[0] == a and same(be, b)) or (same(bs, a) and j.get("cut", [None, None])[1] == b):
                    done = True; break
            if done:
                continue
            prompt = (f"A curated evening uses this video from {mm(a)} to {mm(b)}"
                      + (f", as a piece named “{v['name']}”" if v.get("name") else "") + f". Its job in the evening: “{v['role']}”: {v['why']}\n"
                      f"The evening's subject: “{obj['name']}”: {obj.get('claim', '')}\n"
                      "Watch that window closely (and about 30 seconds either side). Say whether the speaker is on that subject inside the window, quoting the words. Report the exact first and last full sentence, "
                      "whether the start and the end are clean places to cut, and better times if they are not. The viewer is busy: "
                      "the clip should open on the question or the first word of the point, and close on the sentence that lands it.")
            try:
                r = ask(MODEL, [{"type": "text", "text": prompt}, {"type": "video", "uri": f"https://www.youtube.com/watch?v={v['id']}"}],
                        SCHEMA, k, budget=budget, est_tokens=video_tokens(v.get("length")))
            except DailyLimit:
                print("out of requests on this model"); return
            except ApiError as ex:
                print(f"  skipped ({ex.code}) {v['channel'][:20]}"); continue
            d = payload(r)
            if not d:
                continue
            f.write_text(json.dumps({"videoId": v["id"], "channel": v["channel"], "cut": [a, b], "check": d}, indent=1, ensure_ascii=False))
            if d.get("on_subject") != "yes": print(f"  ** {d.get('on_subject', '?').upper()} on subject: {v.get('name') or v['title'][:50]}", flush=True)
            print(f"  {v['channel'][:18]:18} {mm(a)}-{mm(b)} start {'ok' if d['start_clean'] else '-> ' + d['better_start']} · end {'ok' if d['end_clean'] else '-> ' + d['better_end']}", flush=True)


if __name__ == "__main__":
    main()
