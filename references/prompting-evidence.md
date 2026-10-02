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

### Compact discovery descriptions

- **Technique:** keep the skill description short while still naming the user goals and trigger boundary.
- **Evidence class:** official OpenAI documentation and current OpenAI developer guidance.
- **Applies when:** a skill is discoverable automatically and its metadata is added to model context before invocation.
- **Observed behavior:** name and description are primary discovery signals; overly long or overlapping descriptions add always-on context and can make skill selection less reliable.
- **Do not assume:** shorter is always better if it removes the trigger boundary; preserve representative positive and negative cases.
- **Last verified:** 2026-10-02.
- **Sources:** OpenAI Developers “Skills”, “Build skills”, and “Rethinking skills and prompts for GPT-6 Astra”.


### Optional OpenAI agent metadata

- **Evidence class:** official OpenAI Developers submission-validation documentation.
- **Last verified:** 2026-10-02.
- **Observed behavior:** a skill may include `agents/openai.yaml`; if the file is included, `interface.display_name` and `interface.short_description` are required.
- **Optional fields:** `interface.default_prompt`, `policy`, and `policy.allow_implicit_invocation` are optional.
- **Architectural implication:** Omega's generic validator must not impose Omega-specific agent metadata on every generated task skill. Omega-specific expectations belong in Omega's own regression suite.
- **Sources:** OpenAI Developers “Plugin submission errors” and “Build skills”.
