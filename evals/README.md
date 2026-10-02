# Omega Evaluation Runbook

This directory contains maintenance evals for Prompt Architect Omega. These files do not prove model quality by themselves; they define repeatable cases and evidence formats.

## 1. Trigger evaluation

Run the trigger cases in `trigger-evals.json` against the target runtime in a fresh environment. Record what actually happened:

```json
{
  "cases": [
    {"id": "t1", "actual": "trigger"},
    {"id": "n1", "actual": "no-trigger"}
  ]
}
```

Then score it:

```bash
python scripts/score_trigger_eval.py evals/trigger-evals.json observations.json
```

Keep dev and holdout results separate when interpreting changes. Do not tune the description on holdout failures and then continue calling the same cases holdout.

## 2. Baseline vs candidate execution

Run the same benchmark prompts in fresh, comparable environments.

Each run file uses:

```json
{
  "benchmark_version": "1.0",
  "cases": [
    {
      "id": "simple-rewrite",
      "output": "actual model output",
      "metrics": {
        "prompt_chars": 1200,
        "tool_calls": 0,
        "agents": 0
      }
    }
  ]
}
```

Only record metrics that were actually measured. Never estimate token counts or tool calls.

Prepare a blinded comparison:

```bash
python scripts/prepare_ab_eval.py baseline.json candidate.json --out-dir ab --seed 42
```

Give only `ab/blind-pack.json` and the evaluation rubric to an independent comparator. Do not provide `blind-key.json`.

The comparator returns:

```json
{
  "cases": [
    {
      "id": "simple-rewrite",
      "winner": "A",
      "reason": "More complete while remaining concise."
    }
  ]
}
```

Aggregate after judging:

```bash
python scripts/aggregate_ab_eval.py \
  baseline.json candidate.json ab/blind-key.json judgments.json \
  --output report.json
```

## 3. Promotion rule

Do not claim that a candidate is empirically better because deterministic repository tests passed.

A measured improvement claim should be supported by:

- identical benchmark inputs;
- comparable runtime/model/tool conditions;
- fresh runs rather than copied outputs;
- blind comparison where practical;
- actual overhead measurements when available;
- no material regression on trigger holdout or safety/completion gates.

When those conditions cannot be met, report the candidate as structurally validated rather than empirically superior.
