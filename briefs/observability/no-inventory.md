> **Note on the scale figures in the brief.** Actual repo state at `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar` (HEAD = `c15fec4`, last commit 2026-08-15, last *corpus* change 2026-08-13):
> **86 videos** across **6** corpus directories (not ~110). `watchlist.json` lists **7** topics — `loop-engineering` is `queued` and has **no corpus directory at all**, so the gallery renders a tile with zero data behind it.

---

# LENS 1 — Repo Inventory and Data-Readiness Audit

## Part 0 — Ground truth: what is actually in the repo

| topic | videos | verdict mix | age_days | views parseable | transcripts | ledger | claims | relations | indicators |
|---|---|---|---|---|---|---|---|---|---|
| `collapse-audit` | 38 | O7 D15 R7 C6 U3 | 34/38 | 33/38 | 31/38 | 12 | 4 | 7 | 14 |
| `crypto-winter-watch` | 32 | O13 D12 R1 C6 | 18/32 | 18/32 | 18/32 | 14 | 8 | — | 14 |
| `psi-declassified` | 6 | O1 D4 U1 | **0/6** | **0/6** | 0/6 | — | 1 | — | — |
| `open-vs-closed-ai-race` | 6 | D5 U1 | **0/6** | **0/6** | 0/6 | — | 1 | — | — |
| `housing-crash-watch` | 3 | D3 | **0/3** | **0/3** | 0/3 | — | 1 | — | — |
| `the-2026-setup` | 1 | C1 | **0/1** | **0/1** | 0/1 | — | — | — | — |
| `loop-engineering` | **0** | — | — | — | — | — | — | — | — |
| **TOTAL** | **86** | | **52/86** | **51/86** | **49/86** | **26** | **16** | **7** | **28** |

Ledger status counts: `collapse-audit` = REFUTED 2, UPDATED 2, AMBIGUOUS 3, PENDING 5. `crypto-winter-watch` = PENDING 14, everything else 0. **Zero SUPPORTED entries exist anywhere in the repo.** Two narratives carry a ledger; five carry none.

What the receipt strip actually renders today (reproduced by running `computeReceipt`'s logic against the files):

| topic | headline age | score cell | reheat % | next test | source spread |
|---|---|---|---|---|---|
| `collapse-audit` | 11 yrs | `2 / 7 dated calls resolved` (gate blocked) | 40% | 686d | 34ch, top3 = 18% |
| `crypto-winter-watch` | 8 yrs | `0 / 14` | 20% | 13d | 23ch, top3 = 31% |
| `psi-declassified` | 31 yrs | — | — | none dated | gated off (<10 videos) |
| `open-vs-closed-ai-race` | 3 yrs | — | — | none dated | gated off |
| `housing-crash-watch` | 6 yrs | — | — | none dated | gated off |
| `the-2026-setup` | 1 yr | — | — | none dated | gated off |
| `loop-engineering` | — | — | — | none | — |

**Five of seven tiles have exactly one live number on them: a model-estimated age.** The observability product, as data stands, has one narrative with a full instrument panel, one with half of one, and five that are placeholders.

---

## Part 1 — Feature-by-feature disposition

Layer key: **A** = Attention, **S** = Structure, **C** = Accountability, **—** = infrastructure/no layer.

### Accountability layer (the moat — the strongest data in the repo)

| Feature | Where | Disposition | Layer | Reason |
|---|---|---|---|---|
| **Prediction ledger** (`predictions.json`, `renderLedger` `index.html:1436`) | 26 entries, 2 topics | **PROMOTE** | **C** | The only asset in the repo a funded competitor cannot buy. It is currently a *tab* behind the corpus tab. It should be the terminal's spine. |
| **Ledger `status` vocabulary** (PENDING/SUPPORTED/REFUTED/UPDATED/AMBIGUOUS) | `predictions.json` schema | **KEEP AS IS** | **C** | UPDATED is the single most defensible field in the product (deadline-roll = deleted-content moat). Do not touch the vocabulary. |
| **`computeReceipt` score gate** (`index.html:729–762`, `SCORE_GATE=5` `:716`) | — | **REBUILD** | **C** | `resolved = sup + ref` (`:756`) is the verified defect. `collapse-audit` has 7 gradeable outcomes (2 REFUTED + 2 UPDATED + 3 AMBIGUOUS) and renders "2 / 7 — too few to score fairly." The gate is blocked on the *only* narrative that has ever resolved anything. |
| **Receipt strip / headline numbers** (`orientationHtml` `:1021–1061`) | — | **PROMOTE + REBUILD** | **C/A** | Right conception, wrong contents. Today it is 3–5 numbers of which one (age) is a model guess and one ("next test") is fragile — see `parseHorizonDate` below. This becomes the terminal's top rail. |
| **`parseHorizonDate`** (`:722–727`) | — | **REBUILD** | **C** | Takes the *first* 4-digit year in free text. `"by ~2026-2028"` → 2026-07-01, which sits exactly on the 45-day grace boundary at `:743`; `collapse-audit`'s "next test" flips between *due now* and *686d* with no data change. Horizons must be stored as structured `{due_start, due_end, precision}`, not re-parsed from prose on every render. |
| **Overdue-PENDING drift** | `predictions.json` | **REBUILD (process)** | **C** | `dalio-2025-heart-attack` (horizon "by ~2026-2028") is past its parsed date and still PENDING. Nothing in the system ever wakes up and asks "did this land?" A ledger with no resolver is a to-do list. |
| **Genesis / trace-origin** (`traceOrigin` `:1633`, `netlify/functions/trace-origin.mjs`) | 0 narratives traced | **DEMOTE** | **C** | Zero `narrative.json` files carry a `genesis` key. It costs $1–2 of X API per press, and its phrase suggestion depends on `claims.fingerprints`, which **does not exist in any `claims.json` in the repo** (verified: 5/5 files have no `fingerprints` key). It falls back to a name-derived string every time. Keep the code, take the button off the main surface. |

### Structure layer

| Feature | Where | Disposition | Layer | Reason |
|---|---|---|---|---|
| **Verdict labels** (ORIGINAL/DERIVATIVE/RECYCLED/CLICKBAIT/UNREVIEWED) | `videos.json`, `VERDICTS` `:646` | **KEEP AS IS + REFRAME** | **S** | Solid, hand-audited on 49 transcripts. Reframe the *word*: these are **novelty classes**, not quality grades. "RECYCLED share of the last 20" is the novelty instrument; label it that way. |
| **Mutation timeline** (`narrative.mutations`, `timelineHtml` `:1195`) | 6 mutations × 2 narratives | **PROMOTE** | **S** | Second-strongest asset after the ledger, and currently collapsed behind a disclosure button (`:1148`). Mechanism rotation is exactly what "narrative observability" means. |
| **Claims + contested camps** (`claims.json`, `:1315–1354`) | 16 claims, 5 contested | **KEEP AS IS** | **S** | The tug-of-war render is the best contestation instrument in the app. Thin (16 claims across 6 topics) but structurally right. |
| **360 map / relations** (`relations.json`, `render360Svg` `:901`, `map360.mjs`) | 1 narrative, 7 edges | **DEMOTE → REBUILD** | **S** | **Verified worse than the brief states.** Of 7 edges: 4 have `evidence.videoIds: []`, 1 has 2 videos/2 channels, and only **2 of 7 pass the project's own ≥3-videos/≥2-channels gate.** `minted_by: "hand-seeded"` — this map was never produced by the engine. Zero `counters` edges anywhere. It is a research artifact wearing a product's clothes. |
| **Indicators on watch** (`indicators.json`, `indicatorsHtml` `:850`) | 28 dials, 2 narratives | **PROMOTE** | **S→C** | The best-evidenced structure in the repo: avg 7.3 / 4.1 videoIds per dial, read from 31 and 18 transcripts, 23/28 carry `contested_note`, roles are already trigger/countdown/evidence/counter-evidence. This is the natural bridge from Structure into Accountability — a `countdown` dial *is* a clock. Currently buried inside "Deep analytics" (`:1361`). |
| **Radar Read** (`buildRadarRead` `:798–842`) | — | **KEEP AS IS + REFRAME** | **S** | Deterministic, no model call, every clause traceable to stored data. This is the SpotGamma "here is what the positioning shows" line and it already exists. Rename it the *structural read*, and it inherits every `computeReceipt` fix for free. |
| **Three-level explanations** (`narrative.explanations`, `:1269–1275`) | 2 narratives complete | **DEMOTE** | **S** | Free-text prose that drifts from the arrays it describes. **Verified drift:** `crypto-winter-watch` expert text says *"12/18 original verdicts"*; stored data is 13 ORIGINAL of **32** videos (18 was the transcript count at authoring time). Any hand-written number in prose is a future lie. Derive or delete. |
| **`claims-extracted.json`** | 2 topics, orphaned | **REMOVE** | — | Written by `merge_verdicts.py`, read by nothing in `index.html`. Dead intermediate. |

### Attention layer

| Feature | Where | Disposition | Layer | Reason |
|---|---|---|---|---|
| **Source spread** (`computeReceipt` `:750–759`) | 2 topics pass the ≥10 gate | **PROMOTE + REFRAME** | **A** | This is *concentration*, the one genuine attention metric already computed. 34 channels / top-3 = 18% is a real, defensible reading. Name it concentration and put it on the rail. |
| **Corpus composition bar chart** (`vbreak` `:1256`) | — | **COMBINE** | **A/S** | Same data as the verdict mix, rendered twice (once as chips at `:1244`, once as bars). Merge into one novelty-mix instrument. |
| **Predictor breakdown chart** (`:1277–1307`) | — | **KEEP AS IS** | **A/C** | Cheap, derived from `claims.sources` + ledger, and it is the "who is driving this" question. Natural feeder into per-predictor accountability scores later. |
| **Corpus list / video table** (`renderCorpus` `:1392`) | — | **DEMOTE** | **A** | 86 rows of YouTube links is the *evidence drawer*, not a view. It is currently the default tab (`:585`). Terminals do not open on the raw log. |
| **Heat / velocity / breadth** | — | **DOES NOT EXIST** | **A** | See Part 2. There is no time series of any kind in this repo. |

### Shell, engine and workflow

| Feature | Where | Disposition | Layer | Reason |
|---|---|---|---|---|
| **Gallery** (`renderGallery` `:1835`, `fillGalleryStats` `:1865`) | — | **KEEP AS IS + REBUILD tiles** | — | Grid + keyword + industry filter is right. The *tiles* are the problem: 5 of 7 show only a model-guessed age. Tiles should carry the three-layer strip once the data exists. |
| **Industry filter** (`renderGalleryFilters` `:1817`) | — | **REBUILD (schema bug)** | — | `watchlist.json` uses `industry`; `candidates.json` (33 entries) uses **`beat`**. Verified: all 33 candidates read `industry = None`. Shadow candidates can never appear under any industry. One-word fix, but it silently caps the gallery at 7. |
| **Paste-a-link** (`runLookup` `:1887`, `analyze.mjs`) | 17 of 86 videos | **KEEP AS IS + REBUILD writer** | — | The founding loop works and is the acquisition surface. But its writer (`analyze.mjs:149–158`) is the reason 34 videos have no time data at all — see Part 2. |
| **Refresh / buildout** (`refreshNarrative` `:1708`, `sweep.mjs`) | — | **KEEP AS IS + REBUILD writer** | — | Same problem: `sweep.mjs:28` extracts *only* `videoId` from search HTML that already contains `viewCountText` and `publishedTimeText`. It throws away the exact fields the Attention layer needs. |
| **Follow** (`FOLLOW_KEY` `:1547`, `renderYours` `:1555`) | localStorage array | **PROMOTE** | — | The only per-user state that exists, and it is the natural anchor for "change since your last visit" — the killer feature of an observability terminal. Today it stores IDs only; it needs a `lastSeen` timestamp per topic. Note `renderYours:1566` already tries `age_days <= 2` for "new in the last 48h" — which returns 0 for 34 of 86 videos because `age_days` is null. |
| **Watchlist** (`watchlist.json`) | 7 topics | **KEEP AS IS** | — | Correct as the topic registry. Remove or hide `loop-engineering` until it has a corpus. |
| **Candidates** (`candidates.json`) | 33 shadows | **PROMOTE** | **S** | 33 researched shadow narratives is a real backlog and the supply side of the 360 map. Rename `beat` → `industry`, then surface as ghost tiles in the gallery. |
| **Briefs** (`briefs/`, `renderBriefs` `:1497`) | 4 dated + 16 research | **DEMOTE** | — | `briefs/index.json` lists **1 of 4** dated briefs, so the tab shows almost nothing. The 16 research files (360-research/, portable-thesis/) are not indexed at all. Move to internal docs; a terminal does not ship its own design memos as a tab. |
| **Prototypes** (`prototypes/*.html`, 1.4MB PNG) | 4 files | **REMOVE from repo root** | — | 1.5MB of 3D design experiments shipped to GitHub Pages on every deploy. Archive to a branch. |
| **`collector.py`** | last effective run 2026-08-08 | **PROMOTE + REBUILD** | **A** | This is the *only* code path in the whole system that ever captured `published` or `views`. It has not been run in a week. It is the foundation of the Attention layer and it is currently the least-used file in the repo. |
| **`merge_verdicts.py`, `serve.cjs`** | — | **KEEP AS IS** | — | Working local tooling. |
| **Cloudflare port** (`cloudflare/worker.mjs`) | 4 routes | **KEEP AS IS (note gap)** | — | Routes `analyze`/`sweep`/`consolidate`/`trace-origin`. **No `/api/map360` route** — the 360 engine is Netlify-only, so the Cloudflare fallback silently loses a feature. |
| **`claims.fingerprints`** | minted at `consolidate.mjs:165`, read at `:1635` and `:1830` | **REMOVE or REPAIR** | — | Written by the engine, read in two places, **present in zero files**. Dead path in production. |

---

## Part 2 — Data readiness audit for time-series metrics

### The one-sentence answer

**There is no time series in this repository.** Not a partial one, not a degraded one — zero. Every quantity that could move over time is stored as a single string captured once, and no process anywhere re-observes it.

### Verified specifics, one by one

**Q: Is `published` a relative scrape-time string?**
**Yes, and it is worse than that.** `collector.py:98` stores `text_of(vr.get("publishedTimeText"))` verbatim: `"1 hour ago"`, `"4 hours ago"`, `"Streamed 2 days ago"`. These strings are frozen at first capture and **never rewritten** — `collect_topic` (`:170–173`) computes `age_days` on the *newly found* dict, then `continue`s past any video already in `known`. The stored record is never touched again. So a video whose record says `"1 hour ago"` was published on 2026-08-06 and the file still says "1 hour ago" today, nine days later. `renderCorpus:1420` prints that string directly to the user.

For the 34 videos created by the Netlify path, `published` is the **empty string** (`analyze.mjs:152`).

**Q: Is `views` a display string captured once with no `scraped_at`?**
**Yes, confirmed by git.** Values are `"2,768 views"`, `"No views"`, `""`. `viewsNum` (`:707`) regexes digits out at render time. There is no `scraped_at`, no `views_n`, no second observation. Proof from history:

```
git log -p --all -- 'corpus/*/videos.json' | grep -c '^-.*"views"'   →  0
git log -p --all -- 'corpus/*/videos.json' | grep -c '^+.*"views"'   →  86
```

**86 view-count lines added, 0 ever removed.** Every commit touching a `videos.json` is a pure append (`--numstat` shows `15 0`, `15 0`, `15 0`…). No view count in this repo has ever been updated. Velocity is not degraded — it is undefined.

**Q: Does `first_seen` exist on every video?**
**Yes — 86/86.** It is the single reliable timestamp in the system. But it is day-granularity and it clusters at narrative creation, not at discovery:

- `collapse-audit`: 33 on 2026-08-06, 4 on 08-07, 1 on 08-08
- `crypto-winter-watch`: 25 on 08-07, 7 on 08-08
- `psi-declassified`: 6 on 08-09 · `open-vs-closed-ai-race`: 6 on 08-13 · `housing-crash-watch`: 3 on 08-08 · `the-2026-setup`: 1 on 08-07

`first_seen` measures *when Malik founded the narrative*, not when attention arrived. It supports "corpus growth" for exactly the two days each narrative was being built and then flatlines.

**Q: Is there any daily snapshot anywhere?**
**No.** No `snapshots/`, no `history/`, no `.jsonl`. `netlify.toml` declares no scheduled functions. `.github/workflows/` contains one file, `pages.yml`, triggered on `push` and `workflow_dispatch` — **no `schedule:` block anywhere in the repo.** Nothing runs on a clock. Every byte of data in this repo was written by a human pressing a button.

**Q: What does `KEEP_DAYS` do to history?**
`collector.py:32` sets `KEEP_DAYS = 14`, enforced at `:172`: `if age is not None and age > KEEP_DAYS: continue`. Three consequences:

1. **No backfill, ever.** A video published 15 days ago is invisible even if it is the origin video of the narrative. The corpus can only ever contain what was found inside a 14-day trailing window at the moment someone ran the script.
2. **Silent history holes.** The collector last produced data on 2026-08-08. Its window has now fully expired. Everything published 2026-08-01 → today is unrecoverable by this tool.
3. **Sampling bias toward the young.** `search_youtube` sorts newest-first (`sp=CAI`), then the 14-day cut removes the tail. The corpus is structurally a sample of *recent* content, which biases the RECYCLED share and any future velocity metric upward.

**Q: Can git history serve as the time series?**
**No, not today — and this is the finding that matters most.** The repo *is* a versioned JSON store with dated engine commits, which sounds like a free time series. It is not, because the commits are **append-only for the fields that would move**. Verified above: 86 view additions, 0 modifications. Reconstructing `views(t)` from `git log -p` returns exactly one point per video — the same information `first_seen` already gives you.

Commit cadence also fails as a proxy for corpus activity: `collapse-audit/videos.json` has 7 commits on 3 distinct days (all 2026-08-06 → 08-08); `crypto-winter-watch/videos.json` has 14 commits on 2 days. Whole-repo commits by day: 5, 30, 22, 13, 4, 5, 2, 0, 21, 2 — this is a build log, not a heartbeat.

Git *becomes* a usable time series the moment a scheduled job rewrites values in place, because each rewrite is a diff with an authored timestamp. But even then I would not read it from the client: the site fetches static files from `raw.githubusercontent.com` (`RAW_BASE` `:675`), and reconstructing a series would require the commits API plus per-commit blob fetches — many round-trips, rate-limited, and unavailable to the existing `getJSON` path. **Store the series explicitly; let git version the store.**

### What today's data *can* honestly support

| Metric | Supported? | Basis |
|---|---|---|
| **Novelty (verdict mix)** | ✅ Yes | 49 hand-audited transcripts; strongest instrument in the repo |
| **Concentration (source spread)** | ✅ Yes | 34ch/18%, 23ch/31% — computed, gated at ≥10 videos |
| **Breadth (distinct channels)** | ✅ Yes, static | 34 and 23 channels — a level, never a trend |
| **Contestation** | ✅ Yes | 5 contested claims with camps; 23/28 indicators carry `contested_note` |
| **Mutation count / rotation** | ✅ Yes | 6 mutations × 2 narratives, dated |
| **Approximate publish date** | ⚠️ 52/86 | `publishedEst` `:717` = `first_seen − age_days` |
| **Ledger outcomes** | ⚠️ 26 entries, 0 SUPPORTED | And the gate that renders them is broken |
| **Heat (views now)** | ⚠️ 51/86, stale by 7–9 days | Single frozen observation |
| **Velocity (Δviews/Δt)** | ❌ **Impossible** | Requires two observations; the repo has exactly one, forever |
| **Novelty *over time*** | ❌ **Impossible** | No dated re-computation of the verdict mix |
| **Change since last visit** | ❌ **Impossible** | No per-user `lastSeen`, no dated corpus state to diff against |
| **Attention topology / spread between channels** | ❌ **Impossible** | No repeat observation of who posted when |

### The structural cause, named

The system has two writers and they disagree about what a video is.

- **`collector.py`** (`:93–102`) captures `published`, `views`, `length`, `age_days`. It produced 69 of 86 videos and **has not run since 2026-08-08**.
- **`analyze.mjs`** (`:149–158`) writes `published: "", views: "", length: "", age_days: null` — hardcoded empties, because it only has YouTube's oEmbed endpoint, which returns title and author and nothing else.
- **`sweep.mjs`** (`:28–31`) fetches the *full search-results HTML*, which contains `viewCountText` and `publishedTimeText`, and then extracts only `"videoRenderer":{"videoId":"..."}` with a regex. It has the data in memory and discards it.

**Every video added since 2026-08-09 came through the Netlify path.** That is why 5 of 7 narratives have zero temporal data. The product has been quietly running its worst data collector for the last week, and the metric layer the new proposal depends on is precisely the layer that path deletes.

---

## Part 3 — The minimum data model for heat / velocity / novelty / change-since-last-visit

Design constraints: no database, no new host, no credit burn, git stays the store, the client keeps reading static JSON from the raw CDN via the existing `getJSON`.

### Fix 0 — stop the bleeding (≈20 lines, do this first)

None of the below matters if the writers keep discarding time data.

1. **`sweep.mjs:28`** — change the regex to capture the sibling `viewCountText` / `publishedTimeText` already present in the HTML, and return `{videoId, published, views, length}` instead of bare IDs. `refreshNarrative:1751` then stops stamping `published: "just added", age_days: 0`.
2. **`analyze.mjs:149`** — accept those fields when the caller supplies them (the buildout path has them from step 1); keep the empty fallback only for a cold user paste.
3. Add `scraped_at` (ISO datetime) and numeric `views_n` to the video record in **both** writers and in `collector.py`.

### Fix 1 — the observation log (the actual new data)

**`corpus/<id>/observations.jsonl`** — append-only, one line per (video, observation day). JSONL specifically so every daily commit is a pure append and the git diff stays one line per video:

```jsonl
{"d":"2026-08-16","v":"UNYpubnQDC8","views":12403,"rank":3}
{"d":"2026-08-16","v":"6yir9VA3bKQ","views":88120,"rank":7}
```

- `d` — observation date (UTC day)
- `v` — videoId
- `views` — integer, parsed at capture, not at render
- `rank` — optional: position in the newest-first search result for the topic's queries (a free proxy for algorithmic push that costs nothing extra to record)

Size: 86 videos × ~55 bytes = **~5 KB/day, ~1.7 MB/year** across the whole corpus. Trivial for git, trivial for the CDN.

**Second observation lands ~24h after deployment. Velocity exists the day after that.**

### Fix 2 — the daily rollup (what the UI reads)

**`corpus/<id>/pulse.json`** — a capped array of daily rows, newest last, trimmed to 180 entries. The client reads one small file per narrative and never parses the JSONL:

```json
{
  "updated": "2026-08-16",
  "days": [
    {
      "d": "2026-08-16",
      "videos_total": 38,
      "new_24h": 2,
      "new_7d": 5,
      "views_total": 4183220,
      "views_delta_24h": 91400,
      "channels_7d": 6,
      "top3_share": 0.18,
      "verdict_mix": {"ORIGINAL":7,"DERIVATIVE":15,"RECYCLED":7,"CLICKBAIT":6,"UNREVIEWED":3},
      "reheat_share_20": 0.40,
      "pending": 5,
      "resolved": 7,
      "next_test_days": 686
    }
  ]
}
```

This single file yields the whole Attention layer plus change-detection:

| Metric | Derivation |
|---|---|
| **Heat** | `views_total` (level) |
| **Velocity** | `views_delta_24h`, or `days[-1] − days[-8]` for a 7-day slope |
| **Breadth** | `channels_7d` |
| **Concentration** | `top3_share` |
| **Novelty** | `new_7d / videos_total`, and `1 − reheat_share_20` |
| **Change since last visit** | client stores `lastSeen[topicId]`; diff `days[-1]` against the row nearest that date |
| **Accountability drift** | `pending` / `resolved` / `next_test_days` moving between rows *is* the deadline-roll signal, captured automatically |

**Follow becomes the anchor.** Change `FOLLOW_KEY` (`:1547`) from `["collapse-audit", …]` to `{"collapse-audit": {"lastSeen": "2026-08-14"}}`, and `renderYours` (`:1555`) stops guessing with `age_days <= 2` and starts reading a real diff. That single change turns a bookmark into a terminal.

### Fix 3 — who writes it, and when

**GitHub Actions cron, not Netlify.** Reasons: the repo is already the store and already deploys from Actions; `collector.py` needs no API key; Netlify scheduled functions burn build credits, and the existing convention (`[skip netlify]` on engine commits, commit `23873c9` "Stop credit burn") already establishes that data commits must not trigger builds.

**New file: `.github/workflows/pulse.yml`**

```yaml
on:
  schedule:
    - cron: "0 6 * * *"      # 06:00 UTC daily
  workflow_dispatch:
```

The job runs `python3 collector.py --observe` and commits with `[skip netlify]`. `--observe` is a new mode in `collector.py` that:

1. Runs each active topic's queries (same `search_youtube`, already written).
2. For **every** video seen — including ones already in `known`, which today's `:170–173` skips — appends an `observations.jsonl` line.
3. Rewrites `views_n`, `published_at` (absolute, computed once as `scraped_at − age_days`) and `scraped_at` on the stored record. **This also retro-repairs the 34 empty records** the moment any of those videos reappears in a search result.
4. Recomputes `pulse.json` for the topic and appends today's row.
5. Ingests genuinely new videos exactly as today.

`KEEP_DAYS` stays 14 for *ingestion* only. It must not gate *observation* — an 80-day-old video that is still accumulating views is the most interesting thing an attention terminal can show.

### Fix 4 — the accountability resolver (cheap, high value)

Same cron, second job, weekly: read every `predictions.json`, find PENDING entries whose structured `due_end` is past, and write them into **`corpus/<id>/due.json`** as a review queue. This does not auto-grade — auto-grading named people is precisely the legal-risk surface the prior research flagged. It produces a *worklist*. Today `dalio-2025-heart-attack` sits silently overdue with nothing surfacing it; the ledger's whole value is that someone comes back and closes the loop.

### What this does *not* solve, stated plainly

- **The first 9 days are gone.** Nothing recovers view history for 2026-08-06 → today. The series starts the day the cron does. This is unavoidable and is the strongest possible argument for shipping the cron *before* any UI work: **the moat is time-in-market, and the clock does not start until something is recording.**
- **The 34 Netlify-path videos** only self-heal if they resurface in a topic query. User-pasted videos from unrelated channels may never reappear; those records will keep `views: ""` permanently.
- **Views are a YouTube-supplied display string** at whatever granularity YouTube rounds to ("1.2M views"). Velocity below that granularity is noise. Parse to an integer and store the raw string too.
- **Five of seven narratives have essentially no corpus.** No data model fixes a 1-video narrative. The Attention layer will be honest and empty on `the-2026-setup`, `housing-crash-watch`, `psi-declassified`, `open-vs-closed-ai-race` until the collector runs against them with real queries — note that four of these were founded by paste-a-link and their `watchlist.json` queries have **never been swept by `collector.py` at all**.

---

## Files referenced

- `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/index.html` — `computeReceipt` :729, `publishedEst` :717, `parseHorizonDate` :722, `narrativeStats` :766, `buildRadarRead` :798, `indicatorsHtml` :850, `orientationHtml` :1021, `dashboardHtml` :1064, `renderNarrativeCard` :1235, `renderCorpus` :1392, `renderLedger` :1436, `follows/FOLLOW_KEY` :1547, `renderYours` :1555, `refreshNarrative` :1708, `renderGallery` :1835, `fillGalleryStats` :1865
- `.../narrative-radar/collector.py` — `KEEP_DAYS` :32, `age_days` :72, `search_youtube` fields :93–102, known-video skip :167–178
- `.../narrative-radar/netlify/functions/analyze.mjs` — `videoEntry` :149–158 (`published:"" views:"" age_days:null`)
- `.../narrative-radar/netlify/functions/sweep.mjs` — :28–31 (discards `viewCountText`/`publishedTimeText`)
- `.../narrative-radar/netlify/functions/consolidate.mjs` — fingerprint minting :165–167 (never persisted)
- `.../narrative-radar/.github/workflows/pages.yml` — the only workflow; no `schedule:`
- `.../narrative-radar/corpus/collapse-audit/relations.json` — `minted_by: "hand-seeded"`, 2 of 7 edges pass the evidence gate
- `.../narrative-radar/candidates.json` — 33 entries keyed `beat`, not `industry`
