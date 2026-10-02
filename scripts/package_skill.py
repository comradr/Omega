#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RUNTIME_DIRS = {"agents", "assets", "references", "scripts", "evals"}
EXCLUDED_NAMES = {"test_scaffolder.py", "test_validator.py", "test_eval_harness.py", "test_plugin_package.py", "package_plugin.py", "run_ci_checks.py"}
EXCLUDED_SUFFIXES = {".zip", ".skill"}
MAX_FILES = 500
MAX_FILE_BYTES = 25 * 1024 * 1024
MAX_ZIP_BYTES = 50 * 1024 * 1024

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
    files = sorted(set(files))
    if len(files) > MAX_FILES:
        raise SystemExit(f"Package has {len(files)} files; OpenAI limit is {MAX_FILES}")
    for rel in files:
        if (root / rel).stat().st_size > MAX_FILE_BYTES:
            raise SystemExit(f"{rel} exceeds the 25 MB uncompressed file limit")
    return files

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

    zip_out = root.parent / f"{name}.zip"
    skill_out = root.parent / f"{name}.skill"
    for out in (zip_out, skill_out):
        if out.exists():
            out.unlink()

    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in files:
            zf.write(root / rel, Path(name) / rel)
    if zip_out.stat().st_size > MAX_ZIP_BYTES:
        raise SystemExit(f"{zip_out.name} exceeds the 50 MB upload limit")

    # OpenAI's documented skill-upload artifact is the ZIP. Keep .skill only as
    # a byte-identical compatibility alias for runtimes that explicitly accept it.
    shutil.copyfile(zip_out, skill_out)
    outputs = [zip_out, skill_out]

    for out in outputs:
        with tempfile.TemporaryDirectory(prefix="omega-package-") as td:
            with zipfile.ZipFile(out) as zf:
                roots = {Path(entry).parts[0] for entry in zf.namelist() if entry and not entry.endswith("/")}
                if roots != {name}:
                    raise SystemExit(f"{out.name} must contain exactly one top-level folder named {name}")
                zf.extractall(td)
            extracted = Path(td) / name
            if extracted_manifest(extracted) != files:
                raise SystemExit(f"Manifest mismatch after packaging {out.name}")
            run_validator(extracted, strict=True)

    if sha256(zip_out) != sha256(skill_out):
        raise SystemExit("Compatibility .skill artifact must be byte-identical to canonical ZIP")

    for out in outputs:
        print(f"{out} sha256={sha256(out)} files={len(files)} bytes={out.stat().st_size}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
