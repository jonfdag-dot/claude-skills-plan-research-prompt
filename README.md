# Claude Research & Planning Kit

Reusable Claude Code skills, research findings, and project plans in one starter kit. Includes nine skills, four worker definitions, templates, and offline validators.

[Setup guide](CLAUDE.md) · [Skill index](.claude/skills/INDEX.md) · [All files](FILES.md)

## See what's inside

```text
.
├── CLAUDE.md                 Setup guide and instructions for the whole kit
├── .claude/
│   ├── CLAUDE.md             Shared conventions and library routing
│   ├── skills/               Nine skills with references and templates
│   └── agents/               Research, review, implementation, skill workers
├── llm-plan-links/           Plans, decisions, progress, and handoffs
│   ├── projects.json         Maps source projects to their plan folders
│   └── starter-example/      Example plan and ROLES.md navigation
└── llm-research-links/       Sources, findings, and research reports
    ├── notes/                Findings organized by subject
    ├── reports/              Research syntheses
    └── scripts/research.py   Search, inspect, and save findings
```

## Add it to your setup

1. Merge the selected `.claude/skills/` and `.claude/agents/` folders into `~/.claude/` for all projects, or your project's `.claude/` for local use. Preserve existing files.
2. Put the two libraries at `~/llm-plan-links/` and `~/llm-research-links/`, or update the routes to match your locations.
3. Merge the relevant shared instructions into your existing `CLAUDE.md`. Use the [project template](llm-plan-links/scripts/templates/project-CLAUDE.md.template) to connect an active project to both libraries.
4. Start a fresh Claude Code session. Check `/memory` and `/agents`, then invoke a skill below.

Use Python 3.11+ for the bundled tools. See the [setup guide](CLAUDE.md#integrate-with-any-active-project) for path changes and installation details.

## Choose a skill

Type `/skill-name` followed by your request in Claude Code. Each link opens the skill's instructions.

| Skill | Example request |
| --- | --- |
| [agents-markdown-editor](.claude/skills/agents-markdown-editor/SKILL.md) | Audit this project's CLAUDE.md for conflicting or stale instructions. |
| [skill-creator](.claude/skills/skill-creator/SKILL.md) | Create a reusable skill for reviewing API changes. |
| [writing-skills](.claude/skills/writing-skills/SKILL.md) | Tighten this skill's description, steps, and examples. |
| [subagent-driven-development](.claude/skills/subagent-driven-development/SKILL.md) | Split this plan into bounded worker tasks and integrate their results. |
| [prompt-goal-handoff-plan-creator](.claude/skills/prompt-goal-handoff-plan-creator/SKILL.md) | Create a continuation bundle for the next session. |
| [web-research](.claude/skills/web-research/SKILL.md) | Deep-research this question, challenge the conclusion, and save useful findings. |
| [brainstorm](.claude/skills/brainstorm/SKILL.md) | Pressure-test this proposal against simpler alternatives. |
| [prompt-engineering-patterns](.claude/skills/prompt-engineering-patterns/SKILL.md) | Turn these requirements into a clear reusable prompt. |
| [using-superpowers](.claude/skills/using-superpowers/SKILL.md) | Choose the relevant skill for this task. |

## Keep plans across sessions

[llm-plan-links](llm-plan-links/README.md) stores each project's plans, decisions, progress, and handoffs. Each project has a `ROLES.md` index pointing to its current work.

Register your source project in `projects.json` and `projects.md`, create its plan folder, then copy the [plan template](llm-plan-links/scripts/templates/plan.md.template). Ask Claude to maintain that plan and its ROLES entry as work progresses. Move verified completed plans into `complete/`.

For a session handoff, request `/prompt-goal-handoff-plan-creator`. Review and paste `prompt.md` into the new session, followed by `goal.md`; `plan.md` holds the current state.

## Reuse research across projects

[llm-research-links](llm-research-links/README.md) stores source-linked findings with stable IDs, scope, evidence labels, and recheck conditions. Reports hold the synthesis; plans cite the findings that informed a decision.

Ask `/web-research` to search existing findings first, investigate remaining gaps, check counterevidence, and retain useful results. Explicit deep research adds an independent challenge of consequential conclusions. The library starts with one local format example.

From the research library:

```sh
python3 -B scripts/research.py labels --kind domain
python3 -B scripts/research.py find --entity research-evidence --limit 5
python3 -B scripts/research.py show R-0001
```

To save new findings, fill the JSON from `research.py template`, run `research.py add --dry-run packet.json`, then `research.py add packet.json`. Validate either library from its root with `python3 -B scripts/validate.py .`.

[Export notes and licenses](.claude/PORTABILITY.md) · [Verification results](VERIFICATION.md)
