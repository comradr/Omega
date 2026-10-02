# External Meta-Skills Strategy

This file records recommended companion capability families. They are optional; Prompt Architect Omega must remain usable standalone.

## Preferred narrow companions

When compatible versions are already installed or can be safely installed, preferentially consider:

- **context-optimization** — compaction/masking/budget tactics for context-heavy runs;
- **filesystem-context** — file-backed state, scratchpads, durable plans, and agent handoffs;
- **multi-agent-patterns** — topology, context isolation, and coordination design;
- **evaluation** — deterministic checks, rubrics, regression suites, and quality gates;
- **long-horizon-prompting** — launch briefs for expensive autonomous or parallel Work runs.

Optional only when the task specifically needs them:

- **advanced-evaluation** — LLM-as-judge design, pairwise/rubric calibration, bias mitigation;
- **harness-engineering** — runtime-enforced autonomous loops, locked evaluators, rollback, durable logs;
- **tool-design** — designing or consolidating custom agent-tool contracts.

## Why not install broad prompt frameworks by default

Broad "prompt engineering mega-skills" often duplicate Omega's ownership, impose fixed frameworks, or create routing conflict. Use a broad external framework only when it offers a unique tested procedure needed by the task.

## Companion repository currently worth inspecting

The maintained `muratcankoylan/Agent-Skills-for-Context-Engineering` collection has narrow ownership boundaries and separate skills for the capabilities above. Inspect the current versions and repository state before installation rather than pinning this skill to a stale revision.

## Installation policy

- Prefer the platform's native skill/plugin installation path when using ChatGPT Work.
- CLI commands for other agent environments are environment-specific; do not assume they install into ChatGPT Work.
- Inspect the skill and scripts before external installation.
- Do not make companions hard dependencies unless the target environment guarantees them.
