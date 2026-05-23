import os
import json
import random
import requests
from datetime import datetime, timezone
from typing import Optional
import urllib.parse

# Configuration
fallback_images_dir = "img/fallback_images/"
content_directory = "data/content/"
packages_directory = "data/packages/"
software_directory = "data/software/"

if os.path.exists(fallback_images_dir):
    fallback_images = [f for f in os.listdir(fallback_images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
else:
    fallback_images = []

def load_svg_inline_from_url(icon_url, color="black", size=20):
    try:
        response = requests.get(icon_url)
        response.raise_for_status()
        svg_content = response.text
        svg_content = svg_content.replace('<svg ', f'<svg fill="{color}" width="{size}" height="{size}" ')
        return svg_content
    except:
        return "" 

def build_social_url(platform, handle):
    if not handle: return None
    handle = handle.strip()
    handle = urllib.parse.unquote(handle)
    if platform not in ["mastodon", "bluesky"]: handle = handle.lstrip("@")
    if platform == "x": return handle if handle.startswith("http") else f"https://x.com/{handle}"
    elif platform == "mastodon":
        if handle.startswith("http"): return handle
        if "@" in handle[1:]:
            parts = handle.lstrip("@").split("@")
            if len(parts) == 2: return f"https://{parts[1]}/@{parts[0]}"
        return handle
    elif platform == "linkedin": return handle if handle.startswith("http") else f"https://www.linkedin.com/in/{handle.rstrip('/')}"
    elif platform == "github": return handle if handle.startswith("http") else f"https://github.com/{handle}"
    elif platform == "youtube":
        if handle.startswith("http"): return handle
        return f"https://www.youtube.com/{handle}" if handle.startswith("@") else f"https://www.youtube.com/user/{handle}"
    elif platform == "website": return handle if handle.startswith("http") else "http://" + handle
    elif platform == "bluesky": return handle if handle.startswith("http") else f"https://bsky.app/profile/{handle.lstrip('@')}"
    elif platform == "instagram": return handle if handle.startswith("http") else f"https://instagram.com/{handle.lstrip('@')}"
    return None

def add_platform_icon(platform: str, base_icon_url: str, url: Optional[str]) -> Optional[str]:
    if platform == "website": platform = "safari"
    if not url: return None
    icon_url = f"{base_icon_url}{platform}.svg"
    return load_svg_inline_from_url(icon_url, color="#929dad", size=15)

def build_social_icons(social_dict, icon_style='emoji'):
    socials = ""
    base_icon_url = "https://github.com/cosimameyer/awesome-pyladies-creations/raw/main/img/icons/"
    ordered_platforms = ["website", "github", "mastodon", "bluesky", "instagram", "youtube", "linkedin", "x"]
    emoji_icons = {"website": "🌐", "github": "🐙", "mastodon": "🐘", "bluesky": "🦋", "instagram": "📸", "youtube": "▶️", "linkedin": "🧳", "x": "🐦"}
    for platform in ordered_platforms:
        handle = social_dict.get(platform)
        url = build_social_url(platform, handle)
        if not url: continue
        if icon_style == 'emoji':
            label = emoji_icons.get(platform, "🔗")
            socials += f'<a href="{url}" target="_blank" style="margin:0 4px; font-size:16px; text-decoration:none; color:black;">{label}</a> '
        else:
            if platform != "linkedin":
                icon_html = add_platform_icon(platform, base_icon_url, url)
                if icon_html: socials += f'<a href="{url}" target="_blank" style="margin:0 1px;">{icon_html}</a> '
    return socials

def image_exists(url):
    if not url: return False
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except: return False

# 1. Load Data
def load_json_files(path):
    data_list = []
    if os.path.exists(path):
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
                    content = json.load(f)
                    # Handle if the JSON root is a list (like your package entry)
                    if isinstance(content, list): data_list.extend(content)
                    else: data_list.append(content)
    return data_list

content_data = load_json_files(content_directory)
package_data = load_json_files(packages_directory)
software_data = load_json_files(software_directory)

content_data.sort(key=lambda x: x.get('authors', [{}])[0].get('name', 'Unknown'))

# 2. Build Grid
cols = 4
grid_entries, count = "", 0
for entry in content_data:
    count += 1
    authors_list = entry.get('authors', [])
    name = authors_list[0].get('name', 'Unknown') if authors_list else 'Unknown'
    photo_url = entry.get('photo_url')
    if not image_exists(photo_url):
        img_name = random.choice(fallback_images) if fallback_images else ""
        photo_url = f"https://github.com/cosimameyer/awesome-pyladies-creations/raw/main/{fallback_images_dir}{img_name}"
    social_info = authors_list[0].get('social_media', [{}])[0] if authors_list else {}
    social_icons = build_social_icons(social_info)
    grid_entry = f'<a href="{entry.get("url", "#")}"><img width="130" alt="Image of {name}" src="{photo_url}"><br></a><span class="caption">{name}</span><br>{social_icons}|'
    if count % cols == 0: grid_entry += '\n|'
    grid_entries += grid_entry

if count % cols != 0: grid_entries += "| " * (cols - (count % cols)) + "\n|"
full_table = f"{'| ' * cols}|\n{'|:---:' * cols}|\n|{grid_entries}"

# 3. Build Categorized Lists
blogs, youtube, podcasts, libraries, other_software = [], [], [], [], []

def format_entry_line(entry, is_package=False):
    # Surgical fix for authors vs maintainers
    authors_list = entry.get("authors") or entry.get("maintainers") or []
    if not authors_list:
        authors_str = "Unknown"
    else:
        authors_str = ", ".join([a.get("name", "Unknown") for a in authors_list])

    # Surgical fix for naming and URLs in packages
    title = entry.get('title') or entry.get('name', 'Untitled')
    url = entry.get('url') or entry.get('website_url') or entry.get('repo_url') or '#'

    return f"- [{title}]({url}) by {authors_str}"

for entry in content_data:
    line = format_entry_line(entry)
    etype = entry.get("type", "").lower()
    if etype == "blog": blogs.append(line)
    elif etype == "youtube": youtube.append(line)
    elif etype == "podcast": podcasts.append(line)

for entry in package_data:
    libraries.append(format_entry_line(entry, is_package=True))

for entry in software_data:
    other_software.append(format_entry_line(entry))

# 4. Generate README
sections = []
if blogs: sections.extend(["### Blogs", os.linesep.join(blogs)])
if youtube: sections.extend(["### YouTube Channels", os.linesep.join(youtube)])
if podcasts: sections.extend(["### Podcasts", os.linesep.join(podcasts)])
if libraries or other_software:
    sections.append("### Software")
    if libraries: sections.extend(["#### Python Libraries", os.linesep.join(libraries)])
    if other_software: sections.extend(["#### Other Software", os.linesep.join(other_software)])

readme_content = f"""
# Awesome PyLadies' Repository  

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

## What Is This Repository About?  

It provides a curated list of awesome content by PyLadies and collects information to further promote content by [PyLadies on social media](https://cosimameyer.github.io/community-bots/) 🤖  

To contribute, please see [contributing](CONTRIBUTING.md) ✨  

## List of Contributors as Tiles  

{full_table}

## List of Content  

{os.linesep.join(sections)}

---

_Last updated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_

## License  

[![CC0](https://upload.wikimedia.org/wikipedia/commons/6/69/CC0_button.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)