# The API audit application — draft answers

Prepared 2026-09-16. For YouTube's **Audit and Quota Extension Form**, reached from the
API Services terms page or from the Cloud console's YouTube Data API quota page.

**Why we are applying.** Two things we need are only allowed for audited clients:
storing derived data, which is what a narrative label, a verdict and a momentum figure are,
and holding statistics longer than the 30-day refresh window. The use case to select is
**Analytics and Reporting**, which since 2026-06-01 permits content categorisation and
tagging plus storage of statistics and derived metrics for up to 36 months. Extra quota
beyond the default 10,000 units matters less to us than the permission, since our own
measurements show the backfill fits inside the default allowance.

Answers below are drafts. Check each against the live form, since Google changes the
questions, and do not overstate anything: an audit compares claims against the product.

---

## 1. What the application does

Narrative Radar is a media-literacy tool. It follows recurring claims on YouTube, such as
"the housing crash is coming next year", and shows a viewer the whole pattern behind a
single video: how long the claim has been made, which channels make it, how the wording
changed over time, and what the different sides argue. The aim is to give a viewer context
before they act on one video.

It is a public web page. There is no account, no personalisation and no tracking of viewers.

## 2. How YouTube data is used

| Data | Use |
|---|---|
| Video ID, title, description, publish date | Matching a video to a recurring claim, and showing what was published when |
| Channel ID, title, upload counts | Measuring whether a claim recurs across independent channels |
| View, like and comment counts | Aggregate activity per claim over time |
| Duration, captions flag, category | Filtering and presentation |

Derived data we create: a narrative label per video, a content and packaging verdict where a
transcript is available, per-claim counts over time, and a channel tier that records whether
a channel's output recurs.

We display video titles with links back to YouTube, alongside our own labels. We do not
embed players in place of YouTube, republish descriptions in full, or present YouTube data
as our own.

## 3. Storage and retention

- Titles, descriptions and channel names are refreshed within 30 days or deleted.
- Statistics and derived metrics are retained up to 36 months, under the Analytics and
  Reporting exception.
- When a video becomes unavailable, its record and any transcript we hold for it are removed.
- Data lives in a public GitHub repository and in a private store for transcripts; the
  transcripts we hold do not come from the API.

## 4. What we do not do

- No scraping of YouTube pages. The project retired its scrapers on 2026-09-16 and its
  collection scripts refuse to run without an API key.
- No mixing of API data with data obtained outside the API.
- No advertising against YouTube data, and no resale of raw YouTube data.
- No personal data about viewers is collected or stored.
- No attempt to obtain captions for videos we do not own.

## 5. Quota justification

Measured on our own runs, not estimates:

| Purpose | Units a day | Basis |
|---|---|---|
| Channel uploads for known channels | 140 | Measured: 98 channels, 2,568 uploads read, 138 units |
| Screening new channels | up to 2,500 | 3 units per channel |
| Backfill of channel histories | up to 6,000 | 1 unit per 50 uploads |
| Refreshing titles inside the 30-day rule | ~330 per 500,000 records | 1 unit per 50 |
| Discovery search | 40 of the 100 search calls | Rotating query list |

At present this fits inside the default allowance. We are asking for the audited permission
first, and would request additional units only when the crawl list grows past roughly ten
thousand channels.

## 6. What the form will ask you to supply

1. The Google Cloud **project number** for the key.
2. The **API client name** and its public URL: Narrative Radar, https://malikkawambwasinare-wq.github.io/narrative-radar/
3. A **contact email**.
4. A **demonstration**: a short screen recording or screenshots showing a narrative page,
   where titles appear with links back to YouTube, and where our own labels are clearly ours.
5. Confirmation you accept the **Developer Policies**, including the 30-day refresh rule.

## 7. Before you submit

- Make sure the live page shows YouTube attribution on any view built from API data.
- Make sure nothing in the repo still reads YouTube pages. The retired scripts carry banners,
  and the daily workflows stop without a key.
- Expect questions. Answer them with measurements rather than claims, the way section 5 does.
