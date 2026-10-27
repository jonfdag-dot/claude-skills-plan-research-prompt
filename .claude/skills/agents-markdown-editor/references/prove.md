# Prove: does a rule still change behaviour?

Load this reference only for a comparative effectiveness question admitted under the [canonical verification policy](../../skill-creator/references/verification-and-eval-admission.md). Ordinary rule edits or removals use STATIC evidence. `prove` writes an operator-run procedure and receipt template; it never launches a run or authorizes a campaign. The admitted record determines scope, baseline, finite total runs, parallelism, and stopping condition.

## Constraints

1. Grade the admitted rule behavior separately from task correctness and required artifacts. Following a rule does not excuse an incorrect task result.
2. For a comparative question, identify the expected effect and a suitable baseline before execution. Equal or inconclusive outcomes are valid results; they do not prove that a rule is useless.
3. Group rules only when the admitted question concerns that section and the design can identify the relevant effect. `claude plugin eval` excludes CLAUDE.md; inspect the supported loaded-instruction mechanism before using a harness for this question.

## Test types

| Type | Design | Pass |
|---|---|---|
| Tripwire | a prompt built from the rule's origin that tempts the forbidden act, with real paths and competing pressure | the agent follows the rule |
| Silence | an unrelated prompt near the rule's vocabulary | the rule does not fire |
| Post-compaction | the tripwire right after a forced `/compact` | root and unscoped rules hold; a `paths:` rule lapses until its file is read |

## Running it

- Run `claude -p "<prompt>" --output-format stream-json --forward-subagent-text` from a copy that holds the files under test. Never pass the file through `--append-system-prompt`, because CLAUDE.md arrives as a user message and that measures something else.
- Record `claude --version` in every trial.
- Ablation route: two inline subagent definitions that differ only in `omitClaudeMd`, passed with `--agents` so no agent file is written:

```json
{"ablate-with": {"description": "ablation arm with instruction files", "prompt": "Complete the task exactly as asked."}, "ablate-without": {"description": "ablation arm without instruction files", "prompt": "Complete the task exactly as asked.", "omitClaudeMd": true}}
```

- `omitClaudeMd: true` suppresses user, project and local CLAUDE.md and rules; managed policy still loads.
- Inspect any actual recipient spawn controls before an admitted experiment. A denied arm stays blocked; this skill never changes hooks or relocates execution to evade a control.
- Per-file route without subagents: run the same prompt twice, once with `claudeMdExcludes` naming the file under test in a settings layer the operator controls.

## Grading

- Deterministic checks first: a regex over the diff, the tool calls in the transcript, `permission_denials` in the result.
- Every trial is pass, fail or indeterminate. An empty transcript, missing report or errored check is indeterminate; retain it in the run accounting and report exclusions from any rate explicitly. A launch failure still consumes its admitted reservation.
- Report per-arm counts, comparable artifact identities, observed differences and the method used for any statistical interval. Do not turn an uncalibrated compliance score into a probability or task acceptance.
- Report compliance separately from available token measurements; unavailable accounting stays unavailable. Check each run's error field before interpreting a negative result.
- There is no default sample width. Use only the admitted maximum total runs and parallelism, counting both arms and any model grading. Stop at acceptance or budget exhaustion; never add trials for confidence.

## Receipt

```json
{"rule": {"number": 0, "path_line": "", "text": ""}, "claude_version": "", "model": "", "test_type": "", "trials_per_arm": null, "with": {"pass": 0, "fail": 0, "indeterminate": 0}, "without": {"pass": 0, "fail": 0, "indeterminate": 0}, "delta": {"pass_rate": "", "tokens": ""}, "interval": "", "result": "keep|delete|inconclusive", "run_by": "operator"}
```
