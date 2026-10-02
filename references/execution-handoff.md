# Execution Handoff

Use this reference when packaging the final prompt/workflow for ChatGPT Work or another executor.

## 1. Make state factual

For every non-native capability, record its real state. Never blur:

`discovered → reviewed → approved → available → installed → loaded → invoked`

If installation or invocation cannot be verified, phrase the handoff conditionally and provide a fallback.

## 2. Handoff package

A substantial execution package can contain:

- master prompt;
- task-specific skill package/path;
- selected execution skills and the capability each owns;
- required plugins/tools/connections;
- agent contracts or topology;
- source-of-truth files/locations;
- verification checklist;
- explicit unresolved assumptions.

Do not include internal design chatter that the executor does not need.

## 3. Tell the executor to use capabilities

Weak:

> You may find the testing skill useful.

Strong:

> Use the available testing skill for the regression design and verification phase; do not duplicate its full instructions in this prompt.

When a capability is unavailable, provide the task-specific fallback protocol rather than pretending it exists.

## 4. Design-plane versus execution-plane skills

Meta-skills used to create the prompt do not automatically belong in the future task run.

Only pass a meta-skill into the execution plane when the task itself requires that capability during execution (for example, long-horizon context optimization or dynamic skill creation).

## 5. User review

Present enough architecture for the user to judge the system without exposing private reasoning. Invite refinement of goals, constraints, or deliverables—not unnecessary orchestration micromanagement.
