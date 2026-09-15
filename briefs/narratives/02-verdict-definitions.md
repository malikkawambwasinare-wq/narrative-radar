# Research — Operational definitions: clickbait vs original vs commentary vs recycled

Researcher brief, 2026-09-15. Sources were checked, with full text pulled for the key PDFs. Court opinions are quoted (public domain); everything else is paraphrased.

## Part 1. Sources

### Clickbait research

**1. Blom & Hansen 2015**, *Journal of Pragmatics* 76:87–100
- **Rule:** clickbait uses a forward reference ("This is why…") that creates anticipation.
- **Evidence:** 100k Danish headlines; heavier use correlates with commercialisation.
- **Agreement:** not reported.
- **Use:** it names a technique. A forward reference alone is not a failure.

**2. Chakraborty et al. 2016**, "Stop Clickbait", ASONAM
- **Rule:** headlines that lure clicks and often mis-meet the expectation they set.
- **Agreement:** Fleiss' κ = 0.79 across 6 volunteers.
- **Caveat:** Potthast 2018 warns this is inflated, because items came from known clickbait sites vs reputable sites and were easy to separate.

**3. Biyani, Tsioutsiouliklis & Blackmer 2016**, AAAI
- **Rule:** eight types — exaggeration, teasing, inflammatory, formatting, graphic, bait-and-switch (promised thing missing, or behind more clicks), ambiguous, wrong (factually incorrect).
- **Use:** most useful source here. It separates style problems (the first five) from delivery failures (bait-and-switch, wrong). **That split is the OVERSTATED / CLICKBAIT line below.**

**4. Potthast et al. 2018**, COLING; Clickbait Challenge 2017
- **Finding:** a property checklist can't be made operational, and intent is "virtually impossible" to prove, so they measured perceived baitiness on a 4-point scale (5 crowd workers × 38,517 tweets).
- **Agreement:** Fleiss' κ = 0.21 on the 4-point scale; 0.36 when collapsed to two classes; 0.35 on their expert 2016 corpus.
- **Use:** key warning. **Impression-based clickbait judgments are barely reliable.**

**5. Hagen, Fröbe, Jurk & Potthast 2022**, "Clickbait Spoiling", ACL
- **Rule:** clickbait provokes curiosity instead of summarising. A "spoiler" is the short text in the content that satisfies that curiosity: a phrase (42.5%), a passage (40%), or multipart.
- **Evidence:** 5,000 posts, one main annotator with spot checks.
- **Use:** directly applicable. **If the transcript contains the spoiler, the video delivers; if not, it baits.**

**6. Scott 2021**, *Journal of Pragmatics* 175:53–66 (abstract only)
- **Rule:** clickbait overuses definite reference plus superlatives and intensifiers (relevance theory).
- **Use:** style cues. These can push a title toward OVERSTATED, never on their own to CLICKBAIT.

**7. Islam et al. 2026**, "YTClickbait21K", arXiv
- **Method:** 21,238 YouTube videos; three annotators working from a written five-criterion framework (title, thumbnail, cross-modal consistency, engagement, faithfulness), with examples and calibration meetings.
- **Agreement:** mean pairwise κ = 0.651.
- **Caveats:** annotators saw metadata only, and the tie-breaker leans toward labelling clickbait (reverse this).
- **Use:** **a structured framework roughly doubles agreement over impressions.**

### YouTube policy

**8. YouTube Partner Program — reused content** (retrieved 2026-09-15; changelog 2025-07-15 renamed "repetitious" to "inauthentic content", reused-content policy unchanged)
- **Rule:** repurposing others' material without significant original commentary, substantive modification, or educational or entertainment value. The test is whether viewers can see a meaningful difference from the original. It applies even with permission.
- **Allowed:** critical reviews with clips; replays with play explanation; reactions that comment; others' footage with added storyline and commentary; content mainly featuring the creator.
- **Not allowed:** clips stitched with little or no narrative; compilations from other platforms; content uploaded many times by others; mostly non-verbal reactions; readings of material the creator didn't write.
- **Inauthentic content:** mass-produced or templated video, including AI template videos with no original insight.
- **Use:** "readings of other materials" covers AI-narrated restatements.

**9. YouTube spam and deceptive practices** ("malicious clickbait"; the 2024-12-18 "egregious clickbait" enforcement)
- **Rule:** a title or thumbnail that promises something the video doesn't deliver, e.g. "the president resigned!" with no such content, or "full match" on a clip.
- **Use:** YouTube's own test is **delivery of the promise**. Drop the "malicious" (intent) qualifier.

**10. YouTube, "Fair use on YouTube"**
- **Rule:** credit doesn't make a copy transformative. Additions must bring new expression, meaning or message.

### Law

**11. Campbell v. Acuff-Rose**, 510 U.S. 569 (1994)
- **Rule:** does the new work merely "supersede the objects" of the original, or add "something new, with a further purpose or different character"?
- **Rule:** when "commentary has no critical bearing on the substance or style of the original," the claim to borrow diminishes.

**12. Andy Warhol Foundation v. Goldsmith**, 598 U.S. 508 (2023)
- **Rule:** purpose is "a matter of degree." New meaning or message is "not, without more, dispositive." Commentary that targets the original may need to borrow from it ("conjure up"); borrowing that is "merely helpful" is not enough.
- **Our rule:** **repackaging is COMMENTARY only if the additions target the borrowed work and contribute something new. Reframing alone doesn't count.**

### Journalism source typology

**13. Library of Congress** (confirmed via snippet only)
- **Rule:** primary sources are original materials created at the time; secondary sources recount or interpret them.

**14. Reuters Handbook of Journalism**
- **Rule:** material "we did not gather ourselves" must be attributed.
- **Our rule:** **first-hand gathering is the dividing line for ORIGINAL.**

**15. Coddington 2019** (*Aggregating the News*); **Anderson 2013** ("What aggregators do")
- **Rule:** aggregation is defined by its derivative relationship to reporting.

### Coding reliability

**16. Krippendorff 2004** (thresholds via secondary sources)
- **Rule:** rely on α ≥ .800. Use .667–.800 only for tentative conclusions.

**17. Lombard, Snyder-Duch & Bracken 2002**
- **Rule:** don't use percent agreement. .80+ is acceptable in most situations.
- **Rule:** reliability sample of at least 50 units or 10%, rarely more than 300. Pilot about 30. Report how disagreements were resolved.

**18. Neuendorf 2017** (paywalled; not verified)
- The standard codebook reference: exhaustive, mutually exclusive categories; pilot coding; an independent reliability subsample.

## Part 2. Two-axis scheme

Each video gets **two independent verdicts**, e.g. ORIGINAL + CLICKBAIT. The old CLICKBAIT content label is retired.

### Content axis — whose material is it?

**Step 0. Prepare the transcript.**
- Segment it into UPLOADER speech (channel hosts, staff, and guests the channel itself interviewed) and BORROWED material (clips from other creators or outlets, read-aloud text written by others).
- B = borrowed seconds ÷ total seconds.
- If the transcript covers less than 80% of runtime, or speakers can't be told apart: **UNGRADED**.

**Q1. Is B ≥ 0.50?**
- Yes → Q4.
- No → Q2.

**Q2. Does the uploader's speech contain at least one timestampable first-hand contribution that carries the video's main claim?**
- First-hand means: reporting they gathered themselves (witnessed, obtained documents, own interview), their own data, test or measurement, or first-person expert or participant testimony.
- Yes → **ORIGINAL**.
- No → Q3.

**Q3. The uploader is relaying second-hand claims. Do they add a substantive contribution?**
- Substantive means: a new argument or evaluation; counter-evidence, verification or correction; or a synthesis of at least two independent sources into a conclusion none of them states.
- Yes → **COMMENTARY**.
- No, it restates one source sentence by sentence → **RECYCLED**.

**Q4. Borrowed material dominates. Does the uploader add a substantive contribution that targets the borrowed material, with at least 15% of runtime as their own analysis?**
- This is Campbell and Warhol's "critical bearing" test.
- Yes → **COMMENTARY**.
- No, reactions are non-verbal or filler ("wow", "watch this"), or clips are strung together → **RECYCLED**.

**Tie-breakers**

| # | Rule | Detail |
|---|---|---|
| T1 | Main claim decides | When first-hand and second-hand material mix, grade by what the video's main claim rests on |
| T2 | Burden of proof | COMMENTARY requires naming the contribution in one sentence with a timestamp. If the grader can't, it is RECYCLED |
| T3 | Delivery is irrelevant | AI voice, on-camera face and editing effects don't count; judge the script. This deliberately departs from YouTube, which credits "substantive editing" that a transcript can't see |
| T4 | Ownership vs independence | A channel reusing its own material stays ORIGINAL with **REPOST = yes**, so the same evidence isn't double-counted in narrative metrics |
| T5 | Permission is irrelevant | Licensed third-party clips with nothing added are RECYCLED |

The 50%, 15% and 80% cutoffs are design choices, not sourced figures. Calibrate them in the pilot.

**Anchors**

- **ORIGINAL**
  - An on-scene reporter.
  - A news package where the reporter interviewed experts on camera. (Expert quotes lifted from other outlets count as BORROWED → Q4.)
  - A long-form interview the channel conducted, even with a sensational title — the title is graded on the packaging axis.
  - A podcast's own channel posting a 6-minute clip of its episode → ORIGINAL, REPOST = yes.
  - A creator re-uploading their own 2021 video → ORIGINAL, REPOST = yes.
- **COMMENTARY**
  - A reaction that pauses the source 12 times to fact-check it with documents.
  - A synthesis of four outlets into a timeline that exposes a contradiction.
  - A speech critique where clips are ~55% of runtime and each point is rebutted with data.
  - An AI-narrated explainer that compares studies and concludes something none of them state.
- **RECYCLED**
  - A full re-upload of a broadcast by a third-party channel.
  - A "Top 10 moments" compilation with caption-style narration.
  - A reaction that is 90% source audio plus exclamations.
  - An AI voice reading one article nearly verbatim.
  - A clip channel cutting someone else's podcast with no added speech.

### Packaging axis — does the title/thumbnail deliver?

**P1. List every concrete promise in the title and in thumbnail text.**
- Promise types: a named person or organisation; an event or outcome stated as fact; a number or list count; a date; a prediction; a revelation or "the truth"; a completeness claim ("full", "entire", "leaked footage"); a format or access claim ("exclusive interview").
- Label each promise:
  - **CORE** if it's a factual assertion or named deliverable.
  - **STYLE** if it's an intensifier, superlative, caps or emotional framing.
- A question title promises only that the question gets addressed.
- Thumbnail imagery showing a person or event absent from the video counts as a CORE promise.

**P2. Score each CORE promise against the transcript.**

| Score | Meaning |
|---|---|
| DELIVERED | At least one timestamped passage provides it (the "spoiler" exists) |
| WEAKENED | Addressed, but with a smaller number, hedged, or rumour where the title stated fact |
| ABSENT | Not addressed, or deferred to "part 2", "link below" or a paywall (bait-and-switch) |
| CONTRADICTED | The video says otherwise (the "wrong" type) |

**P3. Verdict, in order.**
1. **CLICKBAIT** — any CORE promise is ABSENT or CONTRADICTED, or the title states as fact something the video presents as unconfirmed.
2. **OVERSTATED** — all CORE promises are DELIVERED or WEAKENED, and either at least one is WEAKENED or a STYLE element inflates what the video supports. A curiosity-gap tease that the video pays off lands here.
3. **ACCURATE** — otherwise.

**The line between the two failures:** OVERSTATED means you got what was promised, only smaller. CLICKBAIT means you didn't get it. **Intent is never coded.**

**Anchors**

- **ACCURATE**
  - "Interview: Dr. Mwangi on the 2026 drought forecast"
  - "3 reasons the bill failed", with exactly 3 reasons
  - "Is the ceasefire holding?", examined
- **OVERSTATED**
  - "SHOCKING truth about the budget", delivering an ordinary analysis
  - "10 signs of collapse", where 4 of the signs are trivial
  - "He EXPOSES everything", where one modest disclosure is made
- **CLICKBAIT**
  - "The president RESIGNED", covering rumours only
  - "Full match highlights" on a 40-second clip
  - A thumbnail celebrity who never appears
  - "Leaked audio revealed" with no audio
  - "Minister admits fraud" when the minister denies it (CONTRADICTED)

## Part 3. Reliability protocol

1. **Pilot.** Two graders independently code 30 videos stratified to include every edge case. Revise the codebook, turning each disagreement into an anchor or rule. Pilot codes are excluded from reliability.
2. **Formal sample.** The larger of 50 videos or 10% of the corpus, capped at 300. Draw randomly, then top up so each of the six categories has at least 10 cases. Coding is blind and independent. **An LLM grader is a coder and must pass the same test.**
3. **Statistic.** Krippendorff's α per axis: nominal for CONTENT, ordinal for PACKAGING. Also report α on promise-level P2 scores, plus a confusion matrix. Never percent agreement.
4. **Publication gate, per axis.**

   | α | What may be published |
   |---|---|
   | ≥ .800 | Per-video verdicts |
   | .667–.800 | Aggregate shares only, marked provisional |
   | < .667 | Nothing. Revise the codebook and recode a fresh sample |

   **Baselines:** impression-based clickbait judgments reach κ ≈ 0.21–0.36; a structured framework reaches ≈ 0.65. Clearing .80 likely needs the promise-checking design, not a gestalt judgment.
5. **Disagreements.** Compute α on the independent codes first. Then resolve by discussion, with a third-grader tiebreak. Log the reason, and turn repeated patterns into rules. Never compute α on consensus labels.
6. **Drift.** Double-code a rolling 10% of new videos. If rolling α drops below .800, stop publishing that axis until recalibrated. Re-test after any codebook change.

**Not verified:** Neuendorf's wording (paywalled); the Library of Congress wording (snippet only); Krippendorff's primary text (thresholds via secondary sources). **The 50%, 15% and 80% cutoffs are proposals, not sourced figures.**
