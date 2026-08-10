// Narrative Radar engine on Cloudflare Workers (free tier).
// Thin router over the same handlers Netlify runs — the four function files
// are the single source of truth; this file only maps routes and copies
// Worker secrets into process.env, which the handlers read.
import analyze from "../netlify/functions/analyze.mjs";
import sweep from "../netlify/functions/sweep.mjs";
import consolidate from "../netlify/functions/consolidate.mjs";
import traceOrigin from "../netlify/functions/trace-origin.mjs";

const ROUTES = {
  "/api/analyze": analyze,
  "/api/sweep": sweep,
  "/api/consolidate": consolidate,
  "/api/trace-origin": traceOrigin,
};

export default {
  async fetch(req, env) {
    for (const k of ["ANTHROPIC_API_KEY", "GH_TOKEN", "X_BEARER_TOKEN"]) {
      if (env[k]) process.env[k] = env[k];
    }
    const handler = ROUTES[new URL(req.url).pathname];
    if (!handler) {
      return new Response(JSON.stringify({ error: "not found" }), {
        status: 404,
        headers: { "Content-Type": "application/json" },
      });
    }
    return handler(req);
  },
};
