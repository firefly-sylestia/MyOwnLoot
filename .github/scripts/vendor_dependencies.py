#!/usr/bin/env python3
"""Fetch and vendor the 1.21.1-compatible Smithed libraries into the build tree.

The published ZIP remains a single self-contained datapack. LanternLoad is
already bundled in this repository under data/load and data/minecraft.
"""
from __future__ import annotations

import io
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
URL = (
    "https://api.smithed.dev/v2/download"
    "?pack=itemio&pack=custom-block&version=1.21.1&mode=datapack"
)
EXPECTED = {"itemio", "smithed.custom_block"}


def fail(message: str) -> None:
    raise SystemExit(f"Dependency vendoring failed: {message}")


request = urllib.request.Request(URL, headers={"User-Agent": "MyOwnLoot-1.21.1-build"})
try:
    with urllib.request.urlopen(request, timeout=60) as response:
        archive_bytes = response.read()
except Exception as exc:
    fail(f"could not download Smithed libraries: {exc}")

try:
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
except zipfile.BadZipFile:
    fail("Smithed API did not return a ZIP archive")

# Locate the datapack data/ root regardless of whether the API adds a wrapper
# directory around the archive contents.
members = [name for name in archive.namelist() if not name.endswith("/")]
data_roots: set[str] = set()
for name in members:
    parts = PurePosixPath(name).parts
    if "data" in parts:
        data_roots.add("/".join(parts[: parts.index("data") + 1]))

if not data_roots:
    fail("download archive contains no data/ directory")

# Remove the old bundled library namespaces so no 1.20.4-era files survive.
for namespace in EXPECTED:
    target = ROOT / "data" / namespace
    if target.exists():
        shutil.rmtree(target)

copied: set[str] = set()
for name in members:
    parts = PurePosixPath(name).parts
    if "data" not in parts:
        continue
    index = parts.index("data")
    if len(parts) <= index + 2:
        continue
    relative = Path(*parts[index:])
    # Never allow paths from an archive to escape the datapack.
    if relative.is_absolute() or ".." in relative.parts:
        fail(f"unsafe archive path: {name}")
    namespace = relative.parts[1]
    destination = ROOT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)

    if relative.name.endswith(".json") and "tags" in relative.parts and destination.exists():
        # Smithed libraries share LanternLoad's load tag with this datapack.
        try:
            existing = json.loads(destination.read_text(encoding="utf-8"))
            incoming = json.loads(archive.read(name).decode("utf-8"))
        except Exception as exc:
            fail(f"cannot merge tag file {relative}: {exc}")
        values = existing.setdefault("values", [])
        for value in incoming.get("values", []):
            if value not in values:
                values.append(value)
        destination.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    else:
        destination.write_bytes(archive.read(name))
    copied.add(namespace)

missing = EXPECTED - copied
if missing:
    fail("download did not contain expected namespaces: " + ", ".join(sorted(missing)))

print("Vendored ItemIO 1.3.3 and Smithed Custom Block 0.4.4 for Minecraft 1.21.1.")
print("LanternLoad remains bundled from the repository.")
