# Task Design and Dependencies

Read the relevant section when choosing decomposition, dependency patterns, task descriptions, or workload rebalancing. Delegated plan design still follows the entrypoint's mandatory [long-form-planning.md](long-form-planning.md) rule; an unchanged ready task needs only its accepted contract slice. This reference incorporates task-coordination-strategies v1.0.2 and its task-decomposition and dependency-graphs manuals.

Use [the worker prompt](../implementer-prompt.md) and [evidence-handoff.md](evidence-handoff.md) for canonical brief, receipt, acceptance, and recovery fields. Use [team-selection.md](team-selection.md) only when team composition is a decision, and [team-runtime.md](team-runtime.md) only for an applicable communication or native-tool operation. Ownership and integration strategies remain in parallel-feature-development; hypothesis investigation and review dimensions remain in their separate skills.

## Contents

- Decomposition strategies
- Dependency patterns and anti-patterns
- Task descriptions and authentication example
- Worked decomposition examples
- Workload monitoring and rebalancing
- Conditional Claude task-tool example

## Decomposition strategies

| Split | Example responsibilities | Suitable boundary |
| --- | --- | --- |
| By layer | Frontend components; backend API endpoints; database models/migrations; test suites | A full-stack feature with clear layer contracts; dependencies can limit parallelism |
| By component | Authentication; user profiles; notifications | Modular architectures or microservices with cohesive responsibilities |
| By concern | Security; performance; architecture review | Independent review dimensions or audit questions |
| By file ownership | `src/components/` for implementer 1; `src/api/` for implementer 2; `src/utils/` for implementer 3 | Parallel implementation with disjoint write boundaries |

Choose vertical slices when each owner can deliver connected behavior independently; choose layers when their contracts and ordering justify that split. Give every file one owner, define shared interfaces before dependent implementation, and avoid artificial dependencies. For detailed ownership layouts, contracts, and integration tradeoffs, use parallel-feature-development's selected manual.

## Dependency patterns and anti-patterns

Prefer shallow graphs where the actual contracts allow them. Use task-duration estimates, when available, to identify the longest path of dependent work and its critical prerequisites; a graph alone does not measure completion time. Only required producer-to-consumer relationships belong in `blockedBy`/`blocks`. A valid graph does not establish dispatch readiness: accepted inputs, decisions, ownership, authority, resources, and reachable checks must also exist.

### Independent

```text
Task A ─┐
Task B ─┼─→ Integration
Task C ─┘
```

All three tasks can run together when they have separate files/resources and compatible accepted contracts. Integration waits for A, B, and C. The risk is discovering incompatibilities late; establish interfaces before dispatch rather than assuming separation proves compatibility.

### Sequential

```text
Task A → Task B → Task C → Task D
```

Each task waits for its immediate producer. Use this when a consumer truly needs the preceding result; delays cascade and there is no parallelism within the chain. Remove a relationship if the later task can proceed from an accepted interface or fixture without claiming real-producer acceptance.

### Diamond

```text
        ┌→ Task B ─┐
Task A ─┤          ├→ Task D
        └→ Task C ─┘
```

B and C wait for A, then run together; D waits for both. Shared types are a typical A. A is a bottleneck, so separate interface readiness from later implementation where the contract permits it.

### Fork-join

```text
Phase 1: A1, A2, A3
         ──────────
Phase 2: B1, B2
         ──────────
Phase 3: C1
```

Each phase has internal parallelism; the next waits for its required preceding producers. This suits natural build, test, and authorized release stages. Phase boundaries add delay: do not block every B on every A unless all those dependencies are real. A release phase is not deployment permission.

### Pipeline

```text
Task A ──→ Task B ──→ Task C
  └──→ Task D ──→ Task E
```

B and D wait for A; C waits for B; E waits for D. The two chains can progress independently, but their approaches or interfaces may diverge. Use for independent feature branches sharing an accepted foundation.

### Circular dependency

```text
Task A → Task B → Task C → Task A
```

This deadlocks. Extract the shared dependency into a separate producer or distinguish early interface/fixture proof from later integration. Do not create a reverse edge merely because early acceptance currently references a future producer.

### Unnecessary chain

```text
Task A → Task B → Task C
```

If B does not need A's result, remove that relationship and release B independently. Keep C's actual producer relationships.

### Star bottleneck

```text
     ┌→ B ─┐
A →  ├→ C ─┤→ F
     ├→ D ─┤
     └→ E ─┘
```

Slow A delays every consumer. Investigate whether A can be decomposed without breaking the shared contract; F waits only for the results it actually needs.

## Task descriptions and authentication example

Every brief carries objective, exclusive owned files, stated requirements, producer/consumer interface contracts, observable acceptance, and exclusions. Add task/attempt/parent identity, selected native role, versioned inputs, dependencies, and stop rules through the existing worker prompt rather than inventing another schema. Shared files are owned by a designated producer and read-only to other workers.

The following concrete brief preserves the authentication example. Its password, token, and endpoint choices illustrate a supplied requirement; they are not defaults for unrelated products. Fill its acceptance with the owning project's actual checks.

```text
Objective: Build the user authentication API endpoints.
Owned files:
- src/api/auth.ts
- src/api/middleware/auth-middleware.ts
Read-only shared file: src/types/auth.ts, owned by implementer-1.
Requirements:
- POST /api/login accepts email/password and returns JWT.
- POST /api/register creates a user and returns JWT.
- GET /api/me returns the current user profile and requires authentication.
Interface:
- Import User from src/types/auth.ts.
- Export AuthResponse for frontend consumption.
Acceptance:
- Endpoints return the required HTTP status codes.
- JWT tokens expire after 24 hours.
- Passwords are hashed with bcrypt.
- The brief names the actual covering commands and expected outcomes.
Out of scope: OAuth/social login, password reset, rate limiting.
```

For another stream, substitute its objective, owned files, required behaviors, exports/imports, acceptance, and exclusions in [the existing worker prompt](../implementer-prompt.md). Do not copy the example's application requirements into that stream.

## Worked decomposition examples

### Authentication with vertical slices

The feature adds email/password authentication with login, registration, and profile pages. Establish shared infrastructure before consumers need it.

| Stream and owner | Owned files | Requirements and interface |
| --- | --- | --- |
| Login flow, implementer-1 | `src/pages/login.tsx`, `src/api/login.ts`, `tests/login.test.ts` | Login form and endpoint, input validation, error handling; imports `AuthResponse` from `src/types/auth.ts` |
| Registration flow, implementer-2 | `src/pages/register.tsx`, `src/api/register.ts`, `tests/register.test.ts` | Registration form and endpoint, email validation, password strength; imports the same `AuthResponse` |
| Shared infrastructure, implementer-3 | `src/types/auth.ts`, `src/middleware/auth.ts`, `src/utils/jwt.ts` | Type definitions, JWT middleware, token utilities; no upstream stream dependency |

```text
Stream 3 (types/middleware) ──→ Stream 1 (login)
                             └→ Stream 2 (registration)
```

The original two consumer streams do not assign the promised profile page. Resolve that requirement's owner and acceptance before calling the decomposition complete; do not silently drop it. Accepted types can permit earlier parallel consumer work, while real integration remains pending.

### Projects CRUD by layer

| Stream and owner | Owned files | Requirements | Required producer |
| --- | --- | --- | --- |
| Data, implementer-1 | `src/models/project.ts`, `src/migrations/add-projects.ts`, `src/repositories/project-repo.ts` | Schema, migration, repository pattern | None |
| Business logic, implementer-2 | `src/services/project-service.ts`, `src/validators/project-validator.ts` | CRUD operations, validation, business logic | Data model/repository |
| API, implementer-3 | `src/routes/projects.ts`, `src/controllers/project-controller.ts` | REST endpoints, request parsing, response formatting | Business service |

This example is a sequential data → service → API chain. It illustrates clear ownership, not maximum parallelism. Migration authoring and execution retain their actual project gates and authorization.

## Workload monitoring and rebalancing

| Signal | Possible cause | Next action |
| --- | --- | --- |
| One worker idle while others remain busy | Uneven distribution or no ready input | Reassign an eligible pending task or finish the worker's assignment |
| A worker stuck on one task | Missing input, decision, or concrete failure | Inspect progress and the named blocker; supply context or arrange a bounded repair |
| All tasks blocked | Dependency/readiness issue | Resolve the prerequisite on the critical path |
| One worker has roughly three times another's work | Uneven estimated work | Split or reassign cohesive pending work within scope |

Use the existing task register and live status. Identify ready work and actual capacity, confirm previous writers and mutations stopped before ownership transfer, record the transfer, and notify affected workers. Check progress at meaningful milestones; silence alone does not prove a stall, and a relative task count does not measure effort or throughput. The root owns rebalancing and dispatch; workers return blockers and proposed splits without delegating.

## Conditional Claude task-tool example

Use this recipe only when the active Claude surface exposes `TaskCreate`, `TaskUpdate`, `TaskList`, and `SendMessage` with the required schema. These names describe Claude operations; Codex must use its actual task register and native orchestration tools instead. A task update or teammate message never grants new authority.

```text
TaskCreate: { subject: "Build API endpoints" } → task 1
TaskCreate: { subject: "Build frontend components" } → task 2
TaskCreate: { subject: "Integration testing" } → task 3
TaskUpdate: { taskId: "3", addBlockedBy: ["1", "2"] }
```

The root calls `TaskList` to inspect readiness, identifies idle or overloaded workers, uses `TaskUpdate` for an accepted reassignment, and sends a direct `SendMessage` to affected workers. Monitor the resulting progress without claiming a measured improvement from the graph alone. If these tools are unavailable, maintain the same dependencies and ownership in the existing register; do not install a team plugin merely to use the example.
