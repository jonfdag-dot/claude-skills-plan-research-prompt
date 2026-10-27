# Prompt Optimization Guide

Use this reference to diagnose a prompt that misses a stated requirement. Begin with the failing input, current prompt, actual output, expected behavior, and relevant model/runtime guidance. A request to improve wording does not itself authorize model experiments or production rollout.

## Systematic Refinement Process

### 1. Baseline Establishment

Preserve the original prompt and deciding failure evidence. A measured baseline is needed for a comparative claim, not for every edit. Skill maintenance defaults to inspection and deterministic verification under the [canonical verification and eval admission policy](../../skill-creator/references/verification-and-eval-admission.md). Application experiments belong to the owning evaluation workflow and require the appropriate authorization and finite allowance.

### 2. Iterative Refinement Workflow

1. Identify the requirement the output violates and whether the cause is wording, missing context, conflicting instructions, an unsuitable example, formatting, or an application/tool failure.
2. Make the smallest change that addresses that cause while preserving user and host requirements.
3. Check the changed surface: template rendering, schema validation, required fields, source boundaries, or another applicable deterministic property.
4. If a model-dependent acceptance question remains and evaluation is admitted, compare on representative inputs with a declared grader and stopping condition. Preserve failures and report inconclusive results.

OpenAI's optimizer guidance emphasizes narrow graders and specific criticism, and warns that an optimized prompt can regress on particular inputs. These are useful design lessons; they do not establish improvement for a local workload or make the hosted optimizer a required tool. See [prompt optimizer guidance](https://developers.openai.com/api/docs/guides/prompt-optimizer).

### 3. A/B Testing Framework

For an admitted comparison, hold the relevant model/version, tools, input distribution, and generation settings comparable. Use matched inputs when the question is how two prompts perform on the same workload; a live randomized experiment requires its own deployment authority and design. Separate development examples from held-out evaluation items.

Declare required metrics, their direction, the unit of analysis, and what counts as a tie or inconclusive result before examining results. Higher accuracy and lower latency are different objectives. Do not select the best of repeated answers and label it single-attempt accuracy; any repeated-sampling procedure is a separate evaluated system with its own cost and budget. Route statistical analysis and workload-specific grading to the owning evaluation workflow.

## Optimization Strategies

### Token Reduction

Remove redundant wording only when meaning, authority, required context, and acceptance survive. Global text substitution can change quoted data or a required phrase; review the actual diff. Measure rendered input and output with the relevant tokenizer or provider usage when accounting is required. A shorter file or prompt does not prove lower total cost, latency, or better behavior.

### Latency Reduction

First identify whether time is spent rendering, waiting for tools, processing input, or generating output. Streaming changes when output becomes visible; caching and generation settings depend on the provider. Follow the relevant integration skill for those mechanics. A prompt change is successful only against the required quality and latency criteria, not whichever candidate returns fastest.

### Accuracy Improvement

Repair the observed failure specifically: clarify an ambiguous label, supply missing relevant context, demonstrate a difficult output convention, or express a required evidence boundary. For machine-consumed output, prefer an available native schema mechanism and validate both shape and task semantics. A general instruction to be accurate does not supply missing evidence. See [prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) and [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

## Performance Metrics

Use a task-matched grader. Exact label matching can assess classification; free-text answers need criteria for the requested content, support, and omissions. Keep format validity, task correctness, refusal, incomplete output, and tool failure distinguishable when they affect the decision. A nonempty response is not success.

Report actual sample scope and measurements. No repeated observation means consistency is unmeasured. Word counts are not token counts, and unavailable measurements remain unavailable. Choose repetition and uncertainty analysis only within an admitted experiment; do not invent a universal accuracy threshold or run count.

## Failure Analysis

For each deciding failure, retain the input, prompt/version, output or tool error, violated requirement, and smallest plausible repair. Distinguish missing evidence from contradictory evidence. If the prompt satisfies the contract but the application truncates the response or passes the wrong context, repair or hand off that cause rather than adding unrelated prompt instructions.

## Versioning and Rollback

Keep enough prompt/version identity to reproduce material failures and compare candidates. When an authorized production change is involved, preserve the owning application's release and reversal procedure. Prompt authoring alone does not add a deployment, branch, dashboard, or rollback deliverable. OpenAI documents prompt versioning as a tool for managing changes; see [prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering).

## Common Optimization Patterns

### Pattern 1: Add Structure

Replace “Analyze this text” with named criteria only when those criteria are the requested analysis. Headings or delimiters can distinguish instructions and supplied material; their presence is not a correctness or security guarantee.

### Pattern 2: Add Examples

Add a relevant demonstration when it explains the required behavior better than more prose or when admitted evidence supports it. Choose examples for the target model and workload using [few-shot-learning.md](few-shot-learning.md); do not append placeholder demonstrations.

### Pattern 3: Add Constraints

State a length, label set, schema, or evidence boundary when it preserves a stated requirement or is necessary for requested correctness. Do not invent exact word counts, output sections, or bans to make a prompt look precise.

### Pattern 4: Add One Concrete Check

For a task requiring an invoice total, “confirm the line items sum to it” expresses an observable correctness criterion. A model self-check remains a model output; use an independent calculation when that is the required evidence. Do not turn every task into a verification sequence.

### Pattern 5: Audit Compensating Instructions

Review instructions introduced for an older model against the current contract and guidance. Removing overprescription is model-specific advice, not evidence that fewer instructions always improve results. Preserve requested constraints and distinguish a wording correction from a measured behavioral change. See [GPT-6 Astra skill and prompt guidance](https://learn.chatgpt.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) and the qualifications in [sources-and-contradictions.md](sources-and-contradictions.md).
