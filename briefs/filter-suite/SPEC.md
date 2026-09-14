# Narrative Radar — Series filter bar, final specification

Scope: `index.html` (`SF_DEFAULT`, `seriesFilterBar`, `seriesPass`, `ytTags`, `renderSeries`, `loadTopicData`). Numbers are from the repo as of 2026-09-14: 87 videos in 6 topics, 65 kept after RECYCLED/CLICKBAIT removal (21 ORIGINAL / 39 DERIVATIVE / 5 UNREVIEWED). Collapse Audit: 39 videos, 25 kept (7 episodes + 18 angles), 14 removed. Crypto Winter Watch: 32 videos, 25 kept (13 + 12), 7 removed. Ledger: 26 entries in 2 topics. Extracted claims: 58 in 2 topics (all UNREVIEWED). Every count below was recomputed from disk; where an input document's number did not reproduce, the reproduced number is used and the discrepancy is noted.

Result: 27 keys in `SF_DEFAULT` (26 rendered — `language` only renders with >1 language) become 11: 7 in the primary row, 4 in a drawer, plus one always-rendered fold and one always-rendered "showing" line. Six of the eleven are new or materially changed; the rest are existing controls kept as they are.

---

## 1. The traps, and what closes each

| # | Trap | Closed by | Status on today's data |
|---|---|---|---|
| 1 | Fear-cycle titles (crash/collapse/warning) | `titleBait` = crisis-now (crisis word AND now word); angles fold, episodes badge | Closed for angles: 10 of 44 kept angles fold, 0 of 21 episodes flagged |
| 2 | Urgency words (JUST, NOW, "about to", "prepare") | same control, the now-term half of the conjunction | Closed with 1; single-feature rules were rejected (they hit 6 originals) |
| 3 | Recycled warnings re-cut weekly | Upstream: the RECYCLED verdict (9 removed) now visible in the `showRemoved` fold; `basis` folds verdicts made without the transcript | Closed upstream; no per-channel repeat filter — the proposed ones fold 0 videos on Collapse Audit (see §8) |
| 4 | Sponsored fear | Nothing on disk detects it. YouTube's flag marks ad-read podcasts (7 of 21 originals; 0 of 22 removed videos). `paid` stays as a fact filter in the drawer, never in a preset | Open — see §9 |
| 5 | Engagement bait (caps, `!!`, INSANE) | `titleBait` = shouty; and cutting `minEng`, `minDisc`, `breakout`, which rewarded it | Closed for angles: 6 of 44 kept angles, 0 episodes |
| 6 | Crisis-farming channels | Upstream CLICKBAIT verdict (13 removed); `channelAge` folds angles from channels under a year old at publish | Partly: 4 angles corpus-wide; the strike-count filter folds 1 video corpus-wide and was rejected |
| 7 | Predictions that never resolve | `deadline` (extracted-claim horizons parse to a date or not); ledger chip counts split pending-dated from pending-undated; `track` renamed so "on the ledger" no longer reads as "graded" | Closed in 2 topics for the 23 kept videos with extracted claims; 3 undated-only episodes fold |
| 8 | One-camp confirmation loop | `camp` (Side) under `claim`, with "the other side" | Closed where a claim has ≥2 camps: crypto four-year-cycle (12 kept), bottom-depth (5), open-vs-closed (6). On Collapse Audit the only contested claim disputes the trigger, not the conclusion — the control switches mechanism, not doom vs no-doom, and says so |
| 9 | Expert laundering via clip channels | Upstream RECYCLED removal (DOAC Clips 2 of 3) made visible in `showRemoved`; `speaker` for navigation | Closed upstream; the surviving DOAC Clips video is an ORIGINAL by transcript read |
| 10 | Length inflation | Nothing: the stitched compilations are the removed set (18 of the 20 removed videos with a length sit in 10–30 min). The duration badge stays on the thumbnail | Closed upstream; the `length` filter cannot separate a 25-min compilation from a 25-min interview and is cut |
| 11 | Stale footage sold as new | Upstream RECYCLED (both relative-date collapse videos are removed). Title-year and first_seen rules rejected (they flag forecasts and crawl dates) | Open per video — see §9 |
| 12 | Popularity read as truth | Cutting `minViews` default, `verified`, `minSubs`, `breakout`, `aboveAvg`, the "most viewed" order, and views/subs off the card face | Closed |
| 13 | Live crash streams | Nothing: the 3 live videos on disk are all ORIGINAL primary sources (Coinbase earnings AMA, Crypto Banter interview, Rekt Radio interview); zero doom live streams exist in the corpus | No filter; `live` tag stays on the card |
| 14 | Binge, no stopping point | Numbered episodes; angles already closed by default (`<details class="angles">`); `showRemoved` makes the floor visible | Partly; the watched-fold was rejected as a completion-progress pattern |
| 15 | Shock thumbnails | Not computable: no thumbnail bytes on disk | Open |

---

## 2. Audit of the current controls (all 27 `SF_DEFAULT` keys)

| key | verdict | reason | change |
|---|---|---|---|
| `q` | keep | Navigation; title+channel present 87/87; cannot fail on missing data. Speaker-name matching was rejected (the app does not load claims-extracted.json; every match it would add is already reachable via `speaker`). | None. Primary row, first. Placeholder stays "title or channel". |
| `minViews` | cut | The inherited default of 1,000 is a popularity gate every viewer got without touching it (rule 3). It folds Times Now World (414 views, 1.29M subs) and a 56-view crypto episode; only 7 of 65 kept are under 1K. Angles never read it. | Remove key, the `isLow`/`low`/`lowCount` path and the "low-reach" fold. Views move to the details hover. |
| `sort` | rethreshold | Chronological order is the product; "newest first" is a reading choice. "Most viewed" is the popularity-first order and the one ordering rule 3 forbids the bar to offer. "Next test first" was rejected (§8). | Options: as it happened / newest first. Drop `views`. |
| `length` | cut | Closes no trap: "10–30 min" returns 46 of 70 parseable; the compilations are removed upstream; blank for 100% of three corpora (15 of 65 kept) and treated as fail. | Remove. `thumb()` already badges duration. |
| `basis` | rename | The one honesty control we own, hidden behind "Verdict basis" and a 3-way select with a maintainer option. | Checkbox "Transcript-read verdicts only", primary row, default off. See §5. |
| `category` | cut | Creator-chosen: DOAC files as People & Blogs, David Lin's podcast as News & Politics; "news outlets only" implied credibility the field cannot carry. | Remove. Category goes to the details hover. |
| `verified` | cut | An exact subset of subscribers ≥100K (0 verified under 100K; 16 videos from unverified channels over 100K). A tick reads as vetting. | Remove from bar and card. |
| `minSubs` | cut | Size as truth. 9 of 65 kept are from channels under 10K; the biggest crisis farms have the most subscribers. | Remove from bar and card. No subscriber count anywhere in the Series view. |
| `minAge` | rethreshold | 1 year is the only threshold with a farm signal (8 videos from channels under 1 yr: 4 CLICKBAIT, 1 RECYCLED, 2 DERIVATIVE, 1 UNREVIEWED, 0 ORIGINAL); 5+ and 10+ hid 3 and 5 of 7 collapse episodes. Today's version measures age now, not at publish. | Becomes `channelAge`: one checkbox at 1 year, age at publish time, angles fold, episodes badge, drawer. See §5. |
| `maxRate` | cut | Inverted on this corpus: ORIGINAL channels post a median 299 videos/yr vs 156 for removed ones; "1 a week" folds 0 of 7 collapse episodes; ">1/day" folds CNBC, Yahoo Finance, TYT and Times Now while Crypto Nutshell (4 of 5 removed) passes. | Remove. "posts N+/day" moves to the details hover. |
| `channel` | cut | 20 of Collapse Audit's 23 options hold one video; `q` matches channel names already; the proposed re-keying and hide mode fold at most 2 of 25 cards. | Remove. |
| `minEng` | cut | Likes/views is engagement bait's own scoreboard and inverts with size (DOAC 1.9%, a 56-view video 21%); likes null on 8 incl. 2 kept collapse angles. | Remove. Engagement % off the card; likes to the hover. |
| `minDisc` | cut | Comments-per-like rewards argument; .02/.05 pass 73 and 66 of 78 (no-ops); comments-disabled is indistinguishable from zero. | Remove. Comments to the hover. |
| `breakout` | cut | True for 12 of 87: 0 ORIGINAL, 6 DERIVATIVE, 2 RECYCLED, 4 CLICKBAIT — a tiny-denominator artefact (USA ECONOMY: 19 subs). Hides 7/7 collapse and 13/13 crypto episodes. | Remove from bar and card. |
| `aboveAvg` | cut | Lifetime channel average incl. Shorts and back-catalogue (CNBC: 158,846 videos) vs one video's views; a popularity comparison with no bearing on any trap. | Remove from bar and card. |
| `paid` | move | YouTube's creator-ticked flag, present 87/87, but it marks sponsor-read podcasts, not fear sellers: 20 ticked = 7 of 21 ORIGINAL, 11 of 39 DERIVATIVE, 0 of 22 removed. Folding "none disclosed" punishes disclosers, so it never belongs in a preset or under a "sponsored fear" label. | Drawer, relabelled "Paid promotion (YouTube's flag)"; options any / no disclosure ticked / disclosure ticked; tooltip says undisclosed is not unsponsored. |
| `live` | cut | 3 live videos, all crypto, all ORIGINAL primary sources; on Collapse Audit the control can only return nothing. Folding them under a "crash stream" label would hide the best sources. | Remove. `live` tag stays on the card. |
| `chaptered` | cut | YouTube auto-generates chapters and the scraper cannot tell them apart; 30 of 65 kept have them; separates nothing. | Remove. Chapter count to the hover. |
| `captions` | cut | Reviewer signal, not viewer signal; its null value is exactly the 3 unavailable pages, so "none" selected broken videos. | Remove. "captions by creator" to the hover. |
| `language` | cut | The only non-`en` values on disk ("ar" ×2: Crypto Banter, Stefan 3D AI) are both wrong — English shows with a mis-set audio language. | Remove. Reinstate only when a transcript-confirmed non-en code covers ≥3 videos. |
| `track` | rename | The only permitted credibility signal, but "has a ledger record" passes speakers whose every row is unscorable (Saylor, Gerhard) and reads as "graded". On Collapse Audit it keeps 1 of 25 (the DOAC Dalio episode) and folds 6 of 7 episodes; on crypto 14 of 25. | Drawer checkbox "Speaker is on the ledger" with an honest tooltip; the card chip carries the counts. See §5. |
| `speaker` | move | Name directory built from claims.json (collapse 13 of 25 kept, crypto 25 of 25). The laundered copies it was meant to expose are removed upstream, so every collapse option resolves to one kept video. Navigation, like `q`. | Drawer, unchanged. Ledger counts in option labels rejected (they double-counted UPDATED+unscorable rows). |
| `claim` | keep | Membership filter on claims.json sources; unchanged. Needed as the parent of `camp`. The proposed "everyone here agrees · N videos" labels counted removed videos and were social proof. | None to the control. Primary row, group Confirmation loop. |
| `country` | cut | Channel nationality counters no trap; 7 of 65 kept unknown; invites nationality-as-credibility. | Remove. Country to the hover. |
| `from` | cut | Year granularity: Collapse Audit's kept set is entirely Jul–Aug 2026, so the select offered one year. The merged "Published" replacement was rejected (relative windows measure crawl age; "last 30 days" empties every topic today). | Remove. Published date stays on the card. |
| `to` | cut | Same as `from`. | Remove. |
| `season` | cut | All 25 kept Collapse Audit videos fall in S6, so the select is "any" under another name; crypto S5/S6 is a date split; four topics have no mutations. `seasonOf` is purely temporal, so it also stamps a mechanism on videos that do not argue it. | Remove the select. Keep the season headers and prologue in the chronological listing (index.html 1871–1885); they are labels, not filters. |

---

## 3. Presets

Rendered as chips above the bar. Changing any control switches the active chip to "custom". `q` is ignored when matching a preset. All presets keep `sort` as the viewer left it.

| Preset | One line | Exact settings | Measured cost |
|---|---|---|---|
| **Bait off** (default) | Folds crisis-now and shouty titles — angles only; episodes are never folded on a title. | `titleBait:"both"`, everything else off/any | Collapse Audit: 0 of 7 episodes, 7 of 18 angles (Graham Stephan, Economics Help, ITM Trading, Casey Simpson, Meerkat Explains, Reventure Consulting, Meet Kevin). Crypto: 0 of 13 episodes, 3 of 12 angles (Savvy Finance ×2, Crypto Capital Venture). Corpus-wide: 14 of 44 angles, 0 of 21 episodes. |
| **Transcript-read only** | Bait off, plus only verdicts made with the transcript in hand, plus angles from channels under a year old at publish folded. | Bait off + `basis:true` + `channelAge:true` | Collapse Audit: 1 of 7 episodes (E1, David Lin / Rick Rule — metadata verdict), 13 of 18 angles (7 title, 5 basis incl. the 3 UNREVIEWED, 1 channel age: Extraordinary Explained); 5 angles remain visible. Corpus-wide `basis` alone folds 4 of 21 episodes and 28 of 44 angles. |
| **Deadline or nothing** | Bait off, plus fold videos whose every extracted claim has no date. | Bait off + `deadline:"some"` | Collapse Audit: 1 of 7 episodes (E6, DOAC Clips, sole claim "unspecified"), 7 angles (title only); 16 of 25 pass on "claims not extracted" — the filter only bites on the 9 kept videos with extracted claims. Crypto: 2 of 13 episodes (Gerhard, Vandell Aljarrah). Chip disabled outside these two topics with the note "no claims extracted for this story yet". |
| **Everything** | Nothing folded except what our verdicts removed, which stays visible in the removed fold. | all any/off | 0 folded; removed fold still rendered. |

Rejected presets: "No sponsored fear" (would fold 7 of 21 originals for ticking a box), "Both sides" (on Collapse Audit it would present three camps that all predict collapse as balance), "No recycled warnings" (its distinguishing control, `repeats`, folds 0 videos on Collapse Audit). See §8.

---

## 4. Defaults

```js
const SF_KEY = "series-filters-v2";   // bump: stale saved values (minViews:1000 etc.) must not leak in
const SF_DEFAULT = { q: "", sort: "chrono",
                     titleBait: "both",          // any | crisis | shouty | both
                     basis: false,                // Transcript-read verdicts only
                     deadline: "all",             // all | some | every   (rendered only when claims-extracted.json exists)
                     claim: "all", camp: "all",   // camp rendered only when the chosen claim has >= 2 camps
                     channelAge: false,           // drawer
                     track: false,                // drawer
                     speaker: "all",              // drawer
                     paid: "all" };               // drawer: all | no | yes
```

What the defaults do on Collapse Audit (25 kept):
- Episodes: 7 of 7 shown, in chronological order, season headers as today.
- Angles: 11 of 18 shown; 7 folded inside their episode's angle list under one line "7 angles folded: crisis-now title — show" (per episode: 4 under E1, 2 under E3, 1 under E6/E7 depending on same-day tie order).
- Removed fold at the bottom: "14 removed by our verdict — show" (8 RECYCLED, 6 CLICKBAIT; 2 carry the "metadata-only verdict" tag).
- Notice: "1 of 25 videos: YouTube page unavailable at last check (2026-09-13)" (Global Economy Files, hollow `yt`). Today this notice never fires because `keep.filter(v => v.yt)` counts a hollow block as enriched.
- Showing line: `Showing 7 of 7 episodes · 11 of 18 angles (7 folded: crisis-now title) · 14 removed by our verdict · 1 YouTube page unavailable`.
- Compared with today's defaults: today folds 1 episode (Times Now World, 414 views) for reach and shows all 18 angles.

Integrity rules that apply to every control:
1. `seriesPass` returns `null` (pass) or `{ fold: "<reason>" }` or `{ unknown: "<field>" }`; no boolean. Missing data folds as unknown with the field named ("channel age not on file"), never fails silently.
2. ORIGINAL episodes never fold on a title or channel signal (`titleBait`, `channelAge`); they get the badge. They do fold on `basis`, `deadline`, `claim`/`camp`, `track`, `speaker`, `paid` — those are about the verdict, the claim or the speaker, not the packaging.
3. Every fold is in place: a folded episode renders as a one-line `<details class="fold">` in its chronological slot — "Episode 3 · folded: <reason> — show" — and keeps its number. Folded angles group by reason inside the episode's `<details class="angles">`. The "hidden by your filters" bottom bucket (`hid`/`hidCount`) is removed.
4. A video with `yt.channelId == null` (3 on disk: 1 kept) is unknown for every yt-based control and carries the "YouTube page unavailable at last check" tag; `enriched` in `seriesFilterBar` counts `v.yt && v.yt.channelId`.
5. Ledger-derived numbers are counts with their denominator, never rates, never coloured by outcome (STANDARD §8; the `rec.bad` colour class is dropped).
6. Controls with no data in the topic are not rendered: `deadline` outside collapse/crypto; `camp` unless the chosen claim has ≥2 camps; `speaker`/`claim` when claims.json is absent (the-2026-setup); `track` when predictions.json is absent.

---

## 5. Controls

### Primary row (7)

**`q` — Find** · group Find & order · existing, unchanged
- Options: free text, placeholder "title or channel".
- Definition: case-insensitive substring over `v.title + " " + v.channel`. Never folds by itself beyond its match; a non-match folds as "no match".
- Data: videos.json title, channel (87/87). Missing data: none possible.
- Trap: navigation for 9 (typing a guest's name finds the podcast that names its guest in the title).

**`sort` — Order** · Find & order · rethresholded
- Options: as it happened (default) / newest first.
- Definition: ascending/descending `publishedEst(v)` (84 ISO dates; 3 relative strings resolve via `first_seen − age_days`). Angles stay chronological within their episode.
- Missing data: `publishedEst` null sinks to the end labelled "undated" (0 today).
- Trap: 12 (the views order is gone).

**`titleBait` — Title bait** · group Title bait · new
- Options: any / fold crisis-now titles / fold shouty titles / fold both (default).
- Definition: computed client-side from `v.title` with `TITLE_LEXICON_V1` (§6). crisis-now = at least one crisis term AND at least one now term. shouty = ≥3 all-caps alphabetic tokens of 3+ letters outside the acronym list, OR ≥2 exclamation marks. Emoji are excluded by design (the emoji variant flags two originals). DERIVATIVE/UNREVIEWED angles fold with reason "crisis-now title" / "shouty title"; ORIGINAL episodes show the badge and never fold.
- Data: videos.json title (87/87). Measured on the 65 kept: crisis-now 10 (collapse 7, crypto 2, housing 1), shouty 6 (WorldofAI 3, Savvy Finance 2, Crypto Capital Venture 1), overlap 2 → 14 flagged, all DERIVATIVE; 0 ORIGINAL, 0 UNREVIEWED. Among the 22 removed: crisis-now 2, shouty 2. Single-feature rules rejected: crisis words alone hit 34 of 65 incl. 6 originals (Dalio, Rick Rule, Thornton, Keen, Armstrong, Satoshi); now-words alone hit 4 originals.
- Missing data: none possible. Language gate unnecessary (an English lexicon cannot match a non-English title; the two "ar" labels are wrong anyway).
- Trap: 1, 2, 5. Known cost: two newsy titles fold (Economics Help "Big Tech Just Admitted the AI Bubble Is Real", Reventure "Meta CEO just popped the AI Bubble") — acceptable because the fold is one click away and the badge names the rule.

**`basis` — Transcript-read verdicts only** · group Unread verdicts · renamed (was the 3-way "Verdict basis")
- Options: off (default) / on. Tooltip: "Our original/derivative call was made with the transcript in hand — this is about our confidence in the sorting, not whether the video is right."
- Definition: on → keep `verdictBasis(v) === "transcript"`; others fold in place. Fold reason: "sorted from title and metadata only, not yet re-read against the transcript"; for `verdict === "UNREVIEWED"`: "not yet reviewed". `verdictBasis` unchanged: explicit `verdict_basis` (71/87), else note contains "metadata-only", else transcript file present. 0 contradictions on disk.
- Data: videos.json verdict_basis, verdict_note, transcript. Kept transcript-read: 33 of 65 (17 of 21 originals); Collapse Audit 19 of 25 (6 of 7 episodes), crypto 18 of 25.
- Missing data: none (the fallback always resolves).
- Trap: 3 (a provisional "original" may be a re-cut we have not read).

**`deadline` — Claims name a deadline** · group Predictions that never resolve · new · rendered only when `corpus/<topic>/claims-extracted.json` loads
- Options: any (default) / at least one claim dated (`some`) / every claim dated (`every`).
- Definition: per video, `n_claims` and `n_dated` from the stored `horizon_dated` booleans (§6). `some` folds videos with `n_claims > 0 && n_dated === 0` as "no date stated in any extracted claim"; `every` also folds `0 < n_dated < n_claims` as "some claims undated". Videos with no extracted claims pass with the grey tag "claims not extracted" (shown only while the control is active) — absence is not cleanliness. Episodes do fold here: an undated-only episode is the trap itself. Tag text always says "extracted, not adjudicated". Dated means falsifiable, not credible: rendered grey, never green.
- Data: claims-extracted.json (collapse 17 claims / 11 videos, 15 dated; crypto 41 / 18, 24 dated). Kept videos with claims: collapse 9, crypto 14. Undated-only kept: collapse UNYpubnQDC8 (DOAC Clips, ORIGINAL); crypto y9PN4mfk1hs (Gerhard, ORIGINAL), l0Ia0GNzciI (Vandell Aljarrah, ORIGINAL). `every` additionally folds 7 kept crypto videos (6 ORIGINAL) and 0 collapse.
- Missing data: file absent → control hidden; claim without a `horizon_dated` field → treated as vague and the tag reads "horizon not classified".
- Trap: 7.

**`claim` — Cited for claim** · group Confirmation loop · existing, unchanged
- Options: any / one option per claim in claims.json (statement truncated at 68 chars, as today).
- Definition: keep videos whose id is in `x.claims` (from `videoClaims`); others fold as "not cited for this claim".
- Data: claims.json (collapse 4 claims citing 13 of 25 kept; crypto 8 citing 25 of 25; housing/open-vs-closed/psi 1 each; the-2026-setup none → hidden).
- Missing data: uncited videos fold with the reason above.
- Trap: parent of 8.

**`camp` — Side** · group Confirmation loop · new · rendered only when the chosen claim has ≥2 camps
- Options: all sides (default) / one option per camp, labelled by its `position` text / the other side.
- Definition: `camp k` keeps videos in `camps[k].sources`, folds the rest as "other side of this claim" (N = folded cards, never a claim about which side is larger). "The other side" folds the camp containing the video the viewer arrived from: the `parseVideoId()` result of the last `runLookup()` (store it in a module-level `arrivedFrom`), else the last card clicked this session (in memory). If that video is in no camp of the chosen claim, the option is disabled with "the video you came from does not take a side on this claim". Every card cited under a ≥2-camp claim shows "side 2 of 3: <position, 40 chars>" — no per-camp counts. Claims with 0 camps are worded "the N videos here that mention it agree" (agreement inside this corpus, not truth); claims with 1 camp (housing) hide the control.
- Data: claims.json camps. Live: collapse crisis-trigger 3 camps / 6 kept (AI capex 3, credit seizure 1, yen-carry 2 — all three predict the crisis; the claim note says "same conclusion, competing engines", so on this topic Side switches mechanism, and the position text makes that visible); crypto four-year-cycle 2 / 12 kept (dead 3, intact 9), bottom-depth 2 / 5 (deep flush 3, floor holds 2); open-vs-closed 2 / 6 (5 vs 1).
- Missing data: no `arrivedFrom` → "the other side" disabled with the message above.
- Trap: 8.

### Drawer ("More") (4)

**`channelAge` — Not a pop-up channel (1+ year)** · group Pop-up channels · rethresholded from `minAge`
- Options: off (default) / on.
- Definition: `monthsAtPublish = (publishedEst(v) − Date.parse(yt.channelJoined)) / (30.44 d)`; on → angles with `< 12` fold as "channel was N months old when this was posted — not a credibility signal" (N in days when under 2 months); ORIGINAL episodes badge only. The 1-year line is a heuristic and the tooltip says so; no "separates farms" claim anywhere.
- Data: yt.channelJoined (84/87), published. Kept under 1 yr at publish: collapse 2QbG7uwtZb0 (Extraordinary Explained, 14 days) and DCtZrR6vfxk (BEAWARE, 9 days); crypto es5Dw6yDc8o (Tokenly Crypto, 34 days) and CqX7sirvtO8 (The Bitcoin Libertarian, 330 days, ORIGINAL → badge); psi 7cwzQmYevu8 (The Kingdom Files, 360 days). 4 angles fold, 1 episode badged.
- Missing data: `channelJoined` null or `publishedEst` null → `{unknown:"channel age"}`, folded on its own line "1 folded: channel age not on file", never a strike.
- Trap: 6.

**`track` — Speaker is on the ledger** · group Ledger · renamed · rendered only when predictions.json exists
- Options: off (default) / on. Tooltip: "At least one entry on the public prediction ledger — recorded, not necessarily graded. The chip on the card shows the counts."
- Definition: unchanged test `x.recs.length > 0` (`recordFor` via claims.json predictor → `nameKey` → predictions entries). Non-matches fold as "speaker not on the ledger" — never "clean".
- Data: Collapse Audit keeps 1 of 25 (Bu0xNDLNORU; the ledger holds only Ray Dalio, 12 entries) and folds 6 of 7 episodes — the honest state of that ledger; crypto keeps 14 of 25 (10 of 13 episodes). Three kept crypto videos never attach because of name strings ("Gerhard - Bitcoin Strategy" ×2, "Armstrong & Fink"); see §9.
- Missing data: no claims.json speaker for the video → folds as above.
- Trap: 7, 12 (the only credibility signal the product allows).

**`speaker` — Speaker** · group Ledger · moved, unchanged
- Options: any / one per `nameKey`, as today.
- Definition: unchanged membership on `x.speakers`. Non-matches fold as "other speakers".
- Data: claims.json sources. Missing: uncited videos fold.
- Trap: navigation for 9.

**`paid` — Paid promotion (YouTube's flag)** · group YouTube facts · moved
- Options: any (default) / no disclosure ticked / disclosure ticked. Tooltip: "Set by the creator. 20 of 87 ticked it — 7 of 21 originals and 0 of the 22 videos we removed. Undisclosed is not the same as unsponsored."
- Definition: unchanged tests on `yt.paidPromotion`; folds as "creator ticked paid promotion" / "no disclosure ticked". Never part of a preset; never labelled "sponsored fear".
- Missing data: `yt.channelId == null` → unknown.
- Trap: none closed; kept as a fact filter with the `$ paid promotion` badge on the card.

### Always rendered

**`showRemoved` — Removed by our verdict (n)** · not a control
- A `<details class="lowreach">` at the bottom of the listing (after the "before the first original" bucket), collapsed by default, present in every preset including Everything, and present with "0 removed by our verdict" where nothing was removed so its absence is not read as a verdict.
- Each row: verdict (RECYCLED / CLICKBAIT), title as a link, channel, published date, our `verdict_note` with the `[…]` prefix stripped, and a visible tag "metadata-only verdict" when `verdictBasis(v) === "metadata"` (6 of 22: collapse 2, crypto 3, the-2026-setup 1 — the input's "7 of 22" did not reproduce). Rows ordered by published date; no view counts; no thumbnails.
- Data: videos.json verdict, verdict_note (our own analysis; safe to publish). Collapse 14, crypto 7, the-2026-setup 1.
- Trap: rule 4 (fold, never delete); 3 and 9 become checkable.

**Showing line** (`#sf-showing`): `Showing E of E episodes · A of A' angles (n folded: reason, n folded: reason…) · R removed by our verdict · U YouTube page unavailable`, plus the reset button when SF differs from the active preset.

---

## 6. New filters and tags — exact definitions and offline work

### 6.1 `TITLE_LEXICON_V1` (client-side, published in index.html as our own analysis)

```js
const TITLE_LEXICON_V1 = {
  version: 1,
  crisis: /\b(warn(?:s|ed|ing)?|collaps(?:e|es|ed|ing)|crash(?:es|ing|ed)?|bubble|burst|crisis|terrif(?:ied|ying)|chilling|shock(?:ing)?|panic(?:king)?|survive|protect|last chance|final|massive|exposes|hidden|domino|prophecy|doom)\b/i,
  now: /\b(just|now|already|about to|soon|last chance|prepare now|immediately)\b/i,
  acronyms: new Set(["AI","CIA","BTC","CEO","ETH","SUI","ADA","MSTR","GPT","STRC","SRS","AMD","USA","INC","AMA","ETF","FED","GDP","SEC","NYT","CNBC"]),
};
const isCrisisNow = t => TITLE_LEXICON_V1.crisis.test(t) && TITLE_LEXICON_V1.now.test(t);
const isShouty = t => (t.match(/[A-Za-z]{3,}/g) || []).filter(w => w === w.toUpperCase() && !TITLE_LEXICON_V1.acronyms.has(w)).length >= 3
                   || (t.match(/!/g) || []).length >= 2;
```
Badges cite the version: "crisis-now title (lexicon v1)". The acronym list must grow with new tickers and model names; a missed acronym raises a false shout, which is why the threshold is 3 and never 1–2. Re-run the 0-ORIGINAL check whenever the lexicon changes.

### 6.2 `horizon_dated` (offline, deterministic, no model call)

New script `scripts/mark-horizons.mjs`, run after any claims extraction. For each entry in `corpus/<topic>/claims-extracted.json` write `horizon_dated: true|false` and `horizon_rule: "v1"`:

```js
const MONTH = "jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?";
const HORIZON_DATED_V1 = new RegExp(
  `(20\\d\\d|\\b(?:${MONTH})\\b|\\bQ[1-4]\\b|\\bH[12]\\b` +
  `|\\b(?:next|within|in|over the next)\\s?\\d+(?:-\\d+)?\\s?(?:day|week|month|year|decade)s?\\b` +
  `|\\b\\d+-\\d+\\s?(?:days|weeks|months|years)\\b|\\bnext (?:week|month|quarter|year)\\b)`, "i");
```
Bare "next"/"within" are deliberately excluded. Month abbreviations carry word boundaries so "market" does not match "mar". Verified against the 58 horizons: dated = collapse 15 of 17, crypto 24 of 41; vague strings are exactly: "unspecified (no stated date)", "coming months", "next couple of years", "current / late-stage (no explicit date)", "coming weeks to months", "next weeks", "a few months", "current bottoming area (next few months)", "long term (no date)", "unspecified (cyclical)", "this technology revolution (no date)", "next bull cycle, no date stated", "long-term, no date stated", "no date stated ('not too distant future')", "next bull market", "upcoming rule implementation", "this cycle", "next bull leg", "next cycle". Kept: "next 12-18 months", "within 5 years", "2-3 years (into 2029)", "September 1 PMI print", "5-10 years".

`loadTopicData` gains `try { entry.claimsExtracted = await getJSON(\`corpus/${id}/claims-extracted.json\`); } catch (e) {}` (the app does not load this file today). The view never regexes horizons; it reads the stored boolean.

### 6.3 Side (camp) — client-side from claims.json, already loaded
Per video: `camps[videoId] = [{claimId, k, n, position}]` built beside `videoClaims`. Control rendering and "the other side" per §5. `arrivedFrom` is set in `runLookup()` from `parseVideoId(raw)` and by a click handler on `.card`.

### 6.4 Removed fold — client-side from videos.json (§5).

### 6.5 Channel age at publish — client-side (§5). `channelAgeYears` (age now) is deleted with `maxRate`.

### 6.6 Card tags (all computed client-side)
- `basisMark`: "✓ transcript read" / "◌ not yet read" (UNREVIEWED: "◌ not yet reviewed").
- Ledger chip, status-partitioned so nothing is counted twice: `held` SUPPORTED · `refuted` REFUTED · `ambiguous` AMBIGUOUS · `moved` UPDATED · `pending` PENDING with `due.end` · `no date` PENDING without `due.end`. `speakerRecords` replaces the single `open` counter with `pendingDated`/`pendingUndated`. Example: "Ray Dalio · 0 held · 2 refuted · 3 ambiguous · 2 moved · 2 pending · 3 no date" (sums to 12). Single-entry speakers: "Gerhard · 1 pending · no date". No rate on any Series card even when the docket marks a rate publishable (Dalio: `rate_publishable: true`) — rates belong to the ledger page, cards show counts.
- "side k of n: <position>" for videos cited under a ≥2-camp claim.
- "crisis-now title" / "shouty title" (lexicon v1) on every flagged card, folded or not.
- "channel was N months old when this was posted" when under 12 months at publish.
- "extracted, not adjudicated: 3 claims · 3 dated" / "1 claim · no date stated" when `claimsExtracted` covers the video; "claims not extracted" only while `deadline` is active.
- "YouTube page unavailable at last check (2026-09-13)" when `yt.channelId == null`; date from `yt.enrichedOn`.
- "metadata-only verdict" inside the removed fold.

### 6.7 Fold mechanics in `renderSeries`
- `seriesPass(x, ctx)` → `null | {fold} | {unknown}`. Episode loop: if fold/unknown, emit `<details class="fold">` in place with the episode number and reason; else emit the card. Inside each episode, `angles.map(seriesPass)` grouped by reason into one summary line: "3 angles folded: crisis-now title (2), not yet reviewed (1) — show". Remove `isLow`, `low`, `hid`, `lowCount`, `hidCount`, and the `views` sort branch.
- Preset chips: `SF_PRESETS = { bait: {titleBait:"both"}, read: {titleBait:"both", basis:true, channelAge:true}, deadline: {titleBait:"both", deadline:"some"}, everything: {titleBait:"any"} }`, each merged over `SF_DEFAULT` with the other keys at default; active chip = first preset deep-equal to SF ignoring `q` and `sort`, else "custom".

### 6.8 Data hygiene the spec depends on (edits to JSON, no fetch)
- Bump `SF_KEY` (§4).
- Collapse Audit `claims.json`: five predictor strings are theses, not people ("SPV/hidden-debt analysis", "gold/debt thesis", "silver pitch (recycled)", "yen-carry thesis", "Reventure (10-30% correction)" is a firm — acceptable) — replace with the speaker or drop the predictor field so the Speaker list stops offering them.
- `nameKey` alias map: `"gerhard - bitcoin strategy" → "gerhard"`, `"ark ($710k base 2030)" → "ark invest"`; today 2 kept Gerhard videos and the ARK video never attach to their ledger rows.
- Collapse `predictions.json` has no per-entry `predictor`; all 12 rows inherit the file-level "Ray Dalio". Correct today, wrong the day a second speaker is added to that file. Add `predictor` per entry.

---

## 7. Card signal strip

Order on every card (episode and angle), our signals first:
1. Verdict mark: "Episode 7" / angle under Episode 7 / "before the first original" — as today.
2. Basis mark: "✓ transcript read" or "◌ not yet read" / "◌ not yet reviewed".
3. Ledger chip (counts only, uncoloured, click sets `speaker`): "Ray Dalio · 0 held · 2 refuted · 3 ambiguous · 2 moved · 2 pending · 3 no date"; muted "not on the ledger" when the topic has a ledger and the speaker is not on it; nothing when the topic has no ledger.
4. Claim tags: "side 2 of 3: yen-carry unwind" when cited under a ≥2-camp claim; "extracted, not adjudicated: 3 claims · 3 dated" or "1 claim · no date stated" when claims were extracted.
5. Packaging tags (small, grey): "crisis-now title" / "shouty title"; "channel was N months old when posted"; "$ paid promotion (creator ticked)"; "live"; "YouTube page unavailable at last check (2026-09-13)".
6. Second line (grey): channel name · published date · our verdict note (episodes only, as today).

Hover on a single "details" glyph: views, likes, comments, chapters, captions (by creator / auto), YouTube category, channel country, channel since, output rate ("posts N+/day" when ≥365/yr).

Nowhere on the card: subscriber count, verified tick, breakout, above-channel-average, engagement %, comments per 100 likes, regions. These are popularity badges; rule 3 says popularity is never credibility, and a badge is a filter the viewer applies with their eyes.

Every fold line reads "N folded: <reason> — show"; every folded episode keeps its number; the listing ends with "N removed by our verdict — show".

---

## 8. Considered and rejected

Verified against the corpus and dropped. Each would have shipped a control that changes nothing on Collapse Audit, flags something a viewer would dispute, or reads size as truth.

| Proposal | Why rejected |
|---|---|
| `q` matching speaker names / camp positions | `ctx.speakers` comes from claims.json only; the claimed win ("Dalio" surfacing the DOAC Clips re-cut) fails — that re-cut carries Dalio only in claims-extracted.json, which the app does not load, and the other Dalio re-cuts are RECYCLED. Every match it would add is already one pick away in `speaker`; thesis-strings ("yen-carry thesis") would appear as phantom speaker hits. |
| `sort` = "next test first" | On Collapse Audit 1 of 12 ledger entries links by videoId and its `due.end` is null; the nameKey fallback would lend the two Dalio videos a 2028 date from a different claim made elsewhere. Result: 2 videos on top with a borrowed date, 23 "no test date" — and that label conflates unlinked, unscorable and unmigrated. Works only on crypto (11 of 14 dated). |
| `repeats` (near-identical / one per channel per week / per series) | Folds exactly 0 videos on Collapse Audit (its only multi-video kept channel is Tom Bilyeu ×2, Jaccard 0.00, one ORIGINAL). Corpus-wide the default folds 2 WorldofAI reviews of three different model releases — a fold a viewer would dispute, and keep-earliest surfaces the stalest. Crypto Nutshell's template does not survive upstream removal. |
| `strikes` (channel record here) | Effect at the default threshold: 0 folds on Collapse Audit (DOAC Clips' survivor is ORIGINAL → badge only; The Vision Journal has no survivor); 1 fold corpus-wide (Crypto Nutshell's DERIVATIVE survivor). The "4 of 5" figure counts 2 metadata-basis verdicts the definition excludes; honest badge is "2 of 5". A weaker channel prior second-guessing a transcript-read per-video verdict. Revisit when a corpus has a channel with ≥2 removed and ≥1 survivor. |
| `paid` "pitch found by our review" row + "No sponsored fear" preset | relations.json cites 3 videos (2 kept) by hand, one topic. The preset folds 7 of 21 originals for ticking the disclosure box while 0 of 22 removed videos ticked it — it punishes disclosers and teaches the wrong signal. The verdict_note regex hits CNBC "on-record claims". `paid` survives only as a drawer fact filter. |
| `ledgerStatus` (on the clock / awaiting ruling / ruled / never testable / no row) | Collapse `predictions.json` has no per-entry predictor and 1 of 12 rows carries a videoId; the "on the clock" rows attach to no collapse video or, via speaker, to a video that does not contain those claims. Every option resolves to the same 0–1 video that `track` already keeps. Only earns its options on crypto. The status split survives as the card chip. |
| `claim` relabel ("contested · 3 camps" / "everyone here agrees · N videos") | Counts include removed videos (imminent-debt-crisis 5 cited, 4 kept; hard-assets-hedge 4, 2 kept); a count of agreeing videos is social proof — the size-as-truth rule 3 forbids; membership by claim narrows to a one-camp loop by construction. |
| `claimType` + "Both sides" preset | Collapse Audit's only contested claim ("what triggers the crisis") has three camps that all predict collapse; a preset built on `type === "contested"` would label unanimity as balance. Housing's contested claim has one camp. No field records camp polarity. |
| `episodesOnly` | A no-op: angles already render inside a closed `<details class="angles">`; the before-first-original bucket is already closed; 0-ORIGINAL topics already show the empty state. Also "under its episode" overstates a purely date-order attachment. |
| `watched` (hide watched) | Nothing on disk; starts empty for every viewer; the app cannot observe watching, only a click; "N watched — 17 left" is the completion-progress pattern that drives bingeing. |
| `season` select | One option (S6, 25) on Collapse Audit; a date split on crypto; absent elsewhere; stamps a mechanism on videos that do not argue it. Headers stay. |
| `published` (last 30/90 days, this year, per-year) | "Last 30 days" empties every topic against a snapshot corpus (first_seen 2026-08-06..09-14); every other option keeps all 24 dated Collapse Audit videos — identical to From/To. The "surfaced N days after posting" badge reads our crawl date as YouTube surfacing (all 4 psi hits share first_seen 2026-08-09). |
| `length` rebucketing | See §2. |
| `live` as "Live crash streams" | See §2. |
| `channel` re-keyed on channelId with a hide mode | Folds at most 2 of 25 cards on Collapse Audit ("David Lin 4" counted removed videos). |
| `speaker` labels with ledger counts | "4 ruled · 2 moved · 2 on the clock · 6 cannot be scored" sums to 14 on a 12-entry ledger (UPDATED+unscorable counted twice); "1 claim, dated" is false for Gerhard and Saylor. The status-partitioned chip replaces it. |
| `dials` (indicators cited) | indicators.json tracks the 2026-08-13 extraction batch, not content: uncited kept videos include Rick Rule's credit-collapse interview (ORIGINAL, transcript full of figures) and a title that literally names "$250,000 by end of 2026". "Cites 1+" would fold 7 of 25 collapse and 11 of 25 crypto kept, mostly never-extracted. Zero cannot be made to mean zero without a new extraction pass. |
| `minViews` at any default; `verified`; `minSubs`; `minEng`; `minDisc`; `breakout`; `aboveAvg`; `maxRate`; `chaptered`; `captions`; `category`; `country`; `language`; `from`/`to`; `minAge` 3/5/10; "most viewed" order | See §2. |
| aiNarrated / faceless label | Only derivable by regex on verdict_note; negation breaks it ("not a re-cut" matched two originals); 9 of 10 hits are already removed. Needs a `verdict_tags` field emitted by `scripts/review-verdicts.mjs`. |
| undisclosedPromo label | Needs an offline pass over the 67 local transcripts (model or human); note regex too noisy. |
| thumbnailShock | No thumbnail bytes on disk. |
| selfCites (offline transcript regex) | Host and guest inseparable; 20 videos have no transcript. |
| twinTitle across channels | 2 pairs in 87; lower thresholds surface the corpus query words. Badge at most; not built now. |
| datedTitle badge | 3 of the 10 hits are originals; harmless as a badge but duplicates the `deadline` tag. |
| reissued (title year later than publish year) | Flags Martin Armstrong's "Collapse in 2032" ORIGINAL forecast. |
| provenance / story-age series-head line | Constant within a series; not a filter. podcast-evidence.json stores third-party episode titles and must be trimmed to guid/date/count before any public use. Out of scope for the bar. |

---

## 9. Honest limits

What a cautious viewer still cannot filter with today's data, and the cheapest way to get it:

1. **Sponsored fear.** YouTube's flag catches ad-read podcasts (20 ticked; 0 of 22 removed videos). Undisclosed gold/silver/course pitches are known for 3 videos by hand. Cheapest: a `pitch: true|false` boolean set in `scripts/review-verdicts.mjs` at review time — the reviewer already has the transcript open; store the boolean only. No fetch; human minutes per video.
2. **Crisis-farm channels before they earn a strike.** Only `channelAge` (4 angles) and the upstream CLICKBAIT verdicts. Channel-level history needs the channel's upload list (a fetch). Cheapest on disk: revisit `strikes` when any corpus has a channel with ≥2 removed and ≥1 survivor beyond the single case today.
3. **Predictions that never resolve, outside two topics.** Housing, open-vs-closed, psi, the-2026-setup have no ledger and no extracted claims; `deadline` and `track` do not render there. Cheapest: run the claims extraction over those transcripts (offline model or human pass), storing only claim text, horizon and `horizon_dated`.
4. **Coverage inside Collapse Audit.** 9 of 25 kept videos have extracted claims; 16 pass `deadline` on "claims not extracted". Cheapest: extraction over the remaining transcripts on disk (offline pass).
5. **Ledger rows tied to the video that made the claim.** 1 of 12 collapse entries carries a videoId; no per-entry predictor. Cheapest: add `predictor` and `source_video` to each entry at capture (edit predictions.json; `scripts/resolver.mjs` can validate).
6. **Speaker aliasing.** "Gerhard - Bitcoin Strategy" (2 kept videos), "Armstrong & Fink" (1), "ARK ($710K base 2030)" never reach their ledger rows; five collapse "speakers" are theses. Cheapest: edit claims.json strings and add the alias map (§6.8).
7. **Stale footage sold as new, per video.** No signal survives (title-year flags forecasts; first_seen is our crawl). Cheapest: `reissue_of: <videoId>` set at review time when a re-cut is identified.
8. **AI-narrated / faceless / title-over-promises.** Regex on notes: 10 / 9 hits, mostly removed already. Cheapest: `verdict_tags` emitted by `review-verdicts.mjs`; backfill by regex once, hand-check negations.
9. **Camp polarity.** No field says whether a camp is for or against the conclusion; on Collapse Audit all three camps predict collapse. Cheapest: a hand-set `stance: for|against|mechanism` per camp on the 4 contested claims.
10. **Shock thumbnails.** Needs a fetch and a classifier. Not planned.
11. **Blank length on 17 videos** (100% of three corpora) and **3 hollow `yt` blocks.** The next `scripts/enrich_youtube.py` run can write `lengthSeconds` and re-check the 3 pages (a fetch already scheduled); until then the tag says "unavailable at last check", never "removed".
12. **Live crash streams.** None on disk; the 3 live videos are primary sources. Nothing to filter until one appears.
13. **A stopping point.** The finish line is the numbered episode list and the visible removed fold; there is no per-viewer state, by design.