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

def parse_yaml_scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value.startswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed double-quoted YAML scalar") from exc
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ValueError("Malformed single-quoted YAML scalar")
        return value[1:-1].replace("''", "'")

    # Strip an unquoted YAML comment.
    comment = re.search(r"\s+#", value)
    if comment:
        value = value[: comment.start()].rstrip()

    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][-+]?\d+)?", value):
        return float(value)
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Parse the Agent Skills frontmatter subset without an external YAML dependency.

    The Agent Skills schema uses top-level scalar fields plus an optional
    string-to-string metadata mapping. Block scalars are supported for string fields.
    Complex YAML features outside that schema remain the platform validator's job.
    """
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")

    raw = text[4:end]
    lines = raw.splitlines()
    fields: dict[str, object] = {}
    i = 0

    while i < len(lines):
        raw_line = lines[i]
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            i += 1
            continue
        if raw_line[:1].isspace():
            raise ValueError(f"Unexpected indentation in frontmatter line {i + 1}")
        if ":" not in raw_line:
            raise ValueError(f"Invalid frontmatter line {i + 1}: {raw_line!r}")

        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise ValueError(f"Empty frontmatter key on line {i + 1}")
        if key in fields:
            raise ValueError(f"Duplicate frontmatter key: {key}")

        # metadata is the only mapping-valued field in the Agent Skills schema.
        if key == "metadata" and not raw_value:
            metadata: dict[str, object] = {}
            i += 1
            while i < len(lines):
                nested = lines[i]
                if not nested.strip() or nested.lstrip().startswith("#"):
                    i += 1
                    continue
                if not nested[:1].isspace():
                    break
                stripped = nested.strip()
                if ":" not in stripped:
                    raise ValueError(f"Invalid metadata entry on line {i + 1}")
                mkey, mvalue = stripped.split(":", 1)
                mkey = mkey.strip()
                if not mkey or mkey in metadata:
                    raise ValueError(f"Invalid or duplicate metadata key on line {i + 1}")
                metadata[mkey] = parse_yaml_scalar(mvalue)
                i += 1
            fields[key] = metadata
            continue

        # Accept an inline metadata map as valid YAML without pretending this
        # lightweight preflight can deeply parse every YAML flow-style edge case.
        if key == "metadata" and raw_value.startswith("{") and raw_value.endswith("}"):
            fields[key] = {"__inline__": raw_value}
            i += 1
            continue

        # Support YAML literal/folded block scalars used by string fields.
        if raw_value in {"|", "|-", "|+", ">", ">-", ">+"}:
            fold = raw_value.startswith(">")
            block: list[str] = []
            i += 1
            while i < len(lines):
                nested = lines[i]
                if nested and not nested[:1].isspace():
                    break
                if not nested.strip():
                    block.append("")
                    i += 1
                    continue
                block.append(nested.lstrip())
                i += 1
            fields[key] = (" " if fold else "\n").join(block).strip()
            continue

        fields[key] = parse_yaml_scalar(raw_value)
        i += 1

    return fields, text[end + 5 :]


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed quoted YAML scalar") from exc
    return value


def parse_agent_metadata(text: str) -> dict[str, dict[str, object]]:
    """Parse the small subset of agents/openai.yaml needed by this validator.

    This intentionally validates section structure without adding a PyYAML runtime
    dependency to every generated skill.
    """
    sections: dict[str, dict[str, object]] = {}
    current: str | None = None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        leading = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in leading:
            raise ValueError(f"Tabs are not supported in agents/openai.yaml indentation on line {lineno}")
        indent = len(leading)
        stripped = raw.strip()
        if indent == 0:
            if ":" not in stripped:
                raise ValueError(f"Expected top-level mapping key on line {lineno}")
            key, value = stripped.split(":", 1)
            current = key.strip()
            if not current:
                raise ValueError(f"Empty top-level key on line {lineno}")
            sections.setdefault(current, {})
            if value.strip():
                # Valid YAML also permits inline mappings. Without a YAML dependency,
                # record the value and let the platform perform full schema validation.
                sections[current]["__inline__"] = value.strip()
            continue
        if current is None:
            raise ValueError(f"Nested value before top-level section on line {lineno}")
        if ":" not in stripped:
            raise ValueError(f"Malformed mapping entry on line {lineno}")
        key, value = stripped.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Empty mapping key on line {lineno}")
        if not value.strip():
            # Nested mappings such as dependencies.tools are outside the fields
            # this lightweight validator needs; keep the key as a marker.
            sections[current][key] = {}
            continue
        sections[current][key] = parse_scalar(value)
    return sections

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

        allowed_frontmatter = {
            "name",
            "description",
            "license",
            "compatibility",
            "metadata",
            "allowed-tools",
        }
        extra = set(fields) - allowed_frontmatter
        if extra:
            errors.append(f"Unsupported Agent Skills frontmatter fields: {sorted(extra)}")

        name = fields.get("name", "")
        description = fields.get("description", "")
        license_value = fields.get("license")
        compatibility = fields.get("compatibility")
        metadata = fields.get("metadata")
        allowed_tools = fields.get("allowed-tools")

        if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append("Invalid skill name")
        if args.strict_folder_name and isinstance(name, str) and name and root.name != name:
            errors.append(f"Folder name '{root.name}' must match skill name '{name}'")
        if not isinstance(description, str) or not description or len(description) > 1024:
            errors.append("Description must be a non-empty string of at most 1,024 characters")

        if license_value is not None and not isinstance(license_value, str):
            errors.append("license must be a string when provided")
        if compatibility is not None:
            if not isinstance(compatibility, str) or not (1 <= len(compatibility) <= 500):
                errors.append("compatibility must be a non-empty string of at most 500 characters")
        if allowed_tools is not None and not isinstance(allowed_tools, str):
            errors.append("allowed-tools must be a space-separated string when provided")
        if metadata is not None:
            if not isinstance(metadata, dict):
                errors.append("metadata must be a string-to-string mapping")
            elif "__inline__" in metadata:
                warnings.append("inline metadata YAML accepted; deep metadata validation deferred to platform")
            else:
                for mkey, mvalue in metadata.items():
                    if not isinstance(mkey, str) or not isinstance(mvalue, str):
                        errors.append("metadata keys and values must be strings")
                        break
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

    # agents/openai.yaml is optional in the OpenAI skill format.
    # If present, its interface mapping has required display metadata; default_prompt
    # and policy fields remain optional.
    agent = root / "agents" / "openai.yaml"
    if agent.is_file():
        try:
            agent_text = agent.read_text(encoding="utf-8")
            sections = parse_agent_metadata(agent_text)
        except (UnicodeDecodeError, ValueError) as exc:
            errors.append(f"Invalid agents/openai.yaml: {exc}")
            sections = {}

        interface = sections.get("interface")
        if not isinstance(interface, dict):
            errors.append("agents/openai.yaml must contain an interface mapping")
        elif "__inline__" in interface:
            warnings.append("agents/openai.yaml uses inline interface YAML; deep field validation deferred to platform")
        else:
            display = interface.get("display_name")
            short = interface.get("short_description")
            default = interface.get("default_prompt")
            if not isinstance(display, str) or not display.strip():
                errors.append("agents/openai.yaml interface.display_name must be a non-empty string")
            if not isinstance(short, str) or not short.strip():
                errors.append("agents/openai.yaml interface.short_description must be a non-empty string")
            if default is not None and (not isinstance(default, str) or not default.strip()):
                errors.append("agents/openai.yaml interface.default_prompt must be non-empty when provided")

        policy = sections.get("policy")
        if policy is not None:
            if not isinstance(policy, dict):
                errors.append("agents/openai.yaml policy must be a mapping when provided")
            elif "__inline__" in policy:
                warnings.append("agents/openai.yaml uses inline policy YAML; deep field validation deferred to platform")
            else:
                implicit = policy.get("allow_implicit_invocation")
                if implicit is not None and not isinstance(implicit, bool):
                    errors.append("agents/openai.yaml policy.allow_implicit_invocation must be boolean when provided")
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
                valid_splits = {"dev", "holdout"}
                for case in cases:
                    if case.get("expect") not in valid:
                        errors.append(f"{p.relative_to(root)} case {case.get('id')} has invalid expect")
                    if case.get("split") not in valid_splits:
                        errors.append(f"{p.relative_to(root)} case {case.get('id')} has invalid split")
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
