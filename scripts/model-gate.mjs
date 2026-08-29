#!/usr/bin/env node
// Narrative Radar — model quality gate.
//
// analyze.mjs reads ANALYZE_MODEL, so switching to a cheaper model is a config
// change. DO NOT make that change on price alone: the per-video verdict feeds
// published accountability statistics ("7 of 38 original"), so a quiet drop in
// verdict quality is product damage wearing a saving's clothes.
//
// This script dual-runs the SAME prompt and schema production uses over real
// corpus videos and reports how often the candidate agrees with the Opus
// baseline. Ship the cheaper model only if it clears the bar.
//
//   ANTHROPIC_API_KEY=... node scripts/model-gate.mjs
//   ANTHROPIC_API_KEY=... node scripts/model-gate.mjs claude-haiku-4-5 40
//
// Cost: roughly (baseline + candidate) x N x ~$0.03. 30 videos ≈ $1.
//
// Bar (from the review of the collection-engine plan): >= 95% verdict
// agreement AND >= 95% decision agreement. Below that, the saving is not real.

import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
import path from "node:path";
import { SYSTEM, ANALYSIS_SCHEMA, summarizeCorpus, shortlistTopics } from "../netlify/functions/analyze.mjs";

const CANDIDATE = process.argv[2] || "claude-haiku-4-5";
const N = Number(process.argv[3]) || 30;
const BASELINE = process.env.BASELINE_MODEL || "claude-opus-5";
const BAR = 0.95;

const root = path.join(import.meta.dirname, "..");
const rd = (p) => JSON.parse(fs.readFileSync(path.join(root, p), "utf8"));

const watchlist = rd("watchlist.json");
const topics = watchlist.topics.map((t) => {
  const g = (f) => { try { return rd(`corpus/${t.id}/${f}`); } catch { return null; } };
  return { ...t, narrative: g("narrative.json"), videos: (g("videos.json") || {}).videos || [] };
});

// Sample real videos across the shelf, newest-heavy narratives first.
const sample = topics
  .flatMap((t) => t.videos.map((v) => ({ ...v, from: t.id })))
  .filter((v) => v.title && v.channel)
  .sort(() => 0.5 - Math.abs(0.5))          // stable order — reproducible runs
  .slice(0, N);

if (!sample.length) {
  console.error("No corpus videos found — nothing to measure.");
  process.exit(2);
}

const client = new Anthropic();

async function classify(model, meta) {
  const shortlist = shortlistTopics(topics, meta);
  const r = await client.messages.create({
    model,
    max_tokens: 2000,
    output_config: { effort: "low", format: { type: "json_schema", schema: ANALYSIS_SCHEMA } },
    system: SYSTEM,
    messages: [{
      role: "user",
      content: JSON.stringify({
        video_to_analyze: { videoId: meta.videoId, title: meta.title, channel: meta.channel },
        tracked_narratives: summarizeCorpus(shortlist),
      }),
    }],
  });
  if (r.stop_reason === "refusal") return { refused: true, usage: r.usage };
  return { ...JSON.parse(r.content.find((b) => b.type === "text").text), usage: r.usage };
}

const PRICE = {       // $ per million tokens, in / out
  "claude-opus-5": [5, 25], "claude-sonnet-5": [3, 15], "claude-haiku-4-5": [1, 5],
};
const spend = (model, u) => {
  const [i, o] = PRICE[model] || [5, 25];
  return ((u?.input_tokens || 0) * i + (u?.output_tokens || 0) * o) / 1e6;
};

console.log(`Gate: ${CANDIDATE} vs ${BASELINE} over ${sample.length} real corpus videos\n`);

let verdictHits = 0, decisionHits = 0, costA = 0, costB = 0;
const disagreements = [];

for (const [i, v] of sample.entries()) {
  process.stdout.write(`\r  ${i + 1}/${sample.length}…`);
  const [a, b] = await Promise.all([classify(BASELINE, v), classify(CANDIDATE, v)]);
  costA += spend(BASELINE, a.usage); costB += spend(CANDIDATE, b.usage);
  if (a.refused || b.refused) continue;
  if (a.verdict === b.verdict) verdictHits++;
  else disagreements.push({ title: v.title.slice(0, 62), base: a.verdict, cand: b.verdict });
  if (a.decision === b.decision) decisionHits++;
}

const vPct = verdictHits / sample.length, dPct = decisionHits / sample.length;
const pass = vPct >= BAR && dPct >= BAR;

console.log(`\r${" ".repeat(24)}\r`);
console.log(`verdict agreement  : ${(vPct * 100).toFixed(1)}%  (bar ${BAR * 100}%)`);
console.log(`decision agreement : ${(dPct * 100).toFixed(1)}%  (bar ${BAR * 100}%)`);
console.log(`cost this run      : ${BASELINE} $${costA.toFixed(4)} · ${CANDIDATE} $${costB.toFixed(4)}`
  + `  (${(costA / Math.max(costB, 1e-9)).toFixed(1)}x cheaper)`);

if (disagreements.length) {
  console.log(`\ndisagreements (${disagreements.length}):`);
  for (const d of disagreements.slice(0, 12)) {
    console.log(`  ${d.base.padEnd(10)} -> ${d.cand.padEnd(10)}  ${d.title}`);
  }
}

console.log(`\n${pass ? "PASS" : "FAIL"} — ${pass
  ? `set ANALYZE_MODEL=${CANDIDATE} in the function environment.`
  : `keep ${BASELINE}. The cheaper model changes published verdicts too often.`}`);
process.exit(pass ? 0 : 1);
