> **Note:** Everything below came from web research; no repository files were read or modified. The one empirical caveat is stated in §6 — there is no direct evidence that thesis templates improve real-world articulation, so the recommendation is assembled from adjacent literatures and should be tested, not assumed.

---

# LENS 1 — Framework Archaeology & Structural Stress-Test

## 0. BLUF (used here as it should be used — for delivery, not for thinking)

**The founder's structure is roughly correct in shape and wrong in its highest-traffic field.** Five of seven fields are load-bearing. But `WHY (2-3 reasons)` is the one field every user will spend the most time in, and the psychology literature says the "enumerate reasons" format is *specifically the version that does not work* — and may actively increase overconfidence. It must be rewritten as **mechanism**, not reasons.

Three further structural corrections:

1. **`CONFIDENCE` is two variables fused into one.** The IC separates *likelihood* from *confidence in the basis* deliberately. This product can compute half of the second one from data it already has.
2. **The order of formation must not equal the order of presentation.** He has proposed a BLUF *display* order as a *thinking* order. Eliciting POSITION early anchors the user and turns everything after it into rationalisation.
3. **The single most valuable thing here is already built and mislabelled.** Mutation history + "clock moved N times" is a Lakatos progressive/degenerating test. It is currently reported as a neutral count. Made principled, it is a defensible, non-truth-asserting metric no competitor has.

Rejections are in §5. They are real rejections, including of one feature that is the obvious thing to build next (ACH).

---

## 1. Framework archaeology — borrow / reject

### Minto: Pyramid Principle, SCQA, MECE

**Borrow:** SCQA as the *framing* engine, because its output is a **Question** — and this product is already question-centric (the 360 map's organising unit is "the QUESTION this narrative answers"). That alignment is fortunate and should be exploited: SCQA is the on-ramp that generates the map node.

Also borrow Minto's genuinely underrated rule: supporting points must sit at the **same level of abstraction** and must answer the question the governing thought provokes. Lay users reliably produce a mixed bag — one mechanism, one datapoint, one vibe — and experience it as three reasons. It is one reason plus noise.

**Reject: MECE applied to evidence.** This is a category error for this product, and a sharp one. MECE was built for *problem decomposition* (issue trees), not evidence aggregation. This product's evidence is *definitionally overlapping* — DERIVATIVE and RECYCLED labels exist precisely because sources are not independent. The "source concentration" metric in the Radar Read *is a measurement of non-mutual-exclusivity*. Forcing MECE onto the corpus would erase the product's best insight. Keep MECE only for the answer-space layer (what are the rival answers to this question), which is what `competes` already does.

**Reject:** the Pyramid's assumption that the governing thought is a *recommendation*. Critiques note it fails when you have no recommendation yet. Here the governing thought is frequently "this is contested, and here is the shape of the disagreement" — which is a legitimate terminal output, not a failure state.

### BLUF (military/intel origin)

**Borrow:** for output only. The nut-graf and BLUF traditions agree — lead with the point.

**Reject as a thinking order.** Documented failure modes: it reads as cold or evasive when the content is bad news, it stifles exploration when the conclusion isn't formed yet, and it does not mean "be shorter" (a widely-made error). The failure mode that matters most here is **premature commitment**: state the bottom line first and the analyst reverse-engineers support for it. Applied to a general-audience epistemics tool this is severe — a product that asks "what's your position?" on screen one has manufactured an opinion before the user has met the opposition.

### Toulmin — is *warrant* the missing piece?

**Yes as a function; no as a field.** The warrant — the unstated inferential link from grounds to claim — is precisely what's absent from the founder's structure. Map it:

| Toulmin | Founder's field |
|---|---|
| Claim | POSITION ✅ |
| Grounds | WHY (partially) ⚠️ |
| **Warrant** | **absent** ❌ |
| Backing | the corpus ✅ (implicit) |
| Qualifier | CONFIDENCE ✅ |
| Rebuttal | COUNTERWEIGHT ✅ |

So the structure is **Toulmin minus the warrant** — which is the informative diagnosis, since the warrant is the element the pedagogy literature says is hardest. Teachers routinely omit it because students cannot distinguish ground from warrant. **Importing the label "warrant" for an intelligent ordinary user will fail.** Keep the function, drop the vocabulary, and fuse grounds+warrant into a single causal-chain field. §2 shows this converges with two other traditions on the same fix.

### US IC tradecraft — ICD-203, ACH, WEPs

**Borrow (high value): the likelihood ÷ confidence split.** ICD-203 requires products to express *both* the likelihood of the event *and* the analyst's confidence in the basis for that judgment, and to keep the two aligned but distinct. The founder's single `CONFIDENCE` field collapses them. They come apart hard in this domain: you can think a claim is probably right while the evidence base is one guy recycled forty times, or think it unlikely while the sourcing is excellent. **The product already computes a basis-quality proxy** (source concentration, ORIGINAL:DERIVATIVE ratio, resolved-call rate). This is the one place where the corpus can populate the thesis automatically, and it is a strong differentiator.

**Borrow:** the Key Assumptions Check (ICD-203's "distinguish information from assumptions") and "what would change our assessment" — the latter is the direct ancestor of UPDATE CONDITION and validates that field.

**Reject: ACH as a feature.** This matters because a competing-hypotheses grid is the *obvious* thing to build on a 360 map that already has `competes` edges. The research says don't. Dhami et al. (2019) and Chang, Berdini, Mandel & Tetlock (2018) find ACH is vague in multiple respects — unclear how hypotheses are selected, what counts as consistent/inconsistent evidence, or how diagnosticity is judged; it provides no mechanism for revising priors and is prone to **base-rate neglect**; ACH-trained analysts did not follow all its steps; and its popularity is "surprising given the dearth of empirical research testing its utility."

**Borrow the one cheap part of ACH: diagnosticity.** "Which evidence actually discriminates between the camps?" is worth more than the matrix. And note this is already modelled — **`shares_clock` (same falsifiable trigger) *is* a diagnostic test.** Surface it as such.

**Words of estimative probability — borrow the problem, reject the solution.** Kent's 1964 finding is that readers understood "probable" as anywhere from 30% to 75%. Virtually all intelligence organisations still use curated verbal sets "despite the well-documented shortcomings... most of which could be obviated by the use of numeric probabilities" (Barnes 2016; Dhami, Mandel, Mellers & Tetlock 2015). So: **numbers primary, words as labels** — never words alone.

### Bayesian updating / Tetlock

**Borrow:** the outside-view habit ("how often do things of this sort happen in situations of this sort"), and frequent small updates — superforecasters update more often and in smaller increments, and granularity predicts accuracy.

**Reject the granularity finding's naive transfer.** Granularity predicts accuracy *among superforecasters*, where it carries signal. Novice granularity is noise wearing a lab coat. For a product whose founding wound is *"strategies presented as working models,"* false precision is a brand-level betrayal. Use coarse numeric bands.

**Borrow, importantly:** calibration training works mainly by *lowering* confidence — training "reduced confidence levels, which translated into reduced overconfidence and better overall calibration." The correct direction of travel for this product is down, not up.

**The base-rate insight this product uniquely owns:** clean base rates don't exist for most narrative questions. But two *domain-specific* ones do, and they're already in the database: **"this named predictor has landed X of Y resolved calls"** and **"narratives of this shape have moved the clock N times."** That is a real base rate almost no one else can supply. It is the single strongest argument for why this product can do Portable Thesis better than a general-purpose chatbot.

### Popper vs Lakatos — the crown jewel

Popper's naive falsification is *wrong for this domain*: narratives don't die on refutation, they mutate — which the product literally measures.

Lakatos gives the precise criterion. A programme has a hard core plus a protective belt of auxiliary hypotheses. A modification is **progressive** if it yields *novel predictions* that are then corroborated; **degenerating** if the auxiliary hypotheses only explain away existing anomalies after the fact without predicting anything new (*ad hoc* adjustment). Lakatos's own example: 20th-century Marxism, whose adherents "constantly modified auxiliary hypotheses to accommodate events after the fact, without ever predicting novel phenomena in advance."

**Product implication — the highest-leverage idea in this report:** the Radar Read currently reports "clock moved N times" as a neutral count. Lakatos upgrades it into a principled distinction:

> Did this mutation arrive with a **new, dated, falsifiable prediction** (progressive), or did it only **reinterpret a missed one** (degenerating)?

This asserts nothing about truth. It classifies the *form of the revision*. It sits perfectly inside the existing integrity rules, it's derivable from data already held (mutation history × prediction ledger dates), and it is the most defensible non-truth-asserting signal available in this space.

**And it turns on the user.** The same test can be applied to the user's own saved thesis: when they revise, did they revise progressively or move their own goalposts? That is the founder's story made into a mechanic — year-one Malik moved his goalposts too.

### Steelmanning, dialectics, Rapoport

**Borrow:** Rapoport's rule 1 — restate the opposing view so well its holder says *"thanks, I wish I'd put it that way."* It is the only operationalisable, user-testable steelman criterion in the set.

**Reject AI-generated steelmen — on integrity grounds, and it happens to be the better product.** The charity literature is damning: strong charity "licenses too much alteration of the data," courts ethnocentrism "insofar as making others out to be sensible amounts, in practical terms, to making them out to agree with us," and if they don't in fact have a good argument, "it's falsehood to pretend they do." A generated steelman is also a straight violation of the existing rule that **relations require corpus citations**.

So the counterweight must be a **quoted, attributed, real opposing argument from the corpus**. Every competitor will generate the steelman. This one cites it, by name, with a link. That is both the safe choice and the differentiated one.

**Note the ITT's limit** so the UI doesn't overclaim: being able to pass as a believer and still reject the belief doesn't show the belief is wrong — the rejection rests on further beliefs that may themselves be wrong.

### Decision memos — Amazon, McKinsey, Bezos

**Borrow — and this is a sharper borrow than it looks:** Amazon's ban on bullets. Full prose "with no bullet-point shortcuts" means "you can't hide behind vague points or hand-wave complexity." **Prose forces the connective — *because*, *which means*, *unless*. A bullet list lets you omit it.** The connective *is* the warrant. Amazon's formatting rule is a warrant-forcing device.

**Borrow:** PR-FAQ's working-backwards → write the SO WHAT as the actual sentence you would say out loud, to a named audience.

**Borrow:** "disagree and commit" as a legitimate labelled end-state — *"I'm acting on this while unconvinced"* — which is more honest than forcing confidence upward.

**Reject:** length, and the silent-reading ritual (criticised on accessibility grounds — reading-rate variation, ELL, disability — and for suiting neither visual nor auditory processors).

### Investment thesis

**Borrow (strongest single mechanic):** kill criteria written **and dated before the outcome**. "Pre-written invalidation criteria counter confirmation bias, because the test was chosen before the outcome," and "a dated original document counters hindsight bias, because you cannot claim you always knew." Implication: **a thesis the user can silently edit is worthless.** It must be timestamped, locked, and resurfaced when the trigger date arrives — which also gives the product a legitimate return-visit loop that is *not* dwell time.

**Borrow with surgery:** variant perception ("what do I believe that consensus doesn't"). The product already separates consensus claims from contested claims, so it can *place* the user's position against the corpus for free.

**Reject the valorisation.** Variant perception is a finance concept that pays for being right *and* different. Ported naively to a general-audience epistemics product it becomes "contrarian = smart" — which is the exact YouTube-guru pathology the product exists to cure. Borrow the *diagnostic*, never the *reward*.

### Scientific reasoning — severe testing, pre-registration

**Borrow Mayo's severity, and note the nuance that most people get wrong.** A test is severe if it has a low probability of passing the hypothesis when that hypothesis is false. Crucially, **pre-registration alone does not confer severity** — what matters is "how well the data, together with background information, rules out ways in which an inference can be in error," not whether the hypothesis was written down first.

This is a real upgrade over a bare `UPDATE CONDITION`. Users' natural triggers fail in both directions: too vague ("if the data changes") or so extreme they never fire ("if the dollar collapses"). The field needs a **two-part severity prompt**:
- Would this actually happen if I'm wrong? *(catches never-fires)*
- Could this happen even if I'm right? *(catches non-diagnostic)*

### Journalism — nut graf

**Borrow:** SO WHAT ≈ the nut graf, the "so what?" paragraph that tells the reader why to care. Note the craft placement — the nut graf comes *after* the lead, not first, supporting the two-layer disclosure below.

**Critique of the field as proposed:** the founder names five audiences (work meeting, Slack, investment conversation, memo, classroom, friends). **One SO WHAT cannot serve five audiences.** Either the field takes an audience tag or it degenerates into mush.

---

## 2. Stress-test of the seven fields

| Field | Verdict | Reasoning |
|---|---|---|
| **QUESTION** | **Load-bearing — strongest field** | Native to the 360 map. Add a time bound. |
| **POSITION** | Load-bearing, **but must not be elicited first** | Anchoring; must permit "no position yet." |
| **WHY (2-3 reasons)** | ❌ **Weakest field. Rewrite.** | See below — this is the critical finding. |
| **COUNTERWEIGHT** | Load-bearing, underspecified | Must be cited, not generated. |
| **CONFIDENCE** | Load-bearing, **conflated** | Split per ICD-203; half is computable. |
| **UPDATE CONDITION** | **Best-justified field in the proposal** | Needs severity + date + immutability. |
| **SO WHAT** | Keep, weakest justification | Needs an audience or it's mush. |

### The critical finding: `WHY (2-3 reasons)` is the wrong format twice over

**(a) Reasons don't do what he wants; mechanisms do.** Fernbach, Rogers, Fox & Sloman (2013, *Psychological Science*) asked people to rate their understanding of policies, then explain them, then re-rate. Generating a **mechanistic explanation** punctured the illusion of explanatory depth and **moderated attitudes** — it even reduced donations to relevant advocacy groups. The effect **did not occur when people were instead asked to enumerate reasons for their preferences.**

The founder's field asks for the enumerate-reasons version. That is the arm of the experiment that didn't work. Worse: reason-generation is a known confidence-*inflation* route — the list feels substantial, so certainty rises. For a product whose entire reason to exist is that its founder was confidently misled, **a field that manufactures unearned confidence is anti-mission.**

**(b) "2-3" is a defect as a spec.** The dilution effect: people **average** arguments rather than adding them. Moderate-strength support alongside a strong argument is additive, but **weak support alongside a strong argument reduces the strong argument's persuasive effect.** The third reason is almost always the weakest. The instruction "give 2-3 reasons" therefore instructs users to weaken their own case — and to weaken it *in exactly the setting the product is built for*, saying it out loud to another human.

The correct spec is not "fewer" but **"no weak ones"**: one reason that does the real work, a second only if it would survive alone.

**Three traditions converge on the same fix.** Toulmin's missing warrant, Fernbach's mechanism-not-reasons, and Amazon's ban on bullets are three descriptions of one repair: **force a causal chain in prose containing a connective.** That convergence is the strongest evidence in this report.

### Missing fields, ranked

1. **Mechanism / warrant** — not an added field; a *rewrite* of WHY. Highest leverage edit available.
2. **Key assumption** — ICD-203's information-vs-assumption standard. Distinct from update condition: the assumption is *present-tense and internal* ("this only works if X is true now"); the update condition is *future-tense and external*.
3. **Base rate** — include, but **product-supplied, not user-entered** (predictor hit-rate, clock-moves for narratives of this shape). This is the product's unfair advantage.
4. **Scope conditions** — cheap, high value, prevents overreach. Fold into POSITION as a where/when bound rather than adding a field.
5. **Who disagrees and why** — *already covered*; attribution IS the who. Don't add a field.
6. **Prior vs posterior** — valuable for the mission (it shows users their own updating) but as an **auto-captured log**, not a field to fill in.
7. **"What I'd need to see"** — ~80% redundant with update condition. The 20% that isn't: people specify only *dis*confirmers or only *con*firmers. Solve with **one field, both directions**, not two fields.

---

## 3. Proposed minimal structure

Eight elements, tiered — which fits the existing progressive-disclosure pattern rather than fighting for a magic number. Only the top four are mandatory; **the top four alone are the portable part.**

**CORE — what you can actually say out loud**
1. **THE QUESTION** — product-supplied from the 360 map, user confirms; time-bound.
2. **WHERE I LAND** — position + scope/time bound. *"Not yet — I'm leaning"* is a first-class answer.
3. **BECAUSE** — the mechanism. Prose, one causal chain, must contain a connective. One strong link; a second only if it stands alone.
4. **THE BEST CASE AGAINST** — quoted and attributed from the corpus. Never generated.

**DEPTH — unfolds; what makes it defensible**

5. **RESTING ON** — the key assumption that collapses it.
6. **HOW SURE / HOW SOLID** — two dials. *How sure* = coarse numeric band (user). *How solid* = basis strength (largely computed from source concentration + resolved-call rate).
7. **WHAT WOULD MOVE ME** — dated, severity-checked both directions, **locked on save**.
8. **SO I'D SAY** — the spoken sentence, audience-tagged.

### The order correction (the structural critique of the proposal)

The founder has proposed a **presentation** order as a **thinking** order. Separate them:

- **Formation order:** Question → **Best case against (read first)** → Mechanism → Key assumption → *then* commit to a position and confidence → Update condition → Spoken line.
- **Display order:** BLUF — position first.

Meeting the opposition *before* committing is the difference between forming a position and rationalising one. This costs nothing to implement and is probably worth more than any individual field.

### Two upgrades unique to this product

- **Counterweight seeding by relation type.** `competes` (rival answer) is the ordinary counterweight. **`competes_mechanism` is the most valuable and least encountered** — same conclusion, different reason. It tells the user they may be right for the wrong reason, which means *their update condition is pointing at the wrong dial.* Almost no one meets this argument in the wild.
- **`shares_clock` as the diagnostic test** — the salvageable core of ACH without the matrix.

---

## 4. Risks the new direction creates (not currently covered)

**Portable Thesis moves the product from *describing structure* to *helping a user commit*. The integrity rules must be extended, not merely inherited.**

1. **The product must never draft POSITION or BECAUSE.** It supplies the question, the camps, the citations, the base rates. The user supplies the commitment. If the AI writes the position, the product becomes the thing it was built to replace: a confident voice telling you what to think. This is the load-bearing design constraint of the whole direction.
2. **Health narratives must disable Portable Thesis entirely.** The existing see-a-doctor off-ramp is insufficient here. "Form a position you can articulate to another human" applied to a health narrative produces a user confidently advising a friend against medical advice. This is a *new* gap the direction opens.
3. **SO WHAT tagged "investment conversation" edges toward financial advice.** Needs explicit handling.
4. **A false-precision risk on CONFIDENCE.** Given the founder's story, numeric overconfidence rendered in a clean UI is the highest-severity brand failure available.

---

## 5. Reject list

| Reject | Because |
|---|---|
| ACH matrix | Vague, no priors, base-rate neglect, analysts don't follow steps, thin evidence of benefit |
| MECE on evidence | Category error; the corpus is *definitionally* overlapping |
| Toulmin as a 6-part labelled form | Warrant is the documented failure point in teaching; keep function, drop vocabulary |
| Verbal-only probability ladder | Kent: "probable" read as 30–75% |
| AI-generated steelman | Violates corpus-citation rule; charity literature calls it falsification |
| "2-3 reasons" | Dilution effect — instructs users to weaken their own case |
| Reasons instead of mechanism | Fernbach: the reasons arm produced no moderation |
| Contrarianism from variant perception | Reproduces the guru pathology the product cures |
| Position-first elicitation | Anchoring → rationalisation |
| Forcing a position | Manufacturing opinions is the worst failure mode for *this* product |
| Fine-grained novice probabilities | Granularity carries signal only for superforecasters |
| Amazon length + silent-reading ritual | Accessibility critiques; borrow only the prose rule |

---

## 6. Honest caveat and a proposed test

There is **no direct evidence** that a structured thesis template improves real-world articulation. Fernbach is about attitude moderation; calibration training is about accuracy; dilution is about persuasion. The recommendation is assembled from adjacent findings and should be treated as a hypothesis.

The founder's existing metric (time-to-orientation) does not measure articulation, so it cannot validate this direction. A proposed proxy consistent with the anti-dwell-time commitment:

> **Can the user reproduce their position, its mechanism, and the best case against it 48 hours later, without looking?**

That measures retained understanding rather than engagement — and it is the operational form of "what took him 6 years, in 10 seconds."

---

## Sources

- [The "analysis of competing hypotheses" in intelligence analysis — Dhami et al., Applied Cognitive Psychology (2019)](https://onlinelibrary.wiley.com/doi/full/10.1002/acp.3550)
- [Critical review of the Analysis of Competing Hypotheses technique — Intelligence and National Security](https://www.tandfonline.com/doi/abs/10.1080/02684527.2024.2304934)
- [ICD 203 — Analytic Standards (ODNI)](https://www.intelligence.gov/assets/documents/intelligence-community-directives/ICD_203.pdf)
- [Objectivity — ODNI](https://www.dni.gov/index.php/how-we-work/objectivity)
- [Words of estimative probability — Wikipedia](https://en.wikipedia.org/wiki/Words_of_estimative_probability)
- [Statements of Estimative Probability (Kent) — GlobalSecurity](https://www.globalsecurity.org/intell/ops/probability.htm)
- [Making Intelligence Analysis More Intelligent: Using Numeric Probabilities — Barnes](https://www.tandfonline.com/doi/abs/10.1080/02684527.2014.994955)
- [Verbal probabilities: Very likely to be somewhat more confusing than numbers](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6469752/)
- [Political Extremism Is Supported by an Illusion of Understanding — Fernbach, Rogers, Fox & Sloman (2013)](https://journals.sagepub.com/doi/abs/10.1177/0956797612464058)
- [Fernbach et al. 2013 — full PDF](https://ethz.ch/content/dam/ethz/special-interest/usys/ites/ecosystem-management-dam/documents/EducationDOC/EM_DOC/Fernbach%20et%20al%202013%20Political%20extremism%20is%20supported%20by%20an%20illusion%20of%20understanding.pdf)
- [Illusion of explanatory depth — Wikipedia](https://en.wikipedia.org/wiki/Illusion_of_explanatory_depth)
- [The paradox of argument strength: how weak arguments undermine strong arguments — Scientific Reports](https://www.nature.com/articles/s41598-024-73348-1)
- [The Argument Dilution Effect — FeverBee](https://www.feverbee.com/argument-dilution/)
- [The "dilution" effect and sharper advocacy — Temple Law](https://law.temple.edu/aer/2024/10/31/the-dilution-effect-and-sharper-advocacy-another-less-is-more-tool-for-persuasion/)
- [Imre Lakatos — Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/lakatos/)
- [Methodology of scientific research programmes](https://www.qualityresearchinternational.com/socialresearch/methodologyofscientificresearchprogrammes.htm)
- [Notes on Mayo's Severity — PhilSci Archive](https://philsci-archive.pitt.edu/1782/1/severity.notes.html)
- [Pre-Registration as a Severe Testing Device — The Replication Network](https://replicationnetwork.com/2020/05/13/pre-registration-as-a-severe-testing-device/)
- [Preregistration, severity and deviations — Rubin](https://arxiv.org/pdf/2408.12347)
- [Developing expert political judgment: training and practice in forecasting tournaments — Judgment and Decision Making](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/developing-expert-political-judgment-the-impact-of-training-and-practice-on-judgmental-accuracy-in-geopolitical-forecasting-tournaments/123EB18425391D05FA6581FDBB3F309F)
- [Automated calibration training for forecasters — Stone (2023), JBDM](https://onlinelibrary.wiley.com/doi/full/10.1002/bdm.2334)
- [Evidence on good forecasting practices from the Good Judgment Project — AI Impacts](https://aiimpacts.org/evidence-on-good-forecasting-practices-from-the-good-judgment-project/)
- [Ten Commandments for Aspiring Superforecasters — Good Judgment](https://goodjudgment.com/philip-tetlocks-10-commandments-of-superforecasting/)
- [Taming the Warrant in Toulmin's Model of Argument — ERIC EJ891916](https://eric.ed.gov/?id=EJ891916)
- [Toulmin Argument Model — Writing Arguments in STEM](https://pressbooks.calstate.edu/writingargumentsinstem/chapter/toulmin-argument-model/)
- [Rapoport's Rules — RationalWiki](https://rationalwiki.org/wiki/Rapoport's_Rules)
- [Against steelmanning — Noah Smith](https://www.noahpinion.blog/p/against-steelmanning)
- [A New Approach to Charity — Problems in Argument Analysis and Evaluation](https://ecampusontario.pressbooks.pub/wsia062018/chapter/7/)
- [Introduction to the Special Issue on the Principle of Charity in Argumentation — Topoi](https://link.springer.com/article/10.1007/s11245-025-10331-z)
- [The Ideological Turing Test: A Behavioral Measure of Open-Mindedness](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12519043/)
- [ModelThinkers — Minto Pyramid & SCQA](https://modelthinkers.com/mental-model/minto-pyramid-scqa)
- [MECE principle — Wikipedia](https://en.wikipedia.org/wiki/MECE_principle)
- [BLUF (communication) — Wikipedia](https://en.wikipedia.org/wiki/BLUF_(communication))
- [How to Write an Intelligence Product in the BLUF Format (PDF)](https://courses.physics.illinois.edu/phys280/sp2022/docs-for-assignments/BLUF%20Writing%20Format.pdf)
- [BLUF: The Military Standard That Can Make Your Writing More Powerful — Animalz](https://www.animalz.co/blog/bottom-line-up-front)
- [The Amazon Writing Culture — PRFAQ](https://www.theprfaq.com/articles/amazon-writing-culture)
- [Why the Amazon "six-page meeting" process doesn't work](https://www.linkedin.com/pulse/why-amazon-six-page-meeting-process-doesnt-work-sheri)
- [Kill Criteria: Pre-Setting Your Exit Signals — Angus Munro Psychology](https://www.ampsych.com.au/blog/kill-criteria/)
- [Investment Thesis: Meaning, Structure, and How to Actually Write One — MidhaFin](https://www.midhafin.com/equity-investment-thesis)
- [How to Write an Investment Thesis for an Acquisition — CT Acquisitions](https://ctacquisitions.com/how-to-write-an-investment-thesis-acquisition/)
- [Nut graph — Wikipedia](https://en.wikipedia.org/wiki/Nut_graph)
- [Nut grafs: Seven steps to score a winning story structure — Nieman Storyboard](https://niemanstoryboard.org/2021/10/26/nut-grafs-seven-steps-to-score-a-winning-story-structure/)
- [Nut graf and lead duos — NPR Training](https://www.npr.org/sections/npr-training/2025/05/29/g-s1-64764/nut-graf-and-lead-duos-that-point-readers-in-the-right-direction)