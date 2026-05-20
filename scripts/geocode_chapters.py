"""
Auto-geocode chapter content files that have "chapter": true but are missing lat/lon.
Uses Nominatim (OpenStreetMap) — free, no API key required.
Writes coordinates back into the JSON files in-place.
"""

import json
import os
import sys
import time

import requests

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "content")
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "awesome-pyladies-creations geocoder (github.com/cosimameyer/awesome-pyladies-creations)"


def _city_from_name(name: str) -> str:
    """Extract city from 'PyLadies <City>' or similar patterns."""
    lower = name.lower()
    for prefix in ("pyladies ", "pyladies-"):
        if lower.startswith(prefix):
            return name[len(prefix):].strip()
    return name


def geocode(query: str) -> tuple[float, float] | None:
    """Return (lat, lon) or None if not found."""
    try:
        resp = requests.get(
            NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": 1},
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            return round(float(results[0]["lat"]), 4), round(float(results[0]["lon"]), 4)
    except Exception as exc:
        print(f"  Geocoding error for '{query}': {exc}", file=sys.stderr)
    return None


def build_query(entry: dict) -> str:
    """Build the best geocoding query from available fields."""
    country = entry.get("country", "")
    # Try to get city from authors first
    for author in entry.get("authors", []):
        city = _city_from_name(author.get("name", ""))
        if city and country:
            return f"{city}, {country}"
        if city:
            return city
    # Fall back to title
    city = _city_from_name(entry.get("title", ""))
    if city and country:
        return f"{city}, {country}"
    return city or country


def process_file(path: str) -> bool:
    """Geocode a single file. Returns True if the file was updated."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("chapter"):
        return False
    if data.get("lat") is not None and data.get("lon") is not None:
        return False

    query = build_query(data)
    if not query:
        print(f"  Skipping {os.path.basename(path)}: no query could be built")
        return False

    print(f"  Geocoding '{query}' for {os.path.basename(path)} ...")
    time.sleep(1)  # Nominatim rate limit: 1 req/sec
    result = geocode(query)
    if result is None:
        print(f"  No result for '{query}'")
        return False

    lat, lon = result
    data["lat"] = lat
    data["lon"] = lon
    print(f"  -> lat={lat}, lon={lon}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")
    return True


def main() -> int:
    updated = []
    skipped = []

    files = sorted(
        os.path.join(CONTENT_DIR, fn)
        for fn in os.listdir(CONTENT_DIR)
        if fn.endswith(".json")
    )

    for path in files:
        try:
            if process_file(path):
                updated.append(os.path.basename(path))
            else:
                skipped.append(os.path.basename(path))
        except Exception as exc:
            print(f"Error processing {path}: {exc}", file=sys.stderr)

    print(f"\nUpdated {len(updated)} file(s): {', '.join(updated) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
