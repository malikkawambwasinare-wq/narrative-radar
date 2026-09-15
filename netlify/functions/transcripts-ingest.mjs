// Narrative Radar — write or delete transcripts in the private store.
//   POST   /api/transcripts-ingest  { topic, transcripts: { videoId: text, ... } }
//   DELETE /api/transcripts-ingest  { topic, videoIds: [...] }
// Header x-ingest-key must equal the TRANSCRIPT_INGEST_KEY environment variable.
//
// Transcripts are other people's words: they stay in this private, mutable
// store (so a transcript can be removed when its video is), never in git.
import { getStore } from "@netlify/blobs";

const json = (status, body) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

const MAX_TEXT = 600_000;   // characters per transcript; longest on file is ~130k

export default async (req) => {
  const key = process.env.TRANSCRIPT_INGEST_KEY;
  if (!key || key.length < 32 || req.headers.get("x-ingest-key") !== key) return json(401, { error: "unauthorized" });
  if (req.method !== "POST" && req.method !== "DELETE") return json(405, { error: "POST or DELETE" });

  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const topic = body.topic || "";
  if (!/^[a-z0-9-]{2,64}$/.test(topic)) return json(400, { error: "bad topic" });

  // Strong consistency: an upload batch must see the previous batch's write.
  const store = getStore({ name: "transcripts", consistency: "strong" });
  const blobKey = `topic/${topic}`;
  const current = (await store.get(blobKey, { type: "json" })) || {};

  if (req.method === "DELETE") {
    const ids = Array.isArray(body.videoIds) ? body.videoIds : [];
    let removed = 0;
    for (const id of ids) if (id in current) { delete current[id]; removed++; }
    await store.setJSON(blobKey, current);
    return json(200, { topic, removed, total: Object.keys(current).length });
  }

  const incoming = body.transcripts && typeof body.transcripts === "object" ? body.transcripts : {};
  let stored = 0;
  for (const [id, text] of Object.entries(incoming)) {
    if (!/^[\w-]{11}$/.test(id) || typeof text !== "string" || !text || text.length > MAX_TEXT) continue;
    current[id] = text; stored++;
  }
  await store.setJSON(blobKey, current);
  return json(200, { topic, stored, total: Object.keys(current).length });
};
