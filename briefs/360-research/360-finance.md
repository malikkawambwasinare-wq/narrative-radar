# 360 View — Finance Worked Example
## Question: "Is a US market crash imminent?"

Built from: `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/briefs/2026-08-10-flagship-shelf-research.md`, `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/collapse-audit/claims.json`, `corpus/collapse-audit/narrative.json`, `corpus/collapse-audit/predictions.json`, `corpus/crypto-winter-watch/claims.json`, `corpus/housing-crash-watch/narrative.json`, `corpus/the-2026-setup/narrative.json`, and the receipt-strip spec at `briefs/2026-08-11-receipt-strip-spec.md`, plus web search for untracked answers.

---

## 0. The headline finding: the corpus already contains the 360 view in embryo

`corpus/collapse-audit/claims.json` has a contested claim `crisis-trigger` ("What triggers the crisis?") with three camps — AI capex debt, credit-market seizure, Japan repatriation/yen-carry — and this note:

> "The mechanism rotates with the news cycle — the narrative's audit signature. Same conclusion, competing engines."

That is the 360 view at miniature scale, living *inside* one tile. The feature is largely a **promotion of camps to tiles**: what claims.json models as camps within "The 80-Year Collapse," the 360 map models as related narratives around the question. This is both validation (the data model already wants this) and the source of the typology's biggest strain (below).

---

## 1. COMPETES — and where it strains

### 1a. The four named "competitors" are NOT cleanly competing. They are co-traveling variants.

| Narrative | Mechanism | Verdict on "competes" |
|---|---|---|
| The 80-Year Collapse (tracked, `collapse-audit`) | End of the long debt cycle | The **parent**, not a peer — it has absorbed the others as mutations |
| The Everything Bubble Pops (researched #8) | Cheap money inflated all assets; synchronized pop | Near-duplicate of the parent with different messengers (Kiyosaki/Howell vs Dalio) |
| The AI Bubble Watch (researched #1) | Debt-financed AI capex pops | Currently a **camp inside** collapse-audit (`crisis-trigger` camp 1) AND a standalone tile candidate |
| Japan Carry-Trade Doom (researched #7) | JGB yields force carry unwind, drain US liquidity | Also a **camp inside** collapse-audit (`crisis-trigger` camp 3) |

Evidence they co-travel rather than compete:

1. **Belief in one does not displace belief in another.** In the health example, "it's your mitochondria" and "it's vitamin D" are rival diagnoses — adopting one crowds out the other. Here, Dalio's own framing is "convergence" of forces; the mechanisms *stack*. `collapse-audit/narrative.json` shows Dalio adding mechanisms (capital war Feb 2026, AI capex Jul 2026) to the pile without retiring any.
2. **Shared messengers.** Schiff carries carry-trade doom (#7), de-dollarization (#9), AND silver (#6). Burry appears in both AI Bubble (#1) and Everything Bubble (#8) voice lists. Rival camps don't share preachers.
3. **Live absorption.** collapse-audit's Jul 2026 mutation is literally "AI capex as the crisis vector" — the parent ate the newest competitor. The claims.json note even flags it: "Watch for cross-narrative migration."

**Where competition is real:** the true competitive axis for this question is **conclusion + direction**, not mechanism:

- **"No — correction, not crash"** — the sell-side consensus. Exists only as skeptic camps inside doom tiles (#8 "correction-not-crash sell-side consensus"). Never gets its own tile. See strain report.
- **The 2026 Setup (tracked, `the-2026-setup`)** — a genuinely competing answer: "2026 is a generational buying opportunity, position now." Its own narrative.json calls it "structurally the bull-side mirror of rolling-doom." This is the strongest COMPETES edge in the tracked shelf.
- **Crypto Winter Watch (tracked)** — competes on direction for its asset class: consensus "bottom Aug–Nov 2026, new bull leg by 2027" is an anti-crash answer on the same clock the doom narratives use.
- **Untracked competitors** — see section 6 (melt-up-first, passive-flows, private credit).

### 1b. Proposed fix

Split `competes` into two edge types:

- **`competes_answer`** (exclusive): believing one weakens the other. Crash-imminent vs generational-buying-opportunity vs melt-up-first. Rare and valuable.
- **`competes_mechanism`** (co-traveling): rival engines for the same conclusion, mutually reinforcing, mechanism rotates with the news cycle. 80-Year Collapse / Everything Bubble / AI Capex / Carry-Trade. Common in finance; this is the audit signature itself.

Without the split, the 360 map would present four doom variants as if they were genuine alternatives — which reproduces the algorithm's trick (infinite variety inside one worldview) instead of exiting it.

---

## 2. SUPPLEMENTS — the monetization layer

This type works cleanly. The corpus documents it directly.

| Supplement | Rides on | Receipt |
|---|---|---|
| **Hard-assets hedge** (`hard-assets-hedge` in collapse-audit claims.json: gold $7–14K targets) | All doom variants | Corpus note verbatim: "Where the narrative monetizes — several sources are dealers or affiliates. Follow the incentive." |
| **Silver Squeeze / Metals Supercycle** (researched #6) | All doom variants (the hedge product) | Dual role — see strain 4 below |
| **"How to protect your wealth" content / courses / newsletters** | All variants incl. bull-side | The 2026 Setup narrative.json: "excitement is the product being sold" — the bull answer has its own supplement layer (funnels), so supplements attach to ANSWERS, not to doom specifically |
| **De-Dollarization Doom Clock** (researched #9) | Ambiguous — see strain 6 | Schiff messenger overlap; gold monetization attaches to it identically |
| **Bitcoin as hedge** (`million-dollar-btc`, crypto claims.json) | Crash-of-fiat variants | "The faith layer — mostly unfalsifiable on useful horizons" |

**Strain 4 (question-relativity):** Silver Squeeze is a *supplement* in this 360 view but a first-class *answer* to its own question ("why is silver mispriced?") with its own ledger — including a scored HIT (Neumeyer's 2017 $100 call hit Jan 2026). Relations must be **scoped to the question, not global properties of the tile**. An edge is (question, tile, relation), not (tile, tile, relation).

---

## 3. SHARES_CLOCK — every shared clock found in the briefs

This is the typology's best-performing type. Full enumeration:

1. **10yr Treasury > 5%** — the poster child. Sharma's AI-bubble trigger condition (#1, Jul 31) AND the carry-trade repatriation mechanism (#7: "10yr UST dragged toward 5% by repatriation (note: same trigger as Sharma's AI-bubble condition — narratives link!)"). One instrument, two narratives, already flagged in the research brief itself.
2. **Dec 31 2026** — the crowded exit: Polymarket AI-bubble-burst resolution (#1) · Schiff "2026 is when this unfolds" carry-trade (#7) · Schiff dollar-run-in-2026 (#9) · Kiyosaki crash-in-2026 (#8). Four narratives resolve on the same date. A 360 map should render this as one shared clock node with four edges — it is the single highest-leverage accountability moment on the shelf.
3. **Mid/late 2026 liquidity turn** — Howell's liquidity-peak-mid-2026 + 2026–27 maturity wall (#8) vs Crypto Winter's consensus bottom Aug–Nov 2026 then 2027 bull leg (crypto claims.json). Same liquidity-cycle clock, opposite conclusions drawn — a shared clock connecting a doom tile to a bull tile.
4. **Nov 3 2026 midterms** — Dalio's midterm-conflict claim (collapse-audit expert note) · Midterm Wave Watch (#15) · Midterms-Won't-Happen (#18) · Grid Reckoning as "declared 2026 midterm battleground" (#2). One election date clocking four narratives across beats.
5. **~2028 window** — Dalio's first countable debt-crisis clock (Sept 2028, `dalio-2025-debt-3yr`) and Steve Keen's AI-pop ~2027–28 (collapse-audit claims.json). Loose but real.
6. **Aug 2026 yen intervention** (#7, "THIS MONTH") — a live event both camps of carry-trade doom are re-clocking around; doomers call it "a delay, not a fix" (unfalsifiability-drift warning for the ledger).

**Discovered sibling relation — `shares_receipt`:** the **BIS June 2026 annual report** is cited as institutional cover by BOTH AI Bubble Watch (#1) and Everything Bubble (#8). Not a clock — a shared evidence artifact. Likewise **`shares_messenger`**: Schiff appears in 3 tiles, Burry in 2, Dalio bridges collapse-audit and AI-bubble. Messenger overlap turned out to be a *stronger* co-travel signal than clock overlap — it is the reason competes_mechanism edges exist at all. The typology should add at least shares_messenger; it is computable today from the voices/predictor fields (after the normalization pass the receipt-strip spec already requires).

---

## 4. FEEDS — upstream meta-narratives

- **"The fiat/debt endgame"** (money-printing destroys the currency; the supercycle ends) — upstream parent of 80-Year Collapse, Everything Bubble, De-Dollarization, Silver Squeeze, and the bitcoin faith layer. The mirror of "modern life is poisoning you" in the health example.
- **"This time is 1929/2008"** — the historical-rhyme meta; supplies the emotional payload to every variant (Everything Bubble's claim is literally "worse than 1929 + 2008 combined"; Housing Crash Watch is built on "echoing 2008-crash framing" per its narrative.json).
- **"The crash is engineered"** — conspiracy-tier upstream (The Great Taking, section 6); consumes ANY mechanism as evidence of the plan.
- Cross-beat feeds already in the brief: **Grid Reckoning (#2) feeds AI Bubble Watch** (power constraint as the capex-thesis breaker), marked with the brief's own ⚡ collision notation — the ⚡ marks are proto-feeds/shares edges.

**Strain 6:** De-Dollarization resists single classification — it is simultaneously a competing mechanism (dollar run as trigger), an upstream meta (dollar system ending), and a supplement carrier (gold). Verdict: classify per-question; for THIS question it is `competes_mechanism` with a `feeds` edge from the fiat-endgame meta above it.

---

## 5. MUTATES_INTO — lineages

The data model already proves this type exists: `collapse-audit/narrative.json` carries a `mutations` array — six mechanism mutations 2015→2026 for one predictor (1937 analogy → debt supercycle → internal conflict → Phase 5 → capital war → AI capex).

Two distinct phenomena are currently sharing one name:

- **Intra-narrative mechanism rotation** (the Dalio array): same predictor, same conclusion, engine swapped with the news cycle. This is an *audit signature*, already tracked.
- **Inter-narrative succession** (the health example's adrenal-fatigue→mitochondria): same demand, new tile, often new messengers. Finance examples: **subprime (2008) → Everything Bubble (term ~2014) → AI capex bubble (2024–25)** as "the next 2008" re-answered per era; **"the next subprime" → private credit** (Gundlach's phrasing is a literal named mutation — see section 6); **dot-com → AI bubble** as the valuation-analogy lineage.

Recommend reserving `mutates_into` for inter-narrative succession and keeping intra-narrative rotation in the existing mutations array. The bridge case: when a camp inside a tile (AI-capex inside collapse-audit) graduates to its own tile, that is the moment a rotation becomes a lineage — the engine should record the graduation as a dated event.

---

## 6. Untracked competing answers (web search) — candidate shadow tiles

Three genuinely distinct answers to "is a US market crash imminent?" not on the shelf:

### 6a. "Yes — but melt-up first" (David Hunter)
Parabolic final leg of a 43-year bull to S&P 8,000–9,500, THEN an 80% crash and global deflationary bust; bust "likely starts with a second-quarter swoon in 2026" per [Wealthion](https://wealthion.com/news/david-hunter-warning-final-melt-up-to-sp-8000-then-an-80-crash) and [Pinnacle Digest](https://pinnacledigest.com/blog/the-last-melt-up-before-the-fall-david-hunters-2025-warning-for-investors). **Typology note — hybrid edge:** it `competes_answer` near-term (buy, don't sell) while `feeds` the doom conclusion long-term. Relations may need a stance/valence field. **Shadow receipt strip:** the Q2-2026 swoon claim is scoreable NOW (Q2 has passed; the brief's own record shows Mag-7 lost $2.2T in June 2026 — candidate AMBIGUOUS/partial); the S&P 8,000 melt-up leg is cleanly falsifiable; [track-record coverage exists](https://financhill.com/blog/investing/david-hunter-contrarian-track-record) to seed a ledger.

### 6b. "The real bubble is passive flows" (Mike Green)
Passive indexing broke price discovery, concentrated capital, and created a reflexive loop that unwinds 1929-style — with a by-2026 framing in circulation per [WebProNews](https://www.webpronews.com/the-passive-investing-time-bomb-why-one-strategist-warns-the-stock-market-could-face-a-1929-style-reckoning-by-2026/), [ETF Stream](https://www.etfstream.com/articles/mike-green-passive-ownership-is-approaching-dangerous-levels), [Institutional Investor](https://www.institutionalinvestor.com/article/2e5um1swovwbm3x5yyk1s/corner-office/why-michael-green-is-known-as-the-cassandra-of-passive-investing). A genuinely different mechanism (structural, not debt) — the cleanest `competes_mechanism` addition, and it also `feeds` AI Bubble Watch (concentration = Mag-7). **Shadow strip:** "1929-style by 2026" resolves Dec 31 2026 — joins the crowded shared clock in section 3.2; single-messenger narrative ("Cassandra of passive"), so source-spread metric would flag concentration.

### 6c. "Private credit is the next subprime" (Gundlach et al.)
The $1.7T+ (some estimates far larger) opaque private-credit stack has "the same trappings as subprime repackaging in 2006" — Gundlach Jun 2025 via [Yahoo Finance](https://finance.yahoo.com/news/bond-king-jeffrey-gundlach-warns-201825636.html); late-2025 defaults, PIK-toggle stress, Blackstone/KKR/Blue Owl down 20–50%+, withdrawal gates per [CNBC Mar 2026](https://www.cnbc.com/2026/03/11/private-credit-could-be-the-next-crisis-how-worried-should-you-be-.html), [CNBC pushback](https://www.cnbc.com/2026/03/30/private-credit-fears-have-ripped-through-wall-street-in-2026-why-they-may-be-overblown.html), [With Intelligence 2026 outlook](https://www.withintelligence.com/insights/private-credit-outlook-2026/); Wikipedia already titles it the ["2025–2026 private credit crisis"](https://en.wikipedia.org/wiki/2025%E2%80%932026_private_credit_crisis). **Shadow strip:** unusual on this shelf — a doom narrative with events PARTIALLY ARRIVING (candidate SUPPORTED/AMBIGUOUS entries), but Gundlach's founding claim names no date (falsifiability-instrument case). Also a textbook `mutates_into` target: "the next subprime" is the subprime answer's named successor.

*(Considered and noted as feeds-tier rather than a competitor: "The Great Taking" (David Rogers Webb) — the engineered-crash/collateral-seizure meta, [Goodreads](https://www.goodreads.com/book/show/203175664-the-great-taking), [KunstlerCast](https://podcasts.apple.com/us/podcast/kunstlercast-390-david-rogers-webb-and-the-great-taking/id273772632?i=1000638802651) — no dated claims; falsifiability-warning strip state.)*

---

## 7. Per-answer receipt strips (what renders today, per the spec's gates)

| Answer | Age | Score (gated n≥5) | Slippage | Next test | Recycled / spread |
|---|---|---|---|---|---|
| 80-Year Collapse (tracked) | 11 yrs, verified (ledger to 2015-03) | Renders: 0 of 4 gradeable arrived (+3 AMBIGUOUS, ~4 PENDING) — from predictions.json: 2 REFUTED, 2 UPDATED, 3 AMBIGUOUS | 2 evidence-free rolls on record | Nov 2026 (midterm-conflict), then Sept 2028 countable clock | 7 original / 38 — late lifecycle |
| Everything Bubble (researched) | ~12 yrs (term ~2014; Kiyosaki strand 2002) — "roughly, unverified" | Too early (no ledger) — but Kiyosaki rolling-since-2013 is "the deadline-move counter's showcase" | Star metric once built | Dec 31 2026 (Kiyosaki); mid-2026 Howell liquidity peak resolving now | n/a |
| AI Capex Bubble (researched) | ~2 yrs (mid-2024) | Too early — richest clock density on the shelf | None yet (too young to roll) | Polymarket Dec 31 2026; Sharma conditional (10yr>5%); Ives through-2027 | n/a |
| Japan Carry-Trade (researched) | Doom-form 2 yrs (Aug 2024); substrate 1990s — dual-birth display problem, spec's "roughly" state handles it | Too early | Watch: Aug 2026 intervention re-clocking ("delay, not a fix" = drift) | Dec 31 2026 (Schiff) | n/a |
| The 2026 Setup (tracked, bull side) | ~1.3 yrs (2025-04, model estimate) | Unfalsifiable until year-end — falsifiability instrument swaps into slot 2 | Signature to watch: rebrand to "2027 Setup" | Dec 31 2026 | Young corpus |
| Crypto Winter "bottom late 2026" (tracked, bull side) | — | Too early; strongest consensus clock in any corpus | — | Aug–Nov 2026 window, live NOW; bottom-depth camps ($35–40K vs $53–60K floor) directly opposed | 13-source spread on the consensus claim — good independence |
| Housing Crash Watch (tracked) | ~6 yrs (2020-06, estimate) | Too early (3 videos); recycled-share suppressed (<10 indexed) | Encoded in founding claim ("date keeps sliding") | 2026-dated calls: refute or reschedule | Suppressed |
| Silver Squeeze (supplement/answer) | 5–9 yrs by strand | Mixed — has a scored HIT (Neumeyer $100, Jan 2026) then −50% crash: vindication-variant showcase | — | Commerzbank $90 by end-2026; "stays above $100" contested | n/a |
| Melt-up first (shadow) | Honest empty state: "not yet tracked" | Q2-2026 swoon scoreable immediately on founding | — | S&P 8,000 leg | — |
| Passive-flows bubble (shadow) | Empty state | — | — | Dec 31 2026 | Single-messenger flag |
| Private credit (shadow) | Empty state | Events partially arrived — rare SUPPORTED-leaning seed material | — | Founding claim undated — falsifiability warning | — |

---

## 8. Typology strain report (summary)

1. **`competes` must split** into `competes_answer` (exclusive, rare, valuable — crash vs buy-the-dip vs melt-up-first) and `competes_mechanism` (co-traveling engines, mutually reinforcing, shared messengers). The four flagship "competitors" are all the latter. Presenting co-traveling doom variants as a 360 of alternatives would replicate the rabbit hole, not map the exit.
2. **The null answer has no tile.** "Correction, not crash" exists only as skeptic camps inside doom tiles. The 360 map is doom-biased by construction unless camps can be promoted to first-class answers (the crisis-trigger camps show the engine already half-does this).
3. **Add `shares_messenger`** (Schiff x3, Burry x2, computable from voice fields after the normalization pass the receipt-strip spec already mandates) and consider `shares_receipt` (BIS June 2026 report cited by two tiles). Messenger overlap is the strongest co-travel detector found.
4. **Relations are question-scoped, not tile-global.** Silver Squeeze: supplement here, first-class answer to its own question. Edge = (question, tile, type).
5. **`mutates_into` should mean inter-narrative succession only**; intra-narrative mechanism rotation stays in the existing mutations array. Record camp-to-tile graduations (AI-capex leaving collapse-audit) as dated events — that is the moment rotation becomes lineage.
6. **Edges need stance/valence** for hybrids: melt-up-first competes near-term while feeding the doom conclusion; de-dollarization is mechanism-competitor, meta-feeder, and supplement-carrier simultaneously.
7. **`shares_clock` is the strongest type as-is** — and the Dec 31 2026 pileup (four narratives, one date) suggests shared-clock NODES should render as first-class objects on the map: one date, many answers, maximum accountability.

Sources: [Wealthion — Hunter melt-up](https://wealthion.com/news/david-hunter-warning-final-melt-up-to-sp-8000-then-an-80-crash) · [Financhill — Hunter track record](https://financhill.com/blog/investing/david-hunter-contrarian-track-record) · [Pinnacle Digest — Hunter 2025 warning](https://pinnacledigest.com/blog/the-last-melt-up-before-the-fall-david-hunters-2025-warning-for-investors) · [WebProNews — passive time bomb](https://www.webpronews.com/the-passive-investing-time-bomb-why-one-strategist-warns-the-stock-market-could-face-a-1929-style-reckoning-by-2026/) · [ETF Stream — Green](https://www.etfstream.com/articles/mike-green-passive-ownership-is-approaching-dangerous-levels) · [Institutional Investor — Green profile](https://www.institutionalinvestor.com/article/2e5um1swovwbm3x5yyk1s/corner-office/why-michael-green-is-known-as-the-cassandra-of-passive-investing) · [Yahoo Finance — Gundlach](https://finance.yahoo.com/news/bond-king-jeffrey-gundlach-warns-201825636.html) · [CNBC — private credit worry](https://www.cnbc.com/2026/03/11/private-credit-could-be-the-next-crisis-how-worried-should-you-be-.html) · [CNBC — fears overblown](https://www.cnbc.com/2026/03/30/private-credit-fears-have-ripped-through-wall-street-in-2026-why-they-may-be-overblown.html) · [With Intelligence — 2026 outlook](https://www.withintelligence.com/insights/private-credit-outlook-2026/) · [Wikipedia — 2025–2026 private credit crisis](https://en.wikipedia.org/wiki/2025%E2%80%932026_private_credit_crisis) · [Goodreads — The Great Taking](https://www.goodreads.com/book/show/203175664-the-great-taking) · [KunstlerCast 390](https://podcasts.apple.com/us/podcast/kunstlercast-390-david-rogers-webb-and-the-great-taking/id273772632?i=1000638802651)