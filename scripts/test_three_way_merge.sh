#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
rm -rf "$ROOT/work/merge-core" "$ROOT/work/merge-backpacks"
mkdir -p "$ROOT/work" "$ROOT/artifacts"

merge_repo() {
  local fabric_repo="$1"
  local official_repo="$2"
  local dir="$3"
  local report="$4"

  git clone --branch 1.21.x-fabric-dev "$fabric_repo" "$dir"
  cd "$dir"
  git config user.name "Fabric Port CI"
  git config user.email "fabric-port@example.invalid"
  git remote add official "$official_repo"
  git fetch official 1.21.8

  set +e
  git merge --no-commit --no-ff -X ours official/1.21.8 >merge.stdout 2>merge.stderr
  local status=$?
  set -e

  {
    echo "merge_status=$status"
    echo "head=$(git rev-parse HEAD)"
    echo "official=$(git rev-parse official/1.21.8)"
    echo "unmerged_files=$(git diff --name-only --diff-filter=U | wc -l)"
    echo "changed_files=$(git diff --cached --name-only | wc -l)"
    echo "neoforge_import_files=$(grep -RIl '^import net\.neoforged' src/main/java --include='*.java' 2>/dev/null | wc -l)"
    echo
    echo "--- UNMERGED ---"
    git diff --name-only --diff-filter=U || true
    echo
    echo "--- NEOFORGE IMPORT FILES ---"
    grep -RIl '^import net\.neoforged' src/main/java --include='*.java' 2>/dev/null | sort || true
    echo
    echo "--- MERGE STDOUT ---"
    cat merge.stdout || true
    echo "--- MERGE STDERR ---"
    cat merge.stderr || true
  } > "$report"
}

merge_repo https://github.com/Salandora/SophisticatedCore.git https://github.com/P3pp3rF1y/SophisticatedCore.git "$ROOT/work/merge-core" "$ROOT/artifacts/core-merge-report.txt"
merge_repo https://github.com/Salandora/SophisticatedBackpacks.git https://github.com/P3pp3rF1y/SophisticatedBackpacks.git "$ROOT/work/merge-backpacks" "$ROOT/artifacts/backpacks-merge-report.txt"
