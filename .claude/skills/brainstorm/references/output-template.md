# Output template — presenting the decision, proportionally

Pulled when the deliverable is prepared. The record is sized to the decision, not to the template. Include a section only when it has content; never fill one for symmetry.

## Inline or on disk

An inline answer is a complete deliverable when no durable artifact was requested and the verdict is consumed in the conversation. Write a file when the verdict outlives the turn, when the user asks for one, or when the project's convention requires a record for this kind of decision. When you write one, use the landing home defined in `knowledge-library.md` — that file owns the landing rule — and report the actual path after the file exists, never before.

An unfinished record and a completed analysis with unresolved product questions are different things. Say which one you are handing over.

## The compact record

Use this for Quick work and for bounded Standard work. It carries the whole reasoning floor.

```markdown
# Decision: <question>

Verdict: <one of the five>
Commitment and scope: <stage, affected product or task, bounds>
Recommendation: <preferred next step and the strongest reason>

## Evidence and limits
<Load-bearing observations, inferences, and unknowns, each labeled. Source locators. Repository or deployment scope with its date or revision.>

## Comparison and challenge
<The strongest credible alternatives on the same outcome. The strongest objection, its evidence status, and its decision consequence.>

## Domain result
<Only the decisive domain checks, their outcomes, and any remaining blocker.>

## Next commitment
<The experiment or the change brief, proportional to the recommendation. What would reverse the verdict, and who owns any unresolved decision.>
```

## The full record

Expand to this only when the decision needs it: many interacting claims, a large commitment, a repository-wide pressure test, or a handoff that must survive without the conversation. Keep the order.

```markdown
---
status: in_progress
created: <YYYY-MM-DD>
completed:
mode: <GENERATE or PRESSURE-TEST or LEVERAGE>
effort: <Quick or Standard or Deep>
stage: <discovery or prototype or pilot or production>
verdict: <the one chosen verdict>
project: <project name>
readiness: <Ready for Planning or Needs More Exploration>
---

# Brainstorm: <idea or plan name>

## Verdict
<One verdict and the strongest reason, in two or three sentences. Name the alternatives compared, the stage, and the evidence that would reverse it.>

## Problem frame
<Actor, recurring decision, trigger, consequence, current workaround. User, buyer, approver, affected person, and action owner where they differ. The constraint table: required outcomes, hard limits, negotiable constraints, assumptions, each with origin and owner.>

## Capability map
| Capability | Status | Path | Affected | Activation cost | Note |
| --- | --- | --- | --- | --- | --- |
<Statuses from knowledge-library.md. In PRESSURE-TEST, each row is affected, unaffected with a reason, or not assessed. Reserved and dormant capabilities carry the gate that exposes them and what activating them would take. Never-list or kill-register items the idea touched, with the register and the reopen trigger.>

## Claim ledger
| ID | Claim | Label and rider | Decision consequence | Evidence | Falsifier |
| --- | --- | --- | --- | --- | --- |

## Alternatives
| Candidate | Mechanism | Decisive advantage | New burden | Strongest objection | Cheapest test |
| --- | --- | --- | --- | --- | --- |
<The current workflow, the simplest adequate improvement, a buy-or-compose option, and a materially different mechanism appear here or are dismissed with a reason. State the preference boundary: the scenario in which the ranking flips.>

## Challenge results
| Claim | Counterexample | Consequence | Evidence status | Repair or test | Verdict effect |
| --- | --- | --- | --- | --- | --- |
<Plus the competing-hypotheses matrix, failure mechanisms with leading indicator and containment, the removal-test result, gaming scenarios, and architectural scenarios, where the decision needed them.>

## Domain result
<The decisive checks from the domain-expertise.md sections that applied, with outcomes and remaining blockers. This is where expertise reaches the verdict rather than sitting in a reference file.>

## Feasibility vector
| Axis | Status | Stage judged against | Scope and evidence |
| --- | --- | --- | --- |
<Only the applicable axes. NOT APPLICABLE with the stage named is a correct result. A decisive failure is stated as such and never averaged.>

## Customer, economics, form factor
<Only when the idea makes a demand, cost, or surface claim. Benefit categories separate; price inputs dated; the baseline and its conditions named; latency measured end to end or labeled inference; surfaces compared on identical tasks and evidence.>

## Experiments and missing inputs
<Ranked. Each in the template from rules-engine.md, with its state: proposed, running, passed, failed, inconclusive, or blocked.>

## Change brief
<RECOMMEND WITHIN BOUNDS and TEST BEFORE COMMITMENT only, and scaled to the actual change.>

## Sources, checks, and reopen conditions
<Every source with its date, version, and locator. Which checks were run and which kind each was, per the three kinds in rules-engine.md. Unresolved risks. The conditions under which this verdict reopens.>

## Decision register
| ID | Decision | State | Rationale or open question |
| --- | --- | --- | --- |
<Confirmed, Recommended, Assumption, TBD. Open rows are what planning resolves first.>

## Parking lot
<Tangential ideas worth revisiting, one line each.>

## Handoff
<Planning, an ADR, a register update, or nothing, with the reason.>
```

Choose actual values in the frontmatter. Never emit the pipe-separated option list as if it were a value.

## The domain result, by mechanism

This is the section that makes expertise change the verdict. Report only the decisive checks.

| Mechanism | What the domain result must state |
| --- | --- |
| Identification and source-grounded research | The identity task and its scope; error and coverage evidence together; source independence after grouping by origin; grounding or abstention behavior; the dominant cost or latency limit |
| Semantic computation and conversational analytics | The metric interpretation actually executed; computation and join validity at the stated grain; the effective execution identity and the entitlement boundary; the evidence linking the question to the returned number; the tool, export, or action scope where relevant |
| Event evidence and analytical retrieval | The capture boundary and its coverage gaps; request, attempt, and event identity; source-to-derivative lineage; retrieval versus complete computation for the question class; correction and revocation reach; the surface comparison where one is claimed |
| Action across a trust boundary | The effective identity and its entitlement at each hop; what the action changes; idempotency; the observed postcondition; the recovery path |
| Graph of any kind | Which graph is meant; what one edge records; and what the claimed success in one layer does not establish about the others |

## The change brief

For a change that merits planning, state the affected behavior and contracts, the producers and consumers, the data or semantic migration, the compatibility window, the permission implications, observability, the rollout sequence, recovery, and ownership. Scale it to the actual change; a small change gets a short brief.

Ask the migration question in the form the mechanism demands. Does a new identity strategy change persisted identifiers, evidence records, cache keys, correction behavior, or already-published results? Does a semantic definition change invalidate saved queries, conversations, dashboards, tool contracts, exports, or permissions — and can an artifact already downloaded into someone else's environment be invalidated at all? Does a new chunker or embedding model require reprocessing, version coexistence, lineage updates, index invalidation, or reconciliation of historical results?

A rollback of application code does not necessarily restore earlier data semantics and does not reverse an external action. Require a concrete recovery strategy for the effect being proposed. This brief defines that strategy; it does not authorize execution.

For TEST, write the experiment's integration requirements rather than a production design. For REFRAME OR REDESIGN, provide enough of the alternative mechanism to make it reviewable. For REJECT or HOLD, do not elaborate implementation detail the verdict does not justify.

## Finishing

Run the record review in `rules-engine.md` once, on the finished content, then present in this order: the verdict and its strongest reason, the open decision-register rows, and the landing path if a file was written. Offer the handoff the verdict justifies and nothing more.
