# Changelog

## 1.0.0-rc3 — Lower always-on discovery overhead

- Reduced the discovery description from 789 to 302 characters while preserving the trigger boundary.
- Added a 350-character CI guard so future edits cannot silently re-bloat always-on skill metadata.
- Expanded trigger evaluation from 10 to 16 cases with separate dev and holdout sets.
- Added explicit positive and negative holdout checks for prompt/workflow boundaries.
- Recorded current OpenAI evidence for compact discovery descriptions.

## 1.0.0-rc2 — Lean core and hardened release checks

- Reduced `SKILL.md` below the 0.9 baseline while retaining the 1.0 architecture through progressive disclosure.
- Added architecture-state cache and delta invalidation rules.
- Added functional prompt-technique selector.
- Hardened repository validation, package extraction/revalidation, and hostile-input scaffolder tests.
- Added GitHub Actions CI.
- Added a 12-case routing/behavior benchmark corpus and release validation report.
- Development/CI files are excluded from the installable skill package.

## 1.0.0-rc1 — Adaptive, lower-overhead architecture

- Added hidden Direct / Architect / System routing.
- Added Architectural Overhead Gate and Prompt Engineering ROI principle.
- Added delta updates to avoid re-architecting unchanged work.
- Added capability-based runtime adaptation.
- Added trust boundaries for untrusted retrieved/source material.
- Added behavior mining from repeated real corrections and failures.
- Added prompting evidence ledger guidance.
- Added empirical baseline/candidate and blind A/B evaluation guidance.
- Added trigger and behavioral eval datasets plus a deterministic static eval harness.
- Kept the runtime core compact through progressive disclosure.

## 0.9.0 — GitHub baseline

- Established Prompt Architect Omega as a versioned GitHub source of truth.
- Preserved the validated production-candidate skill architecture.
- Includes capability mapping, skill discovery/composition, task-skill compilation, agent orchestration, context/resource policy, prompt compilation, red-team evaluation, execution handoff, and self-benchmark references.
- Includes validators, packager, and task-skill scaffolder.
