# Epistemics — labels, ladders, provenance, stage-relative support, and economics

Pulled whenever the analysis carries evidence: when the claim ledger opens, when research updates it, and when the feasibility vector is scored. This file owns claim labels, evidence sufficiency, and the cost model. It does not own stage gates or verdicts (`rules-engine.md`), research stopping (`research-pipeline.md`), or capability statuses (`knowledge-library.md`).

## The five labels

Every material claim carries exactly one label and its rider. A label without its rider is an unlabeled claim, which is a defect rather than a shortcut.

| Label | Meaning | Mandatory rider |
| --- | --- | --- |
| **VERIFIED** | An inspected primary source that is the authority for the fact, or an observed result, supports this exact claim within its stated scope, or an independent second source agrees; record which in Corroboration. A vendor's statement is verified as a published claim, never as a working feature, unless independently tested. | State the scope. |
| **INFERENCE** | A conclusion drawn from identified evidence. | State the missing causal or applicability link. |
| **ASSUMPTION** | A provisional input adopted so the analysis can proceed. | State what changes if it is wrong. |
| **UNKNOWN** | Required evidence is missing, inaccessible, or inconclusive. | State how it could be obtained. |
| **CONTRADICTED** | Identified evidence conflicts with the claim. | Preserve both accounts and name the difference under investigation. |

Labels describe claims, not sources. VERIFIED never means every implication of the claim is true: "the vendor documents this feature" can be VERIFIED while "it works with our tenant and workload" stays UNKNOWN, and a benchmark result can be VERIFIED for its experiment while the production benefit remains UNKNOWN. Endpoints, scopes, rate limits, prices, retention windows, version numbers, and effective dates recalled from memory are UNKNOWN until retrieved; use ASSUMPTION only when you are deliberately adopting a value for a scenario. Vendor positioning is VERIFIED as positioning and never establishes effectiveness, pricing, feature completeness, or an underserved segment.

## Four independent dimensions

Record these separately and never convert one into another.

| Dimension | Question it answers | Example of the mistake |
| --- | --- | --- |
| Claim status | Is this claim supported, within what scope? | Converting INFERENCE into "partly true", which is a statement about a compound claim's components, not about a derivation |
| Source type and quality | What kind of source is this, and how good is it for this claim? | Converting VERIFIED into a source grade, which describes the source rather than the claim |
| Derivation | What produced this, from what? | Treating a summary of a source as the source |
| Scope | Over what population, workload, version, and date does it hold? | Carrying a claim past the conditions that made it true |

An inference can be correct. A compound claim that is partly true can contain both verified and false components. When a project's vocabulary does not express the same distinction, keep the canonical label and add the project's representation beside it; never replace one with the other.

## The claim-type ladder

Seek the best available evidence for the kind of claim, and refuse the shortcut that resembles evidence. Research technical and business feasibility as distinct questions, and let each inform the other during investigation rather than waiting until the verdict: official documentation can establish a documented capability and never willingness to pay; a customer interview can reveal pain and never that a connector exposes the required field.

| Claim | Best available evidence to seek | Insufficient by itself |
| --- | --- | --- |
| A feature already works | Reachable implementation, applicable configuration, observed behavior, at a named revision | A plan, README, type declaration, unused helper, or a passing unrelated test |
| An integration is feasible | Current official contract, access entitlement, representative payload, a targeted integration observation | A vendor logo or a broad integrations page |
| A method improves an outcome | Original study with comparator, task, population, metric, and limitations; local replication where consequential | A benchmark headline or an undifferentiated average |
| Customers need the product | Recent concrete workflow examples, costly workarounds, decision ownership, observed adoption or commitments | Generated personas or hypothetical enthusiasm |
| Customers will pay | Actual budgets, purchasing authority, procurement constraints, credible commitments | Market size or survey interest alone |
| A rival lacks a capability | A scoped current comparison with documentation and applicable hands-on evidence | Failure to find the capability on a landing page |
| A use is permitted | Applicable current policy, contract, law, jurisdiction, intended use, and qualified review where interpretation is consequential | Generic consent or a broad compliance badge |
| An internal capability is available to reuse | The writer, the reader, the exposure path, the contract, the persisted state, and observed behavior — plus the cost to activate each missing piece | A reserved slot, a schema comment, a plan status line, an archived spec, or a wiki page |

The last row is the one most often shortcut. A placeholder with zero writers establishes only that a placeholder exists. It says nothing about migration, compatibility, exposed behavior, policy checks, operational ownership, or cost. Inspect the path and price the activation before calling anything cheap. Deployed-but-disabled code needs renewed validation and an owner; an unused enum value may need a migration and a compatibility window.

## Provenance record

Record for every decisive claim: source title, publisher or authors, URL or repository path, publication or update date when available, access date, version or revision, the relevant locator, the claim it supports, and its limitation. For an implementation claim also record the inspection date, the repository revision when available, the execution environment, and the relevant configuration — code at HEAD and behavior in a deployed environment are different observations and a claim about one does not transfer to the other. Keep short exact excerpts only when useful and within reproduction limits; otherwise use a precise paraphrase plus the locator. Private sources stay private.

A citation that passes a literal quote check establishes only that the words appeared there. It does not establish that the source is true, that it entails the claim, that it is complete, that its causal reading is valid, or that it applies to today's system. Test each separately, and check supersession and applicability before transferring an older study, benchmark, or version to the current system. Provenance describes origin — entities derived by activities attributed to agents, in the sense of [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) — and never certifies that the content is correct.

## Contradictions

When sources conflict, compare populations, definitions, baselines, measurement windows, versions, methods, and incentives, then record one of three states: **resolved**, **explained by scope**, or **unresolved**. Never average two contradictory figures; report both, name which one governs and why, and log the conflict where the project keeps conflicts.

Syndicated articles, two agents reading the same study, and two workers citing the same vendor page are one source. Do not pool incompatible evidence without an explicit synthesis rationale: documentation, code inspection, traces, and user observation can legitimately triangulate a claim while keeping their different scopes, but a self-reported survey and a randomized task measurement answer different questions and must not be merged into one figure. When you do combine them, say what each contributes and what neither establishes.

## Support is relative to the next commitment

`SUPPORTED` is never a global certificate. Report it with its stage and scope, using the gates in `rules-engine.md`. When support is absent, give the reason: `UNSUPPORTED: untested`, `UNSUPPORTED: insufficient evidence`, or `UNSUPPORTED: inconclusive`. Reserve `CONTRADICTED` for evidence against the claim. A strong UNKNOWN can justify an experiment; it does not automatically justify rejection.

## The feasibility vector

Feasibility is a vector, never a score. Assess each applicable axis separately as **SUPPORTED**, **UNSUPPORTED** with its reason, **CONTRADICTED**, or **NOT APPLICABLE**, each with its evidence, scope, and the stage it is being judged against. Score the axes the decision actually turns on; a discovery-stage idea is not required to answer production axes, and marking them NOT APPLICABLE with the stage named is the correct result rather than a gap.

| Axis | SUPPORTED requires | Decisive failure to watch for |
| --- | --- | --- |
| Problem value | A named actor, recurring decision, trigger, consequence, and current workaround, with a recent real occurrence | An impressive technical problem with no buyer |
| Data access | Demonstrated access under the intended entitlement, with usable coverage, permission fidelity, and change handling | Required data assumed available; a fetch mistaken for complete, ordered, current evidence |
| Semantic validity | Items, identities, metrics, and relationships reconstructed faithfully against labeled examples and realistic negatives | Similarity presented as ownership, dependency, or causation |
| Technical performance | Measured behavior under representative workload with the critical path and end-to-end percentiles named | Component percentiles summed into an invented end-to-end figure |
| Permissions | Authorization applied to records, derivatives, counts, citations, caches, exports, and action destinations, with revocation traced | Fresh authentication mistaken for fresh source permissions |
| Operational reliability | Backfill, duplicate delivery, outages, version changes, partial completion, and recovery rehearsed | Happy path only; a timeout read as a definite failure |
| Economics | Total delivery cost including failed attempts, review, maintenance, and support, with dated price inputs and the accounting boundary declared | Released time monetized without a changed expenditure or a valued outcome |
| Adoption | Real data access granted, an owner assigned, repeat use, procurement work, or budget committed | Hypothetical enthusiasm; a demo's presentation quality read as decision quality |
| Differentiation | A named decision, permitted evidence unavailable in an adequate substitute, lower operating friction, or a better verified outcome | A broad promise to collect data and produce insights |

A decisive failure on any axis is never averaged away: a good interface cannot compensate for unavailable required data, strong demand cannot make a non-identifiable causal claim verified, and an excellent architecture cannot establish that anyone will buy it. Weighted comparison is allowed only among candidates that satisfy every hard constraint, with the scales, preferences, and sensitivity to weighting declared. Do not manufacture numeric precision where the evidence is qualitative.

## Economics, stated symbolically

Until inputs are measured or sourced, keep the cost model symbolic and declare the accounting boundary before using it, so infrastructure and review costs are never counted twice.

```text
Period delivery cost = ingestion + normalization + storage + indexing + inference + evaluation + retries + egress + human review + connector maintenance + support
Cost per accepted result = total cost of all attempts / accepted results
Customer net benefit = attributable realized benefit - implementation and operating cost - transition and review burden
Gross margin = (recognized revenue - attributable cost of delivery) / recognized revenue
```

- Compare incremental cost and benefit against the actual baseline at comparable quality, and name that baseline and its conditions. If accepted results or revenue are zero the ratio is undefined; report volume and total cost instead.
- Cash savings, released capacity, output growth, quality improvement, and risk reduction are separate benefit categories. Monetize each only with explicit assumptions and no double counting. Released time has no cash value unless it changes expenditure or produces a valued outcome.
- Measure cold start, normal operation, bursts, reprocessing, and recovery. Include the initial corpus and its change rate, connector count, tenant skew, duplicate rate, review rate, retention, and cache invalidation. Token, model, and provider prices are dated inputs.
- Provider-side prompt caching and application-side result caching behave differently; never book a cache discount without a measured read.
- For latency, name the critical path, parallel stages, queueing, rate limits, and external dependencies, and measure end-to-end percentiles. Summing component p95 values does not produce an end-to-end p95. Separate interactive response requirements from background completion requirements, and check that a deadline actually cancels work rather than only emitting a signal.
- Protect margin deliberately: token discipline, safe cache reuse, a measured tier or model selection rather than a default to the largest, and a named exit path from every material vendor or architecture dependency.
- Stress the design with a much larger tenant, a sharply higher revision rate, lower cache reuse, and cheaper or stronger incumbent models. Label the multipliers as assumptions, never forecasts, and show sensitivity to the assumptions that actually move the decision instead of supplying a decorative point estimate.

## Units of evidence and value

Pick the unit before measuring anything; most economics arguments fail because the unit of evidence and the unit of value are different things.

| Evidence unit | Value and cost unit |
| --- | --- |
| The smallest thing you can observe and label: an input, a candidate, an independent source, an assertion, an abstention, an attempt, a derived artifact, an execution result | The smallest thing a user would recognize and pay for: an adequately grounded result, a correctly answered decision task, a traceable answer, a completed workflow outcome |

State both, and state the declared quality level at which the cost is counted. Cost per attempt and cost per accepted result differ by the failure rate; a system that abstains more looks cheaper per attempt and may be more expensive per useful answer. Include failure handling, human review, onboarding, data maintenance, and changing workload in the value unit's cost.

## Recording a conflict between documents and code

Documentation, plans, and marketing surfaces drift from implementations. When they disagree, record the disagreement with both locators and both dates, classify which is current versus proposed, and let the code at HEAD govern claims about behavior while the governing document governs claims about intent. Do not silently resolve it in either direction, and do not treat a stale document as a permission or a prohibition it no longer earns.
