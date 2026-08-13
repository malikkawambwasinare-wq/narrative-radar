# Integrity Audit — "360 View of the Claim" (Competing Explanations Map)

Adversarial posture: I assume the map ships as designed and ask how it hurts users, hurts real third parties, or betrays the product's founding promise. Each risk ends with concrete guards (rendering rules, evidence gates, phrasing).

---

## 1. False equivalence — the flattening problem

### The failure mode
A node-and-edge map is a visual grammar of peers. The moment "sleep debt" (boring, true, strongly evidence-backed) and "microplastics stole your energy" (speculative, near-zero clinical evidence) render as same-sized circles on the same canvas, the layout itself asserts *these are comparable candidate answers*. That assertion is false, and it is exactly the move cable-news panels and "teach the controversy" campaigns use. The Receipt Strip is supposed to carry the differentiation, but receipts are text a user must read; the map is a gestalt a user absorbs in one glance. Gestalt beats text. Worse: the product's own honesty gate (score gated at n>=5 resolved predictions) means the *most evidence-backed answer often shows NO score* — sleep debt has few YouTube "predictions" to resolve, so it renders as the blandest, least-decorated node, while the microplastics narrative arrives with a dramatic ledger, a genesis post, and a born-date. The fringe answer literally gets more visual furniture. The honesty gates, designed for single narratives, invert into a fringe-amplifier in comparison view.

There is a second, subtler flattening: Narrative Radar's metrics measure *narrative behavior* (prediction accuracy, recycled share, source spread), not *scientific standing*. A user will read "score: 62%" as "62% likely true." The product has no ground-truth-of-the-world signal at all — and the map view is precisely where users will demand one, because comparison shopping implies a best buy.

### How serious epistemics products avoid it
- **Wikipedia** solves it with WP:DUE — minority views get *proportional* space and are *labeled* as minority, never symmetric layout.
- **Cochrane / GRADE** attach an explicit evidence-certainty tier (high/moderate/low/very low) to every claim; the tier is the loudest element, not a footnote.
- **AllSides / Ground News** never rank truth — they rank *coverage and lean*, and say so in the frame ("who is saying this," not "who is right"). That's the honest lane for this product too.
- **Fact-checkers (PolitiFact et al.)** use ordinal verdict scales rendered *in* the visual (the meter IS the graphic), so the gestalt carries the differentiation.

### Guards
- **G1.1 — Never equal-size nodes.** Node size/weight must encode something real. The honest encoding for this product is *discourse volume* (corpus size), explicitly labeled "how loud, not how true." Do not encode validity you cannot measure.
- **G1.2 — Add one orthogonal axis you CAN defend: "External evidence" tier.** Three values only — `Established` (mainstream clinical/scientific consensus exists for this mechanism, cite 1–2 institutional sources like NIH/NICE/Cochrane), `Contested`, `Unsupported/Fringe`. Human-assigned or human-approved, never model-solo (see §4). Render it as the node's border treatment so the gestalt itself separates tiers — e.g. solid border = established, dashed = contested, dotted+muted = unsupported.
- **G1.3 — Sort order is an editorial act; own it.** Default ordering/placement puts Established answers first/top. Randomized or force-directed layout is false neutrality.
- **G1.4 — The boring-answer slot is mandatory.** Every question-page must render the "boring baseline" answers (for the tiredness question: sleep, iron/thyroid/B12 workup, depression, medication side effects) even when the corpus barely covers them — flagged "low YouTube coverage, high clinical relevance." The asymmetry *is* the product insight: the algorithm under-serves boring answers; the map must over-serve them or it replicates the algorithm's bias with extra steps.
- **G1.5 — Score display in map view needs a comparative honesty gate.** If any node on a map shows a prediction score, nodes without one must show "no resolved track record" — never blank — so absence reads as absence, not neutrality.

---

## 2. Legitimization by adjacency — inclusion is promotion

### The failure mode
Every anti-misinformation practitioner knows the amplification trap: debunking a fringe claim introduces it to people who'd never heard it. A 360 map industrializes this. A user arrives having heard only "vitamin D" and leaves knowing "methylene blue" exists — with a tidy node, a name, and (per the fingerprints feature) *the exact phrases to type into YouTube to find it*. The fingerprints feature, benign on a single-narrative page, becomes a **fringe onboarding kit** in map view. Shadow nodes are worse: an *untracked* name-only stub carries zero receipts — pure legitimization with no countervailing evidence at all, wearing the product's credibility.

There's also a gaming surface: once being-on-the-map has promotional value, sellers have an incentive to manufacture "competition" discourse to earn a node (see §4's evidence gate — it must be resistant to this).

### When an answer should NOT get a node
Adapt notability + harm-weighting:
- **Volume floor:** the answer doesn't clear a minimum corpus threshold (suggest ≥5 independent channels ≥3 independent-origin videos, not one channel's series). Below floor → not rendered, at most counted in an aggregate "N minor answers not shown" chip.
- **Harm override:** answers whose *adoption* is dangerous (e.g. protocols involving prescription-drug self-dosing, extreme fasting for "mitochondrial reset") face a higher bar and, if included, render with a harm flag — but consider that for some, exclusion is safer than a flagged node.
- **Shadow nodes are second-class, always.** Different visual grammar (ghost/outline, no fill, smaller), labeled "mentioned in discourse — not yet tracked, no receipts," non-clickable to any detail page, and **no fingerprints ever shown for shadow nodes**.
- **Fingerprints gating in map view generally:** show fingerprints only on the narrative's own detail page (where the user already knows the narrative), never in the comparison map. The map's job is orientation, not search-term supply.

### The counterweight (why inclusion can still be right)
The user is going to meet the fringe answer *anyway* — the algorithm guarantees it. Meeting it first inside a receipts frame ("recycled share 70%, 0 supported predictions, sellers attached") is inoculation, and prebunking research supports encountering claims first in a critical frame. So the rule is not "exclude fringe" — it's **never render a fringe node without its receipts attached in the same glance** (verdict chip visible on the node itself, not one click away), and never render receipt-less shadow stubs as if they were peers.

---

## 3. The "supplements/monetizes" edge — a defamation surface with real names on it

### The failure mode
This is the audit's highest *legal* risk. "Competes" and "mutates_into" describe ideas. "**Supplements (rides/monetizes)**" describes *conduct by identifiable commercial actors* — it says, in a published product, that a named seller is exploiting a narrative for money. Rendered next to nodes tiered "Unsupported/Fringe," the composed meaning is "this company profits from a false health claim" — an implication of deceptive trade. That's a classic defamation-by-implication setup even if every individual element is technically defensible. And the ledger names *individual predictors* — individuals sue more readily than brands. A single Claude misclassification (a sleep-hygiene educator's channel tagged as "monetizing the mitochondria narrative" because it mentioned NAD+ once) is a plausible demand letter. Note that the product auto-commits classifications to the corpus ("paste-any-link → Claude classifies + auto-commits"), meaning defamatory edges could publish with **no human review at all**.

### Guards
- **G3.1 — Describe the observable, not the motive.** Kill the verbs "rides" and "monetizes" in all rendered copy. Replace with mechanical, provable phrasing: *"Products marketed with this narrative's language"* or *"N videos in this corpus promoting [category] reference this explanation."* You can prove a video used the phrase; you cannot prove intent to exploit.
- **G3.2 — Category-level by default, entity-level only with receipts.** Default render: "supplement products (NAD+ boosters, red-light devices) are marketed alongside this narrative" — no seller names. A named entity requires ≥3 corpus videos where *that entity or its affiliate links* appear tied to the narrative's claims, each citation stored and linkable (the receipt IS the defense — truth, with evidence you can produce).
- **G3.3 — No auto-publish for supplements edges.** Competes/mutates edges may auto-commit; any edge that names or implies a commercial actor goes to a human review queue. This is the one place the paste-and-auto-commit pipeline must have a mandatory human gate.
- **G3.4 — Opinion-framing and a correction channel.** Ship a visible methodology page ("what this tag means, what evidence it requires"), timestamp every edge, and provide a dispute/correction contact. Fast, documented correction on notice is both ethically required and the practical mitigation of defamation exposure.
- **G3.5 — Never compose the accusation visually.** Rendering rule: a supplements edge must not visually inherit the target node's Unsupported tier styling (e.g. don't paint the seller edge red because the narrative is fringe). The product states two facts separately; it must not draw the syllogism.

---

## 4. Model-invented relations — hallucinated edges

### The failure mode
Every edge type has a distinct hallucination flavor, and some are worse than others:
- **competes:** Claude "knows" adrenal fatigue and mitochondria both answer tiredness from world knowledge, and asserts a rivalry the actual corpus never expresses. The map claims to be a map *of the discourse*; a world-knowledge edge is editorializing disguised as observation.
- **shares_clock:** the most seductive and most dangerous — it's a *causal-financial thesis* ("10yr above 5% triggers both X and Y") wearing a data-product costume. If Claude invents or misattributes a shared trigger, the product is publishing an original macro claim. Given the founder's history — the product exists because confident financial narrative-spinning cost him $20k — **shipping model-authored financial linkage theses is the product becoming the thing it fights.** This edge type should be near-fully manual.
- **mutates_into:** a historical succession claim ("adrenal fatigue became mitochondria") that is genuinely contestable intellectual history. Plausible-sounding lineages are exactly what LLMs confabulate best.
- **supplements:** covered in §3 — hallucination here is defamation.

Compounding factor: the auto-commit pipeline means hallucinated edges persist and *accrete apparent authority* (an edge that's been on the map for six months looks established).

### Evidence standard before an edge renders
- **G4.1 — Corpus-grounded or it doesn't exist.** An edge requires *citations into the product's own corpus*, not model knowledge. Baseline gate: **≥3 corpus videos from ≥2 independent channels** in which the relation is actually expressed (for `competes`: the video explicitly contrasts/dismisses the rival answer — "it's not your adrenals, it's your mitochondria"; for `supplements`: the product pitch co-occurs with the narrative's claims in the same video). Multi-channel requirement also blunts the §2 gaming vector (one actor manufacturing "competition" to earn a node).
- **G4.2 — Every edge is clickable to its receipts.** Clicking an edge shows the exact videos (with timestamps/quotes where feasible) that justify it. An edge that can't show its receipts doesn't render. This makes hallucination *auditable* rather than merely hoped-against.
- **G4.3 — Tiered publication gates by risk:** `competes`/`feeds` at the baseline gate, auto-commit OK with edge-level receipts; `mutates_into` requires the baseline gate PLUS human approval (historical claims); `shares_clock` requires a *verbatim shared trigger* already recorded in both narratives' prediction ledgers (same falsifiable condition, independently logged) — Claude may only *notice* the match, never author the trigger; `supplements` per §3.
- **G4.4 — Candidate vs. published states.** Claude proposes edges into a `candidate` state with its citation list; below-gate candidates are visible in an admin view only. Users never see model conjecture.
- **G4.5 — Edge provenance chip.** Every rendered edge carries "based on N videos · last confirmed [date]" — the Receipt Strip philosophy applied to relations, which is the product's own medicine.

---

## 5. Health-domain duty of care — the map that reads as a differential diagnosis

### The failure mode
"Why am I always tired?" with candidate answers arrayed around it **is the visual form of a differential diagnosis**. No disclaimer changes what the picture is. Three concrete harms:
1. **Anchoring/substitution:** a user with undiagnosed anemia, hypothyroidism, sleep apnea, or depression comparison-shops narratives instead of getting bloodwork. The map's completeness *feels* like a workup ("I've now considered everything") — it satisfies the diagnostic urge and thereby delays the real one. This is the map's most likely real-world harm, and it needs no fringe content to occur.
2. **The best answer isn't on the map.** The true cause for many chronically tired people is a specific, testable medical condition that has no YouTube narrative economy around it. A map built from discourse structurally omits it.
3. **Disclaimer theater:** banner disclaimers are banner-blind within seconds; a footer "not medical advice" is legally decorative and behaviorally null. The research-consistent finding is that *framing built into the content* works where *appended warnings* don't.

### Guards that actually work (framing over disclaiming)
- **G5.1 — Rename the frame.** The page title is never the medical question as if the product answers it. Not "Why am I always tired? — 7 answers" but **"What the internet says about 'why am I always tired'"** or "The tiredness narrative economy." Every headline, breadcrumb, and share-card uses the meta-frame. The product's honest claim is "we map the discourse," so the UI must say *discourse* everywhere the user looks.
- **G5.2 — A functional off-ramp node, not a disclaimer.** For health-domain questions, render one visually distinct, always-first element: *"Persistent fatigue has common, testable medical causes (iron, thyroid, sleep apnea, depression, medication side effects). None of them trend on YouTube. A GP visit with basic bloodwork rules them in or out — start there."* This is an *action* the user can take, placed where the diagnosis-seeking impulse is, which is the only disclaimer pattern with a chance of behavior change. It also doubles as G1.4's boring-baseline slot.
- **G5.3 — Domain flagging with red-line topics.** Tag questions by domain (health/finance/geopolitics). Health questions get G5.2 automatically. Some question-level topics should be refused a 360 map entirely (cancer treatment, vaccine safety, medication discontinuation, mental-health crisis) — domains where "comparison shopping for explanations" is itself the harm pattern (that's how people shop their way from oncology to apricot kernels). Publish the refusal criteria.
- **G5.4 — No symptom-input personalization, ever.** The instant the user can enter *their* symptoms and get a filtered map, it's a symptom checker — a regulated category (potential software-as-medical-device territory in UK/EU) and an ethical cliff. The map is about the discourse, never about the user's body. (Same spirit as Ride Copilot's "the app cannot see the rider's body" rule — this product cannot see the user's blood panel.)
- **G5.5 — Language audit rule.** Rendered copy never uses second-person causal phrasing ("your mitochondria," "your cortisol") outside quoted narrative titles. The product's own voice speaks only about *claims*: "this narrative attributes fatigue to…" Quotes from the discourse render visibly as quotes.

---

## 6. Does the map become the rabbit hole? — the product eating its own premise

### The failure mode
The founding promise is "check in 10 seconds what took me 6 years." The 360 map is, structurally, the opposite artifact: an open-ended explorable graph where every node links to a corpus, a ledger, fingerprints, and *more edges*. Graph UIs are the canonical infinite-browse pattern; `mutates_into` chains are literally guided rabbit holes with historical depth; shadow nodes are teasers for content that doesn't exist yet (the cliffhanger mechanic). The brand says "the algorithm pulls you deeper — this is the exit," and the feature as specced is a beautifully-lit second entrance. There's also a quieter failure: the map makes narrative-consumption feel *virtuous* ("I'm doing epistemics!"), which removes the guilt that might otherwise cap a binge. And an engagement-metric trap: if the team ever optimizes map dwell time upward, the product has formally switched sides.

### Guards
- **G6.1 — The verdict layer is the default; the map is the appendix.** The user's first view of a question is a *closed-form summary* readable in ~10 seconds: "7 competing answers tracked · 1 clinically established · 2 contested · 4 unsupported · boring baseline: see a GP" plus the top 3 nodes with verdict chips. The full explorable graph sits behind one deliberate click ("see the full map"). Answer-first, exploration-optional — the inverse of the algorithm's structure.
- **G6.2 — Bounded depth.** Cap rendered graph distance at 1 hop from the focal question in the default map view. `feeds` meta-narratives ("modern life is poisoning you") render as a labeled backdrop/region, not as a navigable node that opens *its* own 360 (that's the tunnel).
- **G6.3 — No recommendation surface.** Never render "related questions you might like," "trending narratives," or unprompted shadow-node teasers. Every navigation is user-initiated from something they already searched. The product must not have a feed.
- **G6.4 — Session-completion design.** The map has an explicit end-state ("You've seen all 7 tracked answers to this question"), not infinite scroll or endless expansion. Completion messaging ("that's the whole map") is the anti-algorithm move: the algorithm never says "you're done"; this product always should.
- **G6.5 — Metric guardrail (organizational, not UI).** Success metric for the map is *time-to-orientation* (short) and return-with-new-question rate — never dwell time or edges-expanded-per-session. Write this down now, before there's a growth conversation.

---

## Cross-cutting summary — the five hard gates

If only five things survive to implementation, ship these:
1. **No edge without corpus receipts** (≥3 videos, ≥2 independent channels; edges click through to their citations; model proposes, gates publish) — kills §4 and most of §2.
2. **Human review queue for `supplements` and `shares_clock` edges; category-level naming by default; conduct-verbs replaced with observable phrasing** — kills the §3 legal exposure and the worst §4 case.
3. **Three-tier external-evidence border treatment + mandatory boring-baseline slot, Established-first ordering** — kills §1 flattening at the gestalt level, not the footnote level.
4. **Health questions get the meta-frame title + actionable GP off-ramp node + red-line refusal list + no symptom input** — discharges §5 duty of care with framing that behaves, not disclaimers that don't.
5. **Verdict-summary-first, map-behind-a-click, 1-hop depth, no feed, explicit completion state** — keeps the product an exit, not a nicer-looking entrance (§6).

The unifying test for every future map decision: *does this element help year-one Malik leave in 10 seconds with orientation, or does it give him one more thing to click?* The 360 view survives its own audit only if the map is the receipt — never the ride.