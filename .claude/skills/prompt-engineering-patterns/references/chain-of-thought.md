# Reasoning Guidance

Choose reasoning instructions for the target model and task. OpenAI's o-series guidance recommends direct prompts and avoiding chain-of-thought instructions; this is provider guidance for that model family, not proof that every model performs every task better without scaffolding. See [reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices) and the model-specific qualifications in [sources-and-contradictions.md](sources-and-contradictions.md).

## Reasoning and the response contract

- Specify the required answer, evidence, constraints, and observable acceptance. Request a concise justification or calculation when the user or downstream consumer needs it; do not request private chain-of-thought.
- Use a concrete check when it is necessary to the requested correctness, such as confirming invoice line items sum to the reported total. A model's claim that it checked something is not independent verification.
- Audit scaffolding against the current task and model guidance. Preserve governing requirements; remove an instruction only when it is redundant, unsupported, or causes an observed failure. Model-specific advice to simplify prompts is not permission to discard the user's constraints. See [GPT-6 Astra skill and prompt guidance](https://learn.chatgpt.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

Use inspection and deterministic checks first. A model comparison requires admission and a finite run allowance under the [canonical verification and eval admission policy](../../skill-creator/references/verification-and-eval-admission.md).

## Conditional techniques

These are design options, not default instructions or established improvements for the current workload:

- **Worked examples:** demonstrate the task's required output or an observable calculation. Choose representative examples without copying an evaluation item's expected answer into its prompt.
- **Decomposition:** expose real dependencies or intermediate artifacts when later work needs them. Do not impose a universal sequence on an executor that can choose its own method.
- **Repeated sampling:** an admitted application experiment may compare independent answer samples and an aggregation rule. Correlated wrong answers can agree; agreement does not establish truth. Count every sample and any model-based judge within the admitted allowance.

Keep the delivered response as concise as the task permits. Separate the model's internal computation from the explanation the user needs.
