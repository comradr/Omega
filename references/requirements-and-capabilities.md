# Requirements and Capability Modeling

Use this reference when the request is complex, ambiguous, multi-domain, high-consequence, or likely to require multiple tools/agents.

## 1. Build an outcome model

Capture only what changes execution:

- **Goal:** the user's actual desired end state.
- **Deliverable:** the concrete artifact/action/state that proves success.
- **Current state:** what already exists and where it lives.
- **Must preserve:** working behavior, data, architecture, style, interfaces, or constraints that must survive.
- **Non-goals:** nearby work that should not be performed.
- **Failure conditions:** outcomes that would clearly count as failure.
- **Evidence bar:** what must be verified rather than assumed.
- **Autonomy boundary:** decisions the executor may make without user input.
- **Unknowns:** only material unresolved facts or preferences.

Do not turn every preference into a hard constraint. Preserve the user's goal even when their suggested method is suboptimal.

## 2. Resolve uncertainty before asking

Use this order:

1. current conversation;
2. supplied files or repository;
3. connected sources and project state;
4. available tools/plugins;
5. targeted research;
6. low-risk inference.

Ask only when the answer cannot be discovered and different answers would materially change the intended outcome or create irreversible risk.

## 3. Build a capability map

List capabilities rather than product names. Examples:

- repository inspection;
- Kotlin/Compose implementation;
- UI/UX review;
- statistical analysis;
- legal research;
- spreadsheet modeling;
- source verification;
- document generation;
- visual generation;
- browser interaction;
- QA/regression;
- deployment/release.

For each capability, resolve the best provider:

| Capability | Provider | Why | Evidence/state |
|---|---|---|---|
| Example | skill/tool/agent/native | concrete execution benefit | available/installed/etc. |

Avoid duplicating the same capability across several skills or agents unless independent verification is intentional.

## 4. Match instruction freedom to fragility

Use **high freedom** when several approaches are valid and judgment matters.

Use **medium freedom** when a preferred sequence/pattern exists but some adaptation is expected.

Use **low freedom** (scripts/checklists/exact sequence) when the task is fragile, repetitive, destructive, or easy to get subtly wrong.

Do not over-specify frontier models for routine reasoning. Spend instruction detail on requirements, failure modes, evidence, and irreversible boundaries.

## 5. Define source precedence

When sources can conflict, state precedence explicitly. Example only:

1. current explicit user requirements;
2. current project/data and verified behavior;
3. current authoritative documentation;
4. older project documentation;
5. external recommendations/general best practices.

Adapt the order to the domain. Never let generic advice silently override the user's current source of truth.
