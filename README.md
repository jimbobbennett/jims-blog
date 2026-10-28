# Jim's Blog

Blog is here: [jimbobbennett.dev](https://jimbobbennett.dev).

Run with:

```bash
cd blog
hugo server -D
```

## Cloudflare

Deployed as a Cloudflare Worker with static assets (config in `blog/wrangler.jsonc`). One-time: `cd blog && npm install && npx wrangler login`.

```bash
cd blog
npm run preview         # build for localhost and serve with wrangler dev on :8787
npm run preview:remote  # build and upload a version with its own preview URL (not live)
npm run deploy          # build and deploy to production
```
