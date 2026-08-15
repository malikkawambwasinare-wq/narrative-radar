_Grounded in the live repo at `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar` — schemas read from `corpus/*/`, gates read from `index.html`, typology read from `briefs/360-research/SYNTHESIS.md`. Every availability claim below was verified against shipped data, not assumed._

---

# Lens 4 — The Strongest Objection Engine

## 0. BLUF

**Keep the mandate, reject the framing.** "The strongest case against my view" must be mandatory — but the founder's brief specifies it as a property *of the narrative*, and it has to be a property *of the user's stated position and reasons*. That single change reorders everything downstream, including which of his eight sources is "strongest."

Three verdicts up front:

1. **The counter must be selected against the user's load-bearing REASON, not against the narrative.** A devastating objection to a reason the user never relied on is theatre. This is the biggest defect in the proposed design.
2. **The eight sources are not one list — they are two classes doing different jobs.** Four offer a rival position you could hold instead (*substitutive*); four only widen your error bars (*corrosive*). Filling the COUNTERWEIGHT slot with a corrosive counter and calling it "the case against" is a category error that inflates confidence.
3. **Most of the eight are not buildable today.** Verified: `counters` edges = **0 instances** across the entire corpus; `relations.json` exists for **1 of 6** narratives; the prediction-score gate (`n>=5` resolved) is **BLOCKED on every narrative that exists**. Ship (b) and (c) first — they are fully built and nobody has noticed.

And one finding that outranks the rest: **the strongest objections are already sitting in the private transcripts, pre-steelmanned by the narrative's own believers.** I verified this. More in §7.2.

---

## 1. The framing error to fix first

The brief asks: *derive the strongest case against **the narrative**.* But a session ends with a user holding a POSITION with 2–3 REASONS. Those are different objects:

- The user may hold a **weaker version** of the narrative ("a correction is likely" vs the corpus's "1929-scale collapse"). Most corpus counters miss it entirely.
- The user may hold the **right conclusion for a reason the corpus doesn't use**, so the corpus's counters don't touch their warrant.
- The user may **oppose** the narrative (§10).

**The engine's input is `(position, reasons[])`, not `topic_id`.** Selection runs in two steps:

1. **Locate** — map the user's position into the corpus's camp structure (`claims.json` contested camps). Three outcomes: *matches a camp* → that camp's opponents are the counter pool; *matches no camp* → say so ("nothing in this corpus argues what you're arguing") — that is information, not an error; *matches the consensus claim* → §10 logic.
2. **Target the load-bearing reason** — the reason whose removal collapses the position. Heuristic, computable without a model call: the reason that (i) appears in the fewest of the user's other reasons as a premise, and (ii) carries the largest share of the position's specificity (dates, magnitudes, mechanisms). Ask the user to rank if ambiguous — one tap, cheaper than guessing.

> **Design rule:** the objection must attack a REASON the user actually gave, and the UI must show which one it is hitting. "This objection targets your reason #2" is the anti-theatre device.

---

## 2. Data audit — what is derivable today

Verified against shipped files. This is the part that determines the build order.

| # | Counter type | Derives from | Status **today** |
|---|---|---|---|
| (b) | Opposing contested-claim camp | `claims.json` → `claims[].camps[].sources[]` (position + videoId + predictor) | ✅ **Fully built.** Camps carry named predictors and per-camp source counts. |
| (c) | Indicator cutting the other way | `indicators.json` → `contested_note`, `role: "counter-evidence"`, `thresholds[].predictor` | ✅ **Fully built and badly underused.** 14 dials on collapse-audit, each with named opposing readers. |
| (h) | Selection-effect critique | `videos.json` verdicts + `computeReceipt` channel concentration (`spread.pct`), `originalShare`, `reheatShare` | ✅ **Computable now**, zero model cost. |
| (a) | Strongest competing narrative | `relations.json` → `competes` / `competes_mechanism` | ⚠️ **1 of 6 narratives.** Only `collapse-audit` has `relations.json`. |
| (e) | Narrative's own track record | `predictions.json` statuses | ⛔ **Gated off everywhere.** See below. |
| (g) | `counters` / anti-narrative edge | `relations.json` type `counters` | ⛔ **Zero instances shipped.** Type exists in typology only. |
| (d) | Institutional / mainstream consensus | — | ⛔ **No store exists.** Needs the 360-health "institutional verdict" field generalised. |
| (f) | Historical base rate / counterexample | — | ⛔ **No store exists.** Outside-corpus by nature. |

### 2.1 The gate bug worth fixing before anything else

`index.html:757` computes `resolved: sup + ref` — **`UPDATED` and `AMBIGUOUS` are excluded**. Measured:

```
collapse-audit      resolved = 2  (n>=5 gate: BLOCKED)   excluded: UPDATED 2, AMBIGUOUS 3
crypto-winter-watch resolved = 0  (n>=5 gate: BLOCKED)   excluded: UPDATED 0, AMBIGUOUS 0
```

So counter type (e) is unavailable on **every narrative in the product**, and the exclusion is backwards for this purpose. `UPDATED` — the goalpost move — is the *most* damning accountability fact the ledger holds, and it is precisely what the audit exists to surface ("the horizon rolls, ~2yrs out, repeatedly since 2015"). It is currently invisible to the gate.

**Recommendation:** keep `n>=5` for any *accuracy score* (a rate needs a denominator), but add an ungated **clock-integrity statistic** — `UPDATED count`, `median horizon slip`, `years since first claim without resolution`. These are counts, not rates; they need no `n>=5` gate because they make no frequency claim. This unlocks (e) immediately on collapse-audit with the strongest material it has.

### 2.2 Build order this implies

**v1 = (b) + (c) + (h).** All three are shipped data, no new store, no model call for retrieval. (c) in particular is the single best-matched asset in the product to this feature and it currently renders as a passive list.
**v1.5 = (e)** after the clock-integrity fix.
**v2 = (a) + (g)** — requires `relations.json` backfill on 5 narratives (~$0.50 total per the existing map360 costing) and the first `counters` edges ever minted.
**v3 = (d) + (f)** — new external-evidence store, hardest integrity surface.

---

## 3. Taxonomy — two classes, eight types

The class split is the load-bearing distinction and it is missing from the brief.

### Class I — Substitutive (offer a rival position you could hold instead)
**(a)** competing narrative · **(b)** opposing camp · **(d)** institutional consensus · **(g)** anti-narrative

These answer *"what should I believe instead?"* They are the only counters that make a thesis portable, because in a real meeting the objection you face is a rival claim, not an epistemics lecture.

### Class II — Corrosive (degrade the warrant; offer no alternative)
**(c)** contrary indicator · **(e)** track record · **(f)** base rate · **(h)** selection effect

These answer *"why should I trust this less?"* They cannot be the whole answer. A position defeated only by corrosive counters resolves to **"I don't know, and here's why"** — which is a legitimate and valuable portable thesis, and the product should be willing to output it.

> **Hard rule:** the COUNTERWEIGHT slot requires **at least one Class I** counter, or an explicit statement that none was found (§9). A Class II counter never fills the slot alone. This prevents the most likely failure mode — the engine serving a confident-sounding "well, the corpus is concentrated" and the user reading it as "no real opposition exists."

### 3.1 Per-type notes that change how each must be phrased

- **(e) attacks the speaker, not the claim.** Genetic fallacy risk is real: five failed calls do not disprove the sixth. Must be phrased as calibration, never disproof: *"the same clock has moved twice since 2015 — weight the date, not the direction."* This also keeps it inside the existing never-assert-truth rule.
- **(h) is not a counterargument at all.** It is a confidence haircut on the *product's own evidence base*. Given the founder's story — six years inside a corpus with no counters — it should be **always-on and non-dismissible**, but rendered in its own slot, never as "the case against."
- **(g) is the highest-value missing type.** SYNTHESIS.md is right that without `counters` "the map only ever shows believers." Zero instances shipped means the map currently *does* only show believers. `candidates.json` already embeds `counter:` hints inside ~8 `claim_hint` strings — a latent anti-narrative inventory available for near-free extraction.
- **(c) has a hidden superpower.** A contrary indicator with a threshold and a date is simultaneously the objection *and* the UPDATE CONDITION. See §4.4.

---

## 4. The strength model

"Strongest" needs to be computed, not asserted. Four factors, multiplicative — any zero kills the candidate.

```
strength = bite(counter_type × position_type)   // does it hit the load-bearing reason?
         × warrant(source quality)              // would a reasonable person credit it?
         × independence(echo distance)          // is it from outside the same choir?
         × liveness(resolvability)              // does it come with a clock?
```

### 4.1 `bite` — §5 matrix.

### 4.2 `warrant` — quality, explicitly NOT quantity
Reuse signals already stored: video `verdict` (`ORIGINAL` > `DERIVATIVE` >> `RECYCLED`/`CLICKBAIT`), named `predictor` present, falsifiable phrasing (a number or a date), primary-source status. **`RECYCLED`/`CLICKBAIT` sources are ineligible to carry the strongest objection at any source count** — reusing the verdict field the product already trusts.

### 4.3 `independence` — the echo-distance term
A counter voiced from inside the same channel cluster as the position is weak evidence of genuine opposition. Compute from the channel-concentration data `computeReceipt` already produces. Counters from channels outside the top-3 cluster score higher. This is cheap and no competitor has it.

### 4.4 `liveness` — prefer objections that resolve
An objection with a dated, measurable trigger beats a timeless one, because it converts directly into the portable thesis's UPDATE CONDITION field. **The strongest objection and the update condition should be the same object wherever possible.** `indicators.json` thresholds are exactly this shape (`"10yr Treasury yield sustained above 5%"`, `next_check: "2026-12"`), and `relations.json` already carries `shares_clock` edges with `clock.trigger` / `clock.next_check`. This unification is the most elegant integration available between Lens 4 and the rest of the Portable Thesis, and it comes free from shipped fields.

### 4.5 Confidence ceilings — mechanically enforced
The CONFIDENCE field must not be user-chosen free-hand. The objection sets a ceiling:

| Strongest objection found | Max confidence permitted |
|---|---|
| Class I, `ORIGINAL` source, independent cluster, unresolved clock | **Moderate** — a live, well-sourced rival exists |
| Class I, but resolved in the user's favour on a dated clock | **High** |
| Class II only | **Low–Moderate**, flagged "no rival position located" |
| None found, corpus echo index high | **Low** — and say why (§9) |

This is what stops the feature from becoming a confidence-laundering machine: adding a steelman that the user then dismisses feels like due diligence and reliably *raises* stated confidence. The ceiling prevents that.

---

## 5. Situational ranking matrix

Strength is conditional on the **shape of the user's position**. There is no fixed ranking, and any implementation that hardcodes one will be wrong most of the time.

| Position shape | Example | **Strongest** | Also strong | Weak / misleading here |
|---|---|---|---|---|
| **1. Dated prediction** | "Crash before Dec 2026" | **(e) track record** — the ledger's goalpost history is decisive against a date | (f) base rate, (c) contrary dial | (d) — institutions rarely make dated calls |
| **2. Mechanism / causal** | "AI capex debt triggers it" | **(b) opposing camp** — `crisis-trigger` is literally a contested mechanism claim with three camps | (g) anti-narrative, (a) competes_mechanism | (e) — a bad forecaster can still name the right mechanism |
| **3. Magnitude / valuation** | "Equities 40% overvalued" | **(c) contrary indicator** — same dial, opposite read, named | (d) institutional, (f) base rate | (g) — anti-narratives argue kind, not degree |
| **4. Evaluative / action** | "Move to hard assets" | **(d) institutional consensus** + **(h)** on the seller-incentive corpus | (a) rival answer | (f) — base rates don't settle what you should do |
| **5. Descriptive / discourse** | "Everyone credible now says X" | **(h) selection effect** — here it is a *direct refutation*, not a haircut | (a) rival answers exist | (e), (f) — irrelevant to a claim about discourse |

Read `crisis-trigger` in `corpus/collapse-audit/claims.json` as the worked case: a shape-2 position, three camps (AI capex debt / credit-market seizure / Japan yen-carry unwind), each with named predictors and videoIds. Type (b) is available, sourced, and attributable **today**, with no new data.

### 5.1 The second slot the brief is missing

Epistemic strength and social likelihood are different. In a work meeting, the objection you actually get hit with is **(d) mainstream consensus** — because your colleagues will cite the mainstream — even when the epistemically strongest objection is a contested dial.

Since the stated goal is a thesis portable **to another human**, ship **two slots**:

- **"The strongest case against"** — epistemic, ranked by §4.
- **"What you'll actually be hit with"** — social, ranked by prevalence + audience default.

They frequently differ, and the difference is itself the insight: *the objection most likely to be raised is rarely the one most likely to be right.* That line is the feature's soul, and it is the founder's own $20k story stated in the abstract.

---

## 6. Anti-strawman discipline

### 6.1 The three receipts — no objection ships without all three
1. **A named human.** Never "critics argue." `claims.json` camps and `indicators.json` thresholds already carry `predictor`.
2. **A verbatim quote with a timestamp.** Transcripts are `[mm:ss]`-stamped, so every quote maps to `youtube.com/watch?v=<id>&t=<seconds>`. The objection is one click from the human saying it, in context.
3. **A source count with its verdict mix** — shown as provenance, explicitly **not** as strength (§8).

### 6.2 Concession mining — the highest-quality steelman source available, and it already exists

**Verified in the live corpus.** Reflowing transcripts (stripping `[mm:ss]`, collapsing whitespace) and scanning for concessive markers returns 15 hits in collapse-audit alone. The best of them, from `OxE2WncCBd4`:

> "…every single one of my positive arguments has a very valid counter argument. And in terms of what the critics are saying and why the S&P 500 could fall even more than Korea, we need to talk about the bear case."

That is a believer inside the corpus **pre-building the steelman against himself**, on the record, with a timestamp. It is strawman-proof by construction: nobody can claim the objection was weakened by a hostile paraphrase when the narrative's own advocate framed it.

**Ranking consequence: an objection conceded by a believer outranks an objection asserted by an opponent** — it clears independence and warrant simultaneously.

Implementation notes, all verified:
- Regex on raw transcripts **fails** — files are wrapped into short lines, so matches spanning line breaks are missed. Reflow first.
- Density is ~1 hit/transcript and **clustered** in a few videos. So: regex as a cheap pre-filter to pick which transcripts get a model call, then an LLM extraction pass — the same extract → synthesise → adversarial-verify pattern already proven on `indicators.json` (49 transcripts, 7-agent fleet, 2 corrections caught).
- Map the match offset back to the nearest preceding `[mm:ss]` for the deep link.
- Quotes that match *"what would change my mind"* / *"if I'm wrong it'll be because"* are **dual-purpose**: objection AND update condition (§4.4). Extract them into both fields.

### 6.3 Quote-first construction
The dominant LLM failure here is writing a generic objection and then hunting for support, which reliably produces a weaker, blurrier version than any real source holds. Invert it: **retrieve the quote, then write around it.** The generated prose must be *entailed by* the quoted text.

**Verification gate:** *"Would the person quoted endorse this as a fair statement of their argument?"* Run it as an adversarial check pass — the pattern that already caught 2 fabrication/misattribution errors in the indicator build. Any objection whose claim exceeds its quote gets cut back to the quote.

### 6.4 Transcript-publication policy — resolve before shipping
`.gitignore` excludes `corpus/*/transcripts/` by explicit choice; only derived data goes public. Objections need *verbatim* quotes, which is a change in kind from `indicators.json` derived punchlines. Recommended policy: publish **short quotes only** (≤25 words), always attributed, always deep-linked to the source video at the timestamp, never enough to reconstruct a transcript. The deep link means the quote functions as a citation pointing at the creator's own monetised page — defensible, and consistent with the existing "the map is the receipt" stance. **Flag for Malik: this is a policy decision, not an implementation detail.**

---

## 7. Strongest ≠ most common

The product uses source counts as its quality signal nearly everywhere. **For objections, count is actively misleading** — it measures how loud a camp is, and the whole thesis of the product is that loudness is a function of the algorithm, not of truth. A four-video camp of same-day re-cuts is one argument wearing four hats.

The selection algorithm:

```
candidates = all counter-instances opposing the user's load-bearing reason
  |> reject: verdict in (RECYCLED, CLICKBAIT)
  |> reject: no named predictor
  |> reject: no verbatim quote retrievable
  |> require: >= 2 sources AND >= 2 distinct channels   # existence floor, per existing edge gate
  |> dedupe: collapse same-argument instances to ONE candidate,
             keeping the best-warranted instance      # kills the re-cut inflation
  |> score:  bite × warrant × independence × liveness  # count NOT a term
  |> boost:  believer-conceded (§6.2)
  |> return top 1, plus runner-up from a DIFFERENT counter class
```

Two details that matter:

- **Source count is a floor, not a slope.** Two independent channels to exist; beyond that, more sources add nothing to strength. This deliberately reuses the existing `≥3 videos / ≥2 channels` edge gate as the existence test while refusing to let it become a ranking signal.
- **Dedupe before scoring, not after.** Otherwise the most-recycled argument wins on volume — reproducing exactly the failure that cost the founder six years.

---

## 8. When the corpus contains no credible counter

**Yes — the product must say so, prominently, and it must LOWER confidence, not raise it.**

This is the single most important case in the whole lens, because it is the founder's own story stated as a data condition: he spent six years inside a corpus that contained no counter-argument, and read that silence as confirmation.

**Required phrasing shape:**

> **No credible case against was found in this corpus.**
> That is a fact about *this corpus*, not about the world — and it is a reason to trust this corpus **less**, not to trust your position more. 22 of 30 videos here trace to 3 channels; 7 are re-cuts of material already counted.

Three rules:

1. **Never fabricate a counter to fill the slot.** "Mandatory" means the *slot* is mandatory; an honest empty-with-explanation is a valid fill. A model-invented objection is a strawman by definition — it has no source, so it cannot survive §6.1.
2. **Distinguish "absent from this corpus" from "does not exist."** The product can only ever claim the former. This falls straight out of the never-assert-truth rule.
3. **Fire the echo index.** Computable now from `computeReceipt`: channel concentration (`spread.pct`), `originalShare`, `reheatShare`, plus camp balance (any contested claim where one camp holds >85% of sources). A high echo index with an empty counter slot is the product's **loudest possible warning** — and it is the exact 10-second signal year-one Malik needed. It should be visually the strongest state the objection card can render, not a greyed-out empty state.

Corollary: an empty counter slot should also trigger the shadow-founding growth loop — *"nothing here argues the other side. Found the anti-narrative →"* — turning the product's weakest epistemic moment into its acquisition mechanic. `candidates.json` already holds ~8 latent anti-narratives in its `counter:` hints.

---

## 9. When the user agrees with the mainstream and the counter is the fringe

Real and common — the crash-imminent corpus is fringe relative to institutional consensus, so a user who concludes "no imminent crash" is *agreeing with the mainstream* while sitting inside a doom corpus.

**Rules:**

1. **Steelman it honestly.** Give the fringe its best-sourced, best-warranted instance under the same §6 discipline. Suppressing it turns the product into a consensus-enforcer, which contradicts its reason for existing — sometimes the fringe is right, and the founder's own backtests were a fringe position against YouTube consensus.
2. **Never launder it.** Present the steelman and its receipt **in the same frame, at the same time** — never the argument now, the track record on click. For the crash corpus that means: strongest case, immediately followed by *2 refuted, 2 goalpost-moves since 2015, first countable clock Sept 2028*. This is the one place where a counter-counter is mandatory rather than optional.
3. **Use the ledger, not adjectives.** "Fringe" is never a verdict the product renders. The asymmetry is expressed only through stored structure: resolution history, mutation count, corpus quality, independence. Same never-assert-truth rule, applied symmetrically.
4. **Institutional consensus gets its own receipt too.** (d) must carry named bodies and dates, and where the mainstream has its *own* failed calls, that belongs in the record. Otherwise the product silently treats institutions as ground truth — and the existing 3-tier border (Established / Contested / Unsupported) plus the mandatory boring-baseline slot already provide the vocabulary to avoid it.
5. **Agreeing with the mainstream does not raise the confidence ceiling.** Consensus is a rival position, not a proof. §4.5 applies unchanged.

---

## 10. New integrity risks this lens creates

**These are risks the existing gates do not cover, because Lens 4 is a new kind of machine.**

### 10.1 A steelman generator pointed at red-line topics — the serious one
The existing health gates specify **red-line refusal topics** (cancer treatment, vaccine safety, med discontinuation). Lens 4 builds a machine whose entire purpose is **making the strongest possible case for a position** — which is precisely the machine you must never point at anti-vax or alt-cancer content. A user holding a mainstream health position (§10 logic) would trigger "the strongest case against" → and the engine would dutifully steelman the red-line fringe, with quotes, named advocates, and receipts.

**The red-line list must be checked BEFORE counter generation, not after.** On a red-line topic the objection slot renders the GP off-ramp and refuses to generate — no steelman, no "some argue." This is the highest-severity gap I found and it is not covered by any shipped gate.

### 10.2 Defamation surface, widened
The existing rule — category-level naming, observable phrasing, never conduct-verbs — was written for `supplements` edges. Objections quote **named individuals** and frequently do so adversarially ("X's last five calls failed"). Extend the rule explicitly: state **observable record only** (dated claim, stated horizon, what happened), never motive or competence. `predictions.json` already models this well — *"An audit trail is not mockery"* is the right register and should govern objection copy verbatim.

### 10.3 Quote-out-of-context
A 25-word adversarial quote is the easiest thing in the product to get wrong. The timestamp deep link is the mitigation — but the adversarial verify pass must include a specific context check: *does the surrounding 200 words reverse the meaning?* Add it to the existing fabrication/misattribution check.

### 10.4 Time-to-orientation vs the restatement exercise
Making the user restate the objection in their own words is pedagogically the strongest known steelman check — and it directly contradicts the success metric (time-to-orientation, never dwell time). **Do not make it default.** Offer it only in an explicit "I'm about to argue this" mode, where the user has opted into spending time. Protecting the metric matters more than the exercise.

---

## 11. Build spec

### 11.1 Storage
No new store for v1 — (b), (c), (h) read shipped files. Add per narrative:

`corpus/<topic>/objections.json`
```jsonc
{
  "note": "Steelmanned objections mined from this corpus. Every entry carries a named human, a verbatim quote, and a timestamped link. Nothing here is a Narrative Radar judgement.",
  "updated": "2026-08-15",
  "method": "concession pre-filter -> LLM extraction -> adversarial context/fabrication verify",
  "objections": [{
    "id": "bull-case-breadth",
    "class": "substitutive",           // substitutive | corrosive
    "type": "b",                       // a..h
    "targets_reason": "index-concentration",
    "position_shapes": [2, 3],         // which position shapes this bites
    "claim": "...",                    // must be ENTAILED by quote
    "quote": { "text": "...", "videoId": "OxE2WncCBd4", "t": 412,
               "predictor": "…", "verdict": "ORIGINAL" },
    "believer_conceded": true,         // §6.2 boost
    "sources": [{ "videoId": "…", "channel": "…", "predictor": "…" }],
    "independence": { "outside_top_cluster": true },
    "clock": { "trigger": "…", "next_check": "2026-12" },  // → update condition
    "counter_counter": { "kind": "ledger", "note": "2 refuted, 2 goalpost-moves since 2015" }
  }]
}
```

### 11.2 Pipeline
`netlify/functions/objections.mjs`, modelled on `map360.mjs` (mint + cache, `[skip netlify]` commit tag, sequential GitHub writes — the 409 race is documented and real). Cheap regex pre-filter selects transcripts; one Opus call per narrative for extraction + steelman + entailment check. Estimated **~$0.05–0.10 per narrative**, in line with map360. Backfill of 6 narratives ≈ **$0.50**.

Selection at render time is deterministic client-side scoring (§7) — no model call per user session. This keeps the marginal cost at ~$0, which puts the whole feature in the **free tier** under the existing pricing thesis. Worth noting: the highest-value new feature costs nothing per use.

### 11.3 UI
Follow the shipped disclosure pattern — summary-first, detail behind one click, explicit completion state.

```
THE STRONGEST CASE AGAINST YOUR REASON #2
"…every single one of my positive arguments has a very valid
 counter argument… we need to talk about the bear case."
   — <named>, <channel>, ORIGINAL ▸ watch at 6:52

Independent of your sources · conceded by a believer · resolves Dec 2026
→ This is also your update condition.

WHAT YOU'LL ACTUALLY BE HIT WITH (differs)   ▸
CONFIDENCE CEILING: Moderate — a live, well-sourced rival exists.
```

Plus the always-on, non-dismissible corpus-quality haircut (h), and — when empty — the §9 warning card as the loudest state in the component.

---

## 12. What I'm rejecting

| Proposed | Verdict |
|---|---|
| Counter derived from **the narrative** | **Reject.** Derive from `(position, reasons)`; target the load-bearing reason (§1). |
| Eight sources as one ranked list | **Reject.** Two classes; Class I required, Class II can never fill the slot alone (§3). |
| A single fixed "strongest" ranking | **Reject.** Strength is conditional on position shape (§5 matrix). |
| "Mandatory" = always produce an objection | **Reject as stated.** The *slot* is mandatory; fabrication is forbidden; empty is a valid, high-value fill (§9). |
| Source count as strength | **Reject.** Count is an existence floor. Recycling inflates it — the exact failure the product exists to catch (§7). |
| Symmetric both-sides presentation | **Reject.** False balance. Objections carry tier borders and receipts; asymmetry is expressed via stored structure only (§10). |
| Outside-corpus (model-knowledge) counters | **Conditional accept.** Needed for (d) and (f), since a 30-video corpus is often an echo chamber — but hard-bordered "not from this corpus," using the existing 3-tier Established/Contested/Unsupported treatment. |
| COUNTERWEIGHT as a single field | **Reject.** Split: epistemic strongest + what-you'll-face + confidence ceiling (§5.1, §4.5). |

---

## 13. Open decisions for Malik

1. **Verbatim-quote publication** (§6.4) — transcripts are private by your choice; objections need short attributed quotes. Policy call, blocks the build.
2. **The `resolved` definition** (§2.1) — fix `sup + ref` to unlock (e) via ungated clock-integrity stats? This also affects the receipt strip already live on Pages.
3. **Red-line pre-check** (§10.1) — confirm the objection engine hard-refuses on red-line health topics before generation. I'd treat this as blocking.
4. **First `counters` edges** — zero exist. Found 2–3 anti-narratives from the `counter:` hints already sitting in `candidates.json`?

### Key files
- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/collapse-audit/claims.json` — contested camps, type (b) source
- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/collapse-audit/indicators.json` — `contested_note` + `role: counter-evidence`, type (c) source
- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/collapse-audit/relations.json` — only `relations.json` in the product; no `counters` edge
- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/collapse-audit/predictions.json` — ledger; the "audit trail is not mockery" register
- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/index.html` — `computeReceipt` (l.729), `narrativeStats` (l.766), `buildRadarRead` (l.795)
- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/briefs/360-research/SYNTHESIS.md` — five hard gates this lens must not violate
- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/candidates.json` — 33 shadow candidates, ~8 with latent `counter:` hints