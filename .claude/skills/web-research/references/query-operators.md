# Query operator craft

## The operators

| Operator | Effect | Note |
|---|---|---|
| `"phrase"` | exact contiguous match | the highest-leverage operator; use it for every error string and API name |
| `-term` | exclude documents containing the term | kills a dominant wrong sense in one token |
| `site:host` | restrict to a host or a path prefix (`site:github.com/vercel`) | target the source suited to the claim |
| `-site:host` | exclude a host | useful for cutting out a content farm that dominates a niche |
| `filetype:ext` | restrict by file type | `pdf` for specs and papers, `md` occasionally for repo docs |
| `intitle:` / `allintitle:` | term must appear in the page title | `intitle:changelog`, `intitle:"migration guide"` |
| `inurl:` / `allinurl:` | term must appear in the URL | `inurl:v2`, `inurl:release-notes` |
| `OR` (capitalised) and `( )` | alternates and grouping | `("release notes" OR changelog) site:github.com` |
| `after:` / `before:` | date bounds, `YYYY-MM-DD` or `YYYY` | Google-family syntax; behaves inconsistently on other surfaces |
| `*` | wildcard word inside a quoted phrase | `"deprecated in * 5.0"` |
| `related:host` | legacy similar-site query form | use only if the active engine documents support |

**Reliability caveat.** Operator support differs by search surface. Verify the active tool supports the syntax; ignored or approximate operators do not establish that an answer is absent. The GitHub qualifiers `is:issue`, `is:pr`, `is:merged`, and `path:` in examples are for GitHub native search, not guaranteed filters in web search. On a web engine, use the repository name, literal symptom, and `site:` where supported, then inspect the result.

## Query patterns by research type

### An error or exception

```
"<most distinctive literal fragment>" <library> <major version>
repo:<org>/<repo> is:issue "<fragment>"
"<fragment>" -site:<content-farm-you-keep-hitting>
```

Strip everything project-specific first: absolute paths, UUIDs, ports, hashes, line numbers, your
own symbol names. Those tokens are what make an error return zero results. Keep the vendor's own
wording, verbatim and quoted.

If the error text is generic (`Cannot read properties of undefined`), it carries no signal by
itself — pair it with the property name, the library, and the operation. Two weak fragments quoted
separately beat one long quoted sentence that no page contains verbatim.

### A current API surface

```
site:<official-docs-host> "<symbol>"
<library> <version> "<symbol>" reference
repo:<org>/<repo> "<symbol>" path:*.d.ts
```

For a signature question, inspect the applicable type definitions and source alongside the docs. Match the release and configuration; source from another version can also mislead.

### When a behaviour changed

```
<library> changelog "<feature>"
site:github.com <org>/<repo> releases "<feature>"
<library> "breaking change" <version-from> <version-to>
repo:<org>/<repo> "<feature>" is:pr is:merged
```

A merged PR provides the diff and discussion. Verify inclusion in a release tag before asserting when the change shipped.

### A migration between versions

```
<library> migration guide <from> to <to>
<library> "upgrade guide" v<to>
site:github.com <org>/<repo> "<from>" "<to>" codemod
```

Check for an applicable official migration guide or codemod before planning manual migration work.

### Comparing two tools

```
<a> vs <b> <specific-dimension> <current-year>
site:github.com <a>/<a> issues "<b>"
<a> "why we moved" OR "migrated from" <b>
```

Use comparison pages as leads to evidence about the specific dimension. Product docs establish documented behavior and vendor assertions; issue threads and practitioner post-mortems can reveal conditions and limitations. Inspect methods and applicable workloads for empirical comparisons rather than assuming vendor neutrality or practitioner authority.

### Security, CVEs, advisories

```
CVE-<year>-<number>
site:github.com/advisories <package>
<package> security advisory <version>
```

For a dependency, `npm audit` / `pip-audit` / `cargo audit` and the GitHub advisory database are
primary and structured; a general web search is the fallback, not the entry point. Always confirm
the affected version range against the advisory itself rather than a summary.

### Specs and standards

```
site:w3.org OR site:whatwg.org "<term>"
"RFC <number>"
<spec-name> filetype:pdf
```

Specs answer "what is required" and "what is undefined". They do not answer "what do browsers
actually do" — for that, pair the spec with the implementation status pages and, where it matters,
with a test.

### An unfamiliar term or acronym

```
"<term>" <domain-word> -site:<the-wrong-domain-that-dominates>
"<term>" glossary OR definition site:<authority>
```

The exclusion is doing the work here: most collision problems are one dominant unrelated meaning,
and one `-term` resolves it faster than three reformulations.

## Query hygiene

- **One question per query.** A query carrying two questions returns pages that answer neither well.
- **Nouns beat sentences.** The engine matches documents, and documents contain nouns.
- **Start with the version-bearing noun and relevant major version.** Add the precise release when the behavior is patch-specific; broaden a sparse query without broadening the claim's applicability.
- **Escalate specificity, do not restart.** If a query is too broad, add one operator. If it returns
  zero, remove one constraint. Rewriting from scratch loses what you learned.
- **Three variants, then reframe.** A fourth reformulation of the same framing is sunk cost. Change
  the artifact, the vocabulary, or the surface (source, issues, changelog, spec).
- **Note the query that worked.** In a multi-step research task, the successful query shape usually
  generalises to the next question in the same domain.
