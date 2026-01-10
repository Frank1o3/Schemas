import yaml
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "registry"
OUTPUT_DIR = ROOT / "docs" / "schemas"

JSON_SCHEMA_VERSION = "https://json-schema.org/draft/2020-12/schema"
BASE_ID = "https://frank1o3.github.io/Schemas/schemas"


def generate_schema(registry_file: pathlib.Path):
    with registry_file.open() as f:
        data = yaml.safe_load(f)

    schema_meta = data["schema"]
    flags = data.get("flags", {})

    # Derive schema ID from path
    relative_path = registry_file.relative_to(REGISTRY_DIR).with_suffix(".schema.json")
    schema_id = f"{BASE_ID}/{relative_path.as_posix()}"

    version = schema_meta.get("version", "0.0.0")
    schema_id = f"{schema_id}#v{version}"

    schema = {
        "$schema": JSON_SCHEMA_VERSION,
        "$id": schema_id,
        "title": schema_meta.get("title"),
        "description": schema_meta.get("description"),
        "type": schema_meta.get("type", "object"),
        "additionalProperties": schema_meta.get("additionalProperties", False),
        "properties": {}
    }

    for flag, meta in flags.items():
        prop = {
            "type": meta["type"],
            "description": meta.get("description", "")
        }

        # Standard validation keywords
        for key in ("minimum", "maximum", "pattern", "enum", "default"):
            if key in meta:
                prop[key] = meta[key]

        # Documentation-only metadata (non-validation)
        for key, value in meta.items():
            if key not in prop and key not in ("type", "description"):
                prop[f"x-{key}"] = value

        schema["properties"][flag] = prop

    return schema


def main():
    for yaml_file in REGISTRY_DIR.rglob("*.y*ml"):
        relative = yaml_file.relative_to(REGISTRY_DIR)
        output_path = OUTPUT_DIR / relative.with_suffix(".schema.json")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        schema = generate_schema(yaml_file)
        output_path.write_text(json.dumps(schema, indent=2))

        print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
