# Jim's Blog

Blog is here: [jimbobbennett.dev](https://jimbobbennett.dev).

Run with:

```bash
cd blog
hugo server -D
```

The blog archive loads the next page of posts automatically as readers scroll.
Hugo's `pagination.pagerSize` in `blog/config.yaml` controls the batch size.
Standard pagination remains available without JavaScript; failed loads offer a
manual retry without losing the posts already displayed.

## Post banners

Older posts that shared the same portrait use generated 1200 × 630 PNG title
cards with the full post title and a topic icon from the bundled Font Awesome
assets. Their existing `banner.png` paths are preserved.

To regenerate these cards after changing a title:

```bash
python3 -m pip install -r .github/scripts/banner-requirements.txt
python3 .github/scripts/generate-post-banners.py --write
```

The script only updates the original duplicated portrait or cards it previously
generated, leaving other artwork untouched. It uses Arial or DejaVu Sans;
pass `--font` and `--bold-font` for explicit font paths. CairoSVG also requires
the native Cairo library.

## Cloudflare

Deployed as a Cloudflare Worker with static assets (config in `blog/wrangler.jsonc`). Cloudflare Workers Builds deploys every push to `main` and gives other branches preview URLs. The `scheduled publish` workflow releases dated drafts by committing to `main`, which triggers that build.

To deploy by hand, one-time: `cd blog && npm install && npx wrangler login`.

```bash
cd blog
npm run preview         # build for localhost and serve with wrangler dev on :8787
npm run preview:remote  # build and upload a version with its own preview URL (not live)
npm run deploy          # build and deploy to production
```
