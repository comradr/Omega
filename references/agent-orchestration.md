# Agent and Subagent Orchestration

Use this reference when deciding whether work should remain single-agent or be split across specialists.

## Principle

Use agents for **context isolation, specialization, parallel independence, or independent verification**. Do not use them for organizational theater.

A reusable contract skeleton is available at [agent-contract-skeleton.md](../assets/agent-contract-skeleton.md) when explicit agent contracts are being produced.

## 1. Subagent justification test

A specialist is justified when at least one is materially true:

- the subtask is substantially independent;
- specialist expertise changes expected quality;
- fresh context reduces anchoring/interference;
- parallelism materially reduces wall-clock work or broadens exploration;
- independent verification lowers meaningful risk;
- keeping all work in one context would create excessive noise.

If none apply, keep the task with the primary architect/executor.

## 2. Primary architect ownership

One coordinator retains:

- user objective;
- requirements model;
- source-of-truth hierarchy;
- architecture decisions;
- conflict resolution;
- final synthesis and completion claim.

Do not let specialists redefine the task independently.

## 3. Agent contract

Every specialist receives:

**Objective** — one bounded responsibility.

**Inputs** — only required files/context/evidence.

**Boundaries** — what not to change or decide.

**Tools** — relevant tools only when routing matters.

**Output** — a concrete artifact or structured finding.

**Completion condition** — when the specialist stops.

**Handoff** — concise format back to the coordinator.

A useful default handoff is:

- status;
- findings;
- evidence/artifact pointers;
- risks;
- recommended action;
- unresolved items.

## 4. Standard specialist roles

Use only the useful subset:

- **Skill Scout:** discovers candidate skills; does not choose final architecture.
- **Domain Specialist:** checks domain-specific assumptions/procedures.
- **Research Specialist:** resolves targeted public factual uncertainty.
- **Context Architect:** designs state/persistence for unusually large runs.
- **Implementation Specialist:** owns a separable implementation component.
- **Prompt Red Team:** attacks ambiguity, loopholes, and false-completion paths in a fresh context.
- **QA Evaluator:** checks evidence against completion criteria.

## 5. Parallelism rules

Parallelize independent work; sequence dependent work.

When exploring uncertain solution spaces, engineer diversity by assigning different evidence slices or approach families—not decorative role names. Keep early workers independent when correlated anchoring is a risk, then synthesize later.

Do not use agreement among similar agents as proof. Agreement is weak evidence if they share assumptions, context, or model priors.

## 6. Context boundaries

Avoid giving every specialist the full project.

Prefer:

`targeted context → specialist artifact → structured handoff`

Do not return giant transcripts to the coordinator when file pointers, evidence, and conclusions suffice.

## 7. Verification independence

For consequential or long-running tasks, favor a fresh-context verifier that did not build the artifact. Give it an explicit failure-mode hunt list rather than "check carefully".

## 8. Supervisor-overload check

Before adding another agent, ask whether coordination cost exceeds the expected benefit. Warning signs:

- specialists need constant clarification from the coordinator;
- responsibilities overlap;
- the same large context is copied repeatedly;
- handoffs are larger than the work product;
- the coordinator spends most of its effort reconciling duplicated analysis.

Simplify topology when these appear.
