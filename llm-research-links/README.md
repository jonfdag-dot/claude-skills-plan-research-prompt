# Shared research library

This repository keeps reusable findings across source projects. Start with a concrete decision, retrieve a few relevant records, investigate what remains and retain only evidence that informed the work. [CLAUDE.md](CLAUDE.md) supplies the short contract; [INDEX.md](INDEX.md) maps each file.

## Layout and ownership

`sources.md` is the six-column permanent source register, queried only through the CLI. `notes/<domain>/<topic>.md` holds canonical R-ID sections; each populated domain has README navigation and an index of pointers. `projects.md` groups applicability without duplicating evidence. `taxonomy.md` defines claim-based domains, and `topics.md` optionally names reusable entity queries. `reports/` holds decision-specific syntheses; plans live in the sibling plan library.

The starter intentionally contains no imported personal findings. One generic example record documents the starter's own plan format, with local provenance and Checked UNKNOWN; it is sample evidence about these files and makes no external product claim. Example IDs are local to this new library and unrelated to any source installation's IDs.

## Research workflow

1. Frame the question, decision, constraints and scope. Read [notes navigation](notes/README.md) and selected domain README.
2. Query labels, exact identities or 1–3 ANDed entities; optional terms rank within that pool. Open the closest few records and owner links. Do not dump the register or preload every domain.
3. Identify gaps and needed freshness. Inspect primary text suited to the claim, versions, methods, qualifications and counterevidence. Treat a snippet or failed fetch as partial access rather than a verified source.
4. Synthesize by subquestion, comparing serious alternatives and competing explanations. Explicit deep research includes a fresh independent challenge of consequential conclusions, followed by the parent's citation, calculation and coverage audit.
5. Retain useful findings as one reconciled packet, validate the write batch and report saved IDs or pending persistence. Stop when additional inquiry is unlikely to change the decision; disclose remaining unknowns.

## Read commands

Run from this repository. All commands below are local and require no network or API key:

```sh
python3 -B scripts/research.py labels --kind domain
python3 -B scripts/research.py labels --entity research-evidence --kind tag
python3 -B scripts/research.py find --entity research-evidence --limit 5
python3 -B scripts/research.py show R-0001
python3 -B scripts/research.py topics --check
python3 -B scripts/research.py template
```

Use `show <exact-URL>` before adding a source. A record's canonical section has its own `## R-0001` heading and qualifications. `find` accepts domains, tags, project slugs, aliases or `kind:value` filters. Results cap at 25; narrow broad pools instead of reading everything. Reuse selected IDs through unchanged follow-ups. A local read never refreshes external evidence.

## Record contract

The register columns are `ID | Source | Useful for | Authority | Checked | Evidence note`. IDs are permanent `R-0001` style identifiers. A source is a titled link to its exact URL or native file identity. Checked is the last successful external inspection date or UNKNOWN; copy/import dates belong in provenance. The evidence link targets `notes/<domain>/<topic>.md#r-0001`.

Each canonical section contains Claim, Status, Basis, Applies to, Evidence, Access, Origin, Recheck, Corroboration, Tags, Projects, Use when and Canonical owner. Tags/projects are unique alphabetically sorted lowercase kebab slugs. Canonical owner is `this library` or a precise titled link to the specialist or source-project record that owns the detailed facts.

| Dimension | Values and interpretation |
| --- | --- |
| Authority | PRIMARY for original evidence suited to the claim; FIRST_PARTY for an interested producer's account; SECONDARY for analysis; DISCOVERY for a lead. |
| Status | VERIFIED for the scoped supported claim; VENDOR CLAIM for an unestablished producer assertion; INFERENCE for a reasoned conclusion; UNKNOWN for insufficient/conflicting support; PROPOSED for an untested option. |
| Basis | DOCUMENTED, AUTHENTICATED, MEASURED or UNKNOWN. Documentation does not prove an authenticated operation or measured performance. |
| Access | INSPECTED, PARTIAL or UNAVAILABLE for the actual supporting content read. |

Origin starts `LIVE;` with retrieval method/date and actual task use, or `IMPORTED;` with original ID, path, revision/hash and original checked date. Recheck names what would reopen the claim. Corroboration distinguishes independent evidence, same-origin cross-checks and absent support. Optional Attempted records a failed fetch without advancing Checked. Optional State is current, superseded or rejected; superseded requires Replacement. Append dated History instead of erasing earlier evidence.

## Add or relabel

Start from the JSON printed by `research.py template`; replace every placeholder. Packets may contain one record or a `records` list. See `scripts/templates/finding.json` for a proposed example and `scripts/templates/report.md.template` for a synthesis outline. The example packet is a scaffold with UNKNOWN/PROPOSED labels, not a claim of source inspection.

```sh
python3 -B scripts/research.py add --dry-run --new-label /path/to/packet.json
python3 -B scripts/research.py add --new-label /path/to/packet.json
python3 -B scripts/research.py relabel R-0001 --add-tag planning --reason 'Explain the actual applicability change'
python3 -B scripts/validate.py .
python3 -B -m unittest discover -s tests -v
```

Use `--new-label` only for deliberate new tags/projects after checking labels. Reusing an existing source for a distinct claim needs `--allow-same-source`; it is not a deduplication bypass. The writer allocates the next ID and updates the row, canonical note, domain index and project pointers together, refusing added integrity diagnostics. Coordinate concurrent writers. Read-only workers return packets; the parent reconciles and saves them.


## Retention and reporting

Keep only findings that supported an answer, implementation, test or decision, ruled out an option, or established a material limitation/contradiction/dead end with future reuse. A URL without a useful claim is not a record. Preserve canonical owners and meaningful provenance; never store credentials or proprietary source bodies.

One report occupies either one file or one folder under reports/; use README.md plus references/ when supporting files are needed. Keep volatile plan state out of reports. Use the sibling [plan library](../llm-plan-links/README.md) for implementation planning and handoffs.

Report saved IDs only after write and reread succeed. If saving fails, return the complete pending packet and specific blocker. An offline structural pass is not a claim that the research itself is verified.
