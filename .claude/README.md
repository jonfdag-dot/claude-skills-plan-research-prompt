# Claude configuration repository

This repository holds reusable working conventions, eight skills. It is a portable adaptation of an existing working setup. It includes the references and deterministic scripts needed by the exported workflows, with personal configuration and product-specific history removed.

| Path | Purpose |
| --- | --- |
| [CLAUDE.md](CLAUDE.md) | Shared instructions and routes to the plan and research libraries. |
| [skills/INDEX.md](skills/INDEX.md) | Skill selection, commands and supporting-resource map. |
| skills/&lt;name&gt;/SKILL.md | The workflow loaded when that skill is selected. |
| skills/&lt;name&gt;/references/ | Details to read only for the current question. |
| skills/&lt;name&gt;/scripts/ | Static instruction, skill or handoff validation. |
| skills/&lt;name&gt;/assets/ | Non-executable templates to copy and fill. |

See [the parent guide](../CLAUDE.md) for setup, and the [license notices](../README.md) for source terms.

For use across projects, review and merge the contents into your existing `~/.claude/`, one file at a time. Put the two library repositories at `~/llm-plan-links` and `~/llm-research-links`, or update all affected routes. Preserve existing skills with the same names until you have compared them. Do not replace your whole configuration directory.

For project-only use, merge `skills/` into the active project's `.claude/`, then merge the relevant shared instructions into its existing root `CLAUDE.md`. Change library commands to their actual locations. A `.claude/CLAUDE.md` inside a project is project guidance; it becomes personal guidance only when installed at `~/.claude/CLAUDE.md`.

Use local Claude Code and Python 3.11 or newer for all bundled scripts. The two library tools need Python 3.10 or newer; the instruction auditor imports `tomllib`, which requires 3.11. Skill validation has a standard-library fallback when PyYAML is absent. Browse/search tools depend on the permissions and capabilities of the installed Claude session.

The human index requires no generated catalog or hook. Start a fresh Claude session after installation, inspect `/memory`, and invoke a selected skill. These are manual integration checks; this export has not run an authenticated Claude session on the recipient's machine.
