# Version and recency disambiguation

Establish applicability before using a source. For software this usually means a resolved version and environment; for general knowledge it may mean a population, place, event period, study design, or definition.

## Establish the target

| Ecosystem | Read |
| --- | --- |
| Node / npm | `package.json`, then the lockfile for the resolved version |
| Python | `requirements.txt`, `pyproject.toml`, `poetry.lock`, or `uv.lock` |
| Go | `go.mod` |
| Rust | `Cargo.toml` and `Cargo.lock` |
| Deno | Pinned import specifiers and the applicable configuration/lockfile |
| Runtime | Runtime version file, declared engines, container image, or CI matrix |
| Browser target | The product's support matrix and build/browser configuration |

A declared range is not the installed version. Use the resolved version for behavior claims; broaden queries to a major/minor version only when necessary to find relevant material. Report an unknown or unpinned version when it affects the answer.

## Read the actual documentation context

Docs often default to latest, but verify the selector, URL, title, banner, or source revision. Neither an unversioned URL nor the absence of an “older version” banner establishes latest. Stable, latest, default-branch source, and released tags may differ. Search engines may return old versions; inspect the destination.

For “when did this change,” consult the changelog, release notes, migration guide, and applicable tag history. A merged PR establishes a change was merged, not that it shipped in a particular release. Confirm tag/release inclusion before assigning a released version.

## Date without guessing

Use published or updated dates, versioned source history, and the relevant release record when available. Distinguish publication date, event date, last source update, and your successful inspection date. A copyright footer or date inferred from an obsolete example is not a reliable publication date. An obsolete example may show a scope mismatch or error rather than when the page was written.

Missing dates require applicability checks proportional to volatility, not automatic rejection. An immutable specification section can remain valid for its version; an undated vendor pricing page can be inspected as current offered terms if scope and source identity support that reading. Do not infer that a recently published article is accurate.

Search date operators can narrow a volatile topic but may be ignored and can omit useful stable evidence. Verify dates and scope on the source itself. Ranking is not evidence of recency, authority, or completeness.

## Resolve or retain contradictions

Compare versions, platforms, configuration, accounts, populations, definitions, methods, and time periods. A v3 statement does not override v2 evidence for a v2 project. If scopes match and evidence still conflicts, keep the contradiction unresolved with both locators and what would settle it; do not force a “stale” or “wrong” label without evidence.

Missing documentation is not proof of unsupported behavior. Record “not found in the searched sources and scope” and a useful reopening trigger instead.

Apply the shared [reuse and recheck rules](evidence-and-retention.md#reuse-and-recheck): refresh volatile claims before consequential use, resolve applicability conflicts, and honor explicit verification requests. Immutable evidence can be reused within scope when current-source requirements permit it. Reuse and failed fetches never advance the successful inspection date.
