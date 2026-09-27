#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$ROOT/work"
rm -rf "$WORK"
mkdir -p "$WORK"

git clone --depth 1 --branch 1.21.1-fabric https://github.com/Salandora/SophisticatedFabricLib.git "$WORK/fabriclib"
git clone --depth 1 --branch 1.21.x-fabric https://github.com/Salandora/SophisticatedCore.git "$WORK/core"
git clone --depth 1 --branch 1.21.x-fabric https://github.com/Salandora/SophisticatedBackpacks.git "$WORK/backpacks"

python3 "$ROOT/scripts/retarget.py" "$WORK/fabriclib"
python3 "$ROOT/scripts/retarget.py" "$WORK/core"
python3 "$ROOT/scripts/retarget.py" "$WORK/backpacks"

printf 'Prepared 1.21.8 sources.\n'
