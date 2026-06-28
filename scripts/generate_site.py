"""
Generate docs/index.html from data/ JSON files.
Reads the same data as generate_readme.py; outputs a static GitHub Pages site.
"""
import json
import markdown as _md
import os
import re
import urllib.parse
from datetime import datetime, timezone
from html import escape

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT            = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR     = os.path.join(ROOT, "data", "content")
PACKAGES_DIR    = os.path.join(ROOT, "data", "packages")
SOFTWARE_DIR    = os.path.join(ROOT, "data", "software")
CHAPTERS_DIR    = os.path.join(ROOT, "data", "chapters")
MEMBERS_DIR     = os.path.join(ROOT, "data", "members")
CONTRIBUTING_MD = os.path.join(ROOT, "CONTRIBUTING.md")
OUT_FILE        = os.path.join(ROOT, "docs", "index.html")

# ── Inline SVG paths for social platforms ──────────────────────────────────────
SVG_PATHS = {
    "github":    "M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z",
    "linkedin":  "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
    "mastodon":  "M23.268 5.313c-.35-2.578-2.617-4.61-5.304-5.004C17.51.242 15.792 0 11.813 0h-.03c-3.98 0-4.835.242-5.288.309C3.882.692 1.496 2.518.917 5.127.64 6.412.61 7.837.661 9.143c.074 1.874.088 3.745.26 5.611.118 1.24.325 2.47.62 3.68.55 2.237 2.777 4.098 4.96 4.857 2.336.792 4.849.923 7.256.38.265-.061.527-.132.786-.213.585-.184 1.27-.39 1.774-.753a.057.057 0 0 0 .023-.043v-1.809a.052.052 0 0 0-.02-.041.053.053 0 0 0-.046-.01 20.282 20.282 0 0 1-4.709.545c-2.73 0-3.463-1.284-3.674-1.818a5.593 5.593 0 0 1-.319-1.433.053.053 0 0 1 .066-.054c1.517.363 3.072.546 4.632.546.376 0 .75 0 1.125-.01 1.57-.044 3.224-.124 4.768-.422.038-.008.077-.015.11-.024 2.435-.464 4.753-1.92 4.989-5.604.008-.145.03-1.52.03-1.67.002-.512.167-3.63-.024-5.545zm-3.748 9.195h-2.561V8.29c0-1.309-.55-1.976-1.67-1.976-1.23 0-1.846.79-1.846 2.35v3.403h-2.546V8.663c0-1.56-.617-2.35-1.848-2.35-1.112 0-1.668.668-1.67 1.977v6.218H4.822V8.102c0-1.31.337-2.35 1.011-3.12.696-.77 1.608-1.164 2.74-1.164 1.311 0 2.302.5 2.962 1.498l.638 1.06.638-1.06c.66-.999 1.65-1.498 2.96-1.498 1.13 0 2.043.395 2.74 1.164.675.77 1.012 1.81 1.012 3.12z",
    "bluesky":   "M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.204-.659-.3-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8z",
    "youtube":   "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z",
    "website":   "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z",
    "x":         "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.737-8.835L1.254 2.25H8.08l4.259 5.63L18.244 2.25zm-1.161 17.52h1.833L7.084 4.126H5.117L17.083 19.77z",
    "instagram": "M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z",
    # Archive/package box — represents PyPI (a package index)
    "pypi": "M1.5 9.75A.75.75 0 0 1 2.25 9h19.5a.75.75 0 0 1 0 1.5H2.25a.75.75 0 0 1-.75-.75zM2.25 4.5A2.25 2.25 0 0 0 0 6.75v.75c0 .414.336.75.75.75h22.5A.75.75 0 0 0 24 7.5v-.75A2.25 2.25 0 0 0 21.75 4.5H2.25zm-.75 6.75v7.5A2.25 2.25 0 0 0 3.75 21h16.5A2.25 2.25 0 0 0 22.5 18.75v-7.5H1.5zm9 2.25h3a.75.75 0 0 1 0 1.5h-3a.75.75 0 0 1 0-1.5z",
    "meetup": "M6.98.555a.518.518 0 0 0-.105.011.53.53 0 1 0 .222 1.04.533.533 0 0 0 .409-.633.531.531 0 0 0-.526-.418zm6.455.638a.984.984 0 0 0-.514.143.99.99 0 1 0 1.02 1.699.99.99 0 0 0 .34-1.36.992.992 0 0 0-.846-.482zm-3.03 2.236a5.029 5.029 0 0 0-4.668 3.248 3.33 3.33 0 0 0-1.46.551 3.374 3.374 0 0 0-.94 4.562 3.634 3.634 0 0 0-.605 4.649 3.603 3.603 0 0 0 2.465 1.597c.018.732.238 1.466.686 2.114a3.9 3.9 0 0 0 5.423.992c.068-.047.12-.106.184-.157.987.881 2.47 1.026 3.607.24a2.91 2.91 0 0 0 1.162-1.69 4.238 4.238 0 0 0 2.584-.739 4.274 4.274 0 0 0 1.19-5.789 2.466 2.466 0 0 0 .433-3.308 2.448 2.448 0 0 0-1.316-.934 4.436 4.436 0 0 0-.776-2.873 4.467 4.467 0 0 0-5.195-1.656 5.106 5.106 0 0 0-2.773-.807zm-5.603.817a.759.759 0 0 0-.423.135.758.758 0 1 0 .863 1.248.757.757 0 0 0 .193-1.055.758.758 0 0 0-.633-.328zm15.994 2.37a.842.842 0 0 0-.47.151.845.845 0 1 0 1.175.215.845.845 0 0 0-.705-.365zm-8.15 1.028c.063 0 .124.005.182.014a.901.901 0 0 1 .45.187c.169.134.273.241.432.393.24.227.414.089.534.02.208-.122.369-.219.984-.208.633.011 1.363.237 1.514 1.317.168 1.199-1.966 4.289-1.817 5.722.106 1.01 1.815.299 1.96 1.22.186 1.198-2.136.753-2.667.493-.832-.408-1.337-1.34-1.12-2.26.16-.688 1.7-3.498 1.757-3.93.059-.44-.177-.476-.324-.484-.19-.01-.34.081-.526.362-.169.255-2.082 4.085-2.248 4.398-.296.56-.67.694-1.044.674-.548-.029-.798-.32-.72-.848.047-.31 1.26-3.049 1.323-3.476.039-.265-.013-.546-.275-.68-.263-.135-.572.07-.664.227-.128.215-1.848 4.706-2.032 5.038-.316.576-.65.76-1.152.784-1.186.056-2.065-.92-1.678-2.116.173-.532 1.316-4.571 1.895-5.599.389-.69 1.468-1.216 2.217-.892.387.167.925.437 1.084.507.366.163.759-.277.913-.412.155-.134.302-.276.49-.357.142-.06.343-.095.532-.094zm10.88 2.057a.468.468 0 0 0-.093.011.467.467 0 0 0-.36.555.47.47 0 0 0 .557.36.47.47 0 0 0 .36-.557.47.47 0 0 0-.464-.37zm-22.518.81a.997.997 0 0 0-.832.434 1 1 0 1 0 1.39-.258 1 1 0 0 0-.558-.176zm21.294 2.094a.635.635 0 0 0-.127.013.627.627 0 0 0-.48.746.628.628 0 0 0 .746.483.628.628 0 0 0 .482-.746.63.63 0 0 0-.621-.496zm-18.24 6.097a.453.453 0 0 0-.092.012.464.464 0 1 0 .195.908.464.464 0 0 0 .356-.553.465.465 0 0 0-.459-.367zm13.675 1.55a1.044 1.044 0 0 0-.583.187 1.047 1.047 0 1 0 1.456.265 1.044 1.044 0 0 0-.873-.451zM11.4 22.154a.643.643 0 0 0-.36.115.646.646 0 0 0-.164.899.646.646 0 0 0 .899.164.646.646 0 0 0 .164-.898.646.646 0 0 0-.54-.28z",
    "facebook": "M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z",
    "map-pin": "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z",
}

PLATFORM_ORDER = ["website", "github", "mastodon", "bluesky", "linkedin", "youtube", "x", "instagram", "meetup", "facebook"]


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_json_files(path):
    entries = []
    if not os.path.exists(path):
        return entries
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".json"):
            with open(os.path.join(path, filename), encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                entries.extend(data)
            else:
                entries.append(data)
    return entries


def build_social_url(platform, handle):
    if not handle:
        return None
    handle = handle.strip()
    handle = urllib.parse.unquote(handle)
    if platform not in ("mastodon", "bluesky"):
        handle = handle.lstrip("@")
    if platform == "x":
        return handle if handle.startswith("http") else f"https://x.com/{handle}"
    if platform == "mastodon":
        if handle.startswith("http"):
            return handle
        parts = handle.lstrip("@").split("@")
        return f"https://{parts[1]}/@{parts[0]}" if len(parts) == 2 else None
    if platform == "linkedin":
        if handle.startswith("http"):
            return handle
        if handle.startswith(("in/", "company/")):
            return f"https://www.linkedin.com/{handle.rstrip('/')}"
        return f"https://www.linkedin.com/in/{handle.rstrip('/')}"
    if platform == "github":
        return handle if handle.startswith("http") else f"https://github.com/{handle}"
    if platform == "youtube":
        if handle.startswith("http"):
            return handle
        return f"https://www.youtube.com/{handle}" if handle.startswith("@") else f"https://www.youtube.com/user/{handle}"
    if platform == "website":
        return handle if handle.startswith("http") else f"http://{handle}"
    if platform == "bluesky":
        return handle if handle.startswith("http") else f"https://bsky.app/profile/{handle.lstrip('@')}"
    if platform == "instagram":
        return handle if handle.startswith("http") else f"https://instagram.com/{handle.lstrip('@')}"
    if platform == "meetup":
        return handle if handle.startswith("http") else f"https://www.meetup.com/{handle}"
    if platform == "facebook":
        return handle if handle.startswith("http") else f"https://facebook.com/{handle}"
    return None


def social_icon_svg(platform, size=14):
    path = SVG_PATHS.get(platform)
    if not path:
        return ""
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="currentColor" aria-hidden="true"><path d="{path}"/></svg>'
    )


def render_social_icons_html(social_dict, size=14):
    icons = []
    for platform in PLATFORM_ORDER:
        handle = social_dict.get(platform)
        url = build_social_url(platform, handle)
        if not url:
            continue
        svg = social_icon_svg(platform, size)
        if svg:
            icons.append(f'<a href="{escape(url)}" target="_blank" rel="noopener" title="{platform}" class="social-icon" onclick="event.stopPropagation()">{svg}</a>')
    return "\n".join(icons)


FALLBACK_IMAGES = [
    "https://github.com/cosimameyer/awesome-pyladies-creations/raw/main/img/fallback_images/pyladies_bot.png",
    "https://github.com/cosimameyer/awesome-pyladies-creations/raw/main/img/fallback_images/pyladies_small.png",
]

def avatar_fallback(name):
    # stable hash so adding more images to FALLBACK_IMAGES rotates evenly
    import hashlib
    idx = int(hashlib.md5(name.encode()).hexdigest(), 16) % len(FALLBACK_IMAGES)
    return FALLBACK_IMAGES[idx]


TAG_CLASS = {
    "blog": "tag-blog", "youtube": "tag-youtube",
    "podcast": "tag-podcast", "package": "tag-package",
}
TYPE_LABEL = {
    "blog": "Blog", "youtube": "YouTube",
    "podcast": "Podcast", "package": "Package",
}
BADGE_CLASS = {
    "blog": "badge-blog", "youtube": "badge-youtube", "podcast": "badge-podcast",
}


def badge_class(content_type):
    return BADGE_CLASS.get(content_type, "badge-blog")


def type_label(content_type):
    return TYPE_LABEL.get(content_type, content_type.title())


# ── Person registry ────────────────────────────────────────────────────────────

class PersonProfile:
    def __init__(self):
        self.types          = []   # ordered, deduplicated list of type strings
        self.social         = {}   # merged {platform: handle}, first value wins per platform
        self.url            = ""   # primary link (first content entry > first package)
        self.photo_url      = ""   # first non-empty photo URL
        self.content_entries = []  # [(type, url), ...] for badge links


def build_person_registry(content_data, all_package_data, member_data=None, chapter_names=None):
    """
    Walk every member file, content entry, and package, collecting each person's
    types, social handles, primary URL, photo, and content_entries.

    Member files (data/members/) are the authoritative source — their photo and
    social handles override anything found in content/package entries, mirroring
    how data/chapters/ files take precedence over synthesised chapter data.

    Content entries and packages add types, content_entries, and primary URL;
    social handles from those sources only fill platforms absent from the member file.

    chapter_names: set of chapter names to exclude from the people registry.
    """
    registry = {}
    chapter_names = chapter_names or set()
    # Track which names come from member files so content entries don't override them.
    member_names = set()

    def merge_social(profile, social_media_list, override=False):
        for sm in social_media_list:
            for platform, handle in sm.items():
                if handle and (override or platform not in profile.social):
                    profile.social[platform] = handle

    # 1. Seed registry from member files — these are authoritative.
    for member in (member_data or []):
        name = member.get("name", "").strip()
        if not name:
            continue
        if name not in registry:
            registry[name] = PersonProfile()
        p = registry[name]
        # Member file wins for photo and social (override=True)
        if member.get("photo_url"):
            p.photo_url = member["photo_url"]
        merge_social(p, member.get("social_media", []), override=True)
        member_names.add(name)

    # 2. Enrich from content entries; member-file values are not overwritten.
    for entry in content_data:
        ctype = entry.get("type", "blog")
        entry_url = entry.get("url", "#")
        for author in entry.get("authors", []):
            name = author.get("name", "")
            if not name or author.get("pyladies") is False:
                continue
            if name in chapter_names:
                continue
            if name not in registry:
                registry[name] = PersonProfile()
            p = registry[name]
            if ctype not in p.types:
                p.types.append(ctype)
            p.content_entries.append((ctype, entry_url))
            if not p.url:
                p.url = entry_url
            if not p.photo_url:
                p.photo_url = entry.get("photo_url", "")
            merge_social(p, author.get("social_media", []))

    # 3. Enrich from packages.
    for pkg in all_package_data:
        pkg_url = pkg.get("pypi_url") or pkg.get("repo_url") or pkg.get("website_url") or "#"
        for m in pkg.get("maintainers", []):
            name = m.get("name", "")
            if not name or m.get("pyladies") is False:
                continue
            if name not in registry:
                registry[name] = PersonProfile()
            p = registry[name]
            if "package" not in p.types:
                p.types.append("package")
            p.content_entries.append(("package", pkg_url))
            if not p.url:
                p.url = pkg_url
            merge_social(p, m.get("social_media", []))

    # 4. For member-only people (no content/package entries), derive a primary URL
    #    from their social handles so the card is still clickable.
    for name in member_names:
        p = registry[name]
        if not p.url:
            for platform in ("website", "github", "linkedin", "twitter", "bluesky"):
                handle = p.social.get(platform)
                if handle:
                    p.url = build_social_url(platform, handle) or ""
                    if p.url:
                        break

    return registry


# ── Card renderers ─────────────────────────────────────────────────────────────

def render_person_card(name, profile):
    fallback = avatar_fallback(name)
    photo_src = escape(profile.photo_url) if profile.photo_url else fallback
    social_html = render_social_icons_html(profile.social)
    data_types = " ".join(profile.types)
    # Build type badges as <a> links — one per type, pointing to first matching content entry
    type_urls = {}
    for ctype, curl in profile.content_entries:
        if ctype not in type_urls:
            type_urls[ctype] = curl
    tags_html = "".join(
        f'<a href="{escape(type_urls.get(t, profile.url))}" target="_blank" rel="noopener" '
        f'class="person-tag {TAG_CLASS.get(t, "tag-blog")}" '
        f'onclick="event.stopPropagation()">{TYPE_LABEL.get(t, t.title())}</a>'
        for t in profile.types
    )
    url = escape(profile.url)
    search_text = escape(name.lower())
    # div wrapper avoids invalid <a> inside <a> (social icon links inside card link)
    return f"""
        <div class="person-card" data-type="{escape(data_types)}" data-search="{search_text}"
             onclick="window.open('{url}','_blank','noopener')" role="link" tabindex="0"
             onkeydown="if(event.key==='Enter')window.open('{url}','_blank','noopener')">
          <img class="person-avatar" src="{photo_src}" alt="{escape(name)}" loading="lazy"
               onerror="this.src='{fallback}'"/>
          <div class="person-info">
            <h3 class="person-name">{escape(name)}</h3>
            <div class="person-tags">{tags_html}</div>
          </div>
          <div class="person-social">{social_html}</div>
        </div>"""


def render_content_card(entry, registry=None):
    title       = escape(entry.get("title", "Untitled"))
    raw_url     = entry.get("url", "#")
    url         = escape(raw_url)
    raw_photo   = entry.get("photo_url", "")
    ctype       = entry.get("type", "blog").lower()
    badge       = badge_class(ctype)
    label       = type_label(ctype)
    description = escape(entry.get("description") or entry.get("subtitle") or "")
    language    = escape((entry.get("language") or "en").upper())
    raw_title   = entry.get("title", "")
    raw_desc    = entry.get("description") or entry.get("subtitle") or ""
    authors     = entry.get("authors", [])
    author_names = ", ".join(a.get("name", "") for a in authors if a.get("name"))
    author_html = f'<p class="content-author">by {escape(author_names)}</p>' if author_names else ""
    search_text = escape(f"{raw_title} {raw_desc} {author_names}".lower())
    fallback    = avatar_fallback(raw_title)
    photo_src   = escape(raw_photo) if raw_photo else fallback

    # Collect social icons for each author from the registry.
    # For podcasts, only show the primary author (marked with "primary": true, or the
    # first author as fallback) so the tile isn't cluttered with every host's icons.
    social_icons_html = ""
    if registry:
        icons = []
        seen_authors = set()
        if ctype == "podcast":
            primary = next((a for a in authors if a.get("primary")), authors[0] if authors else None)
            display_authors = [primary] if primary else []
        else:
            display_authors = authors
        for author in display_authors:
            name = author.get("name", "")
            if not name or name in seen_authors:
                continue
            seen_authors.add(name)
            profile = registry.get(name)
            if profile and profile.social:
                icons.append(render_social_icons_html(profile.social, size=13))
        if icons:
            social_icons_html = f'<div class="content-card-social">{"".join(icons)}</div>'

    return f"""
        <div class="content-card" data-type="{ctype}" data-search="{search_text}"
             onclick="window.open('{url}','_blank','noopener')" role="link" tabindex="0"
             onkeydown="if(event.key==='Enter')window.open('{url}','_blank','noopener')">
          <div class="content-card-header">
            <img class="content-thumb" src="{photo_src}" alt="" loading="lazy"
                 onerror="this.src='{fallback}'"/>
            <span class="content-type-badge {badge}">{label}</span>
          </div>
          <div class="content-card-body">
            <h3>{title}</h3>
            {author_html}
            <p>{description}</p>
          </div>
          <div class="content-card-footer">
            <span class="lang-badge">{language}</span>
            {social_icons_html}
            <span class="arrow">→</span>
          </div>
        </div>"""


def render_package_card(pkg):
    name        = pkg.get("name", "")
    title       = escape(pkg.get("title") or name)
    description = escape(pkg.get("description", ""))
    pypi_url    = escape(pkg.get("pypi_url", "#"))
    repo_url    = escape(pkg.get("repo_url", "#"))
    docs_url    = pkg.get("docs_url") or ""
    logo_url    = pkg.get("logo_url") or ""
    maintainers = pkg.get("maintainers", [])
    maintainer_names = ", ".join(m.get("name", "") for m in maintainers[:3])
    if len(maintainers) > 3:
        maintainer_names += f" + {len(maintainers) - 3} others"
    maintainer_names = escape(maintainer_names)

    logo_html = (
        f'<img class="package-logo" src="{escape(logo_url)}" alt="{title} logo" loading="lazy" onerror="this.style.display=\'none\'"/>'
        if logo_url else
        f'<div class="package-logo-placeholder">{escape(name[:2].upper())}</div>'
    )

    # Suppress docs link only when it points to the same URL as pypi_url
    _pypi_url = (pkg.get("pypi_url") or "").rstrip("/")
    _docs_url = docs_url.rstrip("/")
    docs_link = (
        f'<a href="{escape(docs_url)}" class="pkg-link" title="Docs" target="_blank" rel="noopener">'
        f'{social_icon_svg("website")}</a>'
        if docs_url and _docs_url != _pypi_url else ""
    )

    raw_name  = pkg.get("title") or pkg.get("name", "")
    raw_desc  = pkg.get("description", "")
    raw_maint = " ".join(m.get("name", "") for m in maintainers)
    search_text = escape(f"{raw_name} {raw_desc} {raw_maint}".lower())
    # div wrapper avoids invalid <a> inside <a> (pkg-link anchors inside card link)
    return f"""
        <div class="package-card" data-search="{search_text}"
             onclick="window.open('{pypi_url}','_blank','noopener')"
             role="link" tabindex="0"
             onkeydown="if(event.key==='Enter')window.open('{pypi_url}','_blank','noopener')">
          <div class="package-card-top">
            {logo_html}
            <div class="package-links">
              {docs_link}
              <a href="{repo_url}" class="pkg-link" title="GitHub" target="_blank" rel="noopener"
                 onclick="event.stopPropagation()">{social_icon_svg("github")}</a>
              <a href="{pypi_url}" class="pkg-link" title="PyPI" target="_blank" rel="noopener"
                 onclick="event.stopPropagation()">{social_icon_svg("pypi")}</a>
            </div>
          </div>
          <h3 class="package-name">{title}</h3>
          <p class="package-desc">{description}</p>
          <div class="package-maintainers">
            <span class="maintainer-label">Maintained by</span>
            <span class="maintainers">{maintainer_names}</span>
          </div>
        </div>"""


def render_chapter_card(chapter, content_entry=None):
    name     = escape(chapter.get("name", ""))
    city     = escape(chapter.get("city", ""))
    country  = escape(chapter.get("country", ""))
    location = f"{city}, {country}" if city and country else city or country
    raw_sm = chapter.get("social_media") or []
    if isinstance(raw_sm, list):
        social = {}
        for sm in raw_sm:
            social.update(sm)
    else:
        social = dict(raw_sm)
    # Merge social links from the paired content entry (chapter data takes precedence)
    if content_entry:
        for author in content_entry.get("authors", []):
            for sm in author.get("social_media", []):
                for k, v in sm.items():
                    if k not in social:
                        social[k] = v
    website  = escape(chapter.get("website", "") or social.get("website", "") or "")

    # If this chapter has content, use the content URL as primary click target
    ctype = content_entry.get("type", "blog") if content_entry else None
    content_url = content_entry.get("url", "") if content_entry else ""
    url   = content_url or website or "#"
    search_text = escape(f"{chapter.get('name','')} {city} {country}".lower())

    # Build social icons — chapters store full URLs directly
    icon_html = []
    for platform in ["website", "github", "linkedin", "twitter", "instagram", "meetup", "facebook", "youtube", "mastodon", "bluesky"]:
        raw = social.get(platform) or (chapter.get("website") if platform == "website" else None)
        if not raw:
            continue
        link_url = build_social_url(platform, raw)
        if not link_url:
            continue
        svg = social_icon_svg(platform, 14)
        if svg:
            icon_html.append(
                f'<a href="{escape(link_url)}" target="_blank" rel="noopener" '
                f'title="{platform}" class="social-icon" onclick="event.stopPropagation()">{svg}</a>'
            )

    photo_url     = escape(chapter.get("photo_url", ""))
    pin_svg       = social_icon_svg("map-pin", 14)
    onclick_attr  = f' onclick="window.open(\'{url}\',\'_blank\',\'noopener\')"' if url != "#" else ""
    role_attr     = ' role="link" tabindex="0"' if url != "#" else ""
    social_joined = "".join(icon_html)
    logo_html     = f'<div class="chapter-logo-wrap"><img class="chapter-logo" src="{photo_url}" alt="{name} logo" loading="lazy" onerror="this.style.display=\'none\'"></div>' if photo_url else ""
    badge_html    = f'<span class="person-tag {badge_class(ctype)}">{type_label(ctype)}</span>' if ctype else ""
    return f"""
        <div class="chapter-card" data-search="{search_text}"{role_attr}{onclick_attr}>
          {logo_html}
          <div class="chapter-card-header">
            <span class="chapter-pin">{pin_svg}</span>
            <span class="chapter-location">{escape(location)}</span>
          </div>
          <h3 class="chapter-name">{name}</h3>
          {badge_html}
          <div class="chapter-social">{social_joined}</div>
        </div>"""


# ── Region grouping ────────────────────────────────────────────────────────────

REGION_ORDER = ["Africa", "Asia", "Europe", "Global", "Latin America", "North America", "Oceania"]

COUNTRY_TO_REGION = {
    # North America
    "USA": "North America", "Canada": "North America", "Mexico": "North America",
    # Latin America
    "Brazil": "Latin America", "Bolivia": "Latin America", "Chile": "Latin America",
    "Ecuador": "Latin America", "Guatemala": "Latin America", "Panama": "Latin America",
    "Peru": "Latin America", "Uruguay": "Latin America",
    # Europe
    "Albania": "Europe", "Austria": "Europe", "Belgium": "Europe",
    "Bosnia and Herzegovina": "Europe", "Czech Republic": "Europe", "Finland": "Europe",
    "France": "Europe", "Germany": "Europe", "Greece": "Europe", "Ireland": "Europe",
    "Italy": "Europe", "Kosovo": "Europe", "Norway": "Europe", "Poland": "Europe",
    "Portugal": "Europe", "Russia": "Europe", "Scotland": "Europe", "Slovakia": "Europe",
    "Spain": "Europe", "Sweden": "Europe", "Turkey": "Europe", "United Kingdom": "Europe",
    # Africa
    "Ethiopia": "Africa", "Ghana": "Africa", "Liberia": "Africa", "Madagascar": "Africa",
    "Morocco": "Africa", "Mozambique": "Africa", "Nigeria": "Africa", "Tunisia": "Africa",
    "Uganda": "Africa",
    # Asia
    "India": "Asia", "Indonesia": "Asia", "Japan": "Asia", "Malaysia": "Asia",
    "Singapore": "Asia", "South Korea": "Asia", "Taiwan": "Asia", "Vietnam": "Asia",
    # Oceania
    "Australia": "Oceania",
    # Global
    "Everywhere": "Global",
}


def chapter_region(chapter):
    return COUNTRY_TO_REGION.get(chapter.get("country", ""), "Global")


def group_chapters_by_region(chapters_data):
    groups = {r: [] for r in REGION_ORDER}
    for c in chapters_data:
        groups[chapter_region(c)].append(c)
    return groups


# ── Counts & stats ─────────────────────────────────────────────────────────────

FEATURED_PEOPLE   = 10
FEATURED_CONTENT  = 9
FEATURED_PACKAGES = 6


def count_unique_people(content_data, package_data):
    names = set()
    for e in content_data:
        for a in e.get("authors", []):
            names.add(a.get("name", ""))
    for p in package_data:
        for m in p.get("maintainers", []):
            names.add(m.get("name", ""))
    names.discard("")
    return len(names)


def build_stats_html(n_people, n_blogs, n_youtube, n_podcasts, n_packages, n_chapters=0):
    items = [
        (f"{n_people}+", "Creators"),
        (n_chapters,      "Chapters"),
        (n_blogs,         "Blogs"),
        (n_youtube,       "YouTube"),
        (n_podcasts,      "Podcasts"),
        (n_packages,      "Packages"),
    ]
    parts = []
    for num, label in items:
        if num == 0:
            continue
        if parts:
            parts.append('<div class="stat-divider"></div>')
        parts.append(f'<div class="stat"><span class="stat-num">{num}</span><span class="stat-label">{label}</span></div>')
    return "".join(parts)


# ── Wordmark ────────────────────────────────────────────────────────────────────

_WORDMARK_PATH = os.path.join(ROOT, "docs", "assets", "pyladies_wordmark.svg")

def hero_wordmark_html(color="#EE264D"):
    """
    Read the locally stored PyLadies wordmark SVG, replace all fills with the
    brand color, and return it as an inline SVG with positioning styles applied.
    Falls back to an <img> tag if the file is missing.
    """
    if not os.path.exists(_WORDMARK_PATH):
        return '<img src="assets/pyladies_wordmark.svg" alt="PyLadies" class="hero-wordmark" />'

    with open(_WORDMARK_PATH, encoding="utf-8") as f:
        svg = f.read()

    # Replace only non-black fills with the brand red (preserves black outline/shadow)
    def recolor(m):
        h = m.group(1).lstrip('#')
        h = (h[0]*2 + h[1]*2 + h[2]*2) if len(h) == 3 else h  # expand shorthand
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return m.group(0) if r < 40 and g < 40 and b < 40 else f'fill:{color}'
    svg = re.sub(r'fill:(#[0-9a-fA-F]{3,6})', recolor, svg)

    # Add viewBox from the existing width/height so CSS scaling preserves aspect ratio
    w_m = re.search(r'\bwidth="([^"]+)"', svg)
    h_m = re.search(r'\bheight="([^"]+)"', svg)
    if w_m and h_m and 'viewBox' not in svg:
        svg = re.sub(r'(<svg\b)', rf'\1 viewBox="0 0 {w_m.group(1)} {h_m.group(1)}"', svg, count=1)

    # Remove presentational width/height so our CSS height+auto-width scales correctly
    svg = re.sub(r'\s*\bwidth="[^"]*"', '', svg, count=1)
    svg = re.sub(r'\s*\bheight="[^"]*"', '', svg, count=1)

    # Add the CSS class so sizing is controlled entirely by style.css
    our_style = (
        "width:auto;display:block;"
        "margin:-28px auto 12px;"
        "transform:rotate(-15deg);"
        "transform-origin:center bottom;"
    )
    # Merge with any existing style attribute rather than adding a duplicate
    if re.search(r'<svg\b[^>]*style=', svg, re.DOTALL):
        svg = re.sub(r'(style=")([^"]*)"', lambda m: f'style="{our_style}{m.group(2)}"', svg, count=1)
    else:
        svg = re.sub(r'(<svg\b)', rf'\1 style="{our_style}"', svg, count=1)
    # Add hero-wordmark class so CSS can control height responsively
    svg = re.sub(r'(<svg\b)', r'\1 class="hero-wordmark"', svg, count=1)
    return svg


# ── Shared page chrome ─────────────────────────────────────────────────────────

def nav_html(css_path="assets/style.css", home="index.html", active="", extra_head="", title="Awesome PyLadies"):
    gh_svg = social_icon_svg("github", 16)
    def nav_link(href, label, key):
        cls = ' class="nav-active"' if active == key else ""
        return f'<li><a href="{href}"{cls}>{label}</a></li>'
    favicon_path = css_path.replace("style.css", "pylady_geek.png")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="icon" type="image/png" href="{favicon_path}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="A curated directory of chapters, content, tools, and packages created by PyLadies members." />
  <meta property="og:image" content="{favicon_path}" />
  <link rel="stylesheet" href="{css_path}" />
  {extra_head}
</head>
<body>
  <header class="site-header">
    <nav class="nav-inner">
      <a href="{home}" class="nav-logo">
        <img src="assets/pylady_geek.png"
             alt="PyLadies geek logo" class="nav-geek-logo" />
        <span>Awesome PyLadies</span>
      </a>
      <ul class="nav-links">
        {nav_link("people.html", "People", "people")}
        {nav_link("chapters.html", "Chapters", "chapters")}
        {nav_link("content.html", "Content", "content")}
        {nav_link("packages.html", "Packages", "packages")}
        {nav_link("about.html", "About", "about")}
      </ul>
      <a class="nav-cta" href="https://github.com/cosimameyer/awesome-pyladies-creations" target="_blank" rel="noopener">
        {gh_svg} Contribute
      </a>
      <button class="nav-hamburger" aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </header>
  <script>
    (function() {{
      var btn = document.querySelector('.nav-hamburger');
      var links = document.querySelector('.nav-links');
      if (!btn || !links) return;
      btn.addEventListener('click', function() {{
        var open = links.classList.toggle('nav-open');
        btn.setAttribute('aria-expanded', open);
      }});
    }})();
  </script>"""


def footer_html(updated):
    return f"""
  <section class="cta-section">
    <div class="container cta-inner">
      <h2>Are you a PyLady?</h2>
      <p>Add your blog, package, YouTube channel, or other work to the directory — it takes just one JSON file.</p>
      <a href="contribute.html" class="btn-primary">Read the Contributing Guide</a>
    </div>
  </section>
  <footer class="site-footer">
    <div class="container footer-inner">
      <span>Built from <a href="https://github.com/cosimameyer/awesome-pyladies-creations" target="_blank" rel="noopener">awesome-pyladies-creations</a> · CC0 · updated {updated}</span>
    </div>
  </footer>
</body>
</html>"""


def search_bar_html(placeholder="Search…"):
    return f"""
      <div class="search-wrap">
        <input class="search-input" type="search" placeholder="{placeholder}" aria-label="{placeholder}" />
      </div>"""


# ── Shared JS blocks ────────────────────────────────────────────────────────────

JS_PEOPLE = """
  <script>
    function applyPeopleFilters() {
      const q = (document.querySelector('.search-input')?.value || '').toLowerCase();
      const f = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
      document.querySelectorAll('.person-card').forEach(card => {
        const typeMatch = f === 'all' || card.dataset.type.split(' ').includes(f);
        const textMatch = !q || card.dataset.search.includes(q);
        card.style.display = (typeMatch && textMatch) ? '' : 'none';
      });
    }
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyPeopleFilters();
      });
    });
    document.querySelector('.search-input')?.addEventListener('input', applyPeopleFilters);
  </script>"""

JS_CONTENT = """
  <script>
    function applyContentFilters() {
      const q = (document.querySelector('.search-input')?.value || '').toLowerCase();
      const f = document.querySelector('.tab.active')?.dataset.tab || 'all';
      document.querySelectorAll('.content-card').forEach(card => {
        const typeMatch = f === 'all' || card.dataset.type === f;
        const textMatch = !q || card.dataset.search.includes(q);
        card.style.display = (typeMatch && textMatch) ? '' : 'none';
      });
    }
    document.querySelectorAll('.tab').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyContentFilters();
      });
    });
    document.querySelector('.search-input')?.addEventListener('input', applyContentFilters);
  </script>"""

JS_PACKAGES = """
  <script>
    document.querySelector('.search-input')?.addEventListener('input', function() {
      const q = this.value.toLowerCase();
      document.querySelectorAll('.package-card').forEach(card => {
        card.style.display = (!q || card.dataset.search.includes(q)) ? '' : 'none';
      });
    });
  </script>"""

JS_CHAPTERS_SEARCH = """
  <script>
    document.querySelector('.search-input')?.addEventListener('input', function() {
      const q = this.value.toLowerCase();
      document.querySelectorAll('.chapter-region-group').forEach(group => {
        let anyVisible = false;
        group.querySelectorAll('.chapter-card').forEach(card => {
          const show = !q || card.dataset.search.includes(q);
          card.style.display = show ? '' : 'none';
          if (show) anyVisible = true;
        });
        group.style.display = anyVisible ? '' : 'none';
      });
    });

    (function() {
      var toc = document.querySelector('.chapters-toc');
      if (!toc) return;
      var groups = Array.from(document.querySelectorAll('.chapter-region-group'));
      var links = {};
      toc.querySelectorAll('a').forEach(function(a) { links[a.getAttribute('href').slice(1)] = a; });
      var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) {
          var link = links[e.target.id];
          if (link) link.classList.toggle('toc-active', e.isIntersecting);
        });
      }, {rootMargin: '-10% 0px -70% 0px'});
      groups.forEach(function(g) { observer.observe(g); });
    })();
  </script>"""


def js_chapters_map(chapters_data):
    markers = []
    for c in chapters_data:
        lat = c.get("lat")
        lon = c.get("lon")
        if lat is None or lon is None:
            continue
        name = c.get("name", "").replace("'", "\\'").replace('"', '\\"')
        city = c.get("city", "").replace("'", "\\'")
        country = c.get("country", "").replace("'", "\\'")
        # Best URL: website field, then website from social_media list
        website = c.get("website", "")
        if not website:
            raw_sm = c.get("social_media") or []
            sm = {}
            if isinstance(raw_sm, list):
                for d in raw_sm:
                    sm.update(d)
            else:
                sm = dict(raw_sm)
            website = sm.get("website", "")
        url = escape(website) if website else ""
        search = f"{name} {city} {country}".lower().replace("'", "\\'")
        markers.append(f"[{lat},{lon},'{name}','{url}','{search}']")
    markers_js = ",\n      ".join(markers)
    return f"""
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    (function() {{
      var map = L.map('chapters-map', {{scrollWheelZoom: false}}).setView([20, 10], 2);
      L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        maxZoom: 19
      }}).addTo(map);
      var dot = L.divIcon({{className:'', html:'<div class="map-dot"></div>', iconSize:[12,12], iconAnchor:[6,6]}});
      var pts = [
        {markers_js}
      ];
      var markers_list = [];
      pts.forEach(function(p) {{
        var m = L.marker([p[0],p[1]], {{icon: dot, _search: p[4]}}).addTo(map);
        var popup = p[3]
          ? '<a href="' + p[3] + '" target="_blank" rel="noopener" style="font-weight:600;color:#EE264D">' + p[2] + '</a>'
          : '<span style="font-weight:600">' + p[2] + '</span>';
        m.bindPopup(popup);
        markers_list.push(m);
      }});
      var chapterSearch = document.querySelector('.search-input');
      if (chapterSearch) {{
        chapterSearch.addEventListener('input', function() {{
          var q = this.value.toLowerCase().trim();
          markers_list.forEach(function(m) {{
            var show = !q || (m.options._search || '').includes(q);
            if (show) {{ m.addTo(map); }} else {{ m.remove(); }}
          }});
        }});
      }}
    }})();
  </script>"""


# ── Section builders ────────────────────────────────────────────────────────────

def section_people_full(people_cards, n_podcasts):
    podcast_btn = "<button class='filter-btn' data-filter='podcast'>Podcasters</button>" if n_podcasts else ""
    return f"""
  <section class="section" id="people">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">Community</p>
          <h2 class="section-title">The People</h2>
        </div>
        <p class="section-desc">PyLadies members sharing knowledge, code, and passion with the world.</p>
      </div>
      {search_bar_html("Search by name…")}
      <div class="filter-bar">
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="blog">Bloggers</button>
        <button class="filter-btn" data-filter="youtube">YouTubers</button>
        {podcast_btn}
        <button class="filter-btn" data-filter="package">Package Maintainers</button>
      </div>
      <div class="people-grid">{"".join(people_cards)}</div>
    </div>
  </section>"""


def section_content_full(content_cards, n_podcasts):
    podcast_tab = "<button class='tab' data-tab='podcast'>Podcasts</button>" if n_podcasts else ""
    return f"""
  <section class="section section-alt" id="content">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">Reading &amp; Watching</p>
          <h2 class="section-title">Content</h2>
        </div>
        <p class="section-desc">Blogs, YouTube channels, and podcasts produced by PyLadies members.</p>
      </div>
      {search_bar_html("Search blogs and channels…")}
      <div class="tabs">
        <button class="tab active" data-tab="all">All</button>
        <button class="tab" data-tab="blog">Blogs</button>
        <button class="tab" data-tab="youtube">YouTube</button>
        {podcast_tab}
      </div>
      <div class="content-grid">{"".join(content_cards)}</div>
    </div>
  </section>"""


def section_packages_full(package_cards):
    return f"""
  <section class="section" id="packages">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">Open Source</p>
          <h2 class="section-title">Packages &amp; Tools</h2>
        </div>
        <p class="section-desc">Python packages and software built and maintained by PyLadies members.</p>
      </div>
      {search_bar_html("Search packages…")}
      <div class="packages-grid">{"".join(package_cards)}</div>
    </div>
  </section>"""


def region_slug(region):
    return "region-" + region.lower().replace(" ", "-")


def section_chapters_full(chapter_groups, chapter_content_map=None, chapters_data=None):
    has_map = bool(chapters_data)
    map_block = '<div id="chapters-map"></div>' if has_map else ""
    content_map = chapter_content_map or {}
    groups_html = []
    toc_items = []
    for region in REGION_ORDER:
        cards = chapter_groups.get(region, [])
        if not cards:
            continue
        slug = region_slug(region)
        card_html = "".join(render_chapter_card(c, content_map.get(c.get("name", ""))) for c in cards)
        groups_html.append(f"""
      <div class="chapter-region-group" id="{slug}" data-region="{region}">
        <h3 class="chapter-region-label">{region}</h3>
        <div class="chapters-grid">{card_html}</div>
      </div>""")
        toc_items.append(f'<a href="#{slug}">{region}</a>')
    toc_html = f'<nav class="chapters-toc">{"".join(toc_items)}</nav>'
    return f"""
  {toc_html}
  <section class="section section-alt" id="chapters">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">Global Community</p>
          <h2 class="section-title">PyLadies Chapters</h2>
        </div>
        <p class="section-desc">PyLadies chapters around the world — find your local community.</p>
      </div>
      {map_block}
      {search_bar_html("Search chapters by city or country…")}
      {"".join(groups_html)}
    </div>
  </section>"""


def section_featured(label, title, desc, cards, grid_class, view_all_href, section_id, alt_bg=False):
    bg = " section-alt" if alt_bg else ""
    return f"""
  <section class="section{bg}" id="{section_id}">
    <div class="container">
      <div class="section-header">
        <div>
          <p class="section-label">{label}</p>
          <h2 class="section-title">{title}</h2>
        </div>
        <p class="section-desc">{desc}</p>
      </div>
      <div class="{grid_class}">{"".join(cards)}</div>
      <div class="view-all-wrap">
        <a href="{view_all_href}" class="view-all-btn">View all →</a>
      </div>
    </div>
  </section>"""


def render_contributing_md():
    if not os.path.exists(CONTRIBUTING_MD):
        return "<p>Contributing guide not found.</p>", []
    with open(CONTRIBUTING_MD, encoding="utf-8") as f:
        src = f.read()
    converter = _md.Markdown(extensions=["fenced_code", "tables", "nl2br", "md_in_html", "toc"])
    html = converter.convert(src)
    # Python-Markdown doesn't render GitHub-style task lists as checkboxes;
    # replace the literal "[ ] " text with a styled list item class instead.
    html = html.replace("<li>[ ] ", '<li class="task-list-item"><span class="task-check" aria-hidden="true"></span>')
    html = html.replace("<li>[x] ", '<li class="task-list-item task-list-item--done"><span class="task-check task-check--done" aria-hidden="true"></span>')
    # Extract headings (h2 + h3) for TOC, preserving hierarchy
    toc_items = []
    for item in converter.toc_tokens:
        if item.get("id"):
            toc_items.append((item["id"], item["name"], False))
        for child in item.get("children", []):
            if child.get("id"):
                toc_items.append((child["id"], child["name"], True))
    return html, toc_items


def section_contribute():
    contributing_html, toc_items = render_contributing_md()
    toc_links = "".join(
        f'<a href="#{tid}" class="toc-sub">{name}</a>' if sub else f'<a href="#{tid}">{name}</a>'
        for tid, name, sub in toc_items
    )
    toc_html = f'<nav class="contribute-toc">{toc_links}</nav>' if toc_links else ""
    return f"""
  {toc_html}
  <section class="section" id="contribute">
    <div class="container contribute-wrap">

      <div class="section-header">
        <div>
          <p class="section-label">Get Involved</p>
          <h2 class="section-title">Contribute</h2>
        </div>
      </div>

      <div class="contribute-intro">
        <div class="contribute-card">
          <h3>Add your work</h3>
          <p>New to the directory? Follow the guide below to submit a blog, YouTube channel,
             podcast, Python package, or chapter in one JSON file.</p>
        </div>
        <div class="contribute-card">
          <h3>Edit an existing entry</h3>
          <p>Found a mistake or want to update your details? Every entry lives in a single
             JSON file. Find your file in
             <a href="https://github.com/cosimameyer/awesome-pyladies-creations/tree/main/data/content"
                target="_blank" rel="noopener"><code>data/content/</code></a>,
             <a href="https://github.com/cosimameyer/awesome-pyladies-creations/tree/main/data/packages"
                target="_blank" rel="noopener"><code>data/packages/</code></a>, or
             <a href="https://github.com/cosimameyer/awesome-pyladies-creations/tree/main/data/chapters"
                target="_blank" rel="noopener"><code>data/chapters/</code></a>,
             click the pencil icon on GitHub to edit it directly in your browser,
             and open a pull request — no local setup needed.</p>
        </div>
        <div class="contribute-card">
          <h3>Remove your entry</h3>
          <p>Prefer not to be listed?
             <a href="https://github.com/cosimameyer/awesome-pyladies-creations/issues/new"
                target="_blank" rel="noopener">Open an issue</a>
             or <a href="https://cosimameyer.com" target="_blank" rel="noopener">contact me directly</a>
             and I'll take care of it promptly.</p>
        </div>
      </div>

      <div class="contribute-body md-content">
        {contributing_html}
      </div>

    </div>
  </section>
  <script>
    (function() {{
      var toc = document.querySelector('.contribute-toc');
      if (!toc) return;
      var links = {{}};
      toc.querySelectorAll('a').forEach(function(a) {{
        var id = a.getAttribute('href').replace('#', '');
        if (id) links[id] = a;
      }});
      var headings = Array.from(document.querySelectorAll('.md-content h2, .md-content h3')).filter(function(h) {{ return h.id && links[h.id]; }});
      var observer = new IntersectionObserver(function(entries) {{
        entries.forEach(function(e) {{
          var link = links[e.target.id];
          if (link) link.classList.toggle('toc-active', e.isIntersecting);
        }});
      }}, {{rootMargin: '-10% 0px -70% 0px'}});
      headings.forEach(function(h) {{ observer.observe(h); }});
    }})();
  </script>"""


def section_about():
    return """
  <section class="section">
    <div class="container about-wrap">

      <div class="section-header">
        <div>
          <p class="section-label">About</p>
          <h2 class="section-title">About This Directory</h2>
        </div>
      </div>

      <div class="about-body">
        <h3>Where does this content come from?</h3>
        <p>
          Everything featured here is sourced from the open-source repository
          <a href="https://github.com/cosimameyer/awesome-pyladies-creations"
             target="_blank" rel="noopener">awesome-pyladies-creations</a> on GitHub.
          Each person is reached out to individually before being added — so while this is
          a personally maintained project, the list is community-driven at heart.
          The site rebuilds automatically whenever new entries are added, and more
          PyLadies members are joining all the time.
        </p>

        <h3>Want to add or update an entry?</h3>
        <p>
          If you're a PyLadies member and would like your work featured — or need to update
          or remove an existing entry — it only takes one JSON file.
          <a href="contribute.html" class="about-contribute-link">See the full guide →</a>
        </p>
      </div>

    </div>
  </section>"""


# ── Main ───────────────────────────────────────────────────────────────────────

FEATURED_CHAPTERS = 6


def main():
    content_data  = load_json_files(CONTENT_DIR)
    package_data  = load_json_files(PACKAGES_DIR)
    software_data = load_json_files(SOFTWARE_DIR)
    chapters_data = load_json_files(CHAPTERS_DIR)
    member_data   = load_json_files(MEMBERS_DIR)

    content_data.sort(key=lambda x: x.get("authors", [{}])[0].get("name", ""))
    package_data.sort(key=lambda x: x.get("name", ""))
    software_data.sort(key=lambda x: x.get("name", ""))
    chapters_data.sort(key=lambda x: x.get("name", ""))

    all_data = package_data + software_data

    n_blogs    = sum(1 for e in content_data if e.get("type") == "blog")
    n_youtube  = sum(1 for e in content_data if e.get("type") == "youtube")
    n_podcasts = sum(1 for e in content_data if e.get("type") == "podcast")
    n_packages = len(all_data)

    # Synthesize chapter entries from content entries marked "chapter": true
    # that don't yet have a corresponding file in data/chapters/.
    # This ensures chapters with a YouTube/blog entry show up in the chapters
    # section even before their dedicated chapter JSON is added.
    known_chapter_names = {c.get("name", "") for c in chapters_data}
    for entry in content_data:
        if not entry.get("chapter"):
            continue
        for a in entry.get("authors", []):
            aname = a.get("name", "")
            if not aname or aname in known_chapter_names:
                continue
            city = aname[9:].strip() if aname.lower().startswith("pyladies ") else ""
            synth = {
                "name":       aname,
                "city":       city,
                "country":    entry.get("country", ""),
                "photo_url":  entry.get("photo_url", ""),
                "social_media": a.get("social_media", []),
                "website":    "",
            }
            if entry.get("lat") is not None:
                synth["lat"] = entry["lat"]
            if entry.get("lon") is not None:
                synth["lon"] = entry["lon"]
            chapters_data.append(synth)
            known_chapter_names.add(aname)

    n_chapters = len(chapters_data)

    # Build chapter name set and content map for cross-referencing.
    # Content entries marked "chapter": true must not appear in the people registry.
    chapter_names = {c.get("name", "") for c in chapters_data}
    chapter_names.discard("")

    chapter_content_map = {}
    for entry in content_data:
        for author in entry.get("authors", []):
            aname = author.get("name", "")
            if aname in chapter_names:
                chapter_content_map[aname] = entry

    registry = build_person_registry(content_data, all_data, member_data=member_data, chapter_names=chapter_names)
    n_people   = len(registry)  # count after pyladies:false filter is applied
    registry_sorted = sorted(registry.items(), key=lambda kv: kv[0])

    all_people_cards  = [render_person_card(n, p) for n, p in registry_sorted]
    all_content_cards = [render_content_card(e, registry=registry) for e in content_data]
    all_package_cards = [render_package_card(p) for p in all_data]
    all_chapter_cards = [render_chapter_card(c, chapter_content_map.get(c.get("name", ""))) for c in chapters_data]
    chapter_groups    = group_chapters_by_region(chapters_data)

    # Pass all cards — JS on the index page will randomly pick N to show on each load

    stats = build_stats_html(n_people, n_blogs, n_youtube, n_podcasts, n_packages, n_chapters)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    gh_svg = social_icon_svg("github", 16)

    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)

    # ── index.html ────────────────────────────────────────────────────────────
    index = nav_html(active="") + f"""
  <section class="hero">
    <div class="hero-inner">
      <div class="hero-badge">Open Source · Community · Python</div>
      <h1>Awesome</h1>
      {hero_wordmark_html()}
      <p class="hero-sub">A curated directory of chapters, content, tools, and packages created by PyLadies members — celebrating their voices and work in the Python ecosystem.</p>
      <div class="hero-stats">{stats}</div>
      <div class="hero-actions">
        <a href="people.html" class="btn-primary">Explore the Directory</a>
        <a href="https://github.com/cosimameyer/awesome-pyladies-creations/blob/main/CONTRIBUTING.md"
           class="btn-ghost" target="_blank" rel="noopener">Add Your Work</a>
      </div>
    </div>
    <div class="hero-grid-bg" aria-hidden="true"><div class="dot-grid"></div></div>
  </section>

  {section_featured("Featured", "The People", "PyLadies members sharing knowledge, code, and passion with the world.",
      all_people_cards, "people-grid", "people.html", "featured-people", alt_bg=False)}

  {section_featured("Featured", "PyLadies Chapters", "PyLadies chapters around the world — find your local community.",
      all_chapter_cards, "chapters-grid", "chapters.html", "featured-chapters", alt_bg=True)}

  {section_featured("Featured", "Content", "Blogs, YouTube channels, and podcasts produced by PyLadies members.",
      all_content_cards, "content-grid", "content.html", "featured-content", alt_bg=False)}

  {section_featured("Featured", "Packages &amp; Tools", "Python packages and software built and maintained by PyLadies members.",
      all_package_cards, "packages-grid", "packages.html", "featured-packages", alt_bg=True)}
""" + footer_html(updated) + f"""
  <script>
    window.addEventListener('DOMContentLoaded', function() {{
      [
        ['#featured-people .person-card',     {FEATURED_PEOPLE}],
        ['#featured-content .content-card',   {FEATURED_CONTENT}],
        ['#featured-chapters .chapter-card',  {FEATURED_CHAPTERS}],
        ['#featured-packages .package-card',  {FEATURED_PACKAGES}]
      ].forEach(function(pair) {{
        var sel = pair[0], n = pair[1];
        var cards = Array.from(document.querySelectorAll(sel));
        cards.forEach(function(c) {{ c.style.display = 'none'; }});
        cards.sort(function() {{ return Math.random() - 0.5; }})
             .slice(0, n)
             .forEach(function(c) {{ c.style.display = ''; }});
      }});
    }});
  </script>"""

    with open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8") as f:
        f.write(index)

    # ── people.html ───────────────────────────────────────────────────────────
    people_page = nav_html(home="index.html", active="people", title="People · Awesome PyLadies") + \
        section_people_full(all_people_cards, n_podcasts) + \
        footer_html(updated) + JS_PEOPLE

    with open(os.path.join(ROOT, "docs", "people.html"), "w", encoding="utf-8") as f:
        f.write(people_page)

    # ── content.html ──────────────────────────────────────────────────────────
    content_page = nav_html(home="index.html", active="content", title="Content · Awesome PyLadies") + \
        section_content_full(all_content_cards, n_podcasts) + \
        footer_html(updated) + JS_CONTENT

    with open(os.path.join(ROOT, "docs", "content.html"), "w", encoding="utf-8") as f:
        f.write(content_page)

    # ── packages.html ─────────────────────────────────────────────────────────
    packages_page = nav_html(home="index.html", active="packages", title="Packages · Awesome PyLadies") + \
        section_packages_full(all_package_cards) + \
        footer_html(updated) + JS_PACKAGES

    with open(os.path.join(ROOT, "docs", "packages.html"), "w", encoding="utf-8") as f:
        f.write(packages_page)

    # ── chapters.html ─────────────────────────────────────────────────────────
    leaflet_css = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />'
    chapters_page = nav_html(home="index.html", active="chapters", extra_head=leaflet_css, title="Chapters · Awesome PyLadies") + \
        section_chapters_full(chapter_groups, chapter_content_map, chapters_data) + \
        footer_html(updated) + JS_CHAPTERS_SEARCH + js_chapters_map(chapters_data)

    with open(os.path.join(ROOT, "docs", "chapters.html"), "w", encoding="utf-8") as f:
        f.write(chapters_page)

    # ── about.html ────────────────────────────────────────────────────────────
    about_page = nav_html(home="index.html", active="about", title="About · Awesome PyLadies") + \
        section_about() + footer_html(updated)

    with open(os.path.join(ROOT, "docs", "about.html"), "w", encoding="utf-8") as f:
        f.write(about_page)

    # ── contribute.html ───────────────────────────────────────────────────────
    contribute_page = nav_html(home="index.html", active="contribute", title="Contribute · Awesome PyLadies") + \
        section_contribute() + footer_html(updated)

    with open(os.path.join(ROOT, "docs", "contribute.html"), "w", encoding="utf-8") as f:
        f.write(contribute_page)

    print(
        f"Generated index.html (shows {FEATURED_PEOPLE}/{len(all_people_cards)} people, "
        f"{FEATURED_CONTENT}/{len(all_content_cards)} content, "
        f"{FEATURED_CHAPTERS}/{len(all_chapter_cards)} chapters, "
        f"{FEATURED_PACKAGES}/{len(all_package_cards)} packages randomly) + "
        f"people.html · content.html · chapters.html · packages.html · about.html"
    )


if __name__ == "__main__":
    main()
