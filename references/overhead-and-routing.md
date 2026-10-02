# Architectural Overhead and Routing

Omega must earn its own cost.

## Hidden complexity routing

Do not ask the user to choose a mode.

### Direct
Use for simple, bounded prompt work.
- recover obvious requirements;
- compile directly;
- run a brief self-check;
- no skill search, task skill, or agents unless a concrete gap appears.

### Architect
Use when several constraints/capabilities interact.
- capability map;
- inspect already available relevant skills;
- task skill only if durable rules justify it;
- one focused critic pass;
- targeted references only.

### System
Use for long-running, multi-domain, high-risk, large-context, or multi-agent Work.
- deeper capability/skill discovery;
- task-skill decision;
- context architecture;
- justified specialist topology;
- independent verification;
- empirical evaluation when the overhead is justified.

These are internal routing states, not user-facing modes.

## Overhead gate

Before adding a search, reference, agent, evaluation pass, or generated artifact ask:
1. What decision or failure mode can this change?
2. Is that information already available?
3. Is there a cheaper reliable mechanism?
4. Is expected quality/risk reduction material?

If the answer is no, skip it.

## Prompt Engineering ROI

Evaluate architecture by useful execution improvement relative to added overhead.

Do not optimize a fake universal numeric score. Compare observable outcomes:
- requirements recovered;
- failures prevented;
- verification improved;
- execution quality;
- unnecessary prompt/context size;
- extra calls/agents/time when measurable.

A substantially larger architecture with indistinguishable execution quality is a regression.

## Delta updates

For an existing architecture, process a new requirement as a delta:
- identify affected requirements/decisions;
- update affected sections;
- invalidate stale summaries/evals;
- preserve unaffected verified state;
- rerun only relevant gates.

Do not redesign the whole system after every minor correction.
