# Which channels matter — the channel ledger

Draft spec, 2026-09-16. Answers the one question the channel-crawl plan turns on.
Companion to [the narrative system](../narratives/SYSTEM.md) and [collection at scale](../narratives/03-collection-at-scale.md).

---

## 1. "Matters" is two different jobs

A channel can earn its place in two ways, and confusing them is how a corpus turns into a pile.

| Job | What it gives us | What we do with it |
|---|---|---|
| **Evidence** | Claims we can grade: someone argues a position, brings data, or makes a dated call | Crawl the full upload history |
| **Spread** | Proof a claim travelled: the same story, retold | Count it, do not backfill it |

An originator with 2,000 subscribers matters for evidence. A channel that reposts the same claim to two million people matters for spread. The first tells you what is being argued. The second tells you how big the chorus is, which is the mechanism that makes a claim feel true.

Most selection mistakes come from using reach for the first job.

## 2. What our own corpus already shows

From 1,547 collected videos:

| | Count |
|---|---|
| Distinct channels | 975 |
| Channels with exactly one video | 766, or 79% |
| Channels with three or more | 118 |
| Channels with ten or more | 7 |
| Channels appearing in two or more narratives | 61 |
| Share of all videos held by the top twelve channels | 10% |

There is no dominant set of channels. A search-built corpus is a long tail of one-off uploaders with a thin spine of recurring voices. **The spine is the crawl list. The tail is evidence of spread and nothing more.**

Cost of acting on this today, at 50 records per quota unit:

| Job | Records | Units | Share of one day's quota |
|---|---|---|---|
| Backfill the 118 recurring channels, 500 uploads each | 59,000 | 1,180 | 12% |
| Backfill all 975 known channels | 487,500 | 9,750 | 98% |
| Screen one new channel, 100 uploads | 100 | 3 | 3,300 channels a day |

Our entire known channel set can be backfilled in about one day of default quota. Selection is not about affording the crawl. It is about not drowning the corpus in irrelevance.

## 3. The ledger: three tiers

Every channel we have ever seen gets a row, a tier, a reason and a date. Nothing is judged twice by accident.

**Tier A — crawl and watch.** Proven narrative output. Full uploads crawl up to the 20,000 cap, plus push notification on new uploads, which costs nothing.

**Tier B — screened and pending.** Sampled at 100 uploads, awaiting the admission test. Re-screened when it next appears in a search result.

**Tier C — counted, not crawled.** Appears in our corpus, but its output does not recur. Its videos stay in the narratives that already hold them, as evidence of spread. No backfill.

**Tier D — rejected, with the reason and the date.** So the same channel is not re-tested every month.

## 4. The admission test

A channel enters Tier A when, over its last 100 uploads:

1. **Relevance.** At least 20% of uploads match a tracked narrative's vocabulary in title or description.
2. **Recurrence.** Relevant uploads appear in at least 3 distinct months of the last 12.
3. **Gradeable.** At least one upload carries a claim, not only reaction or entertainment.

This deliberately mirrors the narrative admission test, which asks for three independent channels across two months. A narrative earns its place by recurring across voices; a channel earns its place by recurring across time.

**Reach is not in the test.** It is recorded and used to weight the spread job, never to decide entry. A rule that admits by subscriber count would rebuild YouTube's own ranking inside our engine, and every debate set would have a loud first side and a weak second one.

## 5. Ranking inside Tier A

Once admitted, crawl order is set by what a channel adds, not how big it is.

| Signal | Why it counts | Source |
|---|---|---|
| **Originator lead** | Posted a claim before the rest: dates the mutation and anchors the origin set | Our corpus: earliest video per claim |
| **Original share** | How much of its graded output is first-hand rather than borrowed | Verdicts |
| **Camp coverage** | Argues a side that is currently thin in that narrative | Claims and camps |
| **Persistence** | Months in which it carries the narrative | Upload dates |
| **Cadence** | Uploads per month, so the crawl budget matches what it produces | Upload dates |
| **Reach** | Weight for the spread job only | Views, subscribers |

**Camp coverage carries a deliberate bonus.** The counter-camp is almost always smaller and slower, so a neutral rule under-collects it. Anti-inflammatory diet shows the pattern already: 33 videos for the maximalist camp, 7 for the trial-first skeptics.

## 6. Guardrails

- **Concentration cap.** No single channel supplies more than 20% of a narrative's corpus. Past that, its extra uploads are counted but not added, and the cap is stated on the page.
- **Reason on the row.** Every admission and demotion records why and when, so the crawl list can be audited like the ledger.
- **Ageing.** A Tier A channel with no relevant upload in 6 months drops to B. A Tier C channel that starts recurring rises to B.
- **Amplifiers stay counted.** A channel whose output is all recycled is not crawled deeply, because it adds repetition rather than information. It still appears in spread counts.
- **No profiling of viewers, ever.** This is a ledger of publishers, which is public behaviour.

## 7. Where candidates come from, cheapest first

1. **Channels already in our corpora.** Free, 975 of them, ranked by §4 today.
2. **Channel IDs from the daily search rotation.** Already collected, costs nothing extra.
3. **Featured channels of Tier A members.** One unit each, the snowball method used in published research.
4. **Outside lists.** Outlet directories, fact-check databases, podcast charts, off-platform shares.
5. **Co-citation.** Who a video quotes or reacts to, once transcripts exist.

## 8. Daily quota budget

| Purpose | Share of 10,000 units |
|---|---|
| Backfill Tier A | 60% |
| Screen Tier B candidates | 25% |
| Refresh stats and titles inside the 30-day rule | 15% |
| New uploads from Tier A | 0, push notifications are free |

## 9. What can be built before any key arrives

Rank the 975 channels we already hold by §4 and §5, publish the ledger with its reasons, and see whether the ranking agrees with judgment. That is a script over existing files, needs no API access, no permissions and no decisions, and it is the same code that will rank 100,000 channels later.
