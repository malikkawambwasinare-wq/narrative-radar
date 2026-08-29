# Evidence packets

One packet per claim that has matured past its grace period. A packet is the material a ruling
is made **from**; it is never the ruling.

## The separation, and why it is strict

`scripts/resolver.mjs` says what is due. A packet says what the record shows. **Neither says what
is true** — [STANDARD.md](../STANDARD.md) §6 reserves that for a named human, and it means it.

The failure mode this guards against is subtle and worth naming: a packet that quietly frames the
evidence has already made the ruling, and the signature on it becomes ceremonial. Outsourcing the
frame is outsourcing the judgment. So every packet follows a **fixed template derived from the
published criteria** — not from the case in front of it — and the template forbids the things that
would let a frame in:

- **No recommendation field.** There is nowhere to put one.
- **Reading A and Reading B**, each stated at its strongest, comparable in length and sourcing.
- **All four outcomes restated neutrally**, each with the factual condition that would make it
  correct, with no indication of which applies.
- **Distinguishing questions phrased as questions**, never as answers.
- **Gaps declared.** What could not be established is part of the evidence.

If the facts really do point one way, that is visible to the adjudicator from the facts. It is not
the packet's job to say so.

## Sourcing rules

Every factual assertion carries a URL. Primary sources (congress.gov, senate.gov, official filings,
the Congressional Record) outrank news; news outranks blogs. Anything that cannot be established is
written as **NOT ESTABLISHED**, with a note on what was searched. A blank is always better than a
confident guess — this is a record about named people, and a fabricated citation would poison the
whole instrument.

Archive load-bearing links. A source that disappears after a ruling is itself a finding, and the
ledger should be able to show what it saw.

## Drift audit

Packets may be prepared by an assistant or an analyst. To keep that from silently becoming
delegated judgment, **the adjudicator builds a packet from scratch himself periodically** and
compares it against the prepared one. Divergence in what gets included is the early warning that
the frame has started drifting.

## Files

- `TEMPLATE.md` — the fixed template. Copy it; do not improvise a structure per case.
- `<claim-id>.md` — one packet per claim, named for its ledger id.

A signed ruling is copied back into the claim's entry in `corpus/<topic>/predictions.json`
(`status`, `outcome_note`, `ruled_on`, `standard_version`), and the packet stays here as the
working paper behind it.
