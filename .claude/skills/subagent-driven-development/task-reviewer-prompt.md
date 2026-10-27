# Task Reviewer Prompt Template

Use when an independent review is requested, required by a binding gate, or justified by a concrete unresolved risk. Review supports the deliverable; it is not an automatic stage for every task.

```text
Task: <global task ID, attempt ID, parent/run ID, and deliverable>
Role: <native specialist or investigator and definition source; never the author; differs from the author in context or rubric, and in model where one is available>
Review reason: <requested review, binding gate, or concrete risk>
Acceptance: <original user intent and the user's stated requirements (not requirements a worker wrote), current outcome, frozen requirements, accepted scope and upstream invariants>
Skills: <applicable review skills with verified native locations and reasons; supplied references>
Inputs: <brief, delivered version, relevant diff or artifact paths, existing evidence; omit who wrote the work and the author's persuasive reasoning>
Changed scope: <exact files/range or planning/research sections>
Review boundary: read-only; no Git or external state mutations
Return: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED; acceptance verdict, evidenced findings, version-bound checks actually performed, explicit not-run checks, unresolved required evidence; decisive evidence inline plus root-persisted detailed report.
```

Compare the result with the stated requirements using [evidence-handoff.md](references/evidence-handoff.md). Verify decisive claims against relevant artifacts; reuse valid check results for unchanged work. Read surrounding context when needed to judge a specific issue, without crawling unrelated files. First confirm that the supplied diff or artifact is visible, complete for the assigned change, and tied to the current delivered revision. A missing, inaccessible, or stale package means required evidence missing, not approval. A committed diff does not represent uncommitted work; use the actual delivered artifact. All workers are leaves; do not delegate.

Report a finding only for an acceptance violation supported by evidence, or a critical safety/corruption defect with a reproducible case. Name the requirement, exact location, observed failure, and smallest reproducing check. Severity follows consequence, not preference. Broad architecture wishes, style, unrelated warnings, and speculative robustness do not add requirements.

For code, judge requested behavior against original intent, causal support for the fix, upstream invariants, unnecessary changes, and regressions. Ask whether passing tests could miss the reported defect and name the smallest discriminating input when they could. For plans, judge dependency and decision consistency; for research, check source freshness, version applicability, support, and uncertainty. Do not substitute an elegant implementation for the requested outcome. If required evidence is missing, identify exactly what is missing and whether supplied evidence can resolve it. Do not turn every limitation of a diff into a new gate.

Run a focused check only when a concrete doubt is not answered by existing evidence. Do not automatically repeat suites, commission more reviewers, or reopen closed findings. A follow-up review covers only the cited finding and changed requirements unless new evidence invalidates an earlier closure. After two failed corrections to the same defect, return the unresolved requirement and evidence to the root; do not trigger a third repair cycle.

Return a compact verdict: compliant, acceptance defects found, or required evidence missing. Each finding includes evidence and a reproducer; if none qualify, say so. No mandatory strengths section, Minor backlog, or separate aesthetic approval.

## Blind comparison only

When blind judging is required, replace the ordinary review inputs with an anonymous output packet and frozen rubric only. The root keeps the candidate-to-packet identity map outside the judge's inputs. Exclude candidate labels or identity, model/profile, cost and latency, author rationale, prior verdicts, and any repository access or context that could reveal them. Use the required project reviewer when its native boundary supports this restriction; otherwise the root selects an available independent reviewer with read-only tools, with only those restricted inputs, provided project rules permit that fallback. Never substitute the author or evade a mandatory specialist. If the available runtime cannot restrict the boundary, report the assessment as unblinded and leave any required blind gate unmet. Ordinary artifact/code review remains separate from this anonymous quality judgment.
