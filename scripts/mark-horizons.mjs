#!/usr/bin/env node
// Narrative Radar — stamp every extracted claim with horizon_dated: does its
// stated horizon name a date (year, month, quarter, "within 18 months") or not?
//
//   node scripts/mark-horizons.mjs                 # every topic
//   node scripts/mark-horizons.mjs collapse-audit  # one topic
//
// Deterministic, no model call; the Series page reads the stored boolean and
// never regexes horizons at view time. "next"/"soon"/"this cycle" are vague by
// design: a deadline the speaker can move at will is not a deadline.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// fileURLToPath, not URL.pathname: the repo path has spaces and a curly apostrophe.
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const MONTH = "jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?";
export const HORIZON_DATED_V1 = new RegExp(
  `(20\\d\\d|\\b(?:${MONTH})\\b|\\bQ[1-4]\\b|\\bH[12]\\b` +
  `|\\b(?:next|within|in|over the next|after)\\s?\\d+(?:-\\d+)?\\s?(?:day|week|month|year|decade)s?\\b` +
  `|\\b\\d+\\s?(?:-|to)\\s?\\d+\\s?(?:days|weeks|months|years)\\b|\\b\\d+\\s?(?:days|weeks|months|years)\\b|\\bnext (?:week|month|quarter|year)\\b)`, "i");

const only = process.argv[2];
const topics = fs.readdirSync(path.join(ROOT, "corpus")).filter((t) => !only || t === only);
for (const t of topics) {
  const f = path.join(ROOT, "corpus", t, "claims-extracted.json");
  if (!fs.existsSync(f)) continue;
  const claims = JSON.parse(fs.readFileSync(f, "utf8"));
  let dated = 0;
  for (const c of claims) {
    c.horizon_dated = HORIZON_DATED_V1.test(c.horizon || "");
    c.horizon_rule = "v1";
    if (c.horizon_dated) dated++;
  }
  fs.writeFileSync(f, JSON.stringify(claims, null, 2) + "\n");
  console.log(`${t}: ${dated}/${claims.length} claims name a date`);
}
