#!/usr/bin/env python3
"""Narrative Radar — the one place that talks to Gemini.

Everything the collection engine sends to Gemini goes through here, so the key
handling, the request shape and the rate limit are defined once.

Why a token budget and not a sleep
  The free tier caps input at 250,000 tokens per MINUTE, and video bills at a
  measured 91 tokens per second of runtime. So a 46-minute video exceeds the
  whole minute's budget on its own and can never succeed on the free tier, while
  four ten-minute videos fit comfortably. A fixed pause between calls either
  wastes most of the budget or blows through it depending on video length. This
  module instead spends against a rolling window: it knows what a video will
  cost before sending it, waits until there is room, and refuses the ones that
  can never fit rather than burning a retry to find out.
"""
import json, os, re, sys, time, urllib.error, urllib.request
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODELS = "https://generativelanguage.googleapis.com/v1beta/models"

TOKENS_PER_SECOND = 91      # measured across 143 minutes of video, 2026-09-19
TPM_LIMIT = 250_000         # free tier, gemini-3.8-flash
USD_IN = 0.30 / 1_000_000
USD_OUT = 2.50 / 1_000_000


class ApiError(Exception):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail[:300]}")


class DailyLimit(ApiError):
    """Out of requests until the quota resets. Nothing to do but stop, and
    stopping cleanly matters: whatever has been read so far is cached, and the
    synthesis can run off the cache later without paying for the videos twice."""

    def __init__(self, detail):
        super().__init__(429, detail)


def key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        f = ROOT / ".secrets" / "gemini-api-key"
        if f.exists():
            k = f.read_text().strip()
    if not k:
        sys.exit("No key. Put it in .secrets/gemini-api-key or export GEMINI_API_KEY.\n"
                 "Get one at https://aistudio.google.com/apikey")
    return k


class Budget:
    """A rolling one-minute token window."""

    def __init__(self, limit=TPM_LIMIT, quiet=False):
        self.limit, self.quiet = limit, quiet
        self.spent = deque()  # (when, tokens)

    def _drop_old(self):
        cut = time.time() - 60
        while self.spent and self.spent[0][0] < cut:
            self.spent.popleft()

    def too_big(self, tokens):
        """No amount of waiting makes this one fit."""
        return tokens > self.limit

    def wait_for(self, tokens):
        while True:
            self._drop_old()
            used = sum(t for _, t in self.spent)
            if used + tokens <= self.limit:
                return
            wait = 61 - (time.time() - self.spent[0][0])
            if not self.quiet:
                print(f"    (budget: {used:,} of {self.limit:,} used, waiting {wait:.0f}s)")
            time.sleep(max(wait, 1))

    def record(self, tokens):
        self.spent.append((time.time(), tokens))


def video_tokens(length):
    """Cost of a video from its "MM:SS" or "H:MM:SS" runtime."""
    if not length:
        return None
    try:
        p = [int(x) for x in str(length).split(":")]
    except ValueError:
        return None
    secs = p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else None
    return int(secs * TOKENS_PER_SECOND) if secs else None


def _post(body, k, timeout=600):
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"x-goog-api-key": k, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ApiError(e.code, e.read().decode("utf-8", "ignore"))


def _strip_unknown(body, detail):
    """The API names the field it did not recognise. Take it at its word."""
    m = re.search(r"Unknown parameter '([^']+)'", detail or "")
    if not m:
        return False
    bad, hit = m.group(1).split(".")[-1], [False]

    def walk(n):
        if isinstance(n, dict):
            if bad in n:
                n.pop(bad)
                hit[0] = True
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(body)
    return hit[0]


def ask(model, parts, schema, k, budget=None, est_tokens=None, retries=3):
    """One call. `parts` is a list of {"type": "text"|"video", ...}."""
    if budget and est_tokens:
        if budget.too_big(est_tokens):
            raise ApiError(0, f"needs {est_tokens:,} tokens, over the {budget.limit:,}/min ceiling")
        budget.wait_for(est_tokens)
    body = {"model": model, "input": parts,
            "response_format": {"type": "text", "mime_type": "application/json", "schema": schema}}
    for attempt in range(retries + 1):
        try:
            r = _post(body, k)
            if budget:
                u = r.get("usage") or {}
                budget.record(u.get("total_input_tokens") or est_tokens or 0)
            return r
        except ApiError as e:
            if e.code == 400 and _strip_unknown(body, e.detail):
                continue
            if e.code == 429:
                # Two different limits arrive as the same status code, and they
                # want opposite responses. A per-minute ceiling reopens on its
                # own, so wait. A per-day ceiling will not clear for hours, and
                # every retry against it spends another of the requests you have
                # already run out of — which is how a 24-video run burned its
                # remaining budget discovering the same thing sixteen times.
                if "per day" in e.detail or "PerDay" in e.detail:
                    raise DailyLimit(e.detail)
                if attempt < retries:
                    print(f"    (per-minute limit, waiting 60s — attempt {attempt + 1})")
                    time.sleep(60)
                    if budget:
                        budget.spent.clear()
                    continue
            raise
    raise ApiError(429, "still rate limited after retries")


def payload(r):
    """The answer lives in the step typed model_output; the thought step is an
    opaque signature."""
    for step in r.get("steps", []):
        if isinstance(step, dict) and step.get("type") == "model_output":
            for part in step.get("content", []):
                try:
                    return json.loads(part["text"])
                except Exception:
                    continue
    return None


def spend(r):
    u = r.get("usage") or {}
    out = u.get("total_output_tokens", 0) + u.get("total_thought_tokens", 0)
    return u.get("total_input_tokens", 0) * USD_IN + out * USD_OUT
