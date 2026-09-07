#!/usr/bin/env node
// Narrative Radar — spread trace: where a phrase was first observed, and where
// it was discussed over time, across platforms.
//
//   node scripts/trace-spread.mjs collapse-audit "debt supercycle"
//   node scripts/trace-spread.mjs collapse-audit "debt supercycle" --write
//
// TWO QUESTIONS, TWO DIFFERENT ANSWERS
//   1. Earliest observed — the oldest matching item each source can see.
//   2. Over time — how discussion volume moved, per source, by month.
//
// WHAT THIS DELIBERATELY DOES NOT SAY
// It never says "origin". The earliest thing a source can see is not the first
// time anyone said it: every source has a coverage horizon (Hacker News starts
// 2006, GDELT's article index starts 2017), most of the web is not indexed
// anywhere, and deleted material is invisible by construction. Every record
// carries the source's coverage window so a reader can see what the claim of
// "earliest" is actually worth.
//
// WHAT IT STORES
// Identifiers, dates and counts. No post text, no titles from social sources,
// no author names. Same rule as trace-origin.mjs: the corpus is a public,
// permanent git repository, so it holds pointers and our own observations, not
// other people's content.
//
// SOURCES (all free, no key, no account)
//   Hacker News (Algolia)  full-text, strict phrase, 2006-present
//   GDELT DOC 2.0          100k+ outlets, 65+ languages, volume timeline
//   Crossref               academic works — the "forked from research" layer
//   Bluesky                OPTIONAL: needs BSKY_HANDLE + BSKY_APP_PASSWORD
//
// GDELT NOTE: its HTTPS endpoint does not serve (verified 2026-08-29 — the
// certificate is valid, the TLS connection simply returns nothing), so this
// uses plain HTTP. That means the response is not authenticated in transit.
// Only aggregate volume is taken from it, never a claim about a named person,
// and the limitation is recorded in the output.

import fs from "node:fs";
import path from "node:path";

const root = path.join(import.meta.dirname, "..");
const [topic, phrase, ...rest] = process.argv.slice(2);
const WRITE = rest.includes("--write");

if (!topic || !phrase) {
  console.error("usage: node scripts/trace-spread.mjs <topic> \"<phrase>\" [--write]");
  process.exit(2);
}

const UA = "narrative-radar/1.0 (+https://github.com/malikkawambwasinare-wq/narrative-radar)";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const month = (iso) => (iso || "").slice(0, 7);
const norm = (s) => (s || "").toLowerCase().replace(/[‘’“”]/g, "'").replace(/\s+/g, " ");
const containsPhrase = (text) => norm(text).includes(norm(phrase));

async function getJSON(url, opts = {}) {
  // These are free public endpoints; being throttled is normal and means back
  // off, not fail. GDELT is the awkward one: when you exceed its limit it
  // answers HTTP 200 with a plain-text scolding rather than a 429, so a
  // status-code-only check never sees the real failure mode. Detect both.
  let last = "";
  for (let attempt = 0; attempt < 4; attempt++) {
    const r = await fetch(url, { headers: { "User-Agent": UA, ...(opts.headers || {}) }, ...opts });
    if (r.status === 429 || r.status === 503) { await sleep(6000 * (attempt + 1)); continue; }
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const body = await r.text();
    const head = body.slice(0, 200).trim();
    if (!head.startsWith("{") && !head.startsWith("[")) {
      last = head.slice(0, 120);
      if (/limit requests|rate|too many/i.test(head)) { await sleep(6000 * (attempt + 1)); continue; }
      throw new Error(`non-JSON response: ${last}`);
    }
    try { return JSON.parse(body); }
    catch { throw new Error("malformed JSON response"); }
  }
  throw new Error(`throttled after 4 attempts${last ? ` — "${last}"` : ""}`);
}
const tally = (dates) => {
  const m = {};
  for (const d of dates) if (d) m[month(d)] = (m[month(d)] || 0) + 1;
  return Object.entries(m).sort().map(([month, count]) => ({ month, count }));
};

/* ---------------- Hacker News · strict phrase, 2006-present ---------------- */
async function hackernews() {
  const src = { platform: "hackernews", coverage_from: "2006-10",
    unit: "matching stories and comments", method: "Algolia full-text, quoted phrase" };
  try {
    const d = await getJSON("https://hn.algolia.com/api/v1/search_by_date?query="
      + encodeURIComponent(`"${phrase}"`) + "&tags=(story,comment)&hitsPerPage=200");
    const hits = (d.hits || []).filter((h) =>
      containsPhrase([h.title, h.story_title, h.comment_text, h.story_text].join(" ")));
    const dates = hits.map((h) => h.created_at).filter(Boolean).sort();
    const first = hits.filter((h) => h.created_at === dates[0])[0];
    return { ...src, searched: true, total_matches: hits.length,
      reported_total: d.nbHits ?? null,
      earliest_observed: first ? { date: first.created_at.slice(0, 10), id: String(first.objectID),
        url: `https://news.ycombinator.com/item?id=${first.objectID}` } : null,
      timeline: tally(dates) };
  } catch (e) { return { ...src, searched: false, error: String(e.message) }; }
}

/* ---------------- GDELT · volume, tone, and WHERE — over time ----------------
   Three series, not one. Volume alone says how loud a story is; the other two
   say what kind of story it is:
     tone           — average sentiment of the coverage, so a narrative turning
                      darker is visible as a curve rather than an impression;
     source country — which countries' press carry it, normalized by each
                      country's own output, which is the "views from elsewhere"
                      signal. On "crypto winter" this puts the Philippines,
                      Singapore and Malaysia above the United States.
   GDELT publishes a hard limit of one request per 5 seconds. Respected below;
   exceeding it returns a plain-text scolding, not JSON. */
const GDELT_GAP = 5200;
async function gdelt() {
  const src = { platform: "gdelt_news", coverage_from: "2017-01",
    unit: "share of all monitored global coverage (normalized, not article counts)",
    method: "DOC 2.0 timelinevol + timelinetone + timelinesourcecountry, quoted phrase",
    transport_note: "fetched over plain HTTP — GDELT's HTTPS endpoint does not serve; response is unauthenticated in transit" };
  try {
    const q = encodeURIComponent(`"${phrase}"`);
    const call = (mode, months) => getJSON(
      `http://api.gdeltproject.org/api/v2/doc/doc?query=${q}&mode=${mode}&format=json&timespan=${months}m`);

    const d = await call("timelinevol", 60);
    const pts = (d.timeline?.[0]?.data || []).filter((p) => p.value > 0);

    // Tone: negative = more negative coverage. Reported as a monthly mean.
    await sleep(GDELT_GAP);
    let tone = [];
    try {
      const t = await call("timelinetone", 36);
      const byM = {};
      for (const p of t.timeline?.[0]?.data || []) {
        if (p.value === 0) continue;
        const m = `${p.date.slice(0, 4)}-${p.date.slice(4, 6)}`;
        (byM[m] = byM[m] || []).push(p.value);
      }
      tone = Object.entries(byM).sort()
        .map(([month, v]) => ({ month, mean_tone: +(v.reduce((a, b) => a + b, 0) / v.length).toFixed(3) }));
    } catch { /* optional series */ }

    // Where: total volume-intensity per country over the window.
    await sleep(GDELT_GAP);
    let countries = [];
    try {
      const c = await call("timelinesourcecountry", 12);
      countries = (c.timeline || [])
        .map((s) => ({ country: String(s.series).replace(/ Volume Intensity$/, ""),
          intensity: +(s.data || []).reduce((a, p) => a + p.value, 0).toFixed(3) }))
        .filter((x) => x.intensity > 0)
        .sort((a, b) => b.intensity - a.intensity)
        .slice(0, 15);
    } catch { /* optional series */ }

    src.tone_timeline = tone;
    src.top_countries = countries;
    src.country_note = "share of each country's OWN news output, so small media markets can outrank large ones — this measures where a story is proportionally loud, not raw article counts";
    const byMonth = {};
    for (const p of pts) {
      const m = `${p.date.slice(0, 4)}-${p.date.slice(4, 6)}`;
      byMonth[m] = Math.max(byMonth[m] || 0, p.value);
    }
    return { ...src, searched: true,
      nonzero_days: pts.length,
      earliest_observed: pts.length
        ? { date: `${pts[0].date.slice(0, 4)}-${pts[0].date.slice(4, 6)}-${pts[0].date.slice(6, 8)}`,
            id: null, url: null, note: "first day with non-zero coverage inside the 60-month window" }
        : null,
      peak: pts.length ? pts.reduce((a, b) => (b.value > a.value ? b : a)) : null,
      timeline: Object.entries(byMonth).sort().map(([month, peak_share]) => ({ month, peak_share })) };
  } catch (e) { return { ...src, searched: false, error: String(e.message) }; }
}

/* ---------------- Crossref · the research layer ---------------- */
async function crossref() {
  const SAMPLE = 200;
  const src = { platform: "crossref_research", coverage_from: "pre-1900",
    unit: "academic works whose title contains the phrase",
    method: `Crossref query.title, relevance-ranked top ${SAMPLE}, then STRICT client-side phrase check`,
    sampling_note: `EARLIEST WITHIN THE TOP ${SAMPLE} RELEVANCE-RANKED MATCHES, not necessarily the earliest in Crossref. Crossref matches title words loosely and cannot be date-sorted safely: sorting "quantitative easing" ascending returns 1802 German chemistry papers that share the word "quantitative". Relevance ranking surfaces the real matches; the price is a partial sample.` };
  try {
    const d = await getJSON(`https://api.crossref.org/works?rows=${SAMPLE}`
      + "&select=title,issued,DOI&query.title=" + encodeURIComponent(`"${phrase}"`),
      { headers: { "User-Agent": `${UA} mailto:malikkawambwasinare@gmail.com` } });
    const items = (d.message?.items || [])
      .map((it) => ({ title: (it.title || [])[0] || "", doi: it.DOI,
        parts: it.issued?.["date-parts"]?.[0] || [] }))
      .filter((it) => containsPhrase(it.title) && it.parts[0])
      .map((it) => ({ ...it, date: [it.parts[0], String(it.parts[1] || 1).padStart(2, "0"),
        String(it.parts[2] || 1).padStart(2, "0")].join("-") }))
      .sort((a, b) => a.date.localeCompare(b.date));
    return { ...src, searched: true,
      reported_total_before_filter: d.message?.["total-results"] ?? null,
      total_matches: items.length,
      earliest_observed: items[0]
        ? { date: items[0].date, id: items[0].doi, url: `https://doi.org/${items[0].doi}` } : null,
      timeline: tally(items.map((i) => i.date)) };
  } catch (e) { return { ...src, searched: false, error: String(e.message) }; }
}

/* ---------------- Wikipedia · when it became a named thing, and attention since ----------------
   Two signals the other sources cannot give:
     earliest_observed — the creation date of the article the idea lives under,
                         i.e. when it became nameable rather than merely said;
     timeline          — monthly pageviews, a public attention series.
   The matched article title is always reported, because the best-matching
   article is a judgement and the reader must be able to see what was matched. */
async function wikipedia() {
  const src = { platform: "wikipedia", coverage_from: "2001-01",
    unit: "monthly pageviews of the best-matching article",
    method: "search for the phrase, take the top article, then its first revision and pageview series",
    matching_note: "the top search result is not guaranteed to be the right article — the matched title is reported so it can be checked" };
  try {
    const s = await getJSON("https://en.wikipedia.org/w/api.php?action=query&list=search&format=json"
      + "&srlimit=1&srsearch=" + encodeURIComponent(`"${phrase}"`));
    const hit = s.query?.search?.[0];
    if (!hit) return { ...src, searched: true, total_matches: 0, earliest_observed: null, timeline: [] };
    const title = hit.title;

    const rev = await getJSON("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json"
      + "&rvlimit=1&rvdir=newer&rvprop=timestamp&titles=" + encodeURIComponent(title));
    const created = Object.values(rev.query?.pages || {})[0]?.revisions?.[0]?.timestamp || null;

    const key = encodeURIComponent(title.replace(/ /g, "_"));
    const end = new Date().toISOString().slice(0, 10).replace(/-/g, "") + "00";
    let views = [];
    try {
      const pv = await getJSON("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        + `en.wikipedia/all-access/all-agents/${key}/monthly/2015070100/${end}`,
        { headers: { "User-Agent": `${UA} mailto:malikkawambwasinare@gmail.com` } });
      views = (pv.items || []).map((i) => ({ month: `${i.timestamp.slice(0, 4)}-${i.timestamp.slice(4, 6)}`, count: i.views }));
    } catch { /* pageview series starts 2015-07; older or missing pages return 404 */ }

    return { ...src, searched: true,
      matched_article: title,
      total_matches: hit ? 1 : 0,
      article_hits: s.query?.searchinfo?.totalhits ?? null,
      earliest_observed: created
        ? { date: created.slice(0, 10), id: title,
            url: `https://en.wikipedia.org/wiki/${key}`,
            note: "article creation date — when the idea became a named entry, not when it was first said" }
        : null,
      timeline: views };
  } catch (e) { return { ...src, searched: false, error: String(e.message) }; }
}

/* ---------------- Bluesky · optional, needs a free app password ---------------- */
async function bluesky() {
  const src = { platform: "bluesky", coverage_from: "2023-02",
    unit: "matching posts", method: "app.bsky.feed.searchPosts, quoted phrase" };
  const handle = process.env.BSKY_HANDLE, pw = process.env.BSKY_APP_PASSWORD;
  if (!handle || !pw) {
    return { ...src, searched: false,
      error: "not connected — set BSKY_HANDLE and BSKY_APP_PASSWORD (a free Bluesky account and app password)" };
  }
  try {
    const s = await getJSON("https://bsky.social/xrpc/com.atproto.server.createSession", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ identifier: handle, password: pw }),
    });
    const d = await getJSON("https://bsky.social/xrpc/app.bsky.feed.searchPosts?limit=100&sort=latest&q="
      + encodeURIComponent(`"${phrase}"`), { headers: { Authorization: `Bearer ${s.accessJwt}` } });
    // Text is read only to verify the phrase; only ids and dates are kept.
    const posts = (d.posts || []).filter((p) => containsPhrase(p.record?.text || ""));
    const dates = posts.map((p) => p.record?.createdAt || p.indexedAt).filter(Boolean).sort();
    const first = posts.find((p) => (p.record?.createdAt || p.indexedAt) === dates[0]);
    return { ...src, searched: true, total_matches: posts.length,
      earliest_observed: first ? { date: dates[0].slice(0, 10), id: first.uri, url: first.uri } : null,
      timeline: tally(dates) };
  } catch (e) { return { ...src, searched: false, error: String(e.message) }; }
}

/* ---------------- run ---------------- */
console.log(`SPREAD TRACE · "${phrase}" · topic ${topic}\n`);

const sources = [];
// GDELT last: it is the strictest rate limiter (1 req / 5s) and makes three
// calls of its own, so the other sources buy it recovery time.
for (const [name, fn] of [["hackernews", hackernews], ["crossref", crossref],
                          ["wikipedia", wikipedia], ["bluesky", bluesky],
                          ["gdelt", gdelt]]) {
  process.stdout.write(`  ${name}…`);
  const r = await fn();
  sources.push(r);
  console.log(r.searched
    ? `\r  ${name.padEnd(12)} ${String(r.total_matches ?? r.nonzero_days ?? 0).padStart(5)} hits   earliest ${r.earliest_observed?.date || "—"}`
    : `\r  ${name.padEnd(12)}   skipped: ${r.error}`);
  await sleep(1500);   // these are free endpoints — be a good citizen
}

const found = sources.filter((s) => s.earliest_observed?.date)
  .sort((a, b) => a.earliest_observed.date.localeCompare(b.earliest_observed.date));

const out = {
  topic, phrase, traced_at: new Date().toISOString().slice(0, 10),
  // Deliberate wording. This is the earliest thing the searched sources can
  // SEE, which is a claim about our instruments, not about the world.
  confidence: "earliest_observed",
  earliest_observed_overall: found[0]
    ? { platform: found[0].platform, ...found[0].earliest_observed } : null,
  sources,
  caveats: [
    "EARLIEST OBSERVED, NOT ORIGIN. Each source has a coverage horizon; anything said before it, off it, or since deleted is invisible here.",
    "Absence of a match is not evidence the phrase was not used — it is evidence these sources did not index it.",
    "Timelines are not comparable across sources: Hacker News and Crossref are item counts, GDELT is a normalized share of global coverage.",
    "Only identifiers, dates and counts are stored. No post text, titles from social sources, or author names.",
    "GDELT is fetched over plain HTTP because its HTTPS endpoint does not serve; that response is unauthenticated in transit.",
  ],
};

console.log(`\nEARLIEST OBSERVED: ${out.earliest_observed_overall
  ? `${out.earliest_observed_overall.date} on ${out.earliest_observed_overall.platform}` : "nothing matched"}`);
console.log("(earliest these sources can see — not a claim about who said it first)\n");

const gd = sources.find((s) => s.platform === "gdelt_news");
if (gd?.top_countries?.length) {
  console.log("WHERE IT IS DISCUSSED — share of each country's own news output, last 12 months");
  const max = gd.top_countries[0].intensity;
  for (const c of gd.top_countries.slice(0, 10)) {
    console.log(`  ${c.country.padEnd(22)} ${"█".repeat(Math.max(1, Math.round((c.intensity / max) * 30)))} ${c.intensity}`);
  }
  console.log("  (small media markets can outrank large ones — this is proportional, not raw volume)\n");
}
if (gd?.tone_timeline?.length) {
  const t = gd.tone_timeline.slice(-12);
  console.log("TONE OF COVERAGE — negative is more negative");
  for (const p of t) {
    const n = p.mean_tone < 0;
    console.log(`  ${p.month}  ${n ? " ".repeat(14 - Math.min(14, Math.round(-p.mean_tone * 3))) + "▉".repeat(Math.min(14, Math.round(-p.mean_tone * 3))) + "│" : " ".repeat(14) + "│" + "▉".repeat(Math.min(14, Math.round(p.mean_tone * 3)))}  ${p.mean_tone}`);
  }
  console.log();
}

for (const s of sources.filter((x) => x.timeline?.length)) {
  const t = s.timeline;
  const key = "count" in t[0] ? "count" : "peak_share";
  const max = Math.max(...t.map((p) => p[key]));
  console.log(`${s.platform} — ${t.length} active months (${s.unit})`);
  for (const p of t.slice(-14)) {
    const bar = "█".repeat(Math.max(1, Math.round((p[key] / max) * 34)));
    console.log(`  ${p.month}  ${bar} ${key === "count" ? p[key] : p[key].toFixed(4)}`);
  }
  console.log();
}

if (WRITE) {
  const dir = path.join(root, "corpus", topic);
  if (!fs.existsSync(dir)) { console.error(`No corpus/${topic} — not written.`); process.exit(1); }
  fs.writeFileSync(path.join(dir, "spread.json"), JSON.stringify(out, null, 2) + "\n");
  console.log(`Wrote corpus/${topic}/spread.json`);
} else {
  console.log("Dry run — pass --write to save.");
}
