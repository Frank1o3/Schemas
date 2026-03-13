import yaml
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "registry"
OUTPUT_DIR = ROOT / "docs"

JSON_SCHEMA_VERSION = "https://json-schema.org/draft/2020-12/schema"
BASE_ID = "https://frank1o3.github.io/Schemas"


def generate_schema(registry_file: pathlib.Path):
    """Generate JSON Schema from registry YAML file."""

    with registry_file.open() as f:
        data = yaml.safe_load(f)

    schema_meta = data.get("schema", {})
    flags = data.get("flags", {})

    # Derive schema ID from path
    relative_path = registry_file.relative_to(REGISTRY_DIR).with_suffix(".schema.json")
    schema_id = f"{BASE_ID}/{relative_path.as_posix()}"

    # Base schema
    schema = {
        "$schema": JSON_SCHEMA_VERSION,
        "title": schema_meta.get("title"),
        "description": schema_meta.get("description"),
        "type": schema_meta.get("type", "object"),
    }
    schema["$comment"] = "Generated from registry YAML. Do not edit manually."

    if "required" in schema_meta:
        schema["required"] = schema_meta["required"]

    if "additionalProperties" in schema_meta:
        schema["additionalProperties"] = schema_meta["additionalProperties"]

    # If flags exist, convert them into properties
    if flags:
        schema["properties"] = {}

        for flag, meta in flags.items():
            # Copy schema exactly as written in YAML
            prop = dict(meta)

            # Ensure description exists for documentation consistency
            prop.setdefault("description", "")

            schema["properties"][flag] = prop

    return schema


def main():
    """Generate JSON schemas for all registry YAML files."""

    print(f"Searching for YAML files in {REGISTRY_DIR.relative_to(ROOT)}")
    print(f"Output directory: {OUTPUT_DIR.relative_to(ROOT)}")
    print(f"Base URL: {BASE_ID}")
    print(f"\n{'=' * 60}")

    generated = []
    errors = []

    for yaml_file in sorted(REGISTRY_DIR.rglob("*.y*ml")):
        try:
            relative = yaml_file.relative_to(REGISTRY_DIR)
            output_path = OUTPUT_DIR / relative.with_suffix(".schema.json")

            output_path.parent.mkdir(parents=True, exist_ok=True)

            schema = generate_schema(yaml_file)

            output_path.write_text(json.dumps(schema, indent=2))

            generated.append((yaml_file, output_path))

            print(f"✓ {relative}")
            print(f"  → {output_path.relative_to(ROOT)}")

        except Exception as e:
            errors.append((yaml_file, e))

            print(f"✗ {yaml_file.relative_to(REGISTRY_DIR)}")
            print(f"  Error: {e}")

    print(f"\n{'=' * 60}")
    print("Schema Generation Summary:")
    print(f"  ✓ Generated: {len(generated)}")
    print(f"  ✗ Failed: {len(errors)}")
    print(f"{'=' * 60}\n")

    if errors:
        print("Failed files:")
        for file, error in errors:
            print(f"  - {file.relative_to(REGISTRY_DIR)}: {error}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
