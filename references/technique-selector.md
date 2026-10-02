# Technique Selector

Choose prompt mechanisms by the behavior required, not by named framework popularity.

Use only techniques that materially improve the task.

## Techniques

### Examples / few-shot
Use when examples communicate nuanced output behavior more reliably than prose. Keep examples representative and avoid teaching accidental quirks.

### Structured output
Use when another tool/process will consume the result, strict comparison is needed, or required fields are easy to omit.

### Decomposition
Use when dependencies or independent subtasks make a single undifferentiated pass unreliable. Do not decompose trivial work.

### Tool loop
Use when success requires observing live state, acting, reading diagnostics, and adapting.

### Verification
Use deterministic checks when possible. Add rubric/critic/independent verification only when deterministic checks cannot cover important failure modes.

### Counterexamples / non-counting outcomes
Use when the executor could satisfy the wording while missing the real goal.

### Context isolation
Use when unrelated source material or specialist work would pollute the main reasoning context.

### Trust boundary
Use when retrieved or supplied material may contain instructions that should be treated as data.

### Independent alternatives
Use when solution-space exploration matters and correlated first-pass assumptions are risky. Compare later; do not create decorative duplicate agents.

## Selection rule

For every added technique, be able to state the concrete failure mode or decision it improves. Otherwise omit it.
