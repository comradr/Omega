#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|CHANGEME)\b", re.IGNORECASE)
MAX_FILES = 500
MAX_FILE_BYTES = 25 * 1024 * 1024

def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key:
            raise ValueError("Empty frontmatter key")
        if value.startswith('"'):
            try:
                parsed = json.loads(value)
                if not isinstance(parsed, str):
                    raise ValueError
                value = parsed
            except Exception as exc:
                raise ValueError(f"Invalid quoted scalar for {key}") from exc
        fields[key] = value
    return fields, text[end + 5 :]

def parse_simple_yaml_scalars(text: str) -> dict[str, object]:
    out: dict[str, object] = {}
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        key, value = raw.strip().split(":", 1)
        value = value.strip()
        if not value:
            continue
        if value in {"true", "false"}:
            parsed: object = value == "true"
        elif value.startswith('"'):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                parsed = value.strip('"')
        else:
            parsed = value
        out[key] = parsed
    return out

def resolve_markdown_link(source: Path, target: str, root: Path) -> Path | None:
    target = target.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "skills://")):
        return None
    target = target.split("#", 1)[0]
    if not target:
        return None
    return (source.parent / target).resolve()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--strict-folder-name", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    all_files = [p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    if len(all_files) > MAX_FILES:
        errors.append(f"Skill contains {len(all_files)} files; OpenAI limit is {MAX_FILES}")
    for p in all_files:
        if p.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{p.relative_to(root)} exceeds the 25 MB uncompressed file limit")

    manifests = [p for p in all_files if p.name.lower() == "skill.md"]
    if len(manifests) != 1:
        errors.append(f"Exactly one SKILL.md/skill.md is required; found {len(manifests)}")

    skill = root / "SKILL.md"
    if not skill.is_file() and len(manifests) == 1:
        skill = manifests[0]

    if not skill.is_file():
        errors.append("Missing SKILL.md")
        name = ""
    else:
        text = skill.read_text(encoding="utf-8")
        try:
            fields, body = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(str(exc))
            fields, body = {}, ""

        extra = set(fields) - {"name", "description"}
        if extra:
            errors.append(f"Unsupported frontmatter fields: {sorted(extra)}")

        name = fields.get("name", "")
        description = fields.get("description", "")

        if not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append("Invalid skill name")
        if args.strict_folder_name and name and root.name != name:
            errors.append(f"Folder name '{root.name}' must match skill name '{name}'")
        if not description or len(description) > 1024:
            errors.append("Description must be non-empty and at most 1,024 characters")
        if not body.strip():
            errors.append("Skill instructions/body must be non-empty")
        if len(body.splitlines()) > 500:
            warnings.append("SKILL.md body exceeds 500 lines; consider progressive disclosure")
        if PLACEHOLDER_RE.search(body):
            errors.append("SKILL.md contains unresolved TODO/TBD/CHANGEME placeholder")

    for md in root.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"Invalid UTF-8 in {md.relative_to(root)}: {exc}")
            continue
        for target in MD_LINK_RE.findall(text):
            resolved = resolve_markdown_link(md, target, root)
            if resolved is None:
                continue
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"Markdown link escapes skill root: {md.relative_to(root)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"Broken local link: {md.relative_to(root)} -> {target}")

    agent = root / "agents" / "openai.yaml"
    if not agent.is_file():
        errors.append("Missing agents/openai.yaml")
    else:
        metadata = parse_simple_yaml_scalars(agent.read_text(encoding="utf-8"))
        display = metadata.get("display_name")
        short = metadata.get("short_description")
        default = metadata.get("default_prompt")
        implicit = metadata.get("allow_implicit_invocation")
        if not isinstance(display, str) or not display.strip():
            errors.append("agents/openai.yaml missing display_name")
        if not isinstance(short, str) or not short.strip():
            errors.append("short_description must be a non-empty string")
        if not isinstance(default, str) or (name and f"${name}" not in default):
            errors.append(f"default_prompt must reference ${name or '<skill-name>'}")
        if not isinstance(implicit, bool):
            errors.append("allow_implicit_invocation must be boolean")

    for p in root.rglob("*.py"):
        try:
            ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        except Exception as exc:
            errors.append(f"Python syntax error in {p.relative_to(root)}: {exc}")

    eval_dir = root / "evals"
    if eval_dir.exists():
        for p in eval_dir.glob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"Invalid JSON in {p.relative_to(root)}: {exc}")
                continue
            cases = data.get("cases")
            if not isinstance(cases, list) or not cases:
                errors.append(f"{p.relative_to(root)} must contain non-empty cases[]")
                continue
            ids = [c.get("id") for c in cases if isinstance(c, dict)]
            if len(ids) != len(set(ids)) or any(not x for x in ids):
                errors.append(f"{p.relative_to(root)} contains missing/duplicate case ids")
            if p.name == "trigger-evals.json":
                valid = {"trigger", "no-trigger"}
                for case in cases:
                    if case.get("expect") not in valid:
                        errors.append(f"{p.relative_to(root)} case {case.get('id')} has invalid expect")
                    if not isinstance(case.get("query"), str) or not case["query"].strip():
                        errors.append(f"{p.relative_to(root)} case {case.get('id')} has empty query")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    for w in warnings:
        print("WARNING:", w)
    print(f"VALID: {len(warnings)} warning(s)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
