# Narrative cost model & make-or-buy — corrected synthesis (20 Aug 2026)

Eight-agent investigation: byte-measured pipeline audit + git archaeology (106 commits) on the
make side; live vendor research (transcripts, data feeds, freelance labor) on the buy side; a
unified model; then two adversarial verification passes (arithmetic + strategy). **All verifier
corrections are folded in below** — where a number changed, the correction is noted.

Pricing basis (verified 20 Aug 2026): Opus 5 $5/$25 per MTok · Haiku 4.5 $1/$5 · Batch API −50%.
Founder time at $50/hr (sensitivity at $25/hr in §5). Vendor prices researched Aug 2026 but not
contract-verified — **confirm each price before committing** (flagged by the arithmetic verifier).

## The one-sentence finding

**Narrative Radar's build cost is founder-hour economics wearing an API costume**: Claude/API
spend is 1–4% of the cost of a deep narrative; the ledger backfill and curation hours are
96–99%. So the way to "reduce the cost of making narratives" is a depth policy, not a cheaper
model — and the make-or-buy decision is really a decision about whose hours do the discovery
work, never about the judgment (which is unbuyable by design).

## 1. Cost breakdown — one narrative

### 1a. One-time BUILD (deep, collapse-audit grade: ~30 videos analyzed, transcripts, 14 dials, flagship ledger, 360 map, trace)

| # | Component | Type | CURRENT AS-BUILT | OPTIMIZED-MAKE | BLEND (buy discovery) |
|---|---|---|---|---|---|
| 1 | Research brief (question, camps, queries) | Founder | 1–3 h · $50–150 | same | same — never outsourced (it *is* the editorial position) |
| 2 | Discovery sweep | API | **$0** — sweep.mjs is an HTML scrape; no Claude call, no YouTube quota | $0 | $0 |
| 3 | Transcripts (30–38 videos) | Vendor | $0 — **absent** (title-only verdicts: a quality gap, not a saving) | ~$0 — Supadata free tier; Whisper fallback | same |
| 3b | Transcript QA (ASR errors on names/figures/dates) | Founder | — | 0.5–1 h · $25–50 (check every quote that reaches a published verdict against source audio) | same |
| 4 | Per-video analysis ×30 (analyze.mjs) | API | $0.88–2.01 @ 7-topic shelf; $3.38–4.51 @ 30-topic (quadratic bug) | **$0.19–0.25** (Haiku batch + retrieval fix + transcripts, flat in shelf size — gated on §3 quality test) | same |
| 5 | Claims consolidation + review | API + Founder | $0.03–0.05 + 0.5–1 h | $0.016–0.027 (Opus batch) + 0.5–1 h | same |
| 6 | Indicators: 14 fact-checked dials | Founder | 2–4 h · $100–200 | same | design 1–2 h founder; fact-check bought (in line 7) |
| 7 | Ledger backfill (dated predictions, blind-extraction rule) | Founder / Vendor | **15–20 h · $750–1,000** (flagship grade) | same | **$745 analyst package + ~$3 Filmot + 3–6 h founder verification** (100% check of every published quote/date — 2 h "spot-check" was rejected by the strategy verifier) |
| 8 | 360 map mint + relation curation | API + Founder | $0.03–0.08 + 1–2 h | $0.016–0.039 + 1–2 h | same (judgment kept) |
| 9 | Trace-origin | X API | **$0.75–1.50, $3 cap — no Claude call** (pure X reads @ $0.005) | same | same |
| 10 | Misc QA (verdict passes, corrections) | Founder | 1–2 h · $50–100 | same | same |
| 11 | Claude Code research-session tokens | API | $10–40 (rough) | $10–40 | $10–30 |
| | **Founder hours** | | **20.5–32 h = $1,025–1,600** | **21–33 h = $1,050–1,650** (adds transcript QA) | **8–17 h = $400–850** (incl. 3–6 h backfill verification) |
| | **API + vendor $** | | **$12–44** | **$11–42** | **$759–782** |
| | **ALL-IN** | | **≈ $1,037–1,644 (mid ≈ $1,340)** | **≈ $1,061–1,692** | **≈ $1,159–1,632 (mid ≈ $1,400)** |

Corrections applied vs the model's first draft: hours floor 20.5 h not 21; blend review priced
at 3–6 h not 2 h (which pushes the blend from "saves $103–453" to **roughly cash-neutral at
$50/hr**); Filmot $3.00/narrative not $1.80; one-time analyst onboarding ($300–800: playbook +
1–2 paid trial builds + vetting, plus ~15% rework on the first two builds) must be amortized on
top if the blend is used at all.

### 1b. Recurring RUN per narrative per month (8 new videos + 1 consolidation refresh + weekly sweeps)

| Line | CURRENT @ 7-shelf | CURRENT @ 30-shelf | OPTIMIZED |
|---|---|---|---|
| 8 new-video analyses | $0.23–0.54 | $0.90–1.20 | $0.051–0.068 |
| Consolidation refresh | $0.013–0.028 | $0.013–0.028 | $0.0065–0.014 |
| Sweeps / cron / transcript fetch | $0 | $0 | $0 |
| **API subtotal** | **$0.25–0.57** | **$0.92–1.23** | **$0.06–0.08 — flat in shelf size** |
| Adjudication (1 due/mo assumed) | $12.50 | $12.50 | **$15.60 honest rate** (+25% dispute/correction/criteria-maintenance overhead — strategy verifier) |
| **All-in /narrative/mo** | ~$12.75–13.07 | ~$13.42–13.73 | **~$15.66–15.68** |

Portfolio at 30 narratives, optimized: API ≈ **$1.80–2.40/mo (~$22–29/yr)** vs $27.60–36.90/mo
as-coded — an **11–20× cut**. Adjudication at 30 narratives ≈ 30 rulings ≈ 7.5–9.5 founder-h/mo;
deadlines cluster (December year-end claims), so plan capacity for the cluster, not the average.

### 1c. Shared fixed: ≈ $1–6/mo (Netlify/GitHub free, domain ~$1, Supadata free tier; Filmot ~$30
in backfill months only; Scrape Creators $47 one-time backup ≈ decades of credits).

## 2. Totals by build tier

| Tier | What it is | Cost | Status |
|---|---|---|---|
| **DEEP** (flagship) | collapse-audit grade | **$1,037–1,644, 20.5–32 h** (make) | Reserve for 2–3 flagships |
| **STANDARD** (workhorse) | crypto-winter pattern: engine-assisted 2–4 h ledger + dials | **$300–550, 6–11 h** | **The default build** |
| **LIGHT** | videos + claims only | $50–100, 1–2 h | **Not publishable** — violates the thin-narrative honesty rule (index.html renders a no-ledger narrative with a claim about it that isn't earned). Reclassified as an internal observation stage, promotable to standard |
| 10-narrative Tier-1 shelf | 3 deep (make) + 7 standard | **≈ $5,100–7,700 cash-equivalent, ~62–113 founder-h** | Monthly run ≈ $127–135 all-in (of which API $0.60–0.80) |

## 3. Make-or-buy matrix (verdicts with safeguards)

Strategic constraint (audit form): **anything that constitutes applying the published resolution
standard, or that a reader would treat as the founder's signed judgment, is never bought — at any
price.** The engagement partner signs the opinion; ticking-and-tying is outsourceable.

| Component | Verdict | Why / safeguards |
|---|---|---|
| Research brief | **MAKE** | The editorial position itself |
| Discovery | **MAKE (free)** | Scrape now, free Data API fallback (post-June-2026 granular quota: 100 search calls/day in their own bucket). Buy-side (Tubular ~$27k/yr, Brandwatch $800–3,000/mo) can't see spoken word — pays 5 figures for the free layer |
| Transcripts | **BUY (~$0)** | Supadata free tier; Scrape Creators $47 one-time backup; Groq Whisper ~$0.013/video STT fallback. Safeguard: QA line 3b — ASR mangles exactly what this product publishes (names, tickers, figures, dates) |
| Per-video analysis | **MAKE-CHEAPER, gated** | Haiku 4.5 + Batch + candidate-retrieval fix. **Gate: dual-run 20–30 videos Haiku vs Opus baseline; switch only at ≥95% verdict agreement + comparable claim recall** (2–3 h one-time). Verdicts feed published accountability stats — a cheap model that degrades them is product damage, not savings |
| Consolidation | **MAKE-CHEAPER** | Keep Opus (merging judgment), move to Batch |
| Indicators | **HYBRID** | Dial *selection* = editorial judgment (make); numeric *verification* = commodity (buyable). MTurk rejected on ethics + rework (~$2.63/hr effective wage is a reputational liability for a credibility brand) |
| Ledger backfill | **BUY discovery only when hours bind** | Analyst delivers candidates-plus-evidence, never a filtered ledger; founder verifies 100% of published quotes/dates (3–6 h) and signs selection. Honest break-even ≈ **$42–53/hr** founder opportunity cost — roughly cash-neutral at $50/hr; below that, MAKE. Its real product is **~13–16 freed founder-hours per deep build**, purchased at ~$750 |
| 360 relations | **MAKE** | Connective tissue; judgment |
| Trace-origin | **BUY the data** | X pay-per-use reads, ~$1/trace, cached forever. Risk register: an X reprice is survivable — the "unverified genesis" badge makes traces deferrable by policy |
| Re-observation cron | **MAKE** | ~$0, unbuilt, and it's the moat's delivery mechanism |
| **Adjudication** | **NEVER BUY the ruling** | One judge, one standard, continuously — or cross-pundit grades are meaningless. Evidence packets buyable **only** with structural safeguards (strategy verifier, critical finding): fixed template derived from the published criteria, evidence FOR and AGAINST, archived links, **no recommendation or verdict-lean field**; one dedicated analyst, never rotating; founder periodically builds packets from scratch as a drift audit |

## 4. Cost levers, ranked (corrected)

1. **Right-size ledger depth** — standard 2–4 h engine-assisted ledgers everywhere except 2–3
   flagships. **Saves $550–900 per non-flagship narrative. Zero code. A policy decision.**
2. **Fix the shelf-summary quadratic bug** (candidate retrieval, ~3 topics/call). Corrected
   numbers: growth is **5.9×** at 30 topics (~725 tokens/topic, +$0.0036/call), ≈$2.88/build +
   $0.77/mo/narrative at 30-shelf ≈ **$26–35/mo portfolio**. Near-$0 today; fix before ~15 topics
   because it deletes the O(N²) growth path. ~1 dev-day.
3. **Haiku + Batch, behind the quality gate** — with #2, run API drops 11–20× and goes flat in
   shelf size.
4. **Transcripts at ~$0** — the cheapest credibility upgrade available (+~$0.12/build of Haiku
   input turns title-only verdicts into transcript-grounded ones).
5. **Outsourced backfill discovery** — reframed by verification: not a cost saving but a **time
   purchase** (~$750 buys back ~13–16 h per deep build). Use only for flagship builds under a
   real deadline, after $300–800 one-time analyst onboarding.

## 5. Sensitivity & the regime question

- **At $25/hr founder rate**: deep make $536–842; blend costs **$187–334 more** like-for-like —
  MAKE wins everywhere; 10-shelf ≈ $2,700–4,500; run all-in ≈ $6–8/narrative/mo.
- **The regime must be stated** (strategy verifier): if cash is the binding constraint → MAKE at
  standard depth. If a launch date makes founder-hours binding → BUY flagship discovery. The
  analysis assumes hours bind ("not survivable solo" at 10×deep make = 210–320 h); Malik should
  confirm which regime he is in before contracting anyone.
- **Video-count basis**: costed at 30 analyses/build; collapse-audit actually holds 38 — at 38
  the analyze lines rise ~27% (immaterial, <$0.60/build).

## 6. What the audit corrected about prior beliefs

- **trace-origin has no Claude call** — pure X full-archive reads ($0.005/read, $3 cap), not the
  assumed ~$0.05–0.10 Anthropic spend.
- **sweep.mjs uses no YouTube quota** — HTML scrape, $0; the free Data API is the fallback.
- **Analyze per-call is $0.029–0.067** (byte-measured, output hard-capped by max_tokens=2000),
  not the earlier $0.07–0.38 field estimate.
- **$12.50/resolution was understated** — honest rate ≈ $15.60 with dispute/correction/criteria-
  maintenance overhead, plus 1–2 h/quarter portfolio-wide criteria versioning.
