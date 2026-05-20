import os
import json
import sys
import jsonschema

chapters_dir = "data/chapters/"
schema_path = "scripts/.chapter_schema.json"

with open(schema_path) as f:
    schema = json.load(f)

files = os.listdir(chapters_dir)

non_json = [f for f in files if not f.endswith(".json")]
if non_json:
    print("Error: the following files have the wrong extension (must end with .json):")
    for f in non_json:
        print(f"  {f}")
    sys.exit(1)

errors = []
for filename in files:
    path = os.path.join(chapters_dir, filename)
    with open(path) as f:
        data = json.load(f)
    validator = jsonschema.Draft4Validator(schema)
    file_errors = list(validator.iter_errors(data))
    for err in file_errors:
        errors.append(f"{filename}: {err.message} (path: {'/'.join(str(p) for p in err.absolute_path)})")

if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print(f"All {len(files)} chapter JSON files are valid.")
