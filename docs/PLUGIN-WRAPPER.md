# Skills-only Plugin Wrapper

Omega's canonical source remains the root Agent Skill. The plugin wrapper is generated from that source; it is not a second copy of the project.

## Build

```bash
python scripts/package_plugin.py .
```

This produces:

```text
prompt-architect-omega-plugin.zip
```

The ZIP contains one plugin root:

```text
prompt-architect-omega-plugin/
├── plugin.json
└── skills/
    └── prompt-architect-omega/
        ├── SKILL.md
        ├── agents/
        ├── assets/
        ├── evals/
        ├── references/
        └── scripts/
```

The nested skill is built from the same `package_files()` manifest as the canonical skill ZIP.

## Why this exists

Current OpenAI Plugins can package one or more Skills without an MCP server. The Plugin Directory is available across ChatGPT plans, although installation and individual plugin capabilities still depend on account, role, region, and surface.

This makes the wrapper useful for:

- personal/local plugin testing where that surface supports it;
- a future public Plugin Directory submission;
- OpenAI/Codex environments that consume plugin packages;
- keeping Omega installable even when standalone native Skills are not exposed to the account.

## What this wrapper is not

It is not a second Omega implementation.

Do not manually edit the nested skill inside a generated plugin package. Edit the repository's canonical root skill and rebuild.

The generated package is **not automatically a published public plugin**. Public directory publication still requires OpenAI's upload/review/publishing flow and the applicable publisher identity/listing requirements.

## Plus + Work

For a Plus account:

1. If your ChatGPT surface lets you install a personal/local plugin, prefer the skills-only plugin package.
2. If it exposes native Skill upload, use `prompt-architect-omega.zip`.
3. If neither install surface is available, use the low-overhead GitHub bootstrap in [PLUS-WORK-QUICKSTART.md](PLUS-WORK-QUICKSTART.md).

The fallback bootstrap remains useful on mobile or surfaces where local plugin authoring/install is unavailable.

## Verification

CI:

- builds the plugin ZIP from the canonical skill;
- checks plugin ZIP structure and path safety;
- verifies the portable Agent Plugins schema marker;
- verifies the nested skill with Omega's strict skill validator;
- runs a dedicated plugin-package regression test;
- uploads the plugin ZIP together with the canonical Skill ZIP.
