# Static gates

`scripts/steward-lint.py` runs with no model, no network and no command execution, prints the scope each gate assumed, gives identical output on repeat runs, and exits 1 when any gate blocks (2 on usage errors). Text output lists every block and warn finding; report and info findings are counted, and `--all` lists them.

## Verdicts

- `block`: a static defect candidate or ownership safeguard. Confirm scope and false-positive context before making a Tier 1 claim; it never grants edit authority.
- `warn`: a hazard requiring assessment: a contract check that reads the file, a user-scope duplicate, instruction-file copies inside the repository. For an authorized edit, inspect the G9 reader and its effects, verify the proposed edit satisfies its contract, and record the evidence without renewed approval. The static reader warning can remain after that reason is cleared; unavailable or failing checks stay unresolved, and locked paths remain protected.
- `report`: a lead for propose, never an edit by itself.
- `pass`: nothing above info.
- `indeterminate`: the gate could not measure. Never read it as a pass.

When a block looks wrong, check the scope line before acting on it.

## Gate table

| Gate | Checks | Blocks or warns when | Cannot see |
|---|---|---|---|
| G1 size | lines, bytes and estimated tokens per file and for the unconditional set; instruction-file copies inside the repository | warns once for copies; size is report-only above 200 lines per file or 400 aggregate | real token counts (`/context`) |
| G2 pointers | backticks, Markdown links and absolute paths | blocks a directory-qualified path that exists nowhere, in assertive context | pointers into sibling repositories |
| G3 model phrases | phrase families from the Fable 5 and 5.1 and GPT-6 Astra guides, and text Claude Code already injects (floor 2.1.273; last checked on 2.1.286) | never; report only | whether the phrase still changes behaviour (prove) |
| G4 duplication | 4-gram Jaccard over prose of 10+ words across non-excluded files predicted to load at launch | blocks two project-side files sharing text at 0.90; warns when the pair crosses user and project scope | paraphrases below 0.5 |
| G6 emphasis | uppercase NEVER, MUST, IMPORTANT, CRITICAL, ALWAYS, bold-only lines, bold directive leads, ALL-CAPS runs | never; report above 3 lines per file | which emphasis expresses an accepted preference or safeguard |
| G7 enforcement | claims such as "enforced by" or "is blocked" against hooks, CI, lint and permission machinery | blocks a named machinery path that does not exist, or a claim whose machinery kind is absent | whether existing machinery enforces this exact rule |
| G8 executable | assertive shell/inline commands with resolved package cwd and interpreter script targets; slash commands and literal examples distinguished | blocks a missing script, package script, make target or python module in assertive context | anything that needs running |
| G9 contract | self-claims (exact line counts, byte-identical twins, every path resolving) and resolved content/path consumers in scripts, tests, `.work`, CI and root build files | blocks a false self-claim; warns for identified consumers with their property | complete dynamic dataflow or the full contract (inspect actual target/property) |
| G10 twins | `CLAUDE.md` and `AGENTS.md` in the same directory: symlink, import stub, identical or divergent | blocks a symlink or stub pair until `--ack-canonical` | which direction the operator prefers |
| G12 glob budget | `paths:` brace expansion against 1,000 patterns and 4 MiB; unclosed `[` | blocks over budget or malformed | whether the glob matches the files that matter |
| G13 runtime bytes | non-empty Codex project selection, including configured fallback names, against the selected `project_doc_max_bytes` | blocks a file Codex would truncate or drop | untrusted-project state |
| G15 required reference | skills, agents and documents marked required or must-read | blocks a required skill or agent that is not installed, or a required document that does not exist | plugins installed outside `~/.claude/plugins` |
| G16 generated | standalone paired `<!-- name:start -->` and `<!-- name:end -->` markers outside illustrative code | warns on an unclosed marker; reports each region | which tool regenerates it (read the repository) |

Evidence is the measured fact: counts, bytes, the named path, the Jaccard score, the reading check's path and line. G3, G6 and G7 findings are leads; the item they produce is Tier 2 unless something else verifies it.


## Semantic review beyond static gates

The linter is an aid, not a complete policy or loading verifier. Semantic review finds contradictions across deadlines/grades/releases, surviving effort obligations, output floors, source/query quotas, and claims that every blocker is solvable. Use the qualified catalog, accepted authority and actual consumers; no linter pass proves these absent.

G9 filename mentions require target/property assessment. Deny-path tests and path maps need no universal content-edit block; generator anchors, vocabulary parsers and enforced line counts remain protected. A false count proves an unmet criterion without authorizing its repeal. G7 flags technical claims, not mandatory human review by itself. G8 must distinguish illustrative/runtime commands and resolve actual working directory and script arguments. G16 applies to real standalone markers, not inline/fenced examples.

Classified history remains in the inventory and placement assessment. Excluded files cannot establish active duplication. Config overrides, dynamic readers and exact hook coverage remain explicit uncertainty until relevant evidence resolves them. No check executes embedded commands or authorizes target shipping, installation or external operations.
