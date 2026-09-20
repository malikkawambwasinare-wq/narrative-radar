#!/usr/bin/env python3
"""Narrative Radar — can Gemini read a YouTube video well enough to extract a claim?

    python3 scripts/gemini_pilot.py --list-models   # check the key works
    python3 scripts/gemini_pilot.py                 # 10 videos, dry run, prints the read
    python3 scripts/gemini_pilot.py --write         # also save each read to .cache/

Why this exists
  We cannot fetch captions from YouTube — the API does not serve other people's
  captions and scraping them is a terms violation (SYSTEM.md section 6). But the
  Gemini API accepts a YouTube URL as video input: Google ingests the video on
  their side, we never touch YouTube. If the read is good enough, the wall that
  has kept us at 187 graded videos out of 72,437 comes down.

  This script answers one question before we spend anything: does a model's read
  of the video beat what we already get from the title?

How it judges that
  Half the sample is drawn from the 176 videos that already carry a transcript on
  disk, so the read can be checked against what was actually said. The other half
  has no transcript, which is the real-world case. Every run prints, per video:
  the title (what the engine sees today), Gemini's claim, and — where we have one
  — the first minutes of the true transcript to check it against.

  Those 176 transcripts came from the retired scraper. They stay local, they are
  never published, and this is the last useful thing they do before quarantine.

What it writes
  .cache/gemini-pilot/<videoId>.json   (gitignored — derived third-party text
                                        stays local, same rule as transcripts)
  Nothing in the repo, nothing in the corpus, no verdicts. This is a measurement.

Cost
  Flash-tier input runs about $0.30 per million tokens, and video at low media
  resolution is roughly 100 tokens per second plus 32 for audio. A 10-video
  sample of ~10 minute videos is a few cents, and the free tier covers 8 hours of
  YouTube video a day, so a pilot this size should cost nothing at all.
"""
import json, os, random, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".cache" / "gemini-pilot"
API = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODELS = "https://generativelanguage.googleapis.com/v1beta/models"

WRITE = "--write" in sys.argv
LIST = "--list-models" in sys.argv


def flag(name, default):
    """--n 10 -> 10"""
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


N = int(flag("--n", 10))
MODEL = flag("--model", "gemini-3.8-flash")


def key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        f = ROOT / ".secrets" / "gemini-api-key"
        if f.exists():
            k = f.read_text().strip()
    if not k:
        sys.exit(
            "No key. Either put it in .secrets/gemini-api-key (gitignored) or\n"
            "  export GEMINI_API_KEY=...\n"
            "Get one at https://aistudio.google.com/apikey"
        )
    return k


def post(url, body, k):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": k, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:800]
        raise SystemExit(
            f"\nGemini returned {e.code}.\n{detail}\n\n"
            "If it says the model is not found, run --list-models and pass a live one\n"
            "with --model. Model ids move faster than this script does."
        )


# What we want out of a video. Deliberately narrow: the claim, when it was said,
# whether it is a prediction with a clock on it, and whether something is being
# sold. That is the minimum the ledger needs and nothing more.
SCHEMA = {
    "type": "object",
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The claim as a flat proposition, in the speaker's own terms"},
                    "timestamp": {"type": "string", "description": "MM:SS where it is said"},
                    "speaker": {"type": "string"},
                    "hedged": {"type": "boolean", "description": "True if softened with might/could/some say"},
                    "is_prediction": {"type": "boolean"},
                    "deadline": {"type": "string", "description": "The date or period it is claimed to happen by, or empty"},
                },
                "required": ["text", "timestamp", "hedged", "is_prediction"],
            },
        },
        "sells_something": {"type": "boolean", "description": "Does the video pitch a product, course, newsletter or fund"},
        "one_line": {"type": "string", "description": "What this video argues, in one sentence"},
    },
    "required": ["claims", "sells_something", "one_line"],
}

PROMPT = """You are reading a YouTube video to extract the factual claims it makes.

Return the claims the speaker actually asserts, not the topics covered. A claim is
something that could later turn out to be true or false. Skip greetings, sponsor
reads and calls to subscribe.

For each claim give the timestamp as MM:SS. Mark it hedged if it is softened
("could", "might", "some people say"). Mark it a prediction if it is about the
future, and give the deadline if one is stated or clearly implied.

Be strict. A video that asserts nothing checkable returns an empty claims list —
that is a valid and useful answer."""


def read_video(url, k):
    body = {
        "model": MODEL,
        "input": [
            {"type": "text", "text": PROMPT},
            {"type": "video", "uri": url, "media_resolution": "low"},
        ],
        "response_format": {"type": "text", "mime_type": "application/json", "schema": SCHEMA},
    }
    t0 = time.time()
    r = post(API, body, k)
    return r, time.time() - t0


def payload(r):
    """Pull the JSON out of whatever shape the response arrives in."""
    for path in (
        lambda: r["output"][0]["content"][0]["text"],
        lambda: r["candidates"][0]["content"]["parts"][0]["text"],
        lambda: r["output_text"],
        lambda: r["text"],
    ):
        try:
            return json.loads(path())
        except Exception:
            continue
    return None


def sample():
    """Half with a transcript to check against, half without."""
    have, lack = [], []
    for f in sorted((ROOT / "corpus").glob("*/videos.json")):
        for v in json.load(f.open())["videos"]:
            t = v.get("transcript")
            row = (f.parent.name, v)
            if t and (ROOT / t).exists():
                have.append(row)
            elif v.get("title"):
                lack.append(row)
    random.seed(7)  # same sample every run, so two runs are comparable
    random.shuffle(have)
    random.shuffle(lack)
    half = N // 2
    return have[:half] + lack[: N - min(half, len(have))]


def truth(v, lines=6):
    t = v.get("transcript")
    if not t:
        return None
    p = ROOT / t
    if not p.exists():
        return None
    return "\n".join(p.read_text(errors="ignore").splitlines()[:lines])


def main():
    k = key()

    if LIST:
        req = urllib.request.Request(MODELS, headers={"x-goog-api-key": k})
        with urllib.request.urlopen(req, timeout=60) as r:
            for m in json.loads(r.read()).get("models", []):
                name = m.get("name", "").replace("models/", "")
                if "embedding" not in name:
                    print(f"  {name:38} {m.get('displayName','')}")
        return

    rows = sample()
    if not rows:
        sys.exit("No videos found in corpus/.")
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"{len(rows)} videos · model {MODEL} · low media resolution\n")

    ok = empty = failed = 0
    secs = 0.0
    for i, (topic, v) in enumerate(rows, 1):
        vid, title = v["videoId"], v["title"]
        print(f"[{i}/{len(rows)}] {topic}  {vid}")
        print(f"  title seen today   {title[:88]}")
        try:
            raw, dt = read_video(v["url"], k)
        except SystemExit:
            raise
        except Exception as e:
            print(f"  FAILED             {e}\n")
            failed += 1
            continue
        secs += dt
        data = payload(raw)
        if data is None:
            print(f"  unparsed response  {json.dumps(raw)[:200]}\n")
            failed += 1
            continue
        claims = data.get("claims", [])
        if not claims:
            empty += 1
        else:
            ok += 1
        print(f"  gemini says        {data.get('one_line','')[:88]}")
        print(f"  sells something    {data.get('sells_something')}")
        for c in claims[:3]:
            mark = "hedged" if c.get("hedged") else "flat"
            when = f" by {c['deadline']}" if c.get("deadline") else ""
            print(f"    {c.get('timestamp','--:--')}  [{mark}] {c['text'][:74]}{when}")
        if len(claims) > 3:
            print(f"    … {len(claims)-3} more")
        tr = truth(v)
        if tr:
            print("  actually said (first lines of the real transcript):")
            for line in tr.splitlines():
                print(f"    {line[:84]}")
        usage = raw.get("usage") or raw.get("usageMetadata") or {}
        if usage:
            print(f"  tokens             {json.dumps(usage)[:120]}")
        print(f"  took               {dt:.1f}s")
        if WRITE:
            (OUT / f"{vid}.json").write_text(json.dumps({"topic": topic, "title": title, "read": data, "raw_usage": usage}, indent=1))
        print()

    n = len(rows)
    print(f"{ok} produced claims · {empty} returned none · {failed} failed · {secs:.0f}s total")
    if WRITE:
        print(f"saved to {OUT.relative_to(ROOT)}/ (gitignored)")
    print("\nThe question to answer by eye: for the videos where you can see the real")
    print("transcript, did Gemini get it right? And for all of them — does the claim")
    print("tell you more than the title already did? If not, this route is not worth it.")


if __name__ == "__main__":
    main()
