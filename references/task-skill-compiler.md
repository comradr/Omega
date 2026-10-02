# Task-Specific Skill Compiler

Create a task skill when durable project rules would otherwise be repeatedly rediscovered or bloat the master prompt.

Strong signals:
- many phases or sessions;
- project invariants;
- multiple agents sharing a protocol;
- recurring regression checks;
- deterministic helpers/templates;
- a reusable project workflow.

## Separation

Task skill owns durable rules, source hierarchy, workflow, invariants, failure modes, and reusable helpers.

Master prompt owns the current objective, current inputs, one-run constraints, topology, deliverables, and return condition.

## Preferred structure

- SKILL.md
- agents/openai.yaml — optional OpenAI presentation/policy metadata
- references/ only for material progressive disclosure
- scripts/ for deterministic fragile procedures
- assets/ for reusable templates

Keep frontmatter limited to name and description. Treat description as the trigger surface. Keep SKILL.md concise and procedural.

When OpenAI agent metadata is used, write `default_prompt` as a normal user-facing starter prompt. Do not invent invocation syntax such as `$skill-name` unless the target runtime explicitly documents it.

Do not invent icons, colors, dependencies, or runtime capabilities. Do not vendor entire third-party skills into a generated task skill.

## Runtime creator preference

If the target environment provides an official or built-in skill creator, use it for creating or repairing the actual skill package when doing so improves compatibility. Keep Omega's own requirements/source hierarchy authoritative, then run the deterministic validation/package checks available in the target environment.

## Validation

Check:
- folder/name consistency;
- valid YAML/frontmatter;
- allowed metadata fields;
- local references;
- unresolved placeholders;
- concise progressive-disclosure body;
- script syntax/tests where applicable;
- agent metadata;
- packaged archive contents.

Version durable task skills coherently instead of spawning near-duplicates after every correction.
