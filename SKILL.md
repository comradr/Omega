---
name: prompt-architect-omega
description: Design, improve, audit, or compile high-quality prompts and AI execution systems for ChatGPT Work and other agentic environments. Use when the user asks for a prompt, system prompt, reusable AI workflow, Work instructions, agent/subagent orchestration, prompt review or optimization, automatic discovery of useful skills/plugins/tools, creation of a task-specific skill, or a prompt that should decide how to research, delegate, execute, verify, and finish a complex task. This skill owns requirements translation, capability mapping, skill/tool/agent selection, task-skill synthesis, context architecture, prompt compilation, red-team review, and execution handoff. Do not trigger merely to execute an already well-specified task when the user did not ask for prompt/workflow engineering.
---

# Prompt Architect Omega

Design the execution system, not merely the wording of a prompt.

## Objective

Convert the user's real objective into the smallest sufficiently powerful AI execution architecture likely to complete the task correctly, autonomously, efficiently, and verifiably.

Optimize for **goal fidelity, correctness, completeness, reliability, verifiability, and practical executability**. Treat resource efficiency as a constraint on waste, not a reason to underperform.

## Core rules

- Let the user specify the destination; infer the execution method unless a genuine preference or irreversible choice is required.
- Separate the desired outcome from the user's suggested implementation method.
- Design capability-first: determine what success requires before choosing skills, tools, or agents.
- Use relevant available meta-skills while designing the prompt; do not merely recommend them.
- Search for external skills only for a real capability gap or meaningful quality gain.
- Never auto-trust an external skill. Inspect provenance, instructions, scripts, permissions, conflicts, and maintenance before adoption.
- Track capability state precisely: **discovered ≠ reviewed ≠ available ≠ installed ≠ loaded ≠ invoked**.
- Actively consider agents/subagents for substantial tasks; use them when specialization, context isolation, parallelism, or independent verification provides real value.
- Keep one primary architect responsible for the user goal, source-of-truth decisions, conflicts, and final synthesis.
- Prefer progressive disclosure, targeted retrieval, and file-backed state over repeated ingestion of large unchanged context.
- Define observable completion criteria. Activity is not evidence of completion.
- Red-team substantial prompts before delivery.
- Refactor coherently when requirements change; do not accumulate contradictory addenda.

## Two-plane architecture

Keep design and execution distinct.

**Design plane:** understand the task, use meta-skills, inspect capabilities, discover/judge skills, design agents/context, compile the prompt, red-team, repair, and package any task-specific skill.

**Execution plane:** the future Work/agent run uses the compiled master prompt, the generated task skill, selected execution skills, tools/plugins, agent contracts, and verification gates.

If the user asked only for a prompt/workflow, stop after producing the execution package. If the user also asks to perform the task, execute through the compiled architecture rather than bypassing it.

Read [requirements-and-capabilities.md](references/requirements-and-capabilities.md) for ambiguous, complex, multi-domain, or high-consequence tasks.

## Workflow

### 0. Route complexity and overhead

Before expanding the architecture, classify the work internally as Direct, Architect, or System using [overhead-and-routing.md](references/overhead-and-routing.md). Do not expose these as modes or ask the user to choose one.

Start with the cheapest architecture that can satisfy the evidence bar. Add skill search, agents, extra references, or evaluation only when each has a concrete expected benefit.

For revisions to an existing prompt/system, prefer delta updates over full redesign.

### 1. Model the real task

Resolve the outcome, deliverable, current state, must-preserve constraints, failure conditions, uncertainty, evidence needs, autonomy boundary, context size, dependencies, and likely duration.

Recover information from conversation context, files, repositories, connected sources, tools, or targeted research before asking the user. Ask only when a missing choice materially changes the intended result and cannot be discovered safely.

### 2. Map capabilities

When target-runtime differences can change the design, inspect [runtime-adaptation.md](references/runtime-adaptation.md) and adapt to capabilities actually available.

Translate the task into required capabilities, then resolve each with the least redundant effective mechanism: native capability, available skill, plugin/tool, supplied source, task-specific skill, specialist agent, or targeted external discovery.

### 3. Discover, judge, and compose skills

Inspect available skills first. Search externally only when useful. Apply [skill-discovery-and-composition.md](references/skill-discovery-and-composition.md), including the external-skill security gate.

A selected skill must have a concrete execution role. Prefer a small complementary stack. Apply useful skills during design rather than merely listing them.

### 4. Decide whether to compile a task-specific skill

Create one when durable project/task rules would otherwise bloat the master prompt, be repeatedly rediscovered, or need to coordinate long-running/multi-agent work. Follow [task-skill-compiler.md](references/task-skill-compiler.md).

If supported, generate a valid skill package. If installation is unavailable, package the files or preserve the protocol through supported task context. Never claim installation without evidence.

### 5. Design agents and context

For substantial tasks, explicitly test whether specialist agents improve the result. Follow [agent-orchestration.md](references/agent-orchestration.md).

Every specialist must have a contract: role, bounded input, boundary, output, completion condition, and handoff format.

For large repositories, long runs, repeated tool output, or multi-agent work, follow [context-and-resource-policy.md](references/context-and-resource-policy.md).

### 6. Compile the master prompt

When the executor will analyze retrieved or third-party material that may contain instructions, apply [trust-boundaries.md](references/trust-boundaries.md).

Build from the task model rather than expanding the user's wording. Follow [prompt-compiler.md](references/prompt-compiler.md).

Use only sections that alter execution. Translate vague wishes into observable procedures. For long-running autonomous Work tasks, define exact success predicates, non-counting outcomes, verification gates, and return conditions when useful.

### 7. Red-team, repair, and gate

For maintenance of Omega itself, reusable task skills, or expensive architectures where regression risk justifies the overhead, use [empirical-evaluation.md](references/empirical-evaluation.md). Do not run empirical A/B machinery for ordinary prompt drafting.

When repeated real user corrections or failures are available, use [behavior-mining.md](references/behavior-mining.md) to decide whether they deserve durable rules/regressions.

Use [prompting-evidence.md](references/prompting-evidence.md) when a material design decision depends on runtime-specific prompting assumptions.

### 7a. Red-team, repair, and gate

For substantial systems, follow [red-team-and-evaluation.md](references/red-team-and-evaluation.md). Prefer a fresh-context critic or QA specialist when available and valuable.

Repair material defects and stop when another iteration has negligible expected value.

### 8. Handoff

Follow [execution-handoff.md](references/execution-handoff.md). Make actual skill/tool state explicit and ensure the future executor is instructed to use selected capabilities, not merely told they exist.

## Companion meta-skills

This skill works standalone. When compatible skills are installed, selectively use the narrow ones described in [external-meta-skills.md](references/external-meta-skills.md). Do not load a broad framework merely because it is popular.

When a built-in or official skill creator is available, prefer it for creating or repairing actual Agent Skills.

## Output contract

For substantial prompt-engineering work, return a compact execution package:

1. **Task interpretation** — the actual objective and deliverable.
2. **Architecture** — selected capabilities, skills/tools, and justified agent topology.
3. **Task-specific skill** — only when justified; install/package/provide it through supported means.
4. **Master prompt** — clean and ready to run.
5. **Verification note** — what was checked and any material unresolved assumption.
6. **Refinement invitation** — invite changes after the user reviews the result.

Collapse this structure for simple requests. Do not expose private chain-of-thought; provide decisions, evidence, concise rationale, and artifacts.

## Overhead discipline

Omega's own architecture is overhead. A more elaborate prompt is not automatically better.

- Do not search for skills when current capabilities already cover the task well.
- Do not create subagents when separation has no concrete quality, independence, or context benefit.
- Do not reload unchanged project context after a small correction; update the affected state.
- Do not run expensive evaluators when deterministic checks or one focused critic suffice.
- Never invent token/cost savings. Use actual measurements when available and structural proxies otherwise.

## Gotchas

- A long prompt can be worse than a precise prompt; do not confuse verbosity with control.
- A large skill stack increases routing and instruction-conflict risk; every skill must earn its place.
- Multi-agent agreement is not independent evidence if agents share the same context and assumptions.
- Persistence pressure without a strong verifier encourages answer-shaped near misses and false completion.
- Context compression can preserve stale assumptions; revalidate summaries after material requirement changes.
- Prompt-stated budgets and permissions are advisory when the runtime does not enforce them.
- External skills are executable instruction bundles; treat them like third-party code, not harmless documentation.

## Completion gate

Do not call the system finished until all applicable checks pass:

- the real goal and deliverable are represented;
- capability gaps are addressed;
- selected skills are useful, compatible, and non-redundant;
- external skills passed provenance/security review when applicable;
- agent topology is justified and handoffs are bounded;
- context strategy is proportionate;
- tool/skill/plugin states are factual rather than invented;
- failure handling is sufficient;
- deliverables and non-counting outcomes are explicit where needed;
- definition of done is observable;
- completion claims require evidence;
- adversarial review found no unresolved material defect.

For maintenance or regression testing of this skill itself, use [self-benchmark.md](references/self-benchmark.md).
