# Research pipeline — purposes, packets, the host adapter, receipts, and stopping

Pulled whenever investigation is needed, at any effort level, and when the internal-capability scan needs delegation. This file owns research planning, source strategy, the host dispatch adapter, the receipt, and the rules for stopping research.

## Two purposes, both legitimate

Research serves a material decision or expands the credible options for that decision. Use either purpose at any effort level; neither requires escalation, and neither is a licence for an unbounded scan.

**Decisive-claim research.** Name the claim, its decision consequence, and the observation that could change feasibility, ranking, design, commitment stage, or the next experiment. Seek disconfirming evidence as deliberately as supporting evidence.

**Opportunity research.** Investigate a bounded question about a missing mechanism, an adjacent workflow, an emerging capability, or a better delivery surface. State what kind of alternative the search could reveal and what would count as adequate coverage of that question, so the scan has an end.

Load the relevant sections of `domain-expertise.md` before writing research questions. Domain expertise decides which questions are worth asking; without it the pass researches the wrong claims well.

Keep technical and business evidence distinguishable, but let each inform the other during the investigation rather than only at the verdict. A latency requirement, an onboarding burden, or a cost constraint can change the viable workflow and the viable architecture; discovering that after the research pass wastes the pass.

## Are you ready to research?

Before searching, check that you can name four things: the decision, the material claim or the kind of opportunity, the relevant scope, and an observation that would change the next step. If yes, proceed. If not, refine from the material already available — inspect the repository, the supplied documents, and the governing docs — and only then consider asking the user. Use this readiness condition instead of a numeric confidence score; a number that merely restates the condition adds false precision and no information.

## Research packets by mechanism

| Mechanism | The packet must establish | Strong primary evidence to seek |
| --- | --- | --- |
| Identification and source-grounded research | Exact task, input distribution, identity evidence, behavior on unknown cases, source independence, latency and cost assumptions | Official capability documentation; method papers with their task and dataset scope; labeled product cases; inspected responses and failure traces |
| Semantic computation and conversational analytics | Metric semantics, valid joins, the calculation path, ambiguity handling, effective execution identity and entitlements, schema-change behavior | Semantic contracts; official engine and protocol documentation; query plans and results; expert-reviewed representative questions; relevant evaluation research |
| Event evidence and analytical retrieval | Capture coverage, event and attempt identity, source-to-derivative lineage, retrieval versus complete aggregation, correction and revocation, operating cost | Actual instrumentation and source contracts; traces and event samples; official ingestion and storage documentation; retrieval research with comparable tasks; representative replay cases |
| Action across a trust boundary | Effective identity, token audience, consent, scope, idempotency, observed postcondition, recovery | The protocol or vendor specification at the version deployed; the authorization server's actual behavior; an inspected end-to-end trace |
| Business and form factor | The recurring task, the incumbent workaround, the buyer versus user distinction, deployment burden, adoption friction, the valuable improvement | Direct customer and workflow evidence when available; public studies with matching population and method; official product documentation for adjacent capabilities; task-based prototype observations |

External research never substitutes for customer evidence or repository inspection. When those observations are unavailable, the output is a scoped hypothesis or a proposed experiment, labeled as such. Pricing, limits, versions, and policy claims need their own current checks when they become consequential, and a versioned specification needs the version you are actually reviewing rather than whichever URL you saw first.

## Source strategy

Apply the `web-research` skill inline: query operators, source selection by claim type (its `source-tiers.md`), version and recency disambiguation, triangulation before trusting one page, fetch versus search, and its stop rule. Read beyond snippets. Stamp the retrieval date. VERIFIED follows web-research: a primary source that is the authority for the fact, or an independent second source, recorded through Corroboration; otherwise the claim ships marked single-source.

Treat any comparison page, best-tools list, or capability matrix published by a vendor as competitive intelligence about that vendor's positioning, never as evidence about the vendors it describes. Failure to find a public feature does not prove a rival lacks it; record UNKNOWN with the scope searched. Update the ledger as each receipt arrives, never in a batch at the end.

## Host adapter for delegation

Discover what this host actually provides before relying on any of it. Keep four things distinct, because their names are not interchangeable: an **analysis role** (a way of thinking), a **reference file** (text a worker can read), an **available tool**, and an **actual dispatchable agent target**. A role named in a table is none of the other three.

| Situation | Path |
| --- | --- |
| One to three claims, primary sources likely findable, the answer fits in a few fetches | Inline, at any effort level |
| Contradicting evidence must be hunted symmetrically, a landscape of alternatives or prior art is needed, or a plan carries many interacting claims | One or more read-only `worker-researcher` dispatches, when authorized |
| An internal-capability question across a docs or code tree | `Explore`, read-only, with the scan brief below |
| The idea is a skill | `skills-author-worker` |
| A project defines its own research command or governing research skill | That project's route governs; do not bypass an audited route with a bare command or an invented marker |
| The user explicitly opted in to multi-agent orchestration | The Workflow tool. That opt-in governs orchestration only; it is not a prerequisite for dispatching a single worker the host already permits |

If an optional worker or role file is missing, continue inline where permitted and state the coverage lost. Never invent an agent name, a thread limit, a model setting, or a shutdown capability, and never pass a per-call model or effort override. Authorization to delegate is a separate question from how much research is needed.

Design research systems with `llm-app-patterns` and reusable research-agent prompts with `prompt-engineering-patterns`. Use `web-research` for external evidence, relevant specialist skills for domain method, and the existing strong `worker-researcher` only for bounded independent research or a fresh challenge. The global and project research instructions govern evidence retention, synthesis and stopping.

Do not lift archived role prompts into a live workflow. A worker never sub-dispatches; the parent owns direction, synthesis and persistence, and the brief supplies the bounded question, retained evidence, scope, source expectations, competing explanations, falsifying evidence and required handoff.

## The dispatch brief

Route before dispatch per the host's orchestration rule, write the routing verdict as the first line, and pass paths and IDs rather than pasting a repository or a full plan.

```
Relevant skills: <installed skill paths and why they apply>
Decision frame: <actor, decision, trigger, consequence, stage>
Constraints that bind: <project fence items, by ID or path>
Purpose: <decisive-claim | opportunity>, with the question stated
Claims in scope: <C-IDs, each with its current label and falsifier>
Evidence requirement per claim: <the ladder row it must satisfy>
Role files to Read: <absolute paths>
Functional fallbacks: <the list above, with limits named>
Budget: <maximum fetches or minutes>    Stop rule: saturation or a named blocker
Output location: <scratchpad path>
Completion condition: every claim has a receipt, or an explicit UNKNOWN with how to obtain it
Receipt shape: <below>
```

A skill-selection note is not completion or research validity; require the evidence receipt. Track pending, active, completed, and blocked dispatches explicitly and recover from durable results rather than remembered narrative. Judge receipts against evidence, not reviewer count: agreeing workers are not independent verification, and two workers citing one page are one source. Resolve disagreement by finding the different evidence, assumption, or criterion — never by vote.

## The receipt

Per claim, compact but never truncated past the decisive content: claim ID; label with its rider; source (title, publisher or authors, URL or path, date or version, access date, locator); scope; baseline where applicable; method or operating conditions; limitation or conflicting evidence; the implication for the decision; and the remaining gap. A URL without the supported assertion is not a receipt. Keep the source locators so the main thread can inspect load-bearing evidence directly rather than relying on a compressed summary. Apply the size budget to the total requested output rather than as a per-hit allowance that multiplies, and never let a length limit drop a decisive contradiction or a scope condition.

## Stopping research

- Another retrieval is justified only when it could change an alternative's feasibility, ranking, design, commitment stage, or experiment.
- Stop a line of inquiry when every material claim in it is supported within scope, contradicted, or tied to a concrete missing observation that browsing cannot provide.
- Stop a line by web-research's rule: three consecutive queries yielding only already-seen material, or two substantive reframings without relevant evidence.
- A source count is never a quality proxy, and a reviewer count is never verification.
- An empty search is evidence about the scope searched. Report the paths, terms, and sources actually covered; two empty searches do not establish that a capability, competitor, or study does not exist.
- A research limit produces an explicit partial verdict — a test, a hold, or a bounded recommendation — never invented certainty and never an unsupported recommendation.
- A settled question reopens only on new evidence, a changed requirement, a changed dependency, or a failed acceptance condition. Record the old decision, the changed input, and the conclusions it affects.

## The internal-capability scan brief

Dispatch `Explore` with the project root, the paths from `knowledge-library.md` for that project, and the reserved vocabulary to grep. Ask for, per hit: the capability; its status from the six in `knowledge-library.md`; the path and line; the writer, the reader, and the gate or flag that exposes it; and one sentence on what activating it would actually take. Under 150 words per hit, no code dumps. Ask explicitly for the paths and terms searched, because a negative result is evidence only within them.
