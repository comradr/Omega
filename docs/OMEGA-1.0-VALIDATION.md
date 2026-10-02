# Omega 1.0 Validation

Date: 2026-10-02

## Purpose

This report records what has actually been verified for Omega 1.0 and what remains intentionally unclaimed.

## Baseline versus candidate core

The 0.9.0 `SKILL.md` baseline contains 9,207 characters, 139 lines, and 1,175 whitespace-delimited words.

The RC2 compact core contains 7,186 characters and 857 whitespace-delimited words. RC3 reduces the same core to 6,679 characters and 788 whitespace-delimited words, with no workflow capability removed.

The discovery description is reduced from 789 characters in RC2 to 282 characters in RC3. This matters because OpenAI skill discovery exposes name/description metadata before full skill instructions are loaded. A CI guard now fails if the discovery description grows beyond 350 characters.

These are structural size measurements, not claimed model token counts.

## Verified architecture changes

- hidden Direct / Architect / System routing;
- architectural-overhead gate and ROI discipline;
- delta updates for minor corrections;
- durable architecture-state cache for multi-session work;
- capability-based runtime adaptation;
- external-skill provenance/security gate;
- trust boundaries for untrusted source material;
- functional prompt-technique selection rather than framework-name routing;
- behavior mining from repeated real corrections;
- prompting evidence ledger;
- empirical evaluation protocol;
- trigger, behavior, and benchmark regression corpora;
- dev/holdout trigger evaluation with explicit positive and negative boundary cases;
- always-on discovery-description overhead guard.

## Local deterministic checks

The candidate has passed:

- `python scripts/validate_skill.py .`
- `python scripts/run_static_evals.py .`
- `python scripts/test_scaffolder.py`
- `python -m compileall -q scripts`
- `python scripts/package_skill.py .`

The packaging test validates the source, creates both `.zip` and `.skill`, extracts each archive, checks the package manifest, and validates the extracted skill under its strict `prompt-architect-omega` root name.

A hostile-input scaffolder regression checks YAML-sensitive values including colons, `#`, quotes, backslashes, Unicode, braces, and apostrophes.

## GitHub CI

GitHub Actions is configured to repeat validation, static evals, hostile scaffolder regression, Python compilation, packaging, extraction, and revalidation on pushes and pull requests.

## Current official-platform evidence

OpenAI documentation verified on 2026-10-02 states that Agent Skills use a `SKILL.md` manifest with supporting `references/`, `scripts/`, and `assets/`; discovery exposes skill metadata and selected skills can then load their full instructions/supporting files. OpenAI also documents `agents/openai.yaml` skill interface metadata and `allow_implicit_invocation`.

This supports Omega's progressive-disclosure design.

## Not yet claimed

The repository does **not** yet claim a model-execution quality win from 1.0 over 0.9.

A true differential benchmark requires running the same held-out tasks through baseline and candidate execution environments, collecting actual outputs/cost evidence, and preferably blind-comparing results. The repo now contains the protocol and benchmark corpus needed for that next stage, but deterministic structural checks are not a substitute for model-execution A/B evidence.

## Release rule

Stable 1.0 promotion requires:

1. green local checks;
2. green GitHub CI on the release commit;
3. no unresolved material red-team defect;
4. package contents inspected and installable;
5. model-execution A/B evidence when a repeatable runner is available, or an explicit release note that this evidence is still pending.

## Stable 1.0 promotion record

Version `1.0.0` is promoted after the RC3 branch passed the repository validation workflow and the final red-team pass found no unresolved material architecture defect. The release still does not claim a measured model-execution quality win over 0.9; that claim requires the independent differential benchmark described above.


## 1.0.1 hardening

The 1.0.1 hardening track does not change Omega's runtime prompt-engineering behavior. It tightens packaging and validation around the stable 1.0 skill.

Current OpenAI documentation verified on 2026-10-02 specifies:

- exactly one case-insensitive `SKILL.md` / `skill.md` in a skill bundle;
- non-empty skill instructions;
- maximum zip upload size of 50 MB;
- maximum 500 files per skill version;
- maximum 25 MB uncompressed size per file.

The hardening validator/package pipeline now checks those limits before release, while keeping the existing smaller internal progressive-disclosure guards as Omega-specific quality checks rather than claiming they are OpenAI platform limits.


### 1.0.1 promotion record

The 1.0.1 hardening pull request passed the complete GitHub validation workflow. The generated Actions artifact was downloaded independently, both bundled files were inspected, the inner skill ZIP contained a single `prompt-architect-omega/` root with 29 packaged files, and the extracted bundle passed validator, static architecture evals, and Python compilation again.

The 1.0.1 change set does not modify `SKILL.md`, trigger datasets, or runtime reference behavior relative to stable 1.0.0; it hardens validation, packaging, and release evidence only.


## 1.0.2 validator semantics

A follow-up standards review found that the 1.0.1 generic validator was stricter than the OpenAI skill format in one area: it required `agents/openai.yaml`, `default_prompt`, and `allow_implicit_invocation` for every skill.

Current OpenAI documentation treats `agents/openai.yaml` as optional. When present, the `interface` mapping requires non-empty `display_name` and `short_description`; `default_prompt` and policy fields are optional.

Version 1.0.2 fixes this separation:

- the generic validator accepts a valid skill with no `agents/openai.yaml`;
- a provided agent metadata file must contain the required interface fields;
- optional `default_prompt` and policy fields are validated only when present;
- Omega's own stronger metadata expectations remain enforced by Omega-specific static evals;
- the validator regression suite is now an explicit GitHub Actions step.

This change affects validation/tooling only and does not alter Omega's runtime prompt-engineering behavior.
