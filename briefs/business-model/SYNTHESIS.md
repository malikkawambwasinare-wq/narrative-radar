# Business model — corrected synthesis (16 Aug 2026)

Three-lens investigation (unit economics from real repo costs · distribution & ladder
precedents · geo-perspectives & domain schemas), reconciled with the three prior research
programs (data-moat kill verdict, Portable Thesis, observability). Full reports in this
directory.

## The company, defined

**An adjudication house, not an observability platform.** The product is *the record of who
said what, when it was due, and whether it happened* — a published standard, applied by a
named party, before outcomes are known. The moat is the referee's logbook, not the library
(the library — any narrative graph — is backfillable in weeks with an LLM; the logbook's
timestamps are not).

## Year one: two products, not five rungs

**FREE — the weekly brief.** Not "a site you visit to orient yourself" — that promise has
three corpses (RSS readers, Pocket/read-it-later, Artifact — Instagram's founders, dead in
one year). What works is the brief: Morning Brew (4.4M subs, ~$50M/yr), 1440, and SpotGamma's
Founder's Note all prove the habit lives in the inbox. Format: *"What changed this week:
who resolved, who moved a goalpost, who went quiet"* — with receipts linking to the shelf.
The site becomes the receipt archive the brief cites; paste-a-video stays as top-of-funnel.

**PRO — $39/mo, annual $348 pushed hard.** Daily brief + alerts + "since you last checked"
diffs on followed narratives + **Thesis Intake** (the user's own dated positions scored on
the same clock). Priced at the top of the band deliberately: at $39 viability needs 70 subs;
at $29 it needs 95.

## The arithmetic (from the repo's real costs)

- LTV at $39/mo with finance-category churn (11.7–16.7%/mo): **$225–321 net of Stripe**.
- Viability: **~70 paying subscribers** covers a 30-narrative weekly shelf ($87/mo API on
  Opus, $18 on Haiku) + $2,500/mo founder income.
- The churn treadmill: holding 70 subs ≈ **10 new payers every month, forever** ≈ 100–200
  new engaged free users/month at 5–10% conversion. That number — engaged free users/month —
  is the real KPI and nothing currently measures it. Annual prepay is the escape hatch.
- **Human adjudication is the binding constraint, not API cost**: ~$12.50 of founder time
  per resolution; at a 100-narrative hot shelf, 12–17 hrs/month before triage or disputes.
  The API side of the "every new video" dream drops from $5,750/mo to ~$170/mo with three
  engineering fixes; the human side does not drop, and it IS the product.

## Structural findings that change the code

1. **Quadratic cost bug**: analyze.mjs ships the entire shelf summary (12 sample videos per
   narrative) as input on *every* call. At 100 narratives that's $0.38/call. Fix: candidate
   retrieval (top ~5 narratives per call) → linear, ~$0.07 flat. Plus: Haiku for
   classification-grade calls (5x), Batch API for cron work (2x) → ~10x total.
2. **The free paste flow is an uncapped cost bomb**: every paste spends founder money
   ($0.07–0.38) and *writes to the database* (including founding narratives). 100 pastes/day
   = $210–1,140/mo of other people's usage plus unbounded growth of the adjudication queue.
   Rate limit + new-narrative quarantine (~2–3 days work) is a launch prerequisite.

## The ladder, adjudicated

| Rung | Verdict |
|---|---|
| Free (brief + shelf + paste) | **Real** — after rate caps. Does ALL acquisition; no paid CAC works at $225–321 LTV |
| Pro $39 | **Real — the one paid rung that pencils** (~5–7 weeks of infra: Stripe, auth, diff cron, email) |
| Professional $100–300 | **Fantasy year one.** That buyer buys a *track record*; none exists yet |
| Teams | Deferred — trigger: 3+ Pro users from one org |
| Data/API | Deferred — trigger: inbound institutional interest; remember the graph is backfillable, only the adjudication feed isn't |

## The flywheel, made honest

The pasted vision's flywheel ("pastes make classification better") does not exist — there is
no learning loop. The ladder precedents show the condition under which consumer→pro works:
**the consumer act must generate the asset the professional buys** (Glassdoor reviews,
LinkedIn profiles, TradingView's published charts). Ground News fails this condition and so
buys every user with sponsorships forever; NewsGuard's consumer tier died of it.

The fix is already on the roadmap: **Thesis Intake as the consumer act.** Users logging dated
positions creates aggregate retail positioning/crowdedness per narrative — exactly the
"positioning with receipts" a professional tier sells. The consumer confesses; the aggregate
confession is the product. Secondary: paste-as-nomination with a dispute path (reader-tips
pattern) turns pastes into an error-correction layer on the standard.

## Extension, geo, schemas

- **Browser extension: a trap for now.** NewsGuard proved consumers won't pay for a context
  layer; uBlock/SponsorBlock proved the price is zero; Vanced proved Google kills what
  annoys it. Revisit only when paying Pro users ask for it.
- **Geographic perspectives: mission, not wedge — with one cheap probe.** BBC Monitoring
  (government subscription) and grant-funded NGOs are the only players; African-ecosystem
  framing is a real coverage hole but has no validated buyer. The probe: a "views from
  elsewhere" panel using English-language international outlets already on YouTube (CGTN,
  Al Jazeera EN, DW, CNBC Africa) through the existing pipeline at ~$0.10/narrative — the
  Semafor Signals move. Tests demand before any multi-language spend.
- **Domain schemas: 80% already built for finance** (claims/camps = mechanism, indicators =
  catalyst/indicator, relations = structure). The one schema move that is a moat rather than
  a taxonomy hobby: **structured due dates** `{due_start, due_end, precision}` on all 26
  ledger entries + the analyze schema. That single field unlocks the resolver cron, the
  first scored resolutions, "what changed" alerts, and Thesis Intake scoring.

## The convergence

Four independent research programs — data-moat, Portable Thesis, observability, and this one
— now terminate at the same first move:

**Structured dates → resolver cron → published adjudication rule → first real scorecard →
the weekly brief that announces it.**

Everything else in the vision (Teams, API, extension, geo, health, multi-sensor) is staged
behind named triggers, not calendar dates.
