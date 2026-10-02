#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def index_cases(data: dict, path: Path) -> dict[str, dict]:
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise SystemExit(f"{path}: missing cases[]")
    out: dict[str, dict] = {}
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            raise SystemExit(f"{path}: invalid case")
        if case["id"] in out:
            raise SystemExit(f"{path}: duplicate case id {case['id']}")
        out[case["id"]] = case
    return out

def numeric_metrics(cases: dict[str, dict]) -> dict[str, list[float]]:
    collected: dict[str, list[float]] = {}
    for case in cases.values():
        metrics = case.get("metrics", {})
        if not isinstance(metrics, dict):
            continue
        for key, value in metrics.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                collected.setdefault(key, []).append(float(value))
    return collected

def summarize_metrics(cases: dict[str, dict]) -> dict[str, dict[str, float]]:
    return {
        key: {"mean": mean(values), "sum": sum(values), "count": len(values)}
        for key, values in sorted(numeric_metrics(cases).items())
        if values
    }

def main() -> int:
    ap = argparse.ArgumentParser(description="Aggregate blinded Omega A/B judgments.")
    ap.add_argument("baseline", type=Path)
    ap.add_argument("candidate", type=Path)
    ap.add_argument("key", type=Path)
    ap.add_argument("judgments", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    baseline_data = load_json(args.baseline)
    candidate_data = load_json(args.candidate)
    key_data = load_json(args.key)
    judgments_data = load_json(args.judgments)

    baseline = index_cases(baseline_data, args.baseline)
    candidate = index_cases(candidate_data, args.candidate)
    key = index_cases(key_data, args.key)
    judgments = index_cases(judgments_data, args.judgments)

    case_ids = set(baseline)
    if not (case_ids == set(candidate) == set(key) == set(judgments)):
        raise SystemExit("baseline, candidate, key, and judgments must contain identical case ids")

    for case_id, mapping in key.items():
        if {mapping.get("A"), mapping.get("B")} != {"baseline", "candidate"}:
            raise SystemExit(f"{args.key}: case {case_id} must map A/B exactly once to baseline/candidate")

    counts = {"baseline": 0, "candidate": 0, "tie": 0}
    resolved: list[dict] = []

    for case_id in sorted(case_ids):
        winner = judgments[case_id].get("winner")
        if winner not in {"A", "B", "tie"}:
            raise SystemExit(f"{args.judgments}: case {case_id} winner must be A, B, or tie")
        if winner == "tie":
            actual = "tie"
        else:
            actual = key[case_id].get(winner)
            if actual not in {"baseline", "candidate"}:
                raise SystemExit(f"{args.key}: case {case_id} has invalid blind mapping")
        counts[actual] += 1
        resolved.append({
            "id": case_id,
            "blind_winner": winner,
            "actual_winner": actual,
            "reason": judgments[case_id].get("reason"),
        })

    decided = counts["baseline"] + counts["candidate"]
    candidate_rate = counts["candidate"] / decided if decided else None

    report = {
        "cases": len(case_ids),
        "wins": counts,
        "candidate_win_rate_excluding_ties": candidate_rate,
        "baseline_metrics": summarize_metrics(baseline),
        "candidate_metrics": summarize_metrics(candidate),
        "resolved": resolved,
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
