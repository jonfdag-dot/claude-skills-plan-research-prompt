# Claude Research & Planning Kit

Adopt a shared workflow for researching decisions, planning project work and resuming it across Claude Code sessions.

[Start the setup guide](CLAUDE.md)

The framework has three parts: `.claude/` supplies reusable skills, `llm-research-links/` keeps source-linked findings, and `llm-plan-links/` keeps each project's plans and progress. Connect one existing project first, then reuse the setup across your other projects.

## See how the pieces fit together

```text
claude-skills-plan-research-prompt/
├── README.md                  Overview and getting started
├── CLAUDE.md                  Step-by-step adoption guide
├── FILES.md                   Complete file map
├── .claude/
│   ├── CLAUDE.md              Shared working conventions
│   └── skills/                Eight workflows, references and templates
│       └── INDEX.md           Skill selection and resource guide
├── llm-research-links/
│   ├── sources.md             Register of sources and finding IDs
│   ├── notes/                 Reusable findings organized by subject
│   ├── reports/               Research syntheses
│   └── scripts/               Search, retrieval and evidence tools
└── llm-plan-links/
    ├── projects.json          Source-project registration
    ├── starter-example/       Example plan and ROLES.md index
    └── scripts/               Plan tools and project templates
```

The skills provide instructions for research, brainstorming, prompt writing, planning handoffs and maintaining the instructions themselves. Each skill keeps its supporting references and templates together so Claude can read the material needed for the current task.

The research library preserves findings with sources and stable IDs. The plan library records what a project intends to build, its decisions, progress and next action. A project's `ROLES.md` points to its current plans; those plans can cite the research that informed them.

A typical task starts by searching existing research, investigating gaps and saving useful evidence. A plan turns the decision into implementation work and records progress. When you switch sessions, a handoff carries the current state and next action forward. The libraries can serve multiple projects while each project's application code stays in its own repository.

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
