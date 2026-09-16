# The extraction system — from a video to a narrative on a shelf

Spec, 2026-09-16. Settles the order of operations for extracting every narrative
we can reach, under the API-only decision taken today.

Reads with: [the narrative system](../narratives/SYSTEM.md) · [which channels matter](CHANNELS.md) · [collection at scale](../narratives/03-collection-at-scale.md)

---

## 0. The decision this rests on

**Collection happens through the YouTube Data API only.** Reading YouTube's own pages is scraping, the Terms forbid it, and mixing scraped data with API data puts API access at risk. In force from 2026-09-16.

What changed in the repo the same day:
- The daily sweep refuses to run without an API key, instead of falling back to the search page. The corpus is left untouched and the run says so.
- `collector.py`, `scripts/enrich_youtube.py` and `scripts/fetch_transcripts.py` carry a retired banner. The data they already collected stays; they are not run again.
- Transcripts therefore come from podcast feeds, creator-published transcripts and opt-ins, never from YouTube.

Consequence to accept openly: **no new videos arrive until the `YT_API_KEY` secret exists.** That is the cost of the decision, and it is small next to losing API access.

## 1. The order, which runs three ways

The confusion is real, because the layers appear in a different order depending on what you are doing.

| Phase | Order | Why |
|---|---|---|
| **Collect** | Category → channels → videos | We need vocabulary to know where to look. Industries carry the seed terms that find channels. |
| **Extract** | Video → claim → narrative → category | Claims are the atoms. A narrative is what a claim becomes when it recurs. The shelf is assigned last, from what the narrative turned out to be. |
| **Present** | Industry → narrative → claims → camps → videos | A reader browses from the shelf down. |

So the answer to "claim, then narrative, then category" is **yes, for extraction**, which is the part that creates the value. The category leads only at the collection end, and it is a search heuristic there, not a judgment. It is decided properly after the narrative exists.

## 2. The objects

```
channel   { channelId, tier A|B|C|D, reason, admitted, uploads_crawled }
video     { videoId, channelId, publishedAt, title, description, stats, refreshed }
instance  { videoId, phrase, source: title|description|transcript, found }   — a claim as one video worded it
claim     { id, statement (attributed), instances[], channels[], months[], first_seen, status }
narrative { id, claim_name, hook, frame{problem,cause,outcome,clock}, claims[], camps[],
            born, mutations[], industry, tier: data|full }
industry  { id, name, definition, seed_terms }
```

The unit that recurs is the **claim**. The unit that gets a page is the **narrative**. The unit that gets graded is the **video**.

## 3. The nine stages

**1. Harvest.** Search rotation for discovery inside the 20-day recall window. Channel crawl for backfill. Push notifications for new uploads from Tier A channels, which cost no quota.

**2. Relevance gate.** Does the title or description carry claim wording, and is the wording distinctive rather than common vocabulary? Cheap, rule-based, runs on everything. Today this keeps about half of what we hold: 761 of 1,580 videos.

**3. Claim extraction.** Phrase level now, from titles and descriptions. Model-assisted paraphrase later, on the survivors only. Transcript level when a compliant transcript exists.

**4. Claim clustering.** Instances that state the same proposition become one claim. Today this is phrase overlap plus shared videos. At scale it is embeddings with the same thresholds.

**5. Narrative admission.** A claim, or a group of claims sharing a frame, becomes a narrative when it clears the test: 3 or more independent channels, across 2 or more distinct months, checkable, and not a twin of an existing narrative. A claim that fails stays a claim and keeps accumulating.

**6. Naming.** The attributed claim name first, which states the claim in its believers' words without asserting it. The hook title only once the corpus shows a tension worth naming.

**7. Shelf assignment.** Industry from the narrative's own vocabulary and from where its channels' other narratives sit. YouTube's categories are a weak signal, never the decision: coders agree with the uploader's category only 28% of the time.

**8. Publishing tier.** Auto-admitted narratives get a **data page**: momentum, channels, claim timeline, first appearance. No model spend. A narrative is promoted to a **full page**, with camps, explanations and a ledger, when it earns attention: sustained activity, a reader opening it, or a dated claim to track. This is the cost control that makes "every narrative" affordable.

**9. Grading.** Two-axis verdicts, content and packaging, on videos where a transcript exists, published only past the reliability gate.

Stages 1 and 9 wait on the key and on transcripts. Stages 2 to 8 run today on what we hold.

## 4. Cost discipline

Spend per narrative, not per video.

| Work | Per what | Method |
|---|---|---|
| Relevance, extraction, clustering, admission | Every video | Rules. No model. |
| Naming, framing, camps, explanations | Promoted narratives only | Model |
| Grading | Videos with transcripts | Model, then reliability check |

A million harvested videos must cost nothing but compute. Only the few thousand narratives that survive admission are worth a model call, and only the promoted ones are worth several.

## 5. Quota budget, per day

| Purpose | Share of 10,000 units |
|---|---|
| Backfill Tier A channels | 60% |
| Screen new channel candidates | 25% |
| Refresh titles and stats inside the 30-day rule | 15% |
| New uploads from Tier A | 0, push notifications |

Search is its own 100 calls a day, spent entirely on discovery of new channels and new narratives.

## 6. What "every narrative" honestly means

Every narrative carried by the channels we crawl, in the languages we process, discoverable from titles and descriptions, as of a stated date, with a completeness estimate per narrative.

Not: every narrative on YouTube. The arithmetic for that is in the collection brief, and it is 82 years of default quota.

## 7. Build order

1. **Stages 2 to 5 as a service**, not a script: run over the existing corpus, write claims and narrative candidates to files the page reads. The discovery pass shipped on 2026-09-16 is stage 2 to 4 in its first form.
2. **The channel ledger**, ranking the 975 channels we already hold.
3. **Harvest** when the key arrives: search rotation first, since every day of delay loses videos to the recall window, then the backfill crawl.
4. **The audit application** for the Analytics and Reporting exception, which is what lets us keep derived metrics longer than 30 days.
5. **Storage move** when rows pass a few hundred thousand. JSON in a repo does not carry it.
