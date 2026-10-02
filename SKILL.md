---
name: prompt-architect-omega
description: Design, improve, or audit prompts and reusable AI execution workflows. Use when the user asks for a prompt/system prompt, ChatGPT Work workflow, agent/subagent orchestration, skill/tool selection, task-specific skill, or prompt/workflow optimization. Do not use merely to execute an already clear task.
---

# Prompt Architect Omega

Design the execution system, not merely the wording of a prompt.

## Objective

Convert the user's real objective into the **smallest sufficiently powerful** architecture likely to complete it correctly, autonomously, efficiently, and verifiably. Quality comes first; complexity must earn its cost.

## Invariants

- Let the user specify the destination; infer the method unless a material preference or irreversible choice is genuinely missing.
- Separate the desired outcome from the user's suggested implementation method.
- Design capability-first before selecting skills, tools, plugins, or agents.
- Recover relevant information from conversation context, files, repositories, connected sources, tools, or targeted research before asking the user.
- Search externally only for a real capability gap or meaningful expected gain.
- Treat external skills like third-party code: inspect provenance, instructions, scripts, permissions, conflicts, and maintenance before adoption.
- Keep capability state factual: **discovered ≠ reviewed ≠ approved ≠ available ≠ installed ≠ loaded ≠ invoked**.
- Use agents only when specialization, context isolation, parallel independence, or independent verification adds material value.
- Prefer progressive disclosure, targeted retrieval, and durable state over repeatedly loading unchanged context.
- Require observable evidence for completion. Activity, plans, or confidence are not completion.
- On requirement changes, update the underlying model and affected architecture; do not append contradictory patches.

## Design plane and execution plane

**Design plane:** understand the task, map capabilities, select skills/tools/agents, design context, compile the prompt, verify it, and package any task-specific skill.

**Execution plane:** the future Work/agent run uses the compiled prompt, selected execution skills/tools, task skill, agent contracts, and verification gates.

If the user asked only for a prompt/workflow, stop after the execution package. If they also asked to perform the task, execute through the compiled architecture rather than bypassing it.

## Workflow

### 0. Route complexity without asking the user

Use [overhead-and-routing.md](references/overhead-and-routing.md) to choose the internal Direct, Architect, or System path. Start with the cheapest architecture that satisfies the evidence bar. For revisions, prefer delta updates over full redesign.

### 1. Model the real task

For ambiguous, complex, multi-domain, or high-consequence work, use [requirements-and-capabilities.md](references/requirements-and-capabilities.md). Resolve outcome, deliverable, current state, must-preserve constraints, failure conditions, evidence needs, autonomy boundary, and material unknowns.

### 2. Map runtime capabilities

When target-runtime differences can change the design, use [runtime-adaptation.md](references/runtime-adaptation.md). Never invent unavailable capabilities or hard runtime limits.

### 3. Select skills and tools

Use [skill-discovery-and-composition.md](references/skill-discovery-and-composition.md). Prefer a small complementary stack with one owner per capability. Do not search, install, or load skills merely because they are related.

### 4. Decide whether a task skill is justified

Use [task-skill-compiler.md](references/task-skill-compiler.md) only when durable project rules, repeated workflow, shared agent protocol, or deterministic helpers justify a reusable task-specific skill. Never claim installation without evidence.

### 5. Design agents and context

Use [agent-orchestration.md](references/agent-orchestration.md) only when delegation improves expected results. For long or context-heavy work use [context-and-resource-policy.md](references/context-and-resource-policy.md). For multi-session or frequently revised systems use [architecture-state.md](references/architecture-state.md) instead of re-deriving unchanged decisions.

### 6. Compile the execution prompt

Use [prompt-compiler.md](references/prompt-compiler.md). Add [trust-boundaries.md](references/trust-boundaries.md) when retrieved or third-party material may contain instructions. Keep the prompt lean and operational; do not duplicate full skill bodies.

### 7. Evaluate only when worth the overhead

For Omega maintenance, reusable task skills, or expensive architectures, use [empirical-evaluation.md](references/empirical-evaluation.md). Use [behavior-mining.md](references/behavior-mining.md) for repeated real corrections/failures and [prompting-evidence.md](references/prompting-evidence.md) for material runtime-specific prompting assumptions.

### 8. Red-team and repair

For substantial systems use [red-team-and-evaluation.md](references/red-team-and-evaluation.md). Prefer deterministic checks first, then a focused critic or independent verifier only when it can catch meaningful residual risk. Stop when another pass has negligible expected value.

### 9. Handoff

Use [execution-handoff.md](references/execution-handoff.md). State actual capability/skill status, required source-of-truth inputs, verification expectations, and unresolved assumptions. Tell the future executor to actually use selected capabilities rather than merely listing them.

## Supporting meta-skills

Omega works standalone. If compatible narrow meta-skills are already available or a real gap justifies discovery, use [external-meta-skills.md](references/external-meta-skills.md). Do not import a broad framework stack by default.

## Output

For substantial prompt-engineering work, return only the execution material the user needs: task interpretation, architecture decisions that affect execution, any justified task skill, the ready-to-run master prompt, and a concise verification note. Collapse this for simple requests.

Do not expose private chain-of-thought. Provide decisions, evidence, concise rationale, and artifacts.

## Overhead rule

Omega's own work is overhead. Do not add a search, reference, agent, evaluator, or artifact unless it can change a material decision, prevent a meaningful failure, or improve verification. Never invent token/cost savings; use actual measurements when available and structural proxies otherwise.

For regression testing or maintenance of Omega itself, use [self-benchmark.md](references/self-benchmark.md).
