# Wording Context and Session Handoffs

Use this reference when the requested prompt must remain usable after compaction, a session boundary, or an ownership transfer. SDD's [long-form-planning.md](../../subagent-driven-development/references/long-form-planning.md) owns long-run design; [evidence-handoff.md](../../subagent-driven-development/references/evidence-handoff.md) owns durable state, artifact identity, recovery, limits, and acceptance. This reference words that existing contract rather than adding a second ledger or harness.

## Preserve the necessary facts

Preserve the fields the task actually uses: current objective, accepted amendments, scope, decisions, relevant evidence, remaining work and next action. Carry authority pointers, task/attempt/owner, artifact identities, process state and consumed limits when the supplied workflow requires them. This is a selection guide, not a mandatory handoff schema.

Use exact source and evidence pointers for large material. Keep undiscoverable corrections and constraints inline. A short summary that loses a required invariant is incomplete; a full transcript is usually unnecessary. Native compaction and a context window do not guarantee durable or lossless state.

## Word a resume instruction

```text
Read the current accepted task record and its evidence. Reconcile newer user corrections and relevant changes since that record. Check artifact versions, ownership/process state or unresolved effects when the supplied workflow uses them. Preserve valid completed work and its checks. Resume only pending or invalidated requirements; do not replay an uncertain external mutation or accept a stale attempt from the summary alone.
```

The prompt should point to the existing record, not prescribe a new JSON feature list, notes file, bootstrap script, branch, or commit per session. Require persistence only where the requested work or host already requires it.

For an implementation resume, name the next bounded behavior or artifact and its acceptance condition. Include producer/consumer dependencies and existing status updates when the workflow uses them. Carry operational approvals and runtime execution limits only where the accepted record, applicable governing instructions or host states them; do not invent new gates from the handoff format.

## Word a handoff

```text
Summarize the current objective and scope, accepted decisions, completed work and its deciding evidence, remaining requirements and the next authorized action. Include task/attempt/owner, artifact identities, processes, external effects and consumed limits when the supplied workflow uses those fields. A worker handoff distinguishes its result from parent acceptance and whole-task completion.
```

For an SDD assignment, use its supplied receipt fields in the existing task artifact. A read-only worker returns the report for root persistence. A commit alone does not identify dirty output, and a path or confident summary does not establish acceptance.

## Avoid universal reset and gate rules

Do not require a written spec or separate explorer/builder context for every implementation. An unchanged ready assignment may already have a sufficient accepted contract. Ask for a bounded exploration only when an unknown prevents correct dependent work.

Do not clear useful context, discard implementation, or reset failed-correction counts because a session ended. The root chooses a fresh or resumed worker under SDD; the prompt carries the selected constraints. Required checks and review remain tied to acceptance or a concrete unresolved risk, without an automatic end-to-end panel for each session.

Historical harness accounts in [sources-and-contradictions.md](sources-and-contradictions.md) describe particular models and workloads, including differing reset and verification practices. They motivate attention to durable state, not a guarantee that one file format, session size, commit cadence, or reset policy is optimal. Native controls own enforcement; instruction text cannot create locks, permissions, or unattended continuation.
