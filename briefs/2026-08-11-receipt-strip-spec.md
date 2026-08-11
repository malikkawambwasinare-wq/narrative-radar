# Receipt Strip — final metric spec (11 Aug 2026)

Product of an 8-agent research pass: six lenses (10-second decision, return-and-depth,
forecasting science, misinformation/lifecycle, quant/attention, competitor scan) proposed
44 candidate metrics; a computability auditor verified each against the real repo data;
an integrity auditor attached guards. This spec is the synthesis.

## Verdict on the original five

| Original | Verdict | Why |
|---|---|---|
| Age | KEEP, guarded | "Roughly 11 years (unverified)" until genesis-traced; bare number only when verified. Never stands alone — old ≠ wrong (fuse with Score in the punchline sentence). |
| Deadline moves | UPGRADE | Count undersells and over-accuses. Show TIME slipped ("6 moves — 9 years of 'any day now'"), and split evidence-cited revisions from evidence-free rolls; only the latter feed the headline. Honest updaters are doing science; the metric must not punish them. |
| Score | KEEP, gated | n ≥ 5 resolved before a score renders (PunditTracker's lesson). Below that: "Too early to score — first real test: Nov 2026." AMBIGUOUS always visible in the same sentence ("0 of 7 — plus 2 we couldn't grade"); PENDING count shown. |
| Next test | KEEP, named | "Next test in 47 days: Maloney's 'silver $100 by Nov 2026'." Third state is a warning, not a blank: "This story makes no checkable predictions." |
| Life stage | REPLACE (6/6 lenses) | A model adjective, not a receipt — exactly the opaque-label pattern users mock in NewsGuard-style scores. Replaced by Recycled share. |

## The strip (headline tier, ≤6 slots, adaptive)

1. **Age** — "This story is 11 years old" (⚑ verified badge when genesis-traced; "roughly" + unverified label otherwise).
2. **Score (gated)** — "0 of 9 dated predictions arrived (+2 ungradeable, 4 pending)" | "Too early to score" | *(slot swaps to Falsifiability when there's nothing datable)*.
3. **Slippage** — "Deadline moved 6× — 9 years of 'any day now'" (evidence-free rolls only; reasoned revisions counted separately: "revised once, with reasons").
4. **Next test** — "In 47 days: [predictor]'s [claim]" | "No future dated claims" | "Makes no checkable predictions" (warning state).
5. **Recycled share** — "18 of the last 20 videos we indexed are recycled or clickbait." Trailing window (N=20), denominator in the sentence, suppressed below 10 indexed. Phrasing MUST own the sample: "we indexed", never a census claim.
6. **Source independence** — "71% of the 48 videos we track come from just 3 channels." Computable today from the channel field (after normalization).

**Falsifiability instrument** (swaps into slot 2 for narratives with no dated claims — the
seed-oils problem): "Only 3 of its 12 predictive claims name a date or number." Denominator
restricted to claims tagged predictive at analysis time; disclosed as model-extracted.
Unfalsifiable narratives must never look clean by virtue of an empty ledger.

**Punchline sentence** (auto-written above the strip) fuses Age+Score+Slip+Next-test and MUST
have a vindication variant with equal prominence — the ledger scores wins too:
- Doom variant: "This story is 11 years old, has moved its deadline 6 times, and none of its 9 dated predictions have arrived. Next test: November 2026."
- Vindication variant: "This story called its shot: 4 of 6 dated predictions arrived, including the July 2026 reactor deadline."

## Card tier

- **Messenger's record (per-predictor)** — THE biggest gap found; proposed independently by 5 of 6 lenses. "Maloney: 0 of 7 dated calls in narratives we track; 4 deadline moves." Gate: n≥5 resolved per predictor; phrase as "in narratives we track" (a sample, never the person's whole record); requires channel/predictor name normalization (fields are dirty: "Tom Bilyeu and ProfSteveKeen"). Cross-narrative rollup + predictor pages LATER, and only with a right-of-reply mechanism.
- **Eyeball toll** — "At least 8.4M views; 0 of 9 dated predictions arrived." Render only when Score passes its gate; "at least" mandatory (view coverage is partial and frozen at first scrape); show coverage ("views known for 33 of 38").
- **Staleness** — "No NEW prediction in 14 months; 27 repeat videos since." (needs publish-date reconstruction).
- **Ambiguity rate** — share of resolutions that were ungradeable; pairs with Score.
- **Mutation history** — keep existing timeline; attribute to the crowd ("the reasons offered have included…"), each mechanism needs a dated video receipt; evasion framing reserved for per-predictor view.
- **Common-ground line** — "The one claim both camps make: …" — attribution phrasing only, never asserts truth; links citing videos.
- **What-changed delta** — for returning followers (needs lightweight change-log; schema addition).

## Deep tier (tabs / later)

- Cross-platform lag (X genesis date → first YouTube video) — computable per traced narrative.
- Spread velocity / momentum — ONLY after scheduled systematic sweeps exist; until then corpus growth measures analyst attention, not the world. Label "in our corpus."
- Frozen citations (versioned permalinks with live "superseded" banner).
- Incentive exposure — human-audited flags with evidence URL inline, only monetization whose payoff moves with belief in the narrative; needs a base rate; NOT automatable yet.
- Quiet exits (channels that stopped mentioning failed calls) — do not ship until a targeted post-deadline channel search is run and stored as the receipt.
- Cost-of-belief backtest (financial narratives) — fixed published entry rule (first dated claim's date, never peak), total-return, "hypothetical, not advice." Needs price-data source.

## Data hygiene the build depends on (found by auditing the real repo)

1. `published` is a relative scrape-time string ("4 hours ago") — reconstruct ISO date as
   `first_seen − age_days`; store `published_est` going forward (collector + analyze).
2. `views` is a display string frozen at first scrape — parse numeric, store `views_seen_at`.
3. `channel`/predictor strings are dirty — normalization pass before any per-predictor metric.
4. Ledger UPDATED entries must store the superseded deadline (old → new) + `reason_on_record`
   flag — this powers Slippage and the revision/evasion split. Verdict-pass prompt change.
5. Ledgers exist for only 2 of 5 current narratives — the strip renders per-metric only where
   data qualifies; shells show the "too early" states, never fake numbers. Deep pipeline
   (flagship build) is what earns a full strip.
6. Collector KEEP_DAYS=14 means the corpus is a recent-activity window, not an archive —
   all corpus-composition metrics phrase accordingly ("of the videos we indexed").

## Product-level guards (from the integrity audit)

- Vindication path: every doom-shaped metric has a win-shaped variant of equal visual weight.
- Right of reply before named-predictor pages go public.
- "What would change our mind" steelman line per narrative (card footer).
- Honest empty state for pastes matching nothing we track.
- Future: receipt archiving (videos/posts get deleted), fingerprint-evasion watch (creators
  will paraphrase once they learn the radar matches exact phrases).
