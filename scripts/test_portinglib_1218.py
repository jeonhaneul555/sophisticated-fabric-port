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
b = re.sub(r'^\s*mod(?:CompileOnly|LocalRuntime)\("com\.terraformersmc:modmenu:.*$', '', b, flags=re.M)
build.write_text(b, encoding="utf-8")

# The 1.21.11 gametest helper is development-only and references post-1.21.8 names.
settings = p / "settings.gradle"
st = settings.read_text(encoding="utf-8")
st = st.replace('if (isModuleDir(file)) {\n\t\tString name = file.name', 'if (isModuleDir(file)) {\n\t\tString name = file.name\n\t\tif (name == "gametest") continue')
settings.write_text(st, encoding="utf-8")

# This client render-state field does not exist in 1.21.8 and is unrelated to the modules used by Sophisticated.
aw = p / "modules/base/src/main/resources/porting_lib_base.accesswidener"
a = aw.read_text(encoding="utf-8")
a = "\n".join(line for line in a.splitlines() if "LevelRenderer levelRenderState" not in line) + "\n"
aw.write_text(a, encoding="utf-8")

wrapper = p / "gradle/wrapper/gradle-wrapper.properties"
w = wrapper.read_text(encoding="utf-8")
w = re.sub(r"(?m)^distributionUrl=.*$", r"distributionUrl=https\://services.gradle.org/distributions/gradle-8.14.4-bin.zip", w)
wrapper.write_text(w, encoding="utf-8")
