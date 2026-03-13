# SmithPy Mod Policy Schema

Defines mod conflict and dependency rules for SmithPy

## Schema Structure

**Type:** `object`

This schema uses dynamic keys. Each key represents an entry with the following structure:

```yaml
conflicts:
  type: array
sub_mods:
  type: array
```

## JSON Schema

[View JSON Schema](https://frank1o3.github.io/Schemas/smithpy/policy.schema.json)
