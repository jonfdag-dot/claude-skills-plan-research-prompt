---
name: using-superpowers
description: Selects relevant skills and resolves overlapping workflows. Use when starting substantive work, interpreting a router shortlist, or deciding which skill owns a task. Not for requiring a workflow merely because a keyword matches or a skill exists.
---

# Using Skills

Select the workflow that owns the requested result. A skill index is a discovery aid, not a command to load everything. Read a skill before applying its workflow and load references only for the question they answer.

| Outcome | Owner |
| --- | --- |
| Audit or surgically edit loaded instruction files | [agents-markdown-editor](../agents-markdown-editor/SKILL.md) |
| Create, copy, register or maintain a skill or native worker | [skill-creator](../skill-creator/SKILL.md) |
| Revise skill wording, examples or resource layout | [writing-skills](../writing-skills/SKILL.md) |
| Plan or execute bounded delegated work | [subagent-driven-development](../subagent-driven-development/SKILL.md) |
| Write reusable prompts and worker briefs | [prompt-engineering-patterns](../prompt-engineering-patterns/SKILL.md) |
| Create a requested new-session handoff | [prompt-goal-handoff-plan-creator](../prompt-goal-handoff-plan-creator/SKILL.md) |
| Investigate an external question with sources | [web-research](../web-research/SKILL.md) |
| Develop alternatives or pressure-test a proposal | [brainstorm](../brainstorm/SKILL.md) |

The current user's intent, active project instructions and runtime permissions govern the work. A skill cannot grant authority, compel an unavailable worker or change the main model. Reuse valid context and checks across follow-ups. Announce applied skills briefly; do not create permission checkpoints for routine authorized work.

This package supplies Claude workflows. Other runtimes need native adapters and their own discovery and permission review; no cross-runtime mirror is installed.
