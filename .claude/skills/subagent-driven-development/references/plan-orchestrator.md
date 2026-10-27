# Plan-Install Orchestration

The plan is already written. Execute its requested outcome without losing decisions, repeating completed work, or expanding scope. Apply the task loop in [SKILL.md](../SKILL.md); plans may contain both parallel work and sequential dependencies.

If execution requires designing, decomposing, or materially revising the plan, first read [long-form-planning.md](long-form-planning.md) under the entrypoint's mandatory loading rule. Ordinary execution of an unchanged ready task does not reopen settled planning.

## 1. Roles

The orchestrator owns scope, dependencies, the global register, decisions, integration, and completion. Workers own bounded deliverables and return compact evidence. Use independent review only when requested, required by project rules, or justified by a concrete unresolved risk. The root may inspect relevant sources, run a focused check, or make a small fix when this avoids another handoff.

## 2. Pre-flight

Reuse or record the compact acceptance contract and task register. Resolve material unanswered decisions before dependent edits; do not require a blanket approval of the register. Preserve unrelated dirty files rather than requiring a clean tree, automatic stash, or separate commit.

Record the relevant starting state and actual available check commands. Do not schedule a gate before the task that creates it. Name genuinely unavailable required evidence without pretending it passed; attempt available browser/device checks when authorized and required.

## 3. Packetization

Use the plan's work groups where they remain useful. Preserve explicit dependencies and binding ordering constraints; ranking or historical packet order alone does not make independent work serial.

Split oversized work at useful interfaces and write boundaries. Combine small related items when the same owner can complete them efficiently without broadening scope. Do not split solely because a task touches three files or require a checkpoint between packets.

Separate work requiring a still-missing decision or authority from ready work. Keep required blocked deliverables in the register rather than silently dropping them from completion.

## 4. Run state

Reuse the existing plan, task register, or `~/llm-plan-links/<project-slug>/.session/ledger.md`. If an existing run uses `gates.json`, retain it without imposing a new schema or parallel register. Use task-specific artifact paths for detailed results.

The root persists task/attempt/parent identities, ownership, status, dependency versions, decisions, worker handles, accepted evidence, and remaining work before releasing dependencies. Workers return updates and write only assigned artifacts; read-only workers return full reports for root persistence. Follow [evidence-handoff.md](evidence-handoff.md). Do not clear an existing session directory or overwrite another run's results.

## 5. Execute

Dispatch eligible packets using [the worker template](../implementer-prompt.md). Parallelize independent work under [parallel-dispatch.md](parallel-dispatch.md). Process results and refill capacity continuously; no default per-packet reviewer, human checkpoint, fresh-agent requirement, or commit.

On a blocker, resolve context or dependencies within the authorized scope while unrelated work continues. A worker's ordinary uncertainty is not an automatic user interruption. Escalate when the missing choice or authority materially changes the outcome.

Commit, install, deploy, or mutate shared external state only within existing authorization and project rules. Serialize shared Git operations; commit granularity follows the requested delivery and recoverability needs, not the number of workers.

## 6. Scope and drift

Workers read relevant plan sections, interface contracts, current source anchors, and required skills. A stale line number can be resolved by matching the intended content. If content drift changes the spec's meaning or acceptance, report the exact conflict before dependent edits; do not follow a superseded snippet blindly.

Allow in-scope adjustments that preserve the requested behavior and downstream interface. A needed change outside the assigned write boundary returns to the root for ownership coordination; neither worker nor root silently expands user scope.

## 7. Verification and repair

Use the plan's required evidence, scaled to the requested behavior. For code, run focused checks; for plans, verify dependencies and decisions; for research, supply source evidence. Broader suites or final reviews need a binding requirement or concrete unresolved risk.

Accepted findings cite an acceptance violation or a reproducible critical safety/corruption defect. Capture the reproducer, make a surgical repair, and revisit only affected requirements. Reuse valid prior evidence. Repeated failure without progress requires a revised brief or an explicit blocker.

## 8. Resume and completion

After compaction or restart, read the existing register and result paths, reconcile current user corrections against the summary, check relevant versions and live workers, and resume unfinished work. Reject superseded-attempt completions and inspect uncertain external effects before retrying. Do not repeat completed packets or verification with still-valid evidence.

Complete when the requested deliverables and required checks are satisfied, with required blockers resolved or explicitly deferred by the user. Report any unavailable required proof as a limitation, never a pass. Update the existing plan's lifecycle as its project requires. Do not archive/move plans, reconcile unrelated docs, or trigger a session closer unless that work is part of the authorized outcome.
