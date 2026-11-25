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

    # Minecraft 1.21 renamed registry directories to singular. Restrict
    # checks to registry roots so valid loot_table/blocks and loot_table/items
    # subfolders are not mistaken for old registry names.
    legacy_roots = {
        "functions", "loot_tables", "item_modifiers", "predicates", "advancements",
    }
    legacy_tag_roots = {
        "functions", "blocks", "entity_types", "items", "fluids",
    }
    for path in data.rglob("*"):
        if not path.is_dir():
            continue
        parts = path.relative_to(data).parts
        if len(parts) == 2 and parts[1] in legacy_roots:
            errors.append(f"Legacy 1.20 registry directory remains: {path.relative_to(ROOT)}")
        if len(parts) == 3 and parts[1] == "tags" and parts[2] in legacy_tag_roots:
            errors.append(f"Legacy 1.20 tag registry directory remains: {path.relative_to(ROOT)}")

    json_files = sorted(data.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")

    functions = list(data.rglob("*.mcfunction"))
    if not functions:
        errors.append("No .mcfunction files found")

    # My Own Loot used pre-1.20.5 item NBT. Catch regressions in its own
    # commands and loot tables while allowing legitimate block-entity NBT.
    mol_root = data / "mol"
    if mol_root.is_dir():
        import re
        for path in mol_root.rglob("*.mcfunction"):
            source = path.read_text(encoding="utf-8")
            if re.search(r"\b(?:item|Item)\.tag\b|\bCount:|\bCustomModelData:|\bBlockEntityTag:", source):
                errors.append(f"Legacy item-stack NBT remains: {path.relative_to(ROOT)}")

            # Function macro parameters are only expanded on lines prefixed
            # with '$'. Catch missing prefixes before they reach a server.
            for line_number, line in enumerate(source.splitlines(), start=1):
                stripped = line.lstrip()
                if stripped.startswith("#") or "$(" not in line:
                    continue
                if not stripped.startswith("$"):
                    errors.append(
                        f"Unexpanded function macro in {path.relative_to(ROOT)}:"
                        f"{line_number} (command is missing the leading '$')"
                    )

        for path in mol_root.rglob("*.json"):
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(document, dict):
                icon = document.get("display", {}).get("icon", {})
                if isinstance(icon, dict) and ("nbt" in icon or "item" in icon):
                    errors.append(f"Legacy advancement icon item format remains: {path.relative_to(ROOT)}")
            if re.search(r'"function"\s*:\s*"(?:(?:minecraft):)?copy_nbt"', path.read_text(encoding="utf-8")):
                errors.append(f"Legacy copy_nbt loot function remains: {path.relative_to(ROOT)}")

if errors:
    print("Datapack validation FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("Datapack structure and JSON validation passed.")
print("Note: this does not replace loading the pack in a Minecraft 1.21.1 server.")
