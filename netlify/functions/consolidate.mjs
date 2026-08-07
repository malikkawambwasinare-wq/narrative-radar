// Narrative Radar — refresh step 3: re-consolidate a narrative's core claims
// from its (newly grown) corpus, and commit claims.json back to the repo.
// POST /api/consolidate {topic} → {claims: {...}, persisted}
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

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["claims"],
  properties: {
    claims: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["id", "type", "statement", "note", "camps", "sources"],
        properties: {
          id: { type: "string" },
          type: { type: "string", enum: ["consensus", "contested"] },
          statement: { type: "string" },
          note: { type: "string" },
          camps: {
            type: ["array", "null"],
            items: {
              type: "object",
              additionalProperties: false,
              required: ["position", "sources"],
              properties: {
                position: { type: "string" },
                sources: { type: "array", items: {
                  type: "object", additionalProperties: false,
                  required: ["videoId", "predictor"],
                  properties: { videoId: { type: "string" }, predictor: { type: "string" } },
                } },
              },
            },
          },
          sources: {
            type: ["array", "null"],
            items: {
              type: "object", additionalProperties: false,
              required: ["videoId", "predictor"],
              properties: { videoId: { type: "string" }, predictor: { type: "string" } },
            },
          },
        },
      },
    },
  },
};

const SYSTEM = `You maintain the consolidated claims of a tracked narrative for Narrative Radar. Input: the current consolidated claims, the full video corpus (titles, channels, verdicts, analyst notes), and raw extracted claims where available.

Update the consolidated claims to reflect the corpus:
- A claim belongs here only if it is CONSISTENTLY present across multiple videos (or is a clearly contested question with identifiable camps).
- Preserve existing claim ids and statements unless the corpus genuinely changed them; ADD new sources to existing claims when new videos carry them; add a NEW claim only when several videos support it.
- "consensus" claims use the sources array (camps: null). "contested" claims use camps (sources: null), each camp with its position and sources.
- Every source must be a real videoId from the corpus with the predictor who carries the claim in that video.
- Keep statements ≤ 30 words, notes ≤ 35 words. Notes should say what makes the claim trackable (clocks, falsifiers, incentives).
- Never invent sources or claims not grounded in the given corpus data.`;

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
    const [videos, current, extracted] = await Promise.all([
      fetch(`${RAW}/corpus/${topicId}/videos.json`).then((r) => r.json())
        .then((d) => d.videos),
      fetch(`${RAW}/corpus/${topicId}/claims.json`).then((r) => r.json())
        .catch(() => ({ claims: [] })),
      fetch(`${RAW}/corpus/${topicId}/claims-extracted.json`).then((r) => r.json())
        .catch(() => []),
    ]);

    const client = new Anthropic();
    const response = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 4000,
      output_config: { effort: "low", format: { type: "json_schema", schema: SCHEMA } },
      system: SYSTEM,
      messages: [{
        role: "user",
        content: JSON.stringify({
          current_consolidated_claims: current.claims,
          corpus: videos.map((v) => ({
            videoId: v.videoId, title: v.title, channel: v.channel,
            verdict: v.verdict, note: v.verdict_note,
          })),
          raw_extracted_claims: extracted,
        }),
      }],
    });
    if (response.stop_reason === "refusal") {
      return json(200, { status: "error", error: "consolidation_declined" });
    }
    const out = JSON.parse(response.content.find((b) => b.type === "text")?.text);
    const claims = {
      note: "Consolidated claims: what the corpus consistently talks about. Sources are the analyzed videos that carry each claim. Updated on narrative refresh.",
      updated: new Date().toISOString().slice(0, 10),
      claims: out.claims,
    };

    // Commit back (read for sha, then write)
    let persisted = false;
    const path = `corpus/${topicId}/claims.json`;
    const cur = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
      headers: ghHeaders(),
    });
    const sha = cur.ok ? (await cur.json()).sha : undefined;
    const put = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
      method: "PUT",
      headers: ghHeaders(),
      body: JSON.stringify({
        message: `Engine: re-consolidate claims for ${topicId} (${out.claims.length} claims)`,
        content: Buffer.from(JSON.stringify(claims, null, 2)).toString("base64"),
        ...(sha ? { sha } : {}),
      }),
    });
    persisted = put.ok;

    return json(200, { status: "consolidated", topic: topicId, claims, persisted });
  } catch (e) {
    return json(500, { status: "error", error: String(e.message || e).slice(0, 300) });
  }
};
