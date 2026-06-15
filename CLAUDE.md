# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

The Hugo project lives in `blog/`, not the repo root. All Hugo commands must be run from there.

- Local dev server (shows drafts): `cd blog && hugo server -D`
- Production build: `cd blog && hugo --minify`

There is no test suite, no linter, and no package-manager-managed dependencies (the `package.json` in `blog/` is effectively empty). Hugo version is pinned to `0.159.0` (extended) in CI.

## Architecture

This is a Hugo static site published to `jimbobbennett.dev` via GitHub Pages. Two GitHub Actions workflows drive everything:

- `.github/workflows/gh-pages.yml` — on every push to `main` (and on PRs for build verification), runs `hugo --minify` in `blog/` and deploys `blog/public/` to GitHub Pages.
- `.github/workflows/scheduled-publish.yml` — runs daily at 07:00 UTC. It calls `.github/scripts/publish-scheduled.sh`, which scans `blog/content/blogs/*/index.md`, finds posts whose `publishDate` (falling back to `date`) is today, flips `draft: true` → `draft: false`, commits the change back to `main`, and rebuilds + deploys. Hugo's `buildFuture` is off, so future-dated drafts stay hidden until this job runs on/after their date. **This means scheduling a post is just: set `publishDate` to a future date and `draft: true`. Do not manually flip the draft flag for scheduled posts — the action does it.**

### Content model

- **Blog posts** are Hugo page bundles: `blog/content/blogs/<slug>/index.md` with sibling assets (e.g. `banner.png`, `infographic.pdf`) in the same folder. Reference them in markdown as `/blogs/<slug>/<file>` (site-root paths), not relative paths.
- **Section pages** (`videos`, `podcasts`, `livestreams`, `conferences`, `resume`) are config-driven, not file-per-item. Edit `params.videos`, `params.podcasts`, etc. in `blog/config.yaml` rather than creating markdown files. The matching templates live in `blog/layouts/_default/<section>.html`.
- **Top navigation** is config-driven via `Menus.main` in `blog/config.yaml`. Update menu entries there, not in templates.

### Front matter conventions

The archetype is `blog/archetypes/default.md`. Conventions enforced by templates:

- `featured_image` is a **filename** in the post's bundle directory (e.g. `banner.png`). `layouts/_default/list.html` constructs the card image URL as `{{ .RelPermalink }}/{{ .Params.featured_image }}`, so a leading slash or full path will break the card.
- `image` (optional) is the in-post header image, rendered by `single.html` as-is — site-root paths are fine here.
- `toc` (default `true`) and `showAuthor` (default `true`) toggle the table of contents and author byline in `single.html`.
- `publishDate` is what the scheduled-publish action checks first; `date` is the fallback. Both should be `YYYY-MM-DD`.

### Templates

- Base shell: `blog/layouts/_default/baseof.html`
- Home: `blog/layouts/index.html` + `blog/layouts/partials/sections/*`
- Blog list: `blog/layouts/_default/list.html`
- Blog post: `blog/layouts/_default/single.html`
- Markdown is rendered with `markup.goldmark.renderer.unsafe: true`, so raw HTML in posts is allowed.

### Static assets

Served from `blog/static/` at site root: `/css/...`, `/images/...`, `/downloads/...`, etc. The `CNAME` file at the repo root is for GitHub Pages; `blog/static/CNAME` is the one Hugo actually copies into `public/`.
