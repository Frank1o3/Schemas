import yaml
import json
import pathlib
from jsonschema import validate, ValidationError

ROOT = pathlib.Path(__file__).parents[1]
REGISTRY = ROOT / "registry"
SCHEMA = ROOT / "schemas/_meta/registry.schema.json"


def main():
    # Load schema
    try:
        schema = json.loads(SCHEMA.read_text())
        print(f"✓ Loaded schema from {SCHEMA.relative_to(ROOT)}")
    except Exception as e:
        print(f"✗ Failed to load schema: {e}")
        return 1

    # Track validation results
    validated = []
    failed = []

    # Validate all YAML files
    for file in sorted(REGISTRY.rglob("*.y*ml")):
        try:
            data = yaml.safe_load(file.read_text())
            validate(data, schema)
            validated.append(file)
            print(f"✓ {file.relative_to(ROOT)}")
        except ValidationError as e:
            failed.append((file, e))
            print(f"✗ {file.relative_to(ROOT)}")
            print(f"  Error: {e.message}")
            print(f"  Path: {' -> '.join(str(p) for p in e.path)}")

            # Show helpful context
            if "required" in e.message and "flags" in e.message:
                print("\n  Hint: This file is missing the required 'flags' field.")
                print("  Expected structure:")
                print("    schema:")
                print("      title: ...")
                print("      type: ...")
                print("    flags:")
                print("      flag_name:")
                print("        type: ...")
                print()
        except yaml.YAMLError as e:
            failed.append((file, e))
            print(f"✗ {file.relative_to(ROOT)}")
            print(f"  YAML Error: {e}")
        except Exception as e:
            failed.append((file, e))
            print(f"✗ {file.relative_to(ROOT)}")
            print(f"  Unexpected Error: {e}")

    # Summary
    print(f"\n{'=' * 60}")
    print("Validation Summary:")
    print(f"  ✓ Passed: {len(validated)}")
    print(f"  ✗ Failed: {len(failed)}")
    print(f"{'=' * 60}")

    if failed:
        print("\nFailed files:")
        for file, _ in failed:
            print(f"  - {file.relative_to(ROOT)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
