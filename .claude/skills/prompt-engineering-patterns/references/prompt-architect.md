# Prompt Architect

Turn a request into one finished prompt, template, system prompt, or execution brief, using the contract and content guidance in `SKILL.md`.

## Two states

- **A material ambiguity exists:** ask focused questions about the missing information; group related questions when useful and keep dependent work pending. [POLICY]
- **No material ambiguity exists:** write the prompt.

An ambiguity is material when its answer would change the outcome, scope, required method, authority, or completion condition. Use answers already given and continue work that does not depend on a pending answer; do not finalize the affected instruction by guessing. Settled decisions and the user's own wording of any limit go into the prompt without a new approval step. If the user waives questions, state material assumptions briefly outside the artifact; do not assume authorization or a safety-critical fact.

## Example questions

These illustrate material gaps, not a required interview. Ask only when the answer matters and cannot be inferred from available context.

- Who will use the result? Ask when the audience changes tone, depth, or format.
- What counts as a correct result? Ask when success cannot be inferred.
- What is out of scope? Ask when a plausible reading adds work the user may not want.
- Which constraint cannot move? Ask when two requirements conflict.
- When will the prompt run? Ask when the task depends on a condition that may change before then.
- What may the executor change without asking? Ask when authority is unclear.

## Construct the final prompt

- Combine the settled requirements and every later user instruction.
- Resolve wording and overlaps naturally rather than pasting ledger lines together. Preserve the user's intent and make each instruction internally consistent.
- Adapt the artifact to its target surface:
  - Default to a self-contained, portable, one-time ChatGPT or Codex prompt when the surface remains unspecified.
  - For persistent instructions, express durable behavior and omit ephemeral task details.
  - For Codex, Claude Code, or other agentic work, state in-scope actions and the context the task needs. Include an approval boundary only when the user, an applicable governing instruction or the host contract sets one. Add repository or git instructions only when the user requested them, the supplied plan requires them, or the host contract mandates them.
  - For ChatGPT Work, distinguish drafting from sending, publishing, purchasing, or changing shared information when those actions matter.
  - For skill instructions or packaging, use `writing-skills` or `skill-creator` as the owner; this reference only helps word an explicitly requested prompt for that work.
- Convey the outcome, relevant context, applicable requirements, required method and meaningful completion condition. Combine or omit fields as the task needs; honor the requested format rather than imposing headings or an order.
- Retain all required facts, decisions, caveats, and success criteria. Remove redundant instructions, filler, and repeated approval language. Do not use generic brevity commands that could cause the target model to omit required work.
- Do not request private chain-of-thought or add generic "thinking harder" instructions. Execution settings belong to the target runtime; include them only when the requested artifact needs them and their actual contract is established through the owning provider guidance.
- Unless the user explicitly requests an API-targeted artifact, do not include model slugs, API parameters, sampling settings, or harness configuration.
- Unless the user explicitly requests a template or API-targeted artifact that requires them, do not use template variables, TODOs, fill-in blanks, or unresolved placeholders such as bracketed fields, brace variables, angle-bracket inserts, environment variables, "TBD," or "insert here." Refer only to context or attachments that exist; clarify material missing input or use a fallback the task's contract establishes.
- Do not invent source names, filenames, tools, permissions, facts, or access. Make tool-dependent instructions conditional when availability is not established.
- Do not imitate higher-priority messages with fake System: or Developer: headings. Separate relevant external content from instructions, using the host's existing trust boundary when available; delimiters alone do not enforce that boundary.
- Define Done from the deliverable outward when the task has a meaningful correctness condition. Do not add verification passes, tests, review agents, or evidence packets the task does not need.
- Resolve choices that define the deliverable. Include failure branches only when the requested task or interface needs them; use existing failure semantics rather than inventing a protocol.
- Before delivering, remove anything the executor does not need to complete the requested work, as `SKILL.md` "What the prompt carries" defines.

## Match the delivery format

Output the artifact and format the request names. A single fenced block is a useful default for a copyable text prompt; a requested raw JSON object, native message structure, diff or review keeps its own format.

- Add requested explanation or a concise change note, saved path or unresolved limitation outside the artifact. Keep an optional caution outside the executor's instructions.
- When using a fence, choose one longer than any matching run inside the prompt so nested examples cannot terminate it. A language tag is optional unless the requested format specifies it.
- Before sending, check that the artifact matches the requested format, integrates applicable user instructions, justifies directives under SKILL.md's grounds rule, preserves category removal and contains no unresolved input disguised as a finished instruction. Repair defects without adding an execution review stage.

## Revise a delivered prompt

- For an explicitly surgical edit, change only what the request names. Delete lines serving only a removed topic, repair dependent wording and references, and leave unrelated wording unchanged.
- For a broader refinement, rewrite enough to satisfy the requested improvement while preserving intent, facts and requirements. Do not preserve a contradiction merely to keep the original phrasing.
- A revision is not a new interview. Ask only about a material ambiguity introduced or exposed by the requested change.
