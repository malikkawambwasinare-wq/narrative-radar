# Research — Collecting YouTube at scale: limits, methods, completeness, terms

Researcher brief, sources checked 2026-09-15. API pages last updated 2026-09-14.

**Headline finding:** search cannot backfill a narrative. Recall for past periods collapses 20–60 days after upload. Channel crawling is the only viable backfill; search is for discovery and the live window.

## 1. Facts

### Scale of YouTube

**McGrady, Zheng, Curran, Baumgartner & Zuckerman 2023**, "Dialing for Videos" (*JQD:DM* 3). Random-ID sampling, Oct–Dec 2022: 10,016 hits from ~18.7 trillion guesses.
- ~9.88 billion public searchable videos.
- Median views: 35. 4.88% have zero views; 86.93% have under 1,000.
- 72.64% have no comments.
- The 3.67% of videos with 10k+ views hold 93.61% of all views.
- "People & Blogs" (the default category) holds 55.82% of videos. When the paper's coders agreed on a category, it matched the uploader's category only 28.39% of the time.

**Later estimates**
- Zuckerman, Dec 2023: ~13.3 billion videos; 4+ billion uploaded in 2023 (≈11 million/day).
- TubeStats, sample dated 2024-06-17: ~14.83 billion; median views 41; median length 64 s.

### YouTube Data API v3

**Quotas** (changed 2026-06-01)
- `search.list` has its own bucket: **100 calls/day**, 1 unit each.
- Everything else shares **10,000 units/day**.
- `videos.batchGetStats` (added 2026-06-03) has its own 10,000/day bucket.

**Costs**
- 1 unit: `videos.list`, `channels.list`, `playlistItems.list`, `channelSections.list`.
- 50 units: `captions.list`.
- Captions of other people's videos are not retrievable: `captions.download` needs edit rights, so claims made only in speech are invisible to the API.

**Search limits**
- 50 results per page. `totalResults` is approximate, capped at 1,000,000.
- About 500 results per query in practice.
- Non-relevance orders "might result in a smaller or incomplete result set".
- The docs say not to use search for a channel's recent uploads; use its uploads playlist.
- `regionCode` restricts by viewability. `relevanceLanguage` is a preference, not a filter.
- `relatedToVideoId` was removed 2023-08-07.

**Time-slicing fails for the past** (Rieder, Padilla & Coromina 2025, *Information, Communication & Society*)
- Recall collapses 20–60 days after upload, although the videos still exist.

  | "European Parliament election" (relevance order) | Results |
  |---|---|
  | Day after the vote | 8,354 |
  | +5 weeks | 3,035 (−64%) |
  | +10 weeks | 635 (−92%) |

- Running "chatgpt" 10 times in a row found 773 videos instead of 456.
- Efstratiou (IMC 2025): repeated identical searches drift over 12 weeks; lookups by video ID stay stable.

### Developer policies

- **30-day storage.** Unauthenticated API data may be stored in "limited amounts" for **30 days maximum**, then refreshed or deleted.
- **No derived data.** API clients must not "create new or derived data or metrics", or aggregate API data for insight into YouTube's business.
- **No quota stacking.** One API client = one project. The terms prohibit circumventing quotas.
- **New derived-metrics exception** (2026-06-01), for audited "Analytics & Reporting" use cases:
  - Allows "Content Categorization and Tagging" (what narrative labels are).
  - Allows storing statistics and derived metrics for up to 36 months.
  - Titles, descriptions and creator names still refresh every 30 days.
- **Quota beyond default** requires a compliance audit (Audit and Quota Extension Form). No turnaround is published.
- **Metric break:** public view counting changed on 2026-08-27 to count from the first frame. Before/after comparisons don't hold.

### Channel crawling

- `channels.list` returns each channel's uploads playlist; `playlistItems.list` returns 50 items per unit (title, description, publish date).
- **Uploads playlists stop at the latest 20,000 videos** (Google issue 166292064, marked "Working As Intended"). Very prolific news outlets can't be crawled back further.
- New uploads from known channels: PubSubHubbub push notifications, zero quota.
- **Snowball precedents**
  - Ribeiro et al. 2020: seed channels + the first 200 search results per keyword + two hops of featured channels → 349 channels, 330,925 videos.
  - YouNiverse 2021: 136k channels, 72.9M videos, from channelcrawler lists.
  - Rieder et al. 2020: a sample of 36M+ channels.

### YouTube Researcher Program

- Eligible: accredited non-profit degree-granting institutions in listed countries (Kenya included).
- Research cannot be sold commercially; findings must be published.
- Quota comes with justification; derived metrics are allowed; the 30-day refresh still applies until data is frozen.
- **A commercial Narrative Radar does not qualify.**

### topicCategories

- Wikipedia-URL topic labels on videos and channels. Coarse: Society covers Business, Health, Military, Politics and Religion; Technology sits under Lifestyle; there is no Economy or AI category.
- No validation study found. The weak category agreement in McGrady et al. suggests caution.
- **Use as a weak signal to seed the industry layer, not as the taxonomy.**

### Estimating completeness

- **Capture–recapture.** Estimate the total from the overlap of independent lists.
  - Lawrence & Giles 1998 (*Science*): overlap between search engines gives a lower bound.
  - Spoor et al. 1996; Kastner et al. 2009: four databases found 68% of an estimated 1,838 articles.
- **Stopping rules.** Callaghan & Müller-Hansen 2020; Cormack & Grossman 2016.
- **Pitfalls that make completeness look better than it is.**
  - Dependent lists, or items that differ in how easy they are to find (popular videos are found more often), inflate the overlap. That underestimates the total N. Chao 1987 gives a lower bound that corrects for this.
  - A list that feeds another breaks standard models (Jones et al. 2014). Channels found via search are exactly this.
  - The population is assumed closed, but videos get deleted.

### Topic corpora in practice

- **Knuutila et al. 2021.** Defined "all" by where videos were shared, not by search: 1,091,876 YouTube links in COVID-keyword posts on Facebook, Reddit and Twitter, of which 8,122 were removed as misinformation.
- **Rieder et al. 2025.** Defined "all" as all results from day-sliced searches, then showed that this definition changes over time.

### Scraping

- YouTube's Terms (2023-12-15) ban access "using any automated means (such as robots, botnets or scrapers)", except public search engines following robots.txt or with written permission.
- The Developer Policies ban API clients from scraping or obtaining scraped data. **Mixing scraping with the API jeopardises API access.**

## 2. What "all videos on a narrative" can honestly mean

Proposed public wording:

> "As of [date], every public YouTube video published in [window] whose title, description or tags express [claim X], reachable by our documented methods through the YouTube Data API — queries Q run within 20 days of upload, plus the complete upload histories of channel set C. We report the count found and an estimated total, with a 95% interval, for this reachable population. Excluded: claims made only in speech, private, unlisted or deleted videos, channel back catalogues beyond 20,000 videos, and languages outside L."

**Never claim "every video ever uploaded".** The estimate cannot see videos that no method could reach.

## 3. Recommended architecture

**Industry layer**
- Our own taxonomy. topicCategories and category IDs are weak signals only.

**Narrative layer**
- A claim definition, plus 2–3 query sets with separate vocabularies (keywords, entities, hashtags).
- One relevance classifier applied to every source.

**Search: discovery and the live window**
- 100 calls/day across 120 narratives means rotating: 24 narratives/day × 4 calls (2 query variants × 2 pages), with a 7-day `publishedAfter`.
- Every narrative is covered every 5 days, inside the ~20-day recall window.
- Store the channel IDs from every result.

**Why search can't do the backfill**

| Approach | Calls needed | At 100 calls/day |
|---|---|---|
| 120 narratives × 20 quarters × 3 queries (first page only) | 7,200 | 72 days |
| Same, paging each query to 500 results | 72,000 | ~720 days |
| Day-sliced, the research-grade method (120 × 1,825 days) | 219,000 | ~6 years |

Past-period recall is also down 64–92% anyway.

**Channel crawling: the backfill**
- Seed channels from:
  - search results;
  - outside lists (outlet lists, fact-check databases, off-platform shares);
  - featured channels (`channelSections.list`).
- Crawl uploads playlists. Example: 10,000 channels × 500 uploads = 5M records = 100,000 units ≈ 10 days of default quota.
- Classify each video from its snippet. Fetch `videos.list` only for relevant videos: at a 3% relevance rate, ~150k videos ≈ 3,000 units.
- Discard irrelevant records within 30 days.
- **Crawling wins** for backfill older than ~20 days and for narratives with clear producer channels.
- **Crawling loses** for claims scattered across one-off uploaders, and for channels with 20k+ back catalogues.

**Steady state**

| Task | Daily quota |
|---|---|
| New uploads from known channels (push notifications) | 0 |
| Refresh a 500k-video corpus every 30 days (stats via `batchGetStats`) | ~333 units |
| Add new channels | ~1,000–2,000 units |

After the backfill, this fits the default quota.

**Completeness per narrative**
- **List A:** videos found by search.
- **List B:** videos from channel crawling that did *not* come from this narrative's search results (independent seeds).
- Same classifier, window and as-of date for both.
- **Chapman estimator**
  - N = (nA+1)(nB+1)/(m+1) − 1, where m = videos in both lists.
  - Var = (nA+1)(nB+1)(nA−m)(nB−m) / ((m+1)²(m+2)).
  - Completeness = |A∪B| / N.
- **Worked example:** nA = 800, nB = 600, m = 400 → N ≈ 1,200 (95% CI 1,152–1,247); completeness 83% (80–87%).
- **With 3+ lists:** fit log-linear models that allow pairwise dependence.
- **With repeated search runs:** report Chao's lower bound, N ≥ S_obs + f1²/(2·f2), where f1 and f2 are videos seen exactly once and twice.
- **Assumptions:** a closed population on the as-of date; independent lists; equal findability; identical relevance labelling. Violations usually overstate completeness, so **label the figure an upper bound**.
- Validate against a small gold set built outside YouTube.

## 4. What needs an extension, and a timeline (12 industries × 10 narratives)

**Needs the audit (Analytics & Reporting use case)**
- Storing narrative labels and derived metrics at all.
- Keeping statistics beyond 30 days.
- More than 100 searches/day.
- Backfill faster than ~10 days per 5M crawled records.

**Researcher Program:** only through a genuine academic partner, and its data can't feed the commercial product.

**Timeline** (planning assumptions, not published service levels)

| Weeks | Work |
|---|---|
| 0–2 | Taxonomy and claim definitions; pipeline; file the audit |
| 2–6 | Discover channels (~1,200 searches ≈ 12 days); start live search rotation immediately, since every day of delay loses videos from the 20-day window |
| 4–10 | Channel crawl on default quota (~10 days per 5M records; ~2 days per 5M at a hypothetical 50,000 units/day); hand-label gold sets |
| ~10 | First completeness estimates per narrative |

**Audit approval is the unknown that sets the pace.** Until approved: keep only data that is refreshed within 30 days, and publish no derived metrics.
