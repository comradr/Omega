# Master Prompt Compiler

Use this reference for substantial prompts, ChatGPT Work tasks, tool-using workflows, long-running agents, multi-agent orchestration, or strict deliverables.

## Principle

A prompt is an execution contract, not a transcript of the design discussion.

Compile only instructions that materially alter execution. Let skills and references carry reusable procedures when the environment supports them.

When choosing mechanisms such as examples, decomposition, structured output, context isolation, or independent alternatives, use [technique-selector.md](technique-selector.md) rather than importing a named prompt-framework stack.

A reusable output skeleton is available at [master-prompt-skeleton.md](../assets/master-prompt-skeleton.md). Copy/adapt it only when a file/template is useful; do not load it for trivial prompts.

## 1. Write the success predicate first

State the requested end condition as concretely as the domain permits.

For difficult long-running tasks, explicitly define:

- what must be true at return;
- what artifacts must exist;
- what evidence must support the result;
- what nearby outcomes **do not count** as completion.

Examples of non-counting outcomes:

- a plan instead of implementation;
- a partial audit when full coverage was requested;
- code changed but not built/tested;
- a reduction/hypothesis instead of a verified answer;
- a generated file that was never opened/validated.

## 2. Choose sections by need

Possible sections:

- **Mission / success predicate**
- **Context / current state**
- **Source of truth**
- **Objectives / non-objectives**
- **Inputs and assets**
- **Must-preserve constraints**
- **Selected skills/tools and their roles**
- **Agent topology and handoffs**
- **Workflow / dependency order**
- **Autonomy / approval boundaries**
- **Evidence and verification**
- **Failure recovery**
- **Deliverables**
- **Return condition / definition of done**
- **Reporting format**

Do not include a section if it does not change behavior.

## 3. Operationalize vague instructions

Convert wishes into observable procedures.

Instead of "don't break anything," say to establish the relevant baseline and run regression checks on affected core flows.

Instead of "be thorough," enumerate the dimensions that matter or define a coverage artifact.

Instead of "make it professional," define domain-specific quality criteria.

## 4. Source precedence

When files, documentation, existing behavior, and current user instructions can conflict, state their precedence explicitly.

## 5. Autonomy

Allow normal execution decisions without constant confirmation. Require escalation only for unavailable material preferences, destructive/irreversible actions, or conflicting requirements that cannot be resolved from evidence.

Do not tell the executor to ask questions that tools/files can answer.

## 6. Failure recovery

For fragile work, include a compact loop:

`observe failure → preserve diagnostics → identify likely cause → targeted correction → retry → verify → update task state`

Do not encourage blind repeated retries.

## 7. Verification

Completion is evidence-based. Distinguish:

- implemented;
- compiled/built;
- tested;
- independently verified;
- done.

Adapt to the domain.

## 8. Long-horizon prompts

For expensive autonomous runs, consider a pseudo-formal brief:

- define load-bearing terms;
- exact success predicate;
- explicit non-counting outcomes;
- agent/orchestration policy rather than fixed decorative roles;
- evidence-traceable reporting;
- adversarial audit with domain failure modes;
- return only when the artifact survives the audit.

Do not add persistence pressure without matching verification. Do not invent effort floors when they do not serve a real purpose.

## 9. Keep the prompt lean

Do not repeat full skill instructions inside the prompt when the skill will be available to the executor. Refer to the skill's role and let the runtime load it.

Avoid arbitrary personas, motivational filler, fake scores, repeated "IMPORTANT," and generic requests to "think harder."
