# Skill index

These eight skills are adapted Claude copies. Read an entrypoint when its task fits, then only the supporting references needed. The index is maintained by hand and is not a machine router. Commands below are native skill names after installation.

| Skill | Use | Example command |
| --- | --- | --- |
| [agents-markdown-editor](agents-markdown-editor/SKILL.md) | Audit loaded instructions and apply authorized surgical edits. | `/agents-markdown-editor` |
| [skill-creator](skill-creator/SKILL.md) | Create, import, register and maintain skills. | `/skill-creator` |
| [writing-skills](writing-skills/SKILL.md) | Write skill descriptions, instructions, examples and selective references. | `/writing-skills` |
| [subagent-driven-development](subagent-driven-development/SKILL.md) | Plan and coordinate bounded delegated work with evidence and integration. | `/subagent-driven-development` |
| [prompt-goal-handoff-plan-creator](prompt-goal-handoff-plan-creator/SKILL.md) | Create a requested continuation bundle with prompt, goal and state. | `/prompt-goal-handoff-plan-creator` |
| [web-research](web-research/SKILL.md) | Research claims, challenge consequential conclusions and retain evidence. | `/web-research` |
| [brainstorm](brainstorm/SKILL.md) | Pressure-test an idea with alternatives, research and material counterexamples. | `/brainstorm` |
| [prompt-engineering-patterns](prompt-engineering-patterns/SKILL.md) | Write reusable model prompts and worker briefs with clear contracts. | `/prompt-engineering-patterns` |

## Resource map

Each named skill folder has a SKILL.md entrypoint. The following files retain details, templates or deterministic tools, with their purpose indicated by title or filename. They load selectively; script files run only when their entrypoint calls for the check.

### agents-markdown-editor

| Resource | Purpose |
| --- | --- |
| [references/code-first-cleanup.md](agents-markdown-editor/references/code-first-cleanup.md) | Code and context anchors for instruction cleanup |
| [references/cut-classes.md](agents-markdown-editor/references/cut-classes.md) | Cut classes |
| [references/gates.md](agents-markdown-editor/references/gates.md) | Static gates |
| [references/licenses/OthmanAdi-planning-with-files-LICENSE.txt](agents-markdown-editor/references/licenses/OthmanAdi-planning-with-files-LICENSE.txt) | OthmanAdi planning with files LICENSE |
| [references/loaded-set.md](agents-markdown-editor/references/loaded-set.md) | Loaded set and budgets |
| [references/model-overlays.md](agents-markdown-editor/references/model-overlays.md) | Model guidance as scoped review leads |
| [references/placement-model.md](agents-markdown-editor/references/placement-model.md) | Placement model: eight homes |
| [references/prove.md](agents-markdown-editor/references/prove.md) | Prove: does a rule still change behaviour? |
| [references/review-record.md](agents-markdown-editor/references/review-record.md) | Review record |
| [references/rule-grammar.md](agents-markdown-editor/references/rule-grammar.md) | Rule grammar |
| [references/worked-examples.md](agents-markdown-editor/references/worked-examples.md) | Generic editing examples |
| [scripts/steward-lint.py](agents-markdown-editor/scripts/steward-lint.py) | steward lint |

### skill-creator

| Resource | Purpose |
| --- | --- |
| [LICENSE.txt](skill-creator/LICENSE.txt) | LICENSE |
| [assets/template-skill/SKILL.md.template](skill-creator/assets/template-skill/SKILL.md.template) | Skill Scaffold |
| [references/codex-cascade.md](skill-creator/references/codex-cascade.md) | Runtime scope |
| [references/ecosystem-nesting.md](skill-creator/references/ecosystem-nesting.md) | Native registration in this starter |
| [references/verification-and-eval-admission.md](skill-creator/references/verification-and-eval-admission.md) | Verification and eval admission |
| [scripts/quick_validate.py](skill-creator/scripts/quick_validate.py) | quick validate |

### writing-skills

| Resource | Purpose |
| --- | --- |
| [references/anthropic-best-practices.md](writing-skills/references/anthropic-best-practices.md) | Skill authoring best practices |
| [references/claude-md-testing-example.md](writing-skills/references/claude-md-testing-example.md) | Testing CLAUDE.md Skills Documentation |
| [references/graphviz-conventions.dot](writing-skills/references/graphviz-conventions.dot) | graphviz conventions |
| [references/persuasion-principles.md](writing-skills/references/persuasion-principles.md) | Historical persuasion hypotheses for skill design |
| [references/testing-and-bulletproofing.md](writing-skills/references/testing-and-bulletproofing.md) | Scenario selection and instruction forms |
| [references/testing-skills-with-subagents.md](writing-skills/references/testing-skills-with-subagents.md) | Conditional skill testing with isolated evaluators |
| [references/token-efficiency.md](writing-skills/references/token-efficiency.md) | Resource selection and optional compression |
| [scripts/render-graphs.js](writing-skills/scripts/render-graphs.js) | render graphs |

### subagent-driven-development

| Resource | Purpose |
| --- | --- |
| [implementer-prompt.md](subagent-driven-development/implementer-prompt.md) | Worker Prompt Template |
| [references/evidence-handoff.md](subagent-driven-development/references/evidence-handoff.md) | Evidence Handoff |
| [references/long-form-planning.md](subagent-driven-development/references/long-form-planning.md) | Planning Long-Running Delegated Development |
| [references/native-role-routing.md](subagent-driven-development/references/native-role-routing.md) | Native role routing |
| [references/parallel-dispatch.md](subagent-driven-development/references/parallel-dispatch.md) | Parallel Fan-Out — Independent Tasks |
| [references/plan-orchestrator.md](subagent-driven-development/references/plan-orchestrator.md) | Plan-Install Orchestration |
| [references/task-design.md](subagent-driven-development/references/task-design.md) | Task Design and Dependencies |
| [references/team-runtime.md](subagent-driven-development/references/team-runtime.md) | Native communication and lifecycle |
| [references/team-selection.md](subagent-driven-development/references/team-selection.md) | Team Selection |
| [task-reviewer-prompt.md](subagent-driven-development/task-reviewer-prompt.md) | Task Reviewer Prompt Template |

### prompt-goal-handoff-plan-creator

| Resource | Purpose |
| --- | --- |
| [assets/goal.md.template](prompt-goal-handoff-plan-creator/assets/goal.md.template) | goal.md |
| [assets/plan.md.template](prompt-goal-handoff-plan-creator/assets/plan.md.template) | <Initiative> handoff — YYYY-MM-DD |
| [assets/prompt.md.template](prompt-goal-handoff-plan-creator/assets/prompt.md.template) | prompt.md |
| [assets/references-README.md.template](prompt-goal-handoff-plan-creator/assets/references-README.md.template) | References for <initiative> handoff YYYY-MM-DD |
| [references/bundle-contract.md](prompt-goal-handoff-plan-creator/references/bundle-contract.md) | Bundle contract |
| [references/done-criteria.md](prompt-goal-handoff-plan-creator/references/done-criteria.md) | Done criteria |
| [references/evidence.md](prompt-goal-handoff-plan-creator/references/evidence.md) | Evidence |
| [scripts/check_handoff.py](prompt-goal-handoff-plan-creator/scripts/check_handoff.py) | check handoff |

### web-research

| Resource | Purpose |
| --- | --- |
| [references/evidence-and-retention.md](web-research/references/evidence-and-retention.md) | Evidence and retention |
| [references/query-operators.md](web-research/references/query-operators.md) | Query operator craft |
| [references/second-pass.md](web-research/references/second-pass.md) | Second research pass |
| [references/source-tiers.md](web-research/references/source-tiers.md) | Source selection |
| [references/version-and-recency.md](web-research/references/version-and-recency.md) | Version and recency disambiguation |

### brainstorm

| Resource | Purpose |
| --- | --- |
| [references/brainstorming.md](brainstorm/references/brainstorming.md) | Clarification and the decision register |
| [references/challenge.md](brainstorm/references/challenge.md) | Challenge — the autonomous procedure, and the optional decision interview |
| [references/domain-expertise.md](brainstorm/references/domain-expertise.md) | Domain expertise — transferable method, selected by mechanism |
| [references/epistemics.md](brainstorm/references/epistemics.md) | Epistemics — labels, ladders, provenance, stage-relative support, and economics |
| [references/knowledge-library.md](brainstorm/references/knowledge-library.md) | Repository evidence and landing homes |
| [references/lenses.md](brainstorm/references/lenses.md) | Lenses — Socratic categories, the repertoire, transformations, form factors, and the candidate card |
| [references/output-template.md](brainstorm/references/output-template.md) | Output template — presenting the decision, proportionally |
| [references/research-pipeline.md](brainstorm/references/research-pipeline.md) | Research pipeline — purposes, packets, the host adapter, receipts, and stopping |
| [references/rules-engine.md](brainstorm/references/rules-engine.md) | Rules engine — next action, stage gates, verdicts, experiments, and the three kinds of validation |

### prompt-engineering-patterns

| Resource | Purpose |
| --- | --- |
| [assets/few-shot-examples.json](prompt-engineering-patterns/assets/few-shot-examples.json) | few shot examples |
| [assets/prompt-template-library.md](prompt-engineering-patterns/assets/prompt-template-library.md) | Prompt Template Library |
| [references/chain-of-thought.md](prompt-engineering-patterns/references/chain-of-thought.md) | Reasoning Guidance |
| [references/details.md](prompt-engineering-patterns/references/details.md) | prompt-engineering-patterns — detailed patterns and worked examples |
| [references/few-shot-learning.md](prompt-engineering-patterns/references/few-shot-learning.md) | Few-Shot Learning Guide |
| [references/long-horizon-context.md](prompt-engineering-patterns/references/long-horizon-context.md) | Wording Context and Session Handoffs |
| [references/orchestration-modes.md](prompt-engineering-patterns/references/orchestration-modes.md) | Wording Workflow and Escalation Requests |
| [references/prompt-architect.md](prompt-engineering-patterns/references/prompt-architect.md) | Prompt Architect |
| [references/prompt-optimization.md](prompt-engineering-patterns/references/prompt-optimization.md) | Prompt Optimization Guide |
| [references/prompt-templates.md](prompt-engineering-patterns/references/prompt-templates.md) | Prompt Template Systems |
| [references/sources-and-contradictions.md](prompt-engineering-patterns/references/sources-and-contradictions.md) | Sources, Contradictions, and Dropped Claims |
| [references/subagent-dispatch.md](prompt-engineering-patterns/references/subagent-dispatch.md) | Wording a Subagent Brief |
| [references/system-prompts.md](prompt-engineering-patterns/references/system-prompts.md) | System Prompt Design |

## Static checks

Use Python 3.11 or newer for the complete kit. Validate a skill with `python3 -B <skill-creator>/scripts/quick_validate.py <skill-folder>`. The instruction auditor is `agents-markdown-editor/scripts/steward-lint.py`; the handoff checker is `prompt-goal-handoff-plan-creator/scripts/check_handoff.py`. No model evaluation follows from these checks. Optional graph rendering additionally requires Node and Graphviz; it is not needed for ordinary skill authoring.
