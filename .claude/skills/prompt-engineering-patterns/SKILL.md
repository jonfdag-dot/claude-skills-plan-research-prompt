---
name: prompt-engineering-patterns
description: Writes and diagnoses model prompts, reusable templates, system prompts, and execution briefs while preserving scope, inputs, authority, and acceptance. Use when the deliverable is prompt text, a prompt-behavior diagnosis, examples or structured-output guidance, or the wording of a worker dispatch or session handoff. Not for executing the described task or selecting agent topology/stopping → use subagent-driven-development; skill instructions/descriptions → use writing-skills; skill or agent lifecycle/registration → use skill-creator; application output-quality measurement → use llm-evaluation; model/API policy → use the relevant provider integration skill.
---

# Prompt Engineering Patterns

Writes the smallest complete prompt, template, system prompt, or execution brief for a requested deliverable. Two lanes share this skill: the prompt a model receives in one call, and the brief an agent or a later session executes without you.

This skill authors prompts. Executing one needs a separate request, and this skill cannot grant tools, access, or approvals the host has not given.

Evidence tags: [DOC] is documented guidance scoped to its source and target model in `references/sources-and-contradictions.md`, not a measured improvement for this skill. [POLICY] is an explicit local authoring convention, never cited as a vendor claim. Unsupported technique claims do not become instructions; report them as unestablished.

## The primary rule

Do not add work merely because it could improve the result. A prompt may clarify scope, but it must not create scope. [POLICY]

- A request to implement does not gain competitive research.
- A request for research does not gain implementation.
- A surgical change does not gain an architecture review.
- A request for a prompt does not include executing it.
- A supplied plan's settled decisions are not reopened unless they prevent execution.

Research, discovery, planning, delegation, persistence, testing, repository operations, deployment, and verification are conditional capabilities, never implied steps. Include one only when the requested deliverable depends on it.

## Grounds for an instruction

Keep a constraint, check, approval, stop, review, budget, rollback, status code, failure branch or caution only when it preserves a stated requirement or applicable governing instruction, or is necessary to make the requested result correct. Do not invent permissions, approval workflows, operational bans or extra deliverables from hypothetical risk. A document's presence does not make every sentence in it an instruction. [POLICY] Current provider guidance supports task-relevant boundaries and proportionate checks; it does not establish a universal ban on task-implied checks. [DOC]

When revising a prompt, remove a category the user asked to remove throughout the artifact; do not recreate it as a renamed prohibition, halt, review or final-report requirement. A prompt rewrite cannot remove an independently applicable host restriction; explain an actual conflict outside the artifact. [POLICY]

## Workflow

1. Understand the requested deliverable using the context already available.
2. Ask focused questions only when missing information materially changes the result. Group related questions when useful and keep only dependent work pending; otherwise write the prompt. Do not insert a separate approval step. [POLICY]
3. Research only when the prompt depends on a fact that is unknown, current, or disputed.
4. Compose, deliver, and stop.

Clarification detail and example questions: `references/prompt-architect.md`.

## Shape

Convey the information the task needs in the requested format. These fields are selection aids, not required headings or an ordered template. [POLICY]

- **Outcome:** the deliverable, and who it is for or where it goes.
- **Context:** the facts, source material, and representative inputs the executor needs.
- **Requirements:** the scope and applicable constraints, with an exclusion only when a plausible reading would add unintended work.
- **Method:** steps, tools, protocols and ownership only where the result depends on them.
- **Completion:** what establishes a correct result, when the task has a meaningful correctness condition.

For a delegated brief, word the accepted SDD or host contract using `references/subagent-dispatch.md`; carry only the fields that contract uses. When external content is included, separate it from instructions without repeating a trust-boundary notice the host already supplies. Request evidence and concise rationale rather than private reasoning or a quoted system prompt/model line. Execution design remains with its owning skill.

Define Done from the deliverable outward. For "rewrite this prompt", Done is the requested prompt with every stated constraint preserved. Files inspected, repository state, tests run, research completed, and handoffs written are not completion conditions unless the task asks for them.

Resolve choices that define the requested deliverable before delivery; leave implementation choices to the executor unless the method is required. Include failure or missing-input behavior when the task or interface needs it, using the existing contract rather than inventing status codes. An unsupported claim remains unknown. Omit generic failure catalogs and repeated checklists. [DOC]

## What the prompt carries

Keep information that changes the executor's actions, establishes a necessary fact or requirement, or defines completion. It must be relevant to the requested scope and valid when the prompt runs; brevity alone does not prove better outcomes. [POLICY]

- Do not transfer author-session state, unrelated discovery, administrative procedure, or speculative precautions.
- Do not introduce commits, branches, working-tree state, staging, rollback, HEAD, tags, or repository-preservation procedures unless the user requested them, the supplied plan requires them, or the host contract mandates them.
- Name source material only when the task depends on it. Do not require broad discovery before a bounded task starts.
- Include a tool or procedure only when the user requested it, a governing instruction requires it, or omitting it would prevent correct completion; use it at the point its output becomes necessary.

## Techniques, when they help

Use a technique only when the target task, the model's guidance, or measured behavior justifies it. Model-specific guidance lives in `references/sources-and-contradictions.md`.

- **Examples.** Use them when they communicate behavior more clearly than another instruction, or when evaluation shows they help. `references/few-shot-learning.md`
- **Reasoning guidance.** Do not add step-by-step reasoning instructions by default. Follow the target model's guidance, and add explicit reasoning structure only when it improves the task. `references/chain-of-thought.md`
- **Structured output.** For a consumer needing typed data, use native constrained generation when available. Parsing and schema validation are distinct from checking factual support; the consuming application handles refusal and incomplete output. [Pattern 1](references/details.md#pattern-1-structured-output-with-pydantic).
- **Context and instruction structure.** Separate instructions, source material and examples with clear headings or delimiters. Include relevant evidence and remove irrelevant material; no delimiter is a security boundary or universally optimal format. [DOC]
- **Model changes.** Recheck inherited prompting habits against the target model's current guidance. Stronger emphasis, more examples, more reasoning text and more verification are not universal improvements. `references/sources-and-contradictions.md`
- **Templates and system prompts.** `references/prompt-templates.md`, `references/system-prompts.md`
- **A prompt that underperforms.** `references/prompt-optimization.md`
- **Worked examples.** `references/details.md`

## Development briefs

Distinguish the latest request: planning produces or revises a plan; implementation changes the requested behavior or artifact and runs relevant checks; verification assesses delivered results against acceptance. Existing plans supply intent, settled decisions, procedure and handoff context. They guide execution; a plan or status update alone does not satisfy an implementation request. Historical plans and handoffs do not establish the current runtime mode. [POLICY]

For implementation briefs, name the bounded behavior or artifact and observable result, including an affected interface when relevant. When downstream work depends on the result, state **output → next consumer → unlock condition**. Choose the smallest sufficient acceptance evidence and state its limits; compilation alone does not establish rendered behavior or a live data path. Do not prescribe a universal test suite. [POLICY]

Direct deliberate changes within the requested scope. Carry operational approvals only when the user, an applicable governing instruction or the host requires them. Continue through ready authorized work until the requested result is delivered or remaining requirements need input. Update existing status and evidence with blockers, downstream dependencies and the next ready task when the task uses those records; do not add plan hierarchy merely to resume implementation. If the runtime prohibits execution, identify the active restriction and required transition. [POLICY]

## Planning prompts

Apply these when the requested prompt asks an agent to produce or revise a plan, or review its closure. Resuming implementation from a plan follows Development briefs.

- Ask for a plan when material uncertainty, sequencing, cross-session continuity, or risk makes one useful. Clear bounded changes get direct instructions.
- **Acceptance carries the contract.** State the observable result and smallest sufficient evidence for the plan's tasks or milestones, including failure or invalid-input behavior when the user, plan or affected interface requires it. Use actual available commands and expected results when applicable; do not invent commands or an exhaustive edge-case panel. [POLICY]
- **Interfaces, not guessed internals.** Identify affected files, interfaces and constraints when they matter to the plan. Use bounded exploration for an unknown that prevents correct dependent work instead of prescribing guessed internals. [DOC]
- **Clarify only what changes the plan.** Surface unresolved choices that affect requirements, architecture, data, authority, interfaces, or acceptance; use bounded exploration for discoverable facts and keep dependent work pending rather than guessed. [POLICY]
- **Match the requested phases.** For a plan-only request concerning source changes, say "do not edit source files" and finish when the requested plan is delivered. When authoring a prompt for planning and implementation together, have its executor carry the run through both phases without an invented approval or stop. Preserve actual runtime restrictions: a prompt cannot switch modes or grant execution authority. [POLICY]
- **Resume from state, close by convergence.** Use the plan's recorded state and reconcile evidence against current inputs; rerun only failed or invalidated checks. Resumption or compaction alone does not invalidate passing evidence. When the requested artifact is a read-only closure review, compare the plan with the delivered changes and report only missing, partial, contradicting or unrequested work. Completion requires valid observed evidence. [POLICY]

## Delegated work

Write the worker's instructions clearly. Do not decide whether to delegate, how many workers to use, or which orchestration mode to use; route those decisions to the owning skill.

| Load only when | Read |
| --- | --- |
| The requested artifact is a dispatch brief or return contract | `references/subagent-dispatch.md` |
| The requested artifact is the wording of a workflow request or escalation clause | `references/orchestration-modes.md` |
| The prompt's own task crosses a context or session boundary | `references/long-horizon-context.md` |

## Deliver

- Keep clarification focused on material missing information and the context needed to answer it.
- Deliver the requested artifact and format: a complete prompt, template, system message, surgical diff, or review. A fenced block is a useful default for a copyable text prompt, not a requirement for every format. Add only requested explanation or a concise change note, saved path or unresolved limitation.
- If an optional caution matters enough to mention, keep it to one note outside the artifact; do not turn it into an executor requirement. Preserve cautions that are actual requirements. [POLICY]
- Do not execute the prompt unless separately asked.

Supporting files: `assets/prompt-template-library.md`, `assets/few-shot-examples.json`, and `evals/cases.json`, whose stored statuses do not establish current passes.

## Not this skill

This skill words the instruction. It does not choose the machinery, the roster, or the plan.

- Deciding that N tasks are independent and fanning them out, executing an implementation plan through per-task implementer and reviewer subagents, or installing a written plan through serial packet workers: `subagent-driven-development`
- Decomposing work into units, dependency graphs, critical path, workload balance: [SDD task decomposition and dependencies](../subagent-driven-development/references/task-design.md)
- How many agents, which preset team, which subagent type, which display mode: [SDD team size and roles](../subagent-driven-development/references/team-selection.md)
- Message types, plan-approval handshakes, team shutdown: [SDD handoffs and runtime operations](../subagent-driven-development/references/team-runtime.md)
- Allocating review dimensions, deduping findings, calibrating severity: `multi-reviewer-patterns`
- Competing root-cause hypotheses and evidence arbitration: `parallel-debugging`
- File ownership and interface contracts between parallel implementers: `parallel-feature-development`
- Execution state and recovery across compaction or sessions: `subagent-driven-development`, using the existing native task record and evidence handoff
- Effort values, thinking budgets, model selection, API mechanics: `engineer-claude-api`
- Whether the planned work should be built at all, or trimming a plan to what ships: `anti-overbuild`
- Scoring or benchmarking output quality: `llm-evaluation`
- Authoring or registering a SKILL.md: `writing-skills`, `skill-creator`
