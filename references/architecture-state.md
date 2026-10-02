# Architecture State Cache

Use durable architecture state only when reuse will save meaningful work. Do not create it for ordinary Direct-mode requests.

## When to use

- multi-session projects;
- repeated prompt revisions;
- large source-of-truth sets;
- multiple specialists sharing stable decisions;
- expensive capability/skill discovery that should not be repeated unchanged.

## Minimal state

Store only durable execution facts:

- task identity and current goal;
- source-of-truth locations and precedence;
- active requirements and must-preserve constraints;
- material assumptions and unresolved items;
- capability map;
- skill/tool state ledger;
- agent topology, if any;
- key architecture decisions;
- verified evidence pointers;
- current prompt/task-skill version;
- invalidated or stale items.

Do not store giant transcripts or raw tool output when a retrievable pointer and concise finding suffice.

## Reuse gate

Before reusing cached state, check:

1. Is this the same task/project?
2. Has the user superseded any requirement?
3. Have relevant files, runtime capabilities, or external facts changed?
4. Is the cached evidence still fresh enough for the decision?

If a dependency changed, invalidate the affected state instead of trusting it.

## Delta update

For a new correction or requirement:

`new information → affected requirements/decisions → invalidate dependents → update only affected architecture → rerun relevant verification`

Preserve unaffected verified state.

## Suggested file-backed layout

When the runtime supports project files, a compact structure can be:

```text
.omega/
├── state.md
├── decisions.md
├── capability-ledger.md
└── verification.md
```

Use fewer files when the project is small. The layout is a convenience, not a mandatory runtime dependency.

## Privacy and portability

Do not cache secrets or unnecessary personal data. Keep references portable and avoid hard-coding machine-specific paths unless the executor actually needs them.
