## LENS 2 — NARRATIVE STATE MODEL AND METRIC INTEGRITY

**Verdict in one line:** the proposed nine-signal vector is roughly half-measurable on the current data. Three signals (HEAT, VELOCITY, and any attention-weighted composite) must be **killed outright** — not gated, killed — because the pipeline does not capture the quantities they claim to report. Four survive as first-class with tightened definitions. Two of the missing candidates (**corpus coverage/confidence** and **resolution density**) are more valuable than anything in the founder's original list, and one of them should render *above* every other number on the page.

Everything below is grounded in the files, not in the pitch.

---

## PART 1 — THE SUBSTRATE AUDIT (what the data can actually support)

Six facts about the pipeline that constrain every metric. All verified.

**S1. Views and age are frozen at index time and never refreshed.**
`/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/collector.py` lines 168–176: `age_days` is computed, then `if v["videoId"] in known: continue` — known videos are skipped *before* any field is written back. `views` is captured once, in the sweep that first saw the video, and never updated.

The consequence is fatal for HEAT. In `collapse-audit`, the top video carries 3,949,652 views (indexed roughly 12 days after publication); in `crypto-winter-watch`, a video carries 25 views (indexed at "1 hour ago"). These two numbers are not on the same scale — they are readings of different clocks. Summing them, ranking by them, or normalizing them produces a number with no referent.

**S2. 40% of the corpus has no attention data at all, and the fallback fabricates a date.**
34 of 86 videos (`user-submitted` and `auto-buildout`) have `published: ""`, `age_days: null`, `views: ""`. `viewsNum()` (`index.html:707`) returns **0** for missing views — unknown silently becomes zero. Worse, `publishedEst()` (`index.html:718`) falls back to `first_seen` when `age_days` is null, so an operator-pasted video is dated *as if it were published on the day the operator pasted it*.

Measured consequence: `crypto-winter-watch`'s "recent 20" window is **14 of 20 operator-added videos**. The Radar Read line "recent coverage is heavily recycled" is, on that narrative, substantially reading the operator's paste log.

**S3. There is no time series. There is one sweep burst per narrative.**
`collapse-audit`: 33 of 38 videos share `first_seen: 2026-08-06`. Every narrative has 1–3 distinct `first_seen` values. Velocity, acceleration, trend, and staleness all require repeated observation of the same narrative over time. That data does not exist yet, for any narrative.

**S4. The corpus is structurally a 14-day window.**
`KEEP_DAYS = 14` (collector.py:32) discards anything older than two weeks at sweep time. A narrative "born 2015-03" can only ever show the last fortnight of its coverage. Anything older enters by hand. Any metric phrased as a property of the narrative rather than of the window is a lie by omission.

**S5. The denominator is thrown away.** The collector builds `found` (everything the queries returned) and persists only `fresh` (what was new and recent). The count of what the search saw is printed to stdout and discarded. This is the cheapest high-value fix in the entire system — persisting `seen_count` per sweep is what converts "we indexed 12 videos" into "12 of 61 the queries returned."

**S6. The query set is the sampling frame, and it is authored — but it is already recorded per video.** Every video stores its originating `query`. `collapse-audit`'s six queries are *"ray dalio collapse", "80 year cycle economy", "billionaire warning AI economy", "debt crisis prediction", "dollar collapse prediction", "AI bubble crash warning"*. Every one presupposes the crash frame. **Zero counter-framed queries exist.** This is the direct, mechanical cause of the known defect "zero `counters` edges exist" — you cannot index an anti-narrative you never searched for.

---

## PART 2 — TRIAGE OF THE PROPOSED VECTOR

| Proposed | Ruling | Reason |
|---|---|---|
| **HEAT** | **Kill as a signal.** Demote to a per-video exhibit. | S1 + S2. Frozen single-point snapshots at non-uniform ages, missing on 40% of the corpus, with missing coerced to 0. No aggregation of these is honest. |
| **VELOCITY** | **Kill today. Re-open at ≥3 sweeps.** | S3. Requires a time series that does not exist. The honest remnant — publication density inside the sampled window — survives separately and must not carry the name "velocity." |
| **BREADTH** | **First class**, redefined as *channel spread of the sample*. | Already computed (`spread`, index.html:757). Sound, cheap, creator-proof. |
| **CONCENTRATION** | **Redundant — merge into BREADTH.** | Distinct-channel count and top-3 share are two readings of one distribution. Shipping both as separate dials double-counts one fact and invites the reader to treat them as corroborating. One signal, two numbers, one line. |
| **NOVELTY** | **First class**, split by evidence grade. | The verdict mix is the product's actual proprietary judgment. But metadata-only verdicts and transcript-backed verdicts are different epistemic objects and the distinction is already in the data (`transcript` flag, and the `[live analysis, metadata-only]` prefix in `verdict_note`). |
| **MUTATION** | **First class. Strongest asset in the set.** | Human-curated, creator-proof, and it is the moat (it exists only because earlier versions were recorded). Currently under-specified — see the citation gap below. |
| **CONTESTATION** | **First class**, redefined structurally. | Move from "count of contested claims" to camp count + thinnest-camp independence. |
| **CLOCK PRESSURE** | **First class. The cleanest signal in the product.** | Derived purely from `predictions.json` horizons vs. today. Touched by none of S1–S6. Calendar dates mean the same thing across every narrative — the only signal where cross-narrative comparison is unconditionally valid. |
| **ACCOUNTABILITY** | **First class but must split into three.** | The current single concept conflates *hit rate*, *resolution density*, and *slippage*, which have different denominators, different gates, and different legal exposure. |

**Missing candidates — rulings:**

- **Corpus coverage / confidence — ADD, and rank it first.** This is the metric that makes every other metric honest. It is currently absent, which means the UI renders a sparse metric grid for a 3-video narrative and a 38-video narrative in the same visual register.
- **Resolution density — ADD.** Orthogonal to hit rate, valid at n=1, needs no gate, and it discriminates sharply on the real data (below). Arguably the single most interesting number the product can print.
- **Slippage — ADD as a distinct signal**, but note it is only half-computable today (schema gap below).
- **Staleness / silence — DEFER.** Same blocker as velocity (S3). An honest partial exists now ("newest publication date in corpus") but it measures sweep recency, not narrative silence, and must be labelled as such or not shipped.
- **Lifecycle stage — REJECT as a number.** It is an interpretation, which is precisely what the product promises not to render, and it depends on velocity and staleness the product cannot measure. `buildRadarRead()` already expresses it as prose from age + mutation count. Leave it there.
- **Attention-weighted recycled share — REJECT, explicitly and permanently.** It multiplies the product's *best* signal (analyst verdicts) by its *worst* data (frozen, 40%-missing views). Compound error dressed as sophistication. Name it in the design doc as a rejected metric so it does not get proposed again.

---

## PART 3 — THE SURVIVING SET (9 signals, 4 layers)

Renaming note: the ATTENTION layer should be called **SAMPLE**. The product does not observe attention; it observes a search-seeded sample. Naming the layer honestly does more integrity work than any disclaimer placed beneath it.

---

### TIER 0 — CONFIDENCE (renders above everything, gates everything)

#### 1. Corpus Confidence Tier

**Definition:** an ordinal characterization of whether this narrative has enough corpus to be characterized at all.

**Formula** (all inputs exist today):
```
n            = videos.length
n_dated      = count(age_days != null)            // real publication data
n_transcript = count(transcript != null)
n_channels   = distinct(channel)
sweeps       = distinct(first_seen where query not in {user-submitted, auto-buildout})
last_sweep   = max(first_seen)

gates:  SCALE        n_dated >= 10
        DEPTH        n_transcript / n >= 0.5
        INDEPENDENCE n_channels >= 5
        RECENCY      today - last_sweep <= 14        // = KEEP_DAYS

TRACKED = 4 gates passed · SAMPLED = 3 · SEED = <= 2
```

**Normalization:** none. Absolute thresholds, identical across narratives, deliberately. A narrative either has a corpus or it does not.

**Current state:** `collapse-audit` TRACKED (38 videos, 31 transcripts, 34 channels). `crypto-winter-watch` TRACKED/SAMPLED boundary (32 videos, 18 transcripts, 23 channels). **`housing-crash-watch`, `the-2026-setup`, `psi-declassified`, `open-vs-closed-ai-race` are all SEED** — 1 to 6 videos, zero transcripts, zero real sweeps. Four of seven narratives currently render a full metrics UI on top of no corpus.

**Honest label:** "SEED — 3 videos, none read in full, no sweep run. Not enough to characterize."

**Integrity interrogation.** *Measures:* how much the operator has collected. *Does not measure:* how much exists in the world. *Moved by:* operator sweeps, transcript availability, query breadth. *Gameable by creators:* no. *Gameable by operator:* yes, trivially — running more sweeps raises the tier. That is the correct behavior, because the tier is explicitly a claim about the operator's work, not about the narrative. *Direction:* TRACKED is not good and SEED is not bad; a SEED narrative may be more important than a TRACKED one. Label it "how much we have looked," never "signal strength."

---

### LAYER A — SAMPLE

#### 2. Channel Spread

**Definition:** how many distinct channels carry this narrative in our sample, and how concentrated the sample is.

**Formula:** `n_channels = distinct(channel)`; `top3_share = sum(top 3 channel counts) / n`. Gate: `n >= 10`.

**Normalization:** per-narrative only, **never cross-narrative**, because query count differs per topic. The number must always render with its frame: *"34 channels across 38 videos, from 6 queries, swept 6 Aug."*

**Honest label:** "Channel spread in our sample" — never "how widely the narrative has spread."

**Integrity interrogation.** *Measures:* diversity of sources our query set surfaced. *Does not measure:* real-world spread, audience size, or cross-platform reach (X is not indexed at all). *Moved by:* query count and query phrasing far more than by the world. *Gameable by creators:* essentially no — one creator cannot manufacture 30 channels cheaply. *Gameable by the operator:* yes, and this is the important one — **adding a query raises breadth without anything changing in the world.** Mitigation is structural, not verbal: breadth is never rendered without the query count on the same line. *Direction:* high spread does not mean true or important; a 34-channel corpus of clip farms re-cutting one interview is wide and empty — which is exactly what the Originality Mix is for.

#### 3. Publication Density in the Sampled Window

**Definition:** the honest, non-trending remnant of VELOCITY.

**Formula:** `count(age_days != null && age_days <= 14) / 14` → videos/day, stamped with the sweep date.

**Honest label:** "12 videos published in the 14 days before the 6 Aug sweep, from 6 queries — 4.2/day equivalent." **The word "velocity" is banned until ≥3 sweeps exist**, and when it arrives it must be a *delta between sweeps*, never a slope through `first_seen`.

**Integrity interrogation.** *Measures:* publication rate among videos our queries surfaced that were young enough to survive `KEEP_DAYS`. *Does not measure:* the world's publication rate, or any change over time. *Moved by:* S4's 14-day truncation, query phrasing, and YouTube's own ranking of "newest." *Gameable:* by the operator (sweep more often, more queries); by a creator only through volume. *Confidence:* low. Ships only at TRACKED tier. *Direction:* neutral — a fast-publishing narrative is not a true or false one.

#### (not a signal) Reach at Index — a per-video exhibit

Views survive **only** as a per-video attribute in the corpus table, rendered as `"3.9M views · as counted 6 Aug, 12 days after publication"`. Never summed, never averaged, never used as a weight, never sorted across videos with different index ages. `viewsNum()` must be changed to return `null` for missing rather than `0`, and the UI must print "views not captured" rather than a zero.

---

### LAYER B — STRUCTURE

#### 4. Originality Mix

**Definition:** the distribution of analyst verdicts across reviewed videos, split by evidence grade.

**Formula:** over `reviewed = n − UNREVIEWED`, the counts of ORIGINAL / DERIVATIVE / RECYCLED / CLICKBAIT, plus `transcript_backed = count(transcript != null)` and `metadata_only = count(verdict_note starts with "[live analysis, metadata-only]")`.

**Honest label:** *"Of 35 reviewed: 7 original, 15 derivative, 7 recycled, 6 clickbait. 31 read from transcript, 4 judged from title alone."* Rendered as counts. Never as a percentage, never as a single "originality score."

**Integrity interrogation.** *Measures:* one model's single-pass judgment about whether each video contributed new material. *Does not measure:* truth, quality, or importance. **An original lie is still a lie; a recycled clip of a correct claim is still correct.** *Moved by:* the classifier prompt, and whether a transcript was available at all. *Gameable by creators:* yes, and cheaply — 30 seconds of fresh commentary bolted onto a re-cut can push DERIVATIVE toward ORIGINAL. Say so on the page. *Gameable by operator:* yes, via prompt wording. Mitigation: publish the verdict definitions verbatim and expose `verdict_note` per video so any user can check the reasoning. *Confidence:* medium for transcript-backed, **low for metadata-only** — and the two must never be pooled into one number. *Direction:* neither high-original nor high-recycled is good; this is the most likely place for a reader to import a valence that is not there.

#### 5. Mutation Count and Mechanism Interval

**Definition:** how many times the *stated mechanism* of the same conclusion has changed, and how often.

**Formula:** `k = mutations.length`; `span_months = last(mutations).date − born`; `mean_interval = span_months / (k − 1)`.

**On real data:** `collapse-audit` — born 2015-03, six mechanisms, latest 2026-07. **A new reason roughly every 27 months for 11 years, with the conclusion unchanged throughout.** That single sentence is the most defensible, least attention-contaminated statement the product can make, and no competitor with a 2026 start date can produce it.

**Normalization:** none needed — it is already in absolute time units. Fully valid cross-narrative.

**Schema gap to close:** `mutations[]` currently carries `{date, mechanism}` and **no citation**. This is the moat metric and it is the one metric with no evidence trail. Add `source` (videoId or URL) per mutation, and gate the number: display the count only when every mutation is cited, otherwise render the list without the derived interval.

**Integrity interrogation.** *Measures:* recorded restatements of the mechanism. *Does not measure:* whether restating was intellectually honest updating or goalpost-moving — the product must not imply the latter. *Gameable by the predictor:* barely — you can only avoid mutations by never restating. *Gameable by the operator:* yes, this is the real risk — the operator decides what counts as a mutation. Citations plus a `minted_by` provenance stamp (the pattern already used in `relations.json`) are the only defense. *Direction:* many mutations is not automatically bad. Say it in the copy: *"Updating a mechanism as evidence changes is what good forecasters do. What this records is that the conclusion never updated with it."*

#### 6. Contestation Structure

**Definition:** whether the corpus contains genuinely opposed camps, and whether each camp has independent support.

**Formula:** per contested claim in `claims.json` — camp count, sources per camp, and `distinct channels per camp` (join `sources[].videoId` → `videos[].channel`). Flag any camp with fewer than 2 distinct channels as **single-source**.

**On real data:** `crypto-winter-watch` "is the 4-year cycle dead" — 4 sources vs 9 sources across two camps; genuinely contested. `collapse-audit` "what triggers the crisis" — 3 / 1 / 2, so one camp is single-source. `housing-crash-watch` is marked `contested` with **one camp** — that is a schema violation, not a contested claim, and should render as consensus-of-three or as unreviewed.

**Integrity interrogation.** *Measures:* disagreement **among the videos our queries returned**. *Does not measure:* real-world or scientific contestation. A claim settled in the literature can look contested here; a claim fiercely debated can look consensual here. *Moved by, above all else:* **query vocabulary.** Per S6, all six `collapse-audit` queries presuppose the crash frame, so the corpus cannot surface counter-narratives, and the "zero `counters` edges" defect is a mechanical consequence rather than a finding about the world.

**Two required fixes, both cheap:**
1. Every topic's query set must contain at least one counter-framed query (`"why the housing crash isn't coming"`, `"debt doomers wrong"`). Add it to the topic-creation prompt in `analyze.mjs`.
2. The narrative page must display the query list verbatim, and where no counter-framed query exists, print: *"All 6 queries assume the crash frame. The absence of counter-narratives here is a property of the search, not the world."*

---

### LAYER C — ACCOUNTABILITY

This layer is the product. It is also the only layer untouched by S1–S6, because it reads `predictions.json`, not YouTube metadata.

#### 7. Clock Pressure

**Formula:** for each `PENDING` entry with a parseable horizon, `days_to_horizon`. Report `next_horizon_date`, `days_to_next`, and `overdue = count(PENDING with horizon_date < today)`.

**Honest label:** *"Next testable date: 1 Sept 2026 (17 days). Two calls are past their stated date and have not yet been judged."* Surfacing the overdue count turns the known defect into a visible integrity feature.

**Normalization:** absolute calendar dates. **The only signal in the set where cross-narrative comparison is unconditionally valid.**

**Integrity interrogation.** *Measures:* imminence of testability. *Does not measure:* importance or magnitude. *Gameable by the predictor:* yes — by never stating a horizon. **This is why signal 8b exists.** The pair is adversarially closed: a predictor can escape clock pressure only by becoming untestable, and becoming untestable is what resolution density measures. State this pairing on the page; it is the cleanest demonstration in the product that the metric set was designed against a motivated subject.

#### 8a. Ledger Census (replaces "hit rate")

**Fix the known defect precisely.** `computeReceipt` currently sets `resolved = SUPPORTED + REFUTED`, excluding UPDATED and AMBIGUOUS. Correct decomposition:

```
adjudicated = SUPPORTED + REFUTED + AMBIGUOUS + UPDATED   // no longer pending
resolved    = SUPPORTED + REFUTED + AMBIGUOUS             // outcome known
                                                          // UPDATED is a LIVE claim on a moved clock
```

**But fixing the arithmetic does not unblock scoring, and it should not.** Real census:

- `collapse-audit` (12 entries, one predictor): 2 REFUTED · 2 UPDATED · 3 AMBIGUOUS · 5 PENDING · **0 SUPPORTED**. Corrected `resolved` = 5 → exactly hits `SCORE_GATE`. The rate it would publish is **0 of 5** for a named living person, at the minimum sample, with AMBIGUOUS adjudicated by a model.
- `crypto-winter-watch` (14 entries, **13 distinct predictors**): 14 PENDING, 0 adjudicated.

**Two conclusions the data forces:**

1. **Never publish a percentage for a named individual. Publish the census.** "2 refuted, 3 ambiguous, 2 goalpost-moves, 5 pending, every entry sourced" is a *record* — the defensible legal-risk-arbitrage asset already identified. "Dalio accuracy: 0%" is an *opinion*, and it is the sentence that converts this product from a record into a liability. Drop the rate; keep and raise the gate for any derived rate you might later add.
2. **Accountability must be scoped per predictor, not per narrative.** `crypto-winter-watch` pools 13 people who openly disagree with each other; a narrative-level score there would average a bull and a bear into a meaningless number. Add `predictor` as the primary key of the ledger view — the current schema already stores it per entry.

#### 8b. Resolution Density

**Formula:** `dated = count(entries with a parseable horizon date) / total entries`. No gate — valid at n=1, because it is a property of the claims themselves rather than of a sample.

**On real data, it discriminates hard:** `collapse-audit` **3 of 12** claims carry a checkable date. `crypto-winter-watch` **12 of 14**. Same product, same schema, opposite behavior — one ledger is built of vague horizons ("unstated (vague)", "near-term"), the other of specific ones ("September 1, 2026 PMI print", "December 31, 2026").

**Honest label:** *"3 of 12 claims carry a date you could check."* No adjective. The number does the work.

**Integrity interrogation.** *Measures:* falsifiability of what was said. *Does not measure:* correctness, or sincerity. *Gameable by the predictor:* yes — by stating dates and then updating them, which shows up in slippage. *Gameable by the operator:* yes — the transcription of "horizon" from speech into the field is a judgment call. Mitigation: store the verbatim quote alongside the parsed horizon. *Direction:* deliberately unclear, and leave it that way. A vague forecaster may be more honest about their uncertainty than a precise one. Print the number; do not print a verdict about it.

#### 9. Slippage

**Definition:** total time added to a deadline across restatements of the same claim.

**Status: half-computable.** *Mechanism* slippage is available now from `mutations[]` dates. *Clock* slippage is not — each ledger entry has a single `horizon` field, and the moved-to horizon lives in `outcome_note` prose.

**Schema addition required (highest-value change in this document):** add `horizon_date` (ISO) and `superseded_by` (entry id) to prediction entries. Then `slippage_months = Σ(new_horizon_date − old_horizon_date)` over supersession chains, and the product can print: *"Across 11 years the deadline moved forward 2 times, adding N months."* Until then, print the count only (`buildRadarRead` already does), and do not imply a magnitude.

**Why this ranks first among schema changes:** it is the metric that literally cannot be reconstructed by a competitor. It exists only because earlier versions were recorded before they were superseded. Every month it is not captured is a month of moat permanently lost.

---

## PART 4 — THE RAW-VS-SCORE QUESTION

**Ruling: "Heat 84" is never justified. No composite index, no 0–100 scale, no unitless number anywhere in the product.**

Three reasons, in order of force:

1. **There is no population to normalize against.** A 0–100 score implies a distribution. n = 7 narratives, corpus sizes 1 to 38, start dates spanning six days, one of which has a 14-day corpus for an 11-year-old thesis. An 84 would be normalized against nothing, and it would go on meaning nothing at n = 70 unless the narratives were sampled comparably — which S6 guarantees they are not, because each topic has a hand-written query set.
2. **Composites hide confidence heterogeneity.** The inputs have radically different epistemic status: a mutation count is human-verified with dates; a views figure is a frozen snapshot with 40% missing coerced to zero. Any weighted sum of these launders the worst input through the credibility of the best one. That is the exact failure mode the founder already diagnosed and rejected in the SpotGamma analysis.
3. **A single number is a verdict**, and the product's stated promise is structure, not truth. The moment "Collapse Audit: 84" exists, it will be screenshotted without the page around it, and the product becomes the thing it was built as the exit from.

**The editorial law that replaces it — enforceable in code review:**

> Every number rendered in Narrative Radar is one of exactly three things: a **count with a unit**, a **share printed as k of n with the denominator visible**, or a **calendar date**. No unitless index. No number without a denominator or a unit.

**The single permitted exception** is the Confidence Tier, and it is deliberately rendered as **ordinal words** (SEED / SAMPLED / TRACKED) rather than a number — precisely because it gates, and a gate must not look like a measurement.

---

## PART 5 — UI-LEVEL ENFORCEMENT THAT ATTENTION ≠ TRUTH

Disclaimers do not work; readers skip them. These are structural, and each is cheap.

**E1. The sampling frame is attached to the number, not footnoted.** Every SAMPLE-layer figure renders with its frame inline, same line, dimmed: `34 channels · 38 videos · 6 queries · swept 6 Aug`. Not a tooltip, not a modal, not a section note. A number that cannot fit its frame on the same line does not ship.

**E2. Type hierarchy carries the epistemic hierarchy.** Three visually distinct bands, in this order: **WHAT ALREADY HAPPENED** (the ledger — the only band with accent color and the largest type), **WHAT IS CLAIMED** (structure — neutral), **WHAT WE SAMPLED** (attention — smallest, greyest, always frame-stamped). Today the receipt strip gives attention numbers the same visual weight as ledger outcomes. Inverting the hierarchy makes the layout argue the thesis without a word of copy: the only thing allowed to look important is the thing with an outcome.

**E3. No color, no arrows on SAMPLE or STRUCTURE metrics.** Green/red and up/down carry valence, and valence reads as truth. Color is reserved for the ledger's own defined statuses and for the confidence tier. A rising view count is not good news.

**E4. "How this corpus was built" on every narrative page.** The six queries verbatim, sweep dates, videos seen vs. kept (requires the S5 fix), operator-added count, transcript coverage. This is the highest credibility-per-pixel element available and it costs nothing — `query` and `first_seen` are already stored per video. It converts the product's largest weakness (search-seeded, analyst-triggered) into visible methodology. It is also the honest answer to the question in the brief: you do not build attention metrics on operator activity by hiding the operator — you build them by *putting the operator's fingerprint on the page as a first-class object*.

**E5. Empty states must say the true thing, not render a sparse grid.** This is the most dangerous current failure mode: four of seven narratives are SEED, and the UI renders the full metrics layout for them. A sparse grid reads as *low values*, not as *no data*. **Absence rendering as measurement is worse than any bad metric in this document.** A SEED narrative shows one sentence and the corpus list — no metric band at all.

**E6. The counter-search disclosure**, per signal 6 — print the query framing, and where the query set is one-sided, say so.

**E7. One-line honest labels, locked as copy.** "Channel spread in our sample" not "reach." "Publication density in the sampled window" not "velocity." "Reach at index, as counted 6 Aug" not "views." "3 of 12 claims carry a checkable date" with no adjective. Put these in a constants block so they cannot drift.

---

## PART 6 — BUILD ORDER

Pipeline fixes first; three of them must land before any new metric renders, because they change what the numbers mean.

1. **collector.py — refresh `views` and `age_days` on known videos, and persist `seen_count` per sweep.** Removes S1 and S5 together. Until this lands, every attention number is a frozen artifact and the coverage denominator does not exist.
2. **`publishedEst` — stop fabricating dates.** Return `null` when `age_days` is null instead of falling back to `first_seen`; exclude undated videos from the recency window entirely. Fixes the 14-of-20 contamination in `crypto-winter-watch`.
3. **`viewsNum` — return `null`, not `0`, for missing views.**
4. **Ledger schema — add `horizon_date` and `superseded_by`.** Every day this is missing loses moat permanently.
5. **`mutations[]` — add a `source` per entry.**
6. Ship Confidence Tier, and gate the four SEED narratives out of the metrics UI.
7. Ship the corrected ledger census (`resolved = SUP + REF + AMB`), scoped per predictor, **as counts with no rate**.
8. Ship resolution density, clock pressure with overdue count, mutation interval.
9. Ship SAMPLE-layer signals last, at the bottom of the page, in the smallest type — after the frame-stamping (E1) and "how this corpus was built" (E4) are in place.

**Files:** `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/collector.py` (lines 32, 150–190), `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/index.html` (`viewsNum` 707, `publishedEst` 718, `computeReceipt` 729, `narrativeStats` 766, `buildRadarRead` 795), `netlify/functions/sweep.mjs` (query cap at line 57, transcript cap at 61), and `corpus/<id>/{predictions,narrative,claims}.json` for the schema additions.

**The one-sentence summary for the founder:** the accountability layer is real, measurable today, and defensible; the structure layer is real but model-dependent and needs its evidence grades separated; the attention layer is not currently measured at all — it is a record of what the operator searched for on two days in August — and the correct move is not to fix it with better math but to rename it, shrink it, stamp it with its sampling frame, and let the ledger have the top of the page.