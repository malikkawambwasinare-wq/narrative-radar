#!/usr/bin/env python3
"""Narrative Radar — watch every video in a built set, so the pairing can be checked.

    python3 scripts/set_watch.py the-four-year-cycle-debate
    python3 scripts/set_watch.py the-four-year-cycle-debate --model gemini-3.6-flash

Why this exists
  The Director builds a set from titles and descriptions. That is enough to find
  candidates and not enough to know a set is good: a title can promise a claim
  the video never makes, two videos can say the same thing, and a "side" can be
  a sales pitch. This is step two of the teaching loop (build, watch, check,
  fix): Gemini watches each video and answers the questions a pairing depends
  on, in the same shape for every video, so the set can be judged as a whole.

What it asks of each video
  what it actually argues; whether it does the job the Director gave it; its
  format; how much of the runtime is on the story; whether it stands alone or
  assumes you have seen something else; who and what it answers; its claims
  with timestamps; and the best stretch to watch if only part is worth it.

What it writes
  watch/<set>/<videoId>.json   one per video (local; derived third-party text
                               stays out of the public repo)
  A video already watched is never watched again.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gemini import ApiError, Budget, DailyLimit, ask, key, payload, spend, video_tokens

ROOT = Path(__file__).resolve().parent.parent
MODEL = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--model"), "gemini-3.8-flash")

SCHEMA = {"type": "object", "properties": {
    "argues": {"type": "string", "description": "What this video actually argues, in two sentences"},
    "does_its_job": {"type": "string", "enum": ["yes", "partly", "no"],
                     "description": "Does the video do the job it was given in the set?"},
    "job_note": {"type": "string", "description": "Why, in one sentence. If the title promises something the video does not deliver, say so"},
    "format": {"type": "string", "enum": ["documentary", "informational", "primary_source", "interview", "debate",
                                          "investigation", "testimony", "lecture", "commentary", "news_report"]},
    "first_hand": {"type": "boolean", "description": "The speaker makes the case themselves, rather than reacting to someone else's video"},
    "on_story_percent": {"type": "integer", "description": "Roughly what share of the runtime is about this story, 0-100"},
    "starts_at": {"type": "string", "description": "MM:SS where the substance begins, after intros and sponsor reads"},
    "best_stretch": {"type": "string", "description": "MM:SS-MM:SS of the part most worth watching for this story"},
    "stands_alone": {"type": "boolean", "description": "A newcomer could follow it without having seen anything else"},
    "assumes": {"type": "string", "description": "What it assumes the viewer already knows, if anything"},
    "answers": {"type": "string", "description": "The person, video or argument it is responding to, if any"},
    "sells": {"type": "string", "description": "What it pitches (course, group, exchange link, fund), or empty"},
    "claims": {"type": "array", "items": {"type": "object", "properties": {
        "text": {"type": "string"}, "timestamp": {"type": "string"},
        "own": {"type": "boolean", "description": "The channel's own claim, not reported from someone else"},
        "prediction": {"type": "boolean"},
        "deadline": {"type": "string", "description": "Only if said out loud; else empty"}},
        "required": ["text", "timestamp", "own", "prediction", "deadline"]}},
    # Where a cut can open and close. Malik's rule (2026-11-14): start a piece on the
    # words that set it up, ideally the question itself being asked out loud
    # ("What is the Bitcoin halving?"), and end on a line that hands over.
    "entry_points": {"type": "array", "description": "Up to 4 moments a clip could START on: the speaker asks the question, defines the term, or states the point in one clean sentence",
        "items": {"type": "object", "properties": {
            "timestamp": {"type": "string", "description": "MM:SS of the first word"},
            "line": {"type": "string", "description": "The sentence as spoken, word for word, under 25 words"},
            "kind": {"type": "string", "enum": ["question", "definition", "claim", "setup"]}},
            "required": ["timestamp", "line", "kind"]}},
    "exit_points": {"type": "array", "description": "Up to 3 moments a clip could END on: a finished thought, a conclusion, or a line that raises the next question",
        "items": {"type": "object", "properties": {
            "timestamp": {"type": "string", "description": "MM:SS just after the last word"},
            "line": {"type": "string", "description": "The sentence as spoken, under 25 words"}},
            "required": ["timestamp", "line"]}},
    # Malik's rule (2026-11-15): the best clips are professionals saying something
    # the public does not know. So the watch step names who is speaking and what
    # qualifies them, and marks the moments where they share inside knowledge.
    "speakers": {"type": "array", "description": "Who speaks at length, and what qualifies them on this topic",
        "items": {"type": "object", "properties": {
            "name": {"type": "string"},
            "credential": {"type": "string", "description": "Their profession and role as stated or shown in the video; empty if never established"},
            "practises": {"type": "boolean", "description": "They work in this field (clinician, researcher, fund manager, engineer), rather than commenting on it"}},
            "required": ["name", "credential", "practises"]}},
    "insights": {"type": "array", "description": "Up to 5 moments where a professional says something a general viewer is unlikely to know: how things work on the inside, what the data shows, what practitioners see",
        "items": {"type": "object", "properties": {
            "start": {"type": "string", "description": "MM:SS of the first word"},
            "end": {"type": "string", "description": "MM:SS where the thought finishes"},
            "speaker": {"type": "string"},
            "insight": {"type": "string", "description": "What they reveal, in one plain sentence"},
            "opening_line": {"type": "string", "description": "The first sentence as spoken"},
            "why_unknown": {"type": "string", "description": "Why the public would not know this, in a few words"}},
            "required": ["start", "end", "speaker", "insight", "opening_line", "why_unknown"]}},
    # Malik's rule (2026-11-17): a thread is a trailer of the narrative. It wants the
    # famous names at their most quotable: the 10-40 second line that would be
    # quoted in a headline, said by the person themselves, as a complete thought.
    "soundbites": {"type": "array", "description": "Up to 4 lines a trailer for this story would use: a well-known person saying, in their own voice, the line that would be quoted in a headline. 10-40 seconds each, a complete thought",
        "items": {"type": "object", "properties": {
            "start": {"type": "string", "description": "MM:SS of the first word, not before"},
            "end": {"type": "string", "description": "MM:SS just after the last word of the thought"},
            "speaker": {"type": "string"},
            "line": {"type": "string", "description": "The key sentence, word for word"},
            "stance": {"type": "string", "description": "What side of the story this line puts them on, in a few words"},
            "on_camera": {"type": "boolean", "description": "The speaker is seen and heard saying it (not quoted or read out by someone else)"}},
            "required": ["start", "end", "speaker", "line", "stance", "on_camera"]}},
    # Malik's rule (2026-11-27): the unit is the PIECE, not the video. One podcast
    # can hold several pieces on related topics; each gets its own name and goes
    # where it belongs (origin, catch-up, the critics...). So the watcher cuts a
    # long video into its separate pieces instead of naming one best stretch.
    "pieces": {"type": "array", "description": "Every separate stretch worth using on its own, in order. A stretch is one topic, 20 seconds to 6 minutes, that makes sense without the rest. A short single-topic video has one piece; a long interview may have five or more",
        "items": {"type": "object", "properties": {
            "start": {"type": "string", "description": "MM:SS of the first word, ideally the question that sets it up"},
            "end": {"type": "string", "description": "MM:SS just after the sentence that lands the point"},
            "name": {"type": "string", "description": "A plain title for this piece, under 12 words, saying what is said; a striking direct quote is fine"},
            "speaker": {"type": "string"},
            "topic": {"type": "string", "description": "What this stretch is about, in a few words"},
            "belongs": {"type": "string", "enum": ["origin", "catch-up", "the case for", "the critics", "experts and evidence", "ordinary people", "what is being built"],
                        "description": "Where it sits in a story told as origin, catch-up and the other camps"},
            "opens_on": {"type": "string", "description": "The first sentence, word for word"},
            "closes_on": {"type": "string", "description": "The last sentence, word for word"}},
            "required": ["start", "end", "name", "speaker", "topic", "belongs", "opens_on", "closes_on"]}},
    "evidence": {"type": "string", "description": "What evidence is shown on screen or cited: charts, data, studies, none"},
    "tone": {"type": "string", "enum": ["measured", "confident", "hyped", "alarmed"]},
}, "required": ["argues", "does_its_job", "job_note", "format", "first_hand", "on_story_percent", "starts_at",
                "best_stretch", "stands_alone", "assumes", "answers", "sells", "claims", "entry_points", "exit_points", "speakers", "insights", "soundbites", "pieces", "evidence", "tone"]}


# Malik (2026-11-25), on the state-hacking timeline: "and where exactly", "which
# industries". With --incident the watcher also records the event itself.
INCIDENT = {"type": "object", "description": "The hacking incident this video is mainly about",
    "properties": {
        "year": {"type": "string"},
        "name": {"type": "string", "description": "What it is usually called (Stuxnet, OPM breach, SolarWinds)"},
        "attacker": {"type": "string", "description": "Who did it, as the video says; say 'alleged' if attribution is disputed"},
        "attacker_country": {"type": "string"},
        "target": {"type": "string", "description": "The organisation(s) hit"},
        "target_country": {"type": "string"},
        "industry": {"type": "string", "enum": ["government", "defence", "intelligence", "energy", "telecom", "finance", "health",
                                                "media & entertainment", "elections & politics", "technology", "transport", "many"]},
        "taken": {"type": "string", "description": "What was stolen, broken or exposed, in one plain sentence"},
        "disputed": {"type": "string", "description": "What, if anything, the video says is disputed or overstated; else empty"}},
    "required": ["year", "name", "attacker", "attacker_country", "target", "target_country", "industry", "taken", "disputed"]}
if "--incident" in sys.argv:
    SCHEMA["properties"]["incident"] = INCIDENT
    SCHEMA["required"] = SCHEMA["required"] + ["incident"]


def main():
    sid = next((a for a in sys.argv[1:] if not a.startswith("--") and a != MODEL), None)
    if not sid:
        sys.exit(__doc__)
    story = json.loads((ROOT / "library" / f"{sid}.json").read_text())
    out = ROOT / "watch" / sid
    out.mkdir(parents=True, exist_ok=True)
    k, budget = key(), Budget()
    todo = [(e, v) for e in story["episodes"] for v in e["videos"]]
    print(f"{story['title']}: {len(todo)} videos · model {MODEL}")
    cost = 0.0
    for n, (e, v) in enumerate(todo, 1):
        f = out / f"{v['videoId']}.json"
        if f.exists():
            print(f"  [{n}/{len(todo)}] watched  {v['title'][:60]}")
            continue
        prompt = (f"You are checking one video inside a curated set about this story.\n"
                  f"Story claim: {story['central_claim']}\n"
                  f"This video's place: episode “{e['title']}”, job: “{v['role']}”.\n"
                  f"Why it was chosen (from its title and description only): {v.get('why', '')}\n\n"
                  "Watch it and report what is actually in it. Be strict about does_its_job: the choice was made "
                  "without watching, so say plainly if the video does not deliver what its title promised. "
                  "List the main claims with timestamps (at most 8). Give deadlines only if said out loud. "
                  "Timestamps must be exact to the second: a clip will open on the start you give.")
        print(f"  [{n}/{len(todo)}] watching {v['title'][:60]}")
        try:
            r = ask(MODEL, [{"type": "text", "text": prompt}, {"type": "video", "uri": f"https://www.youtube.com/watch?v={v['videoId']}"}],
                    SCHEMA, k, budget=budget, est_tokens=video_tokens(v.get("length")))
        except DailyLimit:
            print("      out of requests for today on this model; run again with --model or tomorrow")
            break
        except ApiError as ex:
            print(f"      skipped ({ex.code}): {ex.detail[:120]}")
            continue
        d = payload(r)
        if not d:
            print("      unparsed"); continue
        cost += spend(r)
        f.write_text(json.dumps({"videoId": v["videoId"], "title": v["title"], "channel": v["channel"], "length": v["length"],
                                 "published": v["published"], "episode": e["key"], "role": v["role"], "watch": d}, indent=1, ensure_ascii=False))
        print(f"      {d['does_its_job']:6} · {d['format']} · {d['on_story_percent']}% on story · {d['tone']}{' · sells: ' + d['sells'][:40] if d['sells'] else ''}")
    print(f"done · ${cost:.3f}")


if __name__ == "__main__":
    main()
