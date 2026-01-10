import yaml
import pathlib

ROOT = pathlib.Path(__file__).parents[1]
REGISTRY = ROOT / "registry"
DOCS = ROOT / "docs" / "schemas"

for file in REGISTRY.rglob("*.y*ml"):
    data = yaml.safe_load(file.read_text())

    # Each schema gets its own directory with index.md
    out_dir = DOCS / file.relative_to(REGISTRY).with_suffix("")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.md"

    lines: list[str] = [
        f"# {data['schema']['title']}",
        "",
        data["schema"].get("description", ""),
    ]

    for name, meta in data["flags"].items():
        lines.append(f"### `{name}`")
        lines.append(f"- Type: `{meta['type']}`")

        if "description" in meta:
            lines.append(f"- Description: {meta['description']}")

        if "allowListStatus" in meta:
            lines.append(f"- Allow-list status: `{meta['allowListStatus']}`")

        if "notes" in meta:
            lines.append(f"- Notes: {meta['notes']}")

        lines.append("")

    out.write_text("\n".join(lines))
    print(f"Generated docs {out}")
