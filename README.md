# Claude Research & Planning Kit

Adopt a shared workflow for researching decisions, planning project work and resuming it across Claude Code sessions.

[Start the setup guide](CLAUDE.md)

The framework has three parts: `.claude/` supplies reusable skills, `llm-research-links/` keeps source-linked findings, and `llm-plan-links/` keeps each project's plans and progress. Connect one existing project first, then reuse the setup across your other projects.

## Set up your first project

1. Put the two libraries at `~/llm-plan-links/` and `~/llm-research-links/`.
2. Merge the bundled skills and shared conventions into your Claude setup.
3. Register your source project in the plan library and add the library routes to its `CLAUDE.md`.
4. Start a fresh session and try one real task, then create a handoff when you need to resume elsewhere.

The [setup guide](CLAUDE.md) covers each step, existing installations, project-local use and example requests. You need Claude Code and Python 3.11 or newer for the bundled tools.

## Find the supporting guides

| Guide | Use it to |
| --- | --- |
| [Skill index](.claude/skills/INDEX.md) | Choose among the eight research, planning and maintenance workflows. |
| [Research library](llm-research-links/README.md) | Search and retain reusable findings with sources. |
| [Plan library](llm-plan-links/README.md) | Register projects and maintain plans and progress. |
| [All files](FILES.md) | Locate the shipped templates, scripts and references. |

[Apache 2.0 license](.claude/skills/skill-creator/LICENSE.txt) · [Retained MIT notice](.claude/skills/agents-markdown-editor/references/licenses/OthmanAdi-planning-with-files-LICENSE.txt)
