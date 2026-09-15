# Research 1 — YouTube's recommender: what it optimises, and how much is the algorithm

Researcher brief, 2026-09-15. Every source was opened (full text via PMC or the publisher where possible).

## 1. What the ranking optimises

**Covington, Adams & Sargin 2016, RecSys** — primary engineering paper; describes the 2016 system only.
- Two stages: candidate generation from implicit feedback (watches), then ranking by expected watch time per impression.
- Explicit signals (thumbs, surveys) were too sparse to train on.
- The paper itself notes that ranking by click-through "often promotes deceptive videos… ('clickbait')".

**Zhao et al. 2019, RecSys** — company A/B test.
- A multitask ranker predicts engagement (clicks, watch time) and satisfaction (likes, ratings, dismissals).
- The predictions are combined with weights that are "manually tuned" and not disclosed. A separate component corrects position bias.
- Live gains: engagement +0.45%, satisfaction +3.07%.

**YouTube's own account** — Goodrow (VP Engineering), 15 Sep 2021. Company claims, not independently audited.
- 2012: the switch from clicks to watch time caused "an immediate 20% drop in views".
- Now optimises "valued watchtime", based on 1–5-star surveys plus a model predicting survey answers for users who don't respond.
- 2019: demoting borderline content cut watch time on non-subscribed, recommended borderline content by 70% in the US.

**The "70% of watch time comes from recommendations" figure**
- Source: a single spoken claim by Neal Mohan at CES, 10 Jan 2018, reported by CNET. CBS's copy of the same article says 75%.
- No method was given. It covers all watch time (music, kids, gaming) and all screens.
- "Arrived through a recommendation" is not "caused by the algorithm": recommendations follow subscriptions and watch history.

## 2. Rabbit holes: algorithm or demand?

### Early audits (logged-out, pre-2019)

**Ribeiro et al. 2020, FAT\*** — observational audit.
- Commenters migrated from IDW/Alt-lite channels to Alt-right channels over time; Alt-right channels were reachable through channel recommendations.
- Commenters are not viewers, logged-out data shows no personalisation, and the migration can't be attributed to the algorithm.

**Ledwich & Zaitsev 2020, First Monday** — observational audit, with the same logged-out limitation.
- Found the opposite: logged-out recommendations favoured mainstream and cable-news channels.

### Real users and causal tests (post-2019 system)

**Hosseinmardi et al. 2021, PNAS** — 309,813-person US desktop panel, 2016–2019.
- Far-right viewers were 0.05% of the panel and stable over time.
- Routes to far-right videos: 36% from another video, 41% from external URLs, 8% from the homepage, 6% from search.
- "No evidence" that recommendations systematically cause far-right engagement.

**Chen, Nyhan, Reifler, Robertson & Wilson 2023, Science Advances** — the best-instrumented study so far. 1,181 people with a browser extension logging what was actually recommended, Jul–Dec 2020.
- Concentration: 15% saw any alternative-channel video and 6% any extremist video. 1.7% of participants accounted for 80% of alternative watch time; 0.6% for 80% of extremist watch time.
- Subscribers to the channel produced 61% of alternative views and 55% of extremist views. Links from outside YouTube produced about half.
- Strict rabbit-hole events were 0.01% of video visits.
- These viewers scored high on racial resentment and hostile sexism.
- Desktop only, so a lower bound.

**Hosseinmardi et al. 2024, PNAS** — causal test on the live system. Logged-in bots replayed 87,988 real user histories, Oct 2021–Dec 2022.
- Paths that followed only recommendations were less partisan than the users' own choices, especially for heavy partisan consumers.
- After switching to moderate content, the sidebar "forgets" a far-right history within about 30 videos; the homepage forgets more slowly.

**Haroon et al. 2023, PNAS** — 100,000 sock-puppet accounts.
- Recommendations were ideologically congenial, most on the homepage.
- Extremity rose significantly but was "substantively small".
- Problematic-channel recommendations went from 1.2% to 2.5% by the 10th video; 36.1% of accounts saw at least one.

**Liu et al. 2025, PNAS** — four RCTs, N = 8,883, on a YouTube-like site with real videos.
- Balanced versus slanted recommendations produced no detectable short-term attitude change.
- Slant did change behaviour: some moderates watched 4.9 of 23 minutes less.

### Settled

For US political content on desktop since 2019:
- Recommendations are not the main route to extreme content.
- Heavy viewing is concentrated among a small, resentful group, and runs through subscriptions and outside links.
- Recommendations match what a user already watches but are less extreme than the user's own choices.

### Contested or unknown

- Anything before 2019.
- Mobile, TV and Shorts.
- Non-English markets.
- Long-run cumulative exposure.
- Non-political harms.
- Whether the algorithm shaped the preferences these studies start from.

## 3. User controls and regret

**Mozilla "YouTube Regrets" 2021** — crowdsourced self-report from 37,380 volunteers and 3,362 reports.
- 71% of regretted videos were recommended rather than searched.
- Recommended videos were regretted 40% more often than searched ones.
- Rates were 60% higher in non-English-primary countries.

**Mozilla "Does This Button Work?" 2022** — randomised test on the live system: 22,722 volunteers, 500M+ recommendations.

How much each control reduced similar unwanted recommendations:

| Control | Reduction |
|---|---|
| "Don't recommend channel" | 43% |
| "Remove from history" | 29% |
| Dislike | 12% |
| "Not interested" | 11% |

39.3% of those surveyed felt the controls changed nothing.

## 4. Autoplay, defaults and session design

- **Schaffner et al. 2025, CSCW** — Netflix, 76 adults, randomised. Autoplay off cut viewing 21 minutes a day. Small RCT, not YouTube.
- **Hiniker et al. 2018, CHI** — field study, 24 homes with preschoolers. Autoplay after planned content lengthened viewing and weakened self-regulation.
- **Lukoff et al. 2021, CHI** — survey of 120 users. Autoplay and recommendations undermine sense of agency; search and playlists support it.
- **Allcott, Gentzkow & Song 2022, AER** — RCT, about 2,000 adults, YouTube among the apps tracked.
  - Self-set limits cut use 16%.
  - Their model attributes 31% of social-media use to self-control problems.
- **Grüning et al. 2023, PNAS** — friction before opening an app.
  - 280 users: 36% of attempts abandoned, and openings down 57% by week 6.
  - A follow-up with 500 people: the option to dismiss drove the effect; the reflective message alone did not.
- **"Take a break" and bedtime reminders** — no independent rigorous evaluation of YouTube's. One weak TikTok study suggests reminders can backfire.
- **Shorts** — no causal study. A 2025 meta-analysis (*Psychological Bulletin*) links heavier short-form use to poorer attention and inhibitory control, but it is correlational.

## 5. Negativity, outrage and engagement

- **Robertson et al. 2023, Nature Human Behaviour** — about 105,000 randomised headline variants, 370M impressions. Each negative word raised click-through 2.3%. Clicks only.
- **Brady et al. 2017, PNAS; Brady et al. 2025, PNAS Nexus** — moral-emotional words raise sharing about 13% (preregistered replication plus meta-analysis).
- **Rathje, Van Bavel & van der Linden 2021, PNAS** — each out-group word raised share odds 67%, about 4.8 times the effect of a negative word.
- **Milli et al. 2025, PNAS Nexus** — ranking by engagement amplified angry, out-group-hostile posts that users didn't actually prefer.
- **YouTube-specific** — one preprint (Park et al. 2026) associates outrage in titles and thumbnails with more views. Observational, not peer reviewed.
- **What transfers to YouTube:** negativity in titles and thumbnails wins clicks there too. Sharing effects transfer less, because YouTube ranks mainly on watch time and surveys.

## 6. What viewers themselves report

- **Pew 2018** — 4,594 US adults.
  - 81% at least occasionally watch recommended videos.
  - 64% sometimes see videos that seem obviously false.
  - In random walks through recommendations, videos got longer and more popular at each step.
- YouTube's move to survey-based "valued watchtime" is the company conceding that watch time and satisfaction diverge.

## Implications for a product competing for attention

- **Drop "escape the algorithm".** For today's YouTube it is mostly wrong: heavy fringe viewing is demand-driven and runs through subscriptions and outside links. Pitch "the angles you never saw" instead, and don't cite the 70% quote as evidence of harm.
- **The paste-a-link moment is the real entry point.** About half of problem views arrive from outside YouTube. Be where links get shared: the share sheet, a browser extension, messaging apps.
- **The problem is narrowness, not escalation.** Balanced exposure alone doesn't shift attitudes in the short term, so measure behaviour (fewer "watched one video and acted" moments), not opinion change.
- **Defaults beat buttons.** Autoplay off cut 21 minutes a day; "Not interested" works about 11% of the time. Put the narrative view in the default path, with a one-tap way to skip it.
- **Compete on valued time, not minutes.** Track regret and "was this worth it" as the north star.
- **Never rank by engagement.** It rebuilds the problem. Order by first appearance, evidence and track record, and label outrage framing.
- **Behaviour change is concentrated.** A small, loyal, resentful group drives most problem viewing. Neutral maps of the camps and each claim's history will land better with them than debunks.
- **Fill the gaps ourselves.** Mobile, Shorts, non-English audiences and long-run effects are unstudied. Run our own randomised tests.
