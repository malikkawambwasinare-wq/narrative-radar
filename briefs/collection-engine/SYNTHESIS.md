# Collection engine & multi-platform expansion — corrected synthesis (28 Aug 2026)

Nine-agent investigation (repo forensics · X API · open platforms · closed platforms · cross-platform claim
matching · architecture plan · three adversarial verification passes). **42 issues were raised against the
plan by the verifiers; the corrections are folded in below.** Where the plan and a verifier disagreed, the
verifier's evidence wins and the original claim is struck through in the notes.

---

## 1. The answer: you are not paying to collect. You never were.

The free-collect / paid-analyze split you wanted **already exists, and you built it.**

- `netlify/functions/sweep.mjs` — no `import Anthropic`, no API key, no YouTube quota. **$0 per sweep.**
- `collector.py` — same, and it parses `ytInitialData` properly (views, published, length, transcripts).
- `trace-origin.mjs` — no Claude call.

Claude is invoked in exactly three files — `analyze.mjs`, `consolidate.mjs`, `map360.mjs` — always on
already-collected data. **100% of your spend is analysis.** The entire 86-video corpus cost roughly
**$3.40–4.00** to analyze, total, ever.

Building "a free collection engine" would not move your bill by one cent.

### Where the money actually goes

Per `analyze.mjs` call, Opus 5 at $5/$25 per MTok (token figures are bytes÷4 estimates — run
`count_tokens` before locking them):

| Component | ~Tokens | Note |
|---|---:|---|
| System prompt | 810 | |
| Schema | 436 | |
| **`summarizeCorpus()`** | **~2,300** | **~64% of input, re-sent on every call** |
| Video metadata | 40 | |
| **Total in / out** | ~3,575 / ~700 | **≈ $0.035 per call** |

Two real defects, both fixable in under two days:

1. **The digest bug.** `summarizeCorpus()` ships a summary of the whole shelf on every call. It scales with
   *tile count*, not corpus depth: ~2,300 tokens at 7 topics, ~18,000 at 50 — where a single analyze call
   costs **$0.114**. This is the O(N²) growth path.
2. **The coupling bug.** `index.html:1908 / 1947 / 1982 / 2006` each auto-fire `refreshNarrative()` 800 ms
   after a lookup, which sweeps (free) then loops `/api/analyze` over up to 5 videos plus a consolidate.
   One pasted link silently costs **~$0.23** of analysis the user never asked for.
   *Correction: the four sites are mutually exclusive branches and `refreshNarrative` is guarded by a
   module-level `if (refreshing) return;` at `index.html:1709` — so it is **one** chain per paste, ~$0.23,
   not four. The fix stands (make it an explicit button); the burn was overstated 4× in the first draft.*

---

## 2. Two bugs that need fixing regardless

- **`cloudflare/worker.mjs:10-15` — `map360` is missing from `ROUTES`.** The shipped `⊕ Map territory`
  button (`index.html:1376`) will 404 the moment you `wrangler deploy`. One line; guaranteed production break.
- **`map360.mjs` and `trace-origin.mjs` are LIVE and billable.** `netlify.toml` declares
  `[functions] directory` with no include/exclude list, so Netlify ships the whole folder. *(This corrects
  a standing assumption in earlier briefs that they were written but not deployed.)* `trace-origin` is the
  **most expensive path in the codebase** — its own header comment says ~150–300 post reads at $0.005;
  with `expansions=author_id` billing user objects at $0.010 the realistic range is **$1.50–4.50**, and
  `READ_BUDGET = 600` does not bound user-object spend.

---

## 3. X: defer. $0 this month. But the reason is bigger than X.

Full-archive search *is* reachable on pay-per-use (~$0.40–1.50/trace), so paperwork was never the blocker.
The blocker is architectural, and it is the most important finding in this whole investigation:

> **Any platform whose terms require honoring deletions is incompatible with committing that platform's
> post text to immutable public git history.**

`trace-origin.mjs:150` writes `earliest.text.slice(0, 240)` — plus author, username and metrics — into
`narrative.json`, which is committed to a public repo. X requires deletion or modification within 24 hours
of a request. **Git cannot do that**: a later commit does not remove data from an earlier one.

Critically, this **also kills the obvious escape hatch.** The plan proposed rebuilding origin-tracing free
on Bluesky — but Bluesky's developer guidelines carry their own deletion-honoring requirement, so it
inherits the identical defect. Swapping platforms does not solve it.

**The fix is the one that also happens to be the moat:** store **IDs plus your own derived analysis**,
never third-party text. A ledger row reading *"2026-03-14 · @account · claim: credit event before Jun 2027 ·
post ID 1234567 · status REFUTED"* is your dated judgment about an observation, not redistributed content.
"Source no longer available" is a fact you observed. Their posts are copyable and deletable; a timestamped
ruling under a published standard is neither.

Revisit X only at revenue: ~$50 loaded with a console cap ≈ $15–30/mo.

---

## 4. Platform tier list — open beats closed on cost *and* coverage

GDELT covers 100k+ outlets in 65+ languages for $0 with unrestricted commercial rights. Bluesky gives full
post text and a free firehose — what X charges five figures for. Podcast RSS carries complete timestamped
transcripts almost nobody indexes. The closed platforms cost money *and* are shut. The one genuine loss is
short-form video (TikTok, Reels) — say so permanently in the UI.

| # | Platform | Cost | Effort | Why |
|---|---|---|---|---|
| 1 | **GDELT DOC 2.0** | $0, no key | 0.5d | **Unrestricted commercial use, attribution only** — the most permissive terms on this list and the only one compatible with permanent storage. Their TLS cert is currently expired; handle it. |
| 2 | **RSS at large** (one parser) | $0 | 1d | One component unlocks Substack, blogs, news, podcasts, YouTube channels, per-account Bluesky/Mastodon. Highest leverage item in the plan. |
| 3 | **Research layer** — OpenAlex + arXiv + Crossref | $0 (OpenAlex key free) | 1.5d | **Your positioning made literal**: "most narratives are forked from actual research." Pin a viral claim to the paper it forked from and show how it diverged. OpenAlex is CC0, 250M works, retraction flags. Highest differentiation per hour of anything here. |
| 4 | **Bluesky AppView** | $0 | 1d | Full post text, reply chains, quote posts. `listRecords` gives signed raw repo records — a better origin-tracing substrate than trace-origin reaches for. Store IDs only (see §3). |
| 5 | **Wayback CDX** | $0 | 1d | Free stealth-edit detection — prove a page said something different before it was quietly changed. **Promoted from BUILD LATER**: this is record infrastructure, not volume. Nobody in this space ships it. |
| 6 | **HN Algolia** | $0, zero auth | 0.5d | Easiest on the list. Financial/technical claims get contested here by people who show their work, often before the claim reaches YouTube. |
| 7 | **Podcast RSS + `podcast:transcript`** | $0 | 1d | One test feed carried 173 transcript tags — complete, timestamped, speaker-labelled, no ASR cost. Where long-form predictive claims incubate, unindexed because everyone assumes transcription is expensive. |
| 8 | **Telegram** `t.me/s/<channel>` | $0, no key | 0.5d | Same pattern as sweep.mjs — reuse the code path. |

**Deprioritized** (volume without record value): Twitch, Rumble, Odysee, Threads.
**Build later:** YouTube Data API v3 — adopting it triggers a 30-day refresh-or-delete rule against a
permanently-versioned corpus *and* converts your scraping from a robots.txt issue into a policy violation;
only 100 `search.list` calls/day. **Blocked:** TikTok (Research API is academic/non-profit only),
Instagram, Facebook, LinkedIn.

*Struck from the plan: "YouTube channel RSS retires the robots.txt risk." It does not —
`/feeds/videos.xml` is disallowed by the same `robots.txt` block as `/results`. Build it for reliability
and lower request volume, not as a compliance fix.*

---

## 5. Three gaps the plan did not have — and you need all three

1. **The free collection has a terms problem, not just a robots problem.** Automated collection from
   youtube.com breaches the YouTube ToS *today*, independent of robots.txt and independent of monetization
   (`sweep.mjs:16`, `collector.py:83` and `:126`). It is free in dollars, not free in exposure. The
   migration target is the open platforms above, which carry no equivalent prohibition.
2. **Defamation.** The product publishes adjudicative statements about identifiable real people, generated
   by a model, at scale, with no human review in the loop. Two controls become requirements, not
   preferences: never publish a bare verdict without its stated basis and a one-click-checkable citation;
   and keep a named human signing each ruling. This is the same control that makes the adjudication moat
   real — it is not overhead.
3. **GDPR.** The corpus is personal data about identifiable individuals in a public repo, and immutable git
   compounds the problem with every commit. Stop committing third-party text and personal data: IDs plus
   derived analysis only. This is the same fix as §3 — one change closes both.

Also unexamined anywhere: **Anthropic is the highest-consequence single dependency** in the system. The
analyzer is 100% Anthropic; an account action is total product failure. Keep the collection layer's terms
posture clean enough that it never puts the analyzer account at risk.

---

## 6. The strategic warning

**Zero of the plan's build days produce a scored prediction.** Its "adjudication" is cross-source claim
*matching* (`same_claim: supports | contradicts | unrelated`) — not the PENDING → SUPPORTED/REFUTED
transition that is the actual moat. Four prior research programs all converged on the same first move, and
this plan walks past it to build breadth instead.

Coverage is copyable. The dated, signed, continuous adjudication record is not. **Do not spend 30 days on
platform adapters before the resolver exists.**

---

## 7. Sequenced build order (corrected estimates)

The plan's "~12 founder-days" was rejected by verification as not credible for one person; realistic scope
is **30–45 days**. Cut it instead:

| # | Work | Days | Why now |
|---|---|---:|---|
| 0 | **Stop the bleeding.** Make the buildout chain an explicit button (4 call sites); add per-IP rate limit, global daily *spend* ceiling, and an Anthropic console cap. Fix `worker.mjs` ROUTES. | 0.5 | Takes per-paste from ~$0.23 to ~$0.036 and caps worst-case exposure. |
| 1 | **Stop writing third-party text to git.** `trace-origin.mjs:150` → IDs only; same for author/username/metrics. | 0.5 | Closes the X, Bluesky, defamation and GDPR exposures at once. |
| 2 | **Cheapen the analyzer.** Delete `summarizeCorpus()` from the payload; drop deterministic schema fields; route triage to Haiku 4.5; add `cache_control`. | 1.5 | Kills the O(N²) path. |
| 3 | **THE RESOLVER — the keystone.** Structured `{due_start, due_end, precision}` on the 26 ledger entries; a dated job that matures PENDING horizons and escalates them for ruling; first scored resolutions. | 3–4 | The moat. Everything else is decoration until this exists. |
| 4 | **The collector as a scheduled job** + freshness alerting that fails loudly (every current failure mode is silent-and-green). | 2 | Only after there is something worth collecting *for*. |
| 5 | **Open-platform adapters**, in tier order: GDELT → RSS → research layer → Bluesky → Wayback. | 5 | Coverage, once the record exists. |

**Cost after steps 0–2**, corrected by verification: **~$50–74/month at 1,000 users** (a 15–23× reduction,
not the 20–40× first claimed), against ~$1,150/month under today's architecture. Enforce the ceiling on
*dollars*, not call count — a call cap does not constrain which model each call routes to.

---

## 8. Infrastructure cautions carried forward

- **Git is a fine read-side CDN and a bad write-side database.** Three concurrent writers with no locking
  produce non-fast-forward rejections. Keep the corpus in git as the published artifact; move mutable state
  (queue, seen-set, per-run state) to Workers KV or D1 (free tier).
- **Cloudflare Workers free tier caps subrequests at 50/invocation** — the current N-way CDN fan-out dies at
  ~24 narratives, not 100. Fix the fan-out before migrating, or budget $5/mo.
- **GitHub Actions**: pushes with the default `GITHUB_TOKEN` do not trigger workflows; scheduled workflows
  auto-disable after 60 days of repo inactivity; add `paths-ignore` for data commits.
- **`.gitignore:1` excludes `corpus/*/transcripts/`** — keep it that way. Full verbatim third-party
  transcripts in a public repo is precisely the exposure §5 is closing.
