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

def write_skill(root: Path, body: str = "Do the task.\n") -> None:
    (root / "SKILL.md").write_text(
        "---\nname: validator-case\ndescription: Test validator behavior.\n---\n\n" + body,
        encoding="utf-8",
    )

def write_agent(
    root: Path,
    *,
    include_default: bool = True,
    include_policy: bool = True,
    include_interface: bool = True,
) -> None:
    (root / "agents").mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    if include_interface:
        lines.extend([
            "interface:",
            '  display_name: "Validator Case"',
            '  short_description: "Validate a test skill bundle"',
        ])
        if include_default:
            lines.append('  default_prompt: "Use this skill for the validator test."')
    else:
        lines.append('display_name: "Wrong level"')
    if include_policy:
        lines.extend([
            "policy:",
            "  allow_implicit_invocation: true",
        ])
    (root / "agents" / "openai.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")

def new_root(prefix: str) -> tuple[tempfile.TemporaryDirectory[str], Path]:
    td = tempfile.TemporaryDirectory(prefix=prefix)
    root = Path(td.name) / "validator-case"
    root.mkdir()
    return td, root

def main() -> int:
    # A minimal valid skill does not require agents/openai.yaml.
    td, root = new_root("omega-validator-no-agent-")
    try:
        write_skill(root)
        run(root, True)
    finally:
        td.cleanup()

    # Agent Skills optional frontmatter fields are accepted and type-checked.
    td, root = new_root("omega-validator-optional-frontmatter-")
    try:
        (root / "SKILL.md").write_text(
            """---
name: validator-case
description: Test optional Agent Skills frontmatter.
license: MIT
compatibility: >
  Requires a runtime with repository access.
metadata:
  author: OpenAI-compatible test
  version: "1.0"
allowed-tools: Read Write
---

Do the task.
""",
            encoding="utf-8",
        )
        run(root, True)
    finally:
        td.cleanup()

    td, root = new_root("omega-validator-bad-metadata-")
    try:
        (root / "SKILL.md").write_text(
            """---
name: validator-case
description: Test invalid metadata.
metadata:
  attempts: 3
---

Do the task.
""",
            encoding="utf-8",
        )
        run(root, False)
    finally:
        td.cleanup()

    td, root = new_root("omega-validator-bad-compatibility-")
    try:
        long_value = "x" * 501
        (root / "SKILL.md").write_text(
            f"---\nname: validator-case\ndescription: Test compatibility.\ncompatibility: {long_value}\n---\n\nDo the task.\n",
            encoding="utf-8",
        )
        run(root, False)
    finally:
        td.cleanup()

    td, root = new_root("omega-validator-unknown-frontmatter-")
    try:
        (root / "SKILL.md").write_text(
            """---
name: validator-case
description: Test unknown field.
imaginary-field: nope
---

Do the task.
""",
            encoding="utf-8",
        )
        run(root, False)
    finally:
        td.cleanup()

    # agents/openai.yaml is valid with only required interface fields.
    td, root = new_root("omega-validator-min-agent-")
    try:
        write_skill(root)
        write_agent(root, include_default=False, include_policy=False)
        run(root, True)
    finally:
        td.cleanup()

    # Valid inline YAML should not be rejected by the lightweight preflight validator.
    td, root = new_root("omega-validator-inline-agent-")
    try:
        write_skill(root)
        (root / "agents").mkdir(parents=True, exist_ok=True)
        (root / "agents" / "openai.yaml").write_text(
            'interface: {display_name: "Inline Case", short_description: "Inline metadata"}\n',
            encoding="utf-8",
        )
        run(root, True)
    finally:
        td.cleanup()

    # Omega-style optional fields are also valid.
    td, root = new_root("omega-validator-full-agent-")
    try:
        write_skill(root)
        write_agent(root)
        run(root, True)
    finally:
        td.cleanup()

    # If agents/openai.yaml exists, interface must be a mapping at the correct level.
    td, root = new_root("omega-validator-bad-agent-")
    try:
        write_skill(root)
        write_agent(root, include_interface=False, include_policy=False)
        run(root, False)
    finally:
        td.cleanup()

    td, root = new_root("omega-validator-empty-")
    try:
        write_skill(root, body="\n")
        run(root, False)
    finally:
        td.cleanup()

    td, root = new_root("omega-validator-duplicate-")
    try:
        write_skill(root)
        nested = root / "nested"
        nested.mkdir()
        (nested / "skill.md").write_text(
            "---\nname: duplicate\ndescription: Duplicate.\n---\n\nDuplicate.",
            encoding="utf-8",
        )
        run(root, False)
    finally:
        td.cleanup()

    print("VALIDATOR-TEST: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
