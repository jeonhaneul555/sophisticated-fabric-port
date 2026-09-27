#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$ROOT/work"
rm -rf "$WORK"
mkdir -p "$WORK"

# Exact Minecraft 1.21.8 official sources (functional baseline)
git clone --depth 1 --branch 1.21.8 https://github.com/P3pp3rF1y/SophisticatedCore.git "$WORK/core"
git clone --depth 1 --branch 1.21.8 https://github.com/P3pp3rF1y/SophisticatedBackpacks.git "$WORK/backpacks"

# Existing GPL Fabric ports used only as loader-port references.
git clone --depth 1 --branch 1.21.x-fabric https://github.com/Salandora/SophisticatedCore.git "$WORK/ref-core"
git clone --depth 1 --branch 1.21.x-fabric https://github.com/Salandora/SophisticatedBackpacks.git "$WORK/ref-backpacks"

python3 "$ROOT/scripts/analyze_port.py" "$WORK/core" "$WORK/ref-core" "$ROOT/artifacts/core-port-report.txt"
python3 "$ROOT/scripts/analyze_port.py" "$WORK/backpacks" "$WORK/ref-backpacks" "$ROOT/artifacts/backpacks-port-report.txt"

printf 'Prepared official 1.21.8 sources and Fabric references.\n'
