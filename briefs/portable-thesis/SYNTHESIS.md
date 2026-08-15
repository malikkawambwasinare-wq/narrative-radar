# Portable Thesis — research synthesis (14 Aug 2026)

Eight-lens investigation (framework archaeology · thinking-vs-presentation · confidence &
calibration · steelman engine · belief updating · adversarial critic · category & moat ·
worked examples on real repo data). Full reports in this directory.

## The verdict

**Build a narrower, inverted version. Do not build "help the user form a position."**

The critic's kill shot, which every other lens independently corroborated:

> Year-one Malik was not short of a thesis. He held a strong, articulate, well-reasoned,
> *borrowed* position on Smart Money Concepts for six years and $20,000. He could have
> filled in all seven fields beautifully in 2020 and every one would have been sincere,
> defensible in a Slack thread, and wrong. **Portable Thesis as specified is a machine for
> producing the exact mental object that cost him six years.** What saved him was not a
> better-structured belief — it was a *backtest*: an external record that scored a position
> he already held.

So invert it. Not *"help me form a view"* but **"take the view I already hold and put it on
the same clock the product puts Dalio on."** Working name: **Thesis Intake / Put it on the clock.**

## Why the original framing fails (four load-bearing findings)

1. **The corpus is a sample of ATTENTION, not of evidence.** Camp A having 14 videos and Camp B
   having 3 means Camp A monetises better on YouTube. Any position derived from corpus balance
   launders algorithmic attention into belief — the exact harm the product exists to reverse.
   Radar Read is safe *because* it only ever describes the media object.
2. **Machine-drafted positions are adopted, not edited.** Logg (algorithm appreciation), Skitka
   (automation bias), Jakesch CHI 2023 (co-writing with an opinionated model shifted users'
   own reported attitudes without their noticing), generation effect. If the system drafts
   POSITION or WHY, the user keeps it, sincerely reports it as their own, and defends it.
   Agency is theatre — worse than theatre, because ownership illusion hardens the belief.
3. **Pyramid Principle and BLUF are conviction-transfer technologies.** They maximise persuasive
   force per unit of evidence. The users' documented failure mode is *being persuaded by
   well-structured confident content*. ICT videos ARE Pyramid Principle — that is why they
   worked on him. Importing them is importing the pathogen as the treatment.
4. **The ordering is backwards.** Koriat/Lichtenstein/Fischhoff: generating reasons FOR a
   conclusion increases overconfidence. Lord/Lepper/Preston: "consider the opposite" works
   ONLY before commitment. WHY → COUNTERWEIGHT is the overconfident order; post-commitment
   steelman-then-rebut is McGuire inoculation — it manufactures armour, not humility.

## Field-by-field autopsy

| Field | Verdict |
|---|---|
| QUESTION | **Keep — strongest field.** Already the 360 spine; the durable object. |
| POSITION | Keep **only if human-typed**, and only with a clock attached. Never machine-authored. |
| WHY (2-3 reasons) | **Replace with MECHANISM** ("how would this actually work, step by step"). Reason-listing inflates confidence; mechanism-explanation deflates extremity (Fernbach et al. 2013). "2-3" is a rhetorical count that fabricates reasons the corpus doesn't support. |
| COUNTERWEIGHT | Keep, **move BEFORE position**, quote verbatim from corpus, **forbid a rebuttal field**. |
| CONFIDENCE | **Kill the number.** A statistic about videos wearing a forecast's clothes. ICD-203 ran the two-dimension experiment for decades with trained analysts: probability and confidence were consistently conflated; confidence terms shifted the *location* of estimates, not the width. Replace with a deterministic evidential-state string. |
| UPDATE CONDITION | **Elevate to mandatory — this is the point of the feature.** Bind to a real dial + date. |
| SO WHAT | **Kill in finance/health.** It is the advice field and the regulatory surface. Substitute: *"what I'd be embarrassed about if I'm wrong."* |

Missing field the founder didn't have: **the warrant** (Toulmin) — the inferential link from
evidence to conclusion. Do not import the word; fuse grounds+warrant into the MECHANISM field.

## What the data actually supports (from the worked examples)

The framework tracks **ledger resolvability, not data volume**:
- White-collar displacement: *no corpus at all*, but resolved dated claims on record → best thesis on the shelf.
- 80-Year Collapse: richest corpus in the repo (38 videos, 12 predictions, 14 indicators) → **cannot render a score**.
- Housing Crash: 3 videos, no ledger → framework fails, correctly. Needs a null card.
- Seed oils (health): **actively hazardous** unfilled — POSITION and SO WHAT become medical advice.

**Prerequisite for a thesis is: ≥1 resolved dated claim + ≥1 named predictor + ≥1 sourced
opposing camp.** Not video count.

## Bugs the research found in shipped code/data

1. `computeReceipt` sets `resolved = SUPPORTED + REFUTED`, excluding UPDATED and AMBIGUOUS.
   Result: the n≥5 score gate is **blocked on every narrative in the product**, and the single
   most damning accountability fact — the goalpost move — is invisible to it.
   **Fix:** keep n≥5 for any *rate*, but add an ungated **clock-integrity statistic**
   (UPDATED count, median horizon slip, years-since-first-claim-unresolved). These are counts,
   not rates; they make no frequency claim so they need no gate.
2. Two ledger entries are past their date and still stored PENDING (`armstrong-2026-clarity`;
   Galloway's Aug 2026 forced-selling count). A thesis pointing at an unscored clock
   manufactures false confidence in the audit itself.
3. Stored prose has drifted from stored data: `crypto-winter-watch/narrative.json` says
   "12/18 original"; videos.json is now 13/32 (41%). Any generator must read arrays, never blurbs.
4. 4 of 7 relations in `collapse-audit/relations.json` carry `videoIds: []` — they fail the
   project's own ≥3 videos / ≥2 channels evidence gate. The counterweight slot is currently
   the least-sourced slot in the framework.
5. Zero `counters` edges exist across the corpus; `relations.json` exists for 1 of 6 narratives.

## Category and moat

- Argument-mapping as a category is **near-total commercial failure** (Kialo, Rationale, bCisive,
  Debategraph). Do not move there.
- The thesis *format* is fully commoditised — any frontier model emits it on request. Zero defensibility.
- What is defensible: **the resolved prediction ledger** (time-in-market — a competitor with $50M
  starts at n=0 and needs 18 months before one call resolves), the **UPDATED/deadline-roll counter**,
  **mutation history**, and **legal-risk arbitrage** (scoring named people on accuracy is what
  general assistants hedge or refuse; the existing guardrails are a licence to operate).
- The category move is *not* "understanding → deciding". It is **"commentary on media → a
  proprietary record of who said what and whether it happened."**
- Switching cost today is ~zero. **Scoring the user's own calibration is the fix** — their record
  of what they thought, when, and whether it landed is the one form of personal data that is
  genuinely theirs, and it compounds exactly like the public ledger.

## Belief updating

- **Most users will never return. Plan for that as the base case.** Value must not depend on it.
- **The update engine is `git diff`, not a cron job.** Store the corpus commit SHA at save time;
  on return, diff HEAD against it and filter to the thesis's footings. No backend, no polling,
  cost incurred only when a user actually comes back.
- **Reasons must be built from citable corpus objects** (prediction id, indicator id, claim id,
  predictor, relation edge) — "footings". If theses are free text, updating is permanently
  impossible. Decide this before shipping anything.
- Version history hangs off **(user, question)**, not (user, narrative) — answers rotate under
  the durable question.
- Add the trigger nobody lists: **silence.** "No new ORIGINAL video in 90 days" is free to
  compute, is a fact about the corpus rather than a claim about the world, and covers the
  overwhelmingly common case where nothing happened.

## Recommended build (staged)

- **Stage 0 — no position at all.** Make the *Radar Read* portable: a deterministic, shareable
  structural card + "my review date". Tests the articulation demand at zero new risk.
- **Stage 1 — Thesis Intake, private only.** User types unaided; the machine returns structure
  (who else says this, their resolved record, the opposing camp verbatim with receipts, the dial
  that would settle it, what's absent from the corpus). Demands a date + dial or nothing saves.
- **Stage 2 — sharing**, counterweight-first format, only if Stage 1's scoring rate clears a
  pre-registered bar (suggest: ≥30% of theses returned to and scored, or delete the feature).
- **Never:** machine-composed positions, numeric confidence, SO WHAT in finance/health,
  re-ingesting user theses into the corpus (reflexivity would pollute the instrument).

## The line to keep on the wall

> "The algorithm pulls you deeper. This is the exit." An exit that hands you a well-written
> opinion on the way out isn't an exit — it's a different room with better furniture.
> **The honest exit hands you a deadline.**
