# Runtime Adaptation

Adapt the execution package to capabilities that are actually available.

## Capability profile

Determine only when relevant:
- target surface/runtime;
- skill discovery/loading support;
- tools/plugins/connectors;
- browser/research access;
- repository/filesystem access;
- agent/subagent support;
- persistence/durable artifacts;
- executable scripts/code;
- artifact creation;
- material runtime limits.

Use capability evidence, not model folklore.

## Adaptation rules

If skills can be discovered and loaded, reference them by capability and avoid copying their full bodies into the master prompt.

If skills are unavailable, inline only the operational rules the executor needs.

If subagents are available and justified, use bounded contracts. Otherwise convert the same separation into sequential passes.

If durable state exists, store stable requirements/decisions/evidence there. Otherwise keep a compact explicit state block.

If the runtime cannot enforce a budget, treat prompt-stated budgets as heuristics rather than guarantees.

Unknown capabilities remain unknown. Never convert absence of evidence into availability.
