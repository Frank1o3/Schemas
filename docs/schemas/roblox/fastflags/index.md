# Roblox Fast Flags

Validation schema for Roblox ClientAppSettings Fast Flags

**Version:** 1.0.0

## Configuration Flags

### `FFlagDebugGraphicsPreferVulkan`

**Type:** `boolean`

Prefer Vulkan rendering backend

**Allow-list status:** `allowed`

### `DFIntTextureQualityOverride`

**Type:** `integer`

Overrides texture quality level

**Constraints:**
- Minimum: `0`
- Maximum: `3`

**Allow-list status:** `allowed`

### `DFIntTaskSchedulerTargetFps`

**Type:** `integer`

Community FPS scheduler flag

**Constraints:**
- Minimum: `30`
- Maximum: `1000`

**Allow-list status:** `not-allowlisted`

**Notes:** Ignored by current Roblox clients

## JSON Schema

[View JSON Schema](https://frank1o3.github.io/Schemas/schemas/roblox/fastflags.schema.json)
