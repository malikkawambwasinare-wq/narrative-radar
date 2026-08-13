# Adversarial Review of the Narrative-Relation Typology (v0 → v1)

## Verdict up front

v0 is directionally right but structurally unsound in three places:

1. **`competes` and `mutates_into` are not decidable without the Question.** Both are defined *relative to* "the same question," yet the question is only a label. That makes every competes-edge an O(n²) judgment call with no anchor. **The Question must be a first-class object**, and `competes` becomes mostly *derived*, not annotated.
2. **`shares_clock` is not a narrative-to-narrative relation at all.** It is two narratives pointing at the same *event*. Modeling it as a pairwise edge duplicates the trigger and rots when the trigger resolves. **The Trigger/Clock must also be a first-class object.**
3. **v0 has no way to represent the anti-narrative.** "Seed oils are fine" is not a competitor for the energy question — it answers nothing about tiredness. It exists solely to negate one answer. Without a `counters` type, the 360 view can only ever show believers, which quietly recreates the rabbit hole the product exists to escape.

Two of the five v0 types survive unchanged (`supplements`, `feeds`), two are restructured (`competes`, `shares_clock`), one is demoted to evidence-gated (`mutates_into`), and one is added (`counters`). One candidate type (`co_travels`) is deliberately kept **out** of the annotator vocabulary — see below.

---

## Part 1 — Stress-test findings

### 1a. Does `mutates_into` collapse into `competes` + time?

**Almost, but no — and the difference is exactly the product's value.** Two answers to the same question that merely succeed each other chronologically are just sequential competitors (keto → carnivore for "what should I eat" — carnivore didn't *descend* from keto's refutation; both are still alive and fighting). Mutation requires an **inheritance signal**: the same demand, and demonstrably the same *supply chain* — shared promoters migrating, explicit reframing content ("what we used to call adrenal fatigue is really mitochondrial dysfunction"), or audience fingerprints flowing from one to the other.

Hardening: `mutates_into` survives, but as a **retrospective, evidence-gated** edge. It should never be asserted between two currently-live narratives (that's `competes`); it is confirmed only when the source narrative's corpus has demonstrably declined AND at least one inheritance signal is on file. This also means the annotation UI should demand the evidence, not just the edge.

### 1b. Is `feeds` just a bigger `competes`?

No — but only if the Question object exists to prove it. "Modern life is poisoning you" does not compete with "mitochondrial dysfunction" because they answer **different questions at different granularity**. The meta-narrative answers "what's wrong with the modern world"; belief in it raises the prior on *every* poisoning-flavored answer downstream. The clean rule: **competes is within-question; feeds is cross-question.** Without a Question node this distinction is vibes; with one, it's a query.

Bonus: `feeds` also absorbs generic→specific specialization ("AI is a bubble" feeds "the AI bubble pops in 2026") — the general claim answers a broader question and raises the specific claim's prior. No separate `instance_of` type needed in v1.

### 1c. Does `supplements` collapse into `feeds`?

They are both dependency relations, which is why they feel similar — but the dependency runs in **opposite directions** and fails differently. Test with refutation propagation:

- **Supplements:** if the *target* is refuted, the *source* collapses entirely. If mitochondrial dysfunction isn't the cause of fatigue, NAD+ protocols for fatigue are pointless. The supplement is parasitic on the answer.
- **Feeds:** if the *parent* is refuted, the *child* is weakened but can survive on its own evidence. Microplastics research doesn't die if "modern life is poisoning you" falls out of fashion.

Distinct types. Keep both.

### 1d. Missing type: the anti-narrative (`counters`)

Confirmed missing, and it's the most important addition. "Seed oils are fine, the fear is overblown" has a corpus, promoters, predictions, and its own receipt strip — it is a full narrative whose *thesis is the negation of another narrative's thesis*. It must not be forced into `competes` (it proposes no rival answer to the question) and it cannot be a mere flag on the target (debunk campaigns have their own clickbait economy and their own track record worth scoring).

Product payoff: each answer-card in the 360 view can show its strongest counter-narrative alongside it. That is the difference between "comparison shopping among believers" and an actual exit.

### 1e. Missing type: co-travelers — deliberately excluded from annotation

Narratives that always appear together without competing ("seed oils are poison" + "carnivore fixes everything" share an influencer ecosystem) are real, but `co_travels` as an annotator-assignable type is a **grab-bag hazard**: it becomes the dumping ground for every edge an annotator can't classify, and it encodes correlation as if it were structure. Decision: `co_travels` exists only as a **computed edge** (corpus co-occurrence + shared-promoter overlap above thresholds), never hand-asserted. High co-travel score with no typed edge is precisely the *queue signal* that a typed relation is waiting to be discovered — often a hidden `supplements` (carnivore is arguably the *remedy product* of the seed-oil narrative) or a hidden `feeds`.

### 1f. Should the Question be a first-class object? — Yes, and it's not close

Four independent arguments converge:

1. **Decidability:** `competes`, and `mutates_into` are literally defined as "same question." A label can't be joined on; an object can.
2. **Complexity:** with a Question node, competes is derived from `answers` edges — N edges instead of N² pairwise judgments, and automatically consistent.
3. **Search:** questions have their own fingerprints — "why am I always tired" is *exactly what users type*. The question is the natural entry point; the 360 view **is** the question's page.
4. **Multi-membership:** "seed oils" answers tiredness AND obesity AND heart disease. `answers` must be many-to-many with a salience weight — which is a feature: one narrative correctly appears in several 360 views with different prominence.

Cost to accept: question boundaries are fuzzy ("why am I always tired" vs "chronic fatigue causes" vs "why is everyone tired now"). Questions therefore need aliases/fingerprint merging, same as narratives already do. That's paying a known cost once instead of paying it implicitly on every edge forever.

### 1g. Is `shares_clock` a relation at all?

No. "10yr Treasury above 5%" is a **thing** — a falsifiable event predicate with a resolution state — that both the AI-bubble narrative and the carry-trade narrative *watch*. Model it as a **Trigger node** with `watches` edges from narratives; `shares_clock` becomes a trivial derived join. Wins: no pairwise duplication; when the trigger fires or dies, every watching narrative updates from one place; triggers plug directly into the Receipt Strip's "next falsifiable date" gate, which the product already computes. Guardrail: a trigger is an **event predicate, not a calendar date** — "AGI by 2027" and "financial crisis in 2027" share a year, not a clock.

### 1h. Symmetry and inverses

| Relation | Directed? | Inverse (display name) |
|---|---|---|
| answers | N → Q | "answered by" |
| competes | symmetric (derived) | itself |
| supplements | directed | "ridden by / monetized by" |
| feeds | directed | "downstream of" |
| counters | directed | "countered by" |
| mutates_into | directed (temporal) | "mutated from" |
| watches | N → Trigger | "watched by" |
| co_travels | symmetric (computed) | itself |

Note on `counters`: the *logical* content is symmetric negation, but the *sociological* edge is directed — point it from the narrative framed as a rebuttal (usually later-born, defined by reference to its target). Two independently-arising contradictory narratives may carry both edges.

---

## Part 2 — Hardened v1 typology

### Entities

- **Question** — a durable demand for explanation, with fingerprints/aliases and a born date. The 360 view renders a Question.
- **Narrative** — an answer (tracked tile, or untracked shadow stub), exactly as today.
- **Trigger** — a falsifiable event predicate with a resolution state (pending / fired / expired).

### Relations

**1. `answers` (Narrative → Question, salience-weighted) — the primitive**
- *Definition:* the narrative offers a causal explanation or prediction that resolves this question.
- *Decision rule:* would a believer of this narrative cite it, unprompted, when asked this question? If the narrative only matters *given* another answer is true, it's `supplements`, not `answers`.
- *Examples:* "mitochondrial dysfunction" answers "why am I always tired?"; "the 80-year debt cycle is ending" answers "is a huge financial crisis coming?"
- *Boundary case:* "you're not tired, you're depressed" — an answer, or a **reframing of the question itself**? v1 rule: if it names a cause and the questioner recognizes their question in it, it answers (low salience if the reframe is strong). Persistent reframers may justify a Question-to-Question alias/split in v2.

**2. `competes` (Narrative ↔ Narrative, derived) — rival answers**
- *Definition:* two live narratives that both answer the same Question. Derived from co-`answers`; hand-assertable only against shadow stubs whose Question isn't modeled yet.
- *Decision rule:* same Question, same granularity, both currently accumulating corpus. If granularity differs → check `feeds`. If one is dead → check `mutates_into`. If one merely negates the other → `counters`.
- *Examples:* sleep debt vs. vitamin D deficiency for tiredness; "AI bubble pops" vs. "this time it's a real productivity revolution" for "is AI overvalued?"
- *Boundary case:* "it's ALL of these — modern life attacks you on every front" — a competitor, or a coalition that absorbs all rivals? v1: it answers the broader question, so it `feeds` the specific answers rather than competing with them.

**3. `supplements` (Narrative → Narrative, directed) — rides the answer**
- *Definition:* source's value proposition presupposes the target narrative is true; typically monetizes, extends, or operationalizes it.
- *Decision rule (refutation test):* if the target were conclusively refuted tomorrow, does the source's pitch collapse entirely? Yes → supplements. Merely weakened → feeds (inverted) or nothing.
- *Examples:* NAD+ protocols → mitochondrial dysfunction; "buy gold now" content → "the 80-year debt cycle is ending."
- *Boundary case:* red-light therapy — began as a supplement to the mitochondria answer, but has since grown its own direct corpus ("red light fixes fatigue"). A supplement that **graduates into a competitor** legitimately holds both edges; the corpus split between "presupposing" and "standalone" content decides the weights.

**4. `feeds` (Narrative → Narrative, directed) — upstream prior-raiser**
- *Definition:* source answers a broader Question, and belief in it raises the prior on the target.
- *Decision rule:* different Questions, with source's question strictly more general; source's believers are disproportionately likely to adopt the target, but the target survives the source's refutation on its own evidence. Same question → competes. Total dependency → supplements.
- *Examples:* "modern life is poisoning you" feeds seed-oils, microplastics, and EMF narratives; "institutions are lying to you" feeds nearly every contrarian health and finance narrative on the platform.
- *Boundary case:* "chronic inflammation is the root of all disease" — meta-narrative feeding specific answers, or itself a direct competing answer to "why am I tired?" v1: both edges allowed, corpus-weighted; when a meta-narrative gets used as a direct answer, that dual role is a finding worth surfacing, not an annotation error.

**5. `counters` (Narrative → Narrative, directed) — the anti-narrative *(new)***
- *Definition:* source's central thesis is the negation or refutation of the target's central thesis; it proposes no rival answer of its own to the target's Question.
- *Decision rule (negation test):* can the source be stated as "target's claim is false" with nothing essential left over? Yes → counters. If it also asserts its own answer to the question ("adrenal fatigue isn't real — it's undiagnosed depression"), it earns **two edges**: counters the old answer AND answers the question.
- *Examples:* "seed oils are fine; the fear is cherry-picked rat studies" counters "seed oils are poison"; "there is no 80-year debt cycle; it's pattern-matching on two data points" counters the debt-cycle narrative.
- *Boundary case:* competing answers implicitly negate each other ("it's sleep debt" implies "it's not seed oils") — only under an exclusivity assumption the creators rarely make. v1: `counters` requires the negation to be the content's *explicit thesis*, not an implication of holding a rival view.

**6. `mutates_into` (Narrative → Narrative, directed, retrospective, evidence-gated)**
- *Definition:* the target is the historical successor answering the same Question for substantially the same demand, with demonstrable inheritance.
- *Decision rule:* (a) same Question; (b) source's corpus demonstrably declined before or as the target rose; (c) at least one inheritance signal on file — shared promoters migrating, explicit reframing content, or audience-fingerprint flow. All three or it's just sequential `competes`. Never asserted between two currently-live narratives.
- *Examples:* adrenal fatigue (2000s) → mitochondrial dysfunction (2020s); candida overgrowth (1990s) → leaky gut (2010s) → gut microbiome (2020s) — a chain, which is the product's money shot.
- *Boundary case:* adrenal fatigue never fully died — it persists in older wellness corners. **Mutation without death**: v1 accepts "demonstrably declined," not "extinct," and notes that a later *revival* of the source is the question-level analogue of the corpus-level RECYCLED label — a resonance worth surfacing in UI.

**7. `watches` (Narrative → Trigger) — replaces `shares_clock`**
- *Definition:* the narrative's fate is materially tied to the trigger's resolution.
- *Decision rule:* the trigger must be an event predicate ("10yr yield closes above 5%"), not a shared date; the narrative's own prediction ledger must contain a claim the trigger would resolve. `shares_clock` between narratives is then a derived join on shared Trigger nodes.
- *Examples:* "10yr above 5%" watched by AI-bubble-pop and yen-carry-unwind; "frontier model autonomously completes a full SWE job" watched by AGI-by-2027 and white-collar-jobs-collapse.
- *Boundary case:* soft/vague triggers ("when the next recession hits") — is that an event predicate? v1: only if it can be operationalized to a resolvable criterion (e.g. NBER declaration); otherwise it's rhetoric, not a clock — the same falsifiability bar the Receipt Strip already enforces.

**8. `co_travels` (computed only — not in the annotator vocabulary)**
- Corpus co-occurrence + promoter overlap above thresholds, surfaced as an evidence layer. High co-travel with no typed edge = a queue item saying "there is probably a `supplements` or `feeds` edge here you haven't found."

### Annotator decision tree (order matters)

1. Is the source's thesis the *explicit negation* of the target's? → **counters** (stop, unless it also proposes its own answer — then add **answers**).
2. Does the source's pitch *collapse entirely* if the target is refuted? → **supplements**.
3. Do they answer the **same Question** at the same granularity?
   - Both live → **competes** (usually derived automatically from `answers`).
   - Source declined + inheritance evidence → **mutates_into**.
4. Does the source answer a *broader* Question and raise the target's prior? → **feeds**.
5. Is the connection really a shared falsifiable event? → attach both to a **Trigger** via `watches`; assert no narrative-to-narrative edge.
6. None of the above but they obviously travel together? → assert nothing; let **co_travels** compute, and flag for review.

---

## Part 3 — Change log v0 → v1, and open questions

**Changed:**
- `competes` — kept, but derived from a first-class Question via `answers`; hand-annotation only for shadow stubs.
- `shares_clock` — replaced by Trigger nodes + `watches`; the pairwise relation becomes a derived join.
- `mutates_into` — kept, demoted to retrospective and evidence-gated (three-part rule).
- `supplements`, `feeds` — kept as-is, now separated by the refutation test and the cross-question rule respectively.

**Added:** `counters` (the anti-narrative — the single biggest gap in v0); Question and Trigger as entities; `co_travels` as computed-only evidence.

**Open for v2 (deliberately deferred):**
- Question-to-Question relations (reframes, splits, aliases) — needed once reframing narratives ("you're not tired, you're depressed") accumulate.
- Whether `feeds` should eventually split out an explicit `specializes` (generic claim → dated instance) once prediction-ledger tooling wants to roll specific-claim outcomes up to the generic narrative's score.
- Edge lifecycle: supplements-that-graduate and revived mutation sources show that edges need timestamps and possibly deprecation states, not just existence.

**One-line summary:** v1 = 2 new entities (Question, Trigger), 6 assertable relation types (answers, competes*, supplements, feeds, counters, mutates_into — *competes mostly derived), 1 structural edge (watches), 1 computed layer (co_travels), plus an ordered decision tree that makes each edge a test result rather than a judgment call.