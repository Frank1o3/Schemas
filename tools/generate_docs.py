import yaml
import pathlib

ROOT = pathlib.Path(__file__).parents[1]
REGISTRY = ROOT / "registry"
DOCS = ROOT / "docs"


def generate_doc(yaml_file: pathlib.Path):
    """Generate documentation for a registry YAML file."""
    data = yaml.safe_load(yaml_file.read_text())

    # Create directory structure: docs/schemas/[dir]/[filename]/index.md
    relative_path = yaml_file.relative_to(REGISTRY).with_suffix("")
    out_dir = DOCS / relative_path
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.md"

    # Build documentation
    lines: list[str] = [
        f"# {data['schema']['title']}",
        "",
        data["schema"].get("description", ""),
        "",
    ]

    # Add schema metadata
    if "version" in data["schema"]:
        lines.extend(
            [
                f"**Version:** {data['schema']['version']}",
                "",
            ]
        )

    # Add flags documentation if they exist
    flags = data.get("flags", {})
    if flags:
        lines.extend(
            [
                "## Configuration Flags",
                "",
            ]
        )

        for name, meta in flags.items():
            lines.append(f"### `{name}`")
            lines.append("")
            lines.append(f"**Type:** `{meta['type']}`")
            lines.append("")

            if "description" in meta:
                lines.append(f"{meta['description']}")
                lines.append("")

            # Add validation constraints
            constraints = []
            if "minimum" in meta:
                constraints.append(f"Minimum: `{meta['minimum']}`")
            if "maximum" in meta:
                constraints.append(f"Maximum: `{meta['maximum']}`")
            if "pattern" in meta:
                constraints.append(f"Pattern: `{meta['pattern']}`")
            if "enum" in meta:
                constraints.append(
                    f"Allowed values: {', '.join(f'`{v}`' for v in meta['enum'])}"
                )
            if "default" in meta:
                constraints.append(f"Default: `{meta['default']}`")

            if constraints:
                lines.append("**Constraints:**")
                for constraint in constraints:
                    lines.append(f"- {constraint}")
                lines.append("")

            # Add custom metadata
            if "allowListStatus" in meta:
                lines.append(f"**Allow-list status:** `{meta['allowListStatus']}`")
                lines.append("")

            if "notes" in meta:
                lines.append(f"**Notes:** {meta['notes']}")
                lines.append("")

    # Add schema structure documentation for non-flag schemas
    else:
        lines.extend(
            [
                "## Schema Structure",
                "",
                f"**Type:** `{data['schema']['type']}`",
                "",
            ]
        )

        if "additionalProperties" in data["schema"] and isinstance(
            data["schema"]["additionalProperties"], dict
        ):
            lines.extend(
                [
                    "This schema uses dynamic keys. Each key represents an entry with the following structure:",
                    "",
                    "```yaml",
                ]
            )

            # Document the additionalProperties structure
            props = data["schema"]["additionalProperties"]
            if "properties" in props:
                for prop_name, prop_meta in props["properties"].items():
                    prop_type = prop_meta.get("type", "unknown")
                    prop_desc = prop_meta.get("description", "")
                    lines.append(f"{prop_name}:")
                    lines.append(f"  type: {prop_type}")
                    if prop_desc:
                        lines.append(f"  # {prop_desc}")

            lines.extend(
                [
                    "```",
                    "",
                ]
            )

    # Add JSON Schema link
    schema_url = f"https://frank1o3.github.io/Schemas/{relative_path.as_posix()}.schema.json"
    lines.extend(
        [
            "## JSON Schema",
            "",
            f"[View JSON Schema]({schema_url})",
            "",
        ]
    )

    # Write documentation
    out.write_text("\n".join(lines))
    return out


def main():
    """Generate documentation for all registry YAML files."""
    print(f"Searching for YAML files in {REGISTRY.relative_to(ROOT)}")
    print(f"Output directory: {DOCS.relative_to(ROOT)}")
    print(f"\n{'=' * 60}")

    generated = []
    errors = []

    for yaml_file in sorted(REGISTRY.rglob("*.y*ml")):
        try:
            out = generate_doc(yaml_file)
            generated.append((yaml_file, out))

            relative_yaml = yaml_file.relative_to(REGISTRY)
            relative_doc = out.relative_to(ROOT)
            url = f"https://frank1o3.github.io/Schemas/schemas/{relative_yaml.with_suffix('')}"

            print(f"✓ {relative_yaml}")
            print(f"  → {relative_doc}")
            print(f"  🌐 {url}")

        except Exception as e:
            errors.append((yaml_file, e))
            print(f"✗ {yaml_file.relative_to(REGISTRY)}")
            print(f"  Error: {e}")

    # Summary
    print(f"\n{'=' * 60}")
    print("Documentation Generation Summary:")
    print(f"  ✓ Generated: {len(generated)}")
    print(f"  ✗ Failed: {len(errors)}")
    print(f"{'=' * 60}\n")

    if errors:
        print("Failed files:")
        for file, error in errors:
            print(f"  - {file.relative_to(REGISTRY)}: {error}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
