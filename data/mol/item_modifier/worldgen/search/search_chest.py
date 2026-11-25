#!/usr/bin/env python3
"""Generate the 1.21.1 item modifier used to locate locked structure chests.

The generated modifier adds coordinates to the marker item's custom_data
component. Container matching is delegated to the mol:containers block tag so
vanilla, common-tagged modded containers, and Cobblemon gilded chests are found.
Minecraft 1.20.5+ replaced set_nbt with set_custom_data.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUTPUT = Path(__file__).with_name("search_chest.json")

# The datapack searches each block position in the current 16x16 chunk.
X_RANGE = range(0, 16)
Y_RANGE = range(-64, 320)
Z_RANGE = range(0, 16)

modifiers = []
for x in X_RANGE:
    for y in Y_RANGE:
        for z in Z_RANGE:
            modifiers.append({
                "function": "minecraft:set_custom_data",
                "tag": {"x": x, "y": y, "z": z},
                "conditions": [
                    {
                        "condition": "minecraft:inverted",
                        "term": {
                            "condition": "minecraft:location_check",
                            "offsetX": x,
                            "offsetY": y,
                            "offsetZ": z,
                            "predicate": {
                                "block": {
                                    "nbt": '{"Lock":"§mol:chest"}'
                                }
                            }
                        }
                    },
                    {
                        "condition": "minecraft:location_check",
                        "offsetX": x,
                        "offsetY": y,
                        "offsetZ": z,
                        "predicate": {
                            "block": {"tag": "mol:containers"}
                        }
                    }
                ]
            })

OUTPUT.write_text(json.dumps(modifiers, separators=(",", ":")) + "\n", encoding="utf-8")
print(f"Generated {len(modifiers):,} 1.21.1 chest-location item modifiers: {OUTPUT}")
