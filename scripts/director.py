#!/usr/bin/env python3
"""Narrative Radar — the Director. Builds a story set from YouTube, and edits it by conversation.

    python3 scripts/director.py build "why everyone says bitcoin's 4-year cycle is dead" --budget 60 --write
    python3 scripts/director.py edit four-year-cycle "swap the second spin for something less hyped" --write
    python3 scripts/director.py chat                      # talk to it: first message builds, the rest edit
    python3 scripts/director.py chat four-year-cycle      # talk about a set that already exists

What it is
  The product. A person describes a story in their own words; the Director
  frames it, picks the category's playbook (director/playbooks.json), searches
  YouTube backwards in time for the origin and forwards for the latest, decides
  the turns and the sides, and cuts a three-episode set that ends. Then the
  person can talk to it about the set, and it edits under the same rules.

  It holds no videos. YouTube is the library; what it keeps is the story it
  built (library/<id>.json): the frame, the decisions, the research log, the
  candidate pool it chose from, and the set. That record is what makes the next
  request about the same story instant, and what the navigator will stand on.

The split between model and code
  Judgment is the model's: framing, which video is the origin, what counts as a
  turn, who the sides are and which video argues each at its strongest. Rules
  are code's, so they cannot be talked out of: one video per channel, no Shorts,
  nothing ranked by views, no video the search did not return, and the set ends.
  Every id the model names is checked against what YouTube actually returned.

Budgets (briefs/director/SPEC.md section 5)
  At most 12 searches per new story (1,200 of the 10,000 daily quota units).
  Details cost 1 unit per 50 videos. Edits may spend at most 2 more searches.

Keys
  YT_API_KEY and ANTHROPIC_API_KEY, from the environment or .secrets/
  (youtube-api-key, anthropic-api-key). In GitHub Actions both are secrets
  already; see .github/workflows/director.yml.
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
PLAYBOOKS = json.loads((ROOT / "director" / "playbooks.json").read_text())["playbooks"]
MODEL = os.environ.get("DIRECTOR_MODEL", "claude-opus-5")
WRITE = "--write" in sys.argv
NOW = datetime.now(timezone.utc)

MAX_SEARCHES = 12
MAX_EDIT_SEARCHES = 2
MAX_VIDEO_MIN = 60          # soft cap; longer must be chosen on purpose
SHORT_SECONDS = 180         # Shorts (now up to 3 min) are out of sets (spec, DECIDE 4); budget pressure reached for 78s clips


def flag(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def secret(env, fname):
    v = os.environ.get(env, "").strip()
    if not v:
        p = ROOT / ".secrets" / fname
        if p.exists():
            v = p.read_text().strip()
    return v


# ------------------------------------------------------------------ the log
LOG = []


def say(line):
    """The Director shows its work as it goes (spec section 7)."""
    LOG.append(line)
    print(f"  · {line}", flush=True)


# ------------------------------------------------------------------ YouTube
class Quota:
    def __init__(self, searches):
        self.searches_left, self.units = searches, 0


def yt(endpoint, quota, cost, **params):
    key = secret("YT_API_KEY", "youtube-api-key")
    if not key:
        sys.exit("No YouTube key. Set YT_API_KEY or put it in .secrets/youtube-api-key.")
    params["key"] = key
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?{urllib.parse.urlencode(params)}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                quota.units += cost
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:300]
            if e.code == 403:
                sys.exit(f"YouTube refused ({body}). Usually the daily quota.")
            if attempt == 2:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 * (attempt + 1))


def search(q, quota, before=None, after=None, order="relevance", why=""):
    if quota.searches_left <= 0:
        say(f"search budget spent; skipped “{q}”")
        return []
    quota.searches_left -= 1
    p = {"part": "snippet", "q": q, "type": "video", "maxResults": 50, "order": order,
         "relevanceLanguage": "en", "safeSearch": "moderate", "videoEmbeddable": "true"}
    if before:
        p["publishedBefore"] = before.strftime("%Y-%m-%dT%H:%M:%SZ")
    if after:
        p["publishedAfter"] = after.strftime("%Y-%m-%dT%H:%M:%SZ")
    r = yt("search", quota, 100, **p)
    ids = [it["id"]["videoId"] for it in r.get("items", []) if it.get("id", {}).get("videoId")]
    window = (f" before {before:%Y}" if before else "") + (f" since {after:%b %Y}" if after else "")
    say(f"searched “{q}”{window}{f' — {why}' if why else ''}: {len(ids)} results")
    return ids


def iso_seconds(d):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    dd, h, mi, s = (int(x or 0) for x in m.groups())
    return dd * 86400 + h * 3600 + mi * 60 + s


def details(ids, quota):
    out = {}
    ids = list(dict.fromkeys(ids))
    for i in range(0, len(ids), 50):
        r = yt("videos", quota, 1, part="snippet,contentDetails,status", id=",".join(ids[i:i + 50]), maxResults=50)
        for it in r.get("items", []):
            sn, cd, st = it.get("snippet", {}), it.get("contentDetails", {}), it.get("status", {})
            secs = iso_seconds(cd.get("duration"))
            title = sn.get("title", "")
            out[it["id"]] = {
                "id": it["id"], "title": title, "channel": sn.get("channelTitle", ""),
                "channelId": sn.get("channelId", ""), "published": (sn.get("publishedAt") or "")[:10],
                "seconds": secs, "length": f"{secs // 3600}:{secs % 3600 // 60:02d}:{secs % 60:02d}" if secs >= 3600 else f"{secs // 60}:{secs % 60:02d}",
                "description": (sn.get("description") or "")[:600],
                "live": sn.get("liveBroadcastContent") not in (None, "none"),
                "embeddable": st.get("embeddable", True),
                "short": secs <= SHORT_SECONDS or "#shorts" in title.lower(),
                "lang": (sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "").lower(),
            }
    return out


def usable(v):
    """Hard rules that no conversation can talk the Director out of."""
    if not v or v["live"] or v["short"] or not v["embeddable"] or v["seconds"] <= 0:
        return False
    # English only at launch (spec, DECIDE 5). Search's language setting is a
    # hint, not a filter: the first real build let a German video into a set.
    lang = v.get("lang") or ""
    if lang and not lang.startswith("en"):
        return False
    return not re.search(r"[äöüß]|\b(nicht|und|der|das|ist|pour|para|los)\b", v["title"].lower())


# ------------------------------------------------------------------ Claude
def strict(schema):
    """Structured outputs want every object closed and every field required.
    Done here once, so the schemas below stay readable. Fields that only some
    answers need come back empty, which the code already treats as absent."""
    if isinstance(schema, dict):
        if schema.get("type") == "object" and "properties" in schema:
            schema["additionalProperties"] = False
            schema["required"] = list(schema["properties"])
        for v in schema.values():
            strict(v)
    elif isinstance(schema, list):
        for v in schema:
            strict(v)
    return schema


def claude(system, prompt, schema, effort="medium", max_tokens=8000):
    schema = strict(json.loads(json.dumps(schema)))
    key = secret("ANTHROPIC_API_KEY", "anthropic-api-key")
    if not key:
        sys.exit("No Anthropic key. Set ANTHROPIC_API_KEY or put it in .secrets/anthropic-api-key.")
    body = {"model": MODEL, "max_tokens": max_tokens, "system": system,
            "messages": [{"role": "user", "content": prompt}],
            "output_config": {"format": {"type": "json_schema", "schema": schema}, "effort": effort}}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"}, method="POST")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                m = json.loads(r.read())
            if m.get("parsed_output") is not None:
                return m["parsed_output"]
            text = next((b["text"] for b in m.get("content", []) if b.get("type") == "text"), "{}")
            return json.loads(text)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:400]
            if e.code in (429, 500, 502, 503, 529) and attempt < 2:
                time.sleep(15 * (attempt + 1))
                continue
            sys.exit(f"Claude returned {e.code}: {detail}")
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(10)


SPEC_RULES = """You are the Director of Story Evenings: an AI curator that turns YouTube into story series instead of feeds.
A story is the events; a narrative is one telling of them; a claim is a statement that could turn out true or false.
An origin is the earliest video that STATES the claim, not the earliest on the topic. A turn is a change in the claim
itself (a new cause, villain, deadline, or a reversal); more videos saying the same thing is not a turn. A side is a
distinct position held by more than one channel, represented by its strongest video: first-hand, specific, not a
reaction to a reaction. Stay neutral: never say which side is right, except to state plainly that a prediction's
deadline has passed. Never choose by popularity. Only name video ids that appear in the material you are given.
Write in plain words, no hype."""


# ------------------------------------------------------------------ build
FRAME_SCHEMA = {"type": "object", "properties": {
    "category": {"type": "string", "enum": [p["id"] for p in PLAYBOOKS]},
    "story": {"type": "string", "description": "The story, in a few words"},
    "central_claim": {"type": "string", "description": "The one claim, flat and checkable"},
    "not_about": {"type": "string"},
    "title": {"type": "string", "description": "A short name for the series, 2-5 words, never a question"},
    "queries_now": {"type": "array", "items": {"type": "string"}, "description": "2-3 searches for the latest material"},
    "queries_origin": {"type": "array", "items": {"type": "string"}, "description": "2-3 searches phrased the way the claim was first said"},
    "queries_sides": {"type": "array", "items": {"type": "string"}, "description": "2-3 searches aimed at each side, including the skeptic"},
    "start_year": {"type": "integer", "description": "Best guess of the year the claim first appeared on YouTube"},
    "clarify": {"type": "string", "description": "One question, only if the request is really two stories; otherwise empty"},
}, "required": ["category", "story", "central_claim", "not_about", "title", "queries_now", "queries_origin", "queries_sides", "start_year", "clarify"]}

DECIDE_SCHEMA = {"type": "object", "properties": {
    "origin": {"type": "object", "properties": {
        "videoId": {"type": "string"}, "why": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]}},
        "required": ["videoId", "why", "confidence"]},
    "turns": {"type": "array", "items": {"type": "object", "properties": {
        "date": {"type": "string", "description": "YYYY or YYYY-MM"},
        "change": {"type": "string", "description": "What changed in the claim, under 14 words"},
        "videoId": {"type": "string"}, "why": {"type": "string"}},
        "required": ["date", "change", "videoId", "why"]}},
    "latest": {"type": "array", "items": {"type": "object", "properties": {
        "videoId": {"type": "string"}, "why": {"type": "string"}}, "required": ["videoId", "why"]}},
    "sides": {"type": "array", "items": {"type": "object", "properties": {
        "position": {"type": "string", "description": "Under 12 words"},
        "watch_for": {"type": "string", "description": "The tell: what to notice when this side argues"},
        "videoId": {"type": "string", "description": "The strongest video for this side"},
        "backups": {"type": "array", "items": {"type": "string"}, "description": "Other ids for this side, strongest first"},
        "why": {"type": "string"}},
        "required": ["position", "watch_for", "videoId", "backups", "why"]}},
    "open_question": {"type": "string", "description": "What stays unresolved, in one sentence"},
    "gaps": {"type": "string", "description": "What the material could not establish, if anything"},
}, "required": ["origin", "turns", "latest", "sides", "open_question", "gaps"]}


def playbook(cid):
    return next((p for p in PLAYBOOKS if p["id"] == cid), PLAYBOOKS[-1])


def pb_text(p):
    return (f"Category: {p['name']}\nMethod:\n" + "\n".join(f"- {m}" for m in p["method"])
            + f"\nOrigin means: {p['origin']}\nTurns are: {p['turns']}\nSides are usually: {p['sides']}"
            + f"\nPrefer: {'; '.join(p['prefer'])}\nRed flags: {'; '.join(p['red_flags'])}")


def card(v):
    desc = re.sub(r"\s+", " ", v.get("description") or "")[:260]
    return f"[{v['id']}] {v['published']} · {v['channel']} · {v['length']}\n  {v['title']}\n  {desc}"


def frame(request):
    cats = "\n".join(f"- {p['id']}: {p['name']}" for p in PLAYBOOKS)
    f = claude(SPEC_RULES, f"A person asked for a story: “{request}”\n\nCategories:\n{cats}\n\n"
               "Pick the category, frame the story and its one central claim, say what it is not about, "
               "and write the searches you will run. Origin searches should use the words people used "
               "when the claim first appeared.", FRAME_SCHEMA, effort="medium", max_tokens=3000)
    return f


def gather(f, quota):
    """Search backwards for the origin, across for the sides, forwards for the latest."""
    start = max(2006, min(int(f.get("start_year") or 2018), NOW.year))
    pool = []
    say(f"category: {playbook(f['category'])['name']} · claim: {f['central_claim']}")
    for q in f["queries_now"][:2]:
        pool += search(q, quota, after=NOW - timedelta(days=200), why="latest")
    for q in f["queries_origin"][:3]:
        pool += search(q, quota, before=datetime(start + 2, 1, 1, tzinfo=timezone.utc), order="relevance", why="looking for the origin")
    early = pool[:]
    # Go further back once, in case the claim is older than the guess.
    if f["queries_origin"]:
        pool += search(f["queries_origin"][0], quota, before=datetime(start, 1, 1, tzinfo=timezone.utc), why="checking for anything earlier")
    mid = datetime(start + max(1, (NOW.year - start) // 2), 1, 1, tzinfo=timezone.utc)
    for q in f["queries_origin"][:1]:
        pool += search(q, quota, after=datetime(start + 1, 1, 1, tzinfo=timezone.utc), before=mid, why="the middle years, for turns")
    for q in f["queries_sides"][:3]:
        pool += search(q, quota, why="finding the sides")
    meta = details(pool, quota)
    good = {i: v for i, v in meta.items() if usable(v)}
    say(f"read details of {len(meta)} videos; {len(good)} usable after removing Shorts, live and unembeddable ones")
    return good


def decide(request, f, cands, budget=60):
    p = playbook(f["category"])
    ordered = sorted(cands.values(), key=lambda v: v["published"])
    # One card per channel would hide a channel's own turn, so keep up to 3.
    seen, keep = {}, []
    for v in ordered:
        seen[v["channelId"]] = seen.get(v["channelId"], 0) + 1
        if seen[v["channelId"]] <= 3:
            keep.append(v)
    keep = keep[-220:] if len(keep) > 220 else keep
    say(f"weighing {len(keep)} candidates against the {p['name']} playbook")
    material = "\n".join(card(v) for v in keep)
    return claude(SPEC_RULES + "\n\n" + pb_text(p),
                  f"Request: “{request}”\nStory: {f['story']}\nCentral claim: {f['central_claim']}\nNot about: {f['not_about']}\n\n"
                  f"Candidate videos, oldest first:\n{material}\n\n"
                  "Make the decisions: the origin; the turns (3-6, each with a video from its own period); "
                  "the latest (3-4, newest first); the sides (2-3, each with its strongest video and backups); "
                  "the open question; and the gaps. Judge from titles, descriptions and dates; if the material "
                  "cannot support a decision, say so in gaps rather than guess.\n\n"
                  f"The whole set must fit about {budget} minutes. Everything you pick will not fit, so for each "
                  "turn and side choose the strongest video that is short enough, put the direct counter to the "
                  "claim as the second side, and list backups so a shorter alternative exists. Avoid anything over "
                  "an hour unless nothing else makes the point.",
                  DECIDE_SCHEMA, effort="high", max_tokens=12000)


def clean(d, cands):
    """Drop every id the model named that YouTube did not return."""
    ok = lambda i: i in cands
    if not ok(d["origin"].get("videoId")):
        d["origin"] = None
    d["turns"] = [t for t in d.get("turns", []) if ok(t.get("videoId"))]
    d["latest"] = [x for x in d.get("latest", []) if ok(x.get("videoId"))]
    sides = []
    for s in d.get("sides", []):
        ids = [i for i in [s.get("videoId")] + (s.get("backups") or []) if ok(i)]
        if ids:
            s["videoId"], s["backups"] = ids[0], ids[1:]
            sides.append(s)
    d["sides"] = sides
    return d


def mins(v):
    return v["seconds"] / 60


def assemble(d, cands, budget):
    """Code, not judgment: the per-channel rule, the budget, the ending.

    One budget across the whole set, filled in order of what a set cannot do
    without: the origin, then both main sides, then the latest, then the turns,
    then a third side and more of the latest. The first real build cut episodes
    one at a time and always kept each one's first video, so a 64-minute podcast
    took "Where it stands" alone, the main counter-side was dropped, and a
    60-minute request came back at 111. Within each slot, the first candidate
    that fits wins, so a backup stands in for a video that is too long."""
    used_ch, used_id, total = set(), set(), [0.0]
    cap = budget * 1.1

    def fits(vid, long_ok=False):
        v = cands.get(vid)
        if not v or vid in used_id or v["channelId"] in used_ch:
            return None
        m = mins(v)
        if m > MAX_VIDEO_MIN and not long_ok:
            return None
        if total[0] + m > cap:
            return None
        return v

    def take(ids, role, why, extra=None):
        for long_ok in (False, True):
            for vid in ids:
                v = fits(vid, long_ok)
                if v:
                    used_id.add(vid); used_ch.add(v["channelId"]); total[0] += mins(v)
                    return {"videoId": vid, "title": v["title"], "channel": v["channel"], "length": v["length"],
                            "published": v["published"], "role": role, "why": why, **(extra or {})}
        return None

    sides = d.get("sides", [])[:3]
    roles = ["The claim, at its strongest", "The strongest answer to it", "A third reading"]
    side_item = lambda i: take([sides[i]["videoId"]] + sides[i].get("backups", []), roles[i], sides[i]["why"],
                               {"side": sides[i]["position"], "watch_for": sides[i]["watch_for"]})
    latest = d.get("latest", [])
    picked = {"origin": [], "turns": [], "now": [], "sides": [None, None, None]}

    if d.get("origin"):
        picked["origin"].append(take([d["origin"]["videoId"]], "Where it began", d["origin"]["why"]))
    for i in range(min(2, len(sides))):
        picked["sides"][i] = side_item(i)
    if latest:
        picked["now"].append(take([x["videoId"] for x in latest], "Where it stands", latest[0]["why"]))
    for t in sorted(d.get("turns", []), key=lambda t: t["date"]):
        picked["turns"].append(take([t["videoId"]], f"{t['date']}. {t['change']}", t["why"]))
    if len(sides) > 2:
        picked["sides"][2] = side_item(2)
    for x in latest[1:]:
        picked["now"].append(take([x["videoId"]], "Also new", x["why"]))

    eps = [
        {"key": "origin", "title": "Origin", "about": "How the story got here, oldest first.",
         "videos": [x for x in picked["origin"] + sorted([t for t in picked["turns"] if t], key=lambda t: t["published"]) if x]},
        {"key": "now", "title": "Where it stands", "about": "The newest material, one per channel.",
         "videos": [x for x in picked["now"] if x]},
        {"key": "sides", "title": "The sides", "about": "Each position at its strongest, with what to watch for.",
         "videos": [x for x in picked["sides"] if x]},
    ]
    for e in eps:
        e["minutes"] = round(sum(mins(cands[v["videoId"]]) for v in e["videos"]))
    dropped = [s_["position"] for i, s_ in enumerate(sides) if not picked["sides"][i]]
    if dropped:
        say(f"budget could not fit the side(s): {'; '.join(dropped)}")
    return eps


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48] or "story"


def show(story):
    print(f"\n{story['title']}  ·  {story['category_name']}  ·  {sum(e['minutes'] for e in story['episodes'])} min")
    print(f"Claim: {story['central_claim']}")
    for k, e in enumerate(story["episodes"], 1):
        print(f"\n  Episode {k} · {e['title']} · {e['minutes']} min")
        for v in e["videos"]:
            print(f"    {v['published']}  {v['length']:>7}  {v['channel'][:22]:22}  {v['title'][:60]}")
            print(f"        {v['role']} — {v['why'][:110]}")
            if v.get("watch_for"):
                print(f"        look out for: {v['watch_for'][:110]}")
    print(f"\n  Stays open: {story['open_question']}")
    if story.get("gaps"):
        print(f"  Couldn't establish: {story['gaps']}")
    print("  That's the set. Nothing plays after it.")


def save(story):
    LIB.mkdir(exist_ok=True)
    p = LIB / f"{story['id']}.json"
    if p.exists():
        old = json.loads(p.read_text())
        story["history"] = old.get("history", []) + [{"version": old.get("version", 1), "at": old.get("updated"),
                                                       "episodes": old["episodes"], "note": old.get("last_change", "built")}]
    p.write_text(json.dumps(story, indent=1, ensure_ascii=False) + "\n")
    print(f"\nsaved {p.relative_to(ROOT)}")


def build(request, budget=60, category=None):
    LOG.clear()
    quota = Quota(MAX_SEARCHES)
    say(f"request: “{request}” · {budget} minutes")
    f = frame(request)
    if category:
        f["category"] = category
    if f.get("clarify"):
        say(f"would ask: {f['clarify']} (building the most likely reading meanwhile)")
    cands = gather(f, quota)
    if len(cands) < 6:
        sys.exit("Too little usable material to build a set. Try rewording the request.")
    d = clean(decide(request, f, cands, budget), cands)
    eps = assemble(d, cands, budget)
    pb = playbook(f["category"])
    story = {
        "id": slug(f["title"]), "version": 1, "title": f["title"], "request": request,
        "category": pb["id"], "category_name": pb["name"], "story": f["story"],
        "central_claim": f["central_claim"], "not_about": f["not_about"], "budget": budget,
        "episodes": eps, "sides": d["sides"], "turns": d["turns"], "open_question": d["open_question"],
        "gaps": d.get("gaps", ""), "clarify": f.get("clarify", ""),
        "built": NOW.strftime("%Y-%m-%d"), "updated": NOW.strftime("%Y-%m-%d"), "model": MODEL,
        "quota_units": quota.units, "searches": MAX_SEARCHES - quota.searches_left,
        "research_log": LOG[:],
        # The pool it chose from: edits draw on this before spending a search.
        "candidates": {i: {k: v[k] for k in ("id", "title", "channel", "channelId", "published", "seconds", "length", "description", "lang")}
                       for i, v in cands.items()},
    }
    say(f"spent {story['searches']} searches, {quota.units} quota units")
    show(story)
    if WRITE:
        save(story)
    return story


# ------------------------------------------------------------------ edit
EDIT_SCHEMA = {"type": "object", "properties": {
    "reply": {"type": "string", "description": "What you say back to the person, plainly, in 1-3 sentences"},
    "ops": {"type": "array", "items": {"type": "object", "properties": {
        "op": {"type": "string", "enum": ["remove", "replace", "add", "move", "budget", "search"]},
        "episode": {"type": "string", "enum": ["origin", "now", "sides", ""]},
        "videoId": {"type": "string", "description": "The video to remove, replace, or move"},
        "newVideoId": {"type": "string", "description": "For replace or add: a candidate id"},
        "role": {"type": "string"}, "why": {"type": "string"},
        "to": {"type": "integer", "description": "For move: new position, 1-based"},
        "minutes": {"type": "integer", "description": "For budget"},
        "query": {"type": "string", "description": "For search: what to look for, if no candidate fits"}},
        "required": ["op"]}},
}, "required": ["reply", "ops"]}


def apply_ops(story, ops):
    cands = story["candidates"]
    eps = {e["key"]: e for e in story["episodes"]}
    in_set = lambda: {v["videoId"] for e in story["episodes"] for v in e["videos"]}
    channels = lambda: {cands[v["videoId"]]["channelId"] for e in story["episodes"] for v in e["videos"] if v["videoId"] in cands}
    done = []
    for o in ops:
        op, ep = o.get("op"), eps.get(o.get("episode") or "")
        if op == "budget" and o.get("minutes"):
            story["budget"] = int(o["minutes"]); done.append(f"budget → {story['budget']} min")
        elif op == "remove":
            for e in story["episodes"]:
                before = len(e["videos"])
                e["videos"] = [v for v in e["videos"] if v["videoId"] != o.get("videoId")]
                if len(e["videos"]) < before:
                    done.append(f"removed {o['videoId']}")
        elif op in ("replace", "add"):
            nv = o.get("newVideoId")
            v = cands.get(nv)
            if not v:
                done.append(f"skipped {nv}: not a video the search returned"); continue
            if nv in in_set():
                done.append(f"skipped {nv}: already in the set"); continue
            old_ch = None
            if op == "replace":
                for e in story["episodes"]:
                    for x in e["videos"]:
                        if x["videoId"] == o.get("videoId"):
                            old_ch = cands.get(x["videoId"], {}).get("channelId")
            if v["channelId"] in channels() and v["channelId"] != old_ch:
                done.append(f"skipped {nv}: that channel is already in the set"); continue
            if v["seconds"] <= SHORT_SECONDS:
                done.append(f"skipped {nv}: Shorts stay out of sets"); continue
            item = {"videoId": nv, "title": v["title"], "channel": v["channel"], "length": v["length"],
                    "published": v["published"], "role": o.get("role") or "", "why": o.get("why") or ""}
            if op == "replace":
                for e in story["episodes"]:
                    for k, x in enumerate(e["videos"]):
                        if x["videoId"] == o.get("videoId"):
                            item["role"] = item["role"] or x["role"]
                            for keep in ("side", "watch_for"):
                                if x.get(keep):
                                    item[keep] = x[keep]
                            e["videos"][k] = item
                            done.append(f"replaced {o['videoId']} with {nv}")
            elif ep is not None:
                ep["videos"].append(item); done.append(f"added {nv} to {ep['title']}")
        elif op == "move" and ep is not None:
            vs = ep["videos"]
            k = next((i for i, x in enumerate(vs) if x["videoId"] == o.get("videoId")), None)
            if k is not None:
                x = vs.pop(k); vs.insert(max(0, min(len(vs), int(o.get("to") or 1) - 1)), x)
                done.append(f"moved {o['videoId']} to position {o.get('to')}")
    for e in story["episodes"]:
        e["minutes"] = round(sum(cands[v["videoId"]]["seconds"] / 60 for v in e["videos"] if v["videoId"] in cands))
    return done


def edit(story, instruction):
    LOG.clear()
    cands = story["candidates"]
    current = "\n".join(f"{e['key']}: " + "; ".join(f"[{v['videoId']}] {v['title'][:70]} ({v['channel']}, {v['length']}) — {v['role']}"
                                                      for v in e["videos"]) for e in story["episodes"])
    unused = [v for i, v in cands.items() if i not in {x["videoId"] for e in story["episodes"] for x in e["videos"]}]
    unused = sorted(unused, key=lambda v: v["published"])[-160:]
    pool = "\n".join(card({**v, "description": v.get("description", "")}) for v in unused)
    sys_p = SPEC_RULES + "\n\n" + pb_text(playbook(story["category"])) + (
        "\n\nYou are editing a set with the person who asked for it. Do what they ask within the rules. "
        "Use candidates from the pool; only use op 'search' if nothing in the pool fits. If a request "
        "would break a rule (Shorts, a second video from the same channel, ranking by views), say so and offer the nearest thing. "
        "Never change the time budget unless the person asks; if their request will not fit, make the closest edit that "
        "fits, by swapping or trimming, and offer the longer version in your reply.")
    msg = (f"Set: {story['title']} — claim: {story['central_claim']} — budget {story['budget']} min\n\nCurrent set:\n{current}\n\n"
           f"Unused candidates:\n{pool}\n\nThe person says: “{instruction}”")
    r = claude(sys_p, msg, EDIT_SCHEMA, effort="medium", max_tokens=4000)
    searches = [o for o in r["ops"] if o.get("op") == "search" and o.get("query")][:MAX_EDIT_SEARCHES]
    if searches:
        quota = Quota(MAX_EDIT_SEARCHES)
        ids = []
        for o in searches:
            ids += search(o["query"], quota, why="looking for something the pool lacked")
        new = {i: v for i, v in details(ids, quota).items() if usable(v)}
        for i, v in new.items():
            cands[i] = {k: v[k] for k in ("id", "title", "channel", "channelId", "published", "seconds", "length", "description", "lang")}
        pool = "\n".join(card(v) for v in sorted(new.values(), key=lambda v: v["published"]))
        r = claude(sys_p, msg + f"\n\nYou searched and found:\n{pool}\n\nNow make the edit with these.", EDIT_SCHEMA,
                   effort="medium", max_tokens=4000)
    ops = [o for o in r["ops"] if o.get("op") != "search"]
    # The time limit is the person's, never the Director's. In the first edit
    # test it raised a 60-minute set to 95 on its own to fit a new side. A
    # budget change now stands only when the person's message is about time.
    asked_time = re.search(r"\d+\s*(m\b|min|minute|hour|hr)|longer|shorter|more time|less time|quick|budget", instruction.lower())
    if not asked_time and any(o.get("op") == "budget" for o in ops):
        ops = [o for o in ops if o.get("op") != "budget"]
        say("kept your time limit; the Director may only change it when you ask")
    done = apply_ops(story, ops)
    over = sum(e["minutes"] for e in story["episodes"]) - story["budget"] * 1.1
    if over > 0:
        r["reply"] += f" This runs about {round(over)} minutes over your {story['budget']}; say 'make it fit' and I'll trim, or give me a longer time."
    story["version"] = story.get("version", 1) + 1
    story["updated"] = NOW.strftime("%Y-%m-%d")
    story["last_change"] = instruction
    story.setdefault("conversation", []).append({"you": instruction, "director": r["reply"], "changes": done})
    print(f"\nDirector: {r['reply']}")
    for d_ in done:
        print(f"  · {d_}")
    show(story)
    if WRITE:
        save(story)
    return story


def load(sid):
    p = LIB / f"{sid}.json"
    if not p.exists():
        sys.exit(f"No set called {sid} in library/.")
    return json.loads(p.read_text())


def chat(sid=None):
    global WRITE
    WRITE = True
    story = load(sid) if sid else None
    print("Talk to the Director. Describe a story to build one; once it exists, ask for changes. Empty line to leave.\n")
    while True:
        try:
            line = input("you › ").strip()
        except EOFError:
            break
        if not line:
            break
        story = edit(story, line) if story else build(line, int(flag("--budget", 60)))


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--") and x not in (flag("--budget"), flag("--category"))]
    if not a:
        sys.exit(__doc__)
    mode = a[0]
    if mode == "build" and len(a) > 1:
        build(a[1], int(flag("--budget", 60)), flag("--category"))
    elif mode == "edit" and len(a) > 2:
        edit(load(a[1]), a[2])
    elif mode == "chat":
        chat(a[1] if len(a) > 1 else None)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
