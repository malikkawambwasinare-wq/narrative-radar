# The Narrative Radar Adjudication Standard

**Version 1.0 — published 29 August 2026, before any prediction in this ledger had been
scored under it.**

This document is the rule. It says what counts as a claim, when a claim is due, what each
outcome means, and who decides. It is published in advance and versioned in public so that
every ruling can be checked against the rule that existed when the ruling was made.

That order matters more than anything else here. Data about what people said is copyable;
anyone with a model and a fortnight can reconstruct a corpus. A dated judgment, made under a
fixed published rule, by a named person, *before the outcome was known*, is not
reconstructible by anyone later. **The record is the product. This document is what makes it
a record rather than an opinion.**

---

## 1. What counts as a claim

A statement enters the ledger only if all four are true:

1. **Named claimant.** A specific identifiable person or publication. Not "analysts say."
2. **Stated outcome.** Something that could be observed to happen or not happen.
3. **Date made.** When it was said, to at least month precision, with a source.
4. **A horizon**, even a vague one. Claims with no horizon at all are still recorded — their
   unfalsifiability is itself a finding (§4, UNSCORABLE) — but they are never counted in any
   accuracy rate.

A claim is recorded in the claimant's own terms. We do not sharpen a vague claim into a
falsifiable one to make it scoreable; that would be scoring our paraphrase, not their claim.

## 2. Blind extraction — the rule that protects everything else

**The claim, its horizon and its resolution class are frozen before anyone looks up what
happened.** For any claim already past its horizon at the time of entry, extraction and
resolution are two separate passes, in that order, and the frozen extraction is committed
before the outcome is researched.

Without this rule, hindsight quietly reshapes how strictly a claim is read, and every
backfilled score is contaminated. This is why the ledger distinguishes:

- **LIVE CAPTURE** — recorded before the horizon passed. The claim was frozen while the
  outcome was genuinely unknown.
- **BACKFILL** — recorded after the horizon passed, under blind extraction.

Both are legitimate. Only the first is impossible for a competitor to manufacture later, and
the proportion of the ledger that is live capture is reported openly.

## 3. Resolution classes

Assigned at extraction, before the outcome is known.

| Class | Meaning | How it resolves |
|---|---|---|
| **AUTO** | A public numeric series settles it — a price, an index level, an official print, a certified election result. | Look up the named series at the horizon. The source is recorded with the ruling. |
| **REVIEW** | The outcome is observable but the words need interpretation — "a bottom", "a bull market", "a crisis". | A human applies §4 and writes the reasoning. |
| **UNSCORABLE** | No falsifiable condition, or no horizon. "Dark times ahead." "Soon." | Never scored. Counted and reported as unscorable. |

**A high unscorable rate is a finding, not a gap.** A commentator whose claims cannot be
graded is telling you something about their claims, and the ledger says so out loud.

## 4. Outcomes

| Status | Means |
|---|---|
| **PENDING** | The horizon has not arrived. Not yet judgeable. |
| **SUPPORTED** | The stated outcome occurred inside the stated horizon, by the stated mechanism where one was given. |
| **REFUTED** | The horizon passed and the stated outcome did not occur. |
| **AMBIGUOUS** | Something resembling the outcome occurred, but not via the stated mechanism, or not cleanly inside the horizon. Timing credit without mechanism credit lands here. |
| **UPDATED** | Before the horizon arrived, the claimant restated the same claim with a moved deadline or a changed mechanism. The original is marked UPDATED and the restatement is entered as a new claim, linked to it. |
| **UNSCORABLE** | Per §3. Never counted in an accuracy rate. |

### The goalpost rule

Moving a deadline is not the same as being wrong, and it is not the same as being right. It
is its own event, and it is recorded as one. A claim that has been restated three times shows
three linked entries, and **the count of deadline moves is reported alongside the accuracy
rate, never folded into it.**

### The grace period

A claim is judged **30 days after its horizon ends**. This is a fixed allowance for reporting
lag — an economic print or a certified result is not always available on the day. The grace
period is the same for every claim, set in advance, and never extended to wait for a claim to
come good.

### Mechanism

Where a claimant states a mechanism, the mechanism is part of the claim. An outcome that
arrives by a different route is AMBIGUOUS, not SUPPORTED. Predicting a recession from debt
and getting one from a pandemic is timing credit, not mechanism credit.

## 5. What a ruling must contain

No verdict is published bare. Every ruling records:

- the frozen claim, its horizon, and its resolution class;
- the outcome, and for AUTO claims the named data series and the value observed;
- the reasoning, in one or two sentences;
- the date of the ruling and the version of this standard applied;
- a link to the source, so a reader can check the claim was said as recorded.

A verdict a reader cannot check in one click is not a verdict. It is an assertion.

## 6. Who signs

**Malik Kawambwa** applies this standard and signs every ruling.

One judge, one standard, applied continuously. Rotating adjudicators would inject
inter-rater variance that silently corrupts every cross-claimant comparison the ledger
exists to support. Evidence packets may be prepared by others; **the ruling may not be
delegated, and no ruling is ever generated automatically.** Software here does exactly one
thing: it says what is due. It never says what is true.

## 7. Corrections

Errors get corrected in public, dated, with the original visible. A ledger that quietly edits
its own history is exactly the thing this product exists to catch. Corrections are entries,
not deletions.

## 8. What is deliberately not here

- **No confidence percentages on verdicts.** A number implies a calibration we have not
  earned. Statuses are categorical.
- **No aggregate "accuracy score" per person** until that person has at least five scoreable
  resolved claims. Below five, counts are shown and rates are not.
- **No scoring of opinions, values, or predictions about private life.** Only public,
  dated, falsifiable claims about observable outcomes.
- **No inference about motive.** The ledger records what was claimed and what happened. Why
  someone was wrong is not something this instrument can measure.

## 9. Amendment

This standard is versioned. Changes are additive where possible, dated, and never applied
retroactively to rulings already made — a ruling states the version it was made under, and
that ruling stands under that version. Substantive changes require a new minor version and a
note in the changelog below.

### Changelog

- **1.0 — 2026-08-29.** First published. No prediction in the ledger had been scored under a
  published rule before this date; the classifications existing prior to it are marked
  BACKFILL and were assigned in research, not adjudication.
