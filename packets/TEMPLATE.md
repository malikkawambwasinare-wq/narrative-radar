# Evidence packet — `<claim-id>`

> Prepared under [STANDARD.md](../STANDARD.md) v1.0. This document contains **no recommendation**.
> It exists so a named adjudicator can rule from the record. See [README.md](README.md).

## 1. The frozen claim

Reproduced verbatim from the ledger, with the commit that froze it. Never re-worded here —
STANDARD.md §1 forbids sharpening a claim to make it easier to score.

| | |
|---|---|
| **Claim** | *verbatim* |
| **Claimant** | |
| **Made** | |
| **Stated horizon** | *verbatim* |
| **Due window** | `due.start` → `due.end` (precision) |
| **Resolution class** | auto / review / unscorable |
| **Capture** | live / backfill |
| **Frozen at** | commit hash, date |
| **Source** | URL — and whether it is still reachable |

## 2. The deadline

The date the horizon actually closed, how it was established, and how firmly. If the deadline
itself is contested or slipped, that belongs here — a claim cannot be judged against a date nobody
can pin down.

## 3. What the record shows

A dated timeline of established facts. One row per fact.

| Date | Fact | Source | Type | Confidence |
|---|---|---|---|---|
| | | URL | primary / news / secondary | high / medium / low |

Anything that could not be established is written **NOT ESTABLISHED** here rather than omitted.

## 4. Reading A

The case that the stated event occurred inside the horizon, by the stated mechanism. Stated at its
strongest, on the sourced facts above.

## 5. Reading B

The case that it did not, or that what occurred was not the stated event. Stated at its strongest,
to the same length and standard of sourcing as Reading A.

## 6. What would distinguish them

The specific questions the adjudicator must answer to choose between the readings. **Questions
only.** If a line here can be read as an answer, it does not belong in this section.

## 7. The four outcomes available

Restated from STANDARD.md §4, with the factual condition that would make each correct. No
indication of which applies.

| Outcome | Correct when |
|---|---|
| **SUPPORTED** | The stated outcome occurred inside the horizon, by the stated mechanism where one was given. |
| **REFUTED** | The horizon passed and the stated outcome did not occur. |
| **AMBIGUOUS** | Something resembling the outcome occurred, but not via the stated mechanism, or not cleanly inside the horizon. |
| **UPDATED** | Before the horizon arrived, the claimant restated the claim with a moved deadline or changed mechanism. |

## 8. Gaps

What could not be established, and what would close each gap. A gap that cannot be closed may itself
determine the outcome — an unfalsifiable claim is UNSCORABLE, not REFUTED.

## 9. Sign-off

To be completed by the adjudicator. Nothing above this line may be filled in on their behalf.

```
outcome           : ________________________________________
reasoning         : ________________________________________
                    ________________________________________
ruled by          : ________________________________________
date of ruling    : ________________________________________
standard version  : 1.0
```

Once signed, copy `status`, `outcome_note`, `ruled_on` and `standard_version` back into the claim's
entry in `corpus/<topic>/predictions.json`. This packet stays as the working paper behind it.
