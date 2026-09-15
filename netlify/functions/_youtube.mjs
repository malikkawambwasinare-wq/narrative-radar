/* Narrative Radar — YouTube signals for the live paste path.
   JS port of scripts/enrich_youtube.py so a pasted video lands fully tagged and
   dated at commit time instead of waiting for the batch script.

   Three fetches, all of pages YouTube serves to any browser:
     1. the watch page   → category, channelId, verified, likes, subscribers,
                           paid promotion, live, chapters, captions, language,
                           plus the real publish date, view count and length
     2. one POST to the endpoint the page itself uses for comments → count only
     3. the channel About page → country, joined date, total views, video count

   Storage rule holds: identifiers, counts, dates and category labels only.
   Every step is optional — a timeout or a bot-wall returns partial data, and a
   field we could not read is left absent, never written as a fake zero.

   Datacenter caveat, stated plainly: YouTube serves Netlify/Cloudflare empty
   caption bodies; whether it serves the full watch-page JSON and answers the
   comments POST from those IPs is unverified until the function is deployed.
   `enrichVideo` reports what it got so the caller can say so. */

const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36";
const HEADERS = { "User-Agent": UA, "Accept-Language": "en-US,en;q=0.9", Cookie: "CONSENT=YES+cb; SOCS=CAI" };

const ytjson = (html, name) => {
  const m = html.match(new RegExp(name + String.raw`\s*=\s*(\{.*?\});\s*(?:</script>|var |window)`, "s"));
  try { return m ? JSON.parse(m[1]) : {}; } catch { return {}; }
};
function walk(o, key, out = []) {
  if (Array.isArray(o)) for (const v of o) walk(v, key, out);
  else if (o && typeof o === "object") {
    if (key in o) out.push(o[key]);
    for (const v of Object.values(o)) walk(v, key, out);
  }
  return out;
}
const text = (o) => typeof o === "string" ? o
  : o?.simpleText || o?.content || (o?.runs || []).map((r) => r.text || "").join("") || "";
// "19.6M subscribers" → 19600000; "114,261" → 114261; null when no number.
function toInt(s) {
  const m = String(s || "").match(/([\d.,]+)\s*([KMB])?/);
  if (!m) return null;
  const n = parseFloat(m[1].replace(/,/g, ""));
  return Number.isFinite(n) ? Math.round(n * ({ K: 1e3, M: 1e6, B: 1e9 }[m[2]] || 1)) : null;
}
const MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" ");

async function fetchText(url, init, signal) {
  const r = await fetch(url, { ...init, headers: { ...HEADERS, ...(init?.headers || {}) }, signal });
  if (!r.ok) throw new Error(`HTTP ${r.status} for ${url}`);
  return r.text();
}

export async function videoSignals(videoId, signal) {
  const html = await fetchText(`https://www.youtube.com/watch?v=${videoId}`, {}, signal);
  const pr = ytjson(html, "ytInitialPlayerResponse");
  const d = ytjson(html, "ytInitialData");
  const vd = pr.videoDetails || {};
  const mf = pr.microformat?.playerMicroformatRenderer || {};
  if (!vd.videoId && !mf.category) throw new Error("watch page carried no player data (bot wall or consent page)");
  const owner = walk(d, "videoOwnerRenderer")[0] || {};
  const verified = (owner.badges || []).some((b) =>
    ["BADGE_STYLE_TYPE_VERIFIED", "BADGE_STYLE_TYPE_VERIFIED_ARTIST"].includes(b.metadataBadgeRenderer?.style));
  const handle = walk(owner, "canonicalBaseUrl").find((u) => typeof u === "string" && u.startsWith("/@"))?.slice(1) || null;
  const likeText = walk(d, "accessibilityText").find((s) => typeof s === "string" && s.includes("like this video"));
  const likes = likeText?.includes("other people") ? toInt(likeText.match(/([\d,]+) other people/)?.[1]) : null;
  const tracks = walk(pr, "captionTracks")[0] || [];
  const manual = tracks.some((t) => t.kind !== "asr");
  const lang = walk(pr, "defaultAudioLanguage")[0] || tracks[0]?.languageCode || null;
  const secs = parseInt(vd.lengthSeconds, 10);

  const yt = {
    category: mf.category || null,
    channelId: vd.channelId || null,
    handle,
    verified,
    unlisted: !!mf.isUnlisted,
    familySafe: mf.isFamilySafe !== false,
    regionsAvailable: (mf.availableCountries || []).length || null,
    likes,
    comments: null,
    subscribers: toInt(text(owner.subscriberCountText)),
    paidPromotion: walk(pr, "paidContentOverlayRenderer").length > 0,
    live: !!vd.isLiveContent,
    chapters: Math.floor(walk(d, "macroMarkersListItemRenderer").length / 2) || null,
    captions: manual ? "manual" : tracks.length ? "auto" : null,
    language: (lang || "").split("-")[0] || null,
  };
  const meta = {
    title: vd.title || null,
    channel: vd.author || null,
    published: mf.publishDate ? mf.publishDate.slice(0, 10) : null,
    views: /^\d+$/.test(vd.viewCount || "") ? `${Number(vd.viewCount).toLocaleString("en-US")} views` : null,
    // YouTube's own badge grammar: 16:57, or 1:30:17 past the hour.
    length: Number.isFinite(secs)
      ? (secs >= 3600 ? `${Math.floor(secs / 3600)}:${String(Math.floor(secs / 60) % 60).padStart(2, "0")}:` : `${Math.floor(secs / 60)}:`)
        + String(secs % 60).padStart(2, "0")
      : null,
  };

  // Comment count: the page loads comments by a continuation POST; we make that
  // one call and keep the header count. Best effort — comments may be disabled.
  try {
    const sec = walk(d, "itemSectionRenderer").filter((s) => s.sectionIdentifier === "comment-item-section");
    const token = walk(sec, "token")[0];
    const key = html.match(/"INNERTUBE_API_KEY":"([^"]+)"/)?.[1];
    const ver = html.match(/"INNERTUBE_CLIENT_VERSION":"([^"]+)"/)?.[1];
    if (token && key && ver) {
      const body = JSON.stringify({ context: { client: { clientName: "WEB", clientVersion: ver, hl: "en", gl: "US" } }, continuation: token });
      const res = await fetchText(`https://www.youtube.com/youtubei/v1/next?key=${key}&prettyPrint=false`, {
        method: "POST", body,
        headers: { "Content-Type": "application/json", "X-Youtube-Client-Name": "1", "X-Youtube-Client-Version": ver },
      }, signal);
      const hdr = walk(JSON.parse(res), "commentsHeaderRenderer")[0];
      yt.comments = hdr ? toInt(text(hdr.countText)) : null;
    }
  } catch { /* count stays null: comments off, or the POST refused from this IP */ }
  return { meta, yt };
}

export async function channelSignals(channelId, signal) {
  const html = await fetchText(`https://www.youtube.com/channel/${channelId}/about`, {}, signal);
  const about = walk(ytjson(html, "ytInitialData"), "aboutChannelViewModel")[0] || {};
  const j = text(about.joinedDateText).match(/([A-Z][a-z]{2}) (\d{1,2}), (\d{4})/);
  return {
    channelCountry: text(about.country) || null,
    channelJoined: j ? `${j[3]}-${String(MONTHS.indexOf(j[1]) + 1).padStart(2, "0")}-${j[2].padStart(2, "0")}` : null,
    channelViews: toInt(text(about.viewCountText)),
    channelVideos: toInt(text(about.videoCountText)),
    subscribers: toInt(text(about.subscriberCountText)),
  };
}

/* Fallback when the watch page is bot-walled (every datacenter IP): YouTube's
   search page still answers there, and searching a video's ID returns that
   video's card with its relative age ("3 years ago"), views and length. Age is
   month- or year-coarse, stored as age_days so the timeline can place it. */
const AGO = { second: 1 / 86400, minute: 1 / 1440, hour: 1 / 24, day: 1, week: 7, month: 30.44, year: 365.25 };
export async function searchSignals(videoId, signal) {
  const html = await fetchText(`https://www.youtube.com/results?search_query=${encodeURIComponent(`"${videoId}"`)}`, {}, signal);
  const card = walk(ytjson(html, "ytInitialData"), "videoRenderer").find((r) => r.videoId === videoId);
  if (!card) throw new Error("video not in its own search results");
  // YouTube serves both "3 years ago" and the compact "3y ago" / "2mo ago".
  const SHORT = { s: "second", m: "minute", min: "minute", h: "hour", d: "day", w: "week", mo: "month", y: "year", yr: "year" };
  const rel = text(card.publishedTimeText);
  const long = rel.match(/(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago/);
  const short = !long && rel.match(/(\d+)\s*(mo|min|yr|s|m|h|d|w|y)\b\s*ago/);
  const ago = long || (short && [short[0], short[1], SHORT[short[2]]]);
  const views = text(card.viewCountText).match(/[\d,]+/)?.[0];
  return {
    title: text(card.title) || null,
    channel: text(card.ownerText || card.longBylineText) || null,
    published: text(card.publishedTimeText) || null,          // relative text; not an ISO date
    age_days: ago ? Math.round(+ago[1] * AGO[ago[2]] * 100) / 100 : null,
    views: views ? `${views} views` : null,
    length: text(card.lengthText) || null,
  };
}

/* Everything the batch script stores, under one deadline. Returns
   { meta, yt, got: ["video","comments","channel"] } — `got` lists the steps
   that actually answered, so the caller can be honest about partial data. */
export async function enrichVideo(videoId, { timeoutMs = 6000 } = {}) {
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), timeoutMs);
  const out = { meta: {}, yt: null, got: [] };
  try {
    const { meta, yt } = await videoSignals(videoId, ac.signal);
    out.meta = meta; out.yt = yt; out.got.push("video");
    if (yt.comments != null) out.got.push("comments");
    if (yt.channelId) {
      try {
        const ch = await channelSignals(yt.channelId, ac.signal);
        if (yt.subscribers == null) yt.subscribers = ch.subscribers;
        delete ch.subscribers;
        Object.assign(yt, ch);
        out.got.push("channel");
      } catch { /* channel fields absent, video fields kept */ }
    }
    yt.enrichedOn = new Date().toISOString().slice(0, 10);
  } catch (e) {
    out.error = String(e.message || e);
    // Watch page refused: at least get the video onto the timeline.
    try {
      out.meta = await searchSignals(videoId, ac.signal);
      out.got.push("search");
    } catch { /* no date either; the entry stays undated and says so */ }
  } finally {
    clearTimeout(timer);
  }
  return out;
}
