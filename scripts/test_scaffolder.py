#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "scripts" / "scaffold_task_skill.py"
VALIDATOR = ROOT / "scripts" / "validate_skill.py"

def main() -> int:
    description = """Handles: colon, #hash, "quotes", Windows C:\\Temp\\x, unicode Привет, braces {x}, apostrophe it's."""
    display = 'Hostile: "Skill" #1'

    with tempfile.TemporaryDirectory(prefix="omega-scaffold-") as td:
        subprocess.run([
            sys.executable, str(SCAFFOLD), "hostile-skill",
            "--path", td,
            "--description", description,
            "--display-name", display,
            "--with-references",
            "--with-scripts",
        ], check=True)
        child = Path(td) / "hostile-skill"
        skill = (child / "SKILL.md").read_text(encoding="utf-8")
        agent = (child / "agents" / "openai.yaml").read_text(encoding="utf-8")

        fm = skill.split("---", 2)[1]
        desc_line = next(line for line in fm.splitlines() if line.startswith("description:"))
        decoded = json.loads(desc_line.split(":", 1)[1].strip())
        if decoded != description:
            raise SystemExit("Description escaping did not round-trip")
        if "default_prompt:" not in agent:
            raise SystemExit("Generated agent metadata has no default_prompt")
        if "$hostile-skill" in agent:
            raise SystemExit("Generated default_prompt contains unsupported dollar-style skill invocation")

        subprocess.run([
            sys.executable, str(VALIDATOR), str(child), "--strict-folder-name"
        ], check=True)

    with tempfile.TemporaryDirectory(prefix="omega-scaffold-no-agent-") as td:
        subprocess.run([
            sys.executable, str(SCAFFOLD), "portable-skill",
            "--path", td,
            "--description", "A portable task workflow without OpenAI presentation metadata.",
            "--without-agent-metadata",
        ], check=True)
        child = Path(td) / "portable-skill"
        if (child / "agents" / "openai.yaml").exists():
            raise SystemExit("--without-agent-metadata unexpectedly created agents/openai.yaml")
        subprocess.run([
            sys.executable, str(VALIDATOR), str(child), "--strict-folder-name"
        ], check=True)

    with tempfile.TemporaryDirectory(prefix="omega-scaffold-invalid-") as td:
        proc = subprocess.run([
            sys.executable, str(SCAFFOLD), "invalid-skill",
            "--path", td,
            "--description", " ",
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if proc.returncode == 0:
            raise SystemExit("Scaffolder accepted an empty description")

    print("SCAFFOLDER-TEST: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
