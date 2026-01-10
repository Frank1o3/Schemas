import yaml
import pathlib

ROOT = pathlib.Path(__file__).parents[1]
REGISTRY = ROOT / "registry"
DOCS = ROOT / "docs/schemas"

for file in REGISTRY.rglob("*.y*ml"):
    data = yaml.safe_load(file.read_text())
    out = DOCS / file.relative_to(REGISTRY).with_suffix(".md")
    out.parent.mkdir(parents=True, exist_ok=True)

    lines:list[str] = [
        f"# {data['schema']['title']}",
        "",
        data['schema'].get("description", ""),
        "",
        "## Flags",
        ""
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
