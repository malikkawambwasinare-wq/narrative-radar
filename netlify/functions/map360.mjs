// Narrative Radar — the 360 map: the question a narrative competes to answer,
// and the rival/adjacent answers around it.
// POST /api/map360 {topic, force?}          → mint (or return cached) relations.json
// POST /api/map360 {found_shadow, source_topic} → found a tracked tile from a shadow node
// One Claude call per mint (~$0.05-0.10), cached forever like trace-origin.
// Integrity gates baked in: evidence videoIds must come from this corpus;
// supplements targets are product CATEGORIES, never named sellers or people.
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

const ghHeaders = () => ({
  Authorization: `Bearer ${process.env.GH_TOKEN}`,
  Accept: "application/vnd.github+json",
  "User-Agent": "narrative-radar-engine",
});
async function ghRead(path) {
  const r = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
    headers: ghHeaders(),
  });
  if (!r.ok) return null;
  const f = await r.json();
  return { sha: f.sha, data: JSON.parse(Buffer.from(f.content, "base64").toString("utf-8")) };
}
async function ghWrite(path, data, message, sha) {
  const r = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
    method: "PUT",
    headers: ghHeaders(),
    body: JSON.stringify({
      message: `${message} [skip netlify]`,
      content: Buffer.from(JSON.stringify(data, null, 2)).toString("base64"),
      ...(sha ? { sha } : {}),
    }),
  });
  return r.ok;
}

const REL_TYPES = ["competes", "competes_mechanism", "supplements", "feeds",
  "counters", "mutates_into", "shares_clock"];

const MAP_SCHEMA = {
  type: "object", additionalProperties: false,
  required: ["question", "relations"],
  properties: {
    question: {
      type: "object", additionalProperties: false,
      required: ["text", "demand", "asked_since"],
      properties: {
        text: { type: "string" }, demand: { type: "string" },
        asked_since: { type: "string" },
      },
    },
    relations: {
      type: "array", maxItems: 10,
      items: {
        type: "object", additionalProperties: false,
        required: ["type", "direction", "target_topic_id", "shadow", "label", "clock", "evidence", "confidence"],
        properties: {
          type: { type: "string", enum: REL_TYPES },
          direction: { type: ["string", "null"], enum: ["out", "in", null] },
          target_topic_id: { type: ["string", "null"] },
          shadow: {
            type: ["object", "null"], additionalProperties: false,
            required: ["shadow_id", "name", "claim_hint", "queries"],
            properties: {
              shadow_id: { type: "string" }, name: { type: "string" },
              claim_hint: { type: "string" },
              queries: { type: "array", items: { type: "string" } },
            },
          },
          label: { type: "string" },
          clock: {
            type: ["object", "null"], additionalProperties: false,
            required: ["trigger", "next_check"],
            properties: { trigger: { type: "string" }, next_check: { type: "string" } },
          },
          evidence: {
            type: "object", additionalProperties: false,
            required: ["videoIds", "note"],
            properties: {
              videoIds: { type: "array", items: { type: "string" } },
              note: { type: "string" },
            },
          },
          confidence: { type: "string", enum: ["low", "medium", "high"] },
        },
      },
    },
  },
};

const SYSTEM = `You build the 360 map for Narrative Radar. Core idea: a narrative is one ANSWER competing for a QUESTION — the question is the durable object (the demand behind it); answers rotate. Given one narrative (with its consolidated claims), a digest of all tracked narratives, and a list of researched candidates, state the question this narrative answers, then map the other answers.

Relation types:
- competes: a rival ANSWER — believing it weakens belief in this one (crash-imminent vs generational-buying-opportunity).
- competes_mechanism: a co-traveling variant — same conclusion, rival engine, often shared preachers. Do NOT present these as genuine alternatives; they stack.
- supplements: rides/extends the answer — the product layer sold on its back. TARGETS MUST BE PRODUCT CATEGORIES ("hard-asset hedge products"), NEVER named sellers, brands, or individuals.
- feeds: an upstream meta-narrative answering a broader question that raises this one's prior (direction "in"), or this narrative feeding a more specific one (direction "out").
- counters: the anti-narrative — its thesis is the explicit negation of this one.
- mutates_into: historical succession for the same demand — only when the source has demonstrably declined AND there is an inheritance signal; otherwise use competes.
- shares_clock: both narratives hinge on the SAME falsifiable event predicate (not merely the same year). Fill the clock object with the trigger verbatim.

Rules:
- Prefer target_topic_id from the tracked list; prefer candidate ids for shadows; exactly one of target_topic_id / shadow is non-null per relation.
- evidence.videoIds must come from THIS narrative's corpus (given in the claims' sources) — never invent. Empty videoIds is allowed only when evidence.note explicitly says "model estimate, pending audit".
- clock is required for shares_clock and must be null otherwise.
- 4-8 relations. Quality over coverage. Never self-reference.`;

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "POST") return json(405, { error: "POST only" });
  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }

  try {
    /* ---------- branch 2: found a tile from a shadow node ---------- */
    if (body.found_shadow) {
      const s = body.found_shadow;
      if (!s.shadow_id || !s.name) return json(400, { error: "bad shadow" });
      const today = new Date().toISOString().slice(0, 10);
      // richer candidate data wins over the stub if available
      const cands = await fetch(`${RAW}/candidates.json`).then(r => r.json()).catch(() => null);
      const cand = cands?.candidates?.find(c => c.id === s.shadow_id);
      const name = cand?.name || s.name;
      const claim = cand?.claim_hint || s.claim_hint || "";
      const queries = (cand?.queries?.length ? cand.queries : s.queries) || [];
      const wl = await ghRead("watchlist.json");
      if (!wl) return json(500, { status: "error", error: "watchlist unavailable" });
      if (wl.data.topics.some(t => t.id === s.shadow_id)) {
        return json(200, { status: "exists", topic: s.shadow_id });
      }
      const topicRecord = {
        id: s.shadow_id, name, industry: cand?.beat || "Unsorted",
        status: "active", started: today,
        trigger: `Founded from the 360 map of ${body.source_topic || "a narrative"}`,
        queries, watched_predictors: [], notes: claim,
      };
      wl.data.topics.push(topicRecord);
      const ok1 = await ghWrite("watchlist.json", wl.data,
        `Engine: found ${s.shadow_id} from 360 map of ${body.source_topic || "?"}`, wl.sha);
      const ok2 = await ghWrite(`corpus/${s.shadow_id}/narrative.json`, {
        name, claim, predictor: "to be determined",
        born: today.slice(0, 7),
        born_note: "Founded from 360 map (born date pending audit)",
        mutations: [],
        origin: { type: "map360", source_topic: body.source_topic || null, created: today },
      }, `Engine: narrative.json for ${s.shadow_id}`);
      return json(200, { status: "founded", topic: topicRecord, persisted: ok1 && ok2 });
    }

    /* ---------- branch 1: mint (or return) the 360 map ---------- */
    const topic = body.topic;
    if (!topic) return json(400, { error: "topic required" });

    if (!body.force) {
      const existing = await fetch(`${RAW}/corpus/${topic}/relations.json`)
        .then(r => r.ok ? r.json() : null).catch(() => null);
      if (existing?.relations) {
        return json(200, { status: "already_mapped", topic, map: existing, persisted: true });
      }
    }

    const [narrative, claims, watchlist, cands] = await Promise.all([
      fetch(`${RAW}/corpus/${topic}/narrative.json`).then(r => r.json()),
      fetch(`${RAW}/corpus/${topic}/claims.json`).then(r => r.ok ? r.json() : null).catch(() => null),
      fetch(`${RAW}/watchlist.json`).then(r => r.json()),
      fetch(`${RAW}/candidates.json`).then(r => r.ok ? r.json() : null).catch(() => null),
    ]);

    const trackedIds = watchlist.topics.map(t => t.id);
    const digest = watchlist.topics.map(t =>
      `${t.id}: ${t.name}${t.notes ? ` — ${String(t.notes).slice(0, 120)}` : ""}`).join("\n");
    const candDigest = (cands?.candidates || []).map(c =>
      `${c.id}: ${c.name} — ${c.claim_hint.slice(0, 110)}`).join("\n");
    const compactClaims = (claims?.claims || []).map(c => ({
      id: c.id, type: c.type, statement: c.statement,
      camps: (c.camps || []).map(cp => cp.position),
      sourceVideoIds: [...(c.sources || []), ...(c.camps || []).flatMap(cp => cp.sources || [])]
        .map(x => x.videoId).slice(0, 12),
    }));

    const client = new Anthropic();
    const response = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 2500,
      output_config: { effort: "low", format: { type: "json_schema", schema: MAP_SCHEMA } },
      system: SYSTEM,
      messages: [{
        role: "user",
        content: JSON.stringify({
          this_narrative: { id: topic, name: narrative.name, claim: narrative.claim,
            born: narrative.born, mutations: narrative.mutations },
          consolidated_claims: compactClaims,
          tracked_narratives: digest,
          researched_candidates: candDigest,
        }),
      }],
    });
    if (response.stop_reason === "refusal") {
      return json(200, { status: "error", error: "map_declined" });
    }
    const out = JSON.parse(response.content.find(b => b.type === "text")?.text);

    // server-side validation
    const relations = (out.relations || []).filter(r => REL_TYPES.includes(r.type)).map(r => {
      const rel = { type: r.type, label: r.label, confidence: r.confidence,
        evidence: { videoIds: (r.evidence?.videoIds || []).slice(0, 6),
          note: r.evidence?.note || "" } };
      if (r.direction && (r.type === "feeds" || r.type === "mutates_into")) rel.direction = r.direction;
      if (r.type === "shares_clock" && r.clock?.trigger) rel.clock = r.clock;
      let tid = r.target_topic_id, sh = r.shadow;
      if (tid && !trackedIds.includes(tid)) { sh = sh || { shadow_id: tid, name: r.label, claim_hint: "", queries: [] }; tid = null; }
      if (sh && trackedIds.includes(sh.shadow_id)) { tid = sh.shadow_id; sh = null; }
      if (tid === topic || sh?.shadow_id === topic) return null;
      rel.target = tid
        ? { kind: "tracked", topic_id: tid }
        : sh ? { kind: "shadow", shadow_id: sh.shadow_id, name: sh.name,
            claim_hint: sh.claim_hint || "", queries: (sh.queries || []).slice(0, 6) }
          : null;
      return rel.target ? rel : null;
    }).filter(Boolean);

    const map = {
      note: "The 360 map: the question this narrative competes to answer, and the rival/adjacent answers. Shadows are untracked candidate tiles.",
      updated: new Date().toISOString().slice(0, 10),
      minted_by: "map360",
      question: out.question,
      relations,
    };
    const cur = await ghRead(`corpus/${topic}/relations.json`);
    const persisted = await ghWrite(`corpus/${topic}/relations.json`, map,
      `Engine: 360 map for ${topic} (${relations.length} relations, ${relations.filter(r => r.target.kind === "shadow").length} shadows)`,
      cur?.sha);
    return json(200, { status: "mapped", topic, map, persisted });
  } catch (e) {
    return json(500, { status: "error", error: String(e.message || e).slice(0, 300) });
  }
};
