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
    "curseforge_minecraft_versions": "1.21.8",
    "modrinth_minecraft_versions": "1.21.8",
}
for key, value in replacements.items():
    text = re.sub(rf"(?m)^{re.escape(key)}\s*=.*$", f"{key}={value}", text)
props.write_text(text, encoding="utf-8")

build = project / "build.gradle"
b = build.read_text(encoding="utf-8")
b = re.sub(
    r"id 'fabric-loom' version '[^']+'",
    "id 'fabric-loom' version '1.11.8'",
    b,
)

# Use Mojang's official 1.21.8 mappings while the port is being migrated.
b = re.sub(
    r"mappings\(loom\.layered \{\s*it\.officialMojangMappings\(\)\s*it\.parchment\([^\n]+\)\s*\}\)",
    "mappings loom.officialMojangMappings()",
    b,
    flags=re.S,
)

# SophisticatedFabricLib branch contains a publish placeholder here.
b = b.replace(
    'modImplementation "net.fabricmc.fabric-api:fabric-api:FABRIC_API_VERSION"',
    'modImplementation "net.fabricmc.fabric-api:fabric-api:${project.fabric_version}"',
)
build.write_text(b, encoding="utf-8")

wrapper = project / "gradle/wrapper/gradle-wrapper.properties"
w = wrapper.read_text(encoding="utf-8")
w = re.sub(
    r"(?m)^distributionUrl=.*$",
    r"distributionUrl=https\://services.gradle.org/distributions/gradle-8.14.4-bin.zip",
    w,
)
wrapper.write_text(w, encoding="utf-8")
