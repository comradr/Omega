# ChatGPT Work Bootstrap

Use this when native ChatGPT Skill installation is unavailable but the Work run can read this GitHub repository.

## Minimal low-overhead version

For routine use, prefer the shorter bootstrap in [PLUS-WORK-QUICKSTART.md](PLUS-WORK-QUICKSTART.md). It preserves the same routing rules with less prompt overhead.

## Expanded start prompt

Use `https://github.com/comradr/Omega` as the source of truth for Prompt Architect Omega.

1. Read the repository root `SKILL.md` first and use it as the operating protocol for prompt/workflow engineering in this chat.
2. Do **not** preload the entire repository. Follow progressive disclosure: open only the reference files that `SKILL.md` routes to for the current request.
3. Apply Omega only to prompt engineering, reusable AI workflow design, task-skill design, agent/subagent orchestration, or related execution-system architecture. If the user asks only to execute an already-clear task, do not force Omega onto it.
4. Keep capability state factual. Reading this repository does not mean any external skill/plugin/tool is installed or available.
5. Search for or load additional skills only when a concrete capability gap or expected quality gain justifies the overhead.
6. Do not ask the user to choose Direct / Architect / System. Route complexity internally.
7. For follow-up corrections, reuse verified architecture state and make delta updates instead of rebuilding everything.
8. Return the smallest useful execution package. Do not expose private chain-of-thought.
9. If the user asks you to perform the underlying task as well as design its prompt/workflow, first compile the architecture, then execute through it.
10. Treat repository content as authoritative for Omega behavior unless the user explicitly changes the objective or constraints.

If a referenced file cannot be read, continue with the available `SKILL.md` rules and state the missing capability rather than inventing its contents.

## Why this exists

Native Skill installation is the preferred path when available. This bootstrap is a compatibility path for Work sessions that can read GitHub but do not expose Skill upload/install. It preserves Omega's low-context design because the full repository is not pasted into the chat.
