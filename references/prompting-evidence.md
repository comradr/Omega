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


### Default prompt semantics

- **Evidence class:** official OpenAI Developers examples and validation reference.
- **Last verified:** 2026-10-02.
- **Observed behavior:** `interface.default_prompt` is an optional ordinary string when `agents/openai.yaml` is present.
- **Do not assume:** a dollar-prefixed skill name such as `$skill-name` is required or substituted by ChatGPT. Current OpenAI examples use normal user-facing prompt text.
- **Architectural implication:** Omega and generated task skills use natural starter text unless a target runtime explicitly documents invocation syntax.
- **Sources:** OpenAI Developers “Build skills” and “Plugin submission errors”.

### Direct OpenAI skill ZIP

- **Evidence class:** official OpenAI API Skills documentation.
- **Last verified:** 2026-10-02.
- **Observed behavior:** a skill can be uploaded as a ZIP containing a single top-level folder with one `SKILL.md`; current limits are 50 MB compressed, 500 files, and 25 MB per uncompressed file.
- **Architectural implication:** `prompt-architect-omega.zip` is the canonical OpenAI-targeted bundle. A `.skill` compatibility copy must not be described as universally supported by ChatGPT unless the target surface documents that extension.
- **Source:** OpenAI API “Skills”.


### Agent Skills optional frontmatter

- **Evidence class:** Agent Skills specification referenced by OpenAI's skill documentation.
- **Last verified:** 2026-10-02.
- **Required frontmatter:** `name` and `description`.
- **Optional frontmatter:** `license`, `compatibility`, `metadata`, and experimental `allowed-tools`.
- **Constraints used by Omega preflight:** `compatibility` is at most 500 characters; `metadata` is a string-to-string mapping.
- **Architectural implication:** Omega's generic task-skill validator accepts the documented optional fields rather than imposing the narrower early-project schema.
- **Source:** Agent Skills specification and OpenAI Developers skill validation guidance.


### Skills-only plugin distribution

- **Evidence class:** official OpenAI Help Center and Developers documentation.
- **Last verified:** 2026-10-02.
- **Observed behavior:** plugins can package Skills without an MCP server; portable Agent Plugin packages use root `plugin.json` and discover skills from `skills/`.
- **Availability:** the Plugin Directory is documented across ChatGPT plans, while installation and individual capabilities still vary by plan, workspace, role, region, and surface.
- **Architectural implication:** Omega can ship a generated skills-only Plugin ZIP as a distribution wrapper while retaining the root Agent Skill as the only source of truth.
- **Sources:** OpenAI Developers “Package your plugin”, “Plugin architecture”, and OpenAI Help Center “Plugins in ChatGPT”.
