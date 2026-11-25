#!/usr/bin/env python3
"""Generate the 1.21.1 item modifier used to locate supported loot chests.

The datapack's inventory adapter currently transforms vanilla chest blocks into
vanilla barrels. Modded containers are deliberately excluded until a safe
block-specific adapter exists; treating a modded chest as a vanilla barrel
would leave a detached display entity and could damage the container.
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
