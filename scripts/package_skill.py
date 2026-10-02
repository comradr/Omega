#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RUNTIME_DIRS = {"agents", "assets", "references", "scripts", "evals"}
EXCLUDED_NAMES = {"test_scaffolder.py", "run_ci_checks.py"}
EXCLUDED_SUFFIXES = {".zip", ".skill"}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()

def skill_name(root: Path) -> str:
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end == -1:
        raise SystemExit("Invalid SKILL.md frontmatter")
    for line in text[4:end].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"')
    raise SystemExit("SKILL.md has no name")

def package_files(root: Path) -> list[str]:
    files = ["SKILL.md"]
    for dirname in sorted(RUNTIME_DIRS):
        base = root / dirname
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            if "__pycache__" in p.parts or p.name in EXCLUDED_NAMES:
                continue
            if p.suffix in EXCLUDED_SUFFIXES or p.name == ".DS_Store":
                continue
            files.append(str(p.relative_to(root)).replace("\\", "/"))
    return sorted(set(files))

def extracted_manifest(root: Path) -> list[str]:
    return sorted(
        str(p.relative_to(root)).replace("\\", "/")
        for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )

def run_validator(root: Path, strict: bool = False) -> None:
    cmd = [sys.executable, str(root / "scripts" / "validate_skill.py"), str(root)]
    if strict:
        cmd.append("--strict-folder-name")
    subprocess.run(cmd, check=True)

def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    run_validator(root, strict=False)
    name = skill_name(root)
    files = package_files(root)

    outputs: list[Path] = []
    for ext in ("zip", "skill"):
        out = root.parent / f"{name}.{ext}"
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel in files:
                zf.write(root / rel, Path(name) / rel)
        outputs.append(out)

    for out in outputs:
        with tempfile.TemporaryDirectory(prefix="omega-package-") as td:
            with zipfile.ZipFile(out) as zf:
                zf.extractall(td)
            extracted = Path(td) / name
            if extracted_manifest(extracted) != files:
                raise SystemExit(f"Manifest mismatch after packaging {out.name}")
            run_validator(extracted, strict=True)

    for out in outputs:
        print(f"{out} sha256={sha256(out)} files={len(files)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
