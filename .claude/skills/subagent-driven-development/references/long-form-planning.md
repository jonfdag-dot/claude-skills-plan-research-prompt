# Planning Long-Running Delegated Development

## When this reference applies

Read this reference before designing, decomposing, or materially revising a plan for delegated development, even when no worker will run yet. Reuse a complete copy already in the current context. Apply the requirements proportionately: a small delegated change may need only a short acceptance contract; a long, uncertain, cross-boundary build needs explicit staging and recovery. Do not manufacture long-run machinery for a small task.

This file owns planning design. [plan-orchestrator.md](plan-orchestrator.md) owns execution of a written plan; [evidence-handoff.md](evidence-handoff.md) owns dispatch, receipts, acceptance, and recovery fields; [native-role-routing.md](native-role-routing.md) owns worker selection. Keep those contracts canonical rather than copying their schemas into a new manifest. An implementer of an unchanged ready task consumes its relevant plan slice, not this whole reference.

The requirements below are adopted workflow policy, not claims that a public experiment proved this exact process optimal. The evidence appendix distinguishes documented capability, vendor experience, research, and proposed practice. A skill guides behavior; only the runtime can enforce permissions, isolation, or continuation.

## 1. Preserve intent and authority

Start from the original objective and current agreed outcome. Identify the authoritative requirements, accepted amendments, settled decisions, invariants, explicit non-goals, relevant baseline, and observable completion. Resolve conflicts by the owning project's authority rules, not by whichever document was read last. Verify implementation claims against current artifacts; a completed design document does not prove built behavior.

Distinguish the user's product scope from a worker's ownership boundary. The coordinator can redistribute already-authorized work but cannot widen the product, approve reserved operations, or treat a downstream recommendation as permission. Record material amendments with their source, affected requirements, and what remains unchanged. Preserve rejected alternatives and their reopening conditions when forgetting them would cause repeated work.

Clarify only an unresolved choice that changes requirements, architecture, data, authority, interfaces, or acceptance. Discover facts from the relevant source first. Turn unknown implementation details into bounded exploration with a question, owner, expected evidence, and exit condition; do not guess a detailed design to make the plan look complete. Independent ready work can continue.

## 2. Connect requirements to the integrated result

For each requirement, identify its observable behavior, producing task, affected interface and consumers, necessary evidence, and integration milestone. Reuse existing IDs and formats. Every planned patch must serve an accepted requirement or a necessary dependency. A helper, abstraction, test suite, report, or migration without that connection is not automatically in scope.

Use a compact mapping where several requirements or consumers would otherwise become ambiguous:

| Requirement | Producer and contract | Consumer or integration boundary | Acceptance evidence | Remaining prerequisite |
| --- | --- | --- | --- | --- |
| Existing requirement ID and behavior | Owning task; input → output → failure/denial | Actual consumer; preserved invariant | Check or journey; expected result; tested artifact/environment | Owner; artifact/decision; point of need |

This is a content guide, not a required file or data format. Small changes can express the same connection in prose. Do not duplicate the full requirement text across every task: retain canonical intent and carry the applicable criteria into briefs.

At each acceptance boundary, compare the delivered behavior with the original intent plus accepted amendments. Classify a discrepancy as missing, partial, contradictory, or unrequested; identify whether the implementation or a stale plan is wrong. A plan is not authority to preserve a known mistake, but correction must retain scope and explicit decision ownership.

## 3. Specify contracts before guessed internals

Describe inputs → outputs → failure or denial behavior before implementation. Include applicable types, validation boundaries, state transitions, ownership, compatibility constraints, and invariants. Make semantic obligations explicit: field shape alone does not establish authorization, ordering, units, identity, replay safety, or correctness.

For every shared boundary, name the producer, consumer, source of truth, and what changes require consumer revalidation. Specify relevant negative behavior where the contract demands it. For generators, include an expectation independent of generated output so the same mistake cannot make implementation and tests agree.

Describe only internals necessary for correct integration or a binding constraint. Let the implementer choose ordinary local technique. If a required interface is still unknown, finish the necessary exploration before dependent code rather than inventing signatures, file paths, commands, or runtime capabilities.

Separate these proof levels when relevant:

- Shape or static contract proof establishes the declared interface.
- Fixture proof establishes behavior for controlled inputs and stated assumptions.
- Real-producer integration establishes that actual components work together.
- Operational or host proof establishes behavior in the required environment.
- Release acceptance establishes the complete promised outcome.

A passing lower level never silently substitutes for a required higher level.

## 4. Establish readiness, not merely a valid dependency graph

A task is dispatchable only when its required inputs and accepted dependencies exist, ownership is clear, necessary decisions are resolved, relevant resources are available, effects are authorized, and its acceptance checks are reachable. Graph readiness alone is insufficient.

Inspect semantic dependencies as well as declared edges: where does a required fixture, instruction, schema, identity, generated artifact, or test command come from? Do not schedule a check before its producer exists. If a task references a later producer that depends on it, separate early interface/fixture proof from later real integration; do not add a reverse edge that creates a cycle or declare the full requirement complete.

Plan ownership over files and shared resources. Include applicable generated outputs, lockfiles, migration order, CI configuration, databases, ports, accounts, and external state. Separate checkouts do not isolate shared services. A promised CI gate needs an authorized owner of the CI changes; a local command pass is not CI wiring.

Classify prerequisites by point of need:

| Timing | Planning obligation |
| --- | --- |
| Before starting the selected slice | Resolve the input, toolchain, authority, or decision that prevents any meaningful accepted work. |
| Before a named later stage | Identify owner, required artifact or approval, latest point of need, and dependent work; proceed with unrelated ready work. |
| Not required for this scope | Omit it from execution rather than creating optional setup work. |

For substantial runs, consider applicable accounts, access, fixtures, environments, supplier choices, schema evidence, deployment targets, recovery mechanisms, and budget boundaries. Record availability and secret names only, never values. “Founder will handle setup” is insufficient: name the concrete decision or artifact and when it blocks.

Prearranged access is not approval to mutate. Exact-operation approvals required by the project remain at their actual boundary; unknown future SQL or releases cannot acquire authority from a generic “autonomous install” instruction.

## 5. Stage connected increments and assign integration

Choose stages by connected behavior and risk, not line count, arbitrary packet count, numeric prefixes, or the number of available agents. Each stage names a useful result, required dependency closure, accepted inputs, producer/consumer boundary, necessary proof, and remaining full-deliverable criteria.

Keep one accountable integration owner and one accepted state. Candidate work may be in flight, but accepted artifacts and their evidence must remain identifiable and recoverable. Record candidate versus integrated evidence distinctly. Where outputs meet, run the check that establishes the changed combined behavior; isolated worker success cannot close that boundary.

Dispatch parallel work only when accepted inputs, write/resource ownership, and integration capacity permit it. Do not impose a permanent reviewer/integrator tier or a universal worker count. Required project reviewers remain binding; additional review needs a concrete unresolved correctness risk.

A stage may close a proven subset while its containing deliverable remains incomplete. Keep required blocked work visible rather than redefining release around what passed. If the remaining scope exceeds budget or available authority, present the exact gap for a user decision. A scheduler or worker cannot silently downgrade the target.

## 6. Resolve decisions at the right boundary

Distinguish decisions reserved to the user from reversible technical choices delegated within accepted scope. Use a founder-designated reasoning role only when a consequential ambiguity, conflicting evidence, architecture tradeoff, or failed-repair escalation needs it; do not add an approval loop around routine commands.

A decision brief contains the question, credible alternatives, constraints, relevant evidence, downstream effects, and the authority boundary. Its return contains the recommendation, concise rationale, contrary evidence or uncertainty, and scope impact—not a private reasoning transcript. Record the accepted decision before dependent work.

An agent may prepare a supplier comparison, migration approval package, or release recommendation. It cannot approve its own reserved operation, buy access, expand the product, or infer production authority from a staging success. Batch concrete decision packages when helpful, without inventing permission or blocking unrelated work.

## 7. Plan context and durable state together

The coordinator retains the current objective, authority pointers, accepted state, active ownership, dependency view, unresolved decisions, and next actions. Each worker receives the smallest sufficient contract slice: task/attempt identity, outcome, applicable criteria, relevant source and tests, accepted dependency facts, allowed files/resources, exclusions, necessary checks, and return/stop conditions. Use the existing [implementer prompt](../implementer-prompt.md) and handoff contract.

Link large sources by relevant section or symbol with a freshness identifier where needed. Keep undiscoverable corrections and critical constraints explicit in the brief. Do not send an entire plan inventory, research corpus, raw logs, or accumulated conversation merely because they are available. Context selection must preserve the transitive contract facts needed for this task, not only its immediate file list.

Keep coherent clarification and repair with the same worker when useful; use fresh context for independent work and non-author review. Do not mandate resets at a token percentage, after every packet, or after a fixed number of turns. A context window is not durable project state, and a summary is not proof that all constraints survived.

Use the existing plan or task register as the durable record. Persist meaningful transitions before dependent dispatch: accepted results, decisions, failed attempts, ownership changes, blocked prerequisites, and uncertain effects. Do not require a diary after every tool call, an automatic commit for every task, or another ledger.

Ensure recovery can locate the current authorized objective; actual accepted and candidate artifacts, including relevant dirty changes; criterion-bound evidence and environment assumptions; unresolved criteria; active attempts and resource/process ownership; failed-correction counts; unknown effects; and next action. Use the fields owned by [evidence-handoff.md](evidence-handoff.md), not a competing schema.

On resume, reconcile this record against newer user corrections, current artifacts, and supported worker/process status. Reject superseded closure; confirm or isolate the old writer before transferring ownership. Inspect uncertain external effects read-only before replay. An interrupted response does not prove an operation never happened.

## 8. Budget work without inventing model economics

Preserve the user's root model and native worker definitions. Required specialists win over a generic cheaper role. Delegation can reduce parent-context load but still consumes worker and coordination tokens; a role name is not a price tier. This reference does not authorize model changes or promote an experimental worker.

Plan bounded reasoning at unresolved high-impact decisions, deterministic tooling for applicable mechanical checks, and small relevant worker contexts. Avoid duplicated exploration and raw-output retransmission. Stable reusable instructions can help where caching is supported, but caching does not remove material from the context window or guarantee attention.

When cost optimization is explicitly authorized, agree on representative work, unchanged acceptance, comparison conditions, and the stopping boundary before judging candidates. Count coordination, reviews, failed attempts, repairs, and integrated acceptance—not only generation price. Use existing accounting; unknown consumption stays unknown. Do not build telemetry merely to support an efficiency claim.

For a budgeted long run, record the actual available allowance or user ceiling when accessible, limits on new work, and how to leave recoverable in-flight state. Never infer a weekly completion guarantee from API prices, a model's advertised window, a dependency graph, or one successful pilot. A real budget limit does not waive completion criteria.

## 9. Bound verification and stop at the requested outcome

For each criterion, name the smallest sufficient check or observable journey and expected result, plus binding project gates. Use actual available commands and state what creates any later check. Identify relevant environment and artifact assumptions. Choose negative, authorization, failure, and recovery cases from the actual contract; do not append an exhaustive generic checklist to every task.

Evidence remains valid only for the behavior, artifacts, dependencies, and environment assumptions it covers. A later relevant change reopens the affected criterion and consumers, not every prior test. Compaction or a new worker alone does not invalidate evidence. For delegated-plan resume, reconcile validity first; interpret generic “rerun checks” guidance through this scoped rule rather than automatically repeating unchanged proof.

A decisive pass closes the unchanged criterion. A verification-only assignment reports a decisive failure without implementing. An authorized implementation assignment may repair within scope, then rerun failed and affected checks. Keep the existing two-failed-corrections limit across reassignment and compaction; a fresh attempt is not a reset of defect history. Do not probe equivalent configurations to avoid recording failure.

At the end, light testing is earned by accumulated valid evidence. Retain required final integration, clean-install, host, or release checks where the promised behavior demands them. A build or screenshot does not certify access control, billing, data safety, or real host behavior. Publication and deployment remain separate authorized effects.

When required checks pass and the delivered result matches intent, stop. Optional hardening, stylistic preferences, hypothetical risks, additional confidence, or an unrelated warning do not create more work. Add a check only when its result could change acceptance or the next authorized action.

## 10. Compact plan scaffold

Use the owning project's existing plan format and lifecycle. Cover these questions in that format without requiring a separate file per row:

| Plan section | Required answers |
| --- | --- |
| Outcome and boundaries | What must become true? Which source and amendments govern? What must not change or be added? |
| Current evidence and unknowns | What exists at the relevant baseline? What must be discovered or decided before dependent implementation? |
| Contracts and requirement map | Which producers/consumers, types, transitions, invariants, and failure behaviors connect each requirement to proof? |
| Stages and ready tasks | Which connected increments, dependencies, owners, resources, and prerequisite artifacts make dispatch possible? |
| Integration and acceptance | Who accepts the combined result? Which exact checks prove which criteria, and what remains pending? |
| Continuity and limits | Where do decisions and receipts live? How are stale attempts, unknown effects, repairs, budget limits, and user approvals handled? |
| Completion | What closes the full outcome, what cannot be claimed yet, and when must work stop? |

Before handing off, check for orphan requirements, unrequested tasks, unavailable producers/checks, ownership conflicts, unresolved decisions disguised as assumptions, unsupported completion claims, and duplicated state. A plan can truthfully contain bounded discovery or a blocked future stage; it cannot present undecided dependent implementation as dispatch-ready.

## 11. Worked example: producer → API → UI

Illustrative planning example, not an executed build. The approved outcome is to display an authorized catalog entry in an existing UI. Contract task A owns the catalog schema and its existing contract test; producer B depends on A; API task C consumes B; UI task D consumes C. Each task retains the project's actual file names and commands discovered during planning.

A's proposed acceptance says “return the instructions supplied by B,” but B cannot exist before A. Plan A to establish the instruction field and byte-preserving pass-through using an explicit fixture. Keep the real B → C instruction check pending at the integration stage; do not add B as A's prerequisite or claim fixture success proves real producer behavior. If early CI wiring is promised but only a later task owns its configuration, resolve the ownership or retain CI acceptance as pending before dispatch.

Specify B's typed success/failure result, C's authorized input/output and denial behavior, and D's render/error behavior. Map the complete user outcome to the actual B → C → D journey. Local contract checks, API denial checks, and UI behavior each establish their own criteria; the final journey establishes the connected result. A missing required host account blocks that host proof, not independent local work, and the release remains incomplete.

After A and B are accepted, D changes. Its earlier render evidence is stale; rerun the affected UI and connected journey checks. Reuse A/B evidence if their artifacts and assumptions are unchanged. Persist the accepted D result and remaining host criterion before releasing dependent work.

If the coordinator then compacts and an old D attempt reports success, compare attempt identity and delivered bytes before acceptance. If publication was interrupted, inspect external state before retrying. Reconstruct from the existing register and receipts; do not rebuild the plan, reset repair history, or reread all research. Completion requires the still-promised host proof or an explicit user amendment—not a persuasive summary.

## Evidence and applicability

Evidence reviewed in the retained research synthesis on 2026-09-20. These public sources support specific concerns; none proves this whole workflow optimal or guarantees an autonomous large build within a subscription allowance. Several reports deriving from the same originals are one synthesis lineage, not independent experimental replications.

| Source and evidence class | Supported lesson | Limit |
| --- | --- | --- |
| [Anthropic: effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), 2025-11-26; vendor experience | Incremental work, durable progress, and application-level checks addressed observed long-run failures. | Not an optimal worker count or lossless-compaction guarantee. |
| [Anthropic: harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps), 2026-03-24; vendor experience | Later model/workload changes made some forced resets and repeated sprint evaluation unnecessary. | Remaining evaluation still mattered; confounded comparisons do not establish universal cost savings. |
| [Cursor: scaling agents](https://cursor.com/blog/scaling-agents), 2026-01-14; vendor experience | Coordination and integration design can become bottlenecks at scale. | A large-token experiment does not establish economical team size or weekly-budget feasibility. |
| [OpenAI: Codex best practices](https://learn.chatgpt.com/guides/best-practices); documented guidance, checked 2026-09-20 | Keep coherent work together and offload bounded work rather than using one conversation for an entire project. | Not an empirical reset threshold or guarantee of this account's runtime capabilities. |
| [MAST v3](https://arxiv.org/html/2503.13657v3); research | Identifies specification, coordination, and verification/termination failure categories in studied multi-agent systems. | Different systems and models; not a causal validation of this skill or an Astra benchmark. |

Intent traceability, readiness gates, affected-evidence reuse, and bounded verification are adopted process choices informed by these concerns and the owner's requirements. Exact approval rules and repair limits are owner/project policy. Model routing, concurrency, resets, and additional orchestration remain workload-dependent; validate any proposed change against the actual task without relaxing acceptance. Public evidence remains evidence, never authorization.
