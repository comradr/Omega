#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID = {"trigger", "no-trigger"}

def main() -> int:
    ap = argparse.ArgumentParser(description="Score observed skill activation against trigger evals.")
    ap.add_argument("evals", type=Path)
    ap.add_argument("observations", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    expected_data = json.loads(args.evals.read_text(encoding="utf-8"))
    observed_data = json.loads(args.observations.read_text(encoding="utf-8"))

    expected = {c["id"]: c for c in expected_data.get("cases", [])}
    observed = {c["id"]: c for c in observed_data.get("cases", [])}
    if set(expected) != set(observed):
        raise SystemExit("Trigger evals and observations must contain identical case ids")

    buckets: dict[str, dict[str, int]] = {}
    details: list[dict] = []
    for case_id in sorted(expected):
        exp = expected[case_id].get("expect")
        act = observed[case_id].get("actual")
        split = expected[case_id].get("split", "unspecified")
        if exp not in VALID or act not in VALID:
            raise SystemExit(f"Case {case_id} has invalid trigger label")
        bucket = buckets.setdefault(split, {"correct": 0, "total": 0, "false_positive": 0, "false_negative": 0})
        bucket["total"] += 1
        correct = exp == act
        bucket["correct"] += int(correct)
        if exp == "no-trigger" and act == "trigger":
            bucket["false_positive"] += 1
        if exp == "trigger" and act == "no-trigger":
            bucket["false_negative"] += 1
        details.append({"id": case_id, "split": split, "expected": exp, "actual": act, "correct": correct})

    for bucket in buckets.values():
        bucket["accuracy"] = bucket["correct"] / bucket["total"] if bucket["total"] else 0.0

    total = sum(x["total"] for x in buckets.values())
    correct = sum(x["correct"] for x in buckets.values())
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
