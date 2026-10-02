# Omega 1.0 Release-Candidate Validation

Date: 2026-10-02

## Purpose

This report records what has actually been verified for the Omega 1.0 release candidate and what remains unverified.

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

Do not label the candidate final merely because files validate. Final promotion should require:

1. green local checks;
2. green GitHub CI on the release commit;
3. no unresolved material red-team defect;
4. package contents inspected and installable;
5. model-execution A/B evidence when a repeatable runner is available, or an explicit release note that this evidence is still pending.
