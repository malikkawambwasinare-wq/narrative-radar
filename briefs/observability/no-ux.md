## LENS 6 — UX ARCHITECTURE

I read the shipped `index.html` (2,590 lines) and every JSON in `corpus/`. Three measurements govern every recommendation below, and all three cut against the proposal as written.

**Measurement 1 — there is no time series anywhere in this product.** `views` is a display string (`"16,760 views"`) captured once, at `first_seen`. `age_days` is the video's age *at capture*. Nothing is ever re-sampled: no cron, no history file, and `.github/workflows` is deploy-only. Every video in a narrative shares one `first_seen` date (collapse-audit: 33 videos on 2026-08-06; crypto: 25 on 2026-08-07). **Δ-anything is not computable.** Not heat, not velocity, not breadth-over-time.

**Measurement 2 — corpus size measures Malik, not the narrative.** Six narratives were seeded with an identical 6-query template. They returned 38, 32, 6, 6, 3, and 1 videos. The variance is sweep execution, not narrative size. Any ranked list keyed on volume ranks the founder's browsing history.

**Measurement 3 — the radar has two narratives and five placeholders.** Only collapse-audit and crypto-winter-watch have mutations (6 each), indicators (14 each), ledgers (12/14), and meaningful corpora. The other four have `"predictor": "to be determined"`, zero mutations, 1–6 videos, and a single claim with zero sources. A gallery that renders 7 equal tiles is the product's first lie.

---

### The structural verdict on the three-layer model

**ATTENTION / STRUCTURE / ACCOUNTABILITY is ordered exactly backwards.** Attention is the layer with (a) no data in this repo, (b) no moat — it is precisely the cron-collectable public data the Aug 2026 kill verdict rejected across nine domains, and (c) a permanent contamination problem, because retrieval is query-shaped. Accountability is the layer that holds the named moat: time-in-market, the UPDATED counter, legal-risk arbitrage.

If the UI leads with attention, the product spends its scarce first screen on its weakest, most copyable, most contaminated layer — and re-enters the category the founder already killed. **Invert the stack: ACCOUNTABILITY → STRUCTURE → ATTENTION-as-footnote.**

---

## 1. HOME AS NARRATIVE MARKET

### Triage of the six proposed lists

| List | Verdict | Why |
|---|---|---|
| **Heating fastest** | **Dishonest — cannot ship** | Requires Δviews/Δt. One snapshot exists per video, taken the day the narrative was created. The only available proxy (`views ÷ age_days` at capture) is a lifetime average, and comparing across narratives compares capture dates. |
| **Most contested** | **Contaminated at source** | Contestation is measured on a corpus retrieved by doom-shaped queries — `"dollar collapse prediction"`, `"housing market crash 2026"`, `"is the housing bubble about to pop"`. You cannot measure disagreement with a search string that only returns one camp. The proof is already in the data: **zero `counters` edges exist anywhere on the radar.** That is not a finding about the world; it is query design surfacing as a metric. |
| **Recently emerged** | **Vanity — actively brand-damaging** | `started` is the date Malik pasted a link. Labelling it "emerged" makes the product assert a fact about the world that it derived from its own operator. It violates "never assert truth, only structure." |
| **Most recycled** | **Honest, narrow** | Computable on 2 of 7 (`win` needs ≥10 dated videos; housing/psi/ai-race/2026-setup all fail). Verdicts are model-assigned, so this is a claim about the model as much as the corpus. Keep as a per-narrative badge, kill as a ranked list. |
| **Most mutated** | **Honest, and the right long-run metric** | `mutations[]` is hand-curated, immune to retrieval bias, and is one of the two named moats. Today it is a two-row list (6 and 6; every other narrative is 0). Ship the metric, not the leaderboard. |
| **Nearest clocks** | **The one to lead with — but currently broken** | See the parser bug below. Once fixed, this is the only list that is simultaneously honest, differentiated, uncopyable, and legible in three seconds. |

### The parser bug that blocks the best list

`parseHorizonDate` regexes prose at render time and grabs the *first* `20\d{2}`, defaulting to July 1 when no month is present. On collapse-audit it parses **3 of 12** horizons, and it converts `"by ~2026-2028"` into **2026-07-01** — six weeks in the past. The headline number can therefore render "due now" for a claim whose window runs to 2028, while the stored prose in `explanations.intermediate` correctly says *"the first cleanly countable clock expires Sept 2028."* That is the prose/array drift, with a specific cause.

**Fix:** resolve horizons at write time into a stored `horizon_date` + `horizon_window: [start, end]` + `precision: exact|month|year|range|vague`. Never regex prose in the render path. Nine of twelve collapse horizons are `"unstated (vague)"` or `"~1-2 years"` — those must render as *"no clock"*, which is itself the audit finding.

### Is "browse the environment" a gain or a loss?

**It is a loss, and the framing is a false binary.** Paste-a-link is an *answer* contract: the user brings a video, the product returns orientation. Its success metric is time-to-orientation. A market view swaps that for a *browse* contract, whose native metric is dwell time — the exact metric the founder banned. It also invites the comparison the data cannot survive: seven tiles side by side, five of them empty, sorted by numbers that measure sweep effort.

But the answer is not "keep the search box alone." The honest third option is that home is neither a market nor a search box — it is a **front page of the record**. Not "what is hot" (attention, no moat, no data). Not "what did you bring" (a tool, no reason to return). But *"what is coming due, and what has already been settled"* — which is the only thing on this radar that (a) changes without Malik touching it, because calendars move on their own, and (b) a funded competitor cannot backfill.

### Recommended home: **The Clock Board**

```
NARRATIVE RADAR
The algorithm pulls you deeper. This is the exit.

  [ Paste a video or article link → ]        ← kept, full width, still the primary verb

── DUE SOON ────────────────────────────────────────
  13d   Clarity Act reaches a Senate floor vote      Matt Hougan · Crypto Winter Watch
  77d   Bear bottom lands ~late Oct 2026             Cory Klippsten · Crypto Winter Watch
 138d   Midterm-conflict claim                       Ray Dalio · The 80-Year Collapse
                                        [ all 15 dated claims → ]

── ALREADY SETTLED ─────────────────────────────────
  7 of 12 Dalio calls have reached their horizon.
  0 landed cleanly · 2 refuted · 2 deadlines moved · 3 hit late by another cause
                                        [ open the ledger → ]

── ON RECORD BUT UNDATED ───────────────────────────
  11 claims carry no clock. Nothing here can ever be scored.  [ why this matters → ]

── THE FIELD ───────────────────────────────────────
  2 narratives fully audited · 4 opened, not yet swept
  [ 2 audited tiles, full metrics ]
  [ 4 stub tiles, visibly greyed, labelled "opened — not yet audited" ]
```

**Prioritises:** dated claims nearest resolution; adjudicated outcomes; the undated-claim count as a first-class finding rather than a gap.

**Omits, deliberately:** every volume number, every heat/velocity metric, "recently emerged," any cross-narrative ranking, and any sort order that implies one narrative is bigger than another.

Two moves earn their place. **"On record but undated"** turns the largest hole in the data (9 of 12 collapse horizons unparseable) into the product's sharpest argument — *these people mostly do not make falsifiable claims* — which is the origin story rendered as a metric. And **the stub tiles must look unfinished**: greyed, no numbers, labelled honestly. A radar that shows its own coverage gaps is making a credibility deposit it will need later.

---

## 2. NARRATIVE PAGE

### The five questions vs. the shipped hierarchy

The founder's five (how active / how changing / how structured / what connected to / what happens next) are **a taxonomy of metrics**. The shipped ANSWER → CONTEXT → TEST → EVIDENCE is **a reading order**. They are not competing — but the five questions are strictly worse as a page spine, for three reasons:

1. **"How active" has no data** (Measurement 1). Leading with it means opening every page on the weakest number.
2. **They are the analyst's questions, not the user's.** Year-one Malik does not ask "how structured is this." He asks "is this person right, and is anyone checking."
3. **They lose the answer.** The shipped page opens with the *question* the narrative competes to answer ("Is a US market crash imminent?") and names the narrative as one *answer under review*. That single framing is the product's best idea — it converts a video into a position in a field — and no ordering by metric type preserves it.

**Verdict: the shipped hierarchy is strictly better. Keep it. Fold the five questions in as the grouping labels inside CONTEXT, which is roughly what `dashboardHtml` already does with its three `grp-k` headers.**

### Recommended hierarchy and exact diffs from what ships

Keep ANSWER → CONTEXT → TEST → EVIDENCE. Six changes:

**(a) Promote TEST above CONTEXT.** Shipped order in `renderNarrativeCard` is `orientation → explain → dashboard → answers → whatChanged → claims → whatTestsIt → deepAnalytics`. "What would test it" sits seventh — below the fold, after the metric grid and the claims list. It is the accountability layer, and it is buried under structure and attention. **New order: `orientation → whatTestsIt → dashboard → answers → whatChanged → claims → deepAnalytics`.**

**(b) Fix `computeReceipt`, then split the counter in two.** `resolved: sup + ref` yields 2 for collapse-audit, below `SCORE_GATE = 5`, so the gate never opens. But 7 of 12 entries have reached their horizon (2 REFUTED + 2 UPDATED + 3 AMBIGUOUS). Do not simply widen `resolved` — AMBIGUOUS in a score denominator is a category error. Report two numbers:
- `adjudicated = sup + ref + upd + amb` (7 of 12 — gate-eligible)
- `cleanlyScored = sup + ref` (0 of 2 landed)

The headline becomes *"7 of 12 calls have reached their horizon; 0 landed cleanly, 2 deadlines moved, 3 arrived by another cause."* That is more damning, more accurate, and more defensible than the current suppression — and it survives a lawyer, because every clause cites a stored status.

**(c) Make "no clock" a headline number.** Add `11 undated` beside the resolved counts. Nine of twelve collapse horizons are vague; two of fourteen crypto horizons are. That contrast between predictors *is* the analysis.

**(d) Demote the reheat percentage out of the five headline numbers.** `reheatShare` is `null` on 5 of 7 narratives (needs ≥10 dated videos) and is model-assigned where it exists. Move it into `deepAnalytics`.

**(e) Promote `indicatorsHtml` out of `deepAnalytics`.** The 14 dials per narrative, each with thresholds, named predictors, and `contested_note`, are the densest and most original artifact in the repo — a canonical extraction from 31 and 18 transcripts respectively. They are currently collapsed inside the deepest disclosure, below the corpus composition chart. **They belong directly under `whatTestsIt`,** because that is what they are: the dials the narrative argues through.

**(f) Gate the Radar Read on data sufficiency.** `buildRadarRead` produces confident prose for every narrative, including psi-declassified (6 videos, 0 mutations, 0 predictions), where it will emit *"Established narrative"* on the strength of a `born` field alone. Add a guard: below (say) 10 reviewed videos or 0 ledger entries, print *"Not enough audited material to characterise this narrative yet"* instead.

---

## 3. HEATMAPS

| Proposal | Insight over a list? | Data sufficient? | Survives scrutiny? |
|---|---|---|---|
| Narrative-level metric grid | **No.** 7 rows × ~6 columns is a table with a colour ramp. Colour on 7 rows adds nothing a sort cannot. | n/a | Would fail — it puts stub narratives next to audited ones on equal visual footing. **Reject.** |
| **Source × narrative** | Yes in principle — shared distribution is genuinely novel. | **No. Measured: 68 distinct channels; exactly ONE appears in more than one narrative** (`Econofin`, collapse-audit × housing-crash-watch). The grid is 68×7 with a single off-diagonal cell. | **Reject at this scale.** Revisit at ~20 narratives *within one industry*. Cross-industry overlap will always be near-zero and is not a finding. |
| **Narrative × claim** | Yes in principle — shared assumptions across nominally different narratives is the strongest idea in the proposal. | **No, as specified.** Claim IDs are narrative-local (`imminent-debt-crisis`, `bottom-late-2026`, `four-year-cycle`) with no shared vocabulary and no `fingerprints[]` key present in any `claims.json`. There is nothing to join on. | **Reject as specified — but see below.** |
| Narrative × time | No. | **Impossible** (Measurement 1). | **Reject.** |
| Clock heatmap | Marginally — clustering of expiry dates is real. | 15 parseable dated claims across 2 narratives, 12 of them from one month's sweep. | **Reject as a heatmap; ship as the Clock Board list.** A timeline of 15 items is a list. |

### The one to build: **Indicator × Narrative**

The founder attributed the analytical novelty to the wrong join key. Claims do not share vocabulary. **Indicators do.** `indicators.json` already carries a `category` enum, and the two mapped narratives overlap on four of them: `market_structure`, `credit`, `valuation`, `other`. More concretely, the same underlying dials appear in both corpora under different names — `long-rates-and-fed-path` (collapse) and `global-liquidity-qt` (crypto); `japan-yen-jgb-carry-trade` (collapse) against the crypto clock that `relations.json` already links via `shares_clock` on *"10yr Treasury yield sustained above 5%."*

That yields the exact insight the founder wanted from source × narrative — *two supposedly unrelated stories are running on one dial* — and unlike channel overlap it is **non-trivial at n=2**. A crash narrative and a crypto-bottom narrative resolving on the same rate trigger is a finding on the first day; a channel appearing in two corpora is not a finding until you have dozens.

**Build:** a compact matrix, indicator categories down, narratives across, cells carrying the count of dials plus their role colour (`trigger` / `countdown` / `evidence` / `counter-evidence` — the colour ramp already exists in `IND_ROLE`). Click a cell to open the dials. Gate it to narratives with ≥5 extracted indicators, so it renders as a 2-column matrix today and grows honestly.

**Ship at most one more, later:** the clock heatmap, but only after `horizon_date` is stored at write time and only once ≥40 dated claims exist across ≥5 narratives.

---

## 4. TOPOLOGY

**No. Do not make the 360 map dynamic or temporal. Not at this scale, and not next.**

The evidence against is in the data: 1 of 7 narratives has a `relations.json`; 4 of its 7 edges carry `"videoIds": []` and therefore fail the project's own ≥3 videos / ≥2 channels evidence gate; 5 of 7 targets are `shadow` — untracked, unaudited, model-asserted; and `counters` has zero instances radar-wide. A temporal layer would animate a graph in which **the majority of edges do not meet the standard for existing**, and motion reads as confidence. It would be the single largest integrity liability the product could ship.

There is also no time axis to animate (Measurement 1). "Temporal topology" would mean interpolating between `updated: "2026-08-13"` and nothing.

**Do instead, in this order:**
1. **Fill the empty edges or delete them.** Four uncited edges either earn corpus citations or come out. An honest three-edge map beats a seven-edge map with four assertions.
2. **Find one real `counters` edge.** Run a deliberately inverted query set (`"why the housing crash isn't coming"`, `"debt doomers are wrong"`) against an existing narrative. This does double duty: it produces the missing edge type *and* it is the direct fix for the contestation contamination in §1. If inverted queries surface a counter-camp that the original queries missed, that is measurable proof the corpus was query-shaped — the most valuable diagnostic available right now.
3. **Only then** consider making the map dynamic — and even then, prefer *interactive* (click a node to re-centre) over *temporal*.

---

## BUILD ORDER

1. Store `horizon_date` / `horizon_window` / `precision` at write time; delete prose regexing from the render path. *(Unblocks everything in §1 and §2.)*
2. Split `computeReceipt` into `adjudicated` vs `cleanlyScored`; add the undated-claims count; gate `buildRadarRead` on data sufficiency.
3. Reorder the narrative page: TEST above CONTEXT; indicators out of `deepAnalytics`; reheat share into it.
4. Ship the Clock Board home, with visibly greyed stub tiles.
5. Fill or delete the four uncited relation edges; run one inverted query set to hunt a `counters` edge.
6. Build Indicator × Narrative, gated at ≥5 indicators per narrative.

## THE UNCOMFORTABLE FINDING

The deep prediction ledger — the asset the portable-thesis research named as the primary moat, on the "time in market" argument — **was not accumulated. It was retro-researched.** All twelve collapse-audit entries spanning 2015–2026 cite a single secondary source: `awealthofcommonsense.com/2025/03/predicting-a-financial-crisis/`. The crypto ledger, which *was* built from the corpus, has fourteen entries all dated `2026-08` and all `PENDING` — zero time depth.

The moat argument was: *a competitor with $50M starts at n=0 and needs 18 months before one call resolves.* But collapse-audit demonstrates the counter-example inside this very repo — a well-funded team can reconstruct eleven years of ledger from public secondary sources in an afternoon, exactly as this project did. **What is not reconstructible is the UPDATED status**, which requires having recorded the earlier version before it was restated, and **the mutation history**, which required watching. Those two fields are the real moat; the ledger's raw depth is not.

**UX consequence:** the home page and the narrative page should give `UPDATED` (deadline moves) and `mutations[]` more visual weight than the raw resolved score. The Clock Board's "2 deadlines moved" line is doing more defensive work than "0 of 2 landed" — and the shipped page currently renders deadline moves as a small `warn`-class chip in the headline row. Promote it.
