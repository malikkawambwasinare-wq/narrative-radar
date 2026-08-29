#!/usr/bin/env node
// Narrative Radar — the resolver.
//
// A ledger with no resolver is a to-do list. This is the job that wakes up,
// compares every open claim's structured horizon against the clock, and says
// what is ready to be judged.
//
// IT NEVER RULES. STANDARD.md §6: software says what is due, a named human says
// what is true. This script writes a docket and exits; no status in any
// predictions.json is ever changed by it.
//
//   node scripts/resolver.mjs              # print the docket
//   node scripts/resolver.mjs --write      # also write docket.json for the UI
//   node scripts/resolver.mjs --check      # exit 1 if anything is overdue (CI)
//
// Run it on a schedule. A ledger whose deadlines pass unnoticed is the failure
// mode this whole product exists to document in other people.

import fs from "node:fs";
import path from "node:path";

const root = path.join(import.meta.dirname, "..");
const WRITE = process.argv.includes("--write");
const CHECK = process.argv.includes("--check");

const GRACE_DAYS = 30;        // STANDARD.md §4 — fixed in advance, never extended
const STALE_DAYS = 60;        // ruling overdue this long past grace = a process failure
const SOON_DAYS = 90;         // "approaching" window for the brief

const DAY = 86400000;
const today = (process.env.RESOLVER_TODAY || new Date().toISOString().slice(0, 10));
const now = Date.parse(today + "T00:00:00Z");
const days = (iso) => Math.round((Date.parse(iso + "T00:00:00Z") - now) / DAY);

/* ---------- read every ledger ---------- */
const narratives = [];
for (const topic of fs.readdirSync(path.join(root, "corpus")).sort()) {
  const pf = path.join(root, "corpus", topic, "predictions.json");
  if (!fs.existsSync(pf)) continue;
  const doc = JSON.parse(fs.readFileSync(pf, "utf8"));
  let name = topic;
  try { name = JSON.parse(fs.readFileSync(path.join(root, "corpus", topic, "narrative.json"), "utf8")).name || topic; } catch {}
  narratives.push({ topic, name, doc });
}

/* ---------- classify each entry ---------- */
// open       — the window has not started
// in_window  — inside the stated window; the claim can still come good
// ripening   — window closed, inside the 30-day grace period
// due        — grace elapsed: ready to be ruled
// overdue    — due, and left unruled well past grace (a process failure, ours)
// resolved   — already ruled
// unscorable — no falsifiable window (STANDARD.md §3)
function stateOf(e) {
  if (e.status && e.status !== "PENDING") return "resolved";
  if (!e.due || !e.due.end) return "unscorable";
  const dEnd = days(e.due.end);
  const dStart = e.due.start ? days(e.due.start) : dEnd;
  if (dStart > 0) return "open";
  if (dEnd >= 0) return "in_window";
  if (-dEnd <= GRACE_DAYS) return "ripening";
  if (-dEnd <= GRACE_DAYS + STALE_DAYS) return "due";
  return "overdue";
}

const RANK = { overdue: 0, due: 1, ripening: 2, in_window: 3, open: 4, unscorable: 5, resolved: 6 };
const docket = [], flags = [], perNarrative = [];

for (const { topic, name, doc } of narratives) {
  const rows = (doc.entries || []).map((e) => {
    const state = stateOf(e);
    const dEnd = e.due?.end ? days(e.due.end) : null;
    return {
      topic, narrative: name, id: e.id,
      claimant: e.predictor || doc.predictor || "—",
      claim: e.claim, horizon: e.horizon,
      due: e.due || null, days_to_due: dEnd,
      resolution_class: e.resolution_class || "review",
      capture: e.capture || "n/a",
      status: e.status, state, source: e.source || null,
    };
  });
  docket.push(...rows);

  // Split candidates: an entry whose own notes record a datable sub-claim the
  // stated horizon does not cover. Surfaced for a human, never auto-created.
  for (const e of doc.entries || []) {
    if (/should be split into its own entry/i.test(e.due_basis || "")) {
      flags.push({ topic, id: e.id, kind: "split_candidate",
        note: "A datable sub-claim is recorded in outcome_note but the stated horizon is vague. Enter it as its own claim to put it on a clock." });
    }
  }

  const n = (f) => rows.filter(f).length;
  const scoreable = n((r) => r.resolution_class !== "unscorable");
  // Ruled = met a deadline and was judged. A moved goalpost was superseded, not
  // judged, so it is counted separately (STANDARD.md §4).
  const resolved = n((r) => ["SUPPORTED", "REFUTED", "AMBIGUOUS"].includes(r.status));
  const moved = n((r) => r.status === "UPDATED");
  perNarrative.push({
    topic, name,
    total: rows.length,
    scoreable,
    unscorable: n((r) => r.resolution_class === "unscorable"),
    unscorable_pct: rows.length ? Math.round(100 * n((r) => r.resolution_class === "unscorable") / rows.length) : 0,
    resolved, moved,
    supported: n((r) => r.status === "SUPPORTED"),
    // STANDARD.md §8 — counts below five scoreable resolutions, never a rate.
    rate_publishable: resolved >= 5,
    live: n((r) => r.capture === "live"),
    backfill: n((r) => r.capture === "backfill"),
    actionable: n((r) => r.state === "due" || r.state === "overdue"),
    // The next claim that lands on the judge's desk — its window close PLUS the
    // grace period, not the window close itself. A horizon that shut yesterday
    // is not yet judgeable, and saying "next due" of a past date reads as a bug.
    next: rows.filter((r) => ["open", "in_window", "ripening"].includes(r.state) && r.due?.end)
      .map((r) => ({ ...r, actionable_on: new Date(Date.parse(r.due.end + "T00:00:00Z") + GRACE_DAYS * DAY).toISOString().slice(0, 10) }))
      .sort((a, b) => a.actionable_on.localeCompare(b.actionable_on))[0] || null,
  });
}

docket.sort((a, b) => RANK[a.state] - RANK[b.state]
  || (a.due?.end || "9999").localeCompare(b.due?.end || "9999"));

/* ---------- report ---------- */
const actionable = docket.filter((r) => r.state === "due" || r.state === "overdue");
const soon = docket.filter((r) => ["ripening", "in_window"].includes(r.state)
  || (r.state === "open" && r.days_to_due !== null && r.days_to_due <= SOON_DAYS));

const pad = (s, n) => String(s ?? "").padEnd(n);
console.log(`RESOLVER · ${today} · standard 1.0 · ${GRACE_DAYS}-day grace\n`);

if (actionable.length) {
  console.log(`READY TO RULE (${actionable.length}) — the grace period has elapsed:\n`);
  for (const r of actionable) {
    console.log(`  ${r.state === "overdue" ? "OVERDUE" : "DUE    "} ${pad(r.id, 28)} ${pad(r.resolution_class, 11)} closed ${r.due.end} (${-r.days_to_due}d ago)`);
    console.log(`          ${r.claimant} — ${r.claim.slice(0, 96)}`);
    if (r.source) console.log(`          ${r.source}`);
  }
} else {
  console.log("READY TO RULE (0) — nothing has matured past its grace period.");
}

console.log(`\nAPPROACHING (${soon.length}):`);
for (const r of soon.slice(0, 10)) {
  const when = r.state === "ripening" ? `in grace, ${-r.days_to_due}d past close`
    : r.days_to_due >= 0 ? `closes in ${r.days_to_due}d` : `${-r.days_to_due}d past close`;
  console.log(`  ${pad(r.state, 11)} ${pad(r.id, 28)} ${when}`);
}

console.log("\nPER NARRATIVE:");
console.log("  " + pad("narrative", 24) + pad("entries", 9) + pad("scoreable", 11) + pad("unscorable", 12) + pad("ruled", 8) + pad("live", 6) + "next ruling due");
for (const s of perNarrative) {
  console.log("  " + pad(s.name.slice(0, 22), 24) + pad(s.total, 9) + pad(s.scoreable, 11)
    + pad(`${s.unscorable} (${s.unscorable_pct}%)`, 12)
    + pad(`${s.resolved}${s.rate_publishable ? "" : " *"}`, 8)
    + pad(s.live, 6) + (s.next ? `${s.next.actionable_on}  (${s.next.id})` : "—"));
}
console.log("  * fewer than 5 scoreable resolutions — counts shown, no rate published (STANDARD.md §8)");

if (flags.length) {
  console.log(`\nFLAGS (${flags.length}) — need a human, not a script:`);
  for (const f of flags) console.log(`  ${f.kind}  ${f.topic}/${f.id}\n    ${f.note}`);
}

const totals = {
  entries: docket.length,
  ready_to_rule: actionable.length,
  unscorable: docket.filter((r) => r.resolution_class === "unscorable").length,
  ruled: docket.filter((r) => ["SUPPORTED", "REFUTED", "AMBIGUOUS"].includes(r.status)).length,
  moved: docket.filter((r) => r.status === "UPDATED").length,
  live_capture: docket.filter((r) => r.capture === "live").length,
};
console.log(`\nTOTAL · ${totals.entries} claims · ${totals.ready_to_rule} ready to rule · `
  + `${totals.ruled} ruled · ${totals.moved} deadlines moved · ${totals.unscorable} unscorable · `
  + `${totals.live_capture} live-captured`);

if (WRITE) {
  const out = { generated: today, standard: "1.0", grace_days: GRACE_DAYS, totals, narratives: perNarrative, docket, flags };
  fs.writeFileSync(path.join(root, "docket.json"), JSON.stringify(out, null, 2) + "\n");
  console.log("\nWrote docket.json");
}

if (CHECK && docket.some((r) => r.state === "overdue")) {
  console.error("\nFAIL: claims are overdue past their grace period. Rule them or amend the standard.");
  process.exit(1);
}
