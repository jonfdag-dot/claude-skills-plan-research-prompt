# Native communication and lifecycle

Use the tools actually present in the active Claude session. Distinguish a permission request, an assignment, a status report, acceptance and a shutdown request; one does not imply another. A worker cannot approve itself or expand its assignment.

Give each task an accountable owner and exact output contract. Messages carry only new decisions, evidence or missing context. Follow up on unfinished work at most twice, then revise the assignment or name the blocker. Do not infer failure from silence without checking live task state and known pending tools.

Before transferring write ownership, confirm the earlier worker and mutating commands have stopped or isolate the successor's outputs. Serialize conflicting files, shared Git operations and external state. Preserve other workers' changes and active shared resources.

Use a native leaf subagent for a bounded task. Agent Teams, messaging integrations, worktrees and custom controllers are optional capabilities that require their own actual availability and authorization; this starter does not configure them. A policy instruction to remain a leaf is not a runtime permission guarantee.

The parent integrates returned evidence and records completed and pending work before ending the task. A handoff or a worker's end-of-turn message is not acceptance of the whole requested outcome.
