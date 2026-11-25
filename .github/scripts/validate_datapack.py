#!/usr/bin/env python3
"""Structural checks for the bundled MyOwnLoot Minecraft 1.21.1 datapack."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []

meta_path = ROOT / "pack.mcmeta"
if not meta_path.is_file():
    errors.append("Missing pack.mcmeta")
else:
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        pack_format = meta.get("pack", {}).get("pack_format")
        if pack_format != 48:
            errors.append(f"Expected pack_format 48 for Minecraft 1.21.1, found {pack_format!r}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid pack.mcmeta: {exc}")

data = ROOT / "data"
if not data.is_dir():
    errors.append("Missing data/ directory")
else:
    for namespace in ("mol", "itemio", "iris", "smithed.custom_block"):
        if not (data / namespace).is_dir():
            errors.append(f"Missing bundled namespace: data/{namespace}/")

    # Minecraft 1.21 renamed these datapack registry directories to singular.
    legacy_dirs = {
        "functions", "loot_tables", "item_modifiers", "predicates", "advancements",
        "blocks", "entity_types", "items", "fluids",
    }
    for path in data.rglob("*"):
        if path.is_dir() and path.name in legacy_dirs:
            errors.append(f"Legacy 1.20 directory name remains: {path.relative_to(ROOT)}")

    json_files = sorted(data.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")

    functions = list(data.rglob("*.mcfunction"))
    if not functions:
        errors.append("No .mcfunction files found")

if errors:
    print("Datapack validation FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("Datapack structure and JSON validation passed.")
print("Note: this does not replace loading the pack in a Minecraft 1.21.1 server.")
