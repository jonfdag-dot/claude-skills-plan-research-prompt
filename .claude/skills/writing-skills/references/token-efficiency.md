# Resource selection and optional compression

Select this reference when dividing a skill between its entrypoint and resources, or trimming content within a requested scope. It is authoring guidance, not a model-evaluation or telemetry workflow.

## Loading model

Native discovery advertises metadata; a selected or explicitly preloaded body and supporting references have separate loading stages. A frequently referenced skill does not automatically load its full body every conversation. Inspect the actual host when a version-sensitive loading claim matters.

Word counts and file sizes describe an artifact, not live token consumption, billing, latency or outcome quality. Do not infer measured savings from shorter text or sum every file on disk as if it loaded.

## Selective structure

Keep the capability, inputs, output, failure behavior, permission boundaries and commonly needed decisions in the entrypoint. Put lengthy domain or provider variants in separate references with explicit selection reasons. Give long references navigable sections. Avoid a mandatory chain through unrelated skills or resources.

Cross-reference an existing owner rather than copying its manual. Distinguish a pointer's purpose from its load requirement:

```markdown
Select the migration reference when the requested change alters stored data; it describes compatibility and recovery checks.
```

When a tool's help is the right source for current flags, link the verified tool and ask for the relevant help rather than duplicating a large option catalog. Preserve the exact flags required for the task and any safety-critical defaults.

## Optional compression heuristics

Earlier local guidance proposed under 150 words for a getting-started workflow, under 200 words for a frequently loaded skill and under 500 words for another compact skill. These are optional size heuristics without local workload calibration. They do not override the required contract, examples, failure handling or native metadata.

Remove repetition whose owner is already reachable. Keep one representative example when it covers the capability; use additional examples only for a meaningful boundary. A reusable template or a detailed reference is appropriate when the task needs it.

Do not trim conditions merely to make prose shorter. An instruction can become smaller and less correct. Review the capability/caller mapping and preserved constraints rather than treating word count as the acceptance measure.

## Verification

Use parser, link/path, owned diff and native parity checks appropriate to the change, under the [canonical verification policy](../../skill-creator/references/verification-and-eval-admission.md). A word count can confirm an explicitly requested size target; it does not prove effectiveness. Reuse valid checks and stop after the requested contract passes.
