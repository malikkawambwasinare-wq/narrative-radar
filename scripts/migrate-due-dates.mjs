#!/usr/bin/env node
// Narrative Radar — one-off migration: give every ledger entry a STRUCTURED horizon.
//
// Prose horizons ("by ~2026-2028", "coming weeks to months") cannot be compared
// against a clock, so nothing could ever come due. The UI's parseHorizonDate
// took the FIRST four-digit year it saw, which read "by ~2026-2028" as
// 2026-07-01 and made collapse-audit's "next test" flip between due-now and
// 686 days out with no data change.
//
// Each entry gains:
//   due: { start, end, precision } | null      the window in which it is judgeable
//   resolution_class: auto | review | unscorable   per STANDARD.md §3
//   capture: live | backfill | n/a             per STANDARD.md §2, COMPUTED below
//   due_basis: string                          how the window was read from the prose
//
// The mapping is written out entry by entry rather than parsed, because these
// dates are load-bearing and must be reviewable in a diff. The claimant's own
// words in `horizon` are never altered — STANDARD.md §1 forbids sharpening a
// vague claim into a falsifiable one.
//
//   node scripts/migrate-due-dates.mjs          # dry run, prints the table
//   node scripts/migrate-due-dates.mjs --write  # writes the files

import fs from "node:fs";
import path from "node:path";

const root = path.join(import.meta.dirname, "..");
const WRITE = process.argv.includes("--write");

// The date each ledger file entered the repo — from `git log --diff-filter=A`.
// A claim recorded before its horizon closed is a LIVE capture; one recorded
// after is BACKFILL. Computed, never asserted.
const LEDGER_ADDED = {
  "collapse-audit": "2026-08-06",
  "crypto-winter-watch": "2026-08-07",
};

// precision: how tightly the claimant bounded it. Wider = weaker claim, and the
// ledger reports that rather than hiding it.
const DUE = {
  /* ---------- collapse-audit · Ray Dalio ---------- */
  "dalio-2015-1937":            ["2016-03-01", "2017-03-31", "range",  "review",     "'~1-2 years' from 2015-03"],
  "dalio-2016-supercycle":      [null, null, "none", "unscorable", "'unstated (vague)' — no horizon to judge against"],
  "dalio-2018-downturn":        ["2020-01-01", "2020-12-31", "year",   "review",     "'~2020'"],
  "dalio-2019-recession-risk":  ["2020-01-01", "2021-01-31", "range",  "review",     "'~1-2 years' from 2019-01"],
  "dalio-2020-cash-is-trash":   [null, null, "none", "unscorable", "'near-term' — no bounded window; 'cash is trash' also lacks a falsifiable threshold"],
  "dalio-2022-perfect-storm":   ["2023-10-01", "2024-10-31", "range",  "review",     "'~1-2 years' from 2022-10"],
  "dalio-2023-debt-crisis":     [null, null, "none", "unscorable", "'unstated (vague)'"],
  "dalio-2025-heart-attack":    ["2026-01-01", "2028-12-31", "range",  "review",     "'by ~2026-2028' — the FULL range; reading only the first year was the parser bug"],
  "dalio-2025-doac-dark-times": [null, null, "none", "unscorable", "'unstated (vague)'; 'very dark times' has no falsifiable condition"],
  "dalio-2025-debt-3yr":        ["2028-09-01", "2028-09-30", "month",  "review",     "'by ~2028', made 2025-09 — the first cleanly countable clock in this ledger"],
  "dalio-2026-capital-war":     [null, null, "none", "unscorable", "'near-term'; 'on the brink' has no falsifiable condition"],
  "dalio-2026-doac-80yr":       [null, null, "none", "unscorable", "stated horizon vague. NOTE: outcome_note records a datable sub-claim (House lost at the Nov 2026 midterms) that should be split into its own entry — flagged by the resolver, not auto-created"],

  /* ---------- crypto-winter-watch · multiple cycle-callers ---------- */
  "armstrong-2026-clarity":     ["2026-08-01", "2026-08-07", "month",  "review",     "'before the August 2026 Senate recess' — recess began the first week of August"],
  "gambardello-2026-pmi":       ["2026-09-01", "2026-09-01", "day",    "auto",       "'September 1, 2026 PMI print' — settles on the published ISM manufacturing PMI"],
  "gerhard-2026-selloff":       [null, null, "none", "unscorable", "'coming weeks to months' — unbounded"],
  "soloway-2026-35k":           ["2026-10-01", "2026-11-30", "range",  "auto",       "'by October-November 2026'; a named BTC price settles it"],
  "klippsten-2026-bottom":      ["2026-10-20", "2026-10-31", "range",  "review",     "'late October 2026'; 'the bottom' is only knowable in hindsight — interpretation required"],
  "ivan-2026-bottom":           ["2026-10-01", "2027-02-28", "range",  "review",     "'Oct-Nov 2026 bottom; Jan-Feb 2027 blow-off' — two-legged claim, judged on the full span"],
  "fibswanny-2026-low-now":     ["2026-08-01", "2026-10-31", "range",  "review",     "'August-October 2026'"],
  "hougan-2026-higher":         ["2026-12-31", "2026-12-31", "day",    "auto",       "'December 31, 2026'; a year-end price comparison settles it"],
  "hougan-2027-bull":           ["2027-01-01", "2027-12-31", "year",   "review",     "'2027'; 'bull market' needs a stated threshold the claimant did not give"],
  "phongle-2027-bull":          ["2027-08-01", "2027-08-31", "month",  "review",     "'by August 2027'"],
  "sophie-2028-cycle-intact":   ["2027-01-01", "2028-12-31", "range",  "review",     "'2027-2028'; 'cycle intact' is interpretive"],
  "saylor-1m-no-winters":       [null, null, "none", "unscorable", "'unstated (vague)' — a price target with no date cannot be missed"],
  "ark-2030-710k":              ["2030-01-01", "2030-12-31", "year",   "auto",       "'2030'; a named BTC price target settles it"],
  "pal-2030-singularity":       ["2030-01-01", "2030-12-31", "year",   "review",     "'by 2030'; 'singularity' has no agreed measurable definition"],
};

let touched = 0, missing = [], rows = [];

for (const topic of fs.readdirSync(path.join(root, "corpus"))) {
  const file = path.join(root, "corpus", topic, "predictions.json");
  if (!fs.existsSync(file)) continue;
  const doc = JSON.parse(fs.readFileSync(file, "utf8"));
  const added = LEDGER_ADDED[topic];

  for (const e of doc.entries || []) {
    const spec = DUE[e.id];
    if (!spec) { missing.push(`${topic}/${e.id}`); continue; }
    const [start, end, precision, cls, basis] = spec;

    e.due = start ? { start, end, precision } : null;
    e.resolution_class = cls;
    // STANDARD.md §2 — computed from the ledger's own git history, not asserted.
    e.capture = !end ? "n/a" : (added && end > added ? "live" : "backfill");
    e.due_basis = basis;
    touched++;
    rows.push([topic, e.id, e.status, cls, start ? `${start} → ${end}` : "—", e.capture]);
  }

  // Record which standard version this ledger is maintained under.
  doc.standard = { version: "1.0", url: "STANDARD.md" };
  if (WRITE) fs.writeFileSync(file, JSON.stringify(doc, null, 2) + "\n");
}

const w = (s, n) => String(s).padEnd(n);
console.log(w("narrative", 22) + w("entry", 30) + w("status", 11) + w("class", 12) + w("due window", 26) + "capture");
console.log("-".repeat(105));
for (const r of rows) console.log(w(r[0], 22) + w(r[1], 30) + w(r[2], 11) + w(r[3], 12) + w(r[4], 26) + r[5]);

const by = (k, v) => rows.filter((r) => r[k] === v).length;
console.log("-".repeat(105));
console.log(`${touched} entries · auto ${by(3, "auto")} · review ${by(3, "review")} · unscorable ${by(3, "unscorable")}`
  + ` · live ${by(5, "live")} · backfill ${by(5, "backfill")}`);
if (missing.length) console.log(`\nNOT IN THE TABLE (left untouched): ${missing.join(", ")}`);
console.log(WRITE ? "\nWritten." : "\nDry run — pass --write to apply.");
