# Sources, Contradictions, and Dropped Claims

The evidence base for this skill. Use the source matching the technique and target model; a documented recommendation is not a measured benefit for the local skill.

## Tag legend

| Tag | Meaning |
|---|---|
| [DOC] | Supported by an inspected primary or first-party source, with model, task and date qualifications preserved |
| [OPINION] | Historical design opinion; not an established technique or authority to add work |
| [POLICY] | The owner's standing rule for this machine; binding inside this skill, never cited as a vendor claim |
| [UNVERIFIED] | Circulating claim with no primary source located; recorded for reference only, and it never directs behavior, sets a limit, or defines an API contract |
| DROPPED | Claim removed because no source supports it. Do not reintroduce without a live primary page |

## Current technique decisions: 2026-10-09

These sources were inspected for the 2026-10-09 research update. The older orchestration inventory below remains historical and was not comprehensively reverified. The private source reports are outside this export; the original-source pointers and scoped summaries are retained below. The 2026-10-10 authoring refinement reuses this evidence; it does not advance source inspection dates or establish measured improvement.

| Source | Supported use and limits |
| --- | --- |
| [OpenAI GPT-6 guidance](https://developers.openai.com/api/docs/guides/latest-model), living documentation | Remove hypothetical approval flows; use proportionate checks. These recommendations do not eliminate real authority or acceptance requirements. |
| [OpenAI GPT-5.5 guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5), model-specific view | Preserve the product contract while reducing procedure. Outcome-oriented prompting includes relevant stopping and missing-evidence behavior. GPT-5.5 retires from ChatGPT and Codex with ChatGPT sign-in on 2026-10-14 (API unaffected); apply this view only to API workloads still on GPT-5.5. |
| [Eric Provencher, OpenAI](https://learn.chatgpt.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), 2026-09-11 | Reassess inherited skill instructions; load references by task. Guidance concerns Astra and does not measure this skill's improvement. |
| [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning-best-practices), primarily o-series examples | Start with direct instructions; examples and explicit reasoning are conditional. Do not mistake this for a ban on useful explanations or task planning. |
| [Claude prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), living documentation | Clear instructions, representative examples, delimiters and long-context placement are provider guidance; example counts are not universal optima. |
| [Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) and [Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5), living documentation | Opus guidance removes generic verification scaffolding; Sonnet low-effort guidance adds a runnable check when needed. Neither supports a universal verification ban or mandate. |
| [Gemini prompt design](https://ai.google.dev/gemini-api/docs/prompting-strategies), updated 2026-09-17 | Its Gemini 3 template includes validation. Examples and reasoning instructions vary across the page's model generations; adapt the relevant section. |
| [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), Step 3 | Schema adherence does not establish correct content. Incompatible input, refusal and incomplete output require appropriate handling in the consuming application. |
| [Anthropic indirect-injection guidance](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection) | Distinguish external data from instructions when external content is processed. Wording and delimiters do not replace host controls. |
| [Many-Shot ICL](https://arxiv.org/html/2404.11018v3), v3 2024-10-17 | Example count, repetition and ordering effects depend on task; historical long-context experiments do not establish a current universal count. |
| [To CoT or not to CoT?](https://arxiv.org/html/2409.12183v3), v3 2025-05-07 | Gains concentrate in symbolic tasks in the studied benchmarks; this does not establish optimal prompting for today's reasoning agents. |
| [GEPA](https://arxiv.org/pdf/2507.19457v2), v2 2026-02-14 | Feedback-driven optimization has held-out benchmark support and task exceptions. Fewer rollouts is not measured wall-clock or dollar savings. |
| [MOSAIC](https://arxiv.org/html/2601.18554v1), 2026-01-26 | Constraint interactions and load affected synthetic generation on November 2025 models. No universal fifteen-rule budget follows. |
| [GSM-Symbolic](https://arxiv.org/html/2410.05229v2), v2 2025-08-27 | Distractors harmed historical math-task performance; neither universal brevity nor a general inability to reason follows. |

The proposed rule allowing only user/document/host-origin checks is **not established as a universal best practice**. Preserve faithful rewriting and omit invented workflows, while allowing an instruction necessary for the requested task or interface. A supplied document can contain task facts or untrusted text; it is not automatically an authority. Category-removal fidelity and optional cautions outside the artifact are owner choices, not measured techniques.

Do not promote a self-rated confidence threshold, fixed example count, rule-count ceiling, universal role persona, fixed context allocation or automatic model-evaluation loop to a default. The local references remove those unsupported prescriptions. Their absence is not a claim that every variant is ineffective; adoption needs applicable evidence or an explicit user requirement.

## Historical source inventory

Fetched and read on 2026-08-16, except rows marked 2026-09-15 or 2026-09-16. Provider guidance is model-scoped and is not measured improvement for this skill.

| Source | URL | Page date |
|---|---|---|
| Effective context engineering for AI agents | anthropic.com/engineering/effective-context-engineering-for-ai-agents | not confirmed on-page |
| Effective harnesses for long-running agents | anthropic.com/engineering/effective-harnesses-for-long-running-agents | November 26, 2025 (stated on page); rechecked 2026-09-16 |
| How we built our multi-agent research system | anthropic.com/engineering/multi-agent-research-system | June 13, 2025 (stated on page) |
| Writing effective tools for AI agents | anthropic.com/engineering/writing-tools-for-agents | not confirmed on-page |
| Orchestrate subagents at scale with dynamic workflows | code.claude.com/docs/en/workflows | undated (living doc) |
| Introducing dynamic workflows in Claude Code | claude.com/blog/introducing-dynamic-workflows-in-claude-code | undated |
| Subagents | code.claude.com/docs/en/sub-agents | undated (living doc) |
| Best practices for Claude Code | code.claude.com/docs/en/best-practices | undated (living doc); rechecked 2026-09-16 |
| Agent Skills overview | platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | undated (living doc) |
| OpenAI, Model guidance (GPT-5.5 and GPT-6 Astra views) | developers.openai.com/api/docs/guides/latest-model | checked 2026-09-15 |
| OpenAI, Reasoning best practices | developers.openai.com/api/docs/guides/reasoning-best-practices | checked 2026-09-15 |
| Google, Gemini prompt design strategies | ai.google.dev/gemini-api/docs/prompting-strategies | checked 2026-09-15 |
| Anthropic, Prompting best practices | platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | checked 2026-09-15 |
| Choose a permission mode | code.claude.com/docs/en/permission-modes | undated (living doc); checked 2026-09-16 |
| Keep Claude working toward a goal | code.claude.com/docs/en/goal | undated (living doc); checked 2026-09-16 |
| Harness design for long-running application development | anthropic.com/engineering/harness-design-long-running-apps | March 24, 2026 (stated on page); checked 2026-09-16 |
| GitHub Spec Kit clarify and converge command templates | github.com/github/spec-kit/tree/main/templates/commands | undated (main branch); checked 2026-09-16 |
| OpenSpec, editing changes | github.com/Fission-AI/OpenSpec/blob/main/docs/editing-changes.md | undated (main branch); checked 2026-09-16 |
| From Plan to Action: How Well Do Agents Follow the Plan? | arxiv.org/abs/2604.12147 | v3 2026-08-07; checked 2026-09-16 |
| Specification Grounding Drives Test Effectiveness for LLM Code | arxiv.org/abs/2607.06636 | v1 2026-07-07; checked 2026-09-16 |
| Anthropic, Prompting Claude Opus 5 | platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | undated (living doc); checked 2026-09-30 |
| Anthropic, Prompting Claude Opus 5.5 | platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 | undated (living doc); checked 2026-09-30 |
| Anthropic, Prompting Claude Sonnet 5.5 | platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 | undated (living doc); checked 2026-09-30 |
| Anthropic, Prompting Claude Fable 5.1 | platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | undated (living doc); checked 2026-09-30 |

The runtime documentation pages in this inventory are living sources. Version-pinned observations from prior inspections can drift; re-fetch before relying on a runtime mechanism or availability claim.

## Contradictions, un-smoothed

These comparisons record the historical inspections above, including qualifications that prevent overgeneralization. They are not current runtime instructions; use the dated technique decisions above for this skill's adopted guidance and recheck older mechanics when a task needs them.

**1. Is compaction sufficient for continuity?** The mechanisms are complementary, not opposite. The context-engineering post describes compaction, with tool result clearing as "the safest lightest touch form", and also structured note-taking. The long-running-harness post found compaction alone insufficient for its multi-session experiment: it "doesn't always pass perfectly clear instructions to the next agent", so state lived in files and git. Current prompting best practices add that when a window is cleared, "consider starting with a brand new context window rather than using compaction." Compaction within a session; persistent artifacts for anything consequential across a boundary, and only for tasks that cross one.

**2. How many agents is too many?** Three mechanisms, three numbers, none of them "the limit". The multi-agent post prescribes "3-5 subagents in parallel" as the shipped pattern and "more than 10 subagents with clearly divided responsibilities" for complex research, with no ceiling. The dynamic-workflows docs cap a run at 16 concurrent and 1,000 total agents, with an advisory warning above 25 agents or 1.5 million projected tokens. The subagents docs cap a session at 20 concurrently running subagents. Quote the one that matches the mechanism you are using.

**3. Which model should a subagent run?** The multi-agent post reports its result with "Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents". Best practices says to "Control costs by routing tasks to faster, cheaper models like Haiku". The subagents docs document a `model` field and a four-step resolution order. A host project may forbid all three: where a hook or policy pins subagent models, a per-invocation `model` parameter is denied rather than downgraded, and the correct dispatch passes no model parameter at all. Host policy wins because it is enforced, not because it is better reasoned.

**4. Can subagents spawn subagents?** The subagents docs say nesting is on by default, "up to three layers below the main conversation", with the `Agent` tool withheld only at the depth limit. Many host configurations forbid it outright in the worker definition. Both are true at once; check the definition you are dispatching before assuming either.

**5. Does prompt formatting matter?** Three different scopes, three different answers, and collapsing them into one rule is the error. For prompt sections, the context-engineering post hedges formatting away: XML or Markdown to delineate, "although the exact formatting of prompts is likely becoming less important as models become more capable." For tool responses, the tools essay says structure measurably matters: "Even your tool response structure, for example XML, JSON, or Markdown, can have an impact on evaluation performance: there is no one-size-fits-all solution." For agent-editable state files, the harness post makes a behavioral claim in favor of JSON: "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."

**6. Does the multi-agent result transfer to coding?** The page publishing the 90.2% figure also warns that "most coding tasks involve fewer truly parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to other agents in real time." The coding-specific harness post declines to answer: "It's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture." Any use of 90.2% in a coding context carries both caveats or it is misusing the number.

**7. Which plans get dynamic workflows?** The workflows docs say they are "available on all paid plans, with Anthropic API access, and on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry". The launch blog says they are "on by default for Max, Team, and Enterprise plans, and when using Claude Code via the API. Pro plan users can enable them in /config", and names Vertex AI where the docs name Google Cloud's Agent Platform. Neither page reconciles the other.

**8. Should a prompt start with examples, and should it script reasoning?** Scoped by provider, never one recipe. OpenAI, for reasoning models: "Try zero shot first, then few shot if needed" and "Avoid chain-of-thought prompts". Google, for Gemini: "We recommend to always include few-shot examples in your prompts." Anthropic, for current Claude models: a few well-crafted examples improve accuracy and consistency, and with thinking on, "Prefer general instructions over prescriptive steps", with manual chain-of-thought as the fallback when thinking is off. Choose by the target model and the task. A local exception is recorded here as: observed failure, applicable guidance, proposed wording, local evaluation status.

**9. How much procedure should a prompt carry?** Match procedure to the task and model. OpenAI's outcome-oriented guidance preserves relevant constraints and completion conditions. Astra and Opus 5 guidance warns against inherited over-verification, while Sonnet 5.5 at low effort may need an explicit runnable check. These are model-scoped recommendations, not a universal direction toward fewer instructions. They support selective inclusion under the root's grounds rule.

## Dropped claims

These circulate widely and are not in any page fetched for this update. They were removed rather than softened.

- **DROPPED: "`ultrathink` was deprecated in v2.0.x and re-introduced as a per-turn keyword in v2.1.68."** The best-practices page contains no occurrence of `ultrathink`, `think hard`, `think harder`, `megathink`, `extended thinking`, `thinking budget`, or any thinking-effort keyword. No fetched page carries the version history. A version-pinned mechanism claim with no primary source is not a directive.
- **DROPPED: "`ultracompact` is a command."** It appears in neither the best-practices command list nor the workflows command list. A skill that names a nonexistent command teaches a failing keystroke.
- **DROPPED: "Ultra Code Mode" as a product name.** Anthropic's term is dynamic workflows, and `ultracode` is the setting.

## Claims rescoped rather than dropped

- **"Verification is the single most impactful practice in Claude Code."** The superlative has no ranking behind it; the page publishes no comparison or metric. What it does say is directive enough on its own: "Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it", and "show evidence rather than asserting success". This skill quotes those and drops the ranking.
- **"Context rot: performance degrades non-uniformly as input length grows."** No source for the term or its attribution was fetched here. The Anthropic-sourced form is different and weaker: an "attention budget", context as "a finite resource with diminishing marginal returns", and the n-squared attention justification. Use those.
- **"Curate 3 to 5 canonical examples."** Sourced: Anthropic's prompting best-practices page recommends 3 to 5 relevant, diverse examples wrapped in `<example>` tags, or `<examples>` for a set (re-read 2026-09-30; research library R-7372). The context-engineering post adds "a set of diverse, canonical examples" and, on stuffing edge cases, "We do not recommend this."
- **"Ultracode sends xhigh to the model."** The sourced wording is that it "combines `xhigh` reasoning effort with automatic workflow orchestration". No page describes the transport mechanism, defines `xhigh`, or states what effort a keyword-triggered workflow's agents run at.
- **"A subagent returns a 1,000-2,000 token summary, so the report has a required shape."** The historical range does not establish required fields, sections, or enforcement. Current brief references carry the accepted task or host return contract; they do not derive a schema from that range.

## What the sources still do not answer

These questions were unresolved by the historical sources. Current references carry the accepted task and host contract and defer execution design to its owning skill; these gaps do not authorize invented rules.

1. How long a dispatch brief should be, and the trade between a brief that eats the worker's budget and one so thin the worker re-derives context.
2. What goes in a brief beyond four nouns (objective, output format, tool and source guidance, task boundaries). None of the four is further defined anywhere.
3. The shape of a return contract, and what to do when a worker returns prose instead.
4. Worker failure policy: retries, timeouts, escalation, partial results, unusable returns.
5. Overlap and deduplication between siblings. Duplicated work is named as a real failure; the only prescribed remedy is "clearly divided responsibilities".
6. How to choose a fan-out size for a real task, given three incompatible ceilings and no per-agent token budget.
7. How a brief should evolve across a long multi-session run.
8. Adversarial verification mechanics: verifier ratio, voting rule, convergence criterion, confidence threshold.
9. Whether the measured multi-agent research win transfers to coding at all. Both relevant pages decline to claim it.

## Owner policy

Every [POLICY] rule in `SKILL.md` traces here; change it here first.

- **Do not add work merely because it could improve the result; a prompt may clarify scope but must not create scope.** Owner policy, supported in direction by contradiction 9.
- **Grounds, removal fidelity and optional cautions.** Preserve stated or governing requirements and task-essential correctness; omit invented approval workflows and speculative extras. Remove requested categories without substituting equivalent restrictions. Explain a real host conflict outside the artifact. This is the adopted authoring policy; the proposed strict provenance-only prohibition was not supported.
- **Material clarification.** Ask focused questions only when missing information changes the result; related questions may be grouped, and only dependent work waits. This replaces the unsupported one-question-at-a-time requirement. It is local authoring policy, not a measured optimum.
- **Flexible prompt content.** Convey the outcome, relevant context, applicable requirements, required method and meaningful completion condition. These are selection aids, not mandatory headings or an ordered template. Honor the requested output format; preserve exact wording when a surgical edit is requested.
- **Conditional brief fields.** Include dependencies, handoff identities, stopping rules, review labels and return schemas only when the accepted task or consuming workflow uses them. Structured-output guidance distinguishes constrained generation, local validation and factual support.
- **The carry rule and the repository-vocabulary rule.** Owner policy, derived from two incidents on 2026-09-15: a brief that produced 115 tool calls and no edits, and a builder that copied its session's git state into a later-session prompt against an explicit user limit. Plan of record: the claude plan library entry `2026-09-15-prompt-engineering-patterns-scope-discipline.md`.
- **Description form.** This machine's `skill-creator` canon (third person, "Use when", "Not for → use Y", ≤1024 characters). The refinement preserves existing discovery metadata; historical routing checks do not establish current prompt behavior.
