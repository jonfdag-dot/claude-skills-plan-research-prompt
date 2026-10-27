---
name: writing-skills
description: "Authors and reviews skill instructions, discovery wording, examples and selective resources. Use when: drafting or revising SKILL.md content, choosing a skill name, tuning a discovery description, clarifying inputs and outputs, or deciding what belongs inline versus in references, scripts or assets. Not for: lifecycle, import, registration or native agents → skill-creator; loaded instruction files → agents-markdown-editor; comparing or retiring overlapping skills → skill-consolidator."
---

# Writing Skills

Write the smallest content change that satisfies the requested capability. Skills package reusable instructions, patterns, tools or references; a technique's effectiveness remains a separate evidence question.

## Scope

Use this skill for wording, discovery and resource organization. Use skill-creator for creating or changing lifecycle, registration, invocation metadata and native agents; use agents-markdown-editor for the instructions a runtime actually loads. A content edit still requires affected native metadata and human-index updates under skill-creator; this starter has no other-runtime twin.

Capture the intended user outcome, trigger, required inputs, output, constraints and observable acceptance. Reuse the conversation and existing artifacts. Ask only about gaps that materially change the artifact. Preserve user edits, callers and native differences.

For a new skill, first search for an existing capability owner. A reusable project workflow can belong in a project skill; a one-time account of a session usually does not. Keep mechanical enforcement in the appropriate deterministic tool, while documenting the judgment and invocation needed to use it. Do not add hooks, telemetry or a control system as ordinary authoring.

## SKILL.md Structure

Use native YAML frontmatter with `name` and `description`. A portable name is at most 64 characters, lowercase letters, numbers and hyphens, without leading, trailing or consecutive hyphens. On this machine descriptions are at most 1024 characters; additional installed linter constraints remain applicable. Optional native fields need their actual runtime's schema, selected through skill-creator and current native documentation.

The entrypoint explains the capability, use and non-use boundaries, inputs, output or failure, key steps and how to choose supporting resources. Keep the necessary contract inline; select only references that answer the current authoring question. A typical outline is:

```markdown
---
name: example-skill
description: "Produces a named result. Use when: concrete trigger. Not for: nearby intent → existing owner."
---

# Example Skill

State the outcome and scope.

## Contract

State inputs, output, constraints and explicit failure behavior.

## Procedure

Give the steps needed for this capability.

## Resources

Link supporting material and state when and why to read it.
```

Do not turn every heading into a requirement. A short reference skill may need only its scope and lookup guidance; a procedure with important branches needs those branches and failure behavior.

## Discovery wording

Describe what the skill does and concrete conditions for selecting it. Front-load distinguishing vocabulary, write in third person and include the nearest meaningful negative boundary. Omit workflow itineraries, model claims, results and preload rosters from discovery text.

```yaml
description: "Coordinates independent implementation tasks. Use when: an approved plan has separate ownership and interfaces. Not for: a single bounded fix."
```

Use vocabulary the user or agent would search for: named artifacts, error strings, symptoms and useful synonyms. Keep a technology-specific trigger specific to that technology; do not make a generic technique depend on one incidental API name.

A historical description anecdote suggested that workflow detail could distract from full instructions. Its model, sample and deciding artifacts are unavailable here, so it does not establish a universal causal rule. Discovery wording should distinguish selection from execution because those are different responsibilities; measured trigger claims need the canonical evaluation admission policy.

Choose a clear, discriminating name that matches existing library conventions. Active names can help scanning, but do not rename a registered capability just to follow a grammatical preference.

## Instruction and example design

Use concrete actions and observable conditions. Separate a required policy from advice or a historical hypothesis. State genuine exceptions as conditions with their applicable scope; preserve necessary qualifications. Emphasis, prohibitions and persuasion language do not enforce permissions or prove model compliance.

Match the form to the content: a procedure for an ordered task, a table for mappings, an output contract for required fields, and a small flowchart for a non-obvious branch or loop. Keep code and reference data out of flowchart labels. If rendering is requested, use the existing `scripts/render-graphs.js`; select [graphviz conventions](references/graphviz-conventions.dot) for diagram syntax.

Prefer one representative example with enough context to adapt it. Use the language relevant to the workload, self-explanatory names and surrounding prose for explanation. A runnable example needs complete inputs and explicit failure handling. Templates belong in assets when a reusable scaffold is the requested capability; there is no blanket ban on templates.

Examples must preserve user work and task authority. Do not prescribe deletion or starting over merely to satisfy a teaching procedure. Reproduce an observed failure, preserve the baseline, make the smallest authorized repair and verify the requirement.

## Resource layout and loading

Personal skill paths are `~/.claude/skills/<name>/` and `~/.agents/skills/<name>/`. Keep skills at their native discovery depth. Product-bound workflows stay in their owning project.

Discovery metadata, selected or explicitly preloaded bodies and selectively read resources are different loading stages. A file's presence or word count does not establish live context use, token cost, speed or quality. Select [token-efficiency.md](references/token-efficiency.md) when dividing or trimming content; its size targets are optional heuristics and do not justify losing a contract.

Keep commonly needed decisions inline. Link detailed domain material in `references/`, reusable deterministic tools in `scripts/` and non-callable templates or media in `assets/`. Give each resource a clear purpose and loading condition. Use explicit named skill references or links; avoid import syntax that loads unrelated content automatically.

Select [Anthropic best practices](references/anthropic-best-practices.md) for a relevant native authoring question. It is a dated vendor snapshot; evaluation examples in it supply methods, not local admission or current effectiveness evidence.

## Verification and lifecycle handoff

Read the canonical [verification and eval admission policy](../skill-creator/references/verification-and-eval-admission.md) before choosing checks. STATIC is the default for ordinary content, resource, description and routing changes. Verify parser/schema, local links, owned diff, native parity and applicable deterministic behavior. Changed routing needs focused deterministic proof after affected registration has been rebuilt.

Select creator's [ecosystem nesting](../skill-creator/references/ecosystem-nesting.md) only for affected registration and [cascade contract](../skill-creator/references/codex-cascade.md) for the declared single-runtime scope. These lifecycle steps are part of completing the edit, not a reason to preload every creator resource.

Report what changed, actual checks, registration and parity, unavailable accounting and material unresolved limitations. Do not infer efficiency or behavioral gains from concise prose. Reuse valid evidence and stop when acceptance is established.

## Conditional evaluation resources

These references are available only after FOCUSED_EVAL or FULL_EVAL admission under the canonical policy:

| Reference | Select for |
|---|---|
| [testing-and-bulletproofing.md](references/testing-and-bulletproofing.md) | Choosing scenario types and instruction forms for an admitted failure question |
| [testing-skills-with-subagents.md](references/testing-skills-with-subagents.md) | A bounded comparative or pressure-scenario design when isolated evaluator execution is authorized |
| [persuasion-principles.md](references/persuasion-principles.md) | Historical wording hypotheses and their transfer limits |
| [claude-md-testing-example.md](references/claude-md-testing-example.md) | The historical documentation-variant campaign as a design example |

These methods create no ordinary test cases, baselines, model runs or deployment gate. Respect leaf-worker limits, count every admitted model stage within its finite allowance and stop at acceptance or the budget boundary.
