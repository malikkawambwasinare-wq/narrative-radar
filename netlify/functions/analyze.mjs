// Narrative Radar — on-demand analysis engine.
// POST /api/analyze {url} →
//   tracked  : video already in a narrative's corpus (no model call)
//   analyzed : Claude extracted the video's narrative —
//              existing narrative → video committed into its corpus
//              new narrative     → narrative CREATED (watchlist + narrative.json
//                                  + videos.json) and returned so the UI can add
//                                  the tile to the ribbon immediately
//              unrelated         → nothing persisted (music/entertainment/how-to)
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
    status,
    headers: { "Content-Type": "application/json", ...CORS },
  });

function parseVideoId(s) {
  s = (s || "").trim();
  const m = s.match(
    /(?:youtube\.com\/(?:watch\?(?:.*&)?v=|shorts\/|embed\/|live\/)|youtu\.be\/)([\w-]{11})/,
  );
  if (m) return m[1];
  if (/^[\w-]{11}$/.test(s) && /[\d_-]/.test(s)) return s;
  return null;
}

async function getJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url} → ${r.status}`);
  return r.json();
}

/* ---------- GitHub persistence ---------- */
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
      message,
      content: Buffer.from(JSON.stringify(data, null, 2)).toString("base64"),
      ...(sha ? { sha } : {}),
    }),
  });
  return r.ok;
}

/* ---------- Claude analysis ---------- */
const ANALYSIS_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: [
    "decision", "topic_id", "verdict", "verdict_note", "advice",
    "is_update", "update_note", "confidence",
    "new_narrative_id", "new_narrative_name", "new_narrative_claim",
    "new_narrative_born", "new_narrative_born_note", "new_narrative_queries",
  ],
  properties: {
    decision: { type: "string", enum: ["existing_narrative", "new_narrative", "unrelated"] },
    topic_id: { type: ["string", "null"] },
    verdict: { type: "string", enum: ["ORIGINAL", "DERIVATIVE", "RECYCLED", "CLICKBAIT", "UNKNOWN"] },
    verdict_note: { type: "string" },
    advice: { type: "string" },
    is_update: { type: "boolean" },
    update_note: { type: ["string", "null"] },
    confidence: { type: "string", enum: ["low", "medium", "high"] },
    new_narrative_id: { type: ["string", "null"] },
    new_narrative_name: { type: ["string", "null"] },
    new_narrative_claim: { type: ["string", "null"] },
    new_narrative_born: { type: ["string", "null"] },
    new_narrative_born_note: { type: ["string", "null"] },
    new_narrative_queries: { type: "array", items: { type: "string" } },
  },
};

const SYSTEM = `You are the analysis engine for Narrative Radar, a tool that extracts the NARRATIVE behind a YouTube video — the bigger picture the video belongs to — so people escape the rabbit hole. Given a video's metadata and the narratives already tracked, decide:

1. decision:
   - "existing_narrative" — the video's story fits a tracked narrative (set topic_id). Only choose this on a genuine fit of the narrative's core claim, not surface keyword overlap.
   - "new_narrative" — the video carries a real narrative (a recurring claim/story pundits and creators push) that isn't tracked yet. The radar will CREATE this narrative immediately, so define it well:
     * new_narrative_id: short-kebab-slug (e.g. "crypto-winter-watch") — must not equal any existing topic_id
     * new_narrative_name: short evocative title
     * new_narrative_claim: the narrative's core claim in 1-2 sentences
     * new_narrative_born: your best estimate of when this narrative FIRST appeared in public discourse (YYYY or YYYY-MM; e.g. "crypto winter" dates to ~2018) — null if you genuinely can't estimate
     * new_narrative_born_note: one line stating the basis of the estimate; this is a model estimate pending audit
     * new_narrative_queries: 4-6 YouTube search queries for collecting this narrative's video corpus
   - "unrelated" — reserved for content with no narrative to track: music, entertainment, gaming, tutorials. Claims-driven commentary about markets/politics/tech/society almost always carries a narrative.
2. verdict — from metadata alone: ORIGINAL / DERIVATIVE / RECYCLED / CLICKBAIT / UNKNOWN. Be honest about uncertainty; this is metadata-only, no transcript.
3. advice — one sentence on what to do with their time, grounded in the verdict.
4. is_update — for existing narratives: does the metadata suggest NEW claims or a NEW mechanism (an update to the narrative)? Set update_note.

Never invent facts. verdict_note ≤ 30 words, advice ≤ 25 words.`;

async function fetchVideoMeta(videoId) {
  const r = await fetch(
    `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`,
  );
  if (!r.ok) return null;
  const o = await r.json();
  return { videoId, title: o.title, channel: o.author_name };
}

const summarizeCorpus = (topics) =>
  topics.map((t) => ({
    topic_id: t.id,
    status: t.status,
    narrative: t.narrative && {
      name: t.narrative.name,
      claim: t.narrative.claim,
      born: t.narrative.born,
      mutations: (t.narrative.mutations || []).map((m) => m.mechanism),
    },
    sample_videos: (t.videos || []).slice(0, 12).map((v) => ({
      title: v.title, channel: v.channel, verdict: v.verdict, length: v.length,
    })),
  }));

const videoEntry = (videoId, meta, verdict, note, today) => ({
  videoId, url: `https://www.youtube.com/watch?v=${videoId}`,
  title: meta.title, channel: meta.channel,
  published: "", views: "", length: "",
  query: "user-submitted", age_days: null, first_seen: today,
  transcript: null,
  verdict: verdict === "UNKNOWN" ? "UNREVIEWED" : verdict,
  verdict_note: `[live analysis, metadata-only] ${note}`,
});

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "POST") return json(405, { error: "POST only" });

  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const videoId = parseVideoId(body.url);
  if (!videoId) return json(400, { error: "not_a_youtube_link" });

  try {
    const watchlist = await getJSON(`${RAW}/watchlist.json`);
    const topics = await Promise.all(
      watchlist.topics.map(async (t) => ({
        id: t.id,
        status: t.status,
        name: t.name,
        narrative: await getJSON(`${RAW}/corpus/${t.id}/narrative.json`).catch(() => null),
        videos: await getJSON(`${RAW}/corpus/${t.id}/videos.json`)
          .then((d) => d.videos).catch(() => []),
      })),
    );

    // Already tracked → instant answer
    for (const t of topics) {
      const v = (t.videos || []).find((x) => x.videoId === videoId);
      if (v) {
        return json(200, {
          status: "tracked", topic_id: t.id, video: v,
          narrative: t.narrative && {
            name: t.narrative.name, claim: t.narrative.claim,
            born: t.narrative.born, mutations: (t.narrative.mutations || []).length,
          },
        });
      }
    }

    const meta = await fetchVideoMeta(videoId);
    if (!meta) return json(404, { error: "video_not_found" });

    const client = new Anthropic();
    const response = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 2000,
      output_config: { effort: "low", format: { type: "json_schema", schema: ANALYSIS_SCHEMA } },
      system: SYSTEM,
      messages: [{
        role: "user",
        content: JSON.stringify({
          video_to_analyze: meta,
          tracked_narratives: summarizeCorpus(topics),
        }),
      }],
    });
    if (response.stop_reason === "refusal") {
      return json(200, { status: "error", error: "analysis_declined" });
    }
    const analysis = JSON.parse(response.content.find((b) => b.type === "text")?.text);
    const today = new Date().toISOString().slice(0, 10);

    // Slug collision safety: a "new" narrative matching an existing id is existing
    if (analysis.decision === "new_narrative" &&
        watchlist.topics.some((t) => t.id === analysis.new_narrative_id)) {
      analysis.decision = "existing_narrative";
      analysis.topic_id = analysis.new_narrative_id;
    }

    if (analysis.decision === "existing_narrative" && analysis.topic_id) {
      const entry = videoEntry(videoId, meta, analysis.verdict, analysis.verdict_note, today);
      let persisted = false;
      const cur = await ghRead(`corpus/${analysis.topic_id}/videos.json`);
      if (cur && !cur.data.videos.some((v) => v.videoId === videoId)) {
        cur.data.videos.push(entry);
        persisted = await ghWrite(
          `corpus/${analysis.topic_id}/videos.json`, cur.data,
          `Engine: add ${videoId} to ${analysis.topic_id} (${entry.verdict})`, cur.sha,
        );
      }
      const n = topics.find((t) => t.id === analysis.topic_id)?.narrative;
      return json(200, {
        status: "analyzed", video: meta, analysis, persisted, video_entry: entry,
        narrative: n && {
          name: n.name, claim: n.claim, born: n.born,
          mutations: (n.mutations || []).length,
        },
      });
    }

    if (analysis.decision === "new_narrative" && analysis.new_narrative_id) {
      const id = analysis.new_narrative_id;
      const entry = videoEntry(videoId, meta, analysis.verdict, analysis.verdict_note, today);
      const narrative = {
        name: analysis.new_narrative_name,
        claim: analysis.new_narrative_claim,
        predictor: "to be determined",
        born: analysis.new_narrative_born || today.slice(0, 7),
        born_note: `${analysis.new_narrative_born_note || "Engine estimate"} (model estimate, pending audit)`,
        mutations: [],
        origin: { type: "engine", first_video: videoId, created: today },
      };
      const topicRecord = {
        id, name: analysis.new_narrative_name, status: "active", started: today,
        trigger: `User-submitted video: ${meta.title} (${meta.channel})`,
        queries: analysis.new_narrative_queries || [],
        watched_predictors: [],
        notes: `Created by the analysis engine. ${analysis.new_narrative_claim}`,
      };
      // watchlist first (read-modify-write), then the two new files in parallel
      let persisted = false;
      const wl = await ghRead("watchlist.json");
      if (wl && !wl.data.topics.some((t) => t.id === id)) {
        wl.data.topics.push(topicRecord);
        const ok1 = await ghWrite("watchlist.json", wl.data,
          `Engine: new narrative "${analysis.new_narrative_name}" (${id})`, wl.sha);
        const [ok2, ok3] = await Promise.all([
          ghWrite(`corpus/${id}/narrative.json`, narrative,
            `Engine: narrative.json for ${id}`),
          ghWrite(`corpus/${id}/videos.json`, { videos: [entry] },
            `Engine: first video for ${id} (${entry.verdict})`),
        ]);
        persisted = ok1 && ok2 && ok3;
      }
      return json(200, {
        status: "analyzed", video: meta, analysis, persisted,
        created_topic: topicRecord, narrative, video_entry: entry,
      });
    }

    // unrelated
    return json(200, { status: "analyzed", video: meta, analysis, persisted: false });
  } catch (e) {
    return json(500, { status: "error", error: String(e.message || e).slice(0, 300) });
  }
};
