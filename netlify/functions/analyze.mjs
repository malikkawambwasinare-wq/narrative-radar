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
import { guard } from "./_guard.mjs";
import { enrichVideo } from "./_youtube.mjs";

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
      message: `${message} [skip netlify]`,
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
  // `advice` and `new_narrative_id` are deliberately absent: the client already
  // derives advice deterministically from the verdict (ADVICE map in
  // index.html), and the server slugifies the id from the name. Asking the
  // model for either buys nothing and bills at the output rate.
  required: [
    "decision", "topic_id", "verdict", "verdict_note",
    "is_update", "update_note", "confidence",
    "new_narrative_name", "new_narrative_claim_name", "new_narrative_claim",
    "new_narrative_born", "new_narrative_born_note", "new_narrative_queries",
    "new_narrative_industry", "new_narrative_camps",
    "explanation_layman", "explanation_intermediate", "explanation_expert",
  ],
  properties: {
    decision: { type: "string", enum: ["existing_narrative", "new_narrative", "unrelated"] },
    topic_id: { type: ["string", "null"] },
    verdict: { type: "string", enum: ["ORIGINAL", "DERIVATIVE", "RECYCLED", "CLICKBAIT", "UNKNOWN"] },
    verdict_note: { type: "string" },
    is_update: { type: "boolean" },
    update_note: { type: ["string", "null"] },
    confidence: { type: "string", enum: ["low", "medium", "high"] },
    new_narrative_name: { type: ["string", "null"] },
    new_narrative_claim_name: { type: ["string", "null"] },
    new_narrative_claim: { type: ["string", "null"] },
    new_narrative_born: { type: ["string", "null"] },
    new_narrative_born_note: { type: ["string", "null"] },
    new_narrative_queries: { type: "array", items: { type: "string" } },
    // A nullable enum must be spelled as anyOf — the API's structured-output
    // validator rejects `type: ["string","null"]` next to string enum values,
    // which silently broke every live paste until a real one was traced.
    new_narrative_industry: { anyOf: [
      { type: "string", enum: ["AI & technology", "Economy & markets", "Health & biotech", "Politics & geopolitics", "Energy & climate", "Fringe & unexplained", "Culture & society", "Entertainment & media", "Gaming", "Sports", "Internet & creator economy", "Unsorted"] },
      { type: "null" },
    ] },
    // The sides a viewer should hear before deciding, each with what to look out for.
    new_narrative_camps: { type: "array", items: {
      type: "object", additionalProperties: false, required: ["position", "watch_for"],
      properties: { position: { type: "string" }, watch_for: { type: "string" } },
    } },
    explanation_layman: { type: ["string", "null"] },
    explanation_intermediate: { type: ["string", "null"] },
    explanation_expert: { type: ["string", "null"] },
  },
};

const SYSTEM = `You are the analysis engine for Narrative Radar, a tool that extracts the NARRATIVE behind a YouTube video — the bigger picture the video belongs to — so people escape the rabbit hole. Given a video's metadata and the narratives already tracked, decide:

1. decision:
   - "existing_narrative" — the video's story fits a tracked narrative (set topic_id). Only choose this on a genuine fit of the narrative's core claim, not surface keyword overlap.
   - "new_narrative" — the video carries a real narrative (a recurring claim/story pundits and creators push) that isn't tracked yet. The radar will CREATE this narrative immediately, so define it well:
     * new_narrative_name: the title is the hook — write it to earn the click, honestly. Lead with the finding the page can back up, with its number or year where there is one, and keep the narrative's key search terms. Where there is no finding yet, name the competing explanation ("X or Y") — never a question, which plants the claim (e.g. "Housing Crash: Is It Always Next Year?", "The US Debt Collapse That's Been 'Imminent' Since 2015"). It must be something the narrative page can back up: state a pattern only if it is established, otherwise ask it as a question. Never use fear-plus-urgency wording (warning, collapse, crash alongside now, soon, about to), ALL CAPS or exclamation marks — the radar flags exactly those titles on other people's videos. ≤ 60 characters, no em dash (the radar derives the slug from it).
     * new_narrative_claim_name: the narrative's plain label, which ATTRIBUTES the claim and never asserts it: the claim in its believers' own words inside double quotes, then "story" (e.g. The "housing crash is coming next year" story). A believer should accept it as a fair statement of what they believe. Add no villain, out-group or moral words the narrative itself doesn't use.
     * new_narrative_claim: the narrative's core claim in 1-2 sentences
     * new_narrative_born: your best estimate of when this narrative FIRST appeared in public discourse (YYYY or YYYY-MM; e.g. "crypto winter" dates to ~2018) — null if you genuinely can't estimate
     * new_narrative_born_note: one line stating the basis of the estimate; this is a model estimate pending audit
     * new_narrative_queries: 4-6 YouTube search queries for collecting this narrative's video corpus
     * new_narrative_industry: the shelf this narrative belongs on — one of "AI & technology", "Economy & markets", "Health & biotech", "Politics & geopolitics", "Energy & climate", "Entertainment & media", "Gaming", "Sports", "Internet & creator economy", "Fringe & unexplained", "Culture & society", or "Unsorted" if none fit
     * new_narrative_camps: the 2-4 sides a viewer should hear before forming an opinion. Each: position (≤ 15 words, stated fairly, as its best advocates would) and watch_for (≤ 20 words: the tell a viewer should look out for in videos from that side — e.g. biomarker studies sold as cures, a product pitch, a moving deadline). Empty array for other decisions.
     * explanation_layman / explanation_intermediate / explanation_expert: three explanations of the narrative (each ≤ 75 words). Layman: plain everyday words, no jargon, why they should care. Intermediate: the mechanism and the main camps, named. Expert: audit framing — falsifiers, incentives, lifecycle stage. Null for other decisions.
     * TAILOR TO THE INDUSTRY. Economy & markets, Politics & geopolitics, Energy & climate, AI & technology, Gaming: these narratives make calls that resolve on a date — frame the expert explanation around clocks and deadlines. Health & biotech, Culture & society, Fringe & unexplained, Entertainment & media, Sports: claims are judged against EVIDENCE, not a calendar — never frame them as predictions or clocks; name what evidence would settle them (outcome trials vs biomarker or mechanism studies, anecdote, replication) and who profits from the claim.
   - "unrelated" — reserved ONLY for content carrying no recurring claim at all: music tracks themselves, let's-plays, vlogs, pure tutorials, highlight reels. Note that commentary ABOUT entertainment, gaming, sport or the creator economy usually DOES carry a narrative ("streaming is dying", "GTA 6 will slip again", "the games industry is collapsing", "AI is taking the charts") — those are tracked narratives, not unrelated content. Claims-driven commentary about markets/politics/tech/society/culture almost always carries a narrative.
2. verdict — from metadata alone: ORIGINAL / DERIVATIVE / RECYCLED / CLICKBAIT / UNKNOWN. Be honest about uncertainty; this is metadata-only, no transcript.
3. is_update — for existing narratives: does the metadata suggest NEW claims or a NEW mechanism (an update to the narrative)? Set update_note.

The tracked narratives you are shown are a SHORTLIST pre-selected by keyword overlap, not the whole shelf. If none genuinely fits, say so — prefer "new_narrative" or "unrelated" over forcing a poor match.

Never invent facts. verdict_note ≤ 30 words.`;

async function fetchVideoMeta(videoId) {
  const r = await fetch(
    `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`,
  );
  if (!r.ok) return null;
  const o = await r.json();
  return { videoId, title: o.title, channel: o.author_name };
}

/* ---------- candidate retrieval ----------
   Previously this function shipped a digest of EVERY tracked narrative on every
   call, and the handler fetched narrative.json + videos.json for every topic to
   build it. Both scaled with shelf size: ~2,300 tokens and 14 subrequests at 7
   narratives, ~18,000 tokens and 100+ subrequests at 50 — an O(N^2) spend curve
   and a hard wall at Cloudflare's 50-subrequest free-tier cap.

   Now a deterministic keyword score picks the few plausible topics from
   watchlist.json alone (one request, no model call), and only those get fetched
   and sent. Cost and subrequests are constant in shelf size.

   Tradeoff, stated plainly: the "already tracked" fast path now scans the
   shortlist rather than the whole shelf, so a video tracked under a topic that
   scores zero could be re-analyzed. In practice a tracked video was found BY
   that topic's own queries, so it scores highly; and the write path already
   refuses duplicates, so the worst case is one wasted call, never a bad write. */
const STOPWORDS = new Set(("the a an and or of for to in on at by from is are be will "
  + "you your this that with how why what when it its as we they he she i not no "
  + "new now just get make video watch full part official").split(" "));
const keywords = (s) =>
  ((s || "").toLowerCase().match(/[a-z0-9]{3,}/g) || []).filter((w) => !STOPWORDS.has(w));

const CANDIDATE_K = Number(process.env.CANDIDATE_TOPICS) || 5;

function shortlistTopics(watchTopics, meta, k = CANDIDATE_K) {
  if (watchTopics.length <= k) return watchTopics;
  const probe = new Set(keywords(`${meta.title} ${meta.channel}`));
  return watchTopics
    .map((t) => {
      const bag = new Set(keywords([t.name, t.notes, (t.queries || []).join(" ")].join(" ")));
      let score = 0;
      for (const w of probe) if (bag.has(w)) score++;
      return { t, score };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, k)
    .map((x) => x.t);
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
    // 6, not 12 — the model judges fit from a sample of titles; doubling the
    // sample doubled the bill without measurably improving the decision.
    sample_videos: (t.videos || []).slice(0, 6).map((v) => ({
      title: v.title, channel: v.channel, verdict: v.verdict,
    })),
  }));

// A proposed narrative's twin on the shelf: same trigger video, or names whose
// content words nest (one inside the other) or overlap by ≥ 60%.
function findTwin(topics, proposed) {
  const words = (s) => new Set(keywords(s).filter((w) => w !== "all"));
  const p = words(proposed.name);
  return topics.find((t) => {
    if (t.trigger && t.trigger === proposed.trigger) return true;
    const q = words(t.name.split("—")[0]);
    if (!p.size || !q.size) return false;
    const inter = [...p].filter((w) => q.has(w)).length;
    const nested = inter === Math.min(p.size, q.size);
    return (nested && Math.min(p.size, q.size) >= 2) || inter / new Set([...p, ...q]).size >= 0.6;
  }) || null;
}

const slugify = (s) => (s || "").toLowerCase()
  .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 48);

// Exported so scripts/model-gate.mjs can measure a candidate model against the
// Opus baseline on the EXACT prompt and schema production uses.
export { SYSTEM, ANALYSIS_SCHEMA, summarizeCorpus, shortlistTopics };

const videoEntry = (videoId, meta, verdict, note, today, source, rich) => ({
  videoId, url: `https://www.youtube.com/watch?v=${videoId}`,
  title: meta.title, channel: meta.channel,
  // Real date, views and length from the watch page when YouTube answered;
  // empty strings (the old behaviour) when it did not — the Series page treats
  // an empty date as "undated", never as today.
  published: rich?.meta?.published || "", views: rich?.meta?.views || "", length: rich?.meta?.length || "",
  query: source === "buildout" ? "auto-buildout" : "user-submitted",
  // From the search-page fallback when the watch page was refused: relative
  // age at capture, which the timeline turns into an approximate date.
  age_days: rich?.meta?.age_days ?? null, first_seen: today,
  transcript: null,
  verdict: verdict === "UNKNOWN" ? "UNREVIEWED" : verdict,
  verdict_note: `[live analysis, metadata-only] ${note}`,
  // Explicit, so the site can say which verdicts were read and which were
  // guessed. Datacenter IPs get empty caption bodies from YouTube, so the live
  // path is always metadata; scripts/fetch_transcripts.py + review-verdicts.mjs
  // upgrade it to "transcript" afterwards. Provisional is a state, not a fate.
  verdict_basis: "metadata",
  // The same filter signals the batch script stores, when the fetch succeeded.
  // Absent (not a zeroed stub) when it did not, so the page says "no signals yet".
  ...(rich?.yt ? { yt: rich.yt } : {}),
});

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "POST") return json(405, { error: "POST only" });
  const blocked = guard(req, { cost: 1, cors: CORS });
  if (blocked) return blocked;

  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const videoId = parseVideoId(body.url);
  if (!videoId) return json(400, { error: "not_a_youtube_link" });

  try {
    const watchlist = await getJSON(`${RAW}/watchlist.json`);
    // Every tracked id, for the slug-collision check — free, no extra request.
    const allTopicIds = new Set(watchlist.topics.map((t) => t.id));

    // Metadata first: the shortlist scores against the video's title/channel.
    const meta = await fetchVideoMeta(videoId);
    if (!meta) return json(404, { error: "video_not_found" });
    // Filter signals ride alongside the model call, not ahead of it: started
    // here, awaited only when the entry is written. A slow or refused YouTube
    // costs nothing but the signals (6 s cap), never the verdict.
    const richP = enrichVideo(videoId).catch(() => null);

    const candidates = shortlistTopics(watchlist.topics, meta);
    const topics = await Promise.all(
      candidates.map(async (t) => ({
        id: t.id,
        status: t.status,
        name: t.name,
        narrative: await getJSON(`${RAW}/corpus/${t.id}/narrative.json`).catch(() => null),
        videos: await getJSON(`${RAW}/corpus/${t.id}/videos.json`)
          .then((d) => d.videos).catch(() => []),
      })),
    );
    // Client-supplied context: just-created narratives the raw CDN doesn't know yet
    for (const ct of body.context_topics || []) {
      if (ct?.id && !topics.some((t) => t.id === ct.id)) {
        topics.push({
          id: ct.id, status: "active", name: ct.name || ct.id,
          narrative: ct.narrative || null, videos: ct.videos || [],
        });
      }
    }

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

    const client = new Anthropic();
    const response = await client.messages.create({
      // Configurable so the cheaper model can be switched on AFTER a measured
      // agreement test against this Opus baseline — never blind. These verdicts
      // feed published accountability stats; a quiet quality drop here is
      // product damage, not a saving.
      model: process.env.ANALYZE_MODEL || "claude-opus-5",
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
    const rich = await richP;
    // Surfaced in the response so the UI (and a curl) can see what YouTube
    // answered from this IP: ["video","comments","channel"], partial, or nothing.
    analysis.signals = rich ? { got: rich.got, error: rich.error } : { got: [], error: "enrichment_failed" };

    // The slug is ours to derive, not the model's to invent.
    analysis.new_narrative_id = analysis.decision === "new_narrative"
      ? slugify(analysis.new_narrative_name) : null;

    // Slug collision safety, checked against the WHOLE shelf (not just the
    // shortlist) — a "new" narrative whose slug already exists is an existing one.
    if (analysis.decision === "new_narrative" && allTopicIds.has(analysis.new_narrative_id)) {
      analysis.decision = "existing_narrative";
      analysis.topic_id = analysis.new_narrative_id;
    }
    // A clickbait/recycled shell can't FOUND a narrative unless confidence is high —
    // bait evidences narratives but low-confidence shells create noise tiles
    if (analysis.decision === "new_narrative" &&
        ["CLICKBAIT", "RECYCLED"].includes(analysis.verdict) &&
        analysis.confidence !== "high") {
      analysis.decision = "unrelated";
      analysis.verdict_note += " (New-narrative proposal suppressed: low-confidence clickbait/recycled shell.)";
    }

    if (analysis.decision === "existing_narrative" && analysis.topic_id) {
      const entry = videoEntry(videoId, meta, analysis.verdict, analysis.verdict_note, today, body.source, rich);
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
      const entry = videoEntry(videoId, meta, analysis.verdict, analysis.verdict_note, today, body.source, rich);
      const narrative = {
        name: analysis.new_narrative_claim_name || analysis.new_narrative_name,
        claim: analysis.new_narrative_claim,
        predictor: "to be determined",
        born: analysis.new_narrative_born || today.slice(0, 7),
        born_note: `${analysis.new_narrative_born_note || "Engine estimate"} (model estimate, pending audit)`,
        mutations: [],
        explanations: {
          layman: analysis.explanation_layman || "",
          intermediate: analysis.explanation_intermediate || "",
          expert: analysis.explanation_expert || "",
        },
        origin: { type: "engine", first_video: videoId, created: today },
      };
      const topicRecord = {
        id, name: analysis.new_narrative_name,
        industry: analysis.new_narrative_industry || "Unsorted",
        status: "active", started: today,
        trigger: `User-submitted video: ${meta.title} (${meta.channel})`,
        queries: analysis.new_narrative_queries || [],
        watched_predictors: [],
        notes: `Created by the analysis engine. ${analysis.new_narrative_claim}`,
      };
      // watchlist first (read-modify-write), then the two new files in parallel
      let persisted = false;
      const wl = await ghRead("watchlist.json");
      // Duplicate guard, against the FRESH watchlist (the raw CDN the shortlist
      // read lags by minutes). One paste founded "Chronic Inflammation Is the
      // Root of All Disease" and a second request founded "Inflammation Is the
      // Root of All Disease" from the same video: the slug check missed it.
      // Same trigger video, or one name's content words inside the other's
      // (or ≥ 60% overlap), means the narrative already exists — file the
      // video there instead of founding a twin.
      const dup = wl && findTwin(wl.data.topics, topicRecord);
      if (dup) {
        const cur = await ghRead(`corpus/${dup.id}/videos.json`);
        let added = false;
        if (cur && !cur.data.videos.some((v) => v.videoId === videoId)) {
          cur.data.videos.push(entry);
          added = await ghWrite(`corpus/${dup.id}/videos.json`, cur.data,
            `Engine: add ${videoId} to ${dup.id} (${entry.verdict}; twin of proposed "${analysis.new_narrative_name}")`, cur.sha);
        }
        analysis.decision = "existing_narrative";
        analysis.topic_id = dup.id;
        analysis.verdict_note += ` (Proposed new narrative matched existing "${dup.name}"; filed there.)`;
        return json(200, { status: "analyzed", video: meta, analysis, persisted: added, video_entry: entry });
      }
      if (wl && !wl.data.topics.some((t) => t.id === id)) {
        wl.data.topics.push(topicRecord);
        // Sequential: parallel contents-API writes race on the branch ref (409)
        const ok1 = await ghWrite("watchlist.json", wl.data,
          `Engine: new narrative "${analysis.new_narrative_name}" (${id})`, wl.sha);
        const ok2 = await ghWrite(`corpus/${id}/narrative.json`, narrative,
          `Engine: narrative.json for ${id}`);
        let ok3 = await ghWrite(`corpus/${id}/videos.json`, { videos: [entry] },
          `Engine: first video for ${id} (${entry.verdict})`);
        if (!ok3) {
          ok3 = await ghWrite(`corpus/${id}/videos.json`, { videos: [entry] },
            `Engine: first video for ${id} (${entry.verdict}, retry)`);
        }
        // The sides, from day one: a contested core question whose camps start
        // empty and fill as consolidation files videos under them.
        const camps = (analysis.new_narrative_camps || []).filter((c) => c.position);
        if (camps.length >= 2) {
          await ghWrite(`corpus/${id}/claims.json`, {
            note: "Consolidated claims. The core question's camps were proposed at founding (model, pending audit) and fill with sources on refresh.",
            updated: today, fingerprints: [],
            claims: [{
              id: "core-question", type: "contested",
              statement: `Where the sides split on: ${analysis.new_narrative_claim}`,
              note: "Camps proposed by the engine at founding — pending audit.",
              camps: camps.map((c) => ({ position: c.position, watch_for: c.watch_for, sources: [] })),
              sources: [],
            }],
          }, `Engine: founding camps for ${id}`);
        }
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
