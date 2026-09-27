#!/usr/bin/env python3
from pathlib import Path
import re
import sys

project = Path(sys.argv[1])
props = project / "gradle.properties"
text = props.read_text(encoding="utf-8")
replacements = {
    "minecraft_version": "1.21.8",
    "fabric_version": "0.136.1+1.21.8",
    "loader_version": "0.19.4",
    "release_versions": "1.21.8",
}
for key, value in replacements.items():
    text = re.sub(rf"(?m)^{re.escape(key)}\s*=.*$", f"{key}={value}", text)
props.write_text(text, encoding="utf-8")

build = project / "build.gradle"
b = build.read_text(encoding="utf-8")
b = b.replace("id 'fabric-loom' version '1.10.+'", "id 'fabric-loom' version '1.11.8'")

# Parchment 1.21 mappings cannot safely be layered over Minecraft 1.21.8.
# Start from Mojang's official 1.21.8 mappings.
b = re.sub(
    r"mappings\(loom\.layered \{\s*it\.officialMojangMappings\(\)\s*it\.parchment\([^\n]+\)\s*\}\)",
    "mappings loom.officialMojangMappings()",
    b,
    flags=re.S,
)

build.write_text(b, encoding="utf-8")
