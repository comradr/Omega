#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

def load_run(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise SystemExit(f"{path}: cases[] must be non-empty")
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise SystemExit(f"{path}: each case must be an object")
        case_id = case.get("id")
        output = case.get("output")
        if not isinstance(case_id, str) or not case_id:
            raise SystemExit(f"{path}: every case needs a non-empty id")
        if case_id in seen:
            raise SystemExit(f"{path}: duplicate case id {case_id}")
        if not isinstance(output, str):
            raise SystemExit(f"{path}: case {case_id} output must be a string")
        seen.add(case_id)
    return data

def index_cases(data: dict) -> dict[str, dict]:
    return {case["id"]: case for case in data["cases"]}

def main() -> int:
    ap = argparse.ArgumentParser(description="Create a blinded A/B comparison pack.")
    ap.add_argument("baseline", type=Path)
    ap.add_argument("candidate", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    baseline = load_run(args.baseline)
    candidate = load_run(args.candidate)
    b = index_cases(baseline)
    c = index_cases(candidate)

    if baseline.get("benchmark_version") != candidate.get("benchmark_version"):
        raise SystemExit(
            f"Benchmark versions differ: baseline={baseline.get('benchmark_version')!r}, "
            f"candidate={candidate.get('benchmark_version')!r}"
        )

    if set(b) != set(c):
        missing_b = sorted(set(c) - set(b))
        missing_c = sorted(set(b) - set(c))
        raise SystemExit(f"Case sets differ. Missing baseline={missing_b}; missing candidate={missing_c}")

    rng = random.Random(args.seed)
    blind_cases: list[dict] = []
    key_cases: list[dict] = []

    for case_id in sorted(b):
        flip = bool(rng.getrandbits(1))
        if flip:
            a_name, a_output = "candidate", c[case_id]["output"]
            b_name, b_output = "baseline", b[case_id]["output"]
        else:
            a_name, a_output = "baseline", b[case_id]["output"]
            b_name, b_output = "candidate", c[case_id]["output"]

        blind_cases.append({"id": case_id, "A": a_output, "B": b_output})
        key_cases.append({"id": case_id, "A": a_name, "B": b_name})

    args.out_dir.mkdir(parents=True, exist_ok=True)
    blind = {
        "benchmark_version": baseline.get("benchmark_version"),
        "cases": blind_cases,
    }
    key = {"seed": args.seed, "cases": key_cases}

    (args.out_dir / "blind-pack.json").write_text(
        json.dumps(blind, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.out_dir / "blind-key.json").write_text(
        json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Prepared {len(blind_cases)} blinded cases in {args.out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
