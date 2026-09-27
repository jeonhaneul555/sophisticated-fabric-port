#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$ROOT/work"
mkdir -p "$WORK" "$ROOT/artifacts"

merge_one() {
  local fabric_repo="$1"
  local official_repo="$2"
  local dir="$3"
  local report="$4"

  rm -rf "$dir"
  git clone --branch 1.21.x-fabric-dev "$fabric_repo" "$dir"
  cd "$dir"
  git config user.name "Fabric Port CI"
  git config user.email "fabric-port@example.invalid"
  git remote add official "$official_repo"
  git fetch official 1.21.8

  set +e
  git merge --no-commit --no-ff -X ours official/1.21.8
  set -e

  # Resolve remaining modify/delete and add/add conflicts deterministically.
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    stages="$(git ls-files -u -- "$f" || true)"
    has_ours=0
    has_theirs=0
    grep -q $'\t'"$f" <<<"$stages" && true
    awk '$3==2 {found=1} END{exit !found}' <<<"$stages" && has_ours=1 || true
    awk '$3==3 {found=1} END{exit !found}' <<<"$stages" && has_theirs=1 || true

    if [ "$has_ours" -eq 0 ] || [ "$has_theirs" -eq 0 ]; then
      # If either side deliberately removed a legacy file, keep it removed.
      git rm -f --ignore-unmatch -- "$f" >/dev/null 2>&1 || true
    elif [[ "$f" == src/generated/* ]] || [[ "$f" == src/main/resources/assets/* ]] || [[ "$f" == src/main/resources/data/* ]]; then
      git checkout --theirs -- "$f"
      git add -- "$f"
    else
      # Code conflicts keep the established Fabric implementation, then later
      # compiler-guided patches bring it to the 1.21.8 API.
      git checkout --ours -- "$f"
      git add -- "$f"
    fi
  done < <(git diff --name-only --diff-filter=U)

  git add -A
  git commit -m "Merge official 1.21.8 into Fabric port" >/dev/null

  python3 "$ROOT/scripts/retarget.py" "$dir"

  {
    echo "head=$(git rev-parse HEAD)"
    echo "official=$(git rev-parse official/1.21.8)"
    echo "neoforge_import_files=$(grep -RIl '^import net\.neoforged' src/main/java --include='*.java' 2>/dev/null | wc -l)"
    echo "java_files=$(find src/main/java -name '*.java' | wc -l)"
    echo
    grep -RIl '^import net\.neoforged' src/main/java --include='*.java' 2>/dev/null | sort || true
  } > "$report"
}

merge_one https://github.com/Salandora/SophisticatedCore.git https://github.com/P3pp3rF1y/SophisticatedCore.git "$WORK/core" "$ROOT/artifacts/core-merged-report.txt"
merge_one https://github.com/Salandora/SophisticatedBackpacks.git https://github.com/P3pp3rF1y/SophisticatedBackpacks.git "$WORK/backpacks" "$ROOT/artifacts/backpacks-merged-report.txt"
