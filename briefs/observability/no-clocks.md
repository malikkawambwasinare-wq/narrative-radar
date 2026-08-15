
# Lens 5 — Clocks, Calendar and the Monitoring Loop

I ran the app's own horizon parser against every ledger entry in the corpus before designing anything. The measurements changed several of my conclusions, so I lead with them.

## 0. What I measured (ground truth, 2026-08-15)

Files: `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/collapse-audit/predictions.json`, `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/crypto-winter-watch/predictions.json`, parser at `index.html:722`.

| topic | id | status | horizon (stored) | parser output |
|---|---|---|---|---|
| collapse-audit | dalio-2015-1937 | REFUTED | `~1-2 years` | **null** |
| collapse-audit | dalio-2016-supercycle | UPDATED | `unstated (vague)` | null |
| collapse-audit | dalio-2018-downturn | AMBIGUOUS | `~2020` | 2020-07-01 |
| collapse-audit | dalio-2019-recession-risk | AMBIGUOUS | `~1-2 years` | **null** |
| collapse-audit | dalio-2020-cash-is-trash | AMBIGUOUS | `near-term` | null |
| collapse-audit | dalio-2022-perfect-storm | REFUTED | `~1-2 years` | **null** |
| collapse-audit | dalio-2023-debt-crisis | UPDATED | `unstated (vague)` | null |
| collapse-audit | dalio-2025-heart-attack | PENDING | `by ~2026-2028` | **2026-07-01 → false LAPSE** |
| collapse-audit | dalio-2025-doac-dark-times | PENDING | `unstated (vague)` | null |
| collapse-audit | dalio-2025-debt-3yr | PENDING | `by ~2028` | 2028-07-01 |
| collapse-audit | dalio-2026-capital-war | PENDING | `near-term` | null |
| collapse-audit | dalio-2026-doac-80yr | PENDING | `unstated (vague)` | null |
| crypto | armstrong-2026-clarity | PENDING | `before the August 2026 Senate recess` | **2026-08-28 → hides a real lapse** |
| crypto | gambardello-2026-pmi | PENDING | `September 1, 2026 PMI print` | **2026-09-28 (27 days late)** |
| crypto | gerhard-2026-selloff | PENDING | `coming weeks to months` | null |
| crypto | soloway-2026-35k | PENDING | `by October-November 2026` | 2026-10-28 |
| crypto | klippsten-2026-bottom | PENDING | `late October 2026` | 2026-10-28 |
| crypto | ivan-2026-bottom | PENDING | `Oct-Nov 2026 bottom; Jan-Feb 2027 blow-off` | **2026-10-28, second clock silently dropped** |
| crypto | fibswanny-2026-low-now | PENDING | `August-October 2026` | **2026-08-28 (earliest edge, not latest)** |
| crypto | hougan-2026-higher | PENDING | `December 31, 2026` | 2026-12-28 |
| crypto | hougan-2027-bull | PENDING | `2027` | **2027-07-01 (mid-year, not year-end)** |
| crypto | phongle-2027-bull | PENDING | `by August 2027` | 2027-08-28 |
| crypto | sophie-2028-cycle-intact | PENDING | `2027-2028` | **2027-07-01 (earliest edge)** |
| crypto | saylor-1m-no-winters | PENDING | `unstated (vague)` | null |
| crypto | ark-2030-710k | PENDING | `2030` | 2030-07-01 |
| crypto | pal-2030-singularity | PENDING | `by 2030` | 2030-07-01 |

**26 entries. 11 (42%) unparseable → invisible to the calendar and unscoreable forever. Of the 15 that parse, at least 7 parse to the wrong date.**

Four structural findings fall straight out:

1. **The parser has a hostility bias.** For a range it takes the *first* year (`2027-2028` → 2027; `by ~2026-2028` → 2026). For a bare year it uses July 1, not Dec 31. Both defaults make deadlines arrive *early*, which means the system's error mode is **refuting predictors before their stated window closes**. For a product whose entire asset is being trusted to score named people fairly, this is the most dangerous possible direction to be wrong in. It is also legally the wrong direction.
2. **The two known "lapsed but PENDING" entries are not what they look like.** `dalio-2025-heart-attack` shows lapsed only because the parser read `by ~2026-2028` as 2026 — a **false lapse**. Meanwhile `armstrong-2026-clarity` (`before the August 2026 Senate recess`) is genuinely past its real deadline but parses to Aug 28 and so is **not** flagged. The system is currently flagging a false lapse and hiding a true one simultaneously.
3. **Unparseable ≠ handled.** `parseHorizonDate` returns null and the entry silently vanishes from `next`. Six Dalio claims can never appear on any calendar, never come due, never be scored. They are not pending; they are lost.
4. **No heartbeat exists.** `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/.github/workflows/` contains only `pages.yml`. Sweeps are manual. `first_seen` in `videos.json` has only two distinct values (`2026-08-07`, `2026-08-08`) — it records collection date, not publication. **Nothing in the system currently knows what time it is.** Every design below depends on fixing this first.

---

## 1. What a clock is — the data model

### 1.1 The core distinction

A clock is **a dated commitment to a future observation**. Four kinds appear in the corpus already, and they behave differently enough that collapsing them is a mistake:

| kind | example in corpus | resolves by | who set the date |
|---|---|---|---|
| `dated_horizon` | Hougan: crypto ends 2026 higher | calendar arrival | predictor |
| `conditional_trigger` | FibSwanny: third monthly close under $64,618 | condition met (may never fire) | predictor |
| `external_event` | Armstrong: before the August 2026 Senate recess | world's calendar | world |
| `shared_trigger` | `relations.json` `shares_clock`: "10yr Treasury yield sustained above 5%", `next_check: 2026-12` | condition, watched by ≥2 narratives | operator |

Two of these are already modelled in the repo — `relations.json:shares_clock` carries `clock: {trigger, next_check}` and `indicators.json` carries `role: "countdown" | "trigger"` with `thresholds[]` each attributed to a named predictor. The schema seed exists; it just isn't unified or surfaced as time.

**Critical asymmetry:** only `dated_horizon` and `external_event` can *expire*. A `conditional_trigger` that never fires is not refuted — it is unresolved forever unless the prediction also carried a horizon. This is the loophole every rolling-doom predictor lives in, and the product should name it rather than paper over it. A trigger with no horizon should be labelled **open-ended** and excluded from the accuracy score while counting toward the vagueness rate (§1.5).

### 1.2 Clocks belong to predictions one-to-many, not one-to-one

`ivan-2026-bottom` stores `"Oct-Nov 2026 bottom; Jan-Feb 2027 blow-off"` — two independently scoreable commitments in one string, and the current parser keeps only the first. `soloway-2026-35k` similarly contains a near-term leg ($71-72K) and a bottom leg. `phongle-2027-bull` is explicitly two-part (timing + relative performance) and the `outcome_note` says so.

So: **`prediction.clocks[]`, not `prediction.horizon`.** Each clock scores independently; the parent prediction gets a rolled-up status. This alone roughly doubles the number of scoreable events without collecting a single new video.

### 1.3 Proposed clock record

```jsonc
{
  "clock_id": "ivan-2026-bottom#1",
  "prediction_id": "ivan-2026-bottom",
  "topic": "crypto-winter-watch",
  "predictor": "Ivan on Tech",
  "kind": "dated_horizon",
  "leg": "Bottom lands October-November 2026 near the 200-week MA",

  "window": {
    "opens": "2026-10-01",
    "due":   "2026-11-30",          // ALWAYS the latest edge of the stated range
    "precision": "month_range",      // exact_day | month | month_range | quarter | year | multi_year | conditional | none
    "basis": "stated",               // stated | derived | inferred | none
    "grace_days": 30,
    "stated_text": "Oct-Nov 2026 bottom; Jan-Feb 2027 blow-off"
  },

  "resolution_spec": {               // WRITTEN AT ENTRY TIME. see §3.1
    "observable": "BTC/USD daily close, any exchange in {Coinbase, Binance} composite",
    "supported_if": "the lowest daily close of the 2026 drawdown occurs between 2026-10-01 and 2026-11-30",
    "refuted_if":   "a daily close below that window's low occurs after 2026-11-30 and before 2027-06-30",
    "evidence_tier": "A",
    "known_ambiguity": "‘bottom’ is only knowable in retrospect; needs a lookback bound — hence the 2027-06-30 clause"
  },

  "state": "PENDING",                // PENDING | DUE | OVERDUE | RESOLVED | VOID | OPEN_ENDED
  "verdict": null,                   // SUPPORTED | REFUTED | UPDATED | AMBIGUOUS
  "scored": null                     // see §3
}
```

### 1.4 Parsing the messy horizons — concrete rules

Ordered rules, applied to the strings actually in the corpus. Every rule states its `basis` so the UI can show provenance.

| # | pattern | rule | basis | corpus cases fixed |
|---|---|---|---|---|
| 1 | explicit day (`September 1, 2026`, `December 31, 2026`) | use that exact day, `precision: exact_day` | stated | 2 (currently off by 27 and 3 days) |
| 2 | month + year (`late October 2026`) | due = **last day of that month** | stated | 2 |
| 3 | month range (`October-November 2026`, `August-October 2026`, `Jan-Feb 2027`) | opens = first day of first month, due = **last day of last month** | stated | 4 (currently 3 take the earliest edge) |
| 4 | year range (`~2026-2028`, `2027-2028`) | due = **Dec 31 of the LATER year** | stated | 2 (currently both take the earlier year) |
| 5 | bare year (`2027`, `2030`) | due = **Dec 31**, `precision: year` | stated | 4 |
| 6 | `by <X>` | due = end of X, same as above | stated | 4 |
| 7 | relative duration (`~1-2 years`, `~3 years`, `within the next year`) | due = `date_made` + **upper bound** of the duration | **derived** | 4 — recovers 3 currently-null Dalio entries |
| 8 | named external event (`before the August 2026 Senate recess`) | resolve against an `events.json` calendar of scheduled real-world dates (recesses, FOMC, midterms, halvings, earnings, elections); if absent, operator supplies the date | stated (date) + inferred (lookup) | 1 — and this is the entry currently hiding a true lapse |
| 9 | conditional (`third monthly close under $64,618`, `PMI above 55`) | `kind: conditional_trigger`, no `due` unless a horizon co-occurs; state = `OPEN_ENDED` | stated | all `indicators.thresholds[]` |
| 10 | soft-relative (`near-term`, `coming weeks to months`) | **do not guess.** `precision: none`, route to operator triage (§1.5) | none | 3 |
| 11 | `unstated (vague)` | `precision: none`, `unfalsifiable_as_stated: true` | none | 5 |
| 12 | compound (`;` or two dated legs) | split into N clocks **before** applying 1-11 | — | 2+ |

Two hard invariants:

- **Never take the earliest edge of a range.** Ranges always resolve at their latest edge. Any premature refutation is a credibility event the product cannot afford.
- **Never silently return null.** Rules 10-11 produce a *record*, not an absence.

### 1.5 Unparseable horizons are a feature, not a failure

This is the part I'd push hardest. Route every `precision: none` clock into a **Register of Unfalsifiable Claims**, and require the operator to choose exactly one of:

- **(a) attach an inferred deadline** — `basis: "inferred"`, with a visible operator note. Shown in the UI in a distinct style: *"Narrative Radar assigned this deadline; the predictor did not state one."* Scoreable, but a footnote follows it forever.
- **(b) mark `unfalsifiable_as_stated: true`** — excluded from the accuracy score entirely, counted in the vagueness rate.

There is no option (c) "leave it null", which is what happens today.

**The vagueness rate is the single most valuable metric in this whole lens, and it needs no clock at all.** Measured on the current corpus:

- **Ray Dalio: 6 of 12 entries (50%) carry no stated bound** (`unstated (vague)` ×4, `near-term` ×2). Zero of 12 are hard-dated.
- **Crypto ledger, 13 predictors: 1 of 14 (7%) unfalsifiable; 2 of 14 hard-dated to the day.**

That contrast is publishable *today*, is fully deterministic, requires zero waiting, and directly answers the founder's own origin question — year-one Malik doesn't need to know whether Dalio is right, he needs to know that *half of what Dalio says cannot be checked*. It solves the accountability layer's cold-start problem, which is otherwise brutal (§5).

---

## 2. Clock pressure — argue it shouldn't be a number

**Recommendation: do not ship a scalar "clock pressure" score.** Three reasons, in descending order of force:

1. **It violates the product's own stated position.** The reframe is "make structure observable, leave interpretation to the user" — the SpotGamma analogy. A weighted blend of horizon proximity × predictor count × contestation is not an observation; it is an opinion with the weights hidden inside it. It is exactly the kind of composite that Lens-4-style critics rightly call an editorial index wearing a dashboard costume. The corpus already carries a rule that scores are gated at n≥5 precisely because unsupported numbers are the enemy; a pressure score would be an ungated one.
2. **It composes incommensurables.** Is "3 mutually exclusive calls resolving in 74 days" more or less pressure than "1 vague call from a famous person plus 4 overdue"? Any answer is a weight choice, and the weight choice *is* the entire content of the number.
3. **A single number invites ranking, and ranking narratives by urgency is engagement-farming wearing a new hat.** It produces a leaderboard that rewards whichever narrative is loudest this week — the algorithm the product exists as an exit from.

### What to ship instead

**Two observable numbers and one named object.**

- `days_to_next_judgment` — a count, directly readable, no weights.
- `claims_converging` — how many clocks fall inside that window.

And the object that actually carries the differentiation:

> **CONVERGENCE POINT** — a window in which ≥2 clocks from *opposing camps* come due.

The corpus already contains a textbook one, and it is the single best demo asset in the product:

> **October–November 2026 — 4 calls, mutually exclusive.**
> Soloway: flush to ~$35,000 · Klippsten: floor ~$57.5K, *no deep flush* · Ivan: bottom near the 200-week MA, then blow-off Jan-Feb 2027 · FibSwanny: the low is already in, October bottom never happens.
> `klippsten-2026-bottom.outcome_note` already says it out loud: *"one of them will be wrong on schedule."*

A convergence point is deterministic (camp membership already lives in `claims.json:camps[]`), needs no weights, and is *self-evidently* interesting without being told it is. It is the honest version of "pressure": pressure isn't a temperature, it's a **collision with a date on it**.

If a single glanceable token is needed for tiles, use a **categorical badge derived from threshold counts, not a blend**:

`QUIET` (no clock due <180d) · `TICKING` (≥1 due <90d) · `CONVERGING` (≥2 opposing camps due in same 60d window) · `RESOLVING` (≥1 DUE now) · `OVERDUE` (≥1 past grace, unscored)

Categorical is defensible because each state is a stated rule over observable counts, and the rule can be printed next to the badge.

---

## 3. The resolution ritual — the crux

The founder is right that this is the crux. A ledger that isn't scored is worse than no ledger: it looks like accountability while being its opposite, and the failure is invisible until someone checks — at which point the product's one differentiated asset is revealed as theatre. And note what the measurement above showed: **the system today cannot even reliably tell which entries are due.**

### 3.1 Pre-registration is the highest-leverage change in this entire lens

**A clock may not enter the ledger without a `resolution_spec` written at entry time.**

Without it, scoring at deadline is retro-fitting: the operator decides what "bottom" or "debt crisis" or "perfect storm" meant *after* seeing what happened, which is precisely the sin the product accuses its subjects of. `dalio-2018-downturn` shows the trap live — a 2020 recession happened, but via COVID, not the predicted debt mechanism, so it landed AMBIGUOUS. That call was defensible only because the mechanism was recorded. With no pre-registered spec, that entry could have been scored SUPPORTED by a sympathetic operator or REFUTED by a hostile one, and neither would be checkable.

Pre-registration is also what makes the ledger a **moat rather than a diary**: a competitor with $50M can buy transcripts, but cannot retroactively manufacture specs written before the outcome was known. That is time-in-market made verifiable.

`resolution_spec` minimum fields: `observable` (the specific series/record consulted), `supported_if`, `refuted_if`, `evidence_tier`, `known_ambiguity`. If the operator cannot write `refuted_if`, the claim is unfalsifiable — route to §1.5(b). **That test alone is the entry gate.**

### 3.2 Who scores

**Model drafts, human commits. Never model-auto-commit. Never crowd.**

- **Model drafts.** On `DUE`, a function (the existing `netlify/functions/` pattern extends naturally) produces a *proposal*: candidate evidence, proposed verdict, proposed note, confidence, and an explicit "what would change this verdict" line. This is the labour-saver, and it's where the effort actually goes.
- **Human commits.** The operator confirms, edits, or rejects. Rationale is not squeamishness: (i) scoring a named public figure as REFUTED is an assertion about a real person, and the earlier research already identified legal-risk arbitrage — that arbitrage is only real if a human owns each verdict; (ii) a model that both drafts and commits will, at scale, quietly drift the ledger's standards, and no one will notice because there's no diff to review; (iii) the earlier portable-thesis finding — *machine-drafted positions get adopted, not edited* — applies with full force here, so the commit step must be a deliberate act, not a default-accept.
- **Not crowd.** At n=1 operator and ~7 narratives, crowd scoring is poisonable, has no quorum, and destroys the one thing that makes the ledger coherent: a single consistent judge applying one standard over time. Revisit only past ~10k engaged users, and even then only as *dispute flagging*, never as verdict-setting.

Store the commit: `scored: {by: "operator", at: "...", model_draft_id, agreed: true|false}`. **Publish the disagreement rate.** "The operator overrode the model draft on 22% of resolutions" is a credibility asset and costs nothing to produce.

### 3.3 Evidence standard — tiered, declared per clock at entry

| tier | standard | example |
|---|---|---|
| **A — public record** | a number or a discrete event with an authoritative public source | `gambardello-2026-pmi` (the Sept 1 ISM print); `armstrong-2026-clarity` (a Senate floor vote either occurred or didn't); any BTC price level |
| **B — reported event** | ≥2 independent named outlets describing the same event | "a US debt crisis occurred" |
| **C — judgement** | operator interpretation against the pre-registered spec | "very, very dark times"; "perfect storm" |

**Tier C clocks may not produce a SUPPORTED or REFUTED verdict — only AMBIGUOUS or UPDATED.** That is a strong constraint and I'd hold it. It means the accuracy score is built exclusively from A and B evidence, which is what makes it defensible; and it means vague-but-famous claims land in the vagueness rate instead of the accuracy score, where they can't be argued with. It also removes the operator's biggest temptation, which is scoring the dramatic claims because they're the interesting ones.

### 3.4 AMBIGUOUS — the state that decides whether the ledger is honest

AMBIGUOUS is not a shrug; it's the most information-dense verdict in the schema, and today it's structurally punished. **Fix the counting bug first** (`index.html:756`, `resolved: sup + ref`):

- collapse-audit actual counts: SUPPORTED 0, REFUTED 2, UPDATED 2, AMBIGUOUS 3, PENDING 5 (n=12).
- `resolved` computes as **2**, so the n≥5 score gate fails.
- True resolved (non-PENDING) = **7** — the gate should pass.

**The one narrative in the corpus with real resolved history is the only one being blocked from showing a scorecard, and it's blocked by an accounting choice, not by evidence.** Fix: `resolved = total − pending`.

Then require a **reason code** on every AMBIGUOUS, because the aggregate over codes is itself a finding:

- `mechanism_mismatch` — outcome occurred, predicted cause didn't (`dalio-2018-downturn`, `dalio-2019-recession-risk` — both COVID)
- `partial_magnitude` — direction right, size wrong
- `unfalsifiable_as_stated` — spec couldn't be written even at deadline
- `evidence_unavailable` — needed record doesn't exist or is paywalled
- `timing_only` — right window, wrong mechanism

AMBIGUOUS is **terminal but reopenable**: reopen only when new evidence appears, and every reopen appends to `history[]` and is shown. Never silently rewritten.

And publish AMBIGUOUS separately rather than folding it into a hit rate. "Dalio: 0 supported / 2 refuted / 3 ambiguous / 2 goalpost-moved / 5 pending, 50% of claims unbounded" is a far stronger and far more defensible object than any percentage. It also fits the stated integrity rule — structure, not truth.

### 3.5 Preventing silent rot — make rot visible and make it cost the operator

Willpower will not do this. The system must be built so that **an unscored clock degrades the product's own displayed credibility**, so neglect is punished by the thing the operator cares about.

**(a) Split PENDING into four states.** This is the structural fix — today one bucket hides both "not yet" and "we failed to do our job":

- `PENDING` — due date in the future. Nothing owed.
- `DUE` — due date reached, inside grace. **Operator debt.**
- `OVERDUE` — past due + grace, unscored. **Publicly visible operator debt.**
- `VOID` — clock invalidated (predictor retracted, prediction superseded). Requires a note.

`OVERDUE` must never render as `PENDING`. An overdue clock is a fact about *Narrative Radar*, not about the predictor, and conflating them is the exact rot being guarded against.

**(b) Ledger hygiene is a first-class, public number.** On every narrative and on the landing page:

> `Ledger hygiene — 24 clocks · 22 scored within grace · 2 overdue (longest 45 days)`

**(c) A stale ledger visibly downgrades the narrative.** If any clock is OVERDUE >30 days, the narrative tile shows `LEDGER STALE` and its scorecard is suppressed. This is the enforcement mechanism: the operator loses the feature he most wants to show off, precisely when he's earned that loss. It's the same logic as the existing n≥5 gate, applied to freshness instead of sample size.

**(d) Grace scaled to precision.** `exact_day` → 7d · `month` → 30d · `quarter` → 60d · `year` → 90d · `multi_year` → 180d. Prevents nagging on a 2030 clock and prevents dawdling on a dated one.

**(e) A DUE queue is the operator's weekly ritual**, and it's the one genuinely weekly thing in this whole design (§5). Weekly: open the queue, score what's due, triage new vagueness. If the queue is empty, the ritual takes ten seconds — which is the point.

**(f) Never allow a `resolution_spec` edit after `DUE`.** Log the attempt if made. This is the goalpost-move rule applied to the operator himself, and it should be stated publicly. A ledger that audits predictors while exempting its own author is not credible, and someone will eventually check.

---

## 4. The monitoring / follow loop

Current state: `follows()` at `index.html:695`, `FOLLOW_KEY = "nr-follows"` at `:1547` — a localStorage array of topic ids, no timestamps, no diff. No changelog, no sweep log, no scheduled sweep.

### 4.1 Two prerequisites before any of this works

1. **`sweep_log.json`** — `{topic, ran_at, queries[], results, new_items}` per sweep. Without it, silence is indistinguishable from neglect (§4.4), and *every* "since you last checked" claim is unfounded.
2. **`changelog.json` per topic** — append-only, **emitted by the writer, never inferred by the reader.** This matters concretely: the founder already knows *stored prose has drifted from stored arrays*. A client that diffs whole JSON blobs would fire a change event on every prose touch-up and drown the real signal on day one. Only `sweep`, `consolidate`, and operator commits may append.

Then extend follows to `{topic_id: last_seen_iso}` and diff client-side against the changelog. No accounts, no server, no tracking — consistent with the existing device-local design.

### 4.2 Complete taxonomy of change events, tiered

**TIER 0 — NOTIFY.** Accountability-class only. Everything here is a fact about a *person's stated commitment*, never about attention.

| event | why it earns a push |
|---|---|
| `clock.resolved` | the product's whole reason to exist |
| `clock.due` | someone is about to be right or wrong on schedule |
| `prediction.updated` (goalpost-move) | **the signature event.** The earlier research named the UPDATED/deadline-roll counter as a core moat — it exists only because the earlier version was recorded. Every goalpost-move is a proof-of-moat |
| `convergence.imminent` | ≥2 opposing camps due within 30d (the Oct-2026 crypto case) |
| `indicator.threshold_crossed` | only when a *named predictor* stated that threshold — e.g. FibSwanny's `$64,618 third monthly close`. The predictor pre-committed; the world answered |
| `narrative.contradicted_by_own_camp` | a predictor abandons the camp they founded |

**TIER 1 — QUIET DIFF.** Visible on return, never pushed.

new videos since last visit · verdict changes (UNREVIEWED→RECYCLED etc.) · new mutation recorded · new contested camp or new source in an existing camp · new relation edge (esp. the currently-absent `counters` type) · a shadow candidate promoted to tracked · corpus quality changes (transcript coverage, review backlog) · new predictor entering the ledger.

**TIER 2 — RECORD, SHOW NOTHING.** view counts changing · re-uploads and re-cuts of already-catalogued material · new video from an already-saturated channel · velocity fluctuation · anything with no new claim in it.

Tier 2 is deliberately large. Most of what a sweep returns is Tier 2, and it is exactly the class of event the incumbent algorithm treats as Tier 0.

### 4.3 The anti-noise rules

1. **Attention metrics may never trigger a notification.** Not views, not velocity, not new-video count, not "trending." This is a brand-level commitment, not a tuning parameter: *"The algorithm pulls you deeper. This is the exit."* A push that says "this narrative is heating up" is the app becoming the thing it was built to escape. Attention lives in the pull layer only.
2. **Hard budget: ≤1 push per followed narrative per week, ≤4 per user per month, across everything.** Overflow merges into the digest rather than queueing.
3. **No streaks, no badges, no unread counts, no "you haven't checked in."** Each is an engagement mechanic with no informational content.
4. **"Nothing happened" is a valid digest and should be shown.** An empty month is honest and is itself an observation about the narrative.
5. **Every notification states the fact and stops.** `"Klippsten's late-October bottom call comes due in 14 days. Soloway's $35K call resolves in the same window."` No question marks, no teasers, no "find out what happens next."
6. **A push must deep-link to the resolved object**, not to the narrative page. Time-to-orientation is the metric; a notification that dumps you at a landing page fails it.

### 4.4 Silence as an event

Silence is a real and under-served signal — and it's the one most aligned with the product's purpose, because the honest ending of most narratives is not refutation but abandonment.

**Definition (requires the sweep log):** `SILENCE` = ≥3 consecutive scheduled sweeps where `new_items` falls below 25% of that topic's own trailing 90-day median, **and** ≥1 prior sweep exceeded it. Topic-relative, so a slow narrative isn't perpetually "silent."

Two silence events worth surfacing, both Tier 1:

- **`wave_passed`** — heat spike followed by sustained silence. *"No new material in 6 weeks after 32 videos in August."* For a rider of the doom cycle, this is the most useful sentence the product can produce.
- **`silent_through_deadline`** — a clock came DUE and **no video in the corpus mentions it**. This is devastating and completely deterministic: the predictors moved on without scoring themselves. It's the machine-checkable version of the founder's own six-year experience. I'd rank this the second-most-differentiated event in the taxonomy after `prediction.updated`.

**Hard constraint:** silence may only be computed from *scheduled* sweeps. If the scheduler didn't run, the state is `UNKNOWN` and must render as "we didn't look", never as "nothing happened". Given there is currently no scheduled workflow, everything in §4.4 is blocked on adding one.

### 4.5 What to measure instead of engagement

Stated metric is time-to-orientation, never dwell. Loop-specific versions:

- **Resolution coverage** — % of DUE clocks scored within grace. Target ≥95%. *This is the product's health metric.*
- **Notification precision** — % of pushes opened within 48h. If it drops, cut volume; never raise it.
- **Resolution-driven return share** — % of sessions landing on a narrative with a resolution in the past 7d. This distinguishes "came back because something resolved" from "came back out of habit." Only the first is the product working.
- Explicitly **not** measured: sessions/week, dwell, streaks.

---

## 5. Honest assessment — do clocks sustain recurring use?

**Short answer: not weekly, not at current scale, and chasing weekly would break the product. But the founder's instinct that clocks are the most differentiated feature is correct — he's just wrong about which loop they power.**

### The arithmetic

From the measured data: 26 entries → 15 dated → **7 due within 12 months, all 7 inside a single narrative** (crypto-winter-watch). Five of seven narratives have no ledger at all. Distribution: Aug 2026 ×2, Sep ×1, Oct-Nov ×3, Dec ×1, then a **seven-month gap**, then 2027 ×3, 2028 ×1, 2030 ×2.

That is roughly **0.6 resolution events per month today**. Extrapolating at current per-narrative density (~13 entries, ~58% dated, ~47% of dated within 12mo):

| tracked narratives with full ledgers | resolutions/month | felt cadence |
|---|---|---|
| 7 (today's topics, fully built out) | ~2 | monthly |
| 15-20 | ~4-5 | biweekly |
| ~50 | ~12 | weekly |

**Weekly return from resolutions alone needs ~50 fully-laddered narratives.** That is a real target but it is quarters away, not weeks.

### The three things that follow from this

**1. Design for monthly and say so.** The natural artefact is a **monthly resolution digest**: what came due, what was scored, who moved a goalpost, what went silent. Forcing a weekly rhythm means padding with attention events — which is the engagement-farming the founder has already ruled out, arriving through the back door dressed as product-market fit. A tool you open when something resolves, or when you're about to be sold something, is a *good tool*. Retention should be framed as **returns per resolution event**, not weekly actives.

**2. Don't confuse the heartbeat with the moat.** These are different layers and the founder should stop hoping one asset does both jobs:

- **Indicators are the heartbeat.** 28 dials with predictor-attributed thresholds already exist across two narratives (`btc-bear-floor`: $57.5K, $63K, $53-60K, $49-53K, $40K, $35K — six named tripwires from five named people). These cross weekly. They generate genuine return visits. **But they are exactly the cron-job-collectable data the Aug 2026 moat verdict killed** — price levels are free and everyone has them.
- **The prediction ledger is the moat.** Time-in-market, pre-registered specs, goalpost-move history. It generates return visits *rarely*.

The synthesis is that the indicator layer is worth building for cadence while being honest that it's undefended, and its defensibility comes entirely from the *attribution* — "$57,778, because FibSwanny said so on camera on this date" is not a price level, it's a pre-registered commitment. That framing is not copyable from a data feed; it's copyable only from the corpus. **Attribution is what converts a commodity dial into ledger evidence** — and it means the sharpest weekly event isn't "BTC hit $57.5K", it's "BTC hit the level FibSwanny pre-registered, and here is what he said would follow."

**3. The cold-start problem is solved by vagueness, not by waiting.** The accountability layer's brutal weakness is that it needs years. The vagueness rate (§1.5) needs *zero* days and is available at n=1: **Dalio, 50% of claims unbounded, 0 of 12 hard-dated, versus a 13-predictor crypto ledger at 7% unbounded and 2 hard-dated to the day.** That is a real, defensible, publishable finding produceable this afternoon from data already on disk. It should be the accountability layer's launch asset while the clocks accumulate underneath.

### The risk nobody has priced

**The scoring obligation scales linearly with the ledger and is paid in the operator's own hours.** At ~90 entries that's ~2 resolutions/month plus vagueness triage — comfortable. At 50 narratives it's ~12/month plus triage plus dispute handling: a genuine part-time job, and the binding constraint on scale, *more than collection is*.

Which is the honest and rather elegant conclusion: the moat and the bottleneck are the same object. The resolved ledger is defensible **because** it costs accumulated human judgement rather than a cron job — which is precisely the "privileged position" test the Aug 2026 data-moat verdict said was the only thing left standing. Narrative Radar's privileged position isn't the data; it's being the party that has been consistently scoring, on a published standard, since 2026-07-30. **That asset is destroyed the first time the ledger is allowed to rot** — which is why §3.5 (visible hygiene, `OVERDUE` never rendering as `PENDING`, stale ledgers suppressing their own scorecard) is not polish. It is the product.

---

## Build order

1. **Scheduled sweep workflow** — nothing else in the monitoring loop is valid without a heartbeat. `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/.github/workflows/` currently has only `pages.yml`.
2. **Fix `resolved = total − pending`** at `index.html:756` — one line, unblocks the score gate on the only narrative with resolved history.
3. **Rewrite `parseHorizonDate`** (`index.html:722`) per §1.4 — latest-edge rule, exact days, `date_made`-relative durations, never-null. Recovers 11 lost clocks and removes the false-lapse/hidden-lapse pair.
4. **`clocks[]` per prediction + `state` split (PENDING/DUE/OVERDUE/VOID)** — makes operator debt visible.
5. **`resolution_spec` required at entry; backfill the 14 crypto PENDINGs before Oct 2026** — the October convergence point is the demo, and it's only worth anything if the specs predate it. This has a real deadline.
6. **Vagueness rate on the scorecard** — ships today, no waiting.
7. **`changelog.json` + `sweep_log.json` + follows-with-timestamps** — the quiet diff.
8. **Convergence points on the calendar; monthly digest.** Notifications last, if at all.
