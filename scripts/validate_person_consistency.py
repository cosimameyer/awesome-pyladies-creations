"""
Check that the same person/chapter's social handles are consistent across all data files.

Sources checked:
  data/content/   — authors[].social_media  (list of dicts, bare handles)
  data/packages/  — maintainers[].social_media (list of dicts, bare handles)
  data/members/   — top-level social_media (list of dicts, bare handles)
  data/chapters/  — top-level social_media (flat dict, full URLs)

Both formats are normalised to a bare handle before comparison so that
  "x": "https://x.com/PyLadiesEdin"
and
  "x": "PyLadiesEdin"
are treated as identical.

Exits 0 if no conflicts, 1 if conflicts are found.
"""
import json
import os
import sys
import urllib.parse

ROOT         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR  = os.path.join(ROOT, "data", "content")
PACKAGES_DIR = os.path.join(ROOT, "data", "packages")
MEMBERS_DIR  = os.path.join(ROOT, "data", "members")
CHAPTERS_DIR = os.path.join(ROOT, "data", "chapters")


def extract_handle(value):
    """
    Normalise a social media value to a bare, lowercase handle for comparison.
    Handles both full URLs and bare handles/usernames.
    """
    if not value:
        return ""
    v = str(value).strip()
    if v.startswith("http"):
        parsed = urllib.parse.urlparse(v)
        # Take the last non-empty path segment as the username
        segments = [s for s in parsed.path.split("/") if s]
        handle = segments[-1] if segments else parsed.netloc
    else:
        handle = v
    return handle.lower().lstrip("@").rstrip("/")


def load_content_entries(directory, person_key):
    """Yield (file_path, name, platform, raw_handle) for content/packages dirs."""
    if not os.path.exists(directory):
        return
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(directory, filename)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            for person in entry.get(person_key, []):
                name = person.get("name", "").strip()
                if not name:
                    continue
                for sm in person.get("social_media", []):
                    for platform, handle in sm.items():
                        if handle:
                            yield path, name, platform, str(handle).strip()


def load_member_entries(directory):
    """Yield (file_path, name, platform, raw_handle) for members dir.
    Member files are top-level objects: {name, photo_url, social_media: [{}]}."""
    if not os.path.exists(directory):
        return
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(directory, filename)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("name", "").strip()
        if not name:
            continue
        for sm in data.get("social_media", []):
            for platform, handle in sm.items():
                if handle:
                    yield path, name, platform, str(handle).strip()


def load_chapter_entries(directory):
    """Yield (file_path, name, platform, raw_handle) for chapters dir.
    Chapter social_media is a list of dicts (same structure as content authors)."""
    if not os.path.exists(directory):
        return
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(directory, filename)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("name", "").strip()
        if not name:
            continue
        for sm in (data.get("social_media") or []):
            for platform, handle in sm.items():
                if handle:
                    yield path, name, platform, str(handle).strip()


def build_registry():
    """Return {name: [(file_path, platform, raw_handle), ...]} for all entries."""
    registry = {}

    for file_path, name, platform, handle in load_content_entries(CONTENT_DIR, "authors"):
        registry.setdefault(name, []).append((file_path, platform, handle))

    for file_path, name, platform, handle in load_content_entries(PACKAGES_DIR, "maintainers"):
        registry.setdefault(name, []).append((file_path, platform, handle))

    for file_path, name, platform, handle in load_member_entries(MEMBERS_DIR):
        registry.setdefault(name, []).append((file_path, platform, handle))

    for file_path, name, platform, handle in load_chapter_entries(CHAPTERS_DIR):
        registry.setdefault(name, []).append((file_path, platform, handle))

    return registry


def find_conflicts(registry):
    """Return list of (name, platform, [(file, handle), ...]) for conflicting entries."""
    conflicts = []
    for name, entries in registry.items():
        by_platform = {}
        for file_path, platform, handle in entries:
            by_platform.setdefault(platform, []).append((file_path, handle))

        for platform, file_handles in by_platform.items():
            unique_values = {}
            for file_path, handle in file_handles:
                n = extract_handle(handle)
                unique_values.setdefault(n, []).append((file_path, handle))

            if len(unique_values) > 1:
                flat = [(fp, h) for fh in unique_values.values() for fp, h in fh]
                conflicts.append((name, platform, flat))

    return conflicts


def main():
    registry  = build_registry()
    conflicts = find_conflicts(registry)

    if not conflicts:
        print(f"No inconsistencies found across {len(registry)} people and chapters.")
        sys.exit(0)

    print(f"Found {len(conflicts)} inconsistenc{'y' if len(conflicts)==1 else 'ies'} across person/chapter entries:\n")
    for name, platform, file_handles in conflicts:
        print(f"  Person/chapter: {name!r}  |  Platform: {platform}")
        for file_path, handle in file_handles:
            rel = os.path.relpath(file_path, ROOT)
            print(f"    {rel}: {handle!r}")
        print()

    sys.exit(1)


if __name__ == "__main__":
    main()
