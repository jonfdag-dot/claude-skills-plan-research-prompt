# Placement model: eight homes

Most of what is wrong with a large instruction file is correct content in the wrong home.

| # | Home | Loads when | Context cost | Enforcement | After `/compact` |
|---|---|---|---|---|---|
| 1 | Hook | at the lifecycle event | none | deterministic | runs outside the context |
| 2 | Permissions or sandbox settings | at the tool call | none | deterministic | runs outside the context |
| 3 | CI, lint or test | on push or pull request | none | deterministic | runs outside the context |
| 4 | Root CLAUDE.md | every session | full text every request | instruction; no technical blocking | re-read from disk |
| 5 | `.claude/rules/` without `paths:` | every session | full text every request | instruction; no technical blocking | re-read |
| 6 | `.claude/rules/` with `paths:` | when Claude reads a matching file | none until triggered | instruction; no technical blocking | lapses until retriggered |
| 7 | Skill | body when invoked, selected or explicitly preloaded; metadata at discovery | metadata plus the selected body and resources actually read | instruction; no technical blocking | inspect the runtime's listing and reload behavior |
| 8 | Doc or reference file | when something points at it | none until read | none | not loaded |

Homes 1 to 3 are locked paths for this skill: propose the stub and write the needed edit into the review record.

## Decision procedure (first yes wins)

1. Does the requested guarantee require technical prevention independent of model compliance? Propose a hook/permission change separately; retain the normative requirement.
2. Can a machine check it after the fact? CI or lint, with at most a one-line pointer in the file.
3. Would it still be true if this project vanished? The user file, a tool description, or nowhere.
4. Does the actual runtime already supply equivalent guidance with the needed scope? Assess overlap and authority before proposing a cut.
5. Is it a multi-step procedure, or relevant only sometimes? A skill (ASK) or a paths-scoped rule.
6. Is it true only for specific files, is reading those files a reliable trigger, and is it safe to lapse after compaction? Paths-scoped rule; all three, not only the first.
7. Is it a fact a reader needs rather than a behaviour? A doc, referenced by one line (ASK).
8. Keep concise root guidance needed for accepted requirements, preferences or non-obvious constraints. No demonstrated incident is required.

## Two layers

A skill fires only if the model judges it relevant from a description that disappears after compaction. Keep the decision in the always-loaded file ("for X, use skill Y") and move the procedure into the skill or scoped rule.

## What belongs in the root

- Build, test and run commands that cannot be guessed.
- Conventions that differ from tool defaults.
- Repository etiquette: branch model, commit conventions, what may never be pushed where.
- Architectural decisions, one line each with a pointer.
- Environment quirks: required variables, the interpreter that actually works.
- Non-obvious gotchas, which should take most of the budget.
- The routing lines that reach the other seven homes.

## Tool and MCP routing

Collapse per-tool prose to one roster line in the root plus a pointer to the routing rule file. Keep the roster: once tool schemas are deferred, a model cannot search for a tool it does not know exists.
