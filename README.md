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

Current stable release: `1.0.3`. It keeps the compact runtime architecture, removes unsupported default-prompt conventions, adds executable blind A/B and trigger-evaluation tooling, and ships both canonical Skill ZIP and generated skills-only Plugin ZIP distribution paths. Model-execution superiority is intentionally not claimed until actual comparable runs are supplied.


## Installation paths

Omega has one canonical source and three distribution paths:

- **OpenAI Skill ZIP:** `prompt-architect-omega.zip`.
- **Skills-only Plugin ZIP:** `prompt-architect-omega-plugin.zip`, generated from the same source for Plugin-capable surfaces.
- **Work bootstrap:** compatibility fallback when the account/surface exposes neither install path.

See [docs/PLUGIN-WRAPPER.md](docs/PLUGIN-WRAPPER.md) and [docs/PLUS-WORK-QUICKSTART.md](docs/PLUS-WORK-QUICKSTART.md).

## Install / use

GitHub is the source of truth, not an assumed direct-install endpoint.

1. Clone or download this repository.
2. Build the canonical Skill bundle with `python scripts/package_skill.py .`. To also build the skills-only Plugin wrapper, run `python scripts/package_plugin.py .`.

3. For OpenAI Skill upload/API use the generated `prompt-architect-omega.zip`, which contains one top-level skill folder as documented by OpenAI. The generated `.skill` file is an identical ZIP-format compatibility artifact; use that extension only on runtimes that explicitly accept it.
4. In a separate prompt-engineering chat, describe the goal normally. Omega should decide the internal complexity path, relevant capabilities, whether skills/subagents/task-skill are justified, and return the smallest useful execution package.

Do not paste the whole repository into every task chat. The installed skill should load detailed references only when needed.


## Use in ChatGPT Work without native Skills

If your ChatGPT surface does not expose native Skill upload/install, use the compact [Plus + Work quickstart](docs/PLUS-WORK-QUICKSTART.md). The expanded compatibility notes remain in [docs/WORK-BOOTSTRAP.md](docs/WORK-BOOTSTRAP.md). Both paths tell Work to read `SKILL.md` first and load references only when needed, preserving Omega's progressive-disclosure/token-overhead design.
