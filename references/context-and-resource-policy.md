# Context and Resource Policy

Use this reference for long-running tasks, large repositories, multiple agents, repeated tool calls, or context pressure.

## Governing rule

Optimize **quality per unit of useful work**, not tokens in isolation.

Spend resources when they materially increase correctness, confidence, completeness, safety, or verification. Stop when another pass has negligible expected information value.

## 1. Context priority

Prefer, roughly in this order:

1. current user objective and constraints;
2. current task state/decisions;
3. directly relevant source material;
4. evidence and failure diagnostics;
5. concise specialist handoffs;
6. historical details only when still decision-relevant.

## 2. Progressive disclosure

Keep the active context lean. Load references, files, or specialist instructions just in time.

Prefer targeted retrieval over whole-repository reads. For large reference files, search for the relevant section first.

## 3. File-backed state

For long work, store durable state in files or supported persistent artifacts, for example:

- requirements/source-of-truth;
- project map;
- baseline/test status;
- decisions;
- issue ledger;
- completed/open work;
- verification matrix;
- agent handoffs.

Avoid making the conversation transcript the only memory system.

## 4. Observation offloading

Large tool outputs often have value only temporarily. Once their useful facts are captured, keep a reference/pointer or structured summary rather than repeatedly re-injecting the raw output—provided the raw source remains retrievable.

## 5. Compression safeguards

Compression is lossy. Preserve:

- unresolved requirements;
- must-preserve rules;
- decisions and their rationale when consequential;
- critical failures;
- evidence pointers;
- open risks;
- current completion status.

After a material user correction or requirement change, revalidate old summaries against the new source of truth.

## 6. Agent partitioning

Use isolated agent contexts when a problem naturally partitions or one context would become noisy. Do not partition merely because multiple agents are available.

## 7. Research/tool stopping rule

Before another expensive action ask:

- Is this information already available?
- Will this likely change a decision or catch a meaningful defect?
- Can related operations be batched?
- Can a smaller slice answer the question?
- Is the next research result likely to be novel rather than repetitive?

If not, stop.

## 8. Runtime limits

Do not invent token, time, agent-count, or cost limits. If the environment exposes real limits, incorporate them. If not, optimize adaptively from observed task complexity.

Prompt-stated budgets are advisory unless the runtime enforces them; do not rely on wording alone for hard safety/permission boundaries.
