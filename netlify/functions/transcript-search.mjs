// Narrative Radar — search inside a narrative's transcripts.
//   GET /api/transcript-search?topic=<id>&q=<word or phrase>
//   → { searched, totalHits, videoCount, videos: [{ videoId, count, hits: [{ t, before, match, after }] }] }
//
// Transcripts live in a private Netlify Blobs store ("transcripts", one JSON
// object per narrative), uploaded from the collecting machine by
// scripts/upload_transcripts.mjs — never in the public repo. Responses carry
// timestamps and a short snippet around each match, nothing more.
import { getStore } from "@netlify/blobs";
import { guard } from "./_guard.mjs";
import { searchTranscripts } from "./_tsearch.mjs";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};
const json = (status, body, extra = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...CORS, ...extra } });

const TTL = 10 * 60 * 1000;
const cache = new Map();   // topic -> { at, map } — warm instances skip the blob read

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "GET") return json(405, { error: "GET only" });
  // No model call, so no spend units — only the per-IP burst limit applies.
  const blocked = guard(req, { cost: 0, cors: CORS });
  if (blocked) return blocked;

  const url = new URL(req.url);
  const topic = url.searchParams.get("topic") || "";
  const q = url.searchParams.get("q") || "";
  if (!/^[a-z0-9-]{2,64}$/.test(topic)) return json(400, { error: "bad topic" });

  try {
    let entry = cache.get(topic);
    if (!entry || Date.now() - entry.at > TTL) {
      const store = getStore({ name: "transcripts" });
      entry = { at: Date.now(), map: (await store.get(`topic/${topic}`, { type: "json" })) || {} };
      cache.set(topic, entry);
    }
    if (!Object.keys(entry.map).length) return json(200, { searched: 0, totalHits: 0, videoCount: 0, videos: [], note: "no transcripts uploaded for this narrative yet" });
    const result = searchTranscripts(entry.map, q);
    if (result.error) return json(400, result);
    return json(200, result, { "Cache-Control": "public, max-age=300" });
  } catch (e) {
    return json(500, { error: String(e.message || e).slice(0, 200) });
  }
};
