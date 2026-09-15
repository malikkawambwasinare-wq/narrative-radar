// Narrative Radar — word/phrase search inside a narrative's transcripts.
//
// Pure functions, shared by the transcript-search endpoint and local tests.
// Transcripts are stored as "[MM:SS] text" or "[H:MM:SS] text" lines. Captions
// break mid-sentence, so matching runs over one flattened string with an
// offset → timestamp map; a phrase split across two caption lines still hits.
//
// What leaves the server is deliberately small: the timestamp of each match
// and a snippet of at most SNIPPET_WORDS words on each side. Full transcripts
// never do — they are other people's words, kept in a private store.

export const SNIPPET_WORDS = 5;       // words either side of the match (≈ 12-word snippet)
export const MAX_HITS_PER_VIDEO = 25;
export const MAX_VIDEOS = 300;

export function parseTranscript(text) {
  const segs = [];
  let flat = "";
  for (const line of String(text || "").split("\n")) {
    const m = line.match(/^\[(\d+):(\d{2})(?::(\d{2}))?\]\s*(.*)$/);
    if (!m) continue;
    const t = m[3] != null ? (+m[1]) * 3600 + (+m[2]) * 60 + (+m[3]) : (+m[1]) * 60 + (+m[2]);
    const body = m[4].replace(/\s+/g, " ").trim();
    if (!body) continue;
    if (flat) flat += " ";
    segs.push({ at: flat.length, t });
    flat += body;
  }
  return { flat, segs };
}

// "seed oil" → phrase; "inflam*" → prefix. Letters/numbers only at the edges,
// so "oil" does not match "toil" and "2027" does not match "20270".
export function buildQuery(q) {
  const clean = String(q || "").toLowerCase().replace(/[“”"]/g, "").replace(/\s+/g, " ").trim();
  if (clean.length < 2 || clean.length > 60) return null;
  const prefix = clean.endsWith("*");
  const words = clean.replace(/\*+$/, "").split(" ").filter(Boolean);
  if (!words.length) return null;
  const esc = (w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const body = words.map(esc).join("[\\s\\-]+");
  return new RegExp(`(?<![\\p{L}\\p{N}])${body}${prefix ? "[\\p{L}\\p{N}]*" : "(?![\\p{L}\\p{N}])"}`, "giu");
}

function timeAt(segs, idx) {
  let lo = 0, hi = segs.length - 1, ans = 0;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (segs[mid].at <= idx) { ans = mid; lo = mid + 1; } else hi = mid - 1;
  }
  return segs.length ? segs[ans].t : 0;
}

function snippet(flat, start, end) {
  const before = flat.slice(Math.max(0, start - 200), start).split(" ");
  const after = flat.slice(end, end + 200).split(" ");
  // A partial word at the cut edge is dropped so the snippet starts and ends cleanly.
  const b = before.slice(before.length > SNIPPET_WORDS ? -SNIPPET_WORDS - 1 : 0).slice(-SNIPPET_WORDS - 1);
  return {
    before: (before.length > SNIPPET_WORDS ? b.slice(1) : b).join(" ").trim(),
    match: flat.slice(start, end),
    after: after.slice(0, SNIPPET_WORDS + 1).join(" ").trim(),
  };
}

/** @param {Record<string,string>} transcripts videoId -> raw transcript text */
export function searchTranscripts(transcripts, q) {
  const re = buildQuery(q);
  if (!re) return { error: "query must be 2–60 characters" };
  const videos = [];
  let totalHits = 0;
  for (const [videoId, text] of Object.entries(transcripts)) {
    const { flat, segs } = parseTranscript(text);
    const lower = flat;                       // the regex is case-insensitive
    const hits = [];
    let count = 0;
    re.lastIndex = 0;
    for (let m; (m = re.exec(lower)); ) {
      count++;
      if (hits.length < MAX_HITS_PER_VIDEO) {
        const t = timeAt(segs, m.index);
        // Collapse repeats inside the same 20 seconds into one hit.
        if (!hits.length || t - hits[hits.length - 1].t >= 20) hits.push({ t, ...snippet(flat, m.index, m.index + m[0].length) });
      }
      if (m[0].length === 0) re.lastIndex++;
    }
    if (count) { videos.push({ videoId, count, hits }); totalHits += count; }
  }
  videos.sort((a, b) => b.count - a.count);
  return { searched: Object.keys(transcripts).length, totalHits, videoCount: videos.length, videos: videos.slice(0, MAX_VIDEOS) };
}
