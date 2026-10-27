---
name: skill-creator
description: "Creates and maintains skill lifecycles. Use when: creating, importing, copying, registering, renaming, moving, delisting or removing a Claude or Codex skill; changing skill invocation or routing registration; explicitly evaluating a skill. Not for: wording, discovery descriptions, examples or resource layout → writing-skills; instruction-file audits → agents-markdown-editor; capability consolidation → skill-consolidator."
---

# Skill Creator

Own a skill's location, lifecycle, native metadata and discovery. Use `writing-skills` for wording and resource design. This starter is Claude-only; Codex parity is not provisioned and creates no additional work.

## Contract

Capture capability, trigger, owning scope, inputs, outputs, constraints and observable completion. Search the existing [index](../INDEX.md) before adding another owner. Preserve unrelated edits. A copying or wording request permits static verification, not paid model evaluations.

## Procedure

1. Read [verification and evaluation admission](references/verification-and-eval-admission.md). STATIC is the default: inspect files, parse metadata, check paths and run focused deterministic checks.
2. Inspect source identity, existing equivalents, notices and licensing before importing. Keep reusable skills in `~/.claude/skills/<name>/`; use `<project>/.claude/skills/<name>/` for project-specific workflows. Keep one `SKILL.md` directly inside each named skill folder.
3. Make the smallest authorized change. Put `name` and a concrete `description` in YAML frontmatter. Names use lowercase letters, digits and hyphens, at most 64 characters; descriptions are at most 1,024 characters in this starter.
4. Keep the essential contract and reference-selection reasons in `SKILL.md`; place details in `references/`, deterministic tools in `scripts/` and copyable scaffolds in `assets/`. Select [writing-skills](../writing-skills/SKILL.md) when changing content.
5. Update the human `skills/INDEX.md` and every affected caller when adding, renaming or removing a skill. Native discovery uses the skill files; this starter has no generated catalog or custom router. Do not invent a curation or hook requirement.
6. Run `python3 -B <skill-creator>/scripts/quick_validate.py <changed-skill-folder>`, check referenced files and review the owned diff. Do not claim live discovery from disk inspection alone.
7. Report resulting capability, files, actual checks, unavailable runtime proof and any residual dependency. Commit, publish or change permission policy only under separate authority.

## Optional templates and evaluation

Use the template in `assets/template-skill/` as a scaffold and replace its placeholders and copied invocation policy deliberately. The canonical admission reference governs any explicitly requested model experiment. Optional evaluator engines and campaign assets are outside this starter; identify the unmet capability rather than claiming an evaluation ran.
