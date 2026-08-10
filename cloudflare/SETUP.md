# Moving the engine to Cloudflare Workers (free)

The engine (analyze / sweep / consolidate / trace-origin) runs the exact same
code as on Netlify — `worker.mjs` just routes requests to the same four files
in `netlify/functions/`. Cloudflare's free tier allows 100,000 requests per
day and does not bill for time spent waiting on the Claude API, which is what
burned the Netlify credits.

## One-time setup (about 10 minutes)

1. **Create a free Cloudflare account** at https://dash.cloudflare.com/sign-up
   (email + password, no card needed).

2. **Log the terminal into that account.** In this folder run:

   ```bash
   npx wrangler login
   ```

   A browser window opens — click "Allow".

3. **Deploy the engine:**

   ```bash
   npx wrangler deploy
   ```

   It prints a URL like `https://narrative-radar-engine.<something>.workers.dev`
   — that is the engine's new address. Save it.

4. **Give it the keys** (same values as in Netlify → Site settings →
   Environment variables — each command waits for you to paste the value):

   ```bash
   npx wrangler secret put ANTHROPIC_API_KEY
   npx wrangler secret put GH_TOKEN
   npx wrangler secret put X_BEARER_TOKEN
   ```

5. Tell Claude the workers.dev URL — the site's `API_BASE` gets pointed at it
   and the engine is tested end to end. After that, Netlify is optional.

## Known risk to test

`/api/sweep` scrapes YouTube search results. YouTube tolerated Netlify's
datacenter IPs; Cloudflare's IPs may be treated differently. If sweep comes
back empty, refresh/buildout loses auto-discovery (paste-a-link analysis is
unaffected). Test before cancelling anything.
