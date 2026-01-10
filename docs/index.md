# Schemas

This repository provides **machine-readable JSON Schemas** and **human-readable documentation** for real-world configuration formats.

Schemas are generated from a validated registry and are intended for:

- Editor validation (VS Code, IntelliJ, etc.)
- Static analysis
- Tooling and automation
- Long-term documentation

---

## How This Repository Works

Schemas in this repository are **not handwritten**.

Each schema is generated from a structured registry definition and validated automatically through CI.  
This ensures:

- Consistent schema structure
- Accurate documentation
- No drift between source and output

Generated files should not be edited manually.

---

## Available Schemas

### Roblox

- **Fast Flags**  
  Validation and documentation for Roblox `ClientAppSettings.json` Fast Flags.  
  Includes both officially allow-listed flags and community-discovered flags, clearly annotated.

---

## Usage

Schemas can be referenced directly in configuration files or tooling.

Example:

```json
{
  "$schema": "https://frank1o3.github.io/Schemas/schemas/roblox/fastflags.schema.json"
}
