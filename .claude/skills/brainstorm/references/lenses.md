# Lenses — Socratic categories, the repertoire, transformations, form factors, and the candidate card

Pulled in P3 for the Socratic categories, in P4 for the transformations and the candidate card, and in P6 for the repertoire. Use a lens because the decision needs it; never run every lens on every idea. Each lens is a working procedure with an inspectable output, not a persona and not a request for private reasoning. Substantive domain method lives in `domain-expertise.md` and project fences live in `knowledge-library.md`; this file holds the general reasoning tools.

## Socratic categories (P3)

| Category | Purpose | Stems |
| --- | --- | --- |
| Clarification | Mutual understanding of the core idea | What do you mean by X? What would this look like in practice? When did this last actually happen, and what was done? |
| Assumption | Surface hidden dependencies | What must be true for this to work? What happens if that is not true? Is this always the case, or are there exceptions? |
| Evidence | Ground claims in verifiable information | What supports this? What contradicts it? What would change your mind? Where has this worked or failed before? |
| Perspective | Explore stakeholders and blind spots | How would the buyer, the approver, and the affected person each see this? What would a critic say? What are we not seeing? |
| Consequence | Understand downstream effects | What happens if this succeeds? If it fails? What are the second-order effects? What else changes? |
| Meta | Question the question | Is this the right problem? Symptom or cause? What are we optimizing for? Is this worth solving now? |

These are categories for your own analysis first. Use them to interrogate the material, and put a question to the user only when the answer would change the recommendation. When the user has asked for a guided interview, pace it per `brainstorming.md`: prefer what and how over why, build each question on the last answer, acknowledge an insight before probing it, and never ask for what the material already answers.

## The repertoire

| Lens | Phase | Procedure | Required output | Failure it counters |
| --- | --- | --- | --- | --- |
| Problem reframing | P1 | Remove the proposed technology from the problem statement. Identify actor, decision, trigger, consequence, and current workaround. | One problem statement and evidence of the recurring decision | Solving an impressive technical problem with no buyer |
| Constraint decomposition | P1 | Separate required outcomes, hard limits, negotiable constraints, and assumptions. Challenge the soft ones. | Constraint table with origins and owners | Treating preferences as laws or ignoring actual limits |
| Competing hypotheses | P6 | Construct plausible explanations for the problem and the evidence that would discriminate between them. Seek disconfirmation symmetrically. | Hypothesis-evidence matrix and reversal conditions | Confirmation bias and explanation by repetition |
| Causal analysis | P6 | Distinguish observed association from intervention effect. Identify selection, confounding, spillover, and downstream effects. | A causal claim with an identification strategy, or an explicit non-causal label | Selling usage correlation as return on investment |
| Architectural tradeoff | P6 | Translate qualities into scenarios with stimulus, environment, response, and measure. Examine interacting qualities. | Scenarios, sensitivity points, tradeoffs | Calling a system scalable or secure without a condition |
| Counterexample construction | P6 | Find the smallest realistic input or sequence that breaks the leading candidate. | A reproducible counterexample, or a clearly labeled untested scenario | Vague objections that cannot guide a fix |
| Failure-first review | P6 | Assume the rollout failed. Trace plausible mechanisms backward, then identify leading indicators and containment. | Failure mechanism, observable signal, recovery route | Happy-path planning and late discovery |
| Robustness analysis | P6 | Vary the material unknowns across plausible scenarios. Identify where the preferred alternative changes. | Decision boundary and a low-regret next step | Optimizing to an unjustified forecast |
| Value-of-information | P5 | Ask which missing observation could change the decision and whether obtaining it is worth the delay and cost. | Ranked research or experiment queue | Endless research with no decision movement |
| Divergent design | P4 | Generate alternatives by changing the actor, decision point, data collected, computation location, and delivery surface. | Distinct mechanisms, including a simple substitute | Renaming the same architecture several times |
| Removal test | P6 | Delete a feature, connector, agent, graph, index, or model call and reassess task success. | Evidence for retaining or removing the complexity | Accumulating capability without incremental value |
| Adversarial incentives | P6 | Examine how people, vendors, agents, and buyers could optimize the reported metric while harming the intended outcome. | Gaming scenario and a less misleading measurement | Good-looking metrics with worse work |

Provenance: competing hypotheses follows Heuer's chapter 8, which cautions that the procedure cannot guarantee correctness; the architecture lens follows ATAM; robustness follows RAND's decision making under deep uncertainty; divergence and problem definition follow the Double Diamond and service discovery. Failure-first review, the removal test, and adversarial incentives are proposed adaptations, not experimentally validated debiasing. These are adopted analytical methods, not a measured claim that this skill improves a recipient workload. Investigate a method's original source before relying on an empirical effect.

## Generative procedures (P4)

The removal test subtracts. These add. Use them to improve the opportunity set before converging, and keep only an alternative that alters an actual mechanism or tradeoff.

| Transformation | Question | Worked example of a real change |
| --- | --- | --- |
| Change the unit of value | Is the useful unit a session, an accepted item, a resolved exception, a verified claim, or a completed decision? | Charging for a verified answer rather than a query changes what must be measured and what may be refused |
| Move the intervention | Could help arrive before work begins, during review, at handoff, or after an outcome appears? | Moving from post-hoc analysis to the moment of capture removes an entire reconstruction problem |
| Remove collection | Could metadata, approved artifacts, or on-demand retrieval answer without retaining raw content? | Retaining identifiers and derived features instead of content changes the retention, permission, and revocation problem at once |
| Move computation | Would processing near the data, customer-hosted computation, or federated queries change feasibility? | Executing in the customer's own data plane converts a data-transfer problem into a deployment problem |
| Reduce ambition | If only one decision and one source were supported, would anyone still pay? What value survives? | The one-source version is usually the honest prototype and often the better product |
| Change the surface | Would the same evidence work better as an inbox item, issue comment, scheduled brief, spreadsheet, API, or exported artifact? | An export the customer runs themselves reaches further and loses your ability to revoke it |
| Strengthen the future baseline | If incumbent models and search become much better and cheaper, what durable value remains? | Whatever survives is the actual moat; if nothing does, say so |
| Reverse the hypothesis | Could apparent duplication be useful independent exploration? Could high activity signal rework? | Reading disagreement as signal rather than noise sometimes turns a quality problem into the feature |
| Recombine selectively | Can deterministic computation supply the numbers while a model handles routing, retrieval, and explanation? | The gate disposes and the model proposes; this is usually the strongest available division of labor |
| Change the feedback loop | What user correction could improve later results, and how would that improvement be measured without treating feedback as automatic truth? | A correction path that cannot change a future answer is a complaint box |
| Change when intelligence runs | Compare precomputation, on-demand work, and a mixture. Which facts need freshness, and which expensive transformations can be reused safely? | Precomputing the durable part and computing only the fresh part is often the whole cost argument |
| Unlock a task | What becomes possible rather than merely faster? | A newly possible task has no incumbent workflow, so it needs its own value evidence and a fair test rather than a speed comparison |
| Borrow across products | Could a provenance envelope, entitlement-aware cache, or evaluation harness be reused? | Test compatibility first; a shared component is cheap, a shared trust boundary or corpus is a separate decision |
| Construct the strongest surprising alternative | Take a mechanism from an adjacent domain and state why it might beat both the proposal and the obvious baseline | Give it a falsifier and a modest validation step rather than requiring production proof at discovery |

Use lightweight concept sketches during divergence — a sentence of mechanism and a sentence of why it might win. Expand into the candidate card only for serious contenders. Demanding fully evidenced objections for every embryonic idea eliminates useful ideas before anyone has investigated them.

## Form factors compared on identical tasks (P4, P6)

A surface earns its place against simpler surfaces on the same task, the same evidence, and the same permissions, with unfamiliar users and realistic data density. Measure correct decisions, missed material evidence, completion time, correction effort, explainability, repeat use, and action completion. Add recovery, user control, and behavior over time. A compelling demonstration is evidence of presentation quality, never of decision quality, adoption, or repeat use. A visual surface must show whether a link is observed, inferred, disputed, or stale.

| Surface | Task that could justify it | Main burden to test | Comparator |
| --- | --- | --- | --- |
| Scheduled brief | Periodic review of a small number of decisions | Freshness, evidence inspection, follow-through | Existing report or analyst summary |
| Table or dashboard | Repeated comparisons with stable metrics | Metric interpretation, selection bias, drill-down | Spreadsheet or existing BI |
| Search and grounded chat | The user knows the question but not where evidence lives | Answerability, citation fidelity, reproducibility | Existing enterprise search |
| Exception inbox | A bounded event requires accountable action | False positives, duplicates, ownership, alert fatigue | Existing ticket queue or manual triage |
| Embedded assistant | Decisions already occur in an IDE, document, or tracker | Installation, permissions, context transfer, interruption | The existing workflow without it |
| API, MCP, or export | Another tool owns the interaction or the automation | Auth, contract stability, discoverability, support, and revocability once distributed | Direct API or existing integration |
| 2D relationship view | Users must trace dependencies or investigate connections | Edge validity, layout stability, hidden evidence, navigation | Search, table, or an explicit dependency list |
| 3D relationship view | A task-specific spatial representation may aid exploration | Occlusion, orientation, accessibility, device cost, misleading proximity | Identical tasks in 2D and non-graph surfaces |

A connector, export, or MCP server is a distribution mechanism. Installation success establishes neither data entitlement, tenant configuration, backfill completeness, nor time to first useful result; assess those separately whenever one-command setup is proposed. An artifact the customer runs in their own environment cannot be recalled, so its permission story must be settled before it ships, not after.

## The candidate card (P4)

Every serious contender carries all of these, or it is not yet a candidate:

- Mechanism: what actually changes, in one sentence.
- Target user and the decision it serves.
- Decisive advantage over the current workflow and over the cheapest adequate substitute.
- New burden it introduces: setup, permissions, review, maintenance, cost.
- Strongest evidence-backed objection.
- Necessary assumptions, each labeled per `epistemics.md`.
- Cheapest discriminating test, in the experiment template of `rules-engine.md`.
- Exit path from every material vendor or architecture dependency it introduces.
- In LEVERAGE: the internal capability it reuses, with its path, status at HEAD, and activation cost; or the external precedent it borrows, with its source and date.

The alternatives set always includes the current workflow, the simplest adequate improvement, a buy-or-compose option, and a materially different mechanism. When one is not credible, say so with the reason instead of inventing a weak entry. Creativity cannot erase a hard constraint and cannot substitute for demand evidence.

## Legacy framework map

| If asked for | Run | Because |
| --- | --- | --- |
| Premortem | Failure-first review, then robustness analysis | Same backward trace from an assumed failure, with leading indicators and containment added |
| SCAMPER | Divergent design plus the generative procedures | Substitute maps to change the unit or the surface, combine to recombine selectively, adapt to an external precedent, modify to reduce ambition, put to other use to change the actor or unit, eliminate to the removal test, reverse to reverse the hypothesis |
| Six Thinking Hats | White is the claim ledger, red is the parking lot plus the user's stated intuition recorded as ASSUMPTION, black is competing hypotheses plus counterexample plus failure-first, yellow is the candidate card's decisive advantage, green is the generative procedures, blue is the routing and the rules engine | Every hat has a lens with an inspectable output |
| Devil's advocate, red team | Counterexample construction and adversarial incentives, per the procedure in `challenge.md` | The attack must produce a concrete counterexample, a superior alternative, or a falsifier |
| Decision matrix, weighted scoring | The feasibility vector first; weights only among candidates that pass every hard constraint | A weighted score hides a decisive failure |

## Data and retrieval lenses (P6, whenever the idea ingests, links, or retrieves data)

Build a source-capability matrix before claiming comprehensive capture. For each source inspect supported objects, access scopes, distribution and approval requirements, content versus metadata availability, history depth, pagination, deletion and edit events, rate limits, retry behavior, identity mapping, and export restrictions. Test initial backfill, incremental updates, repeated delivery, missing pages, out-of-order records, clock differences, expired cursors, delayed edits, outages, permission changes, and reconnects. Separate event time from collection time and processing time, and decide whether a report means what happened then or what was known then. Define a coverage denominator where possible; where the universe of events is unknowable, publish the observed boundary instead of a fabricated percentage. A fetched record has not thereby become complete, ordered, or current evidence, and fresh authentication does not prove fresh source permissions.

| Question class | Candidate mechanism to compare | Decisive failure to test |
| --- | --- | --- |
| Find a known source or exact identifier | Lexical search, metadata lookup, hybrid retrieval | Semantic matching misses an exact match |
| Explain a specific item | Scoped retrieval and source-linked synthesis | A cited passage does not support the explanation |
| Count or compare | Deterministic aggregation over an explicitly defined eligible dataset | Retrieved top-k examples presented as exhaustive counts |
| Find relationships across systems | Supported joins, entity resolution, or graph traversal | Similar names or semantics produce a false connection |
| Summarize global patterns | Stratified summaries, map-reduce, graph summaries, or long context | Popular clusters hide rare but consequential evidence |
| Explain a change in outcome | Descriptive analysis followed by an appropriate causal design | Correlation narrated as an intervention effect |
| Recommend an intervention | Evidence and constraint evaluation with an accountable owner | Correct information produces an unactionable recommendation |

Evaluate answerability before answer quality, including absent, restricted, conflicting, obsolete, and unobservable evidence, and measure useful coverage beside accuracy so that abstaining on every question cannot pass. Where query generation exists, trace its validation and execution boundary per `domain-expertise.md` § Semantic computation and conversational analytics; a read-only query still needs assessment for expensive execution and unintended disclosure.
