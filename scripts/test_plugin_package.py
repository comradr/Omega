#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="omega-plugin-test-") as td:
        workspace = Path(td) / "Omega"
        shutil_source = ROOT
        # package_plugin only reads the source tree and writes beside it. Copy the
        # repository so the regression test cannot alter a developer's real output.
        import shutil
        shutil.copytree(shutil_source, workspace, ignore=shutil.ignore_patterns("__pycache__", "*.zip", "*.skill"))
        subprocess.run(
            [sys.executable, str(workspace / "scripts" / "package_plugin.py"), str(workspace)],
            check=True,
        )
        archive = Path(td) / "prompt-architect-omega-plugin.zip"
        if not archive.is_file():
            raise SystemExit("Plugin packager did not create expected ZIP")

        with zipfile.ZipFile(archive) as zf:
            names = [i.filename for i in zf.infolist() if not i.is_dir()]
            roots = {Path(n).parts[0] for n in names}
            if roots != {"prompt-architect-omega-plugin"}:
                raise SystemExit(f"Unexpected plugin roots: {sorted(roots)}")
            manifest_path = "prompt-architect-omega-plugin/plugin.json"
            manifest = json.loads(zf.read(manifest_path).decode("utf-8"))
            if manifest.get("name") != "prompt-architect-omega":
                raise SystemExit("Plugin manifest name mismatch")
            if manifest.get("version") != (workspace / "VERSION").read_text(encoding="utf-8").strip():
                raise SystemExit("Plugin version does not match VERSION")
            skill_manifest = "prompt-architect-omega-plugin/skills/prompt-architect-omega/SKILL.md"
            if skill_manifest not in names:
                raise SystemExit("Plugin does not contain canonical Omega skill")

    print("PLUGIN-PACKAGE-TEST: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
