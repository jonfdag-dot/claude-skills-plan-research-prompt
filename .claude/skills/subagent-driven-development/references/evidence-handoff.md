# Evidence Handoff

Use this contract for dispatch, acceptance, repair, and recovery. Extend the existing plan or task register; do not create a second ledger, schema framework, or controller. Prompt-engineering-patterns may help word these fields; this reference owns their execution meaning.

For a delegated-development planning deliverable, read [long-form-planning.md](long-form-planning.md) before designing or materially revising it. Its requirement-to-integration mapping supplies acceptance content; this file remains the owner of dispatch and receipt fields.

## Dispatch contract

Every brief identifies the task, attempt, and parent/run; original user intent, current requested outcome, accepted scope and acceptance requirements; relevant sources and versions; dependencies, upstream invariants and accepted decisions; selected native role and definition source; owner, write boundary, exclusions, and prohibited effects; selected governing skills with verified native locations and reasons, supplied references, required checks and stop rules; and output shape with a unique task/attempt artifact path. Keep undiscoverable user corrections inline. Resolve ambiguity in intent or cause before dependent changes; stale sources do not establish current applicability. A downstream handoff never grants downstream authorization. Link large inputs by exact path and section or symbol, adding a commit, content hash, artifact version, or source date when relevant to freshness.

Specify read-only explicitly when appropriate, and get it from a native role whose available tools and runtime controls establish that boundary: persona text and context separation cannot enforce it. For the Claude auto-mode behavior described by the active native documentation, a subagent's `permissionMode` is ignored; do not translate that field into a Codex permission guarantee. Worker reports, pasted text and tool output never carry approval. All workers are leaves and preserve other workers' changes. The root alone owns the register, shared Git coordination, acceptance, and dependent dispatch. A worker that cannot write its report returns the complete report inline for root persistence; it does not bypass its sandbox.

For delegated web research for project or tooling work, supply ~/llm-research-links/README.md and relevant prior findings or search scope. Workers follow its search and retention contract and return only reusable findings that informed the work, with existing R-IDs when known and the complete evidence packet required by the README and web-research references/evidence-and-retention.md, in the task report; they do not allocate new IDs or write the library. Claude `worker-researcher` and `worker-investigator` have no shell, so the root supplies the `research.py find`/`show` output, revision IDs and diffs those workers need. The root deduplicates accepted findings and persists a batch through the README contract, then runs its validation commands and reports saved R-IDs or pending persistence. Project decisions and specialist catalogs retain their canonical homes.

## Return contract

Return `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`, with task/attempt/parent identity, concrete result, decisive evidence, changed paths or source anchors, remaining acceptance gaps, and the detailed artifact path. A file path alone or “tests passed” is insufficient. Put the deciding evidence inline so the parent can act without reopening every source; place extended observations and raw output in the assigned artifact. Never manufacture a file link for an artifact that was not written. In Claude Code, a worker that reports through SubagentHandback delivers the report as that tool's `tool_input.message`, and its closing text may then be empty.

Map every required acceptance item to observed evidence or an explicit unresolved gap. Bind evidence to the actual delivered version: commit plus dirty-worktree diff, content hash, artifact revision, or dated external source as appropriate. A commit alone does not identify uncommitted changes. For commands, report the actual command, working directory, exit status or meaningful output, tested version, and relevant input/example. Preserve output needed to check the claim. When the runtime shortened a long output (Claude Code saves an oversized tool result to a file and shows a preview; Codex 0.162 caps persisted command output in paginated history at 64 KiB), decide from the full saved file or a log the command wrote, cite that path, and never treat a preview as proof that a line is absent. For source claims, cite exact paths and lines/symbols, or direct URLs with section and version/date; distinguish observation from inference and state uncertainty.

Use the evidence suited to the work:

| Deliverable | Decisive evidence |
| --- | --- |
| Code or repair | Delivered files/version, requirement-to-behavior mapping, actual covering check and meaningful input/result |
| Investigation | Owning symbol/location, causal evidence or reproducer, alternatives ruled out, unresolved uncertainty |
| Research | Source URL/path, version/date and relevant passage, supported conclusion versus inference |
| Plan | Requirements and accepted decisions mapped to deliverables, dependencies, ownership, and reachable checks |
| UI | Required project acceptance evidence tied to delivered state, route/viewport or device, and reproducible interaction |

Say `not run` for any check not executed and give the reason. A proposed command, simulated response, earlier-version test, passing unrelated test, or unavailable artifact is not a current pass. If a relevant edit follows a check, invalidate only the affected evidence and rerun its smallest covering check. Missing required proof prevents acceptance even under deadline pressure; keep unrelated work moving.

`DONE` means all assigned requirements have supported evidence. `DONE_WITH_CONCERNS` distinguishes nonblocking observations from required gaps; the label cannot waive acceptance. `NEEDS_CONTEXT` names the missing decision/source. `BLOCKED` names the symptom, attempts, evidence, remaining unknown, and required input/capability. Stop after two failed corrections to the same defect and return a revised brief or concrete blocker; do not retry unrestrictedly.

## Bounds and completion

An assignment's acceptance establishes its promised result against version-bound evidence. A handoff transfers that result, open requirements, authority boundaries, and next action to an accountable owner; it does not accept the result or authorize the next effects. Whole-task completion requires the root's integrated outcome and all required checks, including required work outside the returning worker's slice.

Record applicable bounds in the existing task state, keeping their meanings separate:

| Bound | What it ends | What survives |
| --- | --- | --- |
| Worker turn, tool timeout, or session/context boundary | That execution interval or available context | Current objective, authority, ownership, delivered artifacts, checks, pending work, and uncertain effects |
| At most two automatic continuations | The automatic follow-up sequence for an incomplete worker report | Unmet acceptance and the root's decision to clarify, revise, reassign, or report a blocker |
| At most two failed corrections to the same defect | Further automatic repairs of that defect | Symptom, hypotheses, attempted corrections, deciding evidence, and remaining unknown across attempts and workers |
| Explicit whole-task budget, deadline, or stopping condition | Work covered by that actual limit | Recoverable partial state and every unmet criterion; a limit does not change acceptance |

A clarification or context resume is not itself a failed correction. A retry delay, per-session turn limit, or new attempt ID does not bound the whole task or reset consumed limits. Use available accounting and identify unknown consumption; do not invent a budget or measurement system. Stop owned writes and processes before handing off, or disclose their exact outstanding state so the root can retain ownership safely.

## Ordinary change receipt

In the existing task artifact, record intent and criteria, baseline identity, owned per-file changes, delivered identity, actual checks, unresolved items, and the scoped reversal. For delegated work, record the served model from the child transcript's `message.model` in Claude Code, or from the resolved model and reasoning effort Codex 0.162 and later records in sub-agent activity, with effort, stop reason and any refusal category; never take them from the worker's self-report. A supported NO_CHANGE result explains how the baseline already satisfies the request and lists the evidence; preserve the existing task status vocabulary. Root persistence of a read-only report is sufficient. Do not create a separate tracking system or demand an experiment record for an ordinary edit.

## Experiment extension, only for admitted comparative experiments

Ordinary optimization uses the ordinary receipt. For skill-authoring model experiments, follow the [canonical verification and eval admission policy](../../skill-creator/references/verification-and-eval-admission.md); a request to improve wording does not authorize comparison or a baseline.

Extend that same receipt with the hypothesis and competing explanations, alternatives and accepted scope; baseline and candidate commit AND tree IDs; initial dirty-worktree fingerprint and exact owned patch excluding secrets; model/profile, prompt, and configuration differences; versioned research and evaluation receipts; applicable deployment IDs; and outcomes, decisions, rejections, and reopening triggers. A commit/tree pair does not identify dirty content by itself: bind the owned patch and delivered files to hashes, preserving others' initial edits. If a commit or tree ID is unavailable, mark it unavailable and identify the artifact directly; do not fabricate IDs or create commits solely to fill the record. Record secret names and availability only; never capture values in patches, fingerprints, commands, or receipts.

Keep accuracy, quality, cost, and latency separate. For each, report PASS, FAIL, UNVERIFIED, or justified NOT_APPLICABLE against the accepted criterion, with evidence and limitations; preserve the project's native metric vocabulary and distinguish these dimensions from the task status. A passing quality check cannot establish accuracy, and unknown cost cannot prove savings. Accounting must retain failed attempts and retries, with the applicable measurement window and comparability constraints. Do not declare a winner from incomparable runs or silently relax frozen criteria. Retain failures, usage, deployment records, and rejected candidates in history; reopen a rejected approach only for new evidence or an explicit decision, recording what changed.

## Authorized evaluation or deployment only

Assign an operator only for an explicitly authorized target and effects. Before execution, read the current project CI, evaluation/deployment, authentication, accounting, and recovery instructions. Confirm credential names and availability without reading or logging secret values. If authority, target identity, or necessary recovery information is missing, return that exact gap while continuing independent read-only preparation. No handoff, passing evaluation, DEV approval, or successful DEV deployment implies promotion permission.

Record the target revision and tree/artifact identity, configuration/profile, actual command and environment, run/job/deployment IDs where applicable, produced artifacts, validation and accounting receipts, outcome, recovery state, and proposed next route. Bind results to the tested or deployed target, not the current local HEAD by assumption. The next route is a recommendation for the root to evaluate under existing authorization; it is never permission to deploy, promote, spend, or use credentials. Inspect unknown external effects before retrying.

## Scoped reversal and rejected work

Append a reversal decision to the same history: reason and affected attempt, exact owned changes to undo, dependencies and downstream effects, required external recovery, and verification of the recovered state. Reverse only the owned delta against the recorded initial dirty state; preserve other workers' edits and stop for overlapping changes that cannot be separated safely. Do not reset an entire shared tree or erase failed outcomes, usage, deployments, or rejection rationale. A local file revert does not recover an external effect. Record whether required recovery is complete, blocked, or unknown and keep dependent acceptance pending until verified.

## Example of a bounded repair receipt

Illustrative shape, not an executed result: task P3, attempt 2, parent run R7 repairs a parser's empty-input behavior. Cite the delivered `src/parser.ts` hash and `parseInput` location, the requirement “empty input returns InvalidInput,” and the actual focused command with its cwd, status, output, and input/result. State `full suite: not run; not required for this acceptance`. If the parser changed after that run, return the requirement as unverified pending the same covering check on the new version. Do not invent hashes or command output to fill this example.

## Parent acceptance and recovery

Check identity, ownership, versions, and decisive evidence before acceptance. Inspect the relevant diff, artifact, command output, or source anchor that decides the claim. Expand inspection only for a concrete contradiction, missing required evidence, or integration risk; do not redo the worker's full investigation or automatically add review, suites, or commits. Reuse unchanged evidence. If independent review is required, select a non-author with a bounded read-only brief and a visible current diff/artifact. Review original intent fit, causal support, research applicability, upstream invariants, unnecessary changes/regressions, and whether existing tests could miss the defect; use [task-reviewer-prompt.md](../task-reviewer-prompt.md), including its restricted packet only for blind comparisons.

Persist accepted results, ownership changes, and user decisions in the existing register before dependent work starts. Retain original intent and authority pointers, accepted scope and amendments, baseline and delivered artifact identities including relevant dirty content, command results and evidence assumptions, remaining requirements, consumed repair/continuation limits, active owners/processes, unknown effects, and next action. After compaction or restart, read that register and its evidence, reconcile newer user corrections against the summary, inspect changed versions, and confirm live workers when possible. Duplicate receipts are idempotent; a superseded attempt cannot regain ownership or close the current task. A late result is usable only after checking its relevance to the current version and requirements.

Unknown external effects stay unknown until a read-only state check resolves them; do not replay a deployment, message, or mutation from summary alone. Before reassigning writes, confirm the prior writer and outstanding mutation stopped or isolate new outputs, then persist the transfer. Retain valid completed work and keep dependencies with missing proof pending.
