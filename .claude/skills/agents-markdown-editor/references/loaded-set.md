# Loaded set and budgets

Inventory describes what exists; static resolution predicts what can load; supplied runtime receipts establish observed loading for their session. Resolve the set per runtime, judge it as one document, and prefer measured ground truth over inference.

## Claude Code

- Scopes load and concatenate in this order: managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS), user (`~/.claude/CLAUDE.md`, `~/.claude/rules/`), every directory from the filesystem root down to the working directory (`CLAUDE.md` or `.claude/CLAUDE.md`, then `CLAUDE.local.md`), then project rules (`.claude/rules/`).
- Compare the applicable instructions and accepted authority as a chain; concatenation does not make every apparent difference an unresolved conflict. Quote both locations and distinguish runtime precedence, scope and product decision ownership.
- CLAUDE.md arrives as a user message after the system prompt. A binding instruction differs from technical enforcement; a requested prevention guarantee needs actual hook/permission coverage.
- A `CLAUDE.md` below the working directory loads only when Claude reads files in that subtree. The linter classifies historical/fixture copies from path and content evidence and reports them; inspect activation hazards separately. A `.session` directory name alone does not suppress genuine live guidance.
- Anthropic's documentation targets under 200 lines per CLAUDE.md. It is advice, not a limit; the risk is the aggregate across files that load together.

## @path imports

- `@path` outside code imports a file at launch; `` `@path` `` in backticks is literal text.
- Relative paths resolve against the importing file. Recursion stops at four hops.
- An import outside the working directory needs one-time approval; a declined import loads nothing while the file still reads as if it did.
- Imports do not save context, so an `@path` split is never a size fix.

## Rules with `paths:`

- A rules file without `paths:` loads at launch. With `paths:` it loads when Claude touches a matching file: Read, and since 2.1.288 Write and Edit, and since 2.1.293 a single-file `cat`, `head`, `tail`, `sed -n` or `grep` in Bash; nested CLAUDE.md files follow the same triggers. `paths` is the only rules frontmatter field Claude Code reads, and user rules (`~/.claude/rules/`) load before project rules.
- Three preconditions for a paths-scoped MOVE: touching a matching file is a fair trigger (below 2.1.288 only Read triggers it, so a rule that must fire when a file is created fails there); the rule may lapse after `/compact` until a matching file is touched again; the rules directory is not a symlink into another project, and since 2.1.290 a CLAUDE.md, rule or AGENTS.md symlinked outside the working directories does not load when reads outside them are blocked. Since 2.1.292 the transcript notes a nested instruction file that did not load.
- One rule's `paths` list shares a budget of 1,000 expanded patterns and 4 MiB; brace groups multiply; an over-budget pattern or an unclosed `[` silently matches nothing (G12).

## AGENTS.md and Codex

- Claude Code (2.1.277 and later) reads AGENTS.md through its built-in agents-md plugin only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or above; `~/.claude/CLAUDE.md`, managed CLAUDE.md and `.claude/rules` do not count toward that check. It then reads every `AGENTS.md` and `.claude/AGENTS.md` upward, loads subdirectory files lazily, expands `@` imports and never reads `AGENTS.local.md`, `AGENTS.override.md` or anything under `.agents/`. A repository with both files loads only CLAUDE.md unless user, `--settings` or managed settings set `pluginConfigs["agents-md@builtin"].options.instructionFiles` to `claude-md-and-agents-md`; project and local settings are ignored for that key. The interop routes remain a CLAUDE.md that imports `@AGENTS.md`, which never double-reads, or a symlink; both load the same text, so the saving is maintenance, not tokens. Twins that differ on purpose are a valid setup; do not propose converting them.
- Codex, opencode and kimi-code read AGENTS.md; opencode falls back to CLAUDE.md, including `~/.claude/CLAUDE.md`.
- Codex takes the first non-empty readable `AGENTS.override.md`, `AGENTS.md` or configured fallback filename per directory from the project root to the working directory and joins them root first. Project files share `project_doc_max_bytes` (default 32,768): the file that crosses it is byte-truncated with only a log warning and every deeper file is dropped. The global override/AGENTS selection under the active Codex config root is outside that budget. Resolve `CODEX_HOME` or a selected config root instead of assuming `~/.codex`. Project trust and instruction loading are distinct; disclose trust-sensitive configuration and session overrides not observed by the static tool rather than inferring them from role labels.
- Within the discovered Codex project chain, narrower directory instructions override conflicting broader instructions for their scope; `AGENTS.override.md` replaces `AGENTS.md` in the same directory. Report unresolved same-scope contradictions after applying precedence, rather than treating a valid narrower override as a contradiction.
- Read the budget from the config (G13); never assume the default. Raising it moves the cost rather than removing it.

## What loads versus what exists

- Supplied `/context` and runtime instruction receipts are stronger loading evidence than a model self-report; without them, label the assessment static. `/context` can establish observed context accounting; the linter's figures are estimates at 3.7 characters per token.
- The `InstructionsLoaded` hook reports `file_path` and `load_reason` for files that load and is the only direct proof that a `paths:` rule fired. It does not fire for an AGENTS.md read through the agents-md plugin; confirm that read with `/context`. The operator adds it; this skill never writes settings: `{"hooks": {"InstructionsLoaded": [{"hooks": [{"type": "command", "command": "cat >> /tmp/instructions-loaded.jsonl"}]}]}}`
- Retain concise task routing where the relevant runtime needs it; inspect current compaction/reload behavior rather than transferring another runtime's guarantees.
- A conflict with text the harness injects is visible only in a transcript; read one when the operator supplies it.

## steward-lint.py flags

| Flag | Use |
|---|---|
| `--repo` | repository root (required) |
| `--cwd` | working directory inside the repository; decides the directory chain and the Codex chain |
| `--home` | home directory for user scope (default the real home) |
| `--codex-home` | active Codex root; defaults to `CODEX_HOME` or `<home>/.codex`; controls global instruction discovery |
| `--codex-config` | selected TOML file for project byte budget and fallback instruction filenames; defaults to `<codex-home>/config.toml` |
| `--claude-settings` | repeat selected settings layers in precedence order to assess loading options/exclusions; only loading-related fields are used |
| `--pointer-root` | the real repository when auditing a copy; also used for package scripts and contract checks |
| `--claude-version` | output of `claude --version` |
| `--ack-canonical` | the canonical file the operator named; clears G10 for that pair |
| `--all` | list report and info findings in text output |
| `--json` | full machine-readable report |


## Configuration and coverage limits

Inspect loading-related fields only; never read or log credential values. Honor `claudeMdExcludes`, scoped activation, selected instruction-file configuration and ancestors before counting duplication. Record active settings/config layers and any inaccessible or unspecified layers, CLI overrides, declined imports, trust state and dynamic activation as unknown where unresolved. Tool inventory is not proof of active loading or authorized use.

Separate requested roots from the active working-directory chain. Include filename inventory, content screening and full semantic review as distinct coverage depths, and classify physical aliases, canonical files, native mirrors, generators, distribution/upstream copies, templates and history. A file not active now can still be a hazardous ancestor or lazily activated template. Do not describe archived/upstream content as fully reviewed live policy.

The 2026-10-03 audit observed Claude 2.1.287 and Codex 0.160.0 and supplied retained runtime-source evidence; the 2026-10-10 gap pass observed Claude 2.1.296 and Codex 0.162.1 and refreshed the rule-trigger and symlink lines from the 2.1.288–2.1.293 release notes. These are dated observations, not future minimums or guarantees. Refresh loading claims when the runtime/configuration relevant to a finding changes.

Default settings discovery merges applicable user/project/local exclusions, but project/local layers do not control the built-in `instructionFiles` option. Explicit `--claude-settings` paths represent operator-selected effective layers; their original provenance and actual runtime application remain unverified. Exclusions support basic path-segment globs and recursive `**`; unsupported extended glob syntax is reported as unknown.
