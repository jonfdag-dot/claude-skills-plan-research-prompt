# Team Selection

Read this reference when team size, role selection, or a preset composition is part of the task. It consolidates `team-composition-patterns` v1.0.2 and its agent-type-selection and preset-teams manuals. Presets describe useful divisions of work; they do not require spawning a team for a task the root can complete directly.

The active native definitions and [native-role-routing.md](native-role-routing.md) own role choice, required project specialists, model settings, and worker policy. Verify available roles and tools before dispatch. Map an unavailable legacy role to an installed role with the needed permissions; do not install a plugin or override a native model to reproduce a preset. The root coordinates and accepts work. Workers remain leaves. A preset's lead means the root or a bounded planning or integration assignment, never permission for a worker to spawn teammates.

## Contents

- Sizing a team
- Selecting roles
- Review preset
- Debug preset
- Feature preset
- Fullstack preset
- Research preset
- Security preset
- Migration preset
- Custom teams and troubleshooting

## Sizing a Team

Start with the smallest team whose independent assignments cover the requested outcome. Count coordination, integration, tool availability, live capacity, and any approved run budget before adding a worker. These inherited ranges are planning heuristics, not quotas, automatic dispatch rules, or measured performance claims.

| Complexity | Illustrative size | Suitable work |
| --- | --- | --- |
| Simple | 1–2 | One review dimension, an isolated bug, or a small feature |
| Moderate | 2–3 | Multiple files, two or three concerns, or a medium feature |
| Complex | 3–4 | Cross-cutting concerns, a large feature, or several competing bug hypotheses |
| Very complex | 4–5 | Fullstack work, a comprehensive review, or a systemic issue with separable investigations |

The custom-team starting range of two to four workers is another heuristic. Five or more needs a concrete benefit that outweighs its additional coordination. Similar job titles are acceptable when their outputs are distinct, such as reviewers with different dimensions or investigators with competing hypotheses.

## Selecting Roles

First apply required project roles and global specialists from the native routing manual. Then ask whether the assignment needs writes, read-only code exploration, external evidence, planning, review, or investigation. Choose the installed role whose definition covers that job and verify its effective permissions. Do not infer capabilities from its name alone.

The legacy Claude types below are a compatibility guide for environments that actually expose them. The permissions describe the source roles, not a guarantee about the current session. Native definitions, sandbox restrictions, and the loaded tool schemas take precedence.

| Legacy type | Intended capabilities | Suitable assignment |
| --- | --- | --- |
| `general-purpose` | Read, write, edit, search, and shell when permitted; no assumed team tools | An ad hoc script, automation, a unique tool combination, or a job with no better installed specialist |
| `Explore` | Read and search; no implementation writes | Find files, patterns, dependencies, or architectural facts before planning |
| `Plan` | Read-only planning | Design an approach, decompose tasks, or assess architecture |
| `agent-teams:team-lead` | Read, search, shell, and verified team coordination tools; no assumed implementation writes | Root coordination, task management, integration decisions, and synthesis |
| `agent-teams:team-reviewer` | Read, search, shell, and verified task and messaging tools; no implementation writes | Dimension-specific review with structured findings, evidence, and calibrated severity |
| `agent-teams:team-debugger` | Read, search, shell, and verified task and messaging tools; no implementation writes | Test a hypothesis, collect file:line evidence, and report confidence and a causal chain |
| `agent-teams:team-implementer` | Read, write, edit, search, shell, and verified task and messaging tools | Build within owned files, follow interface contracts, and report integration points |

Claude Agent Teams role names and `/team-spawn` commands in the presets are conditional compatibility recipes. Confirm that the active environment exposes the feature, command, and types; do not assume that the feature requires or is supplied by a particular plugin. Without those surfaces, use installed native roles through the SDD task loop. Codex uses its active agent definitions and native collaboration tools rather than these Claude names or command payloads.

| Selection mistake | Repair |
| --- | --- |
| Assigning implementation to read-only `Explore` | The root reassigns the bounded write task to a permitted implementer |
| Assigning coding to read-only `Plan` | Keep planning read-only and dispatch implementation to a permitted writer |
| Choosing a generic reviewer without the requested review protocol | Supply the applicable checklist and evidence contract, or use the installed review specialist; generic roles are not inherently unable to review |
| Using an implementer for a read-only research assignment | Prefer the installed investigator, explorer, or researcher for that evidence source |

Use [task-design.md](task-design.md) for decomposition and dependencies, and the canonical [worker prompt](../implementer-prompt.md) for dispatch fields. The preset templates below add role-specific fields to that contract; they do not replace task and attempt IDs, ownership, constraints, checks, stop conditions, or the evidence receipt.

## Review Preset

The legacy command is `/team-spawn review`. The default example has three `agent-teams:team-reviewer` assignments. Select only dimensions the change requires, and always compare the change with the user's stated requirements. Use multi-reviewer-patterns (optional separately installed specialist) for checklists, finding deduplication, severity calibration, and synthesis.

| Member label | Dimension | Focus |
| --- | --- | --- |
| `security-reviewer` | Security | Input validation, authentication, injection, secrets, and relevant CVEs |
| `performance-reviewer` | Performance | Query efficiency, memory, caching, and asynchronous patterns |
| `architecture-reviewer` | Architecture | Coupling, applicable design patterns, error handling, and structural constraints |

```text
Subject: Review {target} for {dimension} issues
Dimension: {dimension}
Target: {file list or diff and delivered revision}
Checklist: {applicable dimension-specific checklist}
Output: Findings with file:line, severity, evidence, consequence, and proposed fix
```

Preserved variations are a security-focused pair (`--reviewers security,testing`), a five-dimension review (`--reviewers security,performance,architecture,testing,accessibility`), and a frontend review (`--reviewers architecture,testing,accessibility`). These flags apply only to an installed command that supports them. The root can assign the same dimensions with native tools. Intentional independent verification may overlap; deduplicate its findings rather than dropping that control.

## Debug Preset

The legacy command is `/team-spawn debug`. The example has three `agent-teams:team-debugger` assignments, or an explicitly selected count using `--hypotheses N` when supported. Labels `investigator-1`, `investigator-2`, and `investigator-3` identify separate hypotheses, not duplicate searches. Use parallel-debugging (optional separately installed specialist) for hypothesis formation, confirming and falsifying evidence, and root arbitration.

```text
Subject: Investigate hypothesis: {summary}
Hypothesis: {full falsifiable statement}
Scope: {files, module, or project}
Confirming evidence: {what would support it}
Falsifying evidence: {what would reject it}
Output: Verdict, confidence, file:line evidence, causal chain, and remaining uncertainty
```

The root can end a disproved branch or redirect it through the existing task contract. An investigator does not silently become a writer or dispatch another investigator.

## Feature Preset

The legacy command is `/team-spawn feature`. The example has one `agent-teams:team-lead` function and two `agent-teams:team-implementer` assignments. Use parallel-feature-development (optional separately installed specialist) for ownership and integration decisions.

| Member label | Responsibility |
| --- | --- |
| `feature-lead` | Root decomposition, coordination, and integration |
| `implementer-1` | Work stream one within explicit owned files |
| `implementer-2` | Work stream two within explicit owned files |

```text
Subject: Implement {work stream}
Owned files: {explicit list}
Requirements: {specific deliverables}
Interface contract: {shared types and APIs}
Acceptance: {observable checks}
Blocked by: {actual prerequisite task IDs}
```

The root owns shared files or gives each one a single writer. Two writers must not claim the same file merely because the preset calls for two implementation streams.

## Fullstack Preset

The legacy command is `/team-spawn fullstack`. The example has a lead function and three `agent-teams:team-implementer` assignments spanning frontend, backend, and tests.

| Member label | Layer and responsibility |
| --- | --- |
| `fullstack-lead` | Root coordination, contracts, and integration |
| `frontend-dev` | UI components and client behavior |
| `backend-dev` | API endpoints and business logic |
| `test-dev` | Required unit, integration, and end-to-end checks |

```text
frontend-dev ──┐
               ├──→ test-dev integration verification
backend-dev  ──┘
```

Integration verification depends on accepted frontend and backend outputs. Test design, fixtures, or isolated unit work may start earlier when their inputs are available. Do not create a blanket barrier or add a test suite merely because the preset includes a test role; the requested behavior and applicable verification policy determine the checks.

## Research Preset

The legacy command is `/team-spawn research`. The source example uses three `general-purpose` researchers; the installed native research or investigation role takes precedence for its evidence source. Separate questions or sources rather than having every worker produce the same survey.

| Member label | Example focus |
| --- | --- |
| `researcher-1` | Codebase architecture and existing behavior |
| `researcher-2` | Library or API documentation |
| `researcher-3` | External approaches, examples, or comparison evidence |

Local search can use exposed `Grep`, `Glob`, and `Read` tools or their native equivalents. External research can use exposed `WebSearch` and `WebFetch` tools or their native equivalents. These names do not establish access. The source recipe for a research worker to spawn `Task` with `subagent_type: Explore` conflicts with leaf-worker policy: the worker returns the bounded exploration question to the root, which decides whether to dispatch another assignment.

```text
Subject: Research {topic or question}
Question: {specific uncertainty}
Scope: {codebase files, retained findings, library documentation, or external sources}
Tools: {available local or external search tools appropriate to the sources}
Deliverable: Evidence-backed summary with file:line citations or source URLs
Output: Findings, alternatives, recommendation, uncertainty, and reusable evidence for the root
```

The preserved variations are three local researchers on different modules, three external researchers on different questions, or a mixed codebase, documentation, and external-source composition. A library comparison might assign the following questions; current product names, versions, and prices still require source verification, and these examples do not recommend a provider.

```text
Codebase: Trace the current authentication flow from login to token validation.
Comparison: Compare NextAuth, Clerk, and Auth0 for a Next.js app, including pricing, developer experience, and migration effort.
Documentation: Check the requested NextAuth.js v5 documentation for JWT and session behavior, and establish whether that version fits the project.
```

The root retains reasoning, synthesis, and persistence. A read-only worker returns reusable findings for the root rather than writing the library or expanding its read scope independently.

## Security Preset

The legacy command is `/team-spawn security`. The example has four `agent-teams:team-reviewer` assignments covering different attack surfaces. Apply only relevant checks within the assigned scope and never read or log secret values.

| Member label | Dimension | Focus |
| --- | --- | --- |
| `vuln-reviewer` | OWASP and vulnerabilities | Injection, XSS, CSRF, deserialization, and SSRF |
| `auth-reviewer` | Authentication and access | Authentication, authorization, and session management |
| `deps-reviewer` | Dependencies | Relevant CVEs, supply-chain risks, outdated dependencies, and license constraints |
| `config-reviewer` | Secrets and configuration | Secret names and exposure evidence, environment configuration, debug endpoints, and CORS |

```text
Subject: Audit {target} for {security dimension}
Dimension: {sub-dimension}
Target: {files, directory, or project and revision}
Checklist: {applicable security checks}
Standards: {relevant OWASP Top 10 or CWE references}
Output: File:line findings, evidenced consequence and likelihood, severity, and remediation
```

The source's CVSS-like severity is a structured aid, not an automatic high rating or a claimed numerical score. Use demonstrated consequence, likelihood, and evidence; retain unresolved disagreement in the consolidated report. Variations are a two-member quick scan (`--reviewers owasp,secrets` when supported), the four-dimension audit, or a fifth pipeline and deployment-configuration reviewer when that scope is requested. Review of deployment configuration does not authorize deploying.

## Migration Preset

The legacy command is `/team-spawn migration`. The example combines a lead function, two `agent-teams:team-implementer` assignments, and one `agent-teams:team-reviewer` assignment. Reviewers verify the delivered revision independently rather than editing implementation files.

| Member label | Responsibility |
| --- | --- |
| `migration-lead` | Root plan, coordination, ownership, and conflict handling |
| `migrator-1` | Migration stream one within assigned files or modules |
| `migrator-2` | Migration stream two within assigned files or modules |
| `migration-verify` | Verify migrated behavior and the requested replacement patterns |

```text
Subject: Migrate {module or files} from {old} to {new}
Owned files: {explicit list}
Migration rules: {required transformation patterns}
Old pattern: {what changes}
New pattern: {required replacement}
Acceptance: {relevant checks, regressions, and replacement-pattern criteria}
Blocked by: {actual prerequisite task IDs}
```

```text
migration-lead accepted plan ──→ migrator-1 ──┐
                           └──→ migrator-2 ──┴──→ migration-verify
```

Preserved use cases include React classes to hooks, Vue 2 to Vue 3 or an Angular upgrade; JavaScript to TypeScript or Python 2 to 3; REST v1 to v2 or GraphQL schema changes; ORM or database schema changes; and Webpack to Vite or CRA to Next.js. These are examples of work decomposition, not authorization to upgrade a framework, migrate data, or execute a production operation. Required planning, database specialists, and operation approvals still apply.

## Custom Teams and Troubleshooting

Give the root a concrete coordination and acceptance responsibility. Match assignments to native roles and tools, state ownership before work starts, and keep the team small enough that results can be integrated. Avoid duplicate deliverables while preserving intentional review independence. For messaging, runtime identity, lifecycle, or display choices, read only the applicable section of [team-runtime.md](team-runtime.md).

| Symptom | Bounded response |
| --- | --- |
| A read-only `Explore` or `Plan` assignment needs writes | Return the ownership and permission mismatch to the root; reassign the write task through an authorized native role |
| Coordination grows faster than useful progress | Reassess separate outcomes and actual dependencies; for example, three workers may cover six independent tasks in pairs instead of four workers with overlapping duties, but the choice depends on evidence and capacity |
| tmux panes do not appear | Check the conditional display requirements in the runtime reference, including tmux availability and the active session; use a supported alternative only within configuration authority |
| Reviewers repeatedly find the same issue | Distinguish correctness, security, and performance scopes where useful, then deduplicate results; retain purposeful overlap required for independent verification |
| A spawned teammate does not receive its assignment | Verify the actual spawn or task-delivery operation, recipient handle, and complete brief; check pending tools or idle state before assuming failure |

Do not describe all workers as starting without history. The Claude Code Agent tool starts a fresh agent unless the call selects the `fork` type; Agent Teams teammates use their own task context and need a complete brief. Codex inheritance depends on the actual spawn options; use no-history dispatch when supported and required by native policy. In every runtime, send the bounded goal, ownership, constraints, and done condition explicitly rather than relying on inherited memory.
