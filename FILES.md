# Complete file map

This is the complete shipped tree, excluding local Git metadata. Read the parent CLAUDE.md for integration, the skill index for each supporting resource, and each library INDEX.md for its files.

```text
claude-skills-plan-research-prompt/
├── .claude/
│   ├── agents/
│   │   ├── README.md
│   │   ├── opus-worker.md
│   │   ├── skills-author-worker.md
│   │   ├── worker-investigator.md
│   │   └── worker-researcher.md
│   ├── skills/
│   │   ├── agents-markdown-editor/
│   │   │   ├── references/
│   │   │   │   ├── licenses/
│   │   │   │   │   └── OthmanAdi-planning-with-files-LICENSE.txt
│   │   │   │   ├── code-first-cleanup.md
│   │   │   │   ├── cut-classes.md
│   │   │   │   ├── gates.md
│   │   │   │   ├── loaded-set.md
│   │   │   │   ├── model-overlays.md
│   │   │   │   ├── placement-model.md
│   │   │   │   ├── prove.md
│   │   │   │   ├── review-record.md
│   │   │   │   ├── rule-grammar.md
│   │   │   │   └── worked-examples.md
│   │   │   ├── scripts/
│   │   │   │   └── steward-lint.py
│   │   │   └── SKILL.md
│   │   ├── brainstorm/
│   │   │   ├── references/
│   │   │   │   ├── brainstorming.md
│   │   │   │   ├── challenge.md
│   │   │   │   ├── domain-expertise.md
│   │   │   │   ├── epistemics.md
│   │   │   │   ├── knowledge-library.md
│   │   │   │   ├── lenses.md
│   │   │   │   ├── output-template.md
│   │   │   │   ├── research-pipeline.md
│   │   │   │   └── rules-engine.md
│   │   │   └── SKILL.md
│   │   ├── prompt-engineering-patterns/
│   │   │   ├── assets/
│   │   │   │   ├── few-shot-examples.json
│   │   │   │   └── prompt-template-library.md
│   │   │   ├── references/
│   │   │   │   ├── chain-of-thought.md
│   │   │   │   ├── details.md
│   │   │   │   ├── few-shot-learning.md
│   │   │   │   ├── long-horizon-context.md
│   │   │   │   ├── orchestration-modes.md
│   │   │   │   ├── prompt-architect.md
│   │   │   │   ├── prompt-optimization.md
│   │   │   │   ├── prompt-templates.md
│   │   │   │   ├── sources-and-contradictions.md
│   │   │   │   ├── subagent-dispatch.md
│   │   │   │   └── system-prompts.md
│   │   │   └── SKILL.md
│   │   ├── prompt-goal-handoff-plan-creator/
│   │   │   ├── assets/
│   │   │   │   ├── goal.md.template
│   │   │   │   ├── plan.md.template
│   │   │   │   ├── prompt.md.template
│   │   │   │   └── references-README.md.template
│   │   │   ├── references/
│   │   │   │   ├── bundle-contract.md
│   │   │   │   ├── done-criteria.md
│   │   │   │   └── evidence.md
│   │   │   ├── scripts/
│   │   │   │   └── check_handoff.py
│   │   │   └── SKILL.md
│   │   ├── skill-creator/
│   │   │   ├── assets/
│   │   │   │   └── template-skill/
│   │   │   │       └── SKILL.md.template
│   │   │   ├── references/
│   │   │   │   ├── codex-cascade.md
│   │   │   │   ├── ecosystem-nesting.md
│   │   │   │   └── verification-and-eval-admission.md
│   │   │   ├── scripts/
│   │   │   │   └── quick_validate.py
│   │   │   ├── LICENSE.txt
│   │   │   └── SKILL.md
│   │   ├── subagent-driven-development/
│   │   │   ├── references/
│   │   │   │   ├── evidence-handoff.md
│   │   │   │   ├── long-form-planning.md
│   │   │   │   ├── native-role-routing.md
│   │   │   │   ├── parallel-dispatch.md
│   │   │   │   ├── plan-orchestrator.md
│   │   │   │   ├── task-design.md
│   │   │   │   ├── team-runtime.md
│   │   │   │   └── team-selection.md
│   │   │   ├── SKILL.md
│   │   │   ├── implementer-prompt.md
│   │   │   └── task-reviewer-prompt.md
│   │   ├── using-superpowers/
│   │   │   └── SKILL.md
│   │   ├── web-research/
│   │   │   ├── references/
│   │   │   │   ├── evidence-and-retention.md
│   │   │   │   ├── query-operators.md
│   │   │   │   ├── second-pass.md
│   │   │   │   ├── source-tiers.md
│   │   │   │   └── version-and-recency.md
│   │   │   └── SKILL.md
│   │   ├── writing-skills/
│   │   │   ├── references/
│   │   │   │   ├── anthropic-best-practices.md
│   │   │   │   ├── claude-md-testing-example.md
│   │   │   │   ├── graphviz-conventions.dot
│   │   │   │   ├── persuasion-principles.md
│   │   │   │   ├── testing-and-bulletproofing.md
│   │   │   │   ├── testing-skills-with-subagents.md
│   │   │   │   └── token-efficiency.md
│   │   │   ├── scripts/
│   │   │   │   └── render-graphs.js
│   │   │   └── SKILL.md
│   │   └── INDEX.md
│   ├── CLAUDE.md
│   └── README.md
├── llm-plan-links/
│   ├── scripts/
│   │   ├── templates/
│   │   │   ├── plan.md.template
│   │   │   └── project-CLAUDE.md.template
│   │   ├── roles.py
│   │   └── validate.py
│   ├── starter-example/
│   │   ├── .session/
│   │   │   └── .gitkeep
│   │   ├── complete/
│   │   │   ├── deferred/
│   │   │   │   └── .gitkeep
│   │   │   ├── eval-runs/
│   │   │   │   └── .gitkeep
│   │   │   └── .gitkeep
│   │   ├── eval-runs/
│   │   │   └── .gitkeep
│   │   ├── reviews/
│   │   │   └── .gitkeep
│   │   ├── 2026-10-27-example-plan.md
│   │   └── ROLES.md
│   ├── tests/
│   │   ├── test_roles.py
│   │   └── test_validate.py
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── INDEX.md
│   ├── README.md
│   ├── projects.json
│   └── projects.md
├── llm-research-links/
│   ├── notes/
│   │   ├── research-evidence/
│   │   │   ├── README.md
│   │   │   ├── index.md
│   │   │   └── starter-format.md
│   │   └── README.md
│   ├── reports/
│   │   └── README.md
│   ├── scripts/
│   │   ├── templates/
│   │   │   ├── finding.json
│   │   │   ├── report.md.template
│   │   │   └── starter-record.json
│   │   ├── research.py
│   │   └── validate.py
│   ├── tests/
│   │   ├── test_research.py
│   │   ├── test_validate.py
│   │   ├── test_validate_domains.py
│   │   ├── test_validate_line_links.py
│   │   └── test_validate_ownership.py
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── INDEX.md
│   ├── README.md
│   ├── projects.md
│   ├── sources.md
│   ├── taxonomy.md
│   └── topics.md
├── CLAUDE.md
├── FILES.md
└── README.md
```
