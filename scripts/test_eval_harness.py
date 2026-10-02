#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="omega-eval-") as td:
        work = Path(td)
        baseline = {
            "benchmark_version": "1.0",
            "cases": [
                {"id": "a", "output": "baseline a", "metrics": {"prompt_chars": 100, "agents": 2}},
                {"id": "b", "output": "baseline b", "metrics": {"prompt_chars": 200, "agents": 1}},
            ],
        }
        candidate = {
            "benchmark_version": "1.0",
            "cases": [
                {"id": "a", "output": "candidate a", "metrics": {"prompt_chars": 80, "agents": 0}},
                {"id": "b", "output": "candidate b", "metrics": {"prompt_chars": 120, "agents": 0}},
            ],
        }
        bpath, cpath = work / "baseline.json", work / "candidate.json"
        bpath.write_text(json.dumps(baseline), encoding="utf-8")
        cpath.write_text(json.dumps(candidate), encoding="utf-8")
        out_dir = work / "ab"

        run(str(ROOT / "scripts" / "prepare_ab_eval.py"), str(bpath), str(cpath), "--out-dir", str(out_dir), "--seed", "7")
        key = json.loads((out_dir / "blind-key.json").read_text(encoding="utf-8"))
        judgments = {"cases": []}
        for item in key["cases"]:
            winner = "A" if item["A"] == "candidate" else "B"
            judgments["cases"].append({"id": item["id"], "winner": winner, "reason": "candidate chosen in test"})
        jpath = work / "judgments.json"
        jpath.write_text(json.dumps(judgments), encoding="utf-8")
        report_path = work / "report.json"
        run(
            str(ROOT / "scripts" / "aggregate_ab_eval.py"),
            str(bpath), str(cpath), str(out_dir / "blind-key.json"), str(jpath),
            "--output", str(report_path),
        )
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report["wins"] != {"baseline": 0, "candidate": 2, "tie": 0}:
            raise SystemExit("A/B aggregation mapped blind winners incorrectly")

        evals = {
            "cases": [
                {"id": "t", "split": "dev", "expect": "trigger"},
                {"id": "n", "split": "holdout", "expect": "no-trigger"},
            ]
        }
        obs = {"cases": [{"id": "t", "actual": "trigger"}, {"id": "n", "actual": "no-trigger"}]}
        epath, opath, tpath = work / "triggers.json", work / "observations.json", work / "trigger-report.json"
        epath.write_text(json.dumps(evals), encoding="utf-8")
        opath.write_text(json.dumps(obs), encoding="utf-8")
        run(str(ROOT / "scripts" / "score_trigger_eval.py"), str(epath), str(opath), "--output", str(tpath))
        trigger_report = json.loads(tpath.read_text(encoding="utf-8"))
        if trigger_report["overall_accuracy"] != 1.0:
            raise SystemExit("Trigger scorer regression")

    print("EVAL-HARNESS-TEST: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
