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

**Mutation vs new narrative.** A change of **mechanism** with the same outcome is a mutation, i.e. a new season. Example: the collapse is now caused by AI capex instead of debt. A change of **outcome** is a new narrative.

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

Every narrative has three names, each with a different job.

| Layer | Job | Rule | Example |
|---|---|---|---|
| **ID** | Stable address | Neutral topic slug; never changes | `housing-crash-watch` |
| **Claim name** (card heading) | Say what the story claims without adding belief | **Attribute it; never assert it.** A name is itself one more repetition, so a bare "Seed Oils Are Poison" adds fluency to the claim. It passes if a believer would call it a fair statement of what they believe | *The "housing crash is coming next year" story* |
| **Hook title** (tile) | Earn the click honestly | See the rules below | *Housing Crash: Is It Always Next Year?* |

**Hook title rules**
1. It keeps the narrative's search terms.
2. It opens a concrete gap that the page answers. Headlines perform best at intermediate concreteness (Aubin Le Quéré & Matias 2025).
3. It states a pattern only when our data establishes it; otherwise it asks a question.
4. It passes our own title-bait lexicon.
5. It adds no villain, out-group or moral-emotional words the narrative doesn't use.
6. It never casts believers as fools, and never makes Narrative Radar the hero.

**Formula:** *[the claim in its believers' words] + [the tension our data can show]*

**Current claim names that assert instead of attribute — fix these:**
- "Inflammation Is the Root of All Disease"
- "The Coming US Debt Collapse"
- "The CIA Proved Remote Viewing Works"
- "Open-Source AI Has Caught Up"
- "Now Is the Generational Buying Opportunity"

---

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

The decision is the founder's.

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
