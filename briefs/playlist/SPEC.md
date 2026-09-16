# The Evening Set — a finite, sequenced playlist from the corpus

Draft spec, 2026-09-15. Origin: a viewer who knows roughly what he wants to watch after work
and wants it curated by theme, without browsing.

Related: [psychology synthesis](../psychology/SYNTHESIS.md) · [the narrative system](../narratives/SYSTEM.md) · [filter suite](../filter-suite/SPEC.md)

---

## 1. What it is, and what it must never become

**A set is a finite, ordered evening of watching, built from one or two themes the viewer picks,
that fits the time they have and ends on purpose.**

The danger is obvious: a playlist feature is a recommender, and a recommender is the thing this
product exists to counter. The line between the two is not the algorithm, it is the shape.

| A feed | A set |
|---|---|
| Never ends | 3 to 6 items, then a close card |
| Optimises watch time | Optimises "I understand this now, I can stop" |
| Infers what you want from behaviour | Takes themes you chose, and stores nothing about you |
| Ranks by popularity | Ranks by role in an argument |
| Repeats the same claim in new voices | Bans a repeated claim, because repetition is what makes it feel true |
| Leaves a loop open so you keep going | States what is unresolved and hands it back to you |

**The Google test** (see the competitive note): would YouTube ship this? They would ship a themed
playlist. They would not ship one that caps itself at one video per channel, excludes recycled
uploads, starts a podcast at minute 34 where the evidence is, and then tells you to stop.

## 2. The inputs

1. **Themes.** One or two, chosen from industries or tracked narratives. Two themes are the
   brother's case, so they are first-class: each gets its own mini-arc, never interleaved at random.
2. **Time budget.** 30, 60 or 90 minutes. Real runtimes, shown as a total before the set starts.
3. **Set type.** Three shapes, below.
4. **One toggle.** "Show me the popular version too" adds a single clickbait or recycled example,
   labelled, at the end. It is inoculation, not filler, and it is off by default.

Nothing else. No sign-in, no profile, no watch history. Theme choices stay on the device.

## 3. The three shapes

### The Debate Set (a contested claim)
For a narrative with camps. The shape that earns the product's name.

| Slot | Content | Rule |
|---|---|---|
| Open card | The claim in attributed form, its age, what is at stake, and a prequestion: what would have to be true for this to be right? | Reading, not watching. Prequestions raise later skepticism |
| 1 | The strongest statement of the claim, from its own camp | Best-argued, not most-viewed. Evidence-bearing, no product pitch |
| 2 | The strongest counter, from another camp | Mandatory when camps exist. If the corpus holds no credible counter, the card says so. We never manufacture balance |
| 3 | The receipts | Our own ledger card, or a video that checks the dated claims |
| 4 (if budget) | New information: original reporting, first-hand data, an interview | Content verdict ORIGINAL preferred |
| Close card | What is still unresolved, what would change the picture, what to look out for in the next video on this | Closes the loop deliberately |

### The Catch-Up Set (what is new in my themes)
Newest material only, one per channel, recycled and clickbait excluded, capped at the budget. For
the viewer who follows a story and wants the week, not the rabbit hole.

### The Origin Set (how this story got here)
One narrative, oldest to newest, one video per mutation, so an hour shows five years of the claim
changing shape. Strongest use of what we already own and impossible to assemble on YouTube itself.

## 4. Selection rules

**Hard exclusions.** Packaging verdict CLICKBAIT, content verdict RECYCLED, live streams, anything
longer than the remaining budget without a usable timestamp, a channel already used in this set, a
claim already covered in this set, and paid-promotion videos in any evidence slot. While a video is
ungraded, the title-bait lexicon and the sponsorship flag stand in for the verdicts.

**Ranking within a slot.** Role fit first: does it argue the position the slot needs? Then evidence
signals, then recency. **Never rank by views.** Popularity is shown as context on the card and
belongs to the creator tool, not the viewer's set.

**Start where it matters.** Chapters, and later transcript search hits, give a timestamp, so a
two-hour podcast can contribute eight minutes through a deep link. This is the feature that most
clearly proves whose side we are on.

**Honesty on the card.** An ungraded video says "not graded yet" rather than borrowing a verdict.
Per-video verdicts appear only once the reliability gate passes; until then a set shows the basis,
not a grade.

## 5. What the corpus supports today

| | Videos | Runtime known | Chapters | Graded |
|---|---|---|---|---|
| All eight narratives | 1,547 | 99% | 48% | 12% |

Camps exist on anti-inflammatory diet (3 contested claims), crypto winter (2), the debt collapse (1),
housing (1) and open vs closed AI (1).

So, at launch:
- **Debate Sets**: anti-inflammatory diet now, since all 105 videos are graded and three claims carry
  camps. Others qualify as grading catches up. Gate: camps present and at least 20 graded videos.
- **Catch-Up and Origin Sets**: every narrative, from metadata alone.

## 6. Output

- **In the app.** A set page: the cards in order, total runtime, each video as a deep link at its
  timestamp. Shareable by URL, since the set is defined by its inputs and the corpus.
- **Into YouTube, no account.** A temporary playlist link built from the video ids. Zero quota, no
  sign-in. **To verify:** length limits and whether the link survives on mobile.
- **Into their account.** Later, and only under the API route: creating a playlist costs 50 quota
  units and each video another 50, so the default quota is roughly 28 sets a day. Needs sign-in with
  YouTube permission, which is the user's own account acting for itself.

## 7. Build order

1. **Set builder in the page.** Client-side over the JSON we already ship. Three shapes, theme and
   budget pickers, deep links, temporary playlist link. No new services, no new data.
2. **Timestamps.** Chapters first, transcript hits when the transcript store fills.
3. **Account export.** After the compliance decision, with sign-in.
4. **The evening drop.** Once a week, built from the daily sweep, only if sets get finished.

## 8. How we will know it works

Count **sets finished**, the **counter video watched** in a Debate Set, and a one-tap "I got what I
needed" on the close card. Do not measure watch time, and never optimise for it. A set that makes
someone close the tab after two videos because the question is answered is a success, and any metric
that calls it a failure is the wrong metric.

## 9. Risks

- **It drifts into a recommender.** The rules in §1 are the product. They go in code as constraints,
  not preferences.
- **Thin corpora.** A set from a narrative with three graded videos is padding. The gate in §5 holds.
- **False balance.** A counter slot creates pressure to find a counter. The empty card is the correct
  output when the corpus has none.
- **Budget honesty.** Podcast runtimes are long; without timestamps the 30-minute set will be thin.
- **Temporary playlist links** are unverified and may change. The app page is the primary output.
