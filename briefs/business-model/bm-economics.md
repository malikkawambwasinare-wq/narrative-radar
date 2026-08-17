# LENS 1 — Unit Economics from Real Costs

**Sources read:** `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/netlify/functions/analyze.mjs` (1 opus call, `max_tokens: 2000`, effort low), `consolidate.mjs` (1 opus call, `max_tokens: 1500`), `map360.mjs` (1 opus call, `max_tokens: 2500`), `sweep.mjs` (0 model calls — free HTML scrape), `collector.py` (local, 0 model calls), `briefs/observability/no-business.md`, `no-clocks.md`, plus a measured byte-count of the actual payload the engine ships per call. Pricing verified against current Claude API rates: **Opus $5/$25 per MTok, Sonnet $3/$15, Haiku $1/$5.**

---

## 0. A structural finding that changes all the arithmetic below

`analyze.mjs` (lines 170–220) fetches **every narrative's full summary — 12 sample videos each — and ships the whole shelf as input on every single analyze call** (`summarizeCorpus(topics)`). Measured today at 7 topics / 86 videos: **9,262 chars ≈ 2,315 tokens** of corpus summary per call, plus ~1,100 tokens of system prompt. A mature narrative's summary block is ~650 tokens.

So per-call input cost scales **linearly with shelf size**, and total shelf cost scales with (narratives × per-call input) — **quadratically with the shelf**. Audit framing: this is a control-design deficiency, not an operating cost — every transaction re-reads the entire general ledger. The fix (send only the top ~5 candidate narratives per call, retrieved by keyword/embedding) makes cost linear and caps per-call input at ~4.5K tokens. Every "dream spec" number below is shown both ways.

Per-analyze-call cost (input + ~2,000 output/thinking tokens at effort low):

| Shelf size | Input tokens | Opus cost/call | Haiku cost/call |
|---|---|---|---|
| 7 (today) | ~3,700 | **$0.07** ✓ matches your measured $0.05–0.10 | $0.014 |
| 30 mature | ~20,900 | **$0.155** | $0.031 |
| 100 mature | ~66,400 | **$0.38** | $0.076 |
| Any size, with candidate retrieval | ~4,500 | **$0.07** | $0.015 |

Consolidate (~2–4K in, ~1.2K out): **~$0.05** Opus / ~$0.012 Haiku. Does not scale with shelf. Sweep: **$0**. map360: ~$0.08–0.10, occasional, excluded from cadence math.

**On the "Haiku cuts costs 10–25x" assumption: it's 5x, not 10–25x.** Haiku is $1/$5 vs Opus $5/$25 — exactly 5x on both sides. Sonnet is 1.67x. The Batch API adds another 50% off for non-latency-sensitive refresh work (your cron refreshes qualify), so the real maximum stack is **Haiku + Batch ≈ 10x cheaper than Opus real-time** — the top of your assumed range only with batching, which the current Netlify-function architecture doesn't do. Verdict/classification calls (analyze, consolidate) are classification-grade and are Haiku-safe; keep Opus (or Sonnet) only for map360 and new-narrative *founding* (the call that writes a narrative's claim/explanations — quality there compounds).

---

## 1. Cost side — per narrative per month

At **$50/hr founder time.** Adjudication estimate: tier-A (public record) ~5–10 min, tier-C (judgment vs pre-registered spec) ~30 min; blended **15 min = $12.50/resolution**. Resolution arrival rate from your own ledger data (no-clocks brief): **~0.24 resolutions/narrative/month** at weekly cadence.

### DORMANT (static shelf page)
- API: **$0**. Human: **$0**. But the no-clocks brief's own finding applies: a rotting ledger destroys the product — dormant is only honest if the narrative's ledger is empty or the scorecard is suppressed.

### WEEKLY (1 sweep + 4 analyze + 1 consolidate, ×4.33/mo), 30-narrative shelf
- API per narrative: 4.33 × (4 × $0.155 + $0.05) = 4.33 × $0.67 = **$2.90/mo** (Opus) · **$0.59/mo** (Haiku)
- **Shelf of 30: $87/mo Opus · $18/mo Haiku**
- Human, shelf of 30: 30 × 0.24 = **7.2 resolutions/mo × $12.50 = $90/mo**, + ledger triage/hygiene ~3 hr = $150, + transcript collection (local collector.py, human-triggered, ~1 hr/wk if you want transcripts at all — the engine itself is metadata-only) = $217. **Human total ≈ $460/mo of founder time — 5x the API bill even on Opus.**

### DAILY-HOT (daily sweep + 5 analyze/day + consolidate every 3 days + re-obs cron)
- API per narrative (30-shelf): 150 × $0.155 + 10 × $0.05 = **$23.75/mo** Opus · **$4.77/mo** Haiku
- Re-observation cron: compute free, but it exists to *generate resolutions and catch goalpost-moves* — every catch is founder minutes. Daily-hot plausibly 2–3x the resolution rate: **~$25–40/mo human per hot narrative.**

### The dream spec: "updates with each new video," whole shelf

| | 30 narratives | 100 narratives |
|---|---|---|
| Opus, current architecture | 30 × $23.75 ≈ **$712/mo** | 100 × $57.50 ≈ **$5,750/mo** |
| Haiku, current architecture | ≈ **$143/mo** | ≈ **$1,152/mo** |
| Haiku + candidate retrieval + Batch | ≈ **$50/mo** | ≈ **$170/mo** |
| Human adjudication (2–3x weekly rate) | ~15–22 res/mo ≈ **$190–270/mo** | ~50–70 res/mo ≈ **$625–875/mo** (12–17 hr) |

Two honest conclusions: (a) the API cost of the dream is an *engineering* problem — three fixes (Haiku for classification, candidate retrieval, Batch API) take the 100-narrative dream from $5,750/mo to ~$170/mo; (b) the **human cost is not fixable** — at 100 hot narratives, adjudication alone is 12–17 hr/mo before triage, disputes, or the weekly note, and per your own settled research the adjudication IS the product. The dream spec's binding constraint was never the API bill.

One more cost the ladder ignores: **the free paste-a-video flow spends your money and writes to your database.** Every paste is $0.07–0.38 of Opus plus an auto-commit (new narratives included). At even 100 pastes/day that's $210–1,140/mo of *other people's* usage plus unbounded shelf growth into your adjudication queue. A rate limit and a new-narrative quarantine (~2–3 days of work) is a prerequisite for the free tier being "marketing" rather than a cost bomb.

---

## 2. Revenue side

### LTV at $39/mo, honestly
- Mean lifetime = 1/churn: 11.7%/mo → 8.5 months; 16.7%/mo → 6.0 months.
- Gross LTV: $39 × 6.0 to 8.5 = **$234–$333**. Net of Stripe (2.9% + $0.30 = $1.43/mo → $37.57 net): **$225–$321**.
- Implication: sustainable CAC ceiling ≈ $75–100 (⅓ of LTV). No paid acquisition works at that number in finance; the free shelf + weekly note must do all acquisition — which the prior brief already concluded.

### Subscribers to cover a 30-narrative weekly shelf + minimum viable income
- Costs: $87 API (Opus; $18 on Haiku) + ~$50 hosting/tools/email ≈ $137/mo. Founder floor $2,500/mo.
- ($2,500 + $137) / $37.57 = **70 paying subscribers** ($2,000 floor → 57; $3,000 → 84).
- **The churn treadmill:** at ~14% monthly churn, holding 70 subs means winning **~10 new payers every month, forever.** At the finance-newsletter 5–10% free→paid conversion (your prior brief's benchmark), that's **100–200 new engaged free users/month** — the real KPI, and the number nothing in the current repo measures.
- Annual prepay at $348 (already the prior brief's recommendation) is the churn escape hatch: 8 annual sales = 70-sub-months banked.

### The ladder, rung by rung, with the solo infrastructure bill

| Rung | Infra you'd have to build & run solo | Build time | Ongoing | Verdict |
|---|---|---|---|---|
| **Free radar** | Rate limiting + new-narrative quarantine on paste flow | 2–3 days | ~0 | **Real — required, it's live and currently uncapped** |
| **Radar Pro $20–50** | Stripe checkout+webhooks (1–2 wk), auth/accounts (1–2 wk, Supabase/Clerk), change-detection diff cron (1–2 wk), email alerts via Resend (1 wk), account pages | **~5–7 weeks** | 2–4 hr/wk support+ops | **Real — the one paid rung that pencils.** At $39 you need 70 subs; at $29 you'd need 95 — price at the top of the band. |
| **Professional $100–300** | Alert granularity, full history UI, comparisons, CSV/PDF exports, implied support SLA | +4–6 weeks | support expectations jump | **Fantasy year one.** A $100–300/mo buyer buys a *track record*. Current asset: 26 ledger entries, **0 ever scored**. SpotGamma earned $299 with 5 years of receipts. |
| **Teams (annual)** | Seats/roles, shared watchlists, brief scheduler, invoicing, security questionnaires, a sales motion | 2–3+ months | procurement cycles | **Fantasy** — solo-founder enterprise motion already rejected in prior research. |
| **Data/API licensing** | Metering, keys, docs, versioning, uptime commitments, contracts | 4–6 weeks | SLA forever | **Fantasy — see break-even below.** |
| **Browser extension** | Second codebase, Chrome review, per-page call costs, YouTube ToS exposure | 4+ weeks | store-review treadmill | **Defer** — platform risk is the leading cause of death in this category (your own finding), and it invites uncapped call volume. |
| **Multi-ecosystem / schemas / multi-sensor** | Each multiplies collection AND adjudication surface | months each | linear in founder hours | **Not year one.** They scale the bottleneck (human judgment), not revenue. |

### API/data tier break-even, given the graph is backfillable
Your own settled findings: the founder backfilled 11 years of Dalio calls in 2 weeks with an LLM; Filmot indexes ~645M captioned videos; the analyze prompt is sitting in a public repo. A competitor (or the prospective data customer themselves) can replicate the *entire current graph* for roughly **a few hundred dollars of model calls and 2–4 weeks** — call it ≤ $3,000 all-in. That is the **price ceiling** on licensing the graph: nobody pays more per year for data than it costs to rebuild once. The only non-backfillable asset is the *forward* record of resolutions adjudicated under a published standard before outcomes were known — which today is **zero entries**. Arithmetic: build cost ~200 hrs × $50 = $10,000 of founder time; realistic year-one demand at ≤$3,000/yr price ceiling: 0–2 customers; break-even **> 3 years even in the optimistic case, and negative-EV against spending those 200 hours on Radar Pro instead.** The API tier becomes rational only after ~2+ years of forward record exists — i.e., it's a rung you *earn*, not one you build.

---

## 3. Verdict

**Economically real in year one (solo):** Free radar (with the abuse cap) → Radar Pro at **$39/mo, annual $348 prominent**. That's the whole ladder. Target: 70 subs = $2,600/mo net. Everything above Pro is deferred until a scored forward record exists, because every upper rung's willingness-to-pay is a function of exactly the asset that currently has n=0.

**Maximum honest shelf size:** the moat and the bottleneck are the same object (your no-clocks brief said it; the numbers here confirm it). At a realistic 10 hr/mo of ledger operations, capacity is ~30–40 resolutions/mo including triage — which supports **~25–35 narratives at weekly cadence, of which at most ~5 daily-hot.** The prior brief's "50 narratives = a genuine part-time job" is consistent with this. 100 narratives is achievable on the API side for ~$170/mo after the three engineering fixes, but not on the adjudication side without hiring — and hiring the adjudicator dilutes the single-consistent-judge asset.

**The three cheap engineering moves that change the cost curve** (in order): (1) candidate retrieval in `analyze.mjs` so cost stops scaling quadratically with the shelf — this matters *before* growth, not after; (2) Haiku for analyze/consolidate classification calls (5x), Opus only for narrative founding and map360; (3) Batch API for cron refreshes (further 50%). Combined: ~10x, and the dream spec's API bill becomes a rounding error next to founder time.

**The number that actually gates everything:** 26 ledger entries, 0 scored, ever. At $50/hr, the first ~$100 of founder time spent adjudicating the overdue entries buys more enterprise value than any infrastructure on the ladder — it converts the product from a claim about accountability into evidence of it, and it's the input every revenue line above depends on.

*(Where the audit analogy breaks: in audit, fieldwork hours are billed to the client; here adjudication hours are unpaid cost-of-goods until subscribers exist — the engagement economics run backwards, which is exactly why the churn treadmill math, not the hourly rate, is the survival constraint.)*