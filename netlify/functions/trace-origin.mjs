// Narrative Radar — Genesis layer: trace a narrative's earliest utterance on X.
// POST /api/trace-origin {topic, phrase, force?} →
//   Bisects the X full-archive (back to 2006) on time windows to find the
//   earliest surviving post carrying the phrase, then commits a `genesis`
//   record into the narrative. Pay-per-use X API: ~$0.005/post read;
//   a trace reads ~150-300 posts (~$0.75-1.50). Hard abort at READ_BUDGET.
//   Same phrase traced before → returns the stored genesis free (force:true
//   to re-trace).
const REPO = "malikkawambwasinare-wq/narrative-radar";
const RAW = `https://raw.githubusercontent.com/${REPO}/main`;
const READ_BUDGET = 600; // ~$3 — hard cap per trace
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};
const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status, headers: { "Content-Type": "application/json", ...CORS },
  });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function xSearch(state, query, startISO, endISO, maxResults) {
  if (state.reads >= READ_BUDGET) {
    throw new Error(`read budget exceeded (${state.reads} reads ≈ $${(state.reads * 0.005).toFixed(2)}) — aborted to protect balance`);
  }
  const token = process.env.X_BEARER_TOKEN;
  const params = new URLSearchParams({
    query,
    start_time: startISO,
    end_time: endISO,
    max_results: String(maxResults),
    "tweet.fields": "created_at,public_metrics,author_id",
    expansions: "author_id",
    "user.fields": "username,name",
  });
  for (let attempt = 0; attempt < 2; attempt++) {
    const r = await fetch(`https://api.x.com/2/tweets/search/all?${params}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (r.status === 429) { await sleep(3000); continue; }
    if (!r.ok) throw new Error(`X API ${r.status}: ${(await r.text()).slice(0, 160)}`);
    const d = await r.json();
    state.reads += (d.data || []).length;
    const users = Object.fromEntries((d.includes?.users || []).map((u) => [u.id, u]));
    return (d.data || []).map((t) => ({
      id: t.id,
      text: t.text,
      created_at: t.created_at,
      author: users[t.author_id]?.name || "",
      username: users[t.author_id]?.username || "",
      metrics: t.public_metrics,
    }));
  }
  throw new Error("X API rate limited (429 twice)");
}

const ghHeaders = () => ({
  Authorization: `Bearer ${process.env.GH_TOKEN}`,
  Accept: "application/vnd.github+json",
  "User-Agent": "narrative-radar-engine",
});

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: CORS });
  if (req.method !== "POST") return json(405, { error: "POST only" });
  if (!process.env.X_BEARER_TOKEN) {
    return json(200, { status: "error", error: "x_not_connected" });
  }
  let body;
  try { body = await req.json(); } catch { return json(400, { error: "bad JSON" }); }
  const { topic, phrase } = body;
  if (!topic || !phrase) return json(400, { error: "topic and phrase required" });

  const state = { reads: 0 };
  try {
    const query = `"${phrase.replace(/"/g, "")}" -is:retweet lang:en`;
    const ARCHIVE_START = Date.parse("2006-03-21T00:00:00Z");
    const now = Date.now() - 60_000;
    const iso = (t) => new Date(t).toISOString().replace(/\.\d{3}Z$/, "Z");

    // Use the narrative's born estimate to seed the bracket, but first check
    // for pre-history before it (the estimate could be too late)
    const narrative = await fetch(`${RAW}/corpus/${topic}/narrative.json`)
      .then((r) => r.json()).catch(() => null);

    // Same phrase already traced → return the stored result, spend nothing.
    if (!body.force && narrative?.genesis?.phrase === phrase && narrative.genesis.first_found) {
      return json(200, { status: "already_traced", topic, genesis: narrative.genesis, persisted: true });
    }

    const bornYear = parseInt(((narrative?.born || "").match(/\d{4}/) || [])[0]) || null;
    let lo = ARCHIVE_START;
    let hi = now;
    if (bornYear) {
      const preEnd = Date.parse(`${bornYear - 2}-01-01T00:00:00Z`);
      if (preEnd > ARCHIVE_START) {
        const pre = await xSearch(state, query, iso(ARCHIVE_START), iso(preEnd), 10);
        await sleep(1100);
        if (pre.length) hi = preEnd;           // earlier than the estimate — bisect pre-history
        else lo = preEnd;                       // estimate holds — bisect from there
      }
    }

    // Confirm the phrase exists at all in [lo, hi]
    const any = await xSearch(state, query, iso(lo), iso(hi), 10);
    await sleep(1100);
    if (!any.length) {
      return json(200, { status: "not_found", phrase, reads: state.reads,
        est_cost_usd: +(state.reads * 0.005).toFixed(2) });
    }

    // Bisect down to a ~14-day window containing the earliest post
    let probes = 0;
    while (hi - lo > 14 * 86400_000 && probes < 12) {
      const mid = lo + (hi - lo) / 2;
      const hits = await xSearch(state, query, iso(lo), iso(mid), 10);
      await sleep(1100);
      if (hits.length) hi = mid; else lo = mid;
      probes++;
    }

    // Pull the earliest window fully. X only returns newest-first, so a full
    // page means the window is too dense to expose its oldest post — keep
    // bisecting down to ≤1 day, then re-pull once.
    let windowHits = await xSearch(state, query, iso(lo), iso(hi), 100);
    if (windowHits.length >= 100) {
      for (let extra = 0; hi - lo > 86400_000 && extra < 8; extra++) {
        await sleep(1100);
        const mid = lo + (hi - lo) / 2;
        const early = await xSearch(state, query, iso(lo), iso(mid), 10);
        if (early.length) hi = mid; else lo = mid;
      }
      await sleep(1100);
      windowHits = await xSearch(state, query, iso(lo), iso(hi), 100);
    }
    const dense = windowHits.length >= 100;
    const sorted = windowHits.sort((a, b) => a.created_at.localeCompare(b.created_at));
    const earliest = sorted[0] || any.sort((a, b) => a.created_at.localeCompare(b.created_at))[0];
    const estCost = +(state.reads * 0.005).toFixed(2);

    const genesis = {
      platform: "x",
      phrase,
      first_found: earliest && {
        date: earliest.created_at,
        author: earliest.author,
        username: earliest.username,
        text: earliest.text.slice(0, 240),
        url: `https://x.com/${earliest.username}/status/${earliest.id}`,
        metrics: earliest.metrics,
      },
      runners_up: sorted.slice(1, 3).map((t) => ({
        date: t.created_at, username: t.username, url: `https://x.com/${t.username}/status/${t.id}`,
      })),
      method: "X full-archive time bisection (earliest surviving post; deleted posts invisible)"
        + (dense ? "; phrase very dense — earliest within final day approximate" : ""),
      reads_used: state.reads,
      est_cost_usd: estCost,
      traced_at: new Date().toISOString().slice(0, 10),
    };

    // Commit into narrative.json
    let persisted = false;
    const path = `corpus/${topic}/narrative.json`;
    const cur = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
      headers: ghHeaders(),
    });
    if (cur.ok) {
      const f = await cur.json();
      const n = JSON.parse(Buffer.from(f.content, "base64").toString("utf-8"));
      n.genesis = genesis;
      const put = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
        method: "PUT",
        headers: ghHeaders(),
        body: JSON.stringify({
          message: `Engine: genesis trace for ${topic} (${earliest?.created_at?.slice(0, 10)}, ${state.reads} reads) [skip netlify]`,
          content: Buffer.from(JSON.stringify(n, null, 2)).toString("base64"),
          sha: f.sha,
        }),
      });
      persisted = put.ok;
    }

    return json(200, { status: "traced", topic, genesis, persisted });
  } catch (e) {
    return json(500, { status: "error", error: String(e.message || e).slice(0, 300),
      reads: state.reads, est_cost_usd: +(state.reads * 0.005).toFixed(2) });
  }
};
