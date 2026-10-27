# Clarification and the decision register

The discipline that keeps consequential choices visible and hands them off cleanly to whatever plans the work. Pull it when the idea carries interlocking choices, when a durable handoff is needed, or when the user asks for guided discovery. Pair it with `challenge.md` when those choices should be stress-tested one at a time.

## Ask only what changes the answer

Inspect first. Never ask the user for what the material already answers, and never ask to fill a category that happens to be empty. A question is justified by its effect on a decision or on the authorized next step — not by its category, and not by the format of an interview.

Ask for information only when the answer could materially alter the recommendation or the next step. Otherwise proceed with a named assumption or a conditional recommendation, and say which. An autonomous critique can contain zero questions and still be complete. The two-to-four-questions-per-round format belongs to an actual interview the user asked for, not to every pass.

Respect standing delegation. "Use your judgment" means recommend the consequential choice with its decisive tradeoff and continue; it does not mean every datastore, vendor, or hosting decision becomes a permission checkpoint. Obtain authorization at the real commitment boundary, not at every topic.

## Separate what the user chose from what the system does

These are different kinds of fact and they live in different places.

- A user's stated preference is evidence of their preference. It is not a claim about any system, and it does not need a source. It belongs in the **decision register**.
- What a document specifies, what code does, and what a vendor publishes are claims about the world. They belong in the **claim ledger** with a label from `epistemics.md`.

The confusion between them is expensive in both directions: "the architecture doc specifies PostgreSQL" is not user approval of a new PostgreSQL migration, and "the user prefers PostgreSQL" is not evidence that PostgreSQL is deployed.

## The decision register

Use stable IDs when decisions interact or when the record must survive the conversation. A three-sentence recommendation does not need two registers and a parking lot — do not manufacture structure for a small answer.

Give every decision an ID (D01, D02…), never renumber, and add IDs only when a new answer exposes a genuinely new decision. Each decision carries exactly one state:

| State | Meaning |
|-------|---------|
| **Confirmed** | Explicitly agreed by the user, or established directly by an applicable governing document |
| **Recommended** | Your current practical default, not yet confirmed |
| **Assumption** | Provisionally inferred, safe to revisit |
| **TBD** | Unresolved and material |

Cover only the relevant categories: goal, non-goals, and users; scope; approach and alternatives; data and state; dependencies and integrations; risks and failure modes; validation. Update after each meaningful answer or research finding. Never silently settle a consequential choice — recommend a default, name its decisive tradeoff, and either confirm it or leave it TBD. Keep a parking lot for tangents so they are preserved without derailing the pass.

## The claim ledger

One row per material claim: ID, the claim, its label and rider from `epistemics.md`, the decision consequence, the evidence needed or found, the source when known, and the falsifier. Prioritize the claims whose failure would change whether, what, or how to build. A claim whose resolution cannot move the verdict is recorded UNKNOWN with how it could be obtained, and then left alone.

## Ask well when you do ask

- Named, mutually exclusive choices (2 to 4) → **AskUserQuestion**, recommended option first, its one-sentence tradeoff stated. Treat "Other" or free-form exactly like a typed answer.
- Open-ended or continuous answers → prose, referencing the decision ID.
- Accept "unknown", "TBD", or "all your defaults" and record accordingly.

Stop as soon as the remaining uncertainty can be documented honestly without blocking a useful outcome.

## Recommend a coherent default

When the user has not decided, propose a primary recommendation rather than making them invent requirements. Prefer defaults that are well-supported, simple and proportionate to the real scale, coherent across the whole idea, and reversible where uncertainty is high. Keep mainstream options as candidates but do not privilege them: a less familiar approach with a relevant, testable advantage deserves a fair statement and a cheap discriminating test rather than dismissal. Offer an alternative only when it is a material tradeoff, and state the condition under which it wins. Avoid speculative abstraction and premature structure.

## Quality bar

Before handing off, verify that evidence, confirmed decisions, recommendations, assumptions, and TBDs are distinguishable and nothing unresolved is presented as settled; that the recommendation is coherent end to end; that every risk and every unconfirmed consequential default is called out; and that a future agent or the planning step can see what to decide next without replaying the conversation.
