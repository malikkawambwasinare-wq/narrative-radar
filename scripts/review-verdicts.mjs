#!/usr/bin/env node
// Narrative Radar — upgrade provisional verdicts by actually reading the video.
//
//   node scripts/review-verdicts.mjs                     # dry run, all narratives
//   node scripts/review-verdicts.mjs collapse-audit --write
//   …  --limit 20    --all (re-review even transcript-based verdicts)
//
// THE PROBLEM THIS CLOSES
// A video pasted live gets its ORIGINAL/DERIVATIVE/RECYCLED/CLICKBAIT verdict
// from title + channel alone, and is stamped verdict_basis: "metadata". The
// series view promises no recycled content; a promise built on title guesses is
// exactly the thing this product exists to catch. So "provisional" is a STATE,
// not a caveat: run scripts/fetch_transcripts.py first (free), then this, and
// each provisional verdict is re-made with the transcript in hand and stamped
// verdict_basis: "transcript". The site shows which is which and the count of
// provisional entries falls to zero.
//
// Cost: one model call per video, ~6k tokens of transcript in. Roughly $0.03 on
// Opus 5; set REVIEW_MODEL=claude-haiku-4-5 once scripts/model-gate.mjs passes.

import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
import path from "node:path";

const root = path.join(import.meta.dirname, "..");
const argv = process.argv.slice(2);
const WRITE = argv.includes("--write"), ALL = argv.includes("--all");
const LIMIT = Number((argv[argv.indexOf("--limit") + 1] || 0)) || Infinity;
const ONLY = argv.filter((a, i) => !a.startsWith("--") && argv[i - 1] !== "--limit");
const MODEL = process.env.REVIEW_MODEL || "claude-opus-5";
const today = new Date().toISOString().slice(0, 10);

const SCHEMA = {
  type: "object", additionalProperties: false,
  required: ["verdict", "verdict_note", "is_update", "update_note"],
  properties: {
    verdict: { type: "string", enum: ["ORIGINAL", "DERIVATIVE", "RECYCLED", "CLICKBAIT"] },
    verdict_note: { type: "string" },
    is_update: { type: "boolean" },
    update_note: { type: ["string", "null"] },
  },
};

// The same four verdicts analyze.mjs uses, now judged from what was actually
// said rather than what the title promised.
const SYSTEM = `You grade ONE YouTube video for Narrative Radar, from its transcript, against a narrative it already belongs to.

verdict:
- ORIGINAL   — primary material: the speaker advances the narrative with a new claim, new mechanism, new evidence, or a first-hand position. An interview where the claimant states their own view is ORIGINAL.
- DERIVATIVE — commentary on claims already in the narrative: reacts to, summarises or debates someone else's claim without adding a new one. Honest commentary is DERIVATIVE, not RECYCLED.
- RECYCLED   — repackages existing material: a re-cut, clip compilation, re-upload, or a script that restates existing claims with nothing added.
- CLICKBAIT  — the title/thumbnail promises something the transcript does not deliver (a number, a prediction, a revelation that never appears).

Judge from the transcript. The title is evidence only of packaging. verdict_note ≤ 30 words, concrete: name what is new or what is repeated. Set is_update if the transcript introduces a claim or mechanism not in the narrative's consolidated claims; describe it in update_note.`;

function excerpt(txt, max = 24000) {
  if (txt.length <= max) return txt;
  const a = txt.slice(0, max * 0.6), b = txt.slice(-(max * 0.4));
  return `${a}\n\n[… ${txt.length - max} characters omitted …]\n\n${b}`;
}

const client = new Anthropic();
let changed = 0, reviewed = 0, spent = 0;

for (const topic of fs.readdirSync(path.join(root, "corpus")).sort()) {
  if (ONLY.length && !ONLY.includes(topic)) continue;
  const dir = path.join(root, "corpus", topic);
  const vf = path.join(dir, "videos.json");
  if (!fs.existsSync(vf)) continue;
  const doc = JSON.parse(fs.readFileSync(vf, "utf8"));
  const rd = (f) => { try { return JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")); } catch { return null; } };
  const narrative = rd("narrative.json") || {}, claims = rd("claims.json") || { claims: [] };
  const claimList = (claims.claims || []).map((c) =>
    c.statement + (c.camps ? " — camps: " + c.camps.map((k) => k.position).join(" / ") : ""));

  const todo = doc.videos.filter((v) => v.transcript && fs.existsSync(path.join(root, v.transcript))
    && (ALL || v.verdict_basis !== "transcript"));
  if (!todo.length) continue;
  console.log(`\n${topic} — ${todo.length} to review${ALL ? " (all)" : ""}`);

  for (const v of todo.slice(0, LIMIT - reviewed)) {
    const txt = fs.readFileSync(path.join(root, v.transcript), "utf8");
    let r;
    try {
      r = await client.messages.create({
        model: MODEL, max_tokens: 600,
        output_config: { effort: "low", format: { type: "json_schema", schema: SCHEMA } },
        system: SYSTEM,
        messages: [{ role: "user", content: JSON.stringify({
          narrative: { name: narrative.name, claim: narrative.claim, consolidated_claims: claimList },
          video: { title: v.title, channel: v.channel, published: v.published },
          transcript: excerpt(txt),
        }) }],
      });
    } catch (e) {
      if (/api key|authentication|401/i.test(String(e.message))) {
        console.error("\nNo model credentials. Set ANTHROPIC_API_KEY or run `ant auth login`, then re-run.");
        process.exit(3);
      }
      console.log(`  ! ${v.videoId}: ${String(e.message).slice(0, 80)}`); continue;
    }
    reviewed++;
    spent += ((r.usage?.input_tokens || 0) * (MODEL.includes("haiku") ? 1 : 5)
            + (r.usage?.output_tokens || 0) * (MODEL.includes("haiku") ? 5 : 25)) / 1e6;
    if (r.stop_reason === "refusal") { console.log(`  ! ${v.videoId}: declined`); continue; }
    const a = JSON.parse(r.content.find((b) => b.type === "text").text);
    const was = v.verdict;
    const mark = was === a.verdict ? " " : "→";
    console.log(`  ${was.padEnd(10)} ${mark} ${a.verdict.padEnd(10)} ${v.videoId}  ${(v.title || "").slice(0, 46)}`);
    console.log(`             ${a.verdict_note}`);
    if (was !== a.verdict) changed++;
    if (WRITE) {
      v.verdict = a.verdict;
      v.verdict_note = `[reviewed from transcript ${today}] ${a.verdict_note}`;
      v.verdict_basis = "transcript";
      v.reviewed_on = today;
      if (a.is_update && a.update_note) v.update_note = a.update_note;
    }
    if (reviewed >= LIMIT) break;
  }
  if (WRITE) fs.writeFileSync(vf, JSON.stringify(doc, null, 2) + "\n");
}

console.log(`\n${reviewed} reviewed · ${changed} verdicts changed · ≈$${spent.toFixed(2)} (${MODEL})`
  + (WRITE ? " · written" : " · dry run, pass --write"));
