> **Scope note:** This is a design/research memo for Lens 5 only (belief updating / the living thesis). It is deliberately adversarial. Where I think the founder's framing is wrong, I say so. Retention numbers marked *(estimate)* are my inference, not measurement.

---

# LENS 5 — BELIEF UPDATING / THE LIVING THESIS

## 0. BLUF

**The living thesis is worth building, but almost none of its value comes from users returning.** The evidence says most people will never come back — plan for that as the base case, not the failure case.

Three findings drive everything below:

1. **Lens 5 dictates the data model of Lens 2.** If the Portable Thesis is free text, an update system is *permanently impossible*. Reasons must be built from citable corpus objects (a prediction ID, an indicator ID, a claim ID, a predictor name, a relation edge). Call these the thesis's **footings**. Decide this before shipping the thesis composer, or the belief-updating layer can never be retrofitted.
2. **The update engine is `git diff`, not a cron job.** The corpus is already a versioned git repo with deterministic JSON. Store the commit SHA at thesis-save time; on the user's next visit, diff HEAD against that SHA and filter to the thesis's footings. No backend, no accounts, no polling, no per-user cost. It only spends anything when a user actually returns — which is exactly the right cost curve for a product whose users mostly don't.
3. **The durable object is the QUESTION, not the thesis.** The 360 map already models a narrative as one *answer* competing for a durable *question*, with answers rotating underneath. Version history should therefore hang off `(user, question)`, not `(user, narrative)`. This is a correction to the founder's implicit structure and it makes belief-updating fall out of the existing typology instead of being bolted on. It also unlocks a first-class trigger the founder didn't list: *a new answer to your question was founded.*

---

## 1. The honest answer on whether users return

### The evidence

| Signal | Number | Source |
|---|---|---|
| Median mobile D30 retention, all categories | ~4–8% (Adjust median 7%; iOS 5.3–8%, Android 3.8%) | app benchmark reports, 2026 |
| Habit/journaling apps specifically | >52% discontinue within 30 days; industry avg ~7.9% D30 | habit-tracking industry data |
| Re-engagement email | ~29% open rate, wins back ~14% of inactive subscribers | email benchmark reports, 2026 |
| Push volume tolerance | >6/week → **3.4× more likely to uninstall within 30 days**; 2–5/week → nearly half opt out; ~67% want ≤1/day | push notification statistics, 2026 |
| Weekly digest option | lowers opt-outs ~10% | same |
| Metaculus | ~15k forecasters after a decade; tournaments define "high-participation" as forecasting >75% of questions — implying most forecast very few | Metaculus platform data |
| Good Judgment Project | aggregation **weights forecasters who update more frequently** — a weighting scheme only exists because most people don't update | Mellers/Tetlock, GJP |
| Fatebook (successor to PredictionBook) | ships **email reminders to resolve** as a core mechanic | Fatebook / LessWrong |

### The reading

The Fatebook detail is the most instructive. A tool built by and for the single most updating-inclined population on earth (EA/rationalist forecasters) still concluded that resolution has to be *pushed*, because even they don't come back to close their own loops. If that population needs a reminder, year-one Malik certainly does.

**Do not model retention on Metaculus.** Metaculus users have an identity ("I am a forecaster"), a scoreboard, and a community. Narrative Radar's user is someone with a *question* and a meeting on Thursday. That is a task, not a hobby. Forecasting-platform engagement is the wrong reference class; the right one is "looked something up once."

### Realistic numbers *(estimate, stated as a guess so it can be falsified later)*

Of 100 users who save a thesis:
- **10–20** ever open it again unprompted within 6 months (generously above the D30 median, because saving is a high-intent act)
- With **one** material, well-targeted email: 20–35% open *(benchmark ~29%)*, maybe a third act → **7–12** take an action
- Of those who review, **most will record "no change"** — and that is a correct outcome, not a failure
- Net: **~10–25 second looks, ~5–10 genuine revisions per 100 saved theses**

Design so those 5–10 are your most valuable users and the other 90 lost nothing.

### Two reframes that survive this

**(a) Users don't return to the product — they return to the question.** Re-entry happens when the topic recurs in their life: a meeting, a market move, a friend brings it up. The re-entry action is a *search or a re-paste*, not a notification click. Therefore the single highest-value update surface is: **when a user opens or pastes a narrative they already hold a thesis on, surface their own past thesis and what has changed since — right there, unprompted, in the flow they were already in.** This costs one localStorage lookup and a diff. It requires no accounts, no email, no notifications, and it fires exactly when it is useful.

**(b) The thesis's second life is in the conversation, not the app.** The moment the user needs an update is *before they next say the thing out loud*. So the surface that matters is "check before you cite" — the exported artifact itself, carrying its own staleness. See §7.

### The n=1 trap

Malik will use this feature. Malik is not the user. He is the one person in the funnel who behaves like a Metaculus regular — because he built it, because the $20k gives him motivation nobody else has. **Beware building the living thesis for him and validating it on him.** Every design choice below should be tested against "would a person who used this once for a work meeting benefit?"

---

## 2. Legitimate update triggers, graded

Only events derivable from this product's own data, ranked by whether they should ever be allowed to reach a user.

### Tier A — can justify an out-of-band message

| Trigger | Why it qualifies | Constraint |
|---|---|---|
| **A PENDING prediction resolves** (SUPPORTED/REFUTED) | Dated, attributed, falsifiable. The purest signal the product produces. | Only if that prediction was a footing of the thesis. |
| **A deadline rolls (UPDATED)** | The product's signature structural signal. | Must be phrased as *"the clock moved, not the world."* A rolled deadline is evidence about the predictor's method, never evidence the claim is false. |
| **A named predictor's ledger crosses n≥5 resolved** | The first moment the product is *permitted* to characterise a track record. If the user's WHY leaned on a person, this is the most decision-relevant event the system can generate. | The existing n≥5 gate applies unchanged. |
| **A `counters` edge lands with corpus receipts** | The user's COUNTERWEIGHT just changed — the strongest argument against them is now a different argument. | Requires the ≥3 videos / ≥2 channels receipt gate. |
| **Genesis trace lands** | "This 'new' thesis is from 2014." Fires at most once per narrative. Changes the *age*, not the truth — but for year-one Malik, age is the whole point. | One-shot; never re-fires. |
| **An indicator crosses a named threshold** | Highest user-desire trigger. | **Honest flag: the product cannot fire this today.** indicators.json stores thresholds extracted from transcripts; firing on a crossing requires live external market/econ data the product does not have. That is a new data dependency with real cost and a new failure mode (bad prints, revisions, stale feeds). Also: the `contested_note` must ride along — when camps read the same dial oppositely, a crossing is not a verdict. Treat as v3, not v1. |

### Tier B — belongs in a quiet review, never a notification

- **A new mutation in the mechanism.** Editorially detected, false-positive-prone. Material only when the user's WHY cited the superseded mechanism.
- **A new competing narrative founded / new relation edge minted.** Interesting; rarely position-changing.
- **Silence / decay** *(not on the founder's list — add it)*. No new ORIGINAL video in N weeks. **Absence of events is an event**, it is free to compute, it is a fact about the corpus rather than a claim about the world, and it handles the overwhelmingly common case where nothing happened. "Nothing new in 90 days" is often the single most useful thing you can tell someone holding a thesis.

### Tier C — context only, never a trigger

- **Corpus composition shift (original:recycled ratio).** Badly confounded: a refresh sweep that adds five videos changes the ratio without the world changing. Firing on this would be **notifying the user about your own collection activity**. Only show normalized, and never fire on a shift that coincides with a corpus expansion.

### Tier A+ — the user's own update condition

If the user writes "I'd change my mind if the Fed cuts twice before December," the product can run **one** model call *at review time* asking whether anything in the corpus since the thesis SHA speaks to that condition. Highest precision available, because the user defined it. Cost is incurred only on return. This is the one place a model call earns its keep.

### Hard-forbidden triggers

- **"This narrative is trending."** Volume is the thing this product exists to immunize against. A trending notification is the product becoming the algorithm it was built to be the exit from. Absolute no.
- **Price/market moves not tied to a corpus-named threshold.** That's a finance app, and it invites "we told you so."
- **"A new video was posted."** That's a YouTube subscription. The differentiator is that a new video is usually *not* news.
- **Anything derived from other users' activity.** No social proof, ever.

---

## 3. The materiality gate (the architecture that makes this not-a-feed)

A trigger reaches a user **only if it touches a stored footing of that specific thesis.** This is a join, not a feed.

```
thesis {
  question_id            // durable primary key, per §0.3
  narrative_id           // the answer they landed on
  position, confidence
  footings: [
    {type:"prediction", id:"dalio-2026-midterms", role:"why_1"},
    {type:"indicator",  id:"10yr-above-5",        role:"update_condition"},
    {type:"predictor",  id:"armstrong",           role:"why_2"},
    {type:"relation",   id:"counters:soft-landing", role:"counterweight"}
  ]
  corpus_sha             // git commit at save time — the diff anchor
  saved_at, review_by
}
```

Two consequences worth stating plainly:

- **A thesis with no footings is un-updatable, forever.** The composer should say so at write time: *"Nothing we track can tell you if this changes."* That nudge improves thesis quality at composition — which is value delivered to the 90% who never return.
- **Instrument the gate.** Report the fraction of generated events that were *material* (touched a footing). If it's under ~20%, the trigger taxonomy is too loose and should be cut, not tuned.

---

## 4. Notification design that isn't engagement farming

### The bright line

> **Notify about the world, never about the user.**

Product-side events may generate messages. User-side non-activity may never generate anything. That rule kills, by construction: streaks, badges, "you haven't checked in 30 days," "3 narratives you follow have updates," win-back campaigns, and every other re-engagement pattern. It is a single sentence, it is auditable in code, and it should be published.

### The rules

1. **Zero push notifications. Ever.** Email only. The uninstall data (>6/week → 3.4×; 2–5/week → half opt out) describes a channel this product has no business entering.
2. **Volume: at most one message per thesis per quarter, and one per user per month, rolled up.** Realistic real volume for one thesis is **0–3 events per year.** That is the honest number and it is a feature.
3. **Arm-at-save, not opt-out-later.** At save time the user picks trigger classes: *"Wake me if a call I cited resolves / if my counterweight changes / if the clock rolls."* Default on: resolution, counterweight, predictor-score-gate. Default off: everything else. This converts notification from something done *to* them into something they armed.
4. **The subject line must be the whole product.** `Dalio's Nov-2026 midterm call resolved REFUTED — it was reason #2 of your thesis.` If the user reads only that and never clicks, **the product succeeded.** Corollary: **a low click-through rate is not a failure**, and CTR must be a published anti-metric. This is the only honest expression of time-to-orientation in a notification channel.
5. **Deliberate asymmetry: disconfirmation is pushed, confirmation is pulled.** Events that cut *against* the user's stored position are always delivered; events that support it are batched into the quiet review. This is the exact inverse of an engagement-optimized system (which pushes the good news because it feels good). It is the single most defensible integrity rule in this lens.
6. **Dead man's switch.** Three consecutive ignored messages → stop permanently, say so once, keep the thesis alive in-app. Auto-unsubscribe on non-engagement is the falsifiable, code-auditable commitment that this is not a retention system.
7. **Offer the no-infrastructure path and make it fully good.** "Don't email me — I'll come back" must lead to a genuinely complete experience (§1a return-triggered surfacing). Additionally offer a **user-owned calendar event / .ics** at save time: *"Review this before the Nov 5 meeting."* User-owned, zero infrastructure, no engagement incentive, and it still works if the product dies. For a quarterly-cadence product this may outperform email outright.

---

## 5. Version history

**Append-only. Never edit in place.** Each version stamps: date, position, confidence, footings, `corpus_sha`, and a required *reason for the change* (which trigger, or "own reflection").

### The review ritual — order is the whole design

The decision-journal literature is unambiguous: an explicit prior record is the defence against "I knew it all along," and it is the *rationale*, not just the position, that makes review informative (Armstrong: the surest protection is disciplining ourselves to make explicit predictions, showing what we did in fact know). But a record shown in the wrong order creates the bias it was meant to prevent.

**Correct sequence:**

1. **What changed in the world.** The deterministic diff. No mention of the user's position.
2. **Blind re-elicitation.** *"Given this, where do you land?"* — capture position + confidence fresh, or at minimum a one-tap *moved / didn't move / unsure*.
3. **Then reveal** the old thesis and the diff between old and new.

Showing the old position first anchors the user and turns the evidence review into a defence of the prior. **Blind re-elicitation before reveal is the strongest debiasing move available here and it costs one screen.** It is also the only mechanic in this memo that produces a *measurement*: the gap between blind re-elicitation and stated prior is a personal anchoring score.

Also reconstruct the **epistemic state**, not just the text: *"When you wrote this, the corpus had 18 videos, 3 of 11 calls were resolved, and your counterweight was X."* Hindsight is defeated by remembering what you didn't know, not by re-reading what you wrote.

### Other rules

- **Confidence sparkline across versions.** This is the calibration artifact and it becomes the feature's real payoff at version 4–5.
- **Show the revision count with the same prominence as confidence.** Normalize updating. GJP's finding is that many small updates with occasional large ones is the accuracy-linked behaviour; a product that displays "changed my mind 3 times" as a neutral-to-positive stat is teaching the right thing.
- **"No change" must be exactly as easy as "change,"** one tap, and recorded as a version. Otherwise the UI biases toward revision — the mirror error of anchoring.
- **Hard cap the review at one screen / ~60 seconds.** Time-to-orientation applies to the review too.
- **Users may delete a thesis entirely; they may never edit a past version.** Privacy is all-or-nothing; history is immutable.
- **Retiring is honourable.** "This question stopped mattering" / "this narrative decayed" is a first-class action with its own graveyard view. It defuses sunk-cost on the thesis itself.

---

## 6. Psychology risks and specific countermeasures

| Risk | Evidence | Countermeasure |
|---|---|---|
| **Anchoring on own past position** | classic | Blind re-elicitation before reveal (§5). Show the counterweight before the position. |
| **Escalation of commitment, amplified by public articulation** | Commitment bias is strongest for publicly-stated, high-stakes positions; people rationalize evidence rather than admit error. Notably, escalators are *trusted more* by observers (entrusted with **29% more money**) — so the social payoff for holding firm is real, not imagined. De-escalation requires a context where changing costs no reputation. | (a) **Version history private by default**; the Portable Thesis is for *export*, not for a public profile. (b) Do not display "you shared this" during review — reminding someone they said it out loud increases commitment. (c) **Auto-draft the climbdown**: a three-line *"what I said then / what changed / what I think now"* the user can paste back to the same people. Making the retraction *easy to say* attacks the documented barrier directly. No competitor has this. |
| **The "I called it" trap** | one lucky call → permanent identity | Apply the product's own n≥5 gate **to the user**. No personal score until 5+ resolved theses, and then show **calibration** (were your 70%s right ~70% of the time), never hit rate. No ranks, no leaderboards, no sharing of scores. A personal score must never become a retention hook — that is precisely the dynamic that leaves Metaculus with a devoted minority and a churned majority. |
| **Hindsight bias at review** | "knew it all along"; documented rationale is the defence | Verbatim original rationale + epistemic-state reconstruction (§5). |
| **Confirmation bias in trigger selection** | users will arm the triggers that flatter them | Disconfirming triggers are always delivered regardless of settings (§4.5). |
| **Fear of entrenchment / backfire** | **Wood & Porter: 5 experiments, >10,000 participants, 52 contested issues — corrections overwhelmingly moved people toward accuracy; they could not reliably produce a single backfire.** Later replications agree; backfire is rare and mostly confined to identity-fused beliefs. | **Don't soften disconfirming evidence.** Show it plainly. This is the good news of the lens: the main obstacle is *getting people to look*, not what happens when they do. |
| **Sunk cost on the thesis artifact** | "I spent 20 minutes on this" | Cheap creation + honourable retirement (§5). |
| **Review-as-chore** | habit-app churn | One screen, 60 seconds, legitimate one-tap "nothing here moves me." |

---

## 7. Designing for the user who never returns

This is where the lens earns its keep, and it inverts the feature's apparent purpose.

1. **The thesis must deliver 100% of its value at composition time.** It is a thinking aid and an export artifact first; a tracked object second. If the composer is only worth using because of what happens later, it is not worth using.
2. **The export carries its own staleness.** Every exported thesis is stamped: *"As of 13 Aug 2026 — corpus: 22 videos, 3 of 14 calls resolved. This goes stale when: [update condition]. Review by: [date]."* The artifact then degrades honestly **in the wild, without the product**.
3. **The shared permalink is the return path.** If the user shares a thesis link and someone opens it three months later, the page can show: *"This thesis is 3 months old. 2 of its 4 footings have changed."* The user learns their thesis moved **because someone else read it**. Distribution and updating solved by the same mechanism — and it is the only re-engagement channel that doesn't require the original user to do anything.
4. **Expiry, not decay.** A hard "review by" date, derived from the update condition, displayed as **STALE** past it. Honest, requires no return, and needs no infrastructure.
5. **"Check before you cite" is the real job.** The user's need arises before they next speak, not on a calendar interval — which is another argument that the return-triggered surface beats the notification.

---

## 8. What to reject

- ❌ **A digest/feed of narrative updates.** That's a feed. It is the enemy.
- ❌ **Push notifications** in any version.
- ❌ **Streaks, badges, scores, leaderboards, DAU.**
- ❌ **AI-drafted revised positions.** The product may generate the *deterministic diff summary*; it must never draft the user's new position. Writing "here's what you now believe" is the product asserting a view — the never-assert-truth rule, applied at the personal level. Hard boundary.
- ❌ **Treating the thesis as the durable object.** It's the question (§0.3).
- ⚠️ **Public hosting of user theses — off by default.** A user thesis saying "X is a grifter," published on the product's domain, is the product's defamation problem. The same gate that forces `supplements` edges to name product *categories* rather than sellers applies to user-authored text about named predictors. Exports are user-owned artifacts (copy/download); public permalinks need the same review gate as supplements edges, or should be private-link-only.

---

## 9. Build sequence

**v1 — no backend, no accounts, no notifications** *(fits today's architecture exactly)*
- Theses in localStorage (the `follow` feature already proves this pattern in this codebase)
- Store `corpus_sha` at save; on visit, diff HEAD vs SHA via GitHub API, filter to footings, render the change list — **deterministic, free, auditable, no model call**
- Return-triggered surfacing (§1a) + blind re-elicitation review (§5) + append-only versions
- Export with staleness stamp + optional .ics review reminder
- Ships the whole lens for the user who returns *on their own*, at zero marginal cost

**v2 — after accounts exist** (accounts are already the stated milestone before billing)
- Cross-device sync; the one armed email channel with the §4 caps and dead man's switch
- Shared-permalink staleness banner

**v3 — only if v1/v2 show real demand**
- Live indicator-threshold crossings (new external data dependency, real cost, new failure modes)
- User-condition matching via one model call at review time

---

## 10. Metrics

**Primary:** % of returning-with-a-thesis sessions that reach an explicit disposition (unchanged / revised / retired) **within 90 seconds**.

**Secondary:** calibration improvement across versions (not revision rate alone — a high revision rate can just mean the first thesis was shallow); % of generated events that were material (§3).

**Published anti-metrics — stated as things this product refuses to optimize:** sessions per user, notification CTR, time on page, DAU, thesis count. The receipt strip already established the pattern of shipping honesty gates as visible product; do the same for the metric contract.

---

## 11. Open questions for Malik

1. **Question-keyed or narrative-keyed history?** I argue question-keyed. It's a schema decision that is expensive to reverse.
2. **Does the thesis composer force citable footings?** If no, Lens 5 dies permanently. This must be decided in Lens 2, not here.
3. **Is the user's personal calibration score a feature at all?** I lean toward: yes, gated at n≥5, calibration-only, private, never shareable — and even then it is the feature most likely to quietly turn this into the scoreboard product he doesn't want.
4. **Are public thesis permalinks on the product's domain acceptable given the defamation surface?** My recommendation is private-link-only until there's a review gate.
5. **Do you accept "0–3 notifications per thesis per year" as a success condition?** If that number feels too low, the disagreement is about what this product is, and it should be settled before any of this gets built.

---

## Sources

- [App retention benchmarks 2026 (Day 1/7/30 by category)](https://unstar.app/blog/app-retention-benchmarks-2026) · [Getstream 2026 app retention guide](https://getstream.io/blog/app-retention-guide/) · [UXCam retention benchmarks by industry](https://uxcam.com/blog/mobile-app-retention-benchmarks/)
- [State of habit tracking 2026](https://habit-streak.com/en/blog/habit-tracking/state-of-habit-tracking-2026)
- [Push notification statistics 2026 — Business of Apps](https://www.businessofapps.com/marketplace/push-notifications/research/push-notifications-statistics/) · [How many push notifications are too many](https://thisisglance.com/learning-centre/how-many-push-notifications-are-too-many-for-app-users) · [Braze — Don't bury your customers in notifications](https://www.braze.com/resources/articles/dont-bury-customers-notifications)
- [Email marketing benchmarks 2026 (re-engagement open/win-back rates)](https://searchlab.nl/en/statistics/email-marketing-statistics-2026)
- [Metaculus FAQ](https://www.metaculus.com/faq/) · [Metaculus platform profile & performance data](https://oddsreference.com/predictions/platforms/metaculus)
- [AI Impacts — Evidence on good forecasting practices from the Good Judgment Project](https://aiimpacts.org/evidence-on-good-forecasting-practices-from-the-good-judgment-project/) · [Mellers et al., Identifying and Cultivating Superforecasters (PDF)](https://web.stanford.edu/~knutson/jdm/mellers15.pdf) · [The Good Judgment Project](https://en.wikipedia.org/wiki/The_Good_Judgment_Project)
- [Fatebook — the fastest way to make and track predictions (EA Forum)](https://forum.effectivealtruism.org/posts/DWFRBzK3rAH3HFDZr/fatebook-the-fastest-way-to-make-and-track-predictions) · [PredictionBook](https://predictionbook.com/predictions)
- [Escalation of commitment — Wikipedia](https://en.wikipedia.org/wiki/Escalation_of_commitment) · [Commitment bias — The Decision Lab](https://thedecisionlab.com/biases/commitment-bias) · [Staying the course: decision makers who escalate commitment are trusted and trustworthy (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9354500/)
- [Wood & Porter, The Elusive Backfire Effect (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2819073) · [Examining the replicability of backfire effects after standalone corrections](https://link.springer.com/article/10.1186/s41235-023-00492-z) · [IPR — The elusive backfire effect](https://instituteforpr.org/the-elusive-backfire-effect-does-correcting-misinformation-strengthen-peoples-beliefs-in-false-claims/)
- [Farnam Street — Hindsight bias](https://fs.blog/what-is-hindsight-bias/) · [Eliminating the hindsight bias (ResearchGate)](https://www.researchgate.net/publication/232428907_Eliminating_the_Hindsight_Bias) · [BMT — Hindsight bias and decision records](https://www.bmt.org/insights/hindsight-bias-its-effects-on-decision-making-and-implications-for-project-management/)
- [Poynter — Time spent or time well spent](https://www.poynter.org/reporting-editing/2015/time-spent-or-time-well-spent-how-to-think-about-web-traffic/)
