#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from package_skill import package_files, sha256, skill_name

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MAX_PLUGIN_ZIP_BYTES = 100 * 1024 * 1024
MAX_PLUGIN_ENTRIES = 5000
MAX_PLUGIN_FILE_BYTES = 100 * 1024 * 1024
MAX_PLUGIN_UNCOMPRESSED_BYTES = 512 * 1024 * 1024

def read_version(root: Path) -> str:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION is empty")
    return version

def plugin_manifest(root: Path, name: str, version: str) -> dict:
    return {
        "$schema": PLUGIN_SCHEMA,
        "name": name,
        "version": version,
        "description": "Design, audit, and compile lean AI execution systems and reusable prompt workflows.",
        "repository": "https://github.com/comradr/Omega",
        "keywords": ["prompt-engineering", "workflows", "agents", "skills"],
        "extensions": {
            "com.openai": {
                "interface": {
                    "displayName": "Prompt Architect Omega",
                    "shortDescription": "Design AI execution systems",
                    "longDescription": (
                        "Turn goals into lean, verifiable prompts, workflows, task skills, "
                        "and agent architectures. Omega routes complexity internally and "
                        "adds tools, skills, agents, and evaluation only when they materially "
                        "improve the result."
                    ),
                    "developerName": "comradr",
                    "category": "Developer Tools",
                    "capabilities": [
                        "Prompt and workflow architecture",
                        "Task-skill design",
                        "Agent orchestration",
                        "Context and verification design",
                    ],
                    "defaultPrompt": [
                        "Design the smallest reliable execution system for my goal."
                    ],
                }
            }
        },
    }

def validate_plugin_archive(archive: Path, skill: str) -> None:
    if archive.stat().st_size > MAX_PLUGIN_ZIP_BYTES:
        raise SystemExit(f"{archive.name} exceeds the 100 MB plugin ZIP limit")

    with zipfile.ZipFile(archive) as zf:
        members = [i for i in zf.infolist() if not i.is_dir()]
        if not members:
            raise SystemExit("Plugin ZIP is empty")
        if len(members) > MAX_PLUGIN_ENTRIES:
            raise SystemExit(f"Plugin ZIP has {len(members)} entries; limit is {MAX_PLUGIN_ENTRIES}")

        roots = {Path(i.filename).parts[0] for i in members}
        if len(roots) != 1:
            raise SystemExit("Plugin ZIP must contain exactly one plugin root")
        plugin_root = next(iter(roots))

        total = 0
        normalized: set[str] = set()
        for info in members:
            path = info.filename
            if "\\" in path or path.startswith("/") or ".." in Path(path).parts:
                raise SystemExit(f"Unsafe plugin archive path: {path}")
            norm = path.casefold()
            if norm in normalized:
                raise SystemExit(f"Plugin archive path collision: {path}")
            normalized.add(norm)
            if info.file_size > MAX_PLUGIN_FILE_BYTES:
                raise SystemExit(f"{path} exceeds 100 MiB")
            total += info.file_size

        if total > MAX_PLUGIN_UNCOMPRESSED_BYTES:
            raise SystemExit("Plugin archive exceeds 512 MiB uncompressed")

        required = {
            f"{plugin_root}/plugin.json",
            f"{plugin_root}/skills/{skill}/SKILL.md",
        }
        names = {i.filename for i in members}
        missing = sorted(required - names)
        if missing:
            raise SystemExit(f"Plugin ZIP is missing required files: {missing}")

        manifest = json.loads(zf.read(f"{plugin_root}/plugin.json").decode("utf-8"))
        if manifest.get("$schema") != PLUGIN_SCHEMA:
            raise SystemExit("Plugin manifest has wrong or missing Agent Plugins schema")
        if manifest.get("name") != skill:
            raise SystemExit("Plugin manifest name does not match packaged skill")
        if not manifest.get("version"):
            raise SystemExit("Plugin manifest version is empty")

        with tempfile.TemporaryDirectory(prefix="omega-plugin-") as td:
            zf.extractall(td)
            nested = Path(td) / plugin_root / "skills" / skill
            validator = nested / "scripts" / "validate_skill.py"
            subprocess.run(
                [sys.executable, str(validator), str(nested), "--strict-folder-name"],
                check=True,
            )

def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skill = skill_name(root)
    version = read_version(root)
    files = package_files(root)

    plugin_root = f"{skill}-plugin"
    out = root.parent / f"{skill}-plugin.zip"
    if out.exists():
        out.unlink()

    manifest_bytes = (
        json.dumps(plugin_manifest(root, skill, version), ensure_ascii=False, indent=2)
        + "\n"
    ).encode("utf-8")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{plugin_root}/plugin.json", manifest_bytes)
        for rel in files:
            zf.write(
                root / rel,
                Path(plugin_root) / "skills" / skill / rel,
            )

    validate_plugin_archive(out, skill)
    print(f"{out} sha256={sha256(out)} bytes={out.stat().st_size} skill_files={len(files)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
