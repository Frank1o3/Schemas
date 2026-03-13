# SmithPy Modrinth API Config Schema

Schema for Modrinth API endpoint configuration

## Configuration Flags

### `$schema`

**Type:** `string`

Optional schema reference

### `BASE_URL`

**Type:** `string`

Base Modrinth API URL

**Constraints:**
- Pattern: `^https://`

### `ENDPOINTS`

**Type:** `object`

Modrinth API endpoint mappings

## JSON Schema

[View JSON Schema](https://frank1o3.github.io/Schemas/schemas/smithpy/modrinth_api.schema.json)
