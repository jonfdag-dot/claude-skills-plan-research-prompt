# Challenge — the autonomous procedure, and the optional decision interview

Pulled in P6 for every serious candidate, and in P3 when the user asks for a guided decision interview. The default is autonomous challenge: a critique request is analysis, not an interview, and it should produce results without asking the user anything.

## The default procedure

Challenge the strongest version of the candidate, not a weak restatement of it. Identify the claim whose failure would change the decision, construct a realistic counterexample, and trace the resulting consequence. Distinguish an observed failure from an untested scenario. State the cheapest discriminating check, the possible repair, and whether the objection actually changes the recommendation.

Apply the same standard to the strongest competing option and to the incumbent. Challenging only the proposal produces a false preference for whatever is already there; challenging only the incumbent produces a false preference for the new thing. Both get the same outcomes, the same constraints, and the same scrutiny.

Update affected dependencies when evidence changes, and only those. Do not restart unrelated work, do not relitigate a consciously accepted tradeoff without new evidence, and do not require a user response when the analysis can continue under a stated assumption.

## The challenge record

Every challenge produces one row. An objection with no consequence and no discriminating check does not count against a candidate and does not belong in a risk list.

| Field | Content |
| --- | --- |
| Claim | The specific load-bearing claim under attack |
| Counterexample | The smallest realistic input, sequence, or state that breaks it |
| Consequence | What goes wrong for the user, the data, the money, or the decision |
| Evidence status | Demonstrated, plausible-untested, or contradicted by evidence, labeled per `epistemics.md` |
| Repair or test | The cheapest fix, or the cheapest check that would settle it |
| Verdict effect | Whether it changes the recommendation, narrows its bounds, or leaves it intact |

Repair before rejecting. A promising mechanism with a fixable flaw should be improved and re-tested, not discarded — the goal is the best available decision, not the highest objection count. Then name what would reverse your own position; a challenge you cannot imagine losing is not a challenge.

## What to attack

Choose by what the decision actually turns on, using the repertoire in `lenses.md` and the mechanism sections in `domain-expertise.md`. The classes that most often carry the decisive failure:

- **Missing or partial data** — what the system does when the required evidence is absent, restricted, stale, or contradicted, and whether that state is visible in the answer.
- **Ambiguity** — the input, question, or identifier that has more than one reasonable reading, and what the system does with it.
- **Stale state** — a cached, exported, or derived artifact that outlives the thing it was derived from.
- **Permission change** — revocation, role change, offboarding, and every derivative and serving path that must respond to it.
- **Recovery** — what a timeout, a partial write, or a failed external action leaves behind, and how it is reversed.
- **Scale and skew** — a much larger tenant, a hot partition, a burst, a much higher revision rate, lower cache reuse.
- **Adversarial incentives** — how a person, vendor, agent, or buyer could optimize the reported metric while harming the intended outcome.
- **A stronger future baseline** — what durable value remains when incumbent models, search, and platform features get much better and cheaper.

Worked examples of the shape, one per mechanism class:

- **Identification and grounded research:** two models agree after retrieving copies of the same caption. Test source lineage and independent identity evidence; agreement alone does not settle the claim, and two namers sharing a vendor or base model are one source wearing two hats.
- **Semantic computation:** two reasonable join paths return different totals for the same metric name. Test metric ownership, row grain, join cardinality, and the interpretation actually executed before judging the answer's fluency. A row cap and a read-only check constrain damage and prove nothing about correctness.
- **Event evidence:** a retry creates two delivery events, both enter separate chunks, and a summary reports twice the activity. Test delivery identity, deduplication, derivation lineage, and correction propagation together, because fixing one of the four leaves the bug.
- **Any mechanism with a cache or an export:** an answer remains accessible after the source's access changed. Trace the actual serving path and every derivative rather than accepting that an authorization component exists. An artifact already downloaded into someone else's environment cannot be recalled at all.

## The optional decision interview

Run this only when the user asks for a guided decision walk-through, or when interlocking choices genuinely need their decisions rather than your recommendation. It feeds the same decision register defined in `brainstorming.md`.

Map the decision tree silently first. Extract the settled facts, goals, constraints, and explicit exclusions; inspect the relevant files read-only before asking anything they answer. Include only material decisions — ones whose plausible answers meaningfully change the plan, its risks, or its implementation. Order the unresolved branches by dependency and impact, then walk them depth-first: resolve a parent before its children, finish newly unlocked children before returning to siblings, and do not exhaust a low-value branch merely because it is deepest.

Ask exactly one unresolved decision per turn and wait. Do not smuggle extra questions into a preamble, an option description, or a closing line. Always include your recommended answer and a one-sentence rationale — state a real opinion the user can concretely reject rather than hedging with "it depends" without resolving what it depends on. Use AskUserQuestion for named mutually exclusive choices, recommended option first, each alternative's description naming the condition under which it wins; use prose for open-ended or continuous answers. Treat a free-form or "Other" reply exactly like a typed one.

Process each answer by deciding whether it settles the decision, changes an earlier one, or opens a dependent branch. If it contradicts a settled constraint, leaves a material ambiguity, or accepts a serious avoidable risk, challenge it once with the concrete consequence and ask whether to accept that tradeoff — then respect a consciously accepted one. On "I don't know" or "you decide": apply your recommendation for a low-stakes choice and record it as an assumption; for a fundamental one, switch from interviewing to collaborating — compare the real options against the constraints and failure scenarios, recommend how to evaluate, settle it, then resume. Challenge the plan, never the person.

Keep three running lists — decisions with rationale, open material questions, and revisitable assumptions — recap them compactly about every five decisions and again whenever a changed decision invalidates downstream work. Stop when every material branch is resolved, the user says to wrap up, or the rest is genuinely safer to decide during implementation. If the user stops early, preserve the unresolved items rather than implying completeness. End with a self-contained synthesis: the plan as now understood, the decision record and rationales, the assumptions, the deferred questions with why and when to resolve each, and the material risks plus the validation needed before implementation.

## Delegating reconnaissance

Keep the challenge, the tree, the recommendations, and the running state on the main thread. When reconnaissance would traverse many files and flood context, spawn one focused read-only agent that returns only the relevant pattern in one or two sentences, the load-bearing paths, and the single fact that changes the next recommendation — under about 150 words, no code dumps. Do not delegate a one-shot search, a single named file, per-question fan-out, or judgment.
