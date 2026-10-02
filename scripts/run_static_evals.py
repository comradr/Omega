#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    required_refs = {
        "routing": "overhead-and-routing.md",
        "runtime": "runtime-adaptation.md",
        "trust": "trust-boundaries.md",
        "behavior": "behavior-mining.md",
        "evidence": "prompting-evidence.md",
        "empirical": "empirical-evaluation.md",
    }
    for label, name in required_refs.items():
        if not (root / "references" / name).is_file():
            errors.append(f"missing {label}: {name}")

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    description_line = next(
        (line for line in skill.splitlines() if line.startswith("description:")),
        "",
    )
    discovery_description = description_line.split(":", 1)[1].strip() if ":" in description_line else ""
    if len(discovery_description) > 350:
        errors.append(
            f"skill discovery description grew to {len(discovery_description)} characters (>350 always-on overhead guard)"
        )

    core_lines = len(skill.splitlines())
    core_chars = len(skill)
    if core_lines > 120:
        errors.append(f"SKILL.md core grew to {core_lines} lines (>120 overhead guard)")
    if core_chars > 8000:
        errors.append(f"SKILL.md core grew to {core_chars} characters (>8000 overhead guard)")

    refs = "\n".join(p.read_text(encoding="utf-8").lower() for p in (root / "references").glob("*.md"))
    combined = skill.lower() + "\n" + refs
    anchors = [
        "architectural overhead",
        "runtime adaptation",
        "trust boundaries",
        "behavior mining",
        "empirical evaluation",
        "delta updates",
        "do not ask the user to choose a mode",
    ]
    for anchor in anchors:
        if anchor not in combined:
            errors.append(f"missing concept anchor: {anchor}")

    trigger = json.loads((root / "evals" / "trigger-evals.json").read_text(encoding="utf-8"))
    behavior = json.loads((root / "evals" / "behavior-evals.json").read_text(encoding="utf-8"))
    trigger_cases = trigger.get("cases", [])
    behavior_cases = behavior.get("cases", [])
    if len(trigger_cases) < 18:
        errors.append("trigger eval set must contain at least 18 cases")
    if not any(c.get("expect") == "trigger" for c in trigger_cases):
        errors.append("trigger eval set has no positive cases")
    if not any(c.get("expect") == "no-trigger" for c in trigger_cases):
        errors.append("trigger eval set has no negative cases")
    splits = {c.get("split") for c in trigger_cases}
    if not {"dev", "holdout"}.issubset(splits):
        errors.append("trigger eval set must contain both dev and holdout cases")
    holdout = [c for c in trigger_cases if c.get("split") == "holdout"]
    if not any(c.get("expect") == "trigger" for c in holdout):
        errors.append("holdout trigger eval set has no positive case")
    if not any(c.get("expect") == "no-trigger" for c in holdout):
        errors.append("holdout trigger eval set has no negative case")
    if len(behavior_cases) < 9:
        errors.append("behavior eval set must contain at least 9 cases")

    benchmark = json.loads((root / "evals" / "benchmark-cases.json").read_text(encoding="utf-8"))
    benchmark_cases = benchmark.get("cases", [])
    if len(benchmark_cases) < 12:
        errors.append("benchmark corpus must contain at least 12 cases")
    valid_routes = {"direct", "architect", "system"}
    for case in benchmark_cases:
        if case.get("route") not in valid_routes:
            errors.append(f"benchmark case {case.get('id')} has invalid route")
        if not case.get("must") or not isinstance(case.get("must_not"), list):
            errors.append(f"benchmark case {case.get('id')} lacks must/must_not contract")

    routing = (root / "references" / "overhead-and-routing.md").read_text(encoding="utf-8").lower()
    for phrase in ("no skill search", "no skill search, task skill, or agents", "skip it"):
        if phrase in routing:
            break
    else:
        errors.append("Direct routing does not explicitly suppress unnecessary machinery")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("STATIC-EVALS: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
