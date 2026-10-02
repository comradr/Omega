# Empirical Evaluation

Use empirical evaluation when Omega itself, a task skill, or a high-cost execution architecture is being improved.

## Differential evaluation

Compare the same task under:
- baseline architecture;
- candidate architecture.

Hold the task and evaluation criteria constant.

Observe where measurable:
- requirement coverage;
- correctness;
- capability/tool selection;
- false-completion resistance;
- verification quality;
- artifact quality;
- prompt/context overhead;
- calls/agents/time/tokens when actually available.

Never invent token counts.

## Blind comparison

When feasible, label outputs A/B without revealing old/new or baseline/candidate to the comparator. Judge both against the same rubric and evidence.

## Trigger evaluation

Maintain SHOULD TRIGGER and SHOULD NOT TRIGGER cases. Include informal language, typos, short requests, adjacent tasks, keyword traps, and multilingual cases when relevant.

Use held-out cases when optimizing the description. Do not overfit wording.

## Stopping rule

Empirical evaluation is itself overhead. Use it for changes whose regression risk or expected reuse justifies the cost; do not A/B-test every trivial prompt.


## Repository harness

When maintaining Omega itself, the repository includes a deterministic harness around externally produced model runs:

- `scripts/prepare_ab_eval.py` creates blinded A/B packs and a separate secret mapping key;
- `scripts/aggregate_ab_eval.py` resolves independent judgments and summarizes measured numeric overhead fields;
- `scripts/score_trigger_eval.py` scores observed activation behavior by dev/holdout split;
- `evals/README.md` defines the evidence format and promotion rules.

The harness deliberately does **not** fabricate model runs or token counts. Baseline and candidate outputs must come from actual comparable executions.
