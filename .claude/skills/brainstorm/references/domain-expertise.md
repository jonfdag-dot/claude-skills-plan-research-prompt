# Domain expertise — transferable method, selected by mechanism

Load the sections whose mechanism the idea actually uses, before framing research questions and before comparing candidates. Domain expertise decides which alternatives are worth generating and which claims are worth researching; arriving with it after divergence means researching the wrong things.

Select by mechanism, never by project name. A new product doing conversational analytics needs the semantic section even with no profile of its own; a vision product that also executes actions needs the identification section and the action-authority section. Everything here is transferable method. A project's own invariants, never-lists, and paths live in `knowledge-library.md` and bind only inside that project; a general method never overrides a project's actual fence, and a project's fence never becomes a universal rule.

Each section is organized the same way: the unit of truth, the mechanism choices worth comparing, the characteristic failure modes, the evidence that would settle them, and the questions that actually find defects.

## Identification and source-grounded research

**Unit of truth.** Separate them explicitly, because a system that conflates them will report confidence it has not earned: the input (image, crop, sensor reading), the candidate identity, the independent source, the factual assertion made about the identified thing, and the abstention. A pipeline can be excellent at retrieval and still wrong about identity; it can be right about identity and wrong about every fact it then tells.

**Decompose the task before choosing a mechanism.** Recognizing a category, resolving an exact instance, finding an image's origin, identifying a place, and verifying a claim about any of those are five different tasks with different error criteria. Ask where each transition is supported by evidence rather than by the previous stage's confidence.

**Mechanism choices worth comparing.** Parametric model naming versus retrieval against an index versus a geospatial or catalog lookup versus a corpus of prior verified results. A fusion rule that requires agreement between sources versus one that ranks a single best source. A closed candidate set an arbiter may only choose from, versus free-text generation at the final step — the closed set is the cheaper and stronger guarantee and is worth proposing wherever a final naming step exists.

**Failure modes that actually occur.**

| Failure | What it looks like | What defeats it |
| --- | --- | --- |
| Correlated agreement | Two "independent" namers share a vendor, a base model, a training corpus, or a retrieval index, and agree because they are the same evidence twice | Group evidence by its origin before counting corroboration; demote a same-origin pair unless something structurally different corroborates it |
| Replicated sources | Three pages agree because all three restate one caption, index entry, or model-generated description | Source lineage, not source count; check whether the wording, image, or index entry is shared |
| Class-right, instance-wrong | The system names the type correctly and the specific object wrongly — a replica, an edition, a copy, a second casting, a reproduction of a work | An instance-level discriminator such as location agreement, a catalog identifier, or an explicit generic-name test that refuses to promote a type name to an identity |
| Hint anchoring | OCR text, a page title, a location hint, or the first candidate anchors every subsequent search onto a false identity | Re-run the discriminating cases with the hint withheld or contradicted, and check whether the hint voted or merely seeded |
| Entity confusion over time | The physical object, its reproduction, a photograph of it, and the place it was photographed are treated as one entity; the object moves and the pages go stale | Distinct identifiers per entity kind, and a representation for "moved" and "superseded" |
| Cache outliving its source | A claim keeps serving after its source is corrected, retracted, or made inaccessible, because the cache key is versioned on the template rather than on the source | Cache keys and invalidation traced to source state, not only to prompt or template version; a maximum age you are willing to defend |
| Silent unit dropping | Generated text carries citation markers; unresolvable ones are dropped, and the answer ships thinner than it looks | Count and report dropped units; treat a narrative that survived only by dropping its unsupported parts as a failure signal |

**Abstention is a product feature, not an error path.** Evaluate precision and coverage together — a system that abstains on everything must not be able to pass. Ask whether the system can abstain with a reason the user can act on, whether it can ask for a better input instead of guessing, and whether an unavailable checker fails open (never manufacturing a negative verdict) while anything that moves money or state fails closed.

**Evidence-type discipline.** Retrieval APIs return several distinct signal types and they are not one identity claim. Google's Web Detection, for example, returns web entities, full and partial matching images, pages containing matching images, visually similar images, and best-guess labels as separate fields ([Google Cloud Vision, web detection](https://docs.cloud.google.com/vision/docs/detecting-web)). Represent them separately and verify the specific assertion the product intends to make; a "page contains a matching image" result is an association, not an identity, and not a property.

**Economics and latency.** Measure cost and elapsed time per adequately grounded result at a declared error and coverage level, not per API call. Test cache-warm and cold results separately. Ask the marginal question directly: at what admitted-claim yield is one more search or model call worth buying? A search budget with no measured yield is a spending rule, not a quality rule. For latency, check whether a deadline actually aborts work or only emits a signal, and whether there is a first-output timer distinct from a total-completion timer — the difference between degrading honestly and hanging is visible only at the tail.

**User experience.** Can the user see the likely match, the evidence behind it, the uncertainty, and an efficient correction path? Compare an evidence card or annotated image against chat, a map, or a richer visualization on the actual task, not on appearance. A correction path that cannot change a future answer is a complaint box.

## Semantic computation and conversational analytics

**Unit of truth.** The metric definition and its version; the interpretation of the question; the authorized data scope; the executed result; and the narrative claim. Fluency at the last step tells you nothing about the first four.

**The metric contract is the product.** For each metric ask what it means, who owns it, and which version applies. Specify unit, aggregation, denominator, filters, time basis, currency handling, and exclusions where relevant. Absent fields are the finding: a rate metric with no denominator field anywhere cannot prove that numerator and denominator share a filter set, and a definition with no version cannot tell a consumer that it changed. The dbt semantic-model documentation is a useful concrete comparison for what an explicit contract carries — entities, join keys, dimensions, aggregation time, and metrics as named objects ([dbt semantic models](https://docs.getdbt.com/docs/build/semantic-models)) — used as comparison dimensions, never as a requirement to adopt any particular tool.

**Grain and joins.** Ask what one row represents. Then test whether joins can multiply facts, drop unmatched records, or cross incompatible grains. Include many-to-many relationships, duplicate keys, missing keys, and slowly changing dimensions. A fan-out that inflates row count produces a syntactically valid, cheap, wrong answer that passes every row cap and every read-only check — those guards constrain blast radius and cost, and they say nothing about semantic correctness. Ask separately what blocks sum-of-averages and what blocks aggregating a non-additive measure.

**Time and comparability.** Do "last month", "active", and "growth" use the intended time zone, calendar, cohort, and comparison period, and is that anchor persisted with the metric or re-derived per turn from the model's reading of intent? Re-derived time semantics mean the same phrase can resolve differently six weeks later with no diff to show for it. Distinguish a correction to the data from a change to the metric definition; the second breaks historical comparability even when nothing errors.

**Conversation state.** When the user says "now by region", which filters, entity selections, and definitions persist and which are recomputed? Make material ambiguity visible. Test where clarification is genuinely necessary and where a reasonable interpretation with a stated assumption is better than a question.

**Calculation and explanation must be traceable to each other.** Trace a question through interpretation, the governed query or equivalent computation, the returned result, and the narrative. Ask whether the explanation describes the calculation actually performed, or a separate derived statistics pass that never sees the query. Both designs are defensible; only one of them can answer "why is this number what it is". Check that every number in the narrative appears in the executed result set.

**Query validation, honestly classified.** Read-only enforcement is usually one of: a lexical or regex deny-list, a keyword check, an AST or parser-level check, a relation allow-list, or a database-level privilege. They give very different guarantees, and a deny-list is a filter, not a proof. Look for stored-but-unenforced policy — allowed schemas, forbidden tables, default limits written at connection time and never read on the execution path, or a policy function with no callers — because a persisted policy nobody reads is a promise the product may already be making somewhere in its marketing.

**Authorization is about the effective execution identity, not the feature list.** Trace who the database actually sees. In PostgreSQL, "Superusers and roles with the `BYPASSRLS` attribute always bypass the row security system when accessing a table. Table owners normally bypass row security as well, though a table owner can choose to be subject to row security with `ALTER TABLE ... FORCE ROW LEVEL SECURITY`" ([PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)). So "RLS is enabled" is not evidence; the effective role is. The common real pattern is a privileged service connection plus an application-layer ownership predicate, which is a defensible design and is not the same claim as database-enforced isolation — say which one is true. Then ask whether entitlements survive every surface: UI, API, tool or MCP call, cached result, chart, export, and any capability the product hands the customer to run themselves.

**Schema and semantic evolution.** Ask what invalidates saved conversations, generated queries, cached results, dashboards, exported artifacts, and tool descriptions after a definition changes. Look for the dependency edge; usually there is none, and drift surfaces as a warning that ships anyway. Decide deliberately between defined compatibility and an explicit error, and note that an artifact already downloaded into a customer's environment cannot be recalled — revocation of an export is a different problem from invalidation of a cache.

**Evaluation.** Score interpretation, computation, provenance, refusal, clarification burden, latency, and cost separately, using expert-reviewed tasks whose meanings and correct results are known in advance. A fluent answer and an executable query are both insufficient. Include adversarial inputs, and check that hardening against them does not also reject legitimate queries.

## Event evidence, derivation, and analytical retrieval

**Unit of truth.** Distinguish, and keep distinguishable downstream: the logical request or effort; the delivery event or attempt; the derived artifact (chunk, summary, embedding, projection); the observed action; and the verified outcome. The strongest formulation of the law is that observation is not contribution, contribution is not accepted work, accepted work is not an outcome, and an outcome is not causal impact. Every collapse of two of those is a defect that reads as a feature.

**Capture boundary.** Which requests, responses, tool calls, models, identities, and sources traverse the capture point, and what bypasses it? Does the product claim complete coverage of a clearly defined population, or only of observed traffic? Absence of a signal is not absence of the activity. Publish the observed boundary rather than a fabricated percentage, and treat coverage as a per-surface fact rather than a per-customer one.

**Event identity, retries, and streams.** Define the delivery identity explicitly and state what it is not: it is a delivery identity, never an episode, run, or outcome identity. Then test the whole class — partial streams, cancellation, timeouts, retries, duplicate delivery, out-of-order events, replays with new identifiers, a vendor changing its dedup namespace, and missing completion signals. One logical action must be able to have several attempts without becoming several outcomes; the double-counted-activity bug is the single most common way an evidence product becomes confidently wrong.

**Ingestion isolation.** Is ingestion inline with the user's request or asynchronous? What happens to the original request when storage, summarization, or indexing fails? Compare backpressure, data loss, added latency, and recovery explicitly, and say which side of a checkpoint a partially committed batch lands on. A quarantine that silently flips a coverage threshold changes answers without erroring.

**Payload, retention, and revocation.** Determine what content is necessary, what is redacted or excluded, who can access it, and which derived copies exist. Do not read "all the data" as a justified retention design. Revocation is the test that separates a real permission model from a stated one: name the derivatives — summaries, embeddings, indexes, flags, exports, queued deliveries, digests, caches — and say which are reachable by reverse dependency and which are only reachable by evicting everything. A deletion statement is not an executed revocation test.

**Chunking and summarization.** Preserve source versions, record or event references, context boundaries, and derivation paths; derive chunk identity from stable structural coordinates rather than from the body's hash, so a re-summarized parent does not silently become a different chunk. Then ask what a summary can lose: negation, attribution, sequence, disagreement, exceptions, dates. Ask what happens when a source is corrected — whether downstream summaries are invalidated, and whether a claim can be retained while being marked known-false rather than deleted.

**Retrieval versus complete computation.** Route semantic discovery to retrieval and route totals, populations, and absence claims to complete authorized aggregation. Top-k answering a count question is the classic error; so is treating an empty retrieval as proof of absence. Test cross-chunk questions, exact identifiers, negation, overlapping groups whose counts are non-additive, and questions that should be refused. Label partial coverage on the answer rather than in a footnote.

**Correction and contestability.** Can the affected party see and contest what was recorded about them? Is a user marker an attributed annotation rather than verified evidence? Does a correction propagate to derived artifacts, and does the system derive the correcting subject from the authenticated session rather than accepting it in the request body?

**Drift and recomputation.** After a prompt, model, chunker, embedding, schema, source, or permission change, what must be reprocessed? Can versions coexist? Can stale results be detected? Price the reprocessing before proposing the change, and note that a code rollback does not restore earlier data semantics and does not reverse an external action.

## Say which graph you mean

All three product classes above use the word "graph" for different mechanisms. Name which one is proposed before evaluating it, because success in one layer says nothing about the others.

| Graph meaning | What an edge must record to mean anything | What it cannot establish |
| --- | --- | --- |
| Semantic model | Entities, metrics, relationships, and which calculation paths are valid | That any particular answer is correct |
| Provenance or execution graph | Which event or transformation produced which artifact, and by what activity | That the artifact's content is true |
| Entity knowledge graph | The meaning of the relationship, its source, its standing, and its uncertainty | Causation, or that the relationship still holds |
| Similarity graph | What proximity represents and over what representation it was computed | Ownership, dependency, authorship, or causation |
| Visual graph, including 3D | That the representation improves a named user task against credible alternative surfaces | Anything about the retrieval or the data model beneath it |

A similarity edge is a candidate, not a claim, and must never be readable back as an asserted relation. A presentation coordinate — a layout distance, an orbit radius, an arc — is not an edge and must not be interpretable as one. A useful graph index does not establish a useful graph interface: research showing that graph-based indexing and community summarization help a class of global questions over a text corpus is evidence about retrieval architecture, and evaluating a 3D interface requires its own task comparison with error, time, evidence inspection, correction burden, accessibility, and device constraints measured.

## Action authority across a boundary

Any idea where the system does something on a user's behalf — a tool call, a connector, an MCP surface, a webhook, a write into a customer system — needs this section regardless of domain.

Bind four things explicitly and separately: the identity of the caller, the data scope that identity is entitled to, the contract of the tool or resource, and the authority to take the action. Authenticating a call establishes the first and none of the others. Separate discovering a capability, querying it, explaining it, proposing an action, and executing one; those are five different authorizations that products routinely collapse into one.

For every proposed action, name the actor, the target, the authority, the evidence version acted on, the preconditions, the approval, the idempotency key, the observed postcondition, and the recovery path. A timeout leaves the outcome unknown rather than failed. A rollback of application code does not reverse an external effect.

The MCP security guidance is the current primary source for this class of failure and is worth reading against any tool-exposing design: it treats token passthrough as an anti-pattern and states that "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server", describes the confused-deputy flow that lets a dynamically registered client ride an existing consent cookie, and requires that servers "**MUST NOT** treat possession of a state handle as authentication" ([MCP security best practices, version 2026-07-28](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)). Check the protocol version you are actually reviewing — this guidance is versioned and an older dated URL describes an older model. Protocol conformance still does not demonstrate application authority: trace the effective identity and data scope through the entire path, including caches, exports, and any artifact the customer runs in their own environment.

## Composing this for a product with no profile

Read the request for its mechanisms, load every section that matches, and say which ones applied. Then discover the product's own constraints rather than importing another product's: find its governing document, its invariants and never-lists, its deferred or reserved register, and its evidence conventions, using the generic procedure in `knowledge-library.md`. When none exist, say so in the capability map rather than assuming a fence or assuming its absence.

Two composition rules. First, a mechanism borrowed across products is a hypothesis about fit, not a shared system: a provenance envelope, an entitlement-aware cache, or an evaluation harness may transfer cheaply, while a shared trust boundary, a shared customer corpus, or a shared ontology is a separate decision needing its own evidence and its own authority. Second, a restriction discovered in one product does not travel with the method — check whether the new product has an equivalent fence, and record that you checked.
