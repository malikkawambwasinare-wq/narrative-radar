// Narrative Radar — on-demand analysis engine.
// POST /api/analyze {url} →
//   tracked   : video already in the corpus (no model call)
//   analyzed  : Claude classified it against the tracked narratives and the
//               result was committed back to the GitHub repo (the site's data)
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

const ANALYSIS_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: [
    "decision", "topic_id", "verdict", "verdict_note", "advice",
    "is_update", "update_note", "new_narrative_name", "new_narrative_claim",
    "confidence",
  ],
  properties: {
    decision: { type: "string", enum: ["existing_narrative", "new_narrative", "unrelated"] },
    topic_id: { type: ["string", "null"] },
    verdict: { type: "string", enum: ["ORIGINAL", "DERIVATIVE", "RECYCLED", "CLICKBAIT", "UNKNOWN"] },
    verdict_note: { type: "string" },
    advice: { type: "string" },
    is_update: { type: "boolean" },
    update_note: { type: ["string", "null"] },
    new_narrative_name: { type: ["string", "null"] },
    new_narrative_claim: { type: ["string", "null"] },
    confidence: { type: "string", enum: ["low", "medium", "high"] },
  },
};

const SYSTEM = `You are the analysis engine for Narrative Radar, a tool that helps people escape YouTube rabbit holes. Given a video's metadata and the narratives the radar already tracks, decide:

1. decision — does this video belong to an existing tracked narrative ("existing_narrative", set topic_id), found a genuinely new narrative worth tracking ("new_narrative", propose new_narrative_name and new_narrative_claim), or is it unrelated to narrative-tracking entirely ("unrelated" — e.g. music, entertainment, tutorials)?
2. verdict — from metadata alone (title, channel, dates, view counts, comparison with corpus videos): ORIGINAL (likely primary content/new claims), DERIVATIVE (commentary on known claims), RECYCLED (repackaging existing content — e.g. same runtime as a known interview, re-cut channels, AI-narrated rehash), CLICKBAIT (title promises what content likely doesn't deliver), or UNKNOWN if metadata is insufficient. Be honest about uncertainty — this is metadata-only analysis, without the transcript.
3. advice — one sentence telling the user what to do with their time (watch it / skip it / the narrative summary may suffice), grounded in the verdict.
4. is_update — if part of an existing narrative, does the title/metadata suggest NEW claims or a NEW mechanism for that narrative (an update), or more of the same? Set update_note accordingly.

Never invent facts you don't have. Judge from the actual metadata and corpus patterns. Keep verdict_note ≤ 30 words, advice ≤ 25 words.`;

async function fetchVideoMeta(videoId) {
  const oembed = await fetch(
    `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`,
  );
  if (!oembed.ok) return null;
  const o = await oembed.json();
  return { videoId, title: o.title, channel: o.author_name };
}

function summarizeCorpus(topics) {
  return topics.map((t) => ({
    topic_id: t.id,
    status: t.status,
    narrative: t.narrative
      ? {
          name: t.narrative.name,
          claim: t.narrative.claim,
          born: t.narrative.born,
          mutations: (t.narrative.mutations || []).map((m) => m.mechanism),
        }
      : null,
    sample_videos: (t.videos || []).slice(0, 12).map((v) => ({
      title: v.title, channel: v.channel, verdict: v.verdict, length: v.length,
    })),
  }));
}

async function persistToGitHub(topicId, entry, isInbox) {
  const token = process.env.GH_TOKEN;
  if (!token) return false;
  const path = isInbox ? "corpus/inbox.json" : `corpus/${topicId}/videos.json`;
  const api = `https://api.github.com/repos/${REPO}/contents/${path}`;
  const headers = {
    Authorization: `Bearer ${token}`,
    Accept: "application/vnd.github+json",
    "User-Agent": "narrative-radar-engine",
  };
  const cur = await fetch(api, { headers });
  let sha, data;
  if (cur.ok) {
    const f = await cur.json();
    sha = f.sha;
    data = JSON.parse(Buffer.from(f.content, "base64").toString("utf-8"));
  } else if (isInbox) {
    data = [];
  } else {
    return false;
  }
  if (isInbox) {
    if (data.some((v) => v.videoId === entry.videoId)) return true;
    data.push(entry);
  } else {
    if (data.videos.some((v) => v.videoId === entry.videoId)) return true;
    data.videos.push(entry);
  }
  const put = await fetch(api, {
    method: "PUT",
    headers,
    body: JSON.stringify({
      message: `Engine: analyze ${entry.videoId} (${entry.verdict || "inbox"})`,
      content: Buffer.from(JSON.stringify(data, null, 2)).toString("base64"),
      ...(sha ? { sha } : {}),
    }),
  });
  return put.ok;
}

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "POST") return json(405, { error: "POST only" });

  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const videoId = parseVideoId(body.url);
  if (!videoId) return json(400, { error: "not_a_youtube_link" });

  try {
    // Load the corpus straight from the repo (the same data the site shows)
    const watchlist = await getJSON(`${RAW}/watchlist.json`);
    const topics = await Promise.all(
      watchlist.topics.map(async (t) => ({
        id: t.id,
        status: t.status,
        narrative: await getJSON(`${RAW}/corpus/${t.id}/narrative.json`).catch(() => null),
        videos: await getJSON(`${RAW}/corpus/${t.id}/videos.json`)
          .then((d) => d.videos).catch(() => []),
      })),
    );

    // Already tracked → instant answer, no model call
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
    const text = response.content.find((b) => b.type === "text")?.text;
    const analysis = JSON.parse(text);

    // Persist: existing narrative → straight into that corpus;
    // new/unrelated → inbox for review
    let persisted = false;
    const today = new Date().toISOString().slice(0, 10);
    if (analysis.decision === "existing_narrative" && analysis.topic_id) {
      persisted = await persistToGitHub(analysis.topic_id, {
        videoId, url: `https://www.youtube.com/watch?v=${videoId}`,
        title: meta.title, channel: meta.channel,
        published: "", views: "", length: "",
        query: "user-submitted", age_days: null, first_seen: today,
        transcript: null,
        verdict: analysis.verdict === "UNKNOWN" ? "UNREVIEWED" : analysis.verdict,
        verdict_note: `[live analysis, metadata-only] ${analysis.verdict_note}`,
      }, false);
    } else if (analysis.decision === "new_narrative") {
      persisted = await persistToGitHub(null, {
        videoId, title: meta.title, channel: meta.channel, first_seen: today,
        proposed_narrative: analysis.new_narrative_name,
        proposed_claim: analysis.new_narrative_claim,
        verdict: analysis.verdict, note: analysis.verdict_note,
      }, true);
    }

    const narrative = analysis.topic_id
      ? topics.find((t) => t.id === analysis.topic_id)?.narrative
      : null;
    return json(200, {
      status: "analyzed", video: meta, analysis, persisted,
      narrative: narrative && {
        name: narrative.name, claim: narrative.claim,
        born: narrative.born, mutations: (narrative.mutations || []).length,
      },
    });
  } catch (e) {
    return json(500, { status: "error", error: String(e.message || e).slice(0, 300) });
  }
};
