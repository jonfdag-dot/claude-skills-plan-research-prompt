---
name: subagent-driven-development
description: Coordinates delegated development, planning, and research through task ownership, dependencies, native roles, acceptance, and recovery. Use when designing or executing delegated plans, selecting a team, dispatching independent work, integrating worker results, or resuming unfinished work across compaction or sessions. Not for prompt text alone → use prompt-engineering-patterns; competing bug causes → use parallel-debugging; parallel implementation interfaces → use parallel-feature-development; review finding synthesis → use multi-reviewer-patterns; a small task better completed directly.
---

# Subagent-Driven Development

Coordinate bounded work to complete the user's requested outcome. The parent owns reasoning, integration, shared state and completion. Prefer direct work for a small task that gains nothing from delegation.

## Planning and readiness

Before designing or materially revising a delegated plan, read [long-form-planning.md](references/long-form-planning.md) completely. Scale its use to the task; do not invent infrastructure or approval ceremonies. Durable plans belong in the shared plan library under the owning project's registered folder, with one `ROLES.md` entry and clear acceptance.

Each task needs a goal, task/attempt identifier, context, constraints, owner, allowed files/resources, dependencies, acceptance evidence and expected output. Reuse the existing task register rather than introducing a second ledger. Dispatch only when inputs exist, effects are authorized and necessary checks can run.

Use [native-role-routing.md](references/native-role-routing.md) before selecting a worker and [evidence-handoff.md](references/evidence-handoff.md) when briefing, accepting or recovering work. Use [task-design.md](references/task-design.md) for decomposition, [team-selection.md](references/team-selection.md) for team sizing and [parallel-dispatch.md](references/parallel-dispatch.md) for independent ready work.

## Task loop

1. Dispatch independent ready tasks with exclusive write ownership. Use [implementer-prompt.md](implementer-prompt.md) for the brief. Serialize actual dependencies, shared files, Git mutations and external state changes.
2. Read the returning worker's decisive evidence against the assigned requirements and delivered revision. A DONE message alone is insufficient. Record accepted results and release dependent work; do not repeat the worker's whole investigation.
3. Resolve an actual gap with a bounded repair, clarification or changed assignment. Follow up only while requested work remains unfinished; stop after two automatic continuations. Preserve the symptom and attempted corrections rather than resetting limits by changing workers.
4. Integrate at the boundary where outputs meet and run the focused check that proves the combined behavior. Continue until the requested outcome and required checks are satisfied or a concrete prerequisite requires user input.

## Roles and evidence

Use the active project's required specialist first. Otherwise the bundled `worker-researcher` handles external evidence, `worker-investigator` handles read-only diagnosis/review, `skills-author-worker` handles skills and `opus-worker` handles implementation/integration. Discover actual role availability; do not infer permissions or model policy from a name. The native definitions inherit the main model. All workers are leaves by policy; only the parent dispatches.

The research worker has no shell: the parent supplies retained-library `find`/`show` results and necessary executable-check output. Workers return evidence packets, never allocate permanent IDs or write the shared research library. The parent reconciles and saves a batch.

Use [task-reviewer-prompt.md](task-reviewer-prompt.md) only for a warranted independent review; the author cannot independently review its own changes. Report correctness or requirement gaps with exact evidence, omitting preferences. A passing decisive check closes an unchanged criterion; rerun only when changed evidence or an unresolved gap requires it. No automatic full suite, model evaluation or review panel follows from delegation.

## Continuity and completion

Keep the user's current intent, accepted constraints, authority boundaries, task ownership, valid results, pending checks and next action in the existing plan or task record. Use [plan-orchestrator.md](references/plan-orchestrator.md) to execute an existing plan. A handoff is context rather than permission; current source and user instructions outrank stale task text.

Report the integrated result, actual checks, material limitations and remaining prerequisites. Stop task-owned processes when no longer needed, preserving shared resources. Skill instructions do not enforce locks, permission policy or unattended continuation.
