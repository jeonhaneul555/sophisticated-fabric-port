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
b = build.read_text(encoding="utf-8")nb = b.replace("id 'fabric-loom' version '1.10.+'", "id 'fabric-loom' version '1.11.8'")

# Parchment 1.21 mappings cannot safely be layered over Minecraft 1.21.8.
# Use Mojang's official 1.21.8 mappings first; parameter/Javadoc mappings can be restored later.
b = re.sub(
    r"mappings\(loom\.layered \{\s*it\.officialMojangMappings\(\)\s*it\.parchment\([^\n]+\)\s*\}\)",
    "mappings loom.officialMojangMappings()",
    b,
    flags=re.S,
)

# Public mirrors are already declared. Avoid GitHub Packages credentials during CI.
b = re.sub(
    r"\n\s*maven \{\s*name = \"GitHubPackages\"\s*url = uri\(\"https://maven\.pkg\.github\.com/Salandora/Porting-Lib\"\).*?\n\s*\}\n",
    "\n",
    b,
    flags=re.S,
)
b = re.sub(
    r"\n\s*maven \{\s*name = \"GitHubPackages\"\s*url = uri\(\"https://maven\.pkg\.github\.com/Salandora/SophisticatedCore\"\).*?\n\s*\}\n",
    "\n",
    b,
    flags=re.S,
)
build.write_text(b, encoding="utf-8")
