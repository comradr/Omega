# Prompt Architect Omega

Prompt Architect Omega is a meta-level Agent Skill for designing high-quality AI execution systems. It turns a user's objective into the smallest sufficiently powerful architecture for execution: requirements, capabilities, skills, tools, agents, context strategy, verification, and handoff.

## What Omega does

- translates goals into executable requirements and observable completion criteria;
- maps required capabilities before selecting tools or skills;
- discovers, reviews, and composes skills without blindly installing everything;
- distinguishes discovered, reviewed, available, installed, loaded, and invoked capabilities;
- creates task-specific skills when durable project rules justify one;
- designs bounded agent/subagent contracts and context-isolated handoffs;
- uses progressive disclosure and file-backed state for long-running work;
- compiles master prompts with source precedence, failure recovery, verification, and return gates;
- red-teams substantial execution systems before handoff;
- keeps design-plane meta-skills separate from execution-plane capabilities.

## Repository layout

- `SKILL.md` — compact runtime router and core behavior.
- `agents/openai.yaml` — Agent Skill metadata.
- `references/` — detailed procedures loaded only when relevant.
- `assets/` — reusable prompt and agent-contract skeletons.
- `scripts/` — validation, packaging, and task-skill scaffolding.

## Validate

```bash
python scripts/validate_skill.py .
```

## Package

```bash
python scripts/package_skill.py .
```

## Design principle

Quality first, but architectural overhead must earn its cost. Omega should not spend a large context budget designing a simple task. Complex projects may justify skill discovery, task-skill compilation, specialist agents, persistent state, and independent verification; simple requests should remain direct.

## Status

Main branch remains the 0.9.0 baseline while `omega-1.0` is the active 1.0 release-candidate branch. The candidate adds adaptive complexity routing, architectural-overhead controls, runtime adaptation, trust boundaries, behavior mining, and empirical evaluation.
