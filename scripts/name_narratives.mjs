#!/usr/bin/env node
// Narrative Radar — the naming pass: read each candidate cluster and decide
// whether it is a narrative.
//
//   node scripts/name_narratives.mjs                 # report, writes nothing
//   node scripts/name_narratives.mjs --write         # write narratives-proposed.json
//   node scripts/name_narratives.mjs --limit=20 --write
//
// Why this exists
//   Counting finds phrases that recur. At scale the phrases that recur most are
//   sales formulas — "shocking truth", "nobody sees it coming" — because they
//   travel everywhere precisely by being about nothing. Telling a claim from a
//   catchphrase takes reading, so this is the one stage that uses a model, and
//   it reads clusters (about a hundred) rather than videos (tens of thousands).
//
// What it returns per cluster
//   narrative  — a claim about the world, with its name in its believers' words
//   rhetoric   — a turn of phrase, a genre, or a format. Recorded, never re-proposed
//   duplicate  — a restatement of a narrative we already track
//
// Costs are reported at the end from the API's own token counts.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Anthropic from "@anthropic-ai/sdk";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const WRITE = process.argv.includes("--write");
const arg = (n, d) => (process.argv.find((a) => a.startsWith(`--${n}=`)) || "").split("=")[1] || d;
const LIMIT = +arg("limit", 200);
const BATCH = +arg("batch", 8);
const MODEL = arg("model", "claude-opus-5");
const PRICE = { in: 5 / 1e6, out: 25 / 1e6 };      // claude-opus-5, US$ per token

const read = (f, dflt) => { try { return JSON.parse(fs.readFileSync(path.join(ROOT, f), "utf8")); } catch { return dflt; } };

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["decisions"],
  properties: {
    decisions: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["phrase", "verdict", "why", "claim_name", "claim", "industry", "frame", "duplicate_of"],
        properties: {
          phrase: { type: "string" },
          verdict: { type: "string", enum: ["narrative", "rhetoric", "duplicate"] },
          why: { type: "string" },
          claim_name: { type: ["string", "null"] },
          claim: { type: ["string", "null"] },
          industry: { type: ["string", "null"] },
          duplicate_of: { type: ["string", "null"] },
          frame: {
            type: ["object", "null"],
            additionalProperties: false,
            required: ["problem", "cause", "outcome", "clock"],
            properties: {
              problem: { type: ["string", "null"] },
              cause: { type: ["string", "null"] },
              outcome: { type: ["string", "null"] },
              clock: { type: ["string", "null"] },
            },
          },
        },
      },
    },
  },
};

const SYSTEM = `You decide which repeated phrases on YouTube are narratives.

A NARRATIVE is a claim about the world that could turn out to be wrong: it frames a problem, names a cause, and implies an outcome or a remedy. It is told by many independent channels over months. Examples: "the US housing market will crash next year", "seed oils drive chronic disease", "AGI arrives within two years".

RHETORIC is a phrase that recurs because of how it sells, not what it claims: "shocking truth", "nobody saw it coming", "you won't believe", "expert explains". Also rhetoric: genres and formats ("market close", "weekly recap"), and subjects with no claim attached ("plane crash", "earnings beat").

Judge the phrase by the example titles, which are real titles from the corpus. If the titles do not share one checkable claim, it is rhetoric, however often the phrase recurs. Be strict: a wrongly admitted narrative pollutes the product, while a rejected one can be proposed again when more evidence arrives.

For a narrative, write:
- claim_name: the claim in its believers' own words, ATTRIBUTED and never asserted, in the form The "<claim>" story. A believer should accept it as a fair statement of what they believe. Add no villain, out-group or moral words the narrative itself does not use.
- claim: one or two sentences stating what is claimed.
- frame: the problem it names, the cause it blames, the outcome or remedy it implies, and the clock it runs on (null if the claim carries no date).
- industry: exactly one of the shelves listed in the request, or null if none fit.

Mark DUPLICATE when the phrase restates a narrative already tracked, and name it in duplicate_of.

why: one short sentence, in your own words, for the decision.`;

async function main() {
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error("naming pass: no ANTHROPIC_API_KEY set; nothing read.");
    process.exit(2);
  }
  const cands = (read("discovered.json", { candidates: [] }).candidates || [])
    .filter((c) => c.kind !== "sub-claim").slice(0, LIMIT);
  if (!cands.length) { console.log("naming pass: no candidates to read"); return; }

  const shelves = (read("industries.json", { industries: [] }).industries || []).map((i) => i.name);
  const tracked = (read("watchlist.json", { topics: [] }).topics || [])
    .map((t) => `${t.id}: ${t.name}`);
  const client = new Anthropic();

  const out = [];
  let inTok = 0, outTok = 0, stopped = null;
  for (let i = 0; i < cands.length; i += BATCH) {
    if (stopped) break;
    const slice = cands.slice(i, i + BATCH);
    const body = slice.map((c, n) => [
      `${n + 1}. phrase: "${c.phrase}"`,
      `   evidence: ${c.videos} videos from ${c.channels} independent channels across ${c.months} months (${c.span})`,
      ...(c.also?.length ? [`   also worded: ${c.also.slice(0, 4).join("; ")}`] : []),
      `   example titles:`,
      ...(c.examples || []).slice(0, 3).map((t) => `     - ${t}`),
    ].join("\n")).join("\n\n");

    let r;
    try {
      r = await client.messages.create({
      model: MODEL,
      max_tokens: 8000,
      system: SYSTEM,
      output_config: { format: { type: "json_schema", schema: SCHEMA }, effort: "medium" },
      messages: [{
        role: "user",
        content: `Shelves to choose from: ${shelves.join(" · ")}\n\n` +
          `Narratives already tracked (a restatement of one of these is a duplicate):\n${tracked.join("\n")}\n\n` +
          `Decide on each phrase below. Return one decision per phrase, in order.\n\n${body}`,
      }],
      });
    } catch (e) {
      // Stop on the first failure and keep what was already read, so a run that
      // dies halfway (a spent balance, a rate limit) is not thrown away.
      stopped = e.message || String(e);
      break;
    }
    inTok += r.usage.input_tokens || 0;
    outTok += r.usage.output_tokens || 0;
    const parsed = r.parsed_output || JSON.parse(r.content.find((b) => b.type === "text")?.text || "{}");
    for (const d of parsed.decisions || []) {
      const src = slice.find((c) => c.phrase === d.phrase) || slice[out.length % slice.length];
      out.push({ ...d, evidence: src ? { videos: src.videos, channels: src.channels, months: src.months, span: src.span, examples: src.examples, ids: src.ids?.slice(0, 20) } : null });
    }
    process.stdout.write(`  read ${Math.min(i + BATCH, cands.length)}/${cands.length}\r`);
  }

  // Batches are read independently, so the same claim can be admitted twice
  // under different wording ("AI will replace your job" / "AI will replace these
  // jobs"). One more pass merges them, because a narrative told twice on the
  // shelf is the repetition we exist to expose.
  let merges = [];
  const admitted = out.filter((d) => d.verdict === "narrative");
  if (!stopped && admitted.length > 1) {
    try {
      const m = await client.messages.create({
        model: MODEL,
        max_tokens: 4000,
        system: "You merge narratives that state the same claim. Two entries belong together when a believer in one would say the other is the same belief in different words. Different claims about the same subject stay separate: 'a recession is coming' and 'the job market is collapsing' are different claims. Keep the name that states the claim most plainly, and list every phrase in the group.",
        output_config: { format: { type: "json_schema", schema: {
          type: "object", additionalProperties: false, required: ["groups"],
          properties: { groups: { type: "array", items: {
            type: "object", additionalProperties: false, required: ["claim_name", "phrases"],
            properties: { claim_name: { type: "string" }, phrases: { type: "array", items: { type: "string" } } } } } } } } },
        messages: [{ role: "user", content:
          `Group these narratives. Return every group, including groups of one.\n\n` +
          admitted.map((d) => `- phrase "${d.phrase}" → ${d.claim_name}: ${d.claim}`).join("\n") }],
      });
      inTok += m.usage.input_tokens || 0;
      outTok += m.usage.output_tokens || 0;
      const g = m.parsed_output || JSON.parse(m.content.find((b) => b.type === "text")?.text || "{}");
      merges = (g.groups || []).filter((x) => (x.phrases || []).length > 1);
      for (const group of merges) {
        const keep = admitted.find((d) => d.phrase === group.phrases[0]);
        if (!keep) continue;
        keep.claim_name = group.claim_name;
        keep.merged_from = group.phrases.slice(1);
        for (const ph of group.phrases.slice(1)) {
          const dup = out.find((d) => d.phrase === ph && d.verdict === "narrative");
          if (!dup) continue;
          dup.verdict = "duplicate";
          dup.duplicate_of = group.claim_name;
          dup.why = "Same claim as another proposal, merged.";
          keep.evidence = keep.evidence && dup.evidence ? {
            ...keep.evidence,
            videos: (keep.evidence.videos || 0) + (dup.evidence.videos || 0),
            channels: Math.max(keep.evidence.channels || 0, dup.evidence.channels || 0),
            months: Math.max(keep.evidence.months || 0, dup.evidence.months || 0),
          } : keep.evidence;
        }
      }
    } catch (e) { console.log(`  merge step skipped: ${e.message}`); }
  }

  const by = (v) => out.filter((d) => d.verdict === v);
  console.log(`\nnaming pass · ${cands.length} clusters read · ${MODEL}`);
  console.log(`  narratives ${by("narrative").length} · rhetoric ${by("rhetoric").length} · duplicates ${by("duplicate").length}` +
    (merges.length ? ` · merged ${merges.length} group${merges.length === 1 ? "" : "s"}` : ""));
  for (const d of by("narrative")) {
    console.log(`\n  ${d.claim_name}`);
    console.log(`    ${d.claim}`);
    console.log(`    ${d.industry} · ${d.evidence?.channels} channels · ${d.evidence?.months} months · clock: ${d.frame?.clock || "none"}`);
  }
  const cost = inTok * PRICE.in + outTok * PRICE.out;
  if (stopped) console.log(`\n  STOPPED after ${out.length} of ${cands.length}: ${stopped}`);
  console.log(`\n  ${inTok} input tokens, ${outTok} output tokens · about US$${cost.toFixed(3)}`);

  if (WRITE) {
    fs.writeFileSync(path.join(ROOT, "narratives-proposed.json"), JSON.stringify({
      generated: new Date().toISOString().slice(0, 10), model: MODEL,
      note: "Candidate clusters read by a model: which are narratives, which are turns of phrase, which restate what we track.",
      cost_usd: +cost.toFixed(4), proposals: out,
    }, null, 1) + "\n");
    console.log(`  wrote narratives-proposed.json`);
  }
  if (stopped) process.exit(3);
}

main().catch((e) => { console.error(e.message); process.exit(1); });
