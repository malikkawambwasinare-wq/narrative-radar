# The Narrative System — how narratives are defined, named, graded and collected

Synthesis of three verified research briefs (2026-09-15):
- [01 narrative psychology](01-narrative-psychology.md)
- [02 verdict definitions](02-verdict-definitions.md)
- [03 collection at scale](03-collection-at-scale.md)

Earlier: [psychology of attention](../psychology/SYNTHESIS.md).

---

## 0. Three findings that set the plan

1. **Our current collection breaks YouTube's terms.**
   - YouTube's Terms ban automated access ("robots, botnets or scrapers") without written permission. Our collectors and transcript fetcher read YouTube's pages directly, and so does the daily sweep's no-key route.
   - The official API is the permitted route, but it carries two conditions:
     - titles, descriptions and names must be refreshed or deleted every **30 days**;
     - **derived metrics** — narrative labels, verdicts, momentum — are allowed only under the audited "Analytics & Reporting" exception introduced 2026-06-01.
   - The API also bans combining API data with scraped data.
   - This is a business and legal decision (§6), not a technical one. It is not legal advice.
2. **Search cannot backfill.** Recall for past periods collapses 20–60 days after upload: −64% at five weeks, −92% at ten (Rieder et al. 2025). A five-year corpus has to come from crawling the uploads of known channels. Search is for discovering channels and catching new uploads.
3. **"Every video ever uploaded" is not a defensible claim.** YouTube holds about 10–15 billion videos, and 87% have under 1,000 views. We can collect **every video reachable by documented methods**, with a **measured completeness estimate** (§5). That is honest, and no competitor publishes it.

---

## 1. What a narrative is

**A topic is not a narrative.** "Housing" is a topic. "The US housing crash is coming next year" is a narrative.

A narrative is **a claim that frames a problem, names a cause, and implies an outcome or a remedy**, following Entman's four framing functions. It is **told repeatedly by independent voices over time.**

### The hierarchy

```
Industry  (shelf: Economy & markets, Health & biotech, …)
  └─ Narrative  (the recurring claim)
       ├─ Claims  (checkable statements; dated ones go on the ledger)
       ├─ Camps   (sides of a contested claim)
       └─ Videos  (each with a content verdict + a packaging verdict)
```

### Admission test

A candidate becomes a narrative only if **all** of the following hold:

| # | Test | Rule | Why |
|---|---|---|---|
| 1 | Claim | It states a problem, a cause, and an outcome or remedy — not just a subject | Entman 1993 |
| 2 | Recurrence | At least **3 independent channels** tell it. Reposts of one channel's material count once (repost flag, §4) | Repetition across voices is the strongest persistence mechanism (illusory truth meta-analyses; Weaver 2007: "a repetitive voice can sound like a chorus") |
| 3 | Duration | Told in at least **2 distinct months** | A one-week news spike is an event, not a narrative |
| 4 | Checkability | It can be judged against evidence (health, science) or a clock (markets, politics) | Otherwise it can never be graded |
| 5 | Not a twin | It is not the same core claim and outcome as an existing narrative | Engine duplicate guard |

### One narrative, or two? The slot test

Write each side as one sentence **before** comparing them: *[AGENT] is doing [MECHANISM] to
[TARGET], producing [OUTCOME] by [CLOCK]*. Then check the slots in this order and stop at the
first difference.

| Slot differs | Verdict |
|---|---|
| Outcome | Two narratives |
| Agent, or the blame shifts between accident and intent | Two narratives |
| Mechanism only | One narrative, a mutation — a new season |
| Target only | One narrative, unless the target change moves the outcome |

**Why the agent counts.** People merge stories by role, not by wording. In Bower, Black and Turner
(1979), readers confused "the nurse checked John's blood pressure" with "the dental hygienist
x-rayed Bill's teeth" — sentences sharing no words — because the characters fill the same script
slot. Surface dissimilarity does not stop the merge, so a matcher comparing wording is measuring
the wrong thing. Under this rule "the Fed is killing the dollar" and "BRICS is killing the dollar"
are two narratives, which our earlier mechanism-only rule wrongly fused.

**The abstraction guard.** If two claims can only be merged by climbing to "elites are hiding
something", they are two. The outcome must stay specific enough to be wrong.

**Make it mechanical, not philosophical.** Asking annotators the abstract question "could one
fact-check serve both?" was tried and found unhelpful; replacing it with a concrete judgement
raised agreement to 0.64–0.91 (Kazemi et al. 2021).

---

## 2. The anatomy: why a narrative has a hold

For every narrative, the page shows a "grip profile": which of these ingredients it uses. It is what we mean by "why this story has a hold on you". Ranked by strength of evidence:

| # | Ingredient | Evidence | Detected from |
|---|---|---|---|
| 1 | **Repetition across voices and time** | Several meta-analyses (d ≈ .39–.50); false rumours resurface reworded (Shin 2018) | Corpus over time |
| 2 | **A causal story with identifiable characters** | Transportation meta-analyses; readers raise fewer counter-arguments (ρ = −.20) | Transcript |
| 3 | **A named villain or out-group** | +67% share odds per out-group word (Rathje 2021); villain effect (Zanocco 2018) | Title + transcript |
| 4 | **High-arousal threat** | Anger and anxiety drive sharing (Berger & Milkman 2012); fear appeals d = .29 | Title + transcript |
| 5 | **Threat to people like you** | Threat is the strongest correlate of conspiracy belief (r = .34–.56; Bowes 2023) | Title ("your savings") + transcript |
| 6 | **A remedy** (often sold) | Entman's fourth function; fear appeals work better with an action to take | Transcript (+ pitch flag) |
| 7 | **A clock that can slide** | "Off on timing" excuses (Tetlock 2005). *When Prophecy Fails* is discredited (Kelly 2025): hard, falsified deadlines end movements; **vague and moving ones keep them alive** | Ledger (deadline moves) |
| 8 | **A trusted creator** | Parasocial meta-analysis, correlational | Channel concentration |
| 9 | **Hidden truth / insider status** | Weak (r = .16; marginal replications) | Title ("the truth about…") |
| 10 | **An unresolved question** | Drives clicks; no evidence it helps a story endure (Zeigarnik is unsupported) | Title |

**Ingredient 7 is our strongest durability signal.** A narrative whose deadline has moved twice is being kept alive by the move itself. The ledger's "deadline moved ×2" is therefore a central explanation, not a footnote.

---

## 3. The naming system

Grounded in three briefs: [naming psychology](04-naming-psychology.md), [naming across
fields](05-naming-across-fields.md), [narrative as a belief system](06-narrative-as-belief-system.md).

**Why this matters more than it looks.** Allport and Postman measured what survives as a story
travels: details level out, but the label does not — "when a scene is set, the label conferred
upon the incident tends to remain unchanged." The name outlives the page, the corpus and the
evidence. It is the most durable thing we publish.

### Four layers, because six fields independently arrived at the same architecture

Library cataloguing, folklore indexing, rumour research, fact-checking, disease naming and
extremism research all converge on: a stable meaningless identifier, one authorised name, a
register of variant wordings, and a dated note for every change.

| Layer | Job | Rule |
|---|---|---|
| **ID** | A stable address | Never changes, even when every name does. Links must not rot. |
| **Claim name** | What believers claim | Attributed, never asserted. A believer must accept it as fair. |
| **Hook** | What we found | The strongest thing the corpus proves, in one line. |
| **Variants** | Every other wording seen in the wild | Searchable, never displayed as the name. Records that two phrasings are one narrative. |

The fields disagree on exactly one point: cataloguing says use the group's own words, amplification
research says never use the aggressor's insider language. Both resolve the same way, and this is
how the Library of Congress settled "Illegal aliens": the believers' phrasing lives in the variant
register where search can find it, and the authorised name describes the claim neutrally.

### The hook: one line, one finding, five shapes

| Shape | What it states | Example |
|---|---|---|
| **tally** | A count that lands | Nearly 1 in 3 Anti-Inflammatory Videos Sells Something |
| **clock** | A date that moved, or one that passed | 7 Collapse Deadlines Have Passed. None Landed. |
| **split** | How the sides divide | 64 Channels Say Your Gut Explains Everything |
| **scale** | The volume being pushed | AI Agents Write the Code: 1,541 Videos, 155 Channels |
| **contest** | The competing explanation, where nothing is provable yet | Canada's Condo Crash: Banking Crisis or Contained Slump |

**Never a question.** This replaces the rule written on 18 September, which allowed a question as
the fallback. A question in a name implants the proposition at d ≈ 0.43–0.50, against d ≈ 0.66–0.72
for flatly asserting it (Letourneau & Gawronski 2024, preregistered replication of Wegner 1981,
N = 506). It raises endorsement a week later (Clifford & Sullivan 2023), and readers rate the
format least credible. It spreads the claim at roughly seventy per cent of assertion strength with
none of the accountability. Where uncertainty must be carried, the **contest** shape names the
competing explanation, which is the one format measured not to spread the claim.

### The rules, machine-checked by `scripts/title_check.py`

1. 60 characters or fewer. Google's claim-review standard independently caps claim text at 75 for the same reason.
2. Never a question.
3. No em dash, and no descriptive tail after one.
4. No fear word beside an urgency word, and never shouty. Disease-naming standards ban fear words outright; we allow the claim's own subject noun, because a narrative about a crash cannot be named without the word, but we never add fear the narrative does not carry.
5. At most two figures, each audited. Numbers raise credibility, but decorative precision reads as incompetence to expert readers (Loschelder 2016) and a wrong figure anchors judgement even after retraction (Stubenvoll & Matthes 2021). Two is a deliberate deviation from the brief's "at most one": a moved deadline needs both numbers to show the move.
6. Every number still exists in the corpus within 15%, re-derived on every run. `title_basis` records the figures.
7. Name the claim, never the believer. No "truthers", no "crowd", no pejorative category word — and note that calling something a conspiracy theory does not reduce belief in it anyway (Wood 2016; Douglas et al. 2022), because readers apply that label themselves.
8. Descriptive, never contemptuous. Freedom-threatening language raises anger and counter-arguing and cuts persuasion (Li & Shi 2026, 33 samples).
9. Keep a name stable. Rewrite only when its basis drifts materially, and record the former name with the date.

**What we do not claim.** Nobody has tested a short public name for a recurring claim. Every rule
above is transferred from headlines, tags and warning labels. The attributed form we use for claim
names is untested, and two ideas that once justified it — familiarity backfire and the concreteness
effect — both failed replication. The rules stand on the strongest adjacent evidence, not on proof.

## 4. The verdict standard, v2: two axes, one answer each

**Why v1 was ambiguous.** One field mixed two questions. *Whose material is it?* and *Does the title deliver?* are independent. A genuine Dalio interview (original content) with an invented "60% crash" title (clickbait packaging) forced graders to pick one.

### Content axis (transcript)

**Step 0.** Split the transcript into UPLOADER speech and BORROWED material.
- B = share of runtime that is borrowed.
- Transcript under 80% of runtime, or speakers indistinguishable → **UNGRADED**.

| Step | Question | Yes | No |
|---|---|---|---|
| Q1 | Is B ≥ 50%? | Q4 | Q2 |
| Q2 | Does the uploader's own first-hand material (own reporting, data, interview, testimony) carry the main claim? | **ORIGINAL** | Q3 |
| Q3 | Does the uploader add a substantive contribution — a new argument, counter-evidence, or a synthesis of 2+ sources — nameable in one sentence with a timestamp? | **COMMENTARY** | **RECYCLED** |
| Q4 | Does the uploader's own analysis (≥ 15% of runtime) target the borrowed material ("critical bearing", *Campbell* 1994; *Warhol* 2023)? | **COMMENTARY** | **RECYCLED** |

**Tie-breakers**
- **Main claim:** the main claim decides mixed videos.
- **Burden of proof:** COMMENTARY needs a named contribution with a timestamp. No named contribution → RECYCLED.
- **Delivery:** AI voice or editing effects are irrelevant; the script decides.
- **Own material:** a channel reusing its own material stays ORIGINAL, with **repost = true**. It counts once toward recurrence.
- **Permission:** licensed clips with nothing added are RECYCLED.

### Packaging axis (title + thumbnail vs transcript)

**P1. List every CORE promise.** A named person, an event stated as fact, a number, a date, a prediction, a revelation, "full" / "leaked" / "exclusive". Everything else is a STYLE element: caps, superlatives, emotion.

**P2. Score each CORE promise.**

| Score | Meaning |
|---|---|
| DELIVERED | A timestamped passage provides it |
| WEAKENED | Present, but smaller or hedged |
| ABSENT | Missing, or deferred to "part 2" or a link |
| CONTRADICTED | The video says otherwise |

**P3. Verdict.** Apply in order and stop at the first match.
1. **CLICKBAIT** if any CORE promise is ABSENT or CONTRADICTED, or the title states as fact what the video presents as unconfirmed.
2. **OVERSTATED** if everything is delivered but something is weakened or inflated by style.
3. **ACCURATE** otherwise.

Intent is never judged. This is YouTube's own "does not deliver what was promised" test.

### Stored per video

```json
"content":   {"verdict": "ORIGINAL|COMMENTARY|RECYCLED|UNGRADED", "repost": false,
              "borrowed_share": 0.1, "contribution": {"sentence": "...", "t": 754}},
"packaging": {"verdict": "ACCURATE|OVERSTATED|CLICKBAIT",
              "promises": [{"type": "number", "status": "ABSENT", "t": null}]}
```

The `contribution.sentence` is our own summary, not a quote.

### What gets published (Krippendorff's α, per axis)

| Agreement | What is published |
|---|---|
| α ≥ .80 | Per-video verdicts |
| .667–.80 | Aggregate shares only, marked provisional |
| < .667 | Nothing; revise the codebook |

**How agreement is measured**
- Pilot on 30 videos.
- Reliability sample: the larger of 50 videos or 10% of the corpus, blind and independent.
- **The model grader counts as a coder and must pass against a human.**
- A rolling 10% is double-coded to catch drift.
- For reference: impression-based clickbait judgments reach κ 0.21–0.36; a structured framework about 0.65. Clearing .80 needs the promise-by-promise check above.

### Migration from v1

| v1 verdict | v2 |
|---|---|
| ORIGINAL | ORIGINAL (packaging pending) |
| DERIVATIVE | COMMENTARY or RECYCLED — needs Q3/Q4 |
| RECYCLED | RECYCLED |
| CLICKBAIT | content pending; packaging CLICKBAIT |

Nothing is re-published under v2 until the reliability gate passes.

---

## 5. Collection architecture

**Industry layer**
- Our eleven shelves (plus Unsorted), each with a written definition and seed vocabularies. They live in `industries.json`.
- YouTube's topicCategories and uploader categories are weak signals only. When coders agree on a category, it matches the uploader's choice just 28% of the time.

**Discovery (search, API)**
- Rotate queries within the ~20-day recall window: about 24 narratives × 4 calls a day, which covers every narrative every 5 days.
- Store the **channel IDs** from every result. They seed the backfill.

**Backfill (channel crawl, API)**
- Crawl each seed channel's uploads playlist.
- Classify each video's title and description for narrative relevance, and fetch details only for relevant ones.
- For scale: 10,000 channels × 500 uploads ≈ 100,000 units ≈ 10 days of default quota.
- Limits: channels beyond 20,000 uploads, and one-off uploaders that no channel seed reaches.

**Live (push)**
- Push notifications (PubSubHubbub) for new uploads from known channels. Zero quota.

**Completeness per narrative (capture–recapture)**
- List A: search finds. List B: channel-crawl finds that did *not* come from this narrative's search.
- Chapman estimate: N = (nA+1)(nB+1)/(m+1) − 1.
- Completeness = |A∪B| / N, with a 95% interval.
- **Labelled an upper bound**, because popular videos are easier to find by both methods. Checked against a small gold set built outside YouTube.

**Public definition of "all"**
> "As of [date], every public video published in [window] whose title, description or tags express [claim], reachable by our documented methods, with an estimated total and interval. Excluded: claims made only in speech, private or deleted videos, back catalogues beyond 20,000 per channel, languages outside [L]."

**Transcripts** are the one layer the API cannot give: others' captions are not downloadable. The compliant sources are:
- official podcast feeds (many publish transcripts; otherwise their audio is published for download and can be transcribed locally);
- transcripts creators publish themselves;
- creators who opt in.

**Quota for 11 industries × 10 narratives**
- Default quota covers the live rotation and a slow backfill, about 10 days per 5 million crawled records.
- Faster backfill, more than 100 searches a day, and storing derived metrics beyond 30 days all need the **audit**.
- Realistic first completeness estimates: about week 10.

---

## 6. The compliance decision

| Route | What it gives | What it costs |
|---|---|---|
| **A. Keep scraping** (today's collectors, transcript fetcher, daily sweep's no-key route) | Everything, including transcripts | Against YouTube's Terms. Blocks already hit us (IP-blocked transcripts). Risk of takedown or legal notice. Any future API access is jeopardised, because mixing the two is banned |
| **B. API only + file the audit** (Analytics & Reporting) | Compliant discovery, backfill, details and stats. Narrative labels and derived metrics allowed once audited | 30-day refresh of titles, descriptions and names. Quota limits. Audit wait of unknown length. **No YouTube transcripts** — those come from podcasts, creators or opt-ins |
| **C. Hybrid** | — | Not viable: the policy bans combining API and scraped data |

**Recommendation: B.** The product's credibility rests on playing fairly with sources. A tool that grades other people's honesty cannot be built on a terms violation, and B is the only route that scales without escalating blocks.

### Decided, 2026-09-16: route B, API only

In force. The daily sweep no longer falls back to YouTube's search page and stops instead, leaving
the corpus untouched, until a `YT_API_KEY` secret exists. `collector.py`, `scripts/enrich_youtube.py`
and `scripts/fetch_transcripts.py` are retired and carry a banner saying so; the data they already
collected stays. Transcripts now come only from podcast feeds, creator-published transcripts and
opt-ins. The pipeline this decision governs is [PIPELINE.md](../collection-engine/PIPELINE.md).

---

## 7. What can be built now, and what is gated

**Buildable today** (no keys, no compliance exposure)
1. `industries.json`: the eleven shelves with definitions, seed vocabularies and weak YouTube-category mappings. Existing narratives assigned to shelves.
2. Narrative schema v2: claim core; frame (problem, cause, remedy, clock); grip-profile ingredients; three name layers; admission-test fields.
3. Claim names rewritten in attributed form (the five in §3).
4. STANDARD.md verdict section v2, as a draft, plus a 30-video pilot set from Anti-Inflammatory Diet for the double-coding test.

**Gated on decisions and keys**
- **Industry-wide harvest and five-year backfill:** API key + route B decision; audit for derived metrics stored beyond 30 days.
- **Transcript layer at scale:** podcast feeds and creator sources (compliant), or an explicit decision on route A.
