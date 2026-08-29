// Narrative Radar — spend guard for the paid endpoints.
//
// The paste flow is public and every model call is founder-funded, so an
// unguarded engine is an uncapped bill. This is the cheap first line:
//
//   1. per-IP burst limit  — raw request count in a rolling minute
//   2. global daily ceiling — weighted COST UNITS, not calls, because the
//      endpoints differ by ~40x in price (analyze ~$0.035, a genesis trace
//      $1.50-4.50). A call-count cap would not constrain spend.
//
// State is per-instance and resets on cold start, so this blunts floods but
// does not bind absolutely. THE control that actually binds is the spend limit
// set in the Anthropic console — set it there too; this is defence in depth.
//
// Fails OPEN by design: a bug in the limiter must never take the product down.

const WINDOW_MS = 60_000;
const ipHits = new Map();     // ip -> [timestamps]
let dayKey = null;
let daySpend = 0;             // cost units consumed today

const num = (k, dflt) => {
  const v = Number(process.env[k]);
  return Number.isFinite(v) && v > 0 ? v : dflt;
};

const clientIp = (req) =>
  req.headers.get("x-nf-client-connection-ip") ||
  req.headers.get("cf-connecting-ip") ||
  (req.headers.get("x-forwarded-for") || "").split(",")[0].trim() ||
  "unknown";

function prune(now) {
  if (ipHits.size < 2000) return;              // only sweep when it matters
  for (const [ip, arr] of ipHits) {
    const live = arr.filter((t) => now - t < WINDOW_MS);
    if (live.length) ipHits.set(ip, live);
    else ipHits.delete(ip);
  }
}

/**
 * @param {Request} req
 * @param {{cost?: number, cors?: object}} opts  cost = spend units (1 ≈ one analyze call)
 * @returns {Response|null}  a 429/503 to return immediately, or null to proceed
 */
export function guard(req, { cost = 1, cors = {} } = {}) {
  try {
    const now = Date.now();
    const deny = (status, error, detail) =>
      new Response(JSON.stringify({ error, detail }), {
        status,
        headers: { "Content-Type": "application/json", "Retry-After": "60", ...cors },
      });

    // --- global daily ceiling, in cost units ---
    const today = new Date(now).toISOString().slice(0, 10);
    if (dayKey !== today) { dayKey = today; daySpend = 0; }
    const dailyMax = num("MAX_SPEND_UNITS_PER_DAY", 400);
    if (daySpend + cost > dailyMax) {
      return deny(503, "daily_ceiling_reached",
        "The engine has hit today's spend ceiling. It resets at midnight UTC.");
    }

    // --- per-IP burst limit, in raw requests ---
    const perMin = num("MAX_CALLS_PER_MIN", 10);
    const ip = clientIp(req);
    const recent = (ipHits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
    if (recent.length + 1 > perMin) {
      return deny(429, "rate_limited", "Too many requests — wait a minute and try again.");
    }

    recent.push(now);
    ipHits.set(ip, recent);
    daySpend += cost;
    prune(now);
    return null;
  } catch {
    return null;   // fail open
  }
}

/** Current guard state — handy for a health endpoint or debugging. */
export const guardState = () => ({
  day: dayKey,
  spendUnits: daySpend,
  ceiling: num("MAX_SPEND_UNITS_PER_DAY", 400),
  trackedIps: ipHits.size,
});
