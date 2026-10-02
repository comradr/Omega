# Behavior Mining

Use real corrections and failures to improve durable workflows.

## Inputs

When available, inspect:
- repeated user corrections;
- repeated missed requirements;
- recurring manual workarounds;
- successful runs;
- failed runs;
- regression history.

## Promotion test

A correction becomes a durable rule only when it is:
- repeated or clearly structural;
- relevant to future runs;
- not superseded by a newer explicit preference;
- specific enough to verify.

Otherwise keep it as current-task context.

## Loop

real failure/correction
→ root cause
→ generalizable lesson
→ smallest architectural change
→ regression case
→ retest

Do not patch SKILL.md for every isolated mistake.

## Delta integration

When a durable rule is promoted, update the owning reference/task skill and any relevant benchmark. Remove obsolete or contradictory rules rather than appending history.
