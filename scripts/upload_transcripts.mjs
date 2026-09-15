#!/usr/bin/env node
// Narrative Radar — push local transcripts to the private search store.
//
//   node scripts/upload_transcripts.mjs                       # every narrative
//   node scripts/upload_transcripts.mjs anti-inflammatory-diet
//   node scripts/upload_transcripts.mjs --dry                 # count only, send nothing
//
// Reads corpus/<topic>/transcripts/*.txt (gitignored) for videos that are still
// in that narrative's videos.json, and sends them in batches to the engine's
// transcripts-ingest endpoint. The key comes from TRANSCRIPT_INGEST_KEY or the
// gitignored file .secrets/transcript-ingest-key — it must match the value set
// in the Netlify site's environment variables.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DRY = process.argv.includes("--dry");
const ONLY = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const API = process.env.NR_API || "https://lambent-salmiakki-6ea854.netlify.app";
const BATCH_CHARS = 2_500_000;   // keep each request well under Netlify's 6 MB body limit

const keyFile = path.join(ROOT, ".secrets", "transcript-ingest-key");
const KEY = (process.env.TRANSCRIPT_INGEST_KEY || (fs.existsSync(keyFile) ? fs.readFileSync(keyFile, "utf8") : "")).trim();
if (!KEY && !DRY) { console.error("No ingest key: set TRANSCRIPT_INGEST_KEY or create .secrets/transcript-ingest-key"); process.exit(2); }

async function send(topic, transcripts) {
  const r = await fetch(`${API}/api/transcripts-ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-ingest-key": KEY },
    body: JSON.stringify({ topic, transcripts }),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`HTTP ${r.status} ${JSON.stringify(body)}`);
  return body;
}

let grand = 0;
for (const topic of fs.readdirSync(path.join(ROOT, "corpus")).sort()) {
  if (ONLY.length && !ONLY.includes(topic)) continue;
  const tdir = path.join(ROOT, "corpus", topic, "transcripts");
  const vfile = path.join(ROOT, "corpus", topic, "videos.json");
  if (!fs.existsSync(tdir) || !fs.existsSync(vfile)) continue;
  const inCorpus = new Set(JSON.parse(fs.readFileSync(vfile, "utf8")).videos.map((v) => v.videoId));
  const files = fs.readdirSync(tdir).filter((f) => f.endsWith(".txt") && inCorpus.has(f.slice(0, -4)));
  if (!files.length) continue;
  let batch = {}, chars = 0, sent = 0, total = 0;
  const flush = async () => {
    if (!Object.keys(batch).length) return;
    if (!DRY) total = (await send(topic, batch)).total;
    sent += Object.keys(batch).length; batch = {}; chars = 0;
  };
  for (const f of files) {
    const text = fs.readFileSync(path.join(tdir, f), "utf8");
    if (chars + text.length > BATCH_CHARS) await flush();
    batch[f.slice(0, -4)] = text; chars += text.length;
  }
  await flush();
  grand += sent;
  console.log(`${topic.padEnd(28)} ${DRY ? "would send" : "sent"} ${sent}${DRY ? "" : ` · store now holds ${total}`}`);
}
console.log(`${DRY ? "dry run: " : ""}${grand} transcripts`);
