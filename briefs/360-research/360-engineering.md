# 360 View — Engineering Spec (v0, minimal)

Grounded in the actual code at `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/` (files: `netlify/functions/analyze.mjs`, `consolidate.mjs`, `trace-origin.mjs`, `index.html`, `watchlist.json`, `corpus/collapse-audit/claims.json`, `briefs/2026-08-10-flagship-shelf-research.md`).

---

## 1. Data model — `corpus/<topic>/relations.json` (per-narrative, one new file)

**Decision: per-narrative file, not a global graph.json, not fields on claims.json.**

Why:
- It matches the existing per-topic layout exactly (`narrative.json`, `videos.json`, `predictions.json`, `claims.json`). `loadTopicData()` in `index.html` (line ~971) grows by one line.
- The 360 view of narrative X needs only X's own file — one raw-CDN fetch, zero joins.
- A global `graph.json` would be a hot file: every mint is a GitHub contents-API read-modify-write, and `analyze.mjs` already documents that parallel contents-API writes race on the branch ref (409). Per-topic files keep every engine commit scoped, same as today.
- `claims.json` is delta-merged by `consolidate.mjs`; mixing relation lifecycle into that merge logic is the opposite of minimal.

Relations are **stored from the perspective of the narrative that owns the file** (directed edges out of its question). When narrative B is later mapped it may independently mention A — that duplication is accepted in v0; each 360 view only ever renders one file, so no reconciliation is needed.

### Schema

```json
{
  "note": "The 360 map: the question this narrative competes to answer, and the rival/adjacent answers. Minted by /api/map360; shadows are untracked candidate tiles.",
  "updated": "2026-08-13",
  "minted_by": "map360",
  "question": {
    "text": "Is a debt-driven US economic collapse imminent?",
    "demand": "fear of losing savings; wanting to front-run a crash",
    "asked_since": "2008"
  },
  "relations": [
    {
      "type": "competes",
      "target": { "kind": "tracked", "topic_id": "the-2026-setup" },
      "label": "Same macro moment read as opportunity, not collapse",
      "evidence": { "videoIds": ["qbnuJFRcvQE"], "note": "Keen's AI-bubble strand overlaps both" },
      "confidence": "medium"
    },
    {
      "type": "shares_clock",
      "target": {
        "kind": "shadow",
        "shadow_id": "japan-carry-trade-doom",
        "name": "Japan Carry-Trade Doom",
        "claim_hint": "A yen-carry unwind forces global liquidation",
        "queries": ["japan carry trade unwind", "yen carry trade crisis 2026"]
      },
      "clock": { "trigger": "10yr Treasury yield sustained above 5%", "next_check": "2026-12" },
      "label": "Both narratives fire on the same rate trigger",
      "evidence": { "videoIds": ["YBhwK-VWsxY", "faiJCn20gv0"], "note": "yen-carry camp inside crisis-trigger claim" },
      "confidence": "high"
    },
    {
      "type": "mutates_into",
      "direction": "in",
      "target": { "kind": "shadow", "shadow_id": "peak-oil-doom", "name": "Peak Oil Doom", "claim_hint": "…", "queries": ["…"] },
      "label": "Earlier answer to the same collapse demand (2000s)",
      "evidence": { "videoIds": [], "note": "lineage claim, model-estimated, pending audit" },
      "confidence": "low"
    }
  ]
}
```

Field rules:
- `type`: `competes | supplements | feeds | shares_clock | mutates_into` (the v0 typology as-is).
- `direction`: only meaningful for `feeds` and `mutates_into`; `"out"` (default, this narrative → target) or `"in"` (target → this narrative, e.g. a predecessor in a lineage, or an upstream meta-narrative feeding this one).
- `target` is a tagged union — exactly one of two kinds:
  - `{ "kind": "tracked", "topic_id": "<existing watchlist id>" }`
  - `{ "kind": "shadow", "shadow_id": "<kebab-slug>", "name", "claim_hint", "queries": [4-6 strings] }` — a shadow carries exactly the fields the existing new-narrative founding path needs (see §3), nothing more.
- `evidence.videoIds`: must come from **this narrative's own corpus** (same "never invent sources" discipline as `consolidate.mjs`); may be empty for lineage/meta claims, in which case `evidence.note` must say it's a model estimate — mirroring the `born_note` "(model estimate, pending audit)" convention in `analyze.mjs`.
- `clock`: required iff `type === "shares_clock"`, forbidden otherwise.
- The `question` object lives **here**, not in `narrative.json` — the mint is then a single new-file commit that never touches existing files.

**Key trick — shadow→tracked upgrade is free:** `shadow_id` is by convention a candidate `topic_id`. At render time the client checks `watchlist.topics.some(t => t.id === shadow_id)`; if the tile now exists, the node renders as tracked. No migration write ever converts a shadow — founding the tile upgrades it everywhere automatically.

### Seed vocabulary — `candidates.json` (repo root, one new file)

The 22 researched candidates from `briefs/2026-08-10-flagship-shelf-research.md` become a machine-readable list so `map360` names shadows with already-researched slugs:

```json
{ "candidates": [ { "id": "the-ai-bubble-watch", "name": "The AI Bubble Watch", "claim_hint": "…", "queries": ["…"], "beat": "AI & technology" }, … ] }
```

Converted once, locally, from the brief (zero runtime Claude calls — the research already exists). Exclude #18 (marked SENSITIVE — Malik decides).

---

## 2. Minting — dedicated `map360.mjs`, plus one genuine zero-cost rider in `analyze.mjs`

**Do NOT put it in `consolidate.mjs`.** Fingerprints work as a rider there because they derive from input the call already has (claims + uncited videos of one narrative). Relations need the **cross-narrative** summary (`summarizeCorpus(topics)` — which only `analyze.mjs` builds). Adding that to every refresh's consolidate call bloats a per-refresh call with input for an output that changes roughly never. It would not be zero-cost; it would be a recurring tax.

### 2a. Primary: `netlify/functions/map360.mjs` — POST `/api/map360 {topic, force?}`

Structurally a sibling of `trace-origin.mjs` (dedicated on-demand call, cached result, `force:true` to re-run):

1. If `corpus/<topic>/relations.json` exists and `!force` → return it, no model call (mirrors the "won't re-charge for a phrase it already traced" behavior).
2. Fetch inputs from `RAW`: this topic's `narrative.json` + `claims.json` (compact form, as `consolidate.mjs` does), `watchlist.json` → `summarizeCorpus`-style digest of **all** topics (copy the helper from `analyze.mjs`), and `candidates.json` (names + claim_hints only).
3. One Claude call — `claude-opus-5`, `output_config: { effort: "low", format: { type: "json_schema", schema: MAP_SCHEMA } }`, `max_tokens: 2500`. `MAP_SCHEMA` = the relations.json shape above minus `note/updated/minted_by`, with `target_topic_id: string|null` and `shadow: {…}|null` flattened (exactly one non-null), and relations capped at 10 items.
4. System prompt core: *"A narrative is one ANSWER competing for a QUESTION. State the question this narrative answers (the durable demand behind it), then map the other answers"* + the five relation definitions + *"Prefer tracked topic_ids from the list; prefer candidate ids for shadows; evidence videoIds only from this corpus; empty evidence = mark the note as model estimate. Never invent sources."*
5. Server-side validation (mirrors the slug-collision guards in `analyze.mjs`):
   - `target_topic_id` not in watchlist → demote to shadow using the model's label as `name`.
   - `shadow_id` colliding with an existing topic id → upgrade to `{kind:"tracked"}`.
   - drop `clock` unless type is `shares_clock`; drop self-references.
6. `ghWrite("corpus/<topic>/relations.json", data, "Engine: 360 map for <topic> (<N> relations, <M> shadows)")` — the shared `ghWrite` helper already appends ` [skip netlify]`.
7. Return `{status:"mapped", topic, relations, persisted}`.

**Cost per narrative: exactly 1 Claude call** (input ≈ 4–7k tokens: one narrative + compact claims + ~30-line digest of all tracked topics + candidate names; output ≤ ~1.5k tokens) **+ 1 GitHub commit.** Same cost class as a single `/api/analyze` call. Re-maps are manual (`force:true`), so steady-state cost is ~zero.

### 2b. Rider: extend `ANALYSIS_SCHEMA` in `analyze.mjs` (this one really is free)

In the `new_narrative` branch, the model **already** has the full `tracked_narratives` digest in context. Add optional fields:

- `new_narrative_question: {text, demand, asked_since} | null`
- `new_narrative_relations: []` (same item shape, tracked targets only — no shadow minting from a metadata-only call)

Persist as a fourth sequential `ghWrite` in the existing new-narrative commit chain: `Engine: 360 map for <id> (founding rider)`. Marginal cost: ~0 input tokens, a few hundred output tokens on the call you were already making. Every future engine-founded tile is born with its 360 map.

---

## 3. Shadow nodes → founding path (the growth loop)

A shadow stub already carries `{shadow_id, name, claim_hint, queries}` — which is precisely what the existing buildout machinery needs, because **`refreshNarrative()` in `index.html` (line ~1157) already turns queries into a corpus**: sweep → analyze-each → consolidate.

Founding flow when the user clicks a shadow node:

1. Client shows a confirm strip on the card: *"Japan Carry-Trade Doom isn't tracked yet — found this narrative?"* with button `data-360-found="<shadow_id>"`.
2. On click, POST `/api/map360` with `{found_shadow: {…the stub…}, source_topic: "<current topic>"}` (a second branch inside `map360.mjs` — keeps the function count at one; ~40 lines). Server writes, sequentially (409-safe, same order as `analyze.mjs`'s founding path):
   - `watchlist.json` += topicRecord `{id: shadow_id, name, status:"active", started: today, trigger: "Founded from the 360 map of <source_topic>", queries, watched_predictors: [], notes: claim_hint}` — commit `Engine: found <shadow_id> from 360 map of <source_topic>`
   - `corpus/<shadow_id>/narrative.json` stub `{name, claim: claim_hint, predictor: "to be determined", born: <today YYYY-MM>, born_note: "Founded from 360 map (born date pending audit)", mutations: [], origin: {type:"map360", source_topic, created: today}}` — commit `Engine: narrative.json for <shadow_id>`
   - If the shadow matches a `candidates.json` entry, copy its richer claim/queries/born estimate instead of the stub's.
3. Client: `watchlist.topics.push(topicRecord)`, seed `cache[shadow_id]` (same pattern as `handleEngineResult`'s new-narrative branch, line ~1349), `openRadarAt(shadow_id)`, then `refreshNarrative(shadow_id)` — the existing loop sweeps the queries and builds the corpus while the user watches.
4. Every already-minted relations.json that names this `shadow_id` upgrades to a tracked node automatically on next render (§1 trick). No writes.

This is the loop: every 360 view renders unbuilt tiles as dashed one-click-to-found nodes, and the 22 researched candidates are the pre-loaded inventory.

Cost to found from shadow: 0 Claude calls for the founding itself; the subsequent buildout costs what a normal refresh costs (1 analyze call per swept video + 1 consolidate). Optionally fire a fresh `map360` for the new tile (+1 call).

---

## 4. Client rendering — `render360()` mounted inside `renderNarrativeCard()`

### Data plumbing (3 small edits in `index.html`)

- `loadTopicData()` (~line 971): add `try { entry.relations = await getJSON(\`corpus/${id}/relations.json\`); } catch (e) {}`.
- `renderNarrativeCard()` (~line 815): insert `<div id="map360"></div>` between `${claimsHtml}` and the `${trig …}` trigger block, and add a header-row button next to `⌖ Trace origin`: when `cache[topicId].relations` is absent → `<button class="followbtn mapbtn" data-map360="${topicId}">⊕ Map the territory</button>`; when present → same button with `title="Re-map (force)"` demoted into the section header.
- Document click listener (~line 1380): three new hooks — `[data-map360]` → `runMap360(topicId)` (mirrors the `data-trace`/`runTrace` handler: call API, on success set `cache[topicId].relations`, re-render); `[data-360-open]` → `loadTopic(id)` (tile switch, same as `data-open-topic`); `[data-360-found]` → founding flow from §3.

### What `render360(topicId)` consumes

It needs no new server JSON beyond `relations.json` — it resolves nodes locally:

```js
node = {
  type, direction, label, clock,                 // from the relation
  kind: "tracked" | "shadow",                    // shadow_id in watchlist ⇒ upgraded to "tracked"
  id, name,                                      // topic_id/shadow_id + display name
  receipt: null | { age: "11 yrs", score: "2 of 4 arrived", nextTest: "Sept 2028" } // tracked only, lazy
}
```

### Rendering (SVG radial, ~120 lines, no libraries)

- Center: the `question.text` in a circle, `demand` as the sub-line — the card's framing flips from "the narrative" to "the question it competes to answer."
- Nodes on a ring, grouped into arcs by type (order: `mutates_into[in]` upper-left → `feeds` top → `competes` right → `shares_clock` lower-right → `supplements` bottom); angle = arc start + index within group. Edge styling per type: solid (competes), dotted (supplements), arrowed (feeds/mutates, arrowhead per `direction`), dashed with a small clock glyph + `clock.trigger` label (shares_clock).
- Tracked nodes: solid border, `data-360-open`, plus a micro-receipt. Render the ring synchronously with names first, then async-fill receipts: `for each tracked node: loadTopicData(id).then(d => patch node with computeReceipt(d))` — `computeReceipt()` (~line 590) already produces age/score/next-test; reuse it, take the top 2 fields. This is the "comparison shopping for explanations" payoff: every rival answer wears its receipt.
- Shadow nodes: dashed border, muted, badge `not tracked — found it →`, `data-360-found`.
- Below the SVG, a plain-text list of the same relations (label + evidence note) for accessibility and small screens; the SVG sits in an `overflow-x:auto` wrapper like other wide content.

---

## 5. Migration

**The 6 existing narratives: no data migration at all.** Missing `relations.json` is a first-class state — the card simply shows "⊕ Map the territory" and no 360 section (identical to how a missing `genesis` just means the Trace button hasn't been pressed). Rollout:

1. Commit `candidates.json` (hand/locally converted from the brief): `Add candidates.json — 21 researched shadow candidates for the 360 map [skip netlify]` (21 = 22 minus the SENSITIVE one).
2. Deploy `map360.mjs` + the `index.html` edits (normal deploy, no `[skip netlify]`).
3. Press "Map the territory" on the 5 **active** narratives (`collapse-audit`, `crypto-winter-watch`, `the-2026-setup`, `housing-crash-watch`, `psi-declassified`) — **5 Claude calls total, 5 commits** (`Engine: 360 map for <topic> (…) [skip netlify]`). Skip `loop-engineering` (status `queued`, calibration topic).
4. Expected first-map yields, from the data already on file: `collapse-audit` should emit `competes → the-2026-setup` (tracked), `shares_clock → japan-carry-trade-doom` (shadow, candidate #7 — its yen-carry camp is already a source-cited camp in claims.json), `feeds/competes → the-ai-bubble-watch` (shadow, candidate #1 — the `ai-bubble-pop` claim is already consensus in the corpus), `supplements → hard-asset dealers` strand. The 22 candidates are not migrated into tiles — they surface organically as shadows and get founded by clicks (§3), which is the growth loop working as designed.

### Files touched, complete list

| Path | Change |
|---|---|
| `netlify/functions/map360.mjs` | new (~200 lines: schema, prompt, validation, ghWrite, found_shadow branch) |
| `netlify/functions/analyze.mjs` | +2 schema fields, +1 ghWrite in new-narrative branch (rider) |
| `index.html` | +1 line `loadTopicData`, `#map360` mount + button in `renderNarrativeCard`, `render360()` + 3 click hooks |
| `candidates.json` | new, one-time, from `briefs/2026-08-10-flagship-shelf-research.md` |
| `corpus/<id>/relations.json` | minted per narrative by the engine |
| `consolidate.mjs`, `sweep.mjs`, `trace-origin.mjs`, existing corpus files | untouched |
