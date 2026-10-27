# Source selection

Select a source for the kind of claim it can establish. The shared [evidence method](evidence-and-retention.md#keep-four-judgments-separate) defines Authority, Status, Basis, and Access; they are separate from a source's usefulness as a lead.

## Prefer the record that answers the question

| Question | Best starting evidence | Limit |
| --- | --- | --- |
| Documented API parameters, defaults, or supported options | Official docs for the applicable version | Documentation does not establish account availability or measured runtime behavior. |
| Required behavior or terminology | The specification, standard, or normative record | Implementations may differ; distinguish required from observed behavior. |
| Code behavior | Applicable source, tests, type definitions, and a scoped reproduction when needed | Source inspection is not a run; passing tests prove only their conditions. |
| When a software behavior changed | Release notes, migration guide, tag history, and the relevant change | A merged PR is not proof that a released version contains it. |
| Intent or a known defect | Maintainer issue/PR discussion with identity and later updates checked | Plans and intended fixes do not establish delivery. |
| Historical or public facts | Original archives, public records, authoritative datasets, or direct documents | Establish provenance and the period/population covered; publication date alone is not the event date. |
| Causal, scientific, or performance claims | Original study or measurement with methods, controls, scope, uncertainty, and relevant independent evidence | Authority and recency cannot repair an unsuitable design; correlation does not by itself establish causation. |
| Explanation or synthesis | Relevant expert analysis with traceable underlying evidence | Separate the author's interpretation from the primary findings. |

For technical research, follow primary-source requirements from the active runtime. Community answers and aggregators can reveal the vocabulary, issue, or underlying documentation; inspect and cite the primary record for material technical claims. For general knowledge, a sound secondary synthesis may support an interpretive claim where the research task permits it. Neither an official badge nor a forum label decides every claim's quality.

## Assess unfamiliar or competing sources

Ask who produced the evidence, how they could know, what interests and methods affect it, which scope it covers, and whether its cited support is inspectable. Look for missing qualifiers, subsequent corrections, or contrary evidence. Missing dates create a currency question; they do not automatically disqualify an undated authoritative document. A verifiable error weakens the affected claims and calls for checking related claims, rather than proving every sentence false.

Vendor comparison pages establish what the vendor asserts. Independently measured comparisons with compatible workloads can establish more, but still require their methods and limitations. A local reproduction can answer a local behavior question; it cannot establish universal behavior.

When docs and code disagree, compare the exact versions and conditions before choosing a conclusion. Preserve a documentation defect or unresolved inconsistency with both locators. Same-origin docs/source or changelog/PR pairs are valuable consistency checks, not independent empirical corroboration. Follow the shared method for contradiction status and retention.
