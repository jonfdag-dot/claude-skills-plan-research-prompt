---
name: agents-markdown-editor
description: "Audits and surgically edits loaded agent instruction files, including CLAUDE.md, .claude/rules and AGENTS.md. Use when: instructions are long, stale, ignored or contradictory; enforcement claims lack a mechanism; Codex truncates AGENTS.md; a root file needs placement or byte-budget cleanup; or a generated tool block keeps returning. Not for: SKILL.md wording → writing-skills; skill or native agent lifecycle → skill-creator; a new CLAUDE.md → /init."
---

# Agents Markdown Editor

Audit the instruction set the runtime loads, then apply an authorized bounded edit. A static loading prediction differs from a runtime receipt. Assess the applicable chain rather than judging one file in isolation.

## Scope and boundaries

Inspect `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`, their imports and relevant nested instruction files. Other-runtime files may be inventoried for interoperability, but this kit provisions only Claude. New project instructions can start with Claude's `/init` and the active codebase; this skill owns audit and surgical correction.

`audit` and `propose` leave targets unchanged. A direct bounded edit request authorizes its named scope and checks. Discretionary cuts need a numbered proposal and the user's selected items. Preserve user-scope configuration and unrelated edits; never edit settings, hooks, CI, migrations or enforcement machinery through this skill.

## Audit

1. Establish target roots, cwd, user scope, runtime version, authorization and applicable project contracts. Inventory aliases, imports, local overrides, rules, generated regions, templates and history. Separate file inventory, content screening and full semantic review; inaccessible content stays unknown.
2. Read [loaded-set.md](references/loaded-set.md) for loading questions and [gates.md](references/gates.md) for findings. Run `python3 -B <skill-dir>/scripts/steward-lint.py --repo <repo> --cwd <working-directory> --claude-version '<observed-version>'`. Inspect its effects first. `--home`, `--claude-settings` and `--pointer-root` select the actual scope; do not imply defaults describe an unknown recipient configuration.
3. Present static findings with exact evidence and scope. A completed report with exit 1 means block findings; a crash means unknown coverage. Token figures are estimates. `/memory` and `/context` from a real session supply stronger loading evidence; never invent them.

## Propose

Read every applicable file in the requested semantic scope, record hashes and classify each change KEEP, REWRITE, MOVE, DELETE, PROVE or ASK. Select [cut-classes.md](references/cut-classes.md) for semantic cleanup, [placement-model.md](references/placement-model.md) for placement, [rule-grammar.md](references/rule-grammar.md) for wording and [code-first-cleanup.md](references/code-first-cleanup.md) for oversized roots or generated tool blocks.

Preserve distinct requirements, genuine safeguards, owner boundaries and active runtime behavior. File length or age alone does not establish a defect. Generated content needs its source owner. Resolve canonical ambiguity before editing; do not convert instruction prose into a false claim of enforcement.

Give numbered items with exact path/location, trigger, original and proposed text, reason, preserved obligation and relevant check. Distinguish demonstrated defects from judgment items and unresolved blockers. Propose only changes that affect correctness or the stated request, with no deletion quota or unmeasured speedup claim.

## Apply

Read [review-record.md](references/review-record.md). Apply selected numbered items or the directly authorized bounded change, preserving the baseline and unrelated work. Reconcile changed hashes before overwriting. Keep locked/generated/unresolved items unapplied with a concrete reason. Use [model-overlays.md](references/model-overlays.md) only for a relevant model or context-budget finding.

Run affected static and contract checks, inspect the owned diff and record actual outcomes. Existing valid evidence needs no repeated check. Report applied and remaining items, exact files, actual checks and unverified native behavior. Do not widen into an audit of another project or permission system.

## Prove

Use [prove.md](references/prove.md) to write a requested procedure and receipt template without starting model runs. Model-dependent evaluation requires admission under [verification-and-eval-admission.md](../skill-creator/references/verification-and-eval-admission.md); ordinary instruction edits remain STATIC.
