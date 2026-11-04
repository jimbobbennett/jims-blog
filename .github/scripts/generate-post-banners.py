#!/usr/bin/env python3
"""Replace the duplicated portrait banners with reproducible title cards."""

import argparse
import hashlib
import io
from pathlib import Path
import re

import cairosvg
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
import yaml


ROOT = Path(__file__).resolve().parents[2]
PORTRAIT_HASH = "a8663db12be8313b7af297a0b05ebe3545d7059ab6af3de9d8bbbb60ba2e1786"
GENERATOR = "night-lime-title-card-v1"
WIDTH, HEIGHT = 1200, 630
BACKGROUND = "#111923"
TEXT = "#f4f6f7"
MUTED = "#b4bec5"
ACCENTS = ["#c5f36c", "#75d8ef", "#c5b0ff", "#ffae91", "#f0d477"]

# Personal posts need editorial context rather than technical keyword matching.
OVERRIDES = {
    "christmas-geekery": ("Maker life", "gift"),
    "taking-a-break": ("Personal", "coffee"),
    "updating-my-blog": ("Personal", "desktop"),
    "blind-technology": ("Accessibility", "eye"),
    "new-year-new-me": ("Personal", "rocket"),
    "bubbles-bubbles-bubbles-my-bubbles": ("Personal", "comments"),
    "socialnetworkingandhowtheworldseesme": ("Community", "comments"),
    "bubble-tea": ("Personal", "coffee"),
    "technical-tests": ("Developer life", "flask"),
    "todays-tea": ("Personal", "coffee"),
    "complexion-and-legal-issues": ("Open source", "file-code"),
    "game-of-phones-winter-is-coming": ("Mobile development", "mobile-alt"),
    "waiting-again": ("Personal", "hourglass-half"),
    "waiting-12-05-2014": ("Personal", "hourglass-half"),
    "stay-warm-with-microsoft-xamarin": ("Community", "heart"),
    "trust": ("Personal", "heart"),
    "trust-2": ("Personal", "heart"),
    "usefull-links": ("Developer resources", "code"),
    "lets-eat": ("Personal", "utensils"),
    "synergy": ("Developer tools", "desktop"),
    "im-certified": ("Developer life", "certificate"),
    "hitting-refresh-on-my-career": ("Developer life", "rocket"),
    "popping-my-open-source-cherry": ("Open source", "code"),
    "im-now-a-xamarin-mvp": ("Community", "trophy"),
    "im-on-itunes": ("Podcasts", "microphone-alt"),
    "im-on-itunes-again": ("Podcasts", "microphone-alt"),
    "the-jim-tonic-podcast": ("Podcasts", "microphone-alt"),
    "nugetizer-3000": ("Packages & libraries", "puzzle-piece"),
    "ndepend": ("Developer tools", "code"),
    "performance-tuning-a-website": ("Web development", "rocket"),
    "fabulous-santa-tracker": ("Maker life", "gift"),
    "fauxghost-a-clean-responsive-ghost-theme": ("Web development", "desktop"),
    "favicons-2": ("Web development", "desktop"),
    "why-cant-all-laptops-use-the-same-charger": ("Hardware", "plug"),
}

TOPICS = [
    (r"api keys|security|securing|ssl|firewall|permission", "Security", "lock"),
    (r"geofence|azure maps|locations|on a map", "Maps & location", "map-marker-alt"),
    (r"ibeacon|ibeacons|estimote", "Beacons & location", "broadcast-tower"),
    (r"database|mongodb|collections", "Data", "database"),
    (r"speech|caption", "Speech & accessibility", "microphone-alt"),
    (r"vision|face identification|describing a photo", "Computer vision", "eye"),
    (r"\bai\b|cognitive|models|daughters toys", "AI & machine learning", "microchip"),
    (r"iot|mxchip|serial|raspberry pi|hat cam|makers", "IoT & hardware", "microchip"),
    (r"nuget|pcl|portable class|libraries|jimlib", "Packages & libraries", "puzzle-piece"),
    (r"evolve|dev days|talk|speak|slides|mini-hack", "Speaking & community", "microphone-alt"),
    (r"in action|reviewed", "Books", "book-open"),
    (r"unit test|ui testing|specflow", "Testing", "flask"),
    (r"deployment|heroku|azure functions|appcenter", "Cloud & deployment", "cloud-upload-alt"),
    (r"visual studio|vscode|vs code|add-in|extension|dotnet new|try \.net", "Developer tools", "terminal"),
    (r"api for plex", "APIs & open source", "network-wired"),
    (r"xamarin|android|ios|mvvm|mobile|entry control", "Mobile development", "mobile-alt"),
    (r"website|domain|blog", "Web development", "desktop"),
]


def topic_for(slug, title):
    if slug in OVERRIDES:
        return OVERRIDES[slug]
    for pattern, label, icon in TOPICS:
        if re.search(pattern, title, re.IGNORECASE):
            return label, icon
    return "Developer notes", "code"


def find_font(explicit, bold=False):
    if explicit:
        return ImageFont.truetype(explicit, 20).path
    names = (
        ["Arial Bold.ttf", "DejaVuSans-Bold.ttf"]
        if bold else ["Arial.ttf", "DejaVuSans.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, 20).path
        except OSError:
            continue
    raise SystemExit("No supported font found. Pass --font and --bold-font paths.")


def wrap_title(draw, title, font, max_width):
    lines = []
    current = ""
    for word in title.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if not current:
                raise ValueError(f"Title contains a word too wide to render: {word}")
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def title_layout(draw, title, bold_font):
    for size in range(76, 35, -1):
        font = ImageFont.truetype(bold_font, size)
        try:
            lines = wrap_title(draw, title, font, 1060)
        except ValueError:
            continue
        line_height = round(size * 1.16)
        if len(lines) * line_height <= 330:
            return font, lines, line_height
    raise ValueError(f"Cannot fit the complete title: {title}")


def render_banner(path, title, label, icon, year, accent, regular_font, bold_font):
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(regular_font, 22)
    label_font = ImageFont.truetype(bold_font, 20)
    draw.rectangle((0, 0, WIDTH, 9), fill=accent)
    draw.rounded_rectangle((64, 54, 72, 83), radius=3, fill=accent)
    draw.text((88, 55), label.upper(), font=label_font, fill=accent)

    icon_svg = ROOT / "blog/static/fontawesome-5/svgs/solid" / f"{icon}.svg"
    svg = icon_svg.read_text().replace("<path ", f'<path fill="{accent}" ')
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=58, output_height=58)
    glyph = Image.open(io.BytesIO(png)).convert("RGBA")
    image.paste(glyph, (1076, 48), glyph)

    font, lines, line_height = title_layout(draw, title, bold_font)
    y = 172 + (330 - len(lines) * line_height) // 2
    for line in lines:
        bounds = draw.textbbox((64, y), line, font=font, anchor="lt")
        if bounds[2] > 1130 or bounds[3] > 510:
            raise ValueError(f"Title overflows the banner: {title}")
        draw.text((64, y), line, font=font, fill=TEXT, anchor="lt")
        y += line_height

    draw.line((64, 547, 1136, 547), fill="#34414d", width=2)
    draw.text((64, 572), "Jim Bennett", font=small, fill=TEXT)
    draw.text((236, 573), "/ jimbobbennett.dev", font=small, fill=MUTED)
    draw.text((1136, 572), year, font=small, fill=MUTED, anchor="rt")
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Generator", GENERATOR)
    metadata.add_text("Title", title)
    metadata.add_text("Topic", label)
    metadata.add_text("Icon", icon)
    image.save(path, optimize=True, pnginfo=metadata)
    return font.size, len(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write PNGs; otherwise list candidates.")
    parser.add_argument("--font", help="Path to a regular TrueType font.")
    parser.add_argument("--bold-font", help="Path to a bold TrueType font.")
    args = parser.parse_args()
    regular_font = find_font(args.font)
    bold_font = find_font(args.bold_font, bold=True)
    count = 0
    for post in sorted((ROOT / "blog/content/blogs").glob("*/index.md")):
        text = post.read_text()
        if not text.startswith("---"):
            continue
        front = yaml.safe_load(text.split("---", 2)[1])
        filename = front.get("featured_image")
        if not filename:
            continue
        banner = post.parent / filename
        if not banner.is_file():
            continue
        identical_portrait = hashlib.sha256(banner.read_bytes()).hexdigest() == PORTRAIT_HASH
        with Image.open(banner) as existing:
            generated = existing.info.get("Generator") == GENERATOR
        if not (identical_portrait or generated):
            continue
        title = front["title"]
        label, icon = topic_for(post.parent.name, title)
        accent = ACCENTS[int(hashlib.sha256(post.parent.name.encode()).hexdigest()[:8], 16) % len(ACCENTS)]
        if args.write:
            size, lines = render_banner(
                banner, title, label, icon, str(front["date"])[:4],
                accent, regular_font, bold_font,
            )
            print(f"{post.parent.name}: {label} / {icon} / {size}px / {lines} lines")
        else:
            print(f"{post.parent.name}: {title} [{label} / {icon}]")
        count += 1
    print(f"{'Generated' if args.write else 'Found'} {count} title cards.")


if __name__ == "__main__":
    main()
