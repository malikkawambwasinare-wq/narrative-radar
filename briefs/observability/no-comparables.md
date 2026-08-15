> **Note on `narrative-radar` files:** I did not need to modify any repo files for this lens. Prior verdicts read from `/Users/malikkawambwa/.claude/projects/-Users-malikkawambwa-Desktop-Claude-Code---Cycling/memory/data-moat-research-verdict.md`.

---

# LENS 3 — COMPARABLES AND CATEGORY

## 0. Headline

**The nine-niche kill verdict does not kill this proposal — but it kills three of the four assets the portable-thesis lens named as defensible.** What survives is narrower and differently-shaped than "narrative observability": it is not a data moat, not a metric moat, and not a time-in-market moat. It is a **standard-setting** moat, which is a slower, smaller, and more reputational business than the SpotGamma analogy implies.

The single most damaging finding in this lens is that **the raw archive of deleted YouTube content already exists at ~10,000x the founder's scale, free, run by roughly one person.** The single most encouraging finding is that **no incumbent at any price point covers spoken YouTube claims** — Brandwatch's audio transcript coverage is broadcast TV and radio only, and there is no official YouTube captions API for third-party videos.

---

## 1. SpotGamma — the analogy is weaker than it looks

**What subscribers pay for.** Tiers run roughly $67–$97/mo annual at the low end up to Alpha at ~$224–299/mo, with Institutional starting at **$1,999/mo**. Critically, **all tiers include the same core bundle** — Founder's Notes, key levels, Equity Hub across 3,500+ names. The expensive tiers add HIRO (real-time) and TRACE (heatmap). Pricing tiers currently disagree between spotgamma.com/pricing and /subscribe (2 tiers vs 5), which itself signals a company still testing packaging.

**Is the moat the metric, the data, or the note?** All three sources point the same way: subscribers buy **the daily interpretation**, delivered pre-open and post-close every trading day, written by people with bank/market-maker/hedge-fund backgrounds. The Founder's Note is described as the most foundational and popular product and is bundled into every tier — you cannot buy the data without it.

**The disanalogy that matters.** SpotGamma's input is **OPRA** — the consolidated US options feed. That is a licensed, exchange-controlled, paid feed; OPRA non-display use alone runs a flat **$2,000/month per category, across three categories**. SpotGamma is therefore *not* a cron-job business. It sits behind a paid data seat (a privileged position in the exact sense the founder's Aug 2026 verdict required), it re-derives a model from a feed that no free publisher republishes, and it wraps that in twice-daily human judgement for a buyer whose decision converts to P&L within hours.

Narrative Radar's input — free, scraped, ToS-adjacent YouTube — is on the **wrong side** of that line. Structurally, the input profile resembles the nine rejected niches, not SpotGamma.

**One genuinely useful borrowing:** SpotGamma publishes a **Quarterly Report Card** scoring its own calls. Self-scoring is used as a trust device by the very company being emulated. That validates the accountability instinct — but as a *credibility layer on a paid product*, not as the product.

---

## 2. Bloomberg — the wrong moat to aspire to, and it says why

$31,980/year per seat. The literature converges on four layers: 40 years of data depth (a time-based moat), workflow/compliance embedding, brand distribution via Bloomberg News/TV, and — repeatedly named as the *real* moat — **Instant Bloomberg chat**, the closed network where bond traders actually transact. Cancelling costs you the network, not the data.

**Read-across:** the durable part of a terminal is the thing that gets *worse for the user when they leave*. A Narrative Radar user who cancels loses a bookmark. There is no chat, no counterparty, no compliance record, no colleague on the other end. "Terminal" framing without a lock-in mechanism is aesthetics.

---

## 3. Datadog / observability — the category pays because of the pager, and there is no pager here

Datadog did **$3.43B in 2025 revenue**. Why the category pays: incident detection tied to **SLA/SLO commitments** creates a business justification; then a multi-product ladder (APM → logs → synthetics → RUM → security → CI → DB monitoring) creates data-dependency lock-in. A mid-market stack can run **$123k+/year** across seven tools — commentators now call it "the observability tax," explicitly comparing it to 2000s enterprise software: long contracts, complex billing, switching costs as soft lock-in.

**The analogue test.** Observability pays because (a) an incident has a dollar cost, (b) someone is *on call*, (c) failure is unambiguous and time-stamped. Narrative observability has none of these by default. Nobody is paged when a narrative mutates. **Without an incident, an observability product is a dashboard, and dashboards churn.**

The two places a real incident exists: a **comms/IR team mid-crisis** (that's Zignal/Blackbird — enterprise, $50k–150k, long sales cycles, not solo-buildable) and **a retail investor about to move money** (that's TipRanks — and it's already built, see §7).

---

## 4. Epidemic nowcasting — the public-good trap, stated plainly

HealthMap flagged COVID **11 days before WHO confirmation**; GPHIN caught SARS in 2002. Both are institutionally funded public goods. The one that commercialised — **BlueDot** — did so by becoming **closed and client-only**, not public.

**Read-across:** in nowcasting-under-bad-data, the public artifact never monetises; the *access-restricted* version does. A public radar page that anyone can read is a marketing asset, not a revenue asset. This is the same shape as the founder's own "free publishers cap price at zero" finding, arriving from a different domain.

---

## 5. Social listening incumbents — what they already do, what they charge, what they can't reach

| Vendor | Typical annual price | Overlap with the proposal | Gap |
|---|---|---|---|
| Brandwatch | ~$1,000/mo entry; enterprise from ~$36k/yr | Heat, velocity, breadth, concentration; archive back to **2010**; full X history back to **2006** via Hindsight/Official X Partner status | **Audio transcripts = broadcast TV and radio only.** Not YouTube spoken content |
| Meltwater | ~$6k–$15k/yr, up to $12k–$60k with media monitoring | Same attention layer + earned media | No claim ledger, no resolution |
| Talkwalker | $25k+/yr, six figures at scale | Broadest platform coverage; video analytics with speech-to-text on YouTube/TikTok/IG | Searchable archive, **not** an adjudicated record of who was right |
| Sprinklr | $249/mo self-serve; $100k–150k+/yr enterprise | Full CXM suite | Same |
| Zignal Labs | from ~**$49.5k/yr**; enterprise $150k+ | Explicitly "Narrative Intelligence Cloud"; May 2026 launched Zignal AI for agent-driven mission systems | National-security/mission buyer; no accountability ledger |
| NewsWhip | not disclosed | Predictive earned-media velocity | Same |

**The verified coverage hole.** There is **no official public YouTube API for third-party captions** — the Data API v3 Captions endpoint requires OAuth and only works on videos you own. Brandwatch's transcript layer is broadcast-only. Talkwalker does speech-to-text but sells it as search, not adjudication. So the **spoken-claim layer of YouTube is genuinely under-served at every price point from $0 to $150k/yr.** This is the strongest pro-proposal finding in the lens and it is not obvious from the outside.

**But** the ATTENTION layer of the three-layer model is fully commoditised. Tubular Labs alone indexes **11–15B videos and 28M creators**, from ~$1,000/mo. Heat, velocity, breadth and concentration are table stakes. Building them adds credibility, not defensibility.

---

## 6. Narrative-intelligence natives — the category Gartner just invented, and its financials are grim

Gartner published its **inaugural** Emerging Market Quadrant for Narrative Intelligence – Startup Vendors on **26 June 2026** (Ramirez IV, Kaushik, Khan, Boyes, Senf). Blackbird.AI and Cyabra were both named Market Shapers. A brand-new Gartner category means the buyer does not yet have a budget line — Gartner is describing demand, not proving it.

- **Blackbird.AI** — $28M strategic round Jan 2026, **$58M total**; reports 118% ARR growth and tripled customer wins (no ARR base disclosed). Constellation maps narratives, bot networks, influence topology. Buyer: enterprise risk/comms + public sector.
- **Cyabra** — the cautionary tale. De-SPAC'd 27 March 2026. Q1 2026: revenue **$1.4M** (+12% y/y), ARR **$7.0M** (+19%), net loss **$10.8M**, cash **$3.1M**, **going-concern warning** and a **Nasdaq listing deficiency**. Stock **−92.3%** over twelve months to $0.44 (~$6M market cap) — while holding US State Department, NATO, PepsiCo, e.l.f. and WarnerMedia as customers. *Marquee logos did not produce a viable business.*
- **Graphika** — raised only **$6.49M** ever; survives on DoD contracts (USAF ~$1.9M Jun 2024, SOCOM ~$1.36M Mar 2024) plus bespoke research. Effectively a research shop.
- **Alethea** — $34M total, last round Apr 2024 (GV-led). Artemis is subscription, price undisclosed.
- **PeakMetrics** — $6M Series A Apr 2026, **$16.3M total, 22 FTEs**, "a dozen+" Fortune 500 clients. AI platform *plus forward-deployed engineers* — i.e. the product doesn't sell without humans attached.
- **Pyrra** — outcome: **acquired by AlertMedia**. Absorbed into an alerting suite.
- **Logically** — **filed for administration** after losing Meta and TikTok contracts amid the political rollback of anti-misinformation work; had already cut ~40 of ~200 staff in Feb 2025. Platform-dependent revenue evaporated.
- **Kaito** — the most direct warning. **X revoked API access for apps rewarding posting; Yaps — ~70% of KAITO's utility — was wound down in Jan 2026**, token −17%. The pivot is to a brand/creator marketing platform; Kaito Pro reportedly starts around **$833/mo**. The proof that "people pay to know what the crowd believes" turned out to be proof that *a platform can delete your business in one policy change.*

**Category verdict:** narrative intelligence in 2026 is a category with a Gartner quadrant, ~$100M of aggregate venture funding, one going-concern warning, one administration filing, one absorption, and no visible profitable operator. This is not a rising tide.

---

## 7. The accountability comparables — the ones that actually decide this

These matter more than anything above, because the resolution record is the proposed core asset.

**TipRanks — the existence proof, and the trap.** A "Financial Accountability Engine" measuring **96,000+ experts** including **7,500+ financial bloggers**, scoring accuracy and average return per call; consumer pricing **$29.95/mo Premium, $49.95/mo Ultimate**; **~$20–30M revenue**; ~6M MAU plus ~50M through banks/brokers; **majority stake acquired by Prytek at a $200M valuation**. It also proves the legal-risk-arbitrage thesis is survivable: TipRanks has publicly scored named humans for a decade.

**But read why it works: resolution is mechanical.** A rating resolves against a price series at zero marginal cost. TipRanks never adjudicates. It never argues about whether the claim came true.

**PunditTracker — the direct precedent, and it's gone.** Built 2012–13 to score pundits' predictions, explicitly on the premise that "if they turn out to be wrong, nobody's going to go back and check." Got Slate, WNYC/On the Media, Ritholtz coverage. Crunchbase shows no recent activity; the domain has been repurposed since ~2021. **The exact product, with the exact founding insight, with real press, did not survive.** The delta versus TipRanks is precisely mechanical-vs-judgement resolution — and adjacency to a money decision.

**FinTuber and FinfluencerTracker — already operating in the founder's own niche.** FinTuber compares YouTube finance creators' picks against the S&P 500 with win rates and risk-aware framing. FinfluencerTracker extracts stock calls from YouTube *and* X, applies standardised long/short rules, signals activate next trading day and expire ~3 months, with YTD/1Y/3Y/all-time tables and a free tier plus paid full history. Both are thin and neither discloses scale — but **the "score YouTube finance creators over calendar time" idea is occupied, by indie builders, at consumer price points.**

**Metaculus / Good Judgment — the monetisation shape.** Metaculus is a public-benefit corporation: free public platform + **Metaculus Pro** commissioned private tournaments. Good Judgment sells Superforecaster subscriptions, custom forecasting and training to financial services, energy, government and NGOs. Aggregated public forecasting matched model ensembles and beat classified-access analysts. **Neither monetises the public record. Both monetise bespoke work for institutions.** Same shape as BlueDot.

**Ground News — the consumer willingness-to-pay ceiling.** The closest thing to a working consumer "media observability" product: Blindspot shows lopsided coverage, free users get 6/day, Vantage is **$99.99/yr (~$8.33/mo)**, with mobile tiers from $0.99–$3.99/mo. Widely praised as the best media-literacy tool available. It has raised **~$1.01M** and discloses no revenue. **Consumers will pay roughly $8–10/month for structural media insight, and the best-executed instance of it is a small business.**

---

## 8. THE ARCHIVE TEST — this is where the "deleted content is the moat" claim breaks

The portable-thesis lens named "the UPDATED/deadline-roll counter (it only exists because earlier versions were recorded; deleted content is the moat)" as a core asset. Testing it directly:

- **Filmot** independently indexes **~720 million captions across ~645 million videos and 52 million channels**, in 100+ languages, and — because it snapshotted while videos were live — **still returns title, channel, upload date, description and often the full transcript of videos YouTube no longer serves.** There is a companion userscript that restores deleted/private video titles in playlists automatically. Free. Effectively one operator.
- **Internet Archive / Ghostarchive / Archivarix** cover deleted-video recovery, with real limits: only a tiny fraction of YouTube is ever mirrored, media files often aren't captured, and Ghostarchive caps at 360p/~100MB and skips livestreams and 30-minute-plus videos. But **captions, titles, descriptions and upload dates survive far more often than the video does** — and captions are exactly the input the founder uses.

**Conclusion:** the founder's corpus is ~110 videos. Filmot's is ~645,000,000. **The raw material is not scarce and the archive is not the moat.** Worse for the time-in-market claim: a funded competitor does not need 18 calendar months to reach n=5 resolved calls. Narrowed to, say, 500 trading channels, backfilling three years of captions from Filmot/IA and extracting dated claims with an LLM is a compute problem measured in days, not a calendar problem measured in years. **The "competitor with $50M starts at n=0" argument should be downgraded from a moat to a speed bump.**

What genuinely *cannot* be reconstructed is thin but real: (i) videos deleted before any archive captured them; (ii) the precise state of a claim at first observation — title edits, description rewrites, pinned-comment walk-backs — which archives capture only accidentally; (iii) the fact that a specific standard was applied *at the time*, before the outcome was known. Item (iii) is the only one that is structurally, permanently unbackfillable, and it is **not a data property — it is a procedural/reputational one.**

---

## 9. Does the nine-niche kill verdict kill this? Both sides.

### The case that it DOES

1. **Input profile matches the killed nine exactly.** Free, publicly-published, cron-collectable. The founder's own rule: "if data is cheap for a solo builder to collect, it was cheap for everyone."
2. **The Wayback test applies with force.** It was supposed to be strongest here and it isn't: Filmot at 645M videos is a bigger Wayback than Wayback for this specific asset.
3. **The SpotGamma template requires a paid seat.** OPRA at ~$2k/mo per non-display category is a capital barrier. There is no equivalent barrier protecting YouTube captions — only ToS.
4. **Platform risk is not hypothetical, it is the category's leading cause of death.** YouTube's Developer Policies cap stored API data at **30 days** before mandatory delete-or-refresh, require re-verifying **every 30 days that a video has not been deleted**, and require stored data to stay consistent with live data. That policy is *specifically hostile to keeping a record of deleted content*. Outside the API, PO-token enforcement and IP blocking hardened sharply 2024→2026. Kaito lost ~70% of product utility to one X policy change; Logically went into administration when Meta and TikTok cancelled.
5. **The attention and structure layers are already sold** — Tubular from $1k/mo, Brandwatch/Meltwater/Talkwalker/Zignal at $6k–$150k/yr, plus Blackbird/Cyabra/Alethea on topology.
6. **The precedent product died.** PunditTracker, same thesis, real press, gone.
7. **The category's economics are visibly bad.** Cyabra: NATO + State Department + PepsiCo as clients, and a going-concern warning.

### The case that it DOESN'T

1. **The nine niches all resold an observation. This resells a judgement.** In every rejected niche the number existed before the collector arrived; the business was faster/cheaper access to something already true. A dated, attributed, horizon-bound claim with an adjudicated outcome **does not exist anywhere until someone creates it.** Filmot has the sentence. Nobody has the verdict.
2. **The coverage hole is verified and specific.** No official YouTube captions API for third-party video; Brandwatch's audio transcripts are broadcast-only. A $36k/yr enterprise suite literally cannot tell you what a YouTuber said. That is not a crowded niche.
3. **TipRanks proves the business model at scale** — $200M valuation, $20–30M revenue, consumer pricing, decade-long public scoring of named humans without being sued out of existence.
4. **Ground News proves consumer WTP** for structural media insight at ~$8–10/mo.
5. **The reputational asset is genuinely unbackfillable.** Applying a published standard *before* outcomes are known cannot be faked retroactively — the timestamp is the product. Moody's, Morningstar, Metacritic and PolitiFact are all cheap-to-collect data businesses that became durable by becoming *the referenced standard*.
6. **The founder's failure mode is different from the nine.** Those failed because incumbents already owned the metric layer. Here, **no incumbent owns the adjudication layer for spoken video** — the natives do topology and authenticity, the listening suites do volume, TipRanks does tickers.

### Decision

**Partial kill. Three of four named assets fall; one survives, re-specified.**

| Asset | Status |
|---|---|
| Attention layer (heat/velocity/breadth/concentration) | **Dead as a moat.** Commodity from $0 to $1k/mo. Keep as UI credibility only |
| Structure layer (topology, mutation, contestation) | **Dead as a differentiator.** This is the funded natives' territory, and they are not thriving |
| "Deleted content / the archive is the moat" | **Killed by Filmot.** Retire this claim entirely — it is factually wrong at 645M videos vs 110 |
| "Time-in-market: competitors start at n=0" | **Downgraded to a speed bump.** Backfillable from Filmot/IA + LLM extraction in days |
| **The adjudication standard — a published, fixed rule for what counts as a claim and what counts as resolution, applied by a named party before outcomes are known** | **Survives.** Not a data moat. An institutional/reputation moat |

The nine-niche verdict demanded "a privileged position, not a cron job." **A standard that others cite is a privileged position** — it is just earned over years through consistency and citation rather than bought with a data licence. That is a real answer to the founder's own test. It is also a slow, low-revenue answer, and it must be entered with eyes open.

---

## 10. Consequences for the narrative-observability framing

1. **Drop "observability" as the pitch.** Observability pays because of the pager, the SLO and the dollar cost of an incident. There is no on-call here, and buyers who *do* have narrative incidents are enterprise comms/national-security accounts requiring forward-deployed engineers (PeakMetrics' model) and $50k–150k contracts. That buyer is not solo-serviceable.
2. **Lead with accountability, not attention.** The only layer of the three-layer model that is not already sold by someone with more money is ACCOUNTABILITY. Layers 1 and 2 should be supporting evidence for layer 3, not co-equal.
3. **Prefer mechanically-resolvable claims where possible.** TipRanks lives and PunditTracker died on exactly this axis. Every claim requiring human adjudication carries permanent marginal cost and permanent dispute risk.
4. **The wedge with the best odds** sits at the intersection of everything verified above: **YouTube trading/market-call channels, scoring the claims that are *not* tickers** — regime and strategy claims ("the crash comes in Q4", "this setup wins 90% of the time"). Rationale: FinTuber and FinfluencerTracker already own ticker picks; the listening suites cannot see spoken YouTube at all; resolution can be pinned to public price/market data so it stays cheap; the buyer is the founder's own year-one self; and the price point is proven at $8–30/mo by Ground News and TipRanks. This also stays inside the existing integrity rules — the standard is published, and the product reports outcomes rather than asserting truth.
5. **Assume platform risk is the primary existential threat, not competition.** The Developer Policies' 30-day storage/refresh rule and delete-verification requirement are pointed directly at the intended asset. Kaito and Logically are the precedents. Any plan should include: derived-artifact-only storage, an explicit ToS posture, and no dependency on a single platform's tolerance.
6. **Retire the phrase "the deleted content is the moat"** from all internal and external material. It is the one claim in the prior research that this lens falsifies outright, and repeating it in front of anyone who knows Filmot exists is expensive.

---

## 11. What would change this verdict

- Evidence that Filmot/IA caption coverage of the *specific* channels in scope is materially incomplete (sample 50 known-deleted videos from tracked channels; if <40% have recoverable captions, the archive claim partially revives).
- A buyer interview finding anyone who has an *incident* — a moment where being wrong about a narrative costs them money on a deadline.
- Evidence that FinTuber/FinfluencerTracker have real traction (that would validate demand but confirm the niche is contested) or are abandoned (validating that even the mechanical version doesn't monetise at indie scale — a PunditTracker echo).
- Any sign that Gartner's June 2026 category is pulling real budget rather than describing venture interest — watch whether Blackbird discloses an ARR base rather than a growth rate, and whether Cyabra resolves its going-concern warning.

---

## Sources

[SpotGamma pricing (support)](https://support.spotgamma.com/hc/en-us/articles/1500002666102-What-is-the-cost-of-a-SpotGamma-Subscription) · [SpotGamma plans](https://spotgamma.com/subscribe-to-spotgamma/) · [SpotGamma review 2026 (FlashAlpha)](https://flashalpha.com/articles/spotgamma-review-2026-pricing-features-alternatives) · [SpotGamma Founder's Note](https://support.spotgamma.com/hc/en-us/articles/15341610402579-What-is-the-SpotGamma-Founder-s-Note) · [SpotGamma Quarterly Report Card](https://spotgamma.com/spotgamma-quarterly-report-card/) · [HIRO indicator](https://support.spotgamma.com/hc/en-us/articles/4420646443539-What-is-the-SpotGamma-HIRO-Indicator) · [OPRA fees & licensing](https://www.marketdata.app/education/options/opra-fees/)

[Why Bloomberg Terminal costs $31,980/yr](https://godeldiscount.com/blog/why-is-bloomberg-terminal-so-expensive) · [The greatest moat ever: Bloomberg terminals](https://theownersedge.substack.com/p/the-greatest-moat-ever-how-bloombergs) · [Bloomberg data moat & network effects](https://www.tumisangbogwasi.com/blog/business-war-room/bloomberg-terminal-data-moat-network-effects/)

[The observability tax (OneUptime)](https://oneuptime.com/blog/post/2026-03-29-the-observability-tax-what-your-7-tool-stack-costs/view) · [Datadog pricing 2026](https://openobserve.ai/blog/datadog-pricing/) · [Datadog alternatives / full-stack observability](https://www.groundcover.com/guides/datadog-alternatives-for-full-stack-observability)

[AI in public health: epidemic early warning systems](https://journals.sagepub.com/doi/full/10.1177/03000605231159335) · [HealthMap project (PLOS Medicine)](https://journals.plos.org/plosmedicine/article?id=10.1371%2Fjournal.pmed.0050151) · [The business of pandemic intelligence](https://onlinelibrary.wiley.com/doi/full/10.1111/1758-5899.70050)

[Social listening cost comparison 2026](https://deepclick.com/resources/blog/social-listening-cost-pricing-2026/) · [Brandwatch vs Meltwater vs Talkwalker 2026](https://syncly.app/blog/brandwatch-vs-meltwater-vs-talkwalker) · [Brandwatch historical data back to 2010](https://www.brandwatch.com/blog/now-offering-historical-twitter-data-back-2006/) · [Brandwatch Twitter Hindsight](https://www.prnewswire.com/news-releases/brandwatch-twitter-hindsight-launches-groundbreaking-historical-data-offering-269372021.html) · [Brandwatch vs Talkwalker vs Mention 2026](https://genesysgrowth.com/blog/brandwatch-vs-talkwalker-vs-mention) · [Zignal Labs pricing](https://www.itqlick.com/zignal-labs/pricing) · [Zignal AI launch, May 2026](https://finance.yahoo.com/sectors/technology/articles/zignal-labs-launches-zignal-ai-120000058.html) · [Tubular Labs pricing & scale](https://www.creatorstackclub.com/software/tubular)

[Gartner Emerging Market Quadrant for Narrative Intelligence, 26 June 2026](https://cyabra.com/award/cyabra-is-named-a-market-shaper-in-the-june-2026-gartner-emerging-market-quadrant-for-narrative-intelligence-startup-vendors/) · [Blackbird.AI $28M / $58M total](https://www.securityweek.com/blackbird-ai-raises-28-million-for-narrative-intelligence-platform/) · [Blackbird.AI ARR growth release](https://blackbird.ai/blog/blackbird-ai-reports-arr-growth-triples-customer-wins-and-secures-strategic-funding/) · [Cyabra Q1 2026 results](https://www.stocktitan.net/news/CYAB/cyabra-reports-first-quarter-2026-results-and-highlights-commercial-ffxnh5tnw04y.html) · [Cyabra 10-Q: revenue up, losses deepen](https://www.stocktitan.net/sec-filings/CYAB/10-q-cyabra-inc-quarterly-earnings-report-f3c26058c6f2.html) · [Cyabra stock overview](https://stockanalysis.com/stocks/cyab/) · [Graphika profile & contracts](https://tracxn.com/d/companies/graphika/__V-DFmgHRFAW_IHlzEXicHR2MXf1inWLZ-Kp-Jful1y0) · [Alethea $20M Series B](https://alethea.com/insights/alethea-raises-20m-in-series-b-funding-for-disinformation-mitigation) · [PeakMetrics $6M Series A (Axios)](https://www.axios.com/2026/04/09/peakmetrics-funding-ai-reputation-risk) · [Pyrra profile](https://tracxn.com/d/companies/pyrra-technologies/__0g0XHM7BZRCOQ2JRNeOA64f3jv1kH-5_TgA9iX3CZKY) · [Logically files for administration](https://sifted.eu/articles/logically-ai-fact-check-misinformation-trump-tiktok-meta) · [Logically layoffs](https://sifted.eu/articles/anti-misinformation-startup-logically-lays-off-dozens-in-global-cost-cutting-drive) · [Kaito sunsets Yaps after X ban (CoinDesk)](https://www.coindesk.com/business/2026/01/15/kaito-to-sunset-yaps-as-x-cracks-down-on-infofi-apps-token-falls-17) · [Kaito after Yaps](https://blockeden.xyz/blog/2026/04/18/kaito-yaps-attention-economy-infofi-meritocratic-influence/)

[TipRanks acquired by Prytek at $200M](https://finance.yahoo.com/news/fintech-firm-tipranks-majority-stake-172211344.html) · [TipRanks revenue estimate](https://growjo.com/company/TipRanks) · [TipRanks pricing 2026](https://tradingtoolshub.com/blog/tipranks-pricing-guide-2026/) · [TipRanks blogger accountability (Duke/Geneva study)](https://www.tipranks.com/news/labs/now-its-official-without-tipranks-you-are-following-the-opinions-of-underperforming-bloggers) · [PunditTracker (Ritholtz, 2013)](https://ritholtz.com/2013/02/pundit-tracker/) · [PunditTracker on WNYC On the Media](https://www.wnycstudios.org/podcasts/otm/segments/191468-pundit-tracker) · [PunditTracker Crunchbase](https://www.crunchbase.com/organization/pundittracker) · [FinTuber](https://www.fintuber.io/) · [FinfluencerTracker](https://www.finfluencertracker.com/) · [YouTube finfluencers & retail investors (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6451318) · [Finfluencer recommendations (Economics Letters)](https://www.sciencedirect.com/science/article/abs/pii/S0165176525003489) · [Metaculus review 2026](https://predictgeek.com/prediction-markets/metaculus/) · [Good Judgment × Metaculus](https://goodjudgment.com/owidproject/) · [Ground News review, Aug 2026](https://www.stationx.net/ground-news-review/) · [Ground News funding](https://pitchbook.com/profiles/company/340782-22)

[Filmot](https://filmot.com/) · [Filmot (OSINT tools library)](https://tools.osintnewsletter.com/osint-tools/filmot) · [Finding deleted YouTube videos in 2026](https://socialrails.com/blog/how-to-find-deleted-youtube-videos) · [YouTube API Services Developer Policies](https://developers.google.com/youtube/terms/developer-policies) · [Complying with YouTube's Developer Policies](https://developers.google.com/youtube/terms/developer-policies-guide) · [YouTube transcript API guide 2026](https://outlierkit.com/resources/youtube-transcript-api/) · [Is YouTube scraping allowed? (ScrapeOps, 2026)](https://scrapeops.io/websites/youtube/) · [yt-dlp IP blocking issue](https://github.com/yt-dlp/yt-dlp/issues/16747)
