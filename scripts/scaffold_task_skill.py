#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold a minimal task-specific Agent Skill.")
    ap.add_argument("name")
    ap.add_argument("--path", default=".")
    ap.add_argument("--description", required=True)
    ap.add_argument("--display-name")
    ap.add_argument("--with-references", action="store_true")
    ap.add_argument("--with-scripts", action="store_true")
    ap.add_argument(
        "--without-agent-metadata",
        action="store_true",
        help="Do not create optional agents/openai.yaml metadata.",
    )
    args = ap.parse_args()

    if len(args.name) > 64 or not NAME_RE.fullmatch(args.name):
        raise SystemExit("Invalid skill name: use lowercase letters, digits, and single hyphens")
    description = args.description.strip()
    if not description or len(description) > 1024:
        raise SystemExit("Description must be non-empty and at most 1,024 characters")

    display = (args.display_name or args.name.replace("-", " ").title()).strip()
    if not display:
        raise SystemExit("Display name must be non-empty")

    parent = Path(args.path)
    parent.mkdir(parents=True, exist_ok=True)
    root = parent / args.name
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty directory {root}")
    root.mkdir(parents=True, exist_ok=True)

    if args.with_references:
        (root / "references").mkdir(exist_ok=True)
    if args.with_scripts:
        (root / "scripts").mkdir(exist_ok=True)

    skill_md = f"""---
name: {args.name}
description: {json.dumps(description, ensure_ascii=False)}
---

# {display}

## Objective

Define the durable task-specific workflow and invariants here.

## Workflow

1. Inspect the source of truth.
2. Execute the task-specific procedure.
3. Verify observable completion criteria.
"""
    (root / "SKILL.md").write_text(skill_md, encoding="utf-8")

    if not args.without_agent_metadata:
        (root / "agents").mkdir(exist_ok=True)
        default_prompt = (
            "Use this task-specific workflow to execute the request according to "
            "its project rules and verification requirements."
        )
        agent_yaml = (
            "interface:\n"
            f"  display_name: {json.dumps(display, ensure_ascii=False)}\n"
            '  short_description: "Task-specific execution workflow"\n'
            f"  default_prompt: {json.dumps(default_prompt)}\n"
            "policy:\n"
            "  allow_implicit_invocation: true\n"
        )
        (root / "agents" / "openai.yaml").write_text(agent_yaml, encoding="utf-8")

    validator = Path(__file__).with_name("validate_skill.py")
    if validator.is_file():
        subprocess.run(
            [sys.executable, str(validator), str(root), "--strict-folder-name"],
            check=True,
        )

    print(root)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
