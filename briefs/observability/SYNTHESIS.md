# Narrative Observability — research synthesis (15 Aug 2026)

Seven-lens investigation (repo/data audit · metric design · comparables · adversarial critic ·
clocks & monitoring · UX architecture · user & business). Full reports in this directory.

## VERDICT

**Reject "observability" as the core and as the positioning. Keep one of its three layers —
and it is not the one the proposal leads with.**

The three-layer model is **ordered backwards**. ACCOUNTABILITY is the product; STRUCTURE is
supporting evidence; ATTENTION should be deleted by name, not deferred.

## Ground truth that governs everything (measured, not asserted)

| | Reality |
|---|---|
| Narratives | **6**, not 7 (`loop-engineering` is queued with no corpus directory) |
| Videos | **86**, not ~110 |
| Concentration | 2 narratives hold 70 of 86 videos; 4 hold 16 between them |
| Time series | **None.** `views` is a display string captured once at `first_seen`; `age_days` is age-at-capture; no cron; `.github/workflows` is deploy-only |
| Capture dates | Every video in a narrative shares one `first_seen` (collapse: 33 on Aug 6; crypto: 25 on Aug 7) → **Δ-anything is uncomputable** |
| Ledger | 26 entries, 2 narratives. **Zero SUPPORTED entries exist anywhere in the repo** |
| Novelty verdicts | Assigned from **title + channel + view count only** — `analyze.mjs:119` says "metadata-only, no transcript"; `:155` writes `transcript: null` |
| 360 map | Hand-seeded (`minted_by: "hand-seeded"`); **2 of 7 edges** pass the project's own ≥3-video/≥2-channel gate; zero `counters` edges |
| Tiles | **5 of 7 have exactly one live number: a model-estimated age** |

**The founder's own internal description of the corpus was 28% larger than the corpus.** For a
product whose pitch is "we keep the receipts", soft self-reporting is a category error.

## Why ATTENTION must be deleted, not deferred

1. **Uncomputable.** No time series exists. Heat/velocity/breadth require history the product
   has never stored.
2. **Contaminated by the operator.** Six narratives were seeded with an identical 6-query
   template and returned 38/32/6/6/3/1 videos. That variance is *sweep execution*, not narrative
   size. Any ranked list keyed on volume ranks the founder's browsing history.
3. **It rebuilds the enemy.** A home page ranked by heat is not "like" a feed — it *is* one:
   items ordered by current attention, refreshed on a clock, rewarding return visits. The brand
   line is "The algorithm pulls you deeper. This is the exit."
4. **It encodes the error the product exists to correct** — repetition read as evidence.
5. **It monetises through dwell time**, contradicting the stated metric (time-to-orientation).
6. **It is commodity.** Tubular from $1k/mo; Brandwatch/Meltwater/Talkwalker/Zignal $6k–150k/yr.

## Does the Aug 2026 nine-niche kill verdict apply here? Partially — and precisely

| Claimed asset | Status |
|---|---|
| Attention layer | **Dead as a moat.** Commodity from $0 to $1k/mo |
| Structure layer (topology, contestation) | **Dead as a differentiator.** Funded natives' territory, and they are not thriving (Cyabra: NATO + State Dept + PepsiCo as clients *and* a going-concern warning) |
| "Deleted content is the moat" | **FALSIFIED — retire this claim.** Filmot indexes ~645M videos with captions. Repeating it in front of anyone who knows Filmot exists is expensive |
| "Time-in-market: competitors start at n=0" | **Downgraded to a speed bump.** The founder backfilled 11 years of Dalio calls in two weeks with an LLM. So can anyone |
| **The adjudication standard** — a published, fixed rule for what counts as a claim and what counts as resolution, applied by a named party *before* outcomes are known | **SURVIVES.** Not a data moat; an institutional/reputation moat |

The nine-niche rule demanded "a privileged position, not a cron job." **A standard that others
cite is a privileged position** — earned through consistency and citation rather than bought
with a data licence. Precedents: Moody's, Morningstar, Metacritic, PolitiFact. Slow, low-revenue,
real. Enter with eyes open.

**The genuine structural difference from the nine niches:** they all resold an *observation* —
the number existed before the collector arrived. **This resells a *judgement*.** A dated,
attributed, horizon-bound claim with an adjudicated outcome does not exist anywhere until
someone creates it. Filmot has the sentence; nobody has the verdict.

**The verified coverage hole:** there is no official YouTube captions API for third-party video,
and Brandwatch's audio transcripts are broadcast-only. **A $36k/yr enterprise listening suite
literally cannot tell you what a YouTuber said.**

## The real moat — and it is unbuilt

Not the archive, not time-in-market. **Continuous re-observation of named predictors, so that
goalpost-moves and deletions are captured while they happen.** That requires exactly one thing
the product lacks: a scheduled job that re-checks what it has already seen. It is cheap (a
fetch-and-store cron, well inside a Workers free tier). Build it pointed at the ledger, and the
time series ATTENTION wanted arrives as a byproduct — *earned rather than asserted*.

## Primary user

**Self-directed active investor (macro/crypto) already paying $39–99/mo for market context.**
Passes all four tests simultaneously: weekly need · proven WTP (SpotGamma retail $99/$299; Kaito
Elite $833/mo, 500+ investment teams) · corpus genuinely relevant (4 of 6 live narratives are
Economy & markets) · reachable solo (self-serve, no procurement/SOC 2).

**Sell positioning and crowdedness with receipts — never alpha.** Nobody trades off "Dalio was
refuted."

**Year-one Malik is the mission, not the buyer.** He would not have bought this: at the moment
he most needed it he still believed the guru, and people pay for confirmation, not
disconfirmation. Serve him with the free public shelf — that is the marketing, the SEO surface
and the moral point. Ground News, the best-executed consumer media-literacy product, prices at
$9.99–99.99 **per year** and needs ~60k stories/day to justify it. Not a solo business.

**Churn warning:** paid finance newsletters run ~11.7–16.7% monthly churn (6–8.5 month
lifetimes). Subscribers buy for a window and cancel. Must be answered structurally.

## Best wedge

**YouTube trading/market-call channels, scoring the claims that are NOT tickers** — regime and
strategy claims ("the crash comes in Q4", "this setup wins 90% of the time"). FinTuber and
FinfluencerTracker already own ticker picks; listening suites cannot see spoken YouTube at all;
resolution pins to public price data so it stays cheap; the buyer is the founder's own year-one
self; price proven at $8–30/mo. And it is the founder's own story, productised.

## Primary existential threat: platform policy, not competition

YouTube Developer Policies cap stored API data at **30 days** before mandatory delete-or-refresh
and require re-verifying every 30 days that a video has not been deleted — *specifically hostile
to keeping a record of deleted content*. Kaito lost ~70% of product utility to one X policy
change; Logically went into administration when Meta and TikTok cancelled. Mitigations:
derived-artifact-only storage, explicit ToS posture, no single-platform dependency.

## The next three moves (none is an observability feature; all three are the product)

1. **Fix `resolved`** (`index.html:756`) to include UPDATED and AMBIGUOUS so the ledger becomes
   visible. `collapse-audit` has 7 gradeable outcomes and currently renders "2 / 7 — too few to
   score fairly." The gate is blocked on the only narrative that ever resolved anything.
2. **Stand up a re-observation cron** aimed at the 14 all-PENDING crypto predictions and the
   videos carrying them.
3. **Rebuild the novelty verdict on transcripts.** Today it is a title classifier and must never
   render as a percentage until it isn't.

## Also fix (verified defects)

- `parseHorizonDate` takes the first 4-digit year in free text: `"by ~2026-2028"` → 2026-07-01,
  which sits on the 45-day grace boundary, so collapse-audit's "next test" flips between *due
  now* and *686d* with no data change. Store structured `{due_start, due_end, precision}`.
- 4 of 12 collapse horizons and most vague ones parse to **null** ("~1-2 years", "near-term").
- Overdue-PENDING drift: nothing wakes up and asks "did this land?" A ledger with no resolver is
  a to-do list.
- Stored prose drift: crypto expert text says "12/18 original"; data is 13 of 32.
- `fingerprints` does not exist in any `claims.json` — the trace-origin phrase suggester silently
  falls back to a name-derived string.

## Positioning

**Drop "observability."** Observability pays because of the pager, the SLO and the dollar cost of
an incident. There is no on-call here, and buyers who *do* have narrative incidents are
enterprise comms/national-security accounts needing forward-deployed engineers at $50–150k.

**Use instead:** *the record of who said what, when they said it would happen, and whether it
did.* Checkable, true to the corpus, needs no coverage promise, survives at n=6, requires no
home-page feed, and keeps a verdict at the centre.

## Portable Thesis placement

Reject "optional communication layer after interpretation" — it reintroduces the opinion factory
in better clothes. The correct object remains **Thesis Intake**: the user's own dated position
put on the same clock, scored on arrival. Its role is not communication; it is **retention and
the only genuinely privileged data in the system** (the user's own calibration record).
