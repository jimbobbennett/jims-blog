#!/usr/bin/env bash
#
# Release any blog post whose publish date is today.
#
# For every post under blog/content/blogs whose `publishDate` (or, as a
# fallback, `date`) falls on today's UTC date:
#   * if it is still `draft: true`, flip it to `draft: false` so Hugo will
#     build it (a flip needs a commit back to main), and
#   * either way, mark that a rebuild + deploy is needed so the post goes live.
#
# Hugo's buildFuture is off (the default), so future-dated posts stay hidden
# until a build runs on/after their date — this job is that build.
#
# Outputs (to $GITHUB_OUTPUT):
#   promoted=1  a draft was flipped to draft: false -> the workflow commits it
#   rebuild=1   at least one post is dated today     -> the workflow deploys
set -euo pipefail

TODAY="$(date -u +%Y-%m-%d)"
PROMOTED=0
REBUILD=0

echo "Scanning for posts with a publish date of ${TODAY} (UTC)..."

for f in blog/content/blogs/*/index.md; do
  [ -f "$f" ] || continue

  # Prefer publishDate; fall back to date. Strip quotes and keep the YYYY-MM-DD.
  pd="$(grep -m1 -iE '^publishDate:[[:space:]]*' "$f" | sed -E 's/^[Pp]ublish[Dd]ate:[[:space:]]*//; s/"//g' || true)"
  if [ -z "$pd" ]; then
    pd="$(grep -m1 -iE '^date:[[:space:]]*' "$f" | sed -E 's/^[Dd]ate:[[:space:]]*//; s/"//g' || true)"
  fi
  pd_date="${pd:0:10}"

  [ "$pd_date" = "$TODAY" ] || continue

  REBUILD=1
  echo "  -> Releasing $f (publish date ${pd_date})"

  # If it is currently a draft, flip the first `draft: true` to `draft: false`.
  # awk is used (rather than sed -i) so the in-place edit behaves identically
  # on GNU (CI) and BSD (local macOS) systems.
  draft_line="$(grep -m1 -iE '^draft:[[:space:]]*' "$f" || true)"
  if echo "$draft_line" | grep -qiE '^draft:[[:space:]]*true'; then
    awk '
      !done && /^[Dd]raft:[[:space:]]*[Tt]rue[[:space:]]*$/ { sub(/[Tt]rue/, "false"); done=1 }
      { print }
    ' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
    PROMOTED=1
    echo "     flipped draft: true -> draft: false"
  fi
done

if [ "$REBUILD" -eq 0 ]; then
  echo "No posts scheduled for today. Nothing to publish."
fi

{
  echo "promoted=${PROMOTED}"
  echo "rebuild=${REBUILD}"
} >> "$GITHUB_OUTPUT"
