# Parallel Fan-Out — Independent Tasks

Dispatch independent coding, planning, and research when parallel execution or isolated context improves delivery. Use the shared task loop and acceptance rules in [SKILL.md](../SKILL.md).

## Identify Independent Domains

Group work by outcome and dependencies, not an arbitrary file count or batch size. Independent source investigations, plan sections, and disjoint code changes can run together. Supply shared decisions and interfaces before dependent implementation. Serialize overlapping writes, shared Git operations, and external state mutations; a shared checkout is not an isolated worktree. For parallel writers in Claude Code, `isolation: worktree` gives each worker its own checkout, and `worktree.baseRef` sets its base: `fresh` branches from the origin default branch, `head` from the current HEAD.

Give every deliverable one accountable owner in the global task register. Workers receive enough context to act without reconstructing the whole session. Use [the worker template](../implementer-prompt.md), including dependencies, write boundaries, acceptance evidence, and result paths.

## Capacity and Leaf Workers

Choose concurrency from ready independent work, actual available capacity, and the user's budget. Do not impose a skill-level cap or launch workers simply to fill slots. Claude Code's runtime controls are `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and, for workflows, `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS`; read their current defaults on the [sub-agents](https://code.claude.com/docs/en/sub-agents) and [workflows](https://code.claude.com/docs/en/workflows) pages instead of copying numbers here. Projects can set lower caps: llm-research-links allows three concurrent subagents at depth one. Count live workers against one global allowance, accounting for whether the runtime includes the root in its limit.

Workers are leaves and never spawn or delegate. Return any proposed independent subtask to the root, which records ownership and handles dispatch in the existing register. Do not create descendant queues or a second controller.

## Native Tools and Worker Reuse

Use the actual tools exposed in the current session. On surfaces with `spawn_agent`, `followup_task`, `send_message`, `list_agents`, `wait_agent`, and `interrupt_agent`, follow their current contracts. In Claude Code the tools are Agent (spawn), SendMessage (continue a worker) and TaskStop (stop one); TaskOutput was removed in 2.1.277. Tool names and behavior can differ across clients; a standalone CLI version is not proof of the IDE's live capabilities. Consult current official documentation only for unresolved questions.

Prefer `followup_task` for a compatible available worker when it can start another turn. A plain message may only queue context. A follow-up sent to a running worker can steer its current task: do not treat it as a clean reassignment. Confirm completion and transfer ownership before issuing unrelated work.

Reused threads retain context. Supply task/attempt/parent IDs, boundaries, current dependency versions, and a unique result path explicitly. Follow [native-role-routing.md](native-role-routing.md): fresh independent Codex tasks default to `fork_turns="none"` where supported; justify inherited history and reuse related clarification/repair threads. Never reuse the author as an independent reviewer or rotate on a fixed job count.

Use a close/release operation only if the active toolset exposes one and its result confirms release. A completion, interruption, timeout, or silence alone does not establish that an open thread stopped counting against capacity. If spawning fails at capacity, use available compatible threads or continue useful root work; avoid repeated spawn attempts without evidence of changed capacity.

## Continuous Dispatch and Integration

Process each result as it arrives. Check version-bound acceptance evidence using [evidence-handoff.md](evidence-handoff.md), persist accepted results and decisions, integrate the output, and dispatch newly ready work without waiting for unrelated jobs. Required repair and integration work compete for capacity alongside new research; do not let completed but unintegrated results accumulate indefinitely.

For a 100-job run, keep all task IDs and dependencies in the existing register, but dispatch only ready work that fits the live allowance. Partial and random completion order changes eligibility, not the done condition. A repeated receipt for the same task/attempt adds no new completion; a late result from a superseded attempt does not regain ownership. Check its relevance before using it.

A worker failure blocks its dependents, not unrelated work. Reopen only the affected task and descendants whose evidence the repair invalidates. After compaction or restart, reconcile the register with artifacts and current worker status; do not replay completed tasks or assume old handles survived.

## Progress and Completion

Use task-appropriate deadlines and observable progress for liveness decisions. Inspect available artifacts/status and pending work before interrupting; stop the former writer and outstanding mutations before reassignment, or isolate the new outputs. Do not count two quiet waits as proof of failure or free capacity.

Review result summaries and resolve actual integration conflicts. Run the focused integration evidence required by the acceptance contract or a concrete unresolved risk; there is no default full-suite or broad-review gate. Completion means the requested outputs and required checks are satisfied, not that a wave has returned.

Official guidance: [Codex subagents](https://developers.openai.com/codex/subagents) describes native orchestration, context isolation, shared work risks, and configurable agent settings. The active tool contract takes precedence for callable capabilities. UNVERIFIED without an actual probe: automatic slot reclamation on this surface, indefinite reuse without context cost, and identical CLI/IDE lifecycle behavior.
