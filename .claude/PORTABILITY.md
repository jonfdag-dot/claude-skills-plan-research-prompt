# Portability and provenance

These are adapted copies of an existing Claude skill collection, rather than a dump of a personal configuration directory. The export preserves each selected capability and useful source references while replacing machine-specific integration rules.

## Intentional changes

Library homes use the documented default `~/llm-plan-links` and `~/llm-research-links`; Markdown reading links use relative paths so the kit can move as a unit. Existing project names, product registries, private directories, deployment exceptions, historical reports and source evidence were excluded. Native worker definitions were adapted for this generic distribution and inherit the main model instead of preserving account-specific model pins.

Skill creation uses native Claude skill discovery and the maintained `skills/INDEX.md`. The original machine's generated curation, BM25 router, routing probes, pool launchers and global spawn allowlist are outside this distribution. Existing recipient hooks still apply. Optional evaluation engines, model campaigns and transcript extraction were excluded; static verification does not authorize them.

The handoff skill uses current-session user messages and user-supplied earlier prompts; it does not scan session archives. The independent research worker receives library results from the parent because it has no shell. Unsupported domain skills named in retained discussion are optional leads, not installed requirements.

Codex parity is `DOCUMENT_ONLY / N/A`: this is a Claude-only scope with no Codex runtime provisioned. No Codex files, private runtime settings, hook enforcement, secrets, session logs or personal memory are included. A future Codex port must translate native discovery, tools and permissions separately.

The plan validator preserves lifecycle, role, successor and registry checks; its original exact instruction-line count was replaced with equality and a 200-line upper bound for the starter instructions. The research CLI's project-name examples were changed to generic labels. Existing deterministic tests are included with portable fixture names. Source-root readers additionally accept home-relative and library-relative paths so the sample registration survives moving the kit. The source research pilot and its packet-assessment helper/test were excluded together. Source-root readers additionally accept home-relative and library-relative paths so the sample registration survives moving the kit. The source research pilot and its packet-assessment helper/test were excluded together.

## Rights and checks

The copied skill-creator Apache 2.0 license remains at `skills/skill-creator/LICENSE.txt`; its terms cover the material to which that license applies. This export does not assign a new blanket license to unrelated material. Keep any existing notices and review rights before republishing beyond the requested personal sharing.

`export-manifest.json` records source-relative resource names, source SHA-256, delivered SHA-256 and whether adaptation occurred. Source paths identify skill-relative resources only. Root documentation and generic examples were authored for this kit.

Offline structural checks establish file consistency and path integrity. They do not prove native discovery, factual truth, external URL liveness, model compliance or recipient permissions. Run a fresh local Claude session to verify installation.
