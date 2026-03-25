# Copilot instructions for `jims-blog`

## Build, test, and lint commands

This repository is a Hugo site with the actual site in `blog/`.

- Run locally (including drafts):
  - `cd blog && hugo server -D`
- Production build:
  - `cd blog && hugo --minify`

Testing/linting:

- There is currently no automated test suite configured in this repo.
- There is currently no lint command configured in this repo.
- Because no tests are configured, there is no single-test command available.

CI/deploy reference:

- GitHub Actions workflow `.github/workflows/gh-pages.yml` builds with `cd blog && hugo --minify` and deploys `blog/public` to GitHub Pages on pushes to `main`.

## High-level architecture

- The Hugo project root is `blog/` (not repository root).
- Global site behavior and most non-blog page content are driven from `blog/config.yaml`:
  - navigation (`Menus.main`)
  - hero/about/projects/footer
  - videos, podcasts, livestreams, conferences data under `params.*`
- Template structure:
  - base shell: `blog/layouts/_default/baseof.html`
  - home page: `blog/layouts/index.html` + `blog/layouts/partials/sections/*`
  - blog list page(s): `blog/layouts/_default/list.html`
  - blog post page: `blog/layouts/_default/single.html`
  - section-style pages (videos/podcasts/livestreams/conferences/resume): dedicated templates in `blog/layouts/_default/*.html`
- Static assets are served from `blog/static/` and referenced as site-root paths (`/css/...`, `/images/...`, `/downloads/...`).

## Key conventions in this codebase

- Blog posts are organized as Hugo page bundles:
  - `blog/content/blogs/<slug>/index.md`
  - sibling assets in the same folder (for example `banner.png`)
- Post cards in `layouts/_default/list.html` expect `featured_image` in front matter and construct image URLs as:
  - `{{ .RelPermalink }}/{{ .Params.featured_image }}`
  - So `featured_image` should usually be a filename in the same bundle directory.
- Archetype for new content is `blog/archetypes/default.md` and includes front matter keys like `draft`, `author`, `tags`, `image`, `description`, and `toc`.
- `single.html` uses front matter flags:
  - `showAuthor` (defaults to true)
  - `toc` (defaults to true)
  - `image` for optional header image
- Content for `videos`, `podcasts`, `livestreams`, and `conferences` pages is primarily config-driven from `config.yaml` (`params.videos`, `params.podcasts`, etc.), not per-item markdown files.
- The top navigation is config-driven via `Menus.main`; update menu entries in `config.yaml` rather than editing header template logic for standard nav changes.
