#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import re
import sys

src = Path(sys.argv[1])
ref = Path(sys.argv[2])
out = Path(sys.argv[3])
out.parent.mkdir(parents=True, exist_ok=True)

java_root = src / "src/main/java"
ref_java_root = ref / "src/main/java"
rows = []
imports = Counter()

for p in sorted(java_root.rglob("*.java")):
    text = p.read_text(encoding="utf-8", errors="replace")
    neo_imports = re.findall(r"^import\s+(net\.neoforged\.[^;]+);", text, flags=re.M)
    if not neo_imports:
        continue
    rel = p.relative_to(java_root)
    for imp in neo_imports:
        parts = imp.split(".")
        imports[".".join(parts[:4])] += 1
    rp = ref_java_root / rel
    rows.append((str(rel), len(neo_imports), rp.exists()))

with out.open("w", encoding="utf-8") as f:
    f.write(f"Official source: {src}\n")
    f.write(f"Fabric reference: {ref}\n")
    f.write(f"Java files with NeoForge imports: {len(rows)}\n")
    f.write(f"Same-path Fabric reference available: {sum(1 for _,_,x in rows if x)}\n")
    f.write(f"No same-path Fabric reference: {sum(1 for _,_,x in rows if not x)}\n\n")
    f.write("NeoForge import groups:\n")
    for k, v in imports.most_common():
        f.write(f"{v:4d} {k}\n")
    f.write("\nFiles:\n")
    for rel, count, exists in rows:
        f.write(f"{'REF' if exists else 'NEW'}\t{count:2d}\t{rel}\n")
