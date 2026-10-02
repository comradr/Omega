#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID = {"trigger", "no-trigger"}

def index_cases(data: dict, path: Path, label_field: str) -> dict[str, dict]:
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise SystemExit(f"{path}: cases[] must be non-empty")
    out: dict[str, dict] = {}
    for case in cases:
        if not isinstance(case, dict):
            raise SystemExit(f"{path}: every case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise SystemExit(f"{path}: every case needs a non-empty id")
        if case_id in out:
            raise SystemExit(f"{path}: duplicate case id {case_id}")
        if case.get(label_field) not in VALID:
            raise SystemExit(f"{path}: case {case_id} has invalid {label_field}")
        out[case_id] = case
    return out

def main() -> int:
    ap = argparse.ArgumentParser(description="Score observed skill activation against trigger evals.")
    ap.add_argument("evals", type=Path)
    ap.add_argument("observations", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    expected_data = json.loads(args.evals.read_text(encoding="utf-8"))
    observed_data = json.loads(args.observations.read_text(encoding="utf-8"))
    expected = index_cases(expected_data, args.evals, "expect")
    observed = index_cases(observed_data, args.observations, "actual")

    if set(expected) != set(observed):
        missing_obs = sorted(set(expected) - set(observed))
        extra_obs = sorted(set(observed) - set(expected))
        raise SystemExit(f"Case sets differ. Missing observations={missing_obs}; extra observations={extra_obs}")

    buckets: dict[str, dict[str, int | float]] = {}
    details: list[dict] = []
    for case_id in sorted(expected):
        exp = expected[case_id]["expect"]
        act = observed[case_id]["actual"]
        split = expected[case_id].get("split", "unspecified")
        bucket = buckets.setdefault(
            split,
            {"correct": 0, "total": 0, "false_positive": 0, "false_negative": 0},
        )
        bucket["total"] += 1
        correct = exp == act
        bucket["correct"] += int(correct)
        if exp == "no-trigger" and act == "trigger":
            bucket["false_positive"] += 1
        if exp == "trigger" and act == "no-trigger":
            bucket["false_negative"] += 1
        details.append({"id": case_id, "split": split, "expected": exp, "actual": act, "correct": correct})

    for bucket in buckets.values():
        total = int(bucket["total"])
        bucket["accuracy"] = int(bucket["correct"]) / total if total else 0.0

    total = sum(int(x["total"]) for x in buckets.values())
    correct = sum(int(x["correct"]) for x in buckets.values())
    report = {
        "overall_accuracy": correct / total if total else 0.0,
        "splits": buckets,
        "details": details,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
