#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parent / "validate_skill.py"

def run(root: Path, expect_ok: bool) -> None:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(root)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if (proc.returncode == 0) != expect_ok:
        raise SystemExit(f"Unexpected validator result ({proc.returncode}):\n{proc.stdout}")

def write_minimal(root: Path, body: str = "Do the task.\n") -> None:
    (root / "agents").mkdir(parents=True)
    (root / "SKILL.md").write_text(
        "---\nname: validator-case\ndescription: Test validator behavior.\n---\n\n" + body,
        encoding="utf-8",
    )
    (root / "agents" / "openai.yaml").write_text(
        'interface:\n'
        '  display_name: "Validator Case"\n'
        '  short_description: "Validate a test skill bundle"\n'
        '  default_prompt: "Use $validator-case for this test."\n'
        'policy:\n'
        '  allow_implicit_invocation: true\n',
        encoding="utf-8",
    )

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="omega-validator-") as td:
        root = Path(td) / "validator-case"
        root.mkdir()
        write_minimal(root)
        run(root, True)

    with tempfile.TemporaryDirectory(prefix="omega-validator-empty-") as td:
        root = Path(td) / "validator-case"
        root.mkdir()
        write_minimal(root, body="\n")
        run(root, False)

    with tempfile.TemporaryDirectory(prefix="omega-validator-duplicate-") as td:
        root = Path(td) / "validator-case"
        root.mkdir()
        write_minimal(root)
        nested = root / "nested"
        nested.mkdir()
        (nested / "skill.md").write_text("---\nname: duplicate\ndescription: Duplicate.\n---\n\nDuplicate.", encoding="utf-8")
        run(root, False)

    print("VALIDATOR-TEST: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
