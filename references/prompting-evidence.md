# Prompting Evidence Ledger

Do not treat prompting heuristics as timeless universal laws.

For material techniques, distinguish:
- official/runtime documentation;
- experimentally supported behavior;
- strong empirical observation;
- task-dependent heuristic;
- unverified assumption.

Record evidence only when it changes architecture. Useful fields:
- technique;
- evidence class;
- target runtime/context;
- confidence;
- applicability;
- known counterconditions;
- last verification date/version when relevant.

Prefer capability-based rules over claims such as “model X always needs phrase Y”.

Re-evaluate assumptions when the runtime, model class, tool behavior, or skill platform changes materially.


## Current evidence records

### Progressive skill disclosure

- **Technique:** keep the core `SKILL.md` concise and link supporting material.
- **Evidence class:** official OpenAI documentation.
- **Applies when:** the runtime supports Agent Skills discovery/loading.
- **Observed behavior:** skill discovery uses name/description metadata; selected skills can then load the full `SKILL.md` and supporting files.
- **Do not assume:** every non-OpenAI runtime implements identical loading semantics.
- **Last verified:** 2026-10-02.
- **Sources:** OpenAI Developers “Skills” and “Build skills” documentation.

### External skill trust

- **Technique:** inspect third-party skills and supporting code before making them available.
- **Evidence class:** official OpenAI security guidance.
- **Applies when:** external or shared skill bundles are introduced.
- **Do not assume:** a skill is safe because its instructions look harmless; scripts and tool access are part of the trust surface.
- **Last verified:** 2026-10-02.


### Skill bundle validation limits

- **Evidence class:** official OpenAI Developers documentation.
- **Verified:** 2026-10-02.
- **Current documented constraints:** exactly one case-insensitive `SKILL.md`/ `skill.md` per uploaded bundle, maximum 50 MB compressed zip, maximum 500 files per skill version, and maximum 25 MB per uncompressed file.
- **Manifest constraints:** `description` is required, non-empty, and at most 1,024 characters; the skill instruction body must be non-empty.
- **Agent metadata:** `agents/openai.yaml` is optional. If included, `interface.display_name` and `interface.short_description` are required; `default_prompt` and policy settings are optional.
- **Sources:** OpenAI Developers “Skills”, “Build skills”, and plugin submission validation documentation.
