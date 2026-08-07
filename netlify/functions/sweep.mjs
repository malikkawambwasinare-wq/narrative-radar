// Narrative Radar — refresh step 1: sweep YouTube for new videos in a narrative.
// POST /api/sweep {topic} → {new_videos: [videoId...]} (capped at 5 newest)
const REPO = "malikkawambwasinare-wq/narrative-radar";
const RAW = `https://raw.githubusercontent.com/${REPO}/main`;
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};
const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status, headers: { "Content-Type": "application/json", ...CORS },
  });

async function searchNewest(query) {
  const url = "https://www.youtube.com/results?search_query="
    + encodeURIComponent(query) + "&sp=CAI%253D";
  const r = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9",
      Cookie: "CONSENT=YES+cb; SOCS=CAI",
    },
  });
  if (!r.ok) return [];
  const html = await r.text();
  const ids = [];
  for (const m of html.matchAll(/"videoRenderer":\{"videoId":"([\w-]{11})"/g)) {
    if (!ids.includes(m[1])) ids.push(m[1]);
  }
  return ids;
}

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "POST") return json(405, { error: "POST only" });
  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const topicId = body.topic;
  if (!topicId) return json(400, { error: "topic required" });

  try {
    // Queries/known can come from the client (covers just-created narratives,
    // where the raw CDN hasn't caught up with the engine's commits yet)
    const watchlist = await (await fetch(`${RAW}/watchlist.json`)).json();
    const topic = watchlist.topics.find((t) => t.id === topicId);
    const queries = body.queries?.length ? body.queries : topic?.queries;
    if (!queries?.length) return json(404, { error: "unknown topic" });
    const known = new Set([
      ...(body.known || []),
      ...(await fetch(`${RAW}/corpus/${topicId}/videos.json`)
        .then((r) => r.json()).then((d) => d.videos.map((v) => v.videoId))
        .catch(() => [])),
    ]);
    // Fan out across the topic's queries; newest-first per query
    const results = await Promise.all(
      queries.slice(0, 6).map((q) => searchNewest(q).catch(() => [])),
    );
    const fresh = [];
    for (const ids of results) {
      for (const id of ids.slice(0, 8)) {
        if (!known.has(id) && !fresh.includes(id)) fresh.push(id);
      }
    }
    return json(200, { topic: topicId, new_videos: fresh.slice(0, 5), seen: fresh.length });
  } catch (e) {
    return json(500, { error: String(e.message || e).slice(0, 300) });
  }
};
