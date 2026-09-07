#!/usr/bin/env node
// Narrative Radar — podcast transcript evidence.
//
//   node scripts/podcast-evidence.mjs "The Diary Of A CEO" "debt cycle"
//   node scripts/podcast-evidence.mjs "The Diary Of A CEO" "debt cycle" --topic collapse-audit --write
//   …            --limit 60      how many transcript-bearing episodes to scan (default 40)
//
// WHY THIS EXISTS
// The engine's single biggest quality gap is that verdicts are inferred from a
// video's title and channel — analyze.mjs writes `transcript: null` and labels
// its own output "metadata-only". So "RECYCLED" is an informed guess about
// something nobody read.
//
// Podcasts are the one place that gap closes for free. The `podcast:transcript`
// RSS tag carries a full, timestamped, speaker-agnostic transcript, published
// by the show itself. No ASR bill, no scraping, no key. And long-form
// predictive claims incubate on podcasts before they are clipped for YouTube —
// the flagship narrative in this corpus was triggered by a Diary Of A CEO
// episode.
//
// WHAT IT PRODUCES
// For a phrase, the episodes that actually contain it, and WHERE — a timestamp
// you can jump to. That turns "he says this a lot" into "he said it at 34:12 on
// 2026-07-30, here is the link."
//
// WHAT IT STORES
// Episode ids, dates, transcript URLs, match timestamps and counts. NOT the
// transcript text. A transcript is someone else's content and this corpus is a
// public, permanent git repository; the timestamp plus the URL lets any reader
// hear it for themselves, which is stronger evidence than a quote we typed out.
// Downloaded transcripts are cached under .cache/ and gitignored.

import fs from "node:fs";
import path from "node:path";

const root = path.join(import.meta.dirname, "..");
const argv = process.argv.slice(2);
const flag = (n, d) => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : d; };
const [show, phrase] = argv.filter((a, i) => !a.startsWith("--") && !String(argv[i - 1] || "").startsWith("--"));
const TOPIC = flag("--topic", null);
const LIMIT = Number(flag("--limit", 40));
const WRITE = argv.includes("--write");

if (!show || !phrase) {
  console.error('usage: node scripts/podcast-evidence.mjs "<show name or feed url>" "<phrase>" [--topic <id>] [--limit N] [--write]');
  process.exit(2);
}

const UA = "narrative-radar/1.0 (+https://github.com/malikkawambwasinare-wq/narrative-radar)";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const norm = (s) => (s || "").toLowerCase().replace(/[‘’“”]/g, "'").replace(/\s+/g, " ");
const CACHE = path.join(root, ".cache", "transcripts");
fs.mkdirSync(CACHE, { recursive: true });

async function text(url) {
  const r = await fetch(url, { headers: { "User-Agent": UA }, redirect: "follow" });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.text();
}

/* ---------- 1. resolve the show to an RSS feed ---------- */
async function resolveFeed(q) {
  if (/^https?:\/\//.test(q)) return { feed: q, title: q };
  const r = JSON.parse(await text("https://itunes.apple.com/search?media=podcast&limit=5&term="
    + encodeURIComponent(q)));
  const hit = (r.results || []).find((x) => x.feedUrl);
  if (!hit) throw new Error(`no feed found for "${q}"`);
  return { feed: hit.feedUrl, title: hit.collectionName, artist: hit.artistName };
}

/* ---------- 2. pull the feed's transcript-bearing episodes ---------- */
function parseFeed(xml) {
  const items = xml.split("<item>").slice(1).map((chunk) => {
    const grab = (re) => (chunk.match(re) || [])[1]?.trim() || null;
    const title = grab(/<title>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/title>/);
    const pub = grab(/<pubDate>([\s\S]*?)<\/pubDate>/);
    const guid = grab(/<guid[^>]*>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/guid>/);
    const link = grab(/<link>([\s\S]*?)<\/link>/);
    // Prefer a text transcript; VTT and SRT are timestamped, plain text is not.
    const tags = [...chunk.matchAll(/<podcast:transcript\b([^>]*)\/?>/g)].map((m) => m[1]);
    const pick = tags.find((a) => /vtt/i.test(a)) || tags.find((a) => /srt/i.test(a)) || tags[0];
    const turl = pick ? (pick.match(/url="([^"]+)"/) || [])[1] : null;
    return { title, date: pub ? new Date(pub).toISOString().slice(0, 10) : null, guid, link, transcript_url: turl };
  });
  return items;
}

/* ---------- 3. search one transcript, keep positions not prose ---------- */
// VTT cues are only a few words long, so a multi-word phrase routinely straddles
// a cue boundary — "…the 80" / "year cycle…". Searching cue-by-cue therefore
// misses exactly the phrases worth searching for: an early version of this
// reported zero hits for "80 year" in an episode that says it three times.
//
// So: flatten the transcript into one string while recording, for each
// character offset, the timestamp of the cue it came from. Search the flat
// text; map each match back to its cue's timestamp.
const CUE = /(\d{2}:\d{2}:\d{2})[.,]\d+\s*-->\s*[\d:.,]+\s*\n([\s\S]*?)(?=\n\s*\n|\Z)/g;
function flatten(vtt) {
  let flat = "";
  const marks = [];               // [charOffsetWhereCueStarts, timestamp]
  let m;
  CUE.lastIndex = 0;
  while ((m = CUE.exec(vtt))) {
    marks.push([flat.length, m[1]]);
    flat += norm(m[2]) + " ";
  }
  if (!marks.length) return { flat: norm(vtt), marks: [] };   // no cue structure
  return { flat, marks };
}
function stampAt(marks, offset) {
  let lo = 0, hi = marks.length - 1, best = null;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (marks[mid][0] <= offset) { best = marks[mid][1]; lo = mid + 1; } else hi = mid - 1;
  }
  return best;
}
function findInVtt(vtt, needle) {
  const n = norm(needle);
  const { flat, marks } = flatten(vtt);
  const hits = [];
  let i = flat.indexOf(n);
  while (i !== -1) {
    hits.push(stampAt(marks, i));
    i = flat.indexOf(n, i + n.length);
  }
  return hits;
}

/* ---------- run ---------- */
const meta = await resolveFeed(show);
console.log(`PODCAST EVIDENCE · "${phrase}"`);
console.log(`show : ${meta.title}${meta.artist ? ` — ${meta.artist}` : ""}`);
console.log(`feed : ${meta.feed}\n`);

const xml = await text(meta.feed);
const all = parseFeed(xml);
const withT = all.filter((e) => e.transcript_url);
console.log(`episodes in feed        : ${all.length}`);
console.log(`with published transcript: ${withT.length}  (${Math.round(100 * withT.length / Math.max(all.length, 1))}% — the rest cannot be searched this way)`);
console.log(`scanning the newest      : ${Math.min(LIMIT, withT.length)}\n`);

const results = [];
let scanned = 0, failed = 0;
for (const ep of withT.slice(0, LIMIT)) {
  const key = path.join(CACHE, encodeURIComponent(ep.transcript_url).slice(-120));
  let body;
  try {
    if (fs.existsSync(key)) body = fs.readFileSync(key, "utf8");
    else { body = await text(ep.transcript_url); fs.writeFileSync(key, body); await sleep(250); }
  } catch { failed++; continue; }
  scanned++;
  const hits = findInVtt(body, phrase);
  if (hits.length) {
    results.push({ title: ep.title, date: ep.date, episode_guid: ep.guid, link: ep.link,
      transcript_url: ep.transcript_url, match_count: hits.length,
      timestamps: hits.filter(Boolean).slice(0, 12) });
    console.log(`  ${ep.date}  ${String(hits.length).padStart(3)}×  ${(ep.title || "").slice(0, 62)}`);
    if (hits[0]) console.log(`              first at ${hits[0]}`);
  }
}

console.log(`\nscanned ${scanned} transcripts${failed ? ` (${failed} unreachable)` : ""} · ${results.length} contain the phrase`
  + ` · ${results.reduce((a, r) => a + r.match_count, 0)} total mentions`);

if (!results.length) {
  console.log("No mentions found. That is a fact about these transcripts, not about the show.");
}

if (WRITE) {
  if (!TOPIC) { console.error("\n--write needs --topic <id>"); process.exit(1); }
  const dir = path.join(root, "corpus", TOPIC);
  if (!fs.existsSync(dir)) { console.error(`\nNo corpus/${TOPIC}`); process.exit(1); }
  const out = {
    topic: TOPIC, phrase, show: meta.title, feed: meta.feed,
    traced_at: new Date().toISOString().slice(0, 10),
    episodes_in_feed: all.length, episodes_with_transcript: withT.length, scanned,
    episodes: results,
    storage_note: "Episode identifiers, dates, transcript URLs and match timestamps only. No transcript text is stored — the timestamp plus the URL lets a reader hear the passage at source, which is stronger than a quote we typed.",
    caveats: [
      `Only ${withT.length} of ${all.length} episodes publish a transcript, so absence of a match is not absence of the claim.`,
      "Matching is literal. A paraphrase of the same claim will not be found.",
      "Transcripts are published by the show and may contain transcription errors; a timestamp is a pointer to audio, not a certified quotation.",
    ],
  };
  fs.writeFileSync(path.join(dir, "podcast-evidence.json"), JSON.stringify(out, null, 2) + "\n");
  console.log(`\nWrote corpus/${TOPIC}/podcast-evidence.json`);
}
