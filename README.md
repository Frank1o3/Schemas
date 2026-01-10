# Schemas

A curated collection of JSON Schemas designed for validation, tooling, and documentation.

This repository focuses on **real-world configuration schemas**, including community-maintained and reverse-engineered formats, with clear annotations and validation guarantees.

## Structure

- `schemas/` – All JSON Schema definitions
- `docs/` – Human-readable documentation
- Each schema is versioned, documented, and validated against JSON Schema standards

## Goals

- Strong editor validation (VS Code, IntelliJ, etc.)
- Clear distinction between **official**, **community**, and **deprecated** fields
- Long-term maintainability

## Usage

Schemas can be referenced directly via raw GitHub URLs or vendored locally.

```json
{
  "$schema": "https://example.com/schemas/roblox/fastflags.schema.json"
}
