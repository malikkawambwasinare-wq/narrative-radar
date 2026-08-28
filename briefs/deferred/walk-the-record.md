# Deferred: Walk the Record (3D scroll-world) — 21 Aug 2026

**Status: built, verified, parked.** Not shipped in v1.

## The decision

Ship the plain product first and find out whether people want the *service* — a narrative tracker that
shows what is being claimed, by whom, on what clock, and whether it happened. The immersive walk is an
**add-on**, justified only if the concept itself lands with users. Building audience for a format before
the substance has an audience is the wrong order.

Deferring it also removes the two costs it would carry at launch: a Three.js payload on a page nobody has
asked for yet, and per-narrative hand-choreography (the walk is authored per narrative — it cannot be
generated for a shelf where 5 of 6 narratives are thin).

## Where it lives

- Branch: **`feature/walk-the-record`** — complete, at commit `cc039c2` (v3, "the archive gantry").
- File: `prototypes/walk-the-record.html` (single file, no build step, importmap-loaded three@0.169.0).
- Removed from `main` so the shipped repo stays clean.

## What it is

A five-chapter scroll-world for `collapse-audit`: one persistent built structure — a tread-plated gantry
with year-ribs, handrails, practical lamps and overhead trusses — suspended in a nebula field. Chronology
is geometry: **60 world units = 1 year, 2015 → 2028**. Camera flies a Catmull-Rom spline through
THE QUESTION → THE PREACHERS → THE CLOCKS → THE TESTS → THE LEDGER. Every object is a receipt: hover for
the claim, click for the source. Real corpus videos render as bezelled screens; goalpost-moves render as
amber arcs; the ledger ends on the honest `0 SUPPORTED`.

Design rule enforced throughout: **the atmosphere dramatizes the RECORD** — time passing, clocks turning,
deadlines moving, verdicts stamping — **never the CLAIM**. No dread-fog, no doom mood, no autoplay, native
reversible scroll. An exit from the attention machine cannot itself be one.

## Bringing it back

```
git checkout feature/walk-the-record -- prototypes/walk-the-record.html
```

Then link it from the narrative detail page ("Walk the record →"). Two prerequisites before that is worth
doing:

1. **The keystone must exist.** Chapter 5 ends on a scoreboard; it only pays off once real rulings under a
   published standard are landing there. Today those classifications are backfilled research, badged as such.
2. **Depth.** The walk needs a narrative with a real ledger, real mutations and a real corpus. Only
   `collapse-audit` currently qualifies.

## Revisit trigger

Users engage with the plain narrative pages *and* ask for more depth on a flagship — or the weekly brief
needs a shareable centrepiece. Not before.
