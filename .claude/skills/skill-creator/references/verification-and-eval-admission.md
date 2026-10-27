# Verification and eval admission

This is the canonical skill-authoring verification policy. Its Claude source and Codex native twin represent one policy; downstream instructions reference it rather than inventing additional eval gates. Explicit user constraints and authorization remain binding.

## Three lanes

Verification is the cheapest sufficient evidence that the requested change meets acceptance. Tests/checks are deterministic checks appropriate to the changed surface. Model evals are nondeterministic behavioral or comparative experiments. The name of a script does not determine its lane.

| Lane | Entry condition | Work |
| --- | --- | --- |
| STATIC | Default for ordinary work | Inspection, parser/schema checks, lint, links, parity, build correctness, focused deterministic router probes, diff checks, and applicable project tests |
| FOCUSED_EVAL | Explicit evaluation request, or one named model-dependent acceptance/safety property unresolved by cheaper evidence | Smallest behavioral experiment covering that property |
| FULL_EVAL | Explicit comparative/regression campaign request, or demonstrated broad shared model/harness impact that focused evaluation cannot cover | Bounded comparative or regression campaign over the affected scope |

Creation, editing, optimization, renaming, import, removal, mirroring, reference/documentation/prompt changes, aliases, metadata and narrow routing changes remain STATIC. Complexity, file count, instruction changes, and additional confidence are not admission conditions. A router-engine/shared-scoring change can justify a full deterministic routing corpus without authorizing any model eval.

## Admission before model execution

Admit an eval only when the user explicitly requests an evaluation/benchmark, or a named acceptance or safety property depends on nondeterministic model behavior and cannot be established from valid existing evidence, direct inspection, deterministic checks, or focused integration tests. For FULL_EVAL, also identify the actual comparative request or the demonstrated broad impact; do not escalate merely because focused results are inconvenient.

Before loading evaluation workflow instructions or spawning models, record the unresolved property, why deterministic evidence is insufficient, affected scope, baseline requirement only if comparative, maximum total model runs, allowed parallelism, and observable stopping condition. An explicit evaluation request still needs finite limits. Ask for authorization where the experiment exceeds the task or spending authority. STATIC work creates no admission record, eval cases, baseline, or campaign workspace.

For launcher execution, persist this short record as JSON in the admitted campaign's workspace, not the skill source. Both runtime copies and all stages use the same absolute admission path and campaign-local ledger. Field contract:

| Field | Value |
| --- | --- |
| lane | FOCUSED_EVAL or FULL_EVAL |
| admission_basis | explicit_request or model_dependent_property |
| unresolved_property | Nonempty acceptance/comparison question |
| deterministic_insufficiency | Why existing/cheaper proof cannot answer that question |
| affected_scope | Nonempty list of affected surfaces |
| baseline | null when noncomparative; otherwise the required comparison and identified baseline |
| max_model_runs | Explicit positive integer, no unlimited value |
| allowed_parallelism | Positive integer no greater than max_model_runs; default choice is one |
| stopping_condition | Observable acceptance or inconclusive-stop condition |
| run_allocations | Stage-to-integer run limits whose sum does not exceed max_model_runs; query and improvement for the description launcher, other named stages only when admitted |

Allocate baselines, candidate samples, repetitions, retries, model graders, comparators, analyzers and improvement/shortening calls explicitly. Parallel execution changes scheduling, never total allowance. No implicit retry or replacement campaign resets consumed budget. A run is an evaluator invocation/attempt, not a token, internal provider request, or dollar amount. Report the enforcement boundary honestly.

## Evidence and stopping

Reuse valid evidence; rerun only a failed check or evidence invalidated by relevant changes. Source/twin parity, context compaction, session resume, new report formatting and unchanged baseline identity do not invalidate evidence. A baseline is needed only for a genuinely comparative criterion; do not create or rerun one simply because a skill changed. Fresh paired samples require an admitted comparison design.

Use existing representative cases first. New cases need a specific coverage gap inside an admitted campaign. Start focused; full model regression requires the broad-impact admission above. Deterministic grading precedes model grading. Parallel workers, model graders, blind comparisons and post-hoc analysis are optional admitted stages, not default steps.

Stop when the smallest sufficient evidence establishes acceptance. At the budget or stopping boundary, report unresolved or inconclusive results without adding runs. Do not expand verification because more confidence would be nice. Preserve actual failures and report unavailable measurements. Policy edits establish instruction changes, not measured token, cost, latency or runtime-compliance improvements.

## Routing and parity

Update registration only for affected catalog/routing inputs. Parser/path/schema checks, applicable lint, native discovery metadata and semantic parity remain required. Focused deterministic routing proof applies when routing metadata/behavior changes. Reserve the existing full deterministic routing corpus for router-engine/shared-scoring changes or a named broad-impact requirement. The local skill-eval.py is a deterministic router regression instrument, not a model behavioral eval. No routine change automatically appends routing or behavioral eval dataset rows.

The ordinary workflow is: capture intent → inspect existing authority → make smallest change → deterministic verification → update affected routing/registration → native parity → stop. Checks dependent on rebuilt artifacts run after their update. Reuse shared evidence and run only genuinely native-specific remaining checks.
