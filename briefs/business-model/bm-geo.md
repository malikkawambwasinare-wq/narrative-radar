# Lens 3 — Geographic perspectives and domain schemas

Repo evidence read from `/Users/malikkawambwa/Desktop/Claude Code - Cycling/narrative-radar/corpus/` (collapse-audit is the reference corpus: `claims.json`, `indicators.json`, `predictions.json`, `relations.json`). Web research cited at the end.

---

## Part 1 — Multi-ecosystem comparison ("US vs Chinese-state vs European vs African vs Middle-East framing")

### Who does anything like this today

| Player | What it actually is | Buyer / price | Relevance to the vision |
|---|---|---|---|
| **GDELT** | Free machine-coded global event/media database | Academics; free | Confirms the raw-data route is a dead end for a product: researchers report ~55% key-field accuracy, ~20% redundancy, opaque black-box coding, and — critically — an English-language/Western bias that **under-indexes Swahili, Arabic, French local coverage**. Unusable raw; nobody has turned it into a consumer framing product. |
| **BBC Monitoring** | Human analysts monitoring TV/radio/press/social worldwide, region-by-region subscriptions | Governments (Cabinet Office, FCO, MoD), NGOs, universities, corporates; pricing is quote-only, institutional (Jisc-brokered for universities; premium digests sold separately) | The closest incumbent to "compare state-media framing." It is a **B2G/institutional analyst service**, not software; no self-serve tier, no price on the page. This is what serving policy desks actually looks like: procurement, not checkout. |
| **MEMRI** | Nonprofit translating Middle-East media for Western policy audiences | Donor-funded; output free to Congress/media | Framing-visibility work sustains itself on **grants and donors, not subscriptions** — a recurring pattern in this table. |
| **Semafor Signals** | Editorial feed where journalists use Microsoft/OpenAI tools to pull "perspectives from Chinese, Indian, or Russian media" on breaking stories, with citations | Reader product; **sponsored by Microsoft** for an undisclosed "substantial" sum | Proof the *format* works editorially — and proof of the economics: even Semafor, with a newsroom, funded it via sponsorship, not user revenue. |
| **Ground News** | Blindspot engine over left/center/right | Consumers, $10–100/**year** | Explicitly **US-partisan only**; third-party comparisons name "US-centric focus" and the "narrow left-right framework" as its known gap. The gap is real — and Ground News, at consumer scale, still prices at magazine-subscription levels. |
| **Blackbird.AI / narrative-intelligence vendors** | Enterprise "narrative attack" platforms, 25+ languages; Gartner named Blackbird "company to beat" for narrative intelligence (June 2026) | Global 2000 + national-security agencies; opaque enterprise pricing via Carahsoft | They sell **threat defense to brands/governments**, not perspective comparison to investors. None found marketing African-ecosystem coverage as a product line. |
| **Code for Africa (iLab/CivicSignal), Media Monitoring Africa, MFWA** | The actual African-media-analysis capacity on the continent | **Grant-funded**: USAID, UNDP, Sida, Danida, DW Akademie, Bloomberg ($10M); MMA budget ~€2M/yr of grants | African media monitoring exists — as donor-funded civil-society infrastructure focused on disinfo/elections, not as a subscription product, and not covering "how African media frames global macro narratives." |
| **Africa Confidential** | Expert-written Africa political/business intelligence since 1960 | **£1,044/$1,465/yr**, largely institutional | The one proof that paying demand for Africa-focused intelligence exists — but it's scarce human sourcing, the opposite of a solo founder's automated pipeline. |

### Is the African-ecosystem coverage hole real?

**The hole is verified. The market for it is not.** Three independent confirmations of the hole: GDELT's documented under-indexing of Swahili/local-language coverage; Ground News's documented US-only framing axis; and the fact that every organization actually analyzing African media (CfA, MMA, MFWA) is grant-funded rather than customer-funded. Nobody offers "how African ecosystems frame global narratives" as a buyable product.

But the funding pattern *is* the market signal. Everyone in the framing-comparison business is paid by someone other than the reader: BBC Monitoring by government stakeholders, MEMRI by donors, Semafor Signals by Microsoft, CfA by USAID/UNDP. There is no evidence anywhere in this landscape of individuals paying subscription money to see how other ecosystems frame a story. The settled business-lens research already said why: people pay for confirmation and positioning, not perspective-broadening. Ground News — the best consumer proxy — needs ~60k stories/day to justify $10–100/**year**.

**Who would actually pay, honestly assessed:**
- **Dev-finance / NGO / policy desks** — the only verified buyer class (they already fund CfA and buy BBC Monitoring). But they buy via RFPs, grants, and subcontracts with long cycles and compliance requirements. A solo founder in Dar/Nairobi *can* credibly enter that world (audit training + Swahili + regional context is a genuine fit, and CfA's partner list shows the network exists) — but that is a **services/consulting business**, not Radar Pro. It would consume the founder, not compound the product.
- **Diaspora investors / African CIOs** — no evidence found of either segment buying media-framing analysis from anyone. Unvalidated persona.

**Ingestion cost vs the wedge:** the current engine is one HTML scrape + ~$0.05–0.10 Claude calls over YouTube transcripts. Multi-ecosystem means multi-language transcripts (lower auto-caption quality outside English), non-YouTube sources (much African discourse lives on radio, Facebook, WhatsApp — the exact channels GDELT can't see either), and per-ecosystem source curation. That is a 10x+ pipeline change to serve an unvalidated buyer, while the validated buyer (macro/crypto self-directed investor, $39/mo hypothesis) is still at 0 external users.

**Verdict: vision-only, with one cheap exception.** The exception — the Semafor Signals move at $0.10 a call: the collapse-audit narrative could carry a "views from elsewhere" panel built from **English-language international outlets already on YouTube** (CGTN, Al Jazeera English, DW, CNBC Africa, Arise News) run through the *existing* analyze pipeline. Same infra, same language, same cost, genuinely differentiating on the shelf ("here's how Chinese-state and Gulf English media frame the US-collapse narrative"), and it tests whether anyone cares about perspective comparison before a single shilling is spent on multi-language ingestion. Frame it exactly as the founder says: informing, never adjudicating.

---

## Part 2 — Domain schemas

### How much of the finance schema already exists de facto

Mapping the proposed finance anatomy (claim→mechanism→asset→catalyst→timing→predictor→indicator→outcome) against what collapse-audit already encodes:

| Proposed slot | Already in the repo? | Where |
|---|---|---|
| claim | **Yes** | `claims.json`: `statement`, `type: consensus/contested` |
| mechanism | **Yes** | contested claims carry `camps[]` — e.g. `crisis-trigger` has three competing mechanism camps (AI-capex debt / credit seizure / yen-carry); `relations.json` even has a `competes_mechanism` relation type |
| asset | **Mostly** | indicator `category` (crypto, credit, rates, valuation, commodities… 12 values in use) |
| catalyst | **Yes** | indicator `role: trigger` (11 in use) and `countdown` (2) |
| timing | **Weakly** — the gap | `horizon` is free text; `shares_clock` relations carry `{trigger, next_check}` |
| predictor | **Yes, pervasively** | every threshold, claim source, and ledger entry is predictor-attributed |
| indicator | **Yes** | `indicators.json`: roles trigger/countdown/evidence/counter-evidence, thresholds with `{level, meaning, predictor}` |
| outcome | **Yes (schema), No (practice)** | `predictions.json` has the full PENDING/SUPPORTED/REFUTED/UPDATED/AMBIGUOUS status vocabulary — but **0 of 26 entries have ever been scored against a computed date** |

**The finance schema is roughly 80% built, de facto, extracted from a real corpus.** That is the important precedent: it was not designed up front — it condensed out of 31 transcripts and 312 indicator mentions. The geopolitics and health schemas would be designed against **zero corpora** (the only non-finance narrative, psi-declassified, has no indicators.json or predictions.json at all). Designing ontologies ahead of data is the taxonomy-project-that-never-ends failure mode, and it would also be re-litigating settled research: the adjudication-standard moat requires a *published fixed rule applied before outcomes are known* — one rule, stable, defensible — not three parallel ontologies maintained by one person.

Note also that the existing relation vocabulary (`competes`, `competes_mechanism`, `feeds`, `shares_clock`, `supplements`) is already **domain-agnostic** — it will carry geopolitics unchanged when a geopolitics corpus exists. The schema layer that needs to be per-domain is smaller than the founder thinks.

### The minimal schema move that pays for itself immediately

The single blocking defect is that **time is prose**. Measured across the ledger: `"~1-2 years"`, `"near-term"` (2), `"unstated (vague)"` (5), `"by ~2026-2028"`, `"coming weeks to months"`. No machine can decide when any of these come due — which is why 26 entries / 0 scored, and why the continuous re-observation cron (the identified surviving moat) cannot be built.

**Build now:** add one structured field alongside (not replacing) the free-text horizon, on prediction entries and on `shares_clock` clocks:

```json
"due": { "due_start": "2026-10-01", "due_end": "2027-12-31", "precision": "range|month|year|vague", "basis": "verbatim quote the dates were derived from" }
```

- `precision: "vague"` with null dates is itself an audit finding the ledger already narrates in prose ("that vagueness is itself an audit finding" — dalio-2016-supercycle).
- This one field unlocks, in order: automatic PENDING→due flagging (the cron), first-ever scored resolutions (the accountability core), "three followed narratives changed materially overnight" (the Radar Pro unit of value), and Thesis Intake scoring on the same clock (the retention mechanism). Every settled research thread lands on this same field.
- Cost: ~26 backfill extractions (one cheap Claude pass with human review, exactly like the verdict pass) plus a few lines in the analyze function's output schema.

### Build-now / vision-only split

| Build now | Vision-only (revisit at trigger) |
|---|---|
| Structured `due` dates on all 26 ledger entries + analyze-function schema (the clock field above) | Geopolitics & health ontologies — trigger: a real second-domain corpus of 20+ videos exists and the schema is extracted from it, finance-style |
| Score the first tranche of due predictions under a short **published** adjudication rule (the moat is the rule, and the rule needs the dates) | Multi-language / non-YouTube African-media ingestion — trigger: a named dev-finance/NGO buyer with budget, and accept it becomes a services engagement |
| Optional cheap probe: "views from elsewhere" panel on collapse-audit using English-language international outlets (CGTN, Al Jazeera EN, DW, CNBC Africa) through the existing pipeline | Multi-ecosystem comparison as a product tier; diaspora-investor and African-CIO personas (zero evidence anyone in these segments buys framing analysis) |
| Nothing else — indicator roles, camps, and relation types already carry the finance domain | Formal cross-domain "narrative schema" registry |

**Bottom line:** the geographic-perspectives vision is a real, verified coverage hole served today only by grant money — treat it as mission and marketing surface, not the wedge. The schema vision is 80% already built for the one domain that matters; the only schema work that is a moat rather than a taxonomy hobby is making time computable, because the adjudication standard and the re-observation cron — the two surviving moats from settled research — both stand on it.

---

**Sources:** [BBC Monitoring — Wikipedia](https://en.wikipedia.org/wiki/BBC_Monitoring) · [BBC Monitoring Portal — Jisc](https://subscriptionsmanager.jisc.ac.uk/catalogue/2733) · [UK Parliament evidence on BBC Monitoring](https://committees.parliament.uk/writtenevidence/72975/html/) · [GDELT and the Problem of Decontextualized Data — Source/OpenNews](https://source.opennews.org/articles/gdelt-decontextualized-data/) · [GDELT event database review — MDPI](https://www.mdpi.com/2306-5729/10/10/158) · [Lifting the Veil on Big Data News Repositories](https://www.tandfonline.com/doi/full/10.1080/19312458.2022.2128099) · [Ground News Blindspot](https://ground.news/blindspot) · [Ground News alternatives 2026 — Albis](https://www.albis.news/perspectives/ground-news-alternative-2026) · [Introducing Semafor Signals](https://www.semafor.com/article/02/05/2024/introducing-semafor-signals) · [Semafor Signals build — Press Gazette](https://pressgazette.co.uk/publishers/digital-journalism/semafor-microsoft-signals-ai/) · [Microsoft–Semafor AI newsroom — GeekWire](https://www.geekwire.com/2024/microsoft-announces-ai-newsroom-projects-with-semafor-and-others-as-nyt-lawsuit-looms/) · [Blackbird.AI pricing](https://blackbird.ai/pricing/) · [Blackbird.AI Gartner positioning](https://www.prnewswire.com/news-releases/blackbirdai-is-positioned-as-a-market-shaper-by-gartner-in-the-emerging-market-quadrant-for-narrative-intelligence---startup-vendors-as-of-june-2026-302815893.html) · [Code for Africa vs disinformation — Code for All](https://codeforall.org/2023/02/28/code-for-africa-vs-disinformation/) · [CfA iLab](https://medium.com/code-for-africa/ilabs-fight-against-disinfo-in-the-era-of-new-technologies-12e2f0541676) · [Media Monitoring Africa — Upgrade Democracy](https://upgradedemocracy.de/en/perspective/highlights/media-monitoring-africa/) · [Africa Confidential subscription](https://www.africa-confidential.com/subscription-information) · [Africa Confidential model — GIJN](https://gijn.org/stories/how-africa-confidential-covers-the-continent-with-a-subscription-model-that-works/)