// Narrative Radar — the paste log: did this link land in a narrative we hold?
//   POST /api/paste-log   { events: [{ videoId, hit, topicId?, channel?, channelId? }] }
//   GET  /api/paste-log   → { pastes, hits, misses, rate, missedChannels: [...], since }
//
// One number runs the collection plan: the share of pasted links that land in a
// narrative we already hold. Above roughly three quarters, the library covers
// what people actually watch and further collection is vanity. Below it, the
// misses name the channels to add, so real interest drives collection instead
// of our heuristics.
//
// What is recorded: the video, its channel, and whether we held it. What is
// never recorded: anything about the person — no identity, no session, no
// history. This is a list of publishers, which is public behaviour.
import { getStore } from "@netlify/blobs";
import { guard } from "./_guard.mjs";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};
const json = (status, body) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...CORS } });

const KEY = "log";
const MAX_EVENTS = 20000;          // the tally is what matters; events are a rolling window
const MAX_PER_POST = 50;

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  const stop = await guard(req, { cost: 0 });
  if (stop) return stop;

  const store = getStore({ name: "paste-log", consistency: "strong" });
  const doc = (await store.get(KEY, { type: "json" })) || { pastes: 0, hits: 0, misses: 0, events: [], since: null };

  if (req.method === "GET") {
    const missed = {};
    for (const e of doc.events) {
      if (e.hit || !e.channel) continue;
      const m = (missed[e.channel] ||= { channel: e.channel, channelId: e.channelId || null, pastes: 0 });
      m.pastes++;
    }
    return json(200, {
      pastes: doc.pastes, hits: doc.hits, misses: doc.misses,
      rate: doc.pastes ? +(doc.hits / doc.pastes).toFixed(3) : null,
      missedChannels: Object.values(missed).sort((a, b) => b.pastes - a.pastes).slice(0, 50),
      since: doc.since, recent: doc.events.slice(-25),
    });
  }
  if (req.method !== "POST") return json(405, { error: "GET or POST" });

  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const events = Array.isArray(body.events) ? body.events.slice(0, MAX_PER_POST) : [];
  const now = new Date().toISOString();
  let kept = 0;
  for (const e of events) {
    if (!/^[\w-]{11}$/.test(e.videoId || "")) continue;
    doc.events.push({
      videoId: e.videoId, hit: !!e.hit,
      topicId: typeof e.topicId === "string" ? e.topicId.slice(0, 64) : null,
      channel: typeof e.channel === "string" ? e.channel.slice(0, 120) : null,
      channelId: /^UC[\w-]{22}$/.test(e.channelId || "") ? e.channelId : null,
      at: typeof e.at === "string" && e.at.length <= 24 ? e.at : now,
    });
    doc.pastes++; doc[e.hit ? "hits" : "misses"]++; kept++;
  }
  doc.events = doc.events.slice(-MAX_EVENTS);
  doc.since ||= now;
  if (kept) await store.setJSON(KEY, doc);
  return json(200, { stored: kept, pastes: doc.pastes, hits: doc.hits, misses: doc.misses,
    rate: doc.pastes ? +(doc.hits / doc.pastes).toFixed(3) : null });
};
