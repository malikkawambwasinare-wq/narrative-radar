// Narrative Radar — refresh step 3: re-consolidate a narrative's core claims.
// Delta design: Claude sees only the not-yet-cited videos and returns additions
// (sources joining existing claims) + genuinely new claims. The server merges,
// commits claims.json, and returns the full result. Keeps output small enough
// for the function's time budget.
// POST /api/consolidate {topic} → {claims, persisted}
import Anthropic from "@anthropic-ai/sdk";

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

const SOURCE = {
  type: "object", additionalProperties: false,
  required: ["videoId", "predictor"],
  properties: { videoId: { type: "string" }, predictor: { type: "string" } },
};

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["additions", "new_claims", "fingerprints"],
  properties: {
    fingerprints: { type: "array", items: { type: "string" } },
    additions: {
      type: "array",
      items: {
        type: "object", additionalProperties: false,
        required: ["claim_id", "camp_index", "sources"],
        properties: {
          claim_id: { type: "string" },
          camp_index: { type: ["integer", "null"] },
          sources: { type: "array", items: SOURCE },
        },
      },
    },
    new_claims: {
      type: "array",
      items: {
        type: "object", additionalProperties: false,
        required: ["id", "type", "statement", "note", "camps", "sources"],
        properties: {
          id: { type: "string" },
          type: { type: "string", enum: ["consensus", "contested"] },
          statement: { type: "string" },
          note: { type: "string" },
          camps: {
            type: ["array", "null"],
            items: {
              type: "object", additionalProperties: false,
              required: ["position", "sources"],
              properties: {
                position: { type: "string" },
                sources: { type: "array", items: SOURCE },
              },
            },
          },
          sources: { type: ["array", "null"], items: SOURCE },
        },
      },
    },
  },
};

const SYSTEM = `You maintain the consolidated claims of a tracked narrative for Narrative Radar. Input: the current consolidated claims (contested claims have camps listed with camp_index), and the corpus videos NOT yet cited by any claim.

Return a small delta:
- additions: uncited videos that carry an EXISTING claim → attach as sources ({claim_id, camp_index (null for consensus claims), sources:[{videoId, predictor}]}). Judge from title/channel/verdict/analyst-note. Only attach when the video genuinely carries that claim.
- new_claims: only if several uncited videos together support a claim not yet consolidated (or a clearly contested question). Statements ≤ 30 words, notes ≤ 35 words stating what makes it trackable.
- Videos that fit nothing (clickbait shells, off-claim content) are simply omitted.
- fingerprints: 2-3 short literal phrases (2-5 words) that people repeating THIS narrative actually type — used for exact-phrase archive search on X. Most distinctive first. Draw them from the corpus vocabulary (titles, claim statements), never invent wording; distinctive enough to exclude unrelated topics, natural enough that early adopters wrote them verbatim.
Never invent sources. Return empty arrays if nothing changes (fingerprints may still be returned).`;

const ghHeaders = () => ({
  Authorization: `Bearer ${process.env.GH_TOKEN}`,
  Accept: "application/vnd.github+json",
  "User-Agent": "narrative-radar-engine",
});

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "POST") return json(405, { error: "POST only" });
  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const topicId = body.topic;
  if (!topicId) return json(400, { error: "topic required" });

  try {
    const [rawVideos, current] = await Promise.all([
      fetch(`${RAW}/corpus/${topicId}/videos.json`).then((r) => r.json())
        .then((d) => d.videos).catch(() => []),
      fetch(`${RAW}/corpus/${topicId}/claims.json`).then((r) => r.json())
        .catch(() => ({ claims: [] })),
    ]);
    // Client may supply its live corpus (raw CDN lags fresh engine commits)
    const byId = new Map();
    for (const v of [...rawVideos, ...(body.videos || [])]) {
      if (v?.videoId && !byId.has(v.videoId)) byId.set(v.videoId, v);
    }
    const videos = [...byId.values()];
    if (!videos.length) return json(404, { error: "empty corpus" });

    // Which videos are already cited by some claim?
    const cited = new Set();
    for (const c of current.claims) {
      for (const s of c.sources || []) cited.add(s.videoId);
      for (const camp of c.camps || []) for (const s of camp.sources || []) cited.add(s.videoId);
    }
    const uncited = videos.filter((v) => !cited.has(v.videoId));
    if (!uncited.length) {
      return json(200, { status: "consolidated", topic: topicId, claims: current, persisted: false, unchanged: true });
    }

    const compactClaims = current.claims.map((c) => ({
      id: c.id, type: c.type, statement: c.statement,
      camps: (c.camps || []).map((cp, i) => ({ camp_index: i, position: cp.position })),
    }));

    const client = new Anthropic();
    const response = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 1500,
      output_config: { effort: "low", format: { type: "json_schema", schema: SCHEMA } },
      system: SYSTEM,
      messages: [{
        role: "user",
        content: JSON.stringify({
          current_claims: compactClaims,
          uncited_videos: uncited.map((v) => ({
            videoId: v.videoId, title: v.title, channel: v.channel,
            verdict: v.verdict, note: v.verdict_note,
          })),
        }),
      }],
    });
    if (response.stop_reason === "refusal") {
      return json(200, { status: "error", error: "consolidation_declined" });
    }
    const delta = JSON.parse(response.content.find((b) => b.type === "text")?.text);

    // Merge the delta
    let changed = false;
    for (const add of delta.additions || []) {
      const c = current.claims.find((x) => x.id === add.claim_id);
      if (!c) continue;
      const target = c.type === "contested"
        ? c.camps?.[add.camp_index ?? -1]?.sources
        : (c.sources = c.sources || []);
      if (!target) continue;
      for (const s of add.sources || []) {
        if (!target.some((t) => t.videoId === s.videoId)) { target.push(s); changed = true; }
      }
    }
    for (const nc of delta.new_claims || []) {
      if (!current.claims.some((x) => x.id === nc.id)) { current.claims.push(nc); changed = true; }
    }
    const fp = (delta.fingerprints || []).slice(0, 3);
    if (fp.length && JSON.stringify(fp) !== JSON.stringify(current.fingerprints || [])) {
      current.fingerprints = fp;
      changed = true;
    }

    const claims = {
      note: "Consolidated claims: what the corpus consistently talks about. Sources are the analyzed videos that carry each claim. Updated on narrative refresh.",
      updated: new Date().toISOString().slice(0, 10),
      ...(current.fingerprints ? { fingerprints: current.fingerprints } : {}),
      claims: current.claims,
    };

    let persisted = false;
    if (changed) {
      const path = `corpus/${topicId}/claims.json`;
      const cur = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
        headers: ghHeaders(),
      });
      const sha = cur.ok ? (await cur.json()).sha : undefined;
      const put = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
        method: "PUT",
        headers: ghHeaders(),
        body: JSON.stringify({
          message: `Engine: consolidate claims for ${topicId} (+${(delta.additions || []).length} additions, +${(delta.new_claims || []).length} new) [skip netlify]`,
          content: Buffer.from(JSON.stringify(claims, null, 2)).toString("base64"),
          ...(sha ? { sha } : {}),
        }),
      });
      persisted = put.ok;
    }

    return json(200, { status: "consolidated", topic: topicId, claims, persisted, unchanged: !changed });
  } catch (e) {
    return json(500, { status: "error", error: String(e.message || e).slice(0, 300) });
  }
};
