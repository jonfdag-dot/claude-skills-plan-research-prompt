# Claude research and planning starter kit

This folder shows how to give an agent reusable skills, shared research evidence and durable planning across active projects. Start here, then read only the instructions and indexes for the work you are doing. The examples are generic; they contain no imported personal research or project history.

## The three components

`.claude/` holds how the agent works. `llm-research-links/` holds what the research supports and where it came from. `llm-plan-links/` holds what a project intends to deliver, its current state and how completion will be checked. Keep these responsibilities distinct and connect them with routes and evidence IDs.

```text
claude-skills-plan-research-prompt/
├── CLAUDE.md                         this guide and parent instructions
├── README.md                         first-open pointer
├── FILES.md                          complete file tree
├── VERIFICATION.md                   actual export checks and limits
├── .gitignore                        excludes runtime state and local files
├── .claude/                          component 1: reusable agent setup
│   ├── CLAUDE.md                     shared conventions and library routes
│   ├── README.md                     installation and runtime boundaries
│   ├── PORTABILITY.md                export adaptations and omitted machinery
│   ├── export-manifest.json          resource provenance and delivered hashes
│   ├── agents/
│   │   ├── README.md                 native roles and tool boundaries
│   │   ├── worker-researcher.md       research and independent challenge
│   │   ├── worker-investigator.md     source-only diagnosis and review
│   │   ├── opus-worker.md             bounded implementation and integration
│   │   └── skills-author-worker.md    skill maintenance with static checks
│   └── skills/
│       ├── INDEX.md                  skill selection and every resource's purpose
│       ├── agents-markdown-editor/
│       ├── skill-creator/
│       ├── writing-skills/
│       ├── subagent-driven-development/
│       ├── prompt-goal-handoff-plan-creator/
│       ├── web-research/
│       ├── brainstorm/
│       ├── prompt-engineering-patterns/
│       └── using-superpowers/
├── llm-research-links/               component 2: reusable evidence
│   ├── CLAUDE.md / AGENTS.md          workflow and evidence boundaries
│   ├── README.md / INDEX.md           record contract and file map
│   ├── sources.md                    permanent register, read through the CLI
│   ├── projects.md                   applicability pointers
│   ├── taxonomy.md / topics.md        subject boundaries and repeat queries
│   ├── notes/                        navigation, domain index and sample finding
│   ├── reports/README.md             synthesis/report placement
│   ├── scripts/                      research CLI, validator and templates
│   └── tests/                        deterministic regression checks
└── llm-plan-links/                   component 3: durable plans
    ├── CLAUDE.md / AGENTS.md          storage and lifecycle rules
    ├── README.md / INDEX.md           plan format and navigation
    ├── projects.json / projects.md    source-project ownership registry
    ├── starter-example/
    │   ├── ROLES.md                  current/reference/archive pointers
    │   ├── 2026-10-27-example-plan.md illustrative state and acceptance
    │   ├── complete/                 completed, superseded and deferred history
    │   ├── eval-runs/                evidence for admitted evaluations
    │   ├── reviews/                  review evidence and decisions
    │   └── .session/                 ignored temporary resumable state
    ├── scripts/                      role reader, validator and templates
    └── tests/                        deterministic regression checks
```

Each skill folder contains `SKILL.md` plus its selected references, assets or scripts. Use [the skill resource map](.claude/skills/INDEX.md) for each file's purpose, [the research index](llm-research-links/INDEX.md) for evidence files and [the planning index](llm-plan-links/INDEX.md) for plan files. [FILES.md](FILES.md) expands every shipped file. Empty `.gitkeep` files preserve directory scaffolds; `.gitignore` files exclude local session state and incidental runtime files.

## Read and try it before installation

Open `.claude/README.md`, the skill index and the two library READMEs. Python 3.11 or newer runs the whole toolset; local Claude Code supplies native skill/agent discovery and permitted research tools. No API key is needed for the offline examples.

From this parent folder:

```sh
python3 -B llm-plan-links/scripts/roles.py --root llm-plan-links head starter-example
python3 -B llm-plan-links/scripts/roles.py --root llm-plan-links resolve starter-example --role 'example reference' --runtime claude --json
python3 -B llm-plan-links/scripts/validate.py llm-plan-links
```

From `llm-research-links/`:

```sh
python3 -B scripts/research.py labels --kind domain
python3 -B scripts/research.py find --entity research-evidence --limit 5
python3 -B scripts/research.py show R-0001
python3 -B scripts/validate.py .
```

The sample plan is a reference, and R-0001 documents only the local starter format with Checked UNKNOWN. Neither asserts product delivery or external source inspection.

## Integrate with any active project

1. Keep this folder as a reference copy. Choose the installed library homes; the defaults are `~/llm-plan-links/` and `~/llm-research-links/`. Copy those two complete repositories to those locations if they do not already exist. If either exists, reconcile its contents rather than overwriting it.
2. For skills across projects, review and merge `.claude/CLAUDE.md`, selected `skills/<name>/` folders and needed `agents/*.md` into your existing `~/.claude/`. Preserve the existing configuration. For one-project use, merge skills and agents into `<active-project>/.claude/` and merge the relevant conventions into that project's existing root instructions. Do not nest a second `.claude` folder.
3. Update library paths in the instructions and affected copied skills if using different locations. Relative reading links work while the three repositories stay siblings, including when installed under your home folder. A project-local `.claude/` using centrally stored libraries needs its relative reading links updated too.
4. Register the active source project in the plan library's `projects.json` and `projects.md`, create its plan folder and `ROLES.md`, and validate. Use the documented generic example as a shape, replacing it with actual source ownership.
5. Merge [the project instruction template](llm-plan-links/scripts/templates/project-CLAUDE.md.template) into the active project's `CLAUDE.md`: fill in its actual purpose, architecture, entrypoints, build/tests, library paths and boundaries. Keep existing instructions. This parent guide stays a guide to the kit; avoid copying its full contents into every project.
6. Start a fresh Claude Code session in the active project. Inspect `/memory` and `/agents`, then invoke a relevant skill. Confirm actual discovery and tool access on your installation. Disk validation alone cannot establish live activation.

Claude documents user instructions at `~/.claude/CLAUDE.md` and project instructions at a root or `.claude/CLAUDE.md`; skills live in named folders under the user or project skills root. The starter uses these native surfaces with a human index. See [memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills) and [subagents](https://code.claude.com/docs/en/sub-agents) for current runtime mechanics.

## Run the workflows

For deep research, ask `/web-research` to investigate a concrete question and the decision it informs. It searches existing findings first, investigates gaps and counterevidence, synthesizes, obtains a fresh challenge of consequential conclusions, audits support and retains useful findings. Ask `/brainstorm` to compare alternatives or pressure-test a proposal. The parent supplies library results to a no-shell researcher and owns final reasoning and writes.

For planning, ask for a plan in the registered project's library folder, with an observable outcome, dependencies and proving checks. The project's ROLES file is the stable entrypoint. An implementation request proceeds through authorized ready work and records actual results; writing the plan alone is not delivery.

For a new-session continuation, ask `/prompt-goal-handoff-plan-creator` for a dated bundle. Review and paste `prompt.md` first, then `goal.md` as a normal message. The bundle's `plan.md` is the single state record; `goal.md` stays within 4,000 characters. No special goal command is required.

For instruction maintenance, use `/agents-markdown-editor` with named files and a concrete goal. For skill changes, use `/skill-creator` and `/writing-skills`. Use `/subagent-driven-development` for bounded delegation and `/prompt-engineering-patterns` for reusable briefs. Do not preload every skill.

## Repository and permission boundaries

This public repository tracks all three component directories together, including the hidden `.claude/` folder. A normal clone includes every skill, template and library; no submodules are required. The two library folders can also be copied out and maintained independently. Local session contents remain ignored while `.gitkeep` preserves the required empty scaffold.

The copied skills are portable adaptations, with source notices preserved and changes listed in `.claude/PORTABILITY.md`. This is a Claude-only setup; Codex parity, custom BM25 routing, private hooks, model pins, credentials, logs, memories and personal research were not exported. Existing recipient controls still apply. No instruction file or plan can authorize deployment, deletion, spending, publication or access-policy changes.
