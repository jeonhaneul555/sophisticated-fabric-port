#!/usr/bin/env python3
from pathlib import Path
import re

p = Path("work/porting-lib")
props = p / "gradle.properties"
s = props.read_text(encoding="utf-8")
changes = {
    "loom_version": "1.11.8",
    "minecraft_version": "1.21.8",
    "minecraft_dependency": ">=1.21.8 <1.21.9",
    "loader_version": "0.19.4",
    "fabric_api_version": "0.136.1+1.21.8",
    "parchment_minecraft_version": "none",
    "parchment_version": "none",
}
for key, value in changes.items():
    s = re.sub(rf"(?m)^\s*{re.escape(key)}\s*=.*$", f"{key} = {value}", s)
props.write_text(s, encoding="utf-8")

build = p / "build.gradle"
b = build.read_text(encoding="utf-8")
# Development-only Mod Menu build for 1.21.11 is not needed for library compilation.
b = re.sub(r'^\s*mod(?:CompileOnly|LocalRuntime)\("com\.terraformersmc:modmenu:.*$', '', b, flags=re.M)
build.write_text(b, encoding="utf-8")

wrapper = p / "gradle/wrapper/gradle-wrapper.properties"
w = wrapper.read_text(encoding="utf-8")
w = re.sub(r"(?m)^distributionUrl=.*$", r"distributionUrl=https\://services.gradle.org/distributions/gradle-8.14.4-bin.zip", w)
wrapper.write_text(w, encoding="utf-8")
