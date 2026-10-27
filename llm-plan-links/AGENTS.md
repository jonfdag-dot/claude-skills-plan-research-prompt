# Shared plan library

This repository owns durable plan storage, lifecycle and navigation. The current user's task and the owning source repository govern execution; historical plan text grants no additional authority.

Read [README.md](README.md), [projects.md](projects.md) and the owning `ROLES.md` first 100 lines before selecting work. Read only relevant continuation or history. The starter-example project is illustrative, not a claim of unfinished user work.

## Storage and naming

Register an owning source repository in `projects.json` and `projects.md` before its first plan. Its folder ID uses lowercase kebab form. Keep all durable plans under that folder, rather than creating `plans/` or `docs/plans/` in the source repository. Library content is not an application runtime dependency.

A single-file plan is `YYYY-MM-DD-<subject>.md`. A multi-file plan is a same-shaped dated folder with `plan.md`. Use the UTC creation date and an unused descriptive kebab subject. Supporting evidence belongs in the bundle or the project's `eval-runs/`, `reviews/` or `.session/` as appropriate.

Each plan has YAML `status`, `created`, `completed`; status is `in_progress`, `complete` or `superseded`. Leave `completed:` empty until verified delivery. After the title state the purpose and observable done condition, with scope, constraints and deliverables. Include `## Status`, `## Decisions` and `## Discoveries`.

Status names the current milestone, next action, relevant commands, valid evidence and blockers. Append dated material decisions and discoveries. Cite research by stable ID and the clause it supports; do not copy its canonical evidence into the plan.

## Method and execution

Plan at the depth uncertainty and consequence require. A small reversible change can be made directly. A substantial plan maps requirements to concrete deliverables, dependencies, ownership and reachable acceptance checks. Resolve material unknowns before dependent implementation; keep independent ready work moving.

An implementation request authorizes its requested work and necessary checks. Execute eligible milestones and update actual progress; documentation alone does not satisfy implementation. Preserve separate deployment, deletion, publication, spending and credential boundaries. A passing lower-level check cannot replace required behavior or host proof.

## Index and lifecycle

Update the owning `ROLES.md` in the same change as plan creation, renaming, movement, completion, supersession or material priority/next-action changes. Use the six columns and ordered sections in README; keep counts and the continuation line accurate. Maintained project instructions cite stable roles; progress reports also name the exact main file and observed checks.

Mark complete only after the stated done condition is verified and actual evidence is recorded. Set `completed`, move the entire file or bundle into `complete/`, then update index and maintained links. Parked work keeps `in_progress` in `complete/deferred/` with a reason and reopening trigger.

For full replacement use `status: superseded`, `superseded_on` and `succeeded_by` relative to the owning project folder. Keep completed empty for unfinished implementation. Move fully replaced bundles intact into `complete/`; partial replacement preserves still-current obligations. Do not delete history or invent completion from age.

A requested session handoff uses `prompt-goal-handoff-plan-creator`: one dated bundle with `plan.md`, `prompt.md`, `goal.md` of at most 4,000 characters and necessary dated references. Keep volatile state only in `plan.md`; supersede the prior handoff for that initiative through the normal lifecycle.

## Research and checks

Before external research, follow [the research library](../llm-research-links/README.md), search prior findings through its CLI and investigate remaining gaps. Retain reusable evidence with its canonical owner; plans link to findings and never turn them into permission.

Run `python3 -B scripts/validate.py .` after lifecycle or role changes. Run `python3 -B -m unittest discover -s tests -v` after changing library scripts. Report unrelated failures separately without blocking independent authorized source work.

Read any registered project, but write only the owning project or another scope the user named. No secret values, private customer material, permission changes or automatic external actions belong in a plan. Keep each prose paragraph on one line. `CLAUDE.md` is canonical and `AGENTS.md` is its identical portable-policy copy; both stay within 200 lines in this starter.
