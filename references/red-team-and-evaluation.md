# Red Team and Evaluation

Use this reference before delivering any substantial prompt/execution system and after material revisions.

## 1. Prefer an independent critic

When available and valuable, use a fresh-context Prompt Red Team or QA specialist that did not author the draft. Independence reduces self-rationalization.

The critic should return defects and evidence, not rewrite the whole system unless assigned.

## 2. Adversarial defect hunt

Try to find ways an executor could technically comply while missing the user's real goal.

Check:

- ambiguous success condition;
- missing non-goals/non-counting outcomes;
- conflicting instructions;
- stale or wrong source precedence;
- premature return paths;
- false completion without evidence;
- missing failure handling;
- excessive or insufficient autonomy;
- missing tool/skill availability checks;
- skill conflicts or redundant skills;
- external-skill trust/security gaps;
- duplicated agent work;
- correlated agent agreement mistaken for verification;
- context explosion or repeated whole-project reads;
- unsupported assumptions;
- unverifiable deliverables;
- generated artifacts not actually opened/tested;
- hidden dependence on capabilities the target environment may not have.

## 3. Evaluation rubric

Rate only to drive repair; do not show arbitrary scores unless useful to the user.

Assess:

- goal fidelity;
- requirement coverage;
- instruction clarity;
- practical executability;
- capability/skill fit;
- agent topology;
- context architecture;
- autonomy boundaries;
- failure robustness;
- evidence/verification strength;
- definition of done;
- resource proportionality;
- maintainability under future edits.

Any material defect is a repair item regardless of average score.

## 4. Repair loop

Use:

`draft → adversarial defect report → repair → final gate`

Run another loop only when a material defect remains. Do not spend cycles polishing wording with negligible execution impact.

## 5. Evidence gate

Ensure completion claims can distinguish:

- **confirmed** — supported by direct evidence;
- **tested** — a relevant check was actually run;
- **inferred** — reasoned from evidence but not directly verified;
- **assumed** — a necessary unverified premise;
- **not verified** — explicitly outstanding.

## 6. Regression after user feedback

When the user changes a requirement:

1. update the underlying requirement model;
2. modify affected architecture/skills/agents;
3. remove obsolete instructions;
4. re-check conflicts and source precedence;
5. re-run the relevant adversarial gate.

Do not append contradictory patches at the bottom of an old prompt.
