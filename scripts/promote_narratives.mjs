#!/usr/bin/env node
// Narrative Radar — promote a proposal into a tracked narrative.
//
//   node scripts/promote_narratives.mjs                    # report what would be promoted
//   node scripts/promote_narratives.mjs --write            # promote them
//   node scripts/promote_narratives.mjs --write --min-channels=5 --min-months=5
//
// A proposal is a claim the engine proved recurs. Promotion gives it the things
// a tracked narrative has: a place on the watchlist, its own corpus seeded with
// the videos that evidenced it, search queries so the daily sweep collects for
// it, and a hook title so a person can find it.
//
// The bar (both may be tightened by flags):
//   at least MIN_CHANNELS independent channels, and either MIN_MONTHS distinct
//   months or STRONG_CHANNELS channels — a claim carried by many voices in a
//   short window is live, not thin.
//
// Excluded by hand: a proposal that restates a narrative we already track under
// looser wording. The exclusions are listed in the output with their reason, so
// the judgment is visible rather than silent.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Anthropic from "@anthropic-ai/sdk";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const WRITE = process.argv.includes("--write");
const arg = (n, d) => (process.argv.find((a) => a.startsWith(`--${n}=`)) || "").split("=")[1] || d;
const MIN_CHANNELS = +arg("min-channels", 5);
const MIN_MONTHS = +arg("min-months", 5);
const STRONG_CHANNELS = +arg("strong-channels", 8);
const MODEL = arg("model", "claude-opus-5");
const TODAY = new Date().toISOString().slice(0, 10);

// Restatements of narratives already tracked, under wording loose enough to
// cover several subjects at once. Kept out with the reason on the record.
const EXCLUDE = {
  "crash started": "restates housing-crash-watch and collapse-audit; its titles mix property and stocks",
  "2008 crash": "a severity comparison used across both crash narratives we already track",
};

const rd = (f, d) => { try { return JSON.parse(fs.readFileSync(path.join(ROOT, f), "utf8")); } catch { return d; } };
const wr = (f, o) => fs.writeFileSync(path.join(ROOT, f), JSON.stringify(o, null, f.endsWith("watchlist.json") ? 1 : 2) + "\n");

const slug = (s) => s.toLowerCase().replace(/^the\s+/, "").replace(/["'’“”]/g, "")
  .replace(/\s+story$/, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").split("-").slice(0, 5).join("-");

const SCHEMA = {
  type: "object", additionalProperties: false, required: ["narratives"],
  properties: { narratives: { type: "array", items: {
    type: "object", additionalProperties: false,
    required: ["claim_name", "hook", "title_basis", "born", "born_note", "queries", "layman", "intermediate", "expert"],
    properties: {
      claim_name: { type: "string" },
      hook: { type: "string" },
      title_basis: { type: "string" },
      born: { type: "string" },
      born_note: { type: "string" },
      queries: { type: "array", items: { type: "string" } },
      layman: { type: "string" },
      intermediate: { type: "string" },
      expert: { type: "string" },
    } } } },
};

const SYSTEM = `You prepare a discovered narrative for tracking on Narrative Radar.

For each narrative you are given its attributed claim name, its claim, the evidence, and example titles. Return:

- hook: the title a person sees on the shelf. It must earn the click honestly. Keep the narrative's own search terms, open a real question the page can answer, and stay under 60 characters. State a pattern only if the evidence given supports it; otherwise ask it as a question. Never pair fear words with urgency words (warning, collapse, crash next to now, soon, about to), no ALL CAPS, no exclamation marks, no em dash. Examples of the register: "Housing Crash: Is It Always Next Year?", "Crypto Winter: Is the 4-Year Cycle Finally Dead?"
- title_basis: one short sentence saying what in the evidence justifies the hook.
- born: when this claim first appeared in public discourse, as YYYY or YYYY-MM. Your own estimate, not the corpus start date, since collection began later than the claim.
- born_note: one line on the basis of that estimate.
- queries: 5 YouTube search queries that would collect this narrative. Use the words its own believers and critics use. No quotation marks.
- layman, intermediate, expert: three explanations of the narrative, each at most 70 words. Layman: plain words, why it matters to them. Intermediate: the mechanism and the main camps. Expert: what would falsify it, who gains, where it is in its lifecycle.

Keep the claim_name exactly as given, so it can be matched back.`;

async function main() {
  if (!process.env.ANTHROPIC_API_KEY) { console.error("promote: no ANTHROPIC_API_KEY"); process.exit(2); }
  const proposals = (rd("narratives-proposed.json", { proposals: [] }).proposals || [])
    .filter((p) => p.verdict === "narrative" && !p.promoted);
  const wl = rd("watchlist.json", { topics: [] });
  const pool = rd("discovery-pool.json", { videos: [] });
  const byId = Object.fromEntries((pool.videos || []).map((v) => [v.videoId, v]));

  const pass = [], held = [];
  for (const p of proposals) {
    const e = p.evidence || {};
    const ok = (e.channels || 0) >= MIN_CHANNELS &&
      ((e.months || 0) >= MIN_MONTHS || (e.channels || 0) >= STRONG_CHANNELS);
    if (!ok) { held.push([p, `${e.channels || 0} channels over ${e.months || 0} months is under the bar`]); continue; }
    if (EXCLUDE[p.phrase]) { held.push([p, EXCLUDE[p.phrase]]); continue; }
    pass.push(p);
  }

  console.log(`promote · ${proposals.length} proposals · bar: ${MIN_CHANNELS}+ channels and (${MIN_MONTHS}+ months or ${STRONG_CHANNELS}+ channels)`);
  console.log(`  promoting ${pass.length} · holding ${held.length}`);
  for (const [p, why] of held.filter(([p]) => EXCLUDE[p.phrase])) console.log(`  held: ${p.claim_name} — ${why}`);
  if (!pass.length) return;

  const client = new Anthropic();
  const r = await client.messages.create({
    model: MODEL, max_tokens: 16000, system: SYSTEM,
    output_config: { format: { type: "json_schema", schema: SCHEMA }, effort: "high" },
    messages: [{ role: "user", content: pass.map((p) => {
      const e = p.evidence || {};
      return [`claim_name: ${p.claim_name}`, `claim: ${p.claim}`,
        `industry: ${p.industry}`,
        `evidence: ${e.videos} videos from ${e.channels} channels across ${e.months} months (${e.span})`,
        `clock: ${(p.frame || {}).clock || "none stated"}`,
        `example titles:`, ...(e.examples || []).slice(0, 3).map((t) => `  - ${t}`)].join("\n");
    }).join("\n\n") }],
  });
  const got = (r.parsed_output || JSON.parse(r.content.find((b) => b.type === "text")?.text || "{}")).narratives || [];
  const cost = (r.usage.input_tokens || 0) * 5e-6 + (r.usage.output_tokens || 0) * 25e-6;

  const done = [];
  for (const p of pass) {
    const g = got.find((x) => x.claim_name === p.claim_name) || got[pass.indexOf(p)];
    if (!g) { console.log(`  ! no title came back for ${p.claim_name}`); continue; }
    const id = slug(p.claim_name);
    if ((wl.topics || []).some((t) => t.id === id)) { console.log(`  ! ${id} already on the watchlist`); continue; }
    const e = p.evidence || {};
    const seed = (e.ids || []).map((vid) => byId[vid]).filter(Boolean).map((v) => ({
      videoId: v.videoId, title: v.title, channel: v.channel,
      url: `https://www.youtube.com/watch?v=${v.videoId}`,
      published: v.published, first_seen: v.found || TODAY,
      views: null, length: null, age_days: null,
      query: `discovered: ${p.phrase}`, transcript: null,
      verdict: "UNREVIEWED", verdict_basis: "metadata",
      yt: v.channelId ? { channelId: v.channelId } : {},
    }));

    wl.topics.push({
      id, name: g.hook, industry: p.industry || "Unsorted", status: "active", started: TODAY,
      trigger: `Found by the engine: "${p.phrase}" across ${e.channels} independent channels over ${e.months} months`,
      queries: (g.queries || []).slice(0, 6), watched_predictors: [],
      notes: `Promoted from a discovered proposal on ${TODAY}. ${p.claim}`,
      title_basis: g.title_basis, filters: "v2",
    });
    if (WRITE) {
      fs.mkdirSync(path.join(ROOT, "corpus", id), { recursive: true });
      wr(`corpus/${id}/narrative.json`, {
        name: p.claim_name,
        name_rule: "Attributed, not asserted (briefs/narratives/SYSTEM.md §3): a name is one more repetition of the claim.",
        claim: p.claim,
        predictor: "to be determined",
        born: g.born, born_note: `${g.born_note} (model estimate, pending audit)`,
        mutations: [],
        frame: p.frame || null,
        explanations: { layman: g.layman, intermediate: g.intermediate, expert: g.expert },
        origin: { type: "engine-discovery", phrase: p.phrase, created: TODAY,
          evidence: { videos: e.videos, channels: e.channels, months: e.months, span: e.span } },
      });
      wr(`corpus/${id}/videos.json`, { topic: id, updated: TODAY, videos: seed });
    }
    p.promoted = { id, on: TODAY, hook: g.hook };
    done.push({ id, hook: g.hook, seed: seed.length, name: p.claim_name });
  }

  for (const d of done) console.log(`  + ${d.id.padEnd(30)} ${d.seed} seed videos · ${d.hook}`);
  console.log(`  about US$${cost.toFixed(3)}`);

  if (WRITE && done.length) {
    wr("watchlist.json", wl);
    const prop = rd("narratives-proposed.json", {});
    wr("narratives-proposed.json", prop);      // p.promoted was set on these objects
    const promotedIds = new Set(pass.flatMap((p) => (p.evidence || {}).ids || []));
    pool.videos = (pool.videos || []).filter((v) => !promotedIds.has(v.videoId));
    wr("discovery-pool.json", pool);
    console.log(`  watchlist now ${wl.topics.length} narratives · pool trimmed to ${pool.videos.length}`);
  }
}

main().catch((e) => { console.error(e.message); process.exit(1); });
