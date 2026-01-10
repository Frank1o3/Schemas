import yaml
import json
import pathlib
from jsonschema import validate

ROOT = pathlib.Path(__file__).parents[1]
REGISTRY = ROOT / "registry"
SCHEMA = ROOT / "schemas/_meta/registry.schema.json"

schema = json.loads(SCHEMA.read_text())

for file in REGISTRY.rglob("*.y*ml"):
    data = yaml.safe_load(file.read_text())
    validate(data, schema)
    print(f"Validated {file}")
