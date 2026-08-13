# The 360 View — design synthesis (13 Aug 2026)

Product of a 6-lens research pass (typology stress-test, health + finance worked examples,
competitive scan, engineering spec, integrity audit — full reports in this directory).
Malik's founding insight, validated and sharpened: **a narrative is one answer competing
for a question. The question is the durable object; answers rotate. The 360 view is the
question's page — every rival answer wearing its receipt.**

## The five upgrades research forced on the v0 idea

1. **The Question is a first-class object** (not a label). `competes` becomes derived from
   `answers` edges — N edges instead of N² judgments. Questions have their own fingerprints
   ("why am I always tired" is literally what users type) — the question page is the natural
   search entry point.
2. **Triggers are first-class too.** "10yr Treasury above 5%" is a thing narratives *watch*,
   not a pairwise relation. The Dec 31 2026 pileup (AI-bubble Polymarket, Schiff's carry-trade
   and dollar-run, Kiyosaki's crash) = one clock node, four answers — the highest-leverage
   accountability moment on the shelf.
3. **`competes` splits.** competes_answer (exclusive: crash-imminent vs generational-buying-
   opportunity) vs competes_mechanism (co-traveling doom variants: 80-Year / Everything Bubble /
   AI capex / carry-trade — shared preachers, stacking mechanisms). Without the split the map
   presents four doom variants as "alternatives," reproducing the algorithm's trick: infinite
   variety inside one worldview.
4. **`counters` added** — the anti-narrative ("seed oils are fine") is not a competitor for the
   question; it negates one answer and has its own corpus, preachers, and receipt. Without it
   the map only ever shows believers.
5. **`mutates_into` is retrospective + evidence-gated** — and it's the most protective fact on
   the map. VERIFIED lineage from the health example: adrenal fatigue (1998) forked into
   "HPA-axis dysfunction" (clinical rebrand escaping falsification) and "cortisol face/detox"
   (TikTok rebrand, ~800M views, refuted on record). "This exact claim shape failed under a
   previous name" is the single most protective fact a tired person searching at 1am can see.

## The five hard gates (from the integrity audit — non-negotiable)

1. No edge without corpus receipts (≥3 videos, ≥2 independent channels; every edge clicks
   through to its citations; the model proposes, gates publish).
2. Human review for `supplements` and `shares_clock`; category-level seller naming by default;
   observable phrasing only ("products marketed with this narrative's language"), never
   conduct-verbs ("monetizes") — this is the defamation surface.
3. Three-tier external-evidence border treatment (Established / Contested / Unsupported) +
   the mandatory boring-baseline slot, Established-first ordering. Node size = discourse
   volume, labeled "how loud, not how true."
4. Health questions: meta-frame titles ("What the internet says about…"), a functional GP
   off-ramp node (not a disclaimer), red-line refusal topics (cancer treatment, vaccine
   safety, med discontinuation), and NEVER symptom-input personalization.
5. Verdict-summary-first (10-second closed form: "7 answers tracked · 1 established ·
   4 unsupported · boring baseline: see a GP"), full map behind one click, 1-hop depth,
   no feed, explicit completion state ("that's the whole map"). The map is the receipt,
   never the ride. Success metric: time-to-orientation — never dwell time.

## Competitive position

No product combines: question-as-object + rival answers as comparable nodes + per-node
accountability receipts + temporal lineage + sourced from YouTube/X + 10-second legibility.
Nearest partials: Society Library (structure, no receipts), Metaculus (receipts, no answer
ecology), Ground News (legibility, no accountability). **"Comparison shopping for
explanations" has no incumbent.**

## Build plan (v1, from the engineering spec)

- `corpus/<topic>/relations.json` per narrative (question object + typed relations;
  tracked | shadow targets). Shadow→tracked upgrade is free: shadow_id == candidate
  topic_id; client checks watchlist at render time.
- `netlify/functions/map360.mjs`: POST /api/map360 {topic, force?} — 1 opus call per
  narrative (~$0.05-0.10), cached like trace-origin; + found_shadow branch for the
  growth loop (click a ghost node → founds the tile via existing refresh machinery).
- `candidates.json`: the 21 researched shelf candidates as pre-loaded shadow inventory.
- analyze.mjs rider: new narratives born with question + tracked-only relations (free).
- Client: render360() radial SVG in the narrative card — center = the question,
  arcs by type, tracked nodes carry micro-receipts (computeReceipt reuse), shadows
  dashed with "not tracked — found it →".
- Migration: none. Missing relations.json = "⊕ Map the territory" button, like genesis.
- First run: 5 active narratives × 1 call ≈ $0.50 total.

## Seed maps ready to use

- Health: "why do I feel low energy all the time" — 15 answers, priced rider layer,
  2 verified lineages, receipt audit per answer (360-health.md). Suggested first tiles:
  mitochondria, cortisol-detox (honesty-gap flagship), seed oils, glucose spikes, low-T.
- Finance: "is a US market crash imminent" — mechanism-vs-answer split, full shared-clock
  enumeration, 3 untracked competitors found (melt-up-first/Hunter, passive-flows/Green,
  private-credit/Gundlach) (360-finance.md).

## Health-vertical receipt additions (from the falsifiability audit)

Finance-born strips assume dated predictions; health answers make timeless mechanism
claims. Three added gates: institutional verdict (recognized/contested/refuted by named
bodies) · n-of-1 testability (is there a blood test that settles it FOR YOU — ferritin
yes, mitochondria no) · rider-layer score (evidence + price of what's sold on the answer's
back — Mitopure has RCTs, $2,800 NAD+ drips have none).
