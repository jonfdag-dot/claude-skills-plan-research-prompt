# Shared plan library

Keep one durable planning home across active source projects. Start with [projects.md](projects.md), then the project's `ROLES.md`; read the first 100 lines and expand only for relevant continuation. [CLAUDE.md](CLAUDE.md) is the short behavior contract. [INDEX.md](INDEX.md) maps the files; it is navigation rather than another plan register.

## Layout and file roles

```text
llm-plan-links/
  CLAUDE.md / AGENTS.md
  README.md / INDEX.md
  projects.json / projects.md
  starter-example/
    ROLES.md
    YYYY-MM-DD-example-plan.md
    complete/deferred/ and complete/eval-runs/
    eval-runs/ and reviews/ and .session/
  scripts/
    roles.py / validate.py
    templates/plan.md.template
    templates/project-CLAUDE.md.template
  tests/test_roles.py and tests/test_validate.py
```

`projects.json` owns machine-readable registration and `projects.md` provides the human source-repository map. One `ROLES.md` owns each project's current plan pointers, priority and next action. A plan owns its intent, decisions, current state and evidence. The starter example is explicitly illustrative and remains a reference row.

## Register any active project

1. Add a `projects.json` entry with `id`, `source_root`, `plan_directory`, `imports: []`, `legacy_subtrees: []`, `live_in_complete: []`. Use a real absolute source path, `~/...`, or a source path relative to this library root. Runtime config roots conventionally use `claude` as the ID for `.claude`.
2. Add the human row to `projects.md`. Create the project folder and copy the five empty ROLES sections from the starter example, clearing its reference row and counts.
3. Create `complete/`, `complete/deferred/`, `complete/eval-runs/`, `eval-runs/`, `reviews/` and `.session/`; keep empty directories with `.gitkeep` where needed. Keep private session state out of commits; only the empty scaffold belongs in the starter.
4. Merge the routing paragraphs from `scripts/templates/project-CLAUDE.md.template` into the active project's instructions, replacing every path and ID with its installed value. Keep that project's architecture, build/test commands and approvals.
5. Run the validator. Do not install a second plan store or make application code depend on this library.

## Plan lifecycle

Copy `scripts/templates/plan.md.template` into the owning folder under a UTC date and descriptive subject. Replace every placeholder and register it in ROLES. A bundle uses the same dated name as a directory, with `plan.md` as its main file. Handoff templates live in the configuration repository's handoff skill.

Every plan has `status: in_progress`, `created: YYYY-MM-DD` and an empty `completed:`. After the title, state purpose and observable done. Include Status, Decisions and Discoveries; record real evidence and uncertainty rather than invented passing output.

Verified completion sets `status: complete` and `completed`, moves the artifact intact to `complete/` and updates links/indexes. Full supersession sets `status: superseded`, `superseded_on` and `succeeded_by`, retaining unfinished work honestly. Deferred work keeps `in_progress` in `complete/deferred/` with a reopening trigger. Preserve history and active partial responsibilities.

## ROLES index

Use the columns `Role | State | Priority | Updated | Plan / folder | Brief summary`. Sections appear in this order: Current work, Current references, Deferred, Superseded, Complete, Directory meanings. Each section retains its empty table when unused. A row has one Markdown link to the main file.

Current work sorts priority `now`, `next`, `later`, then newest UTC date, role and target. Other sections use priority `-` and sort newest date first. Unknown dates are `UNKNOWN`. Valid role states are `in_progress`, `blocked`, `reference`, `deferred`, `superseded`, `complete`; these describe the role while plan frontmatter describes implementation lifecycle. Keep the header counts and current/reference continuation beyond line 100 exact.

Run these commands from this repository:

```sh
python3 -B scripts/roles.py head starter-example
python3 -B scripts/roles.py list starter-example --section references --json
python3 -B scripts/roles.py resolve starter-example --role 'example reference' --runtime claude --json
python3 -B scripts/validate.py .
python3 -B -m unittest discover -s tests -v
```

The role reader writes nothing, follows registered successor chains and returns exact reading paths. `--root <library>` supports another installed location. The validator checks registry, names, frontmatter, placement, successors, role metadata and handoff goal length; it also requires the instruction mirrors to match and stay within 200 lines. Relative or home-relative source roots are resolved by the adapted scripts, so moving this whole kit preserves the illustrative registration. Structural checks do not establish product delivery.

## Use with research and handoffs

Search [the shared research library](../llm-research-links/README.md) before new web work. A plan cites the R-ID and supported clause for each deciding finding. Reusable evidence stays in that library; implementation decisions and progress stay here.

For a fresh-session handoff, request the handoff skill, preserve actual user intent and approvals, and create `plan.md`, `prompt.md`, `goal.md` plus needed dated references. State lives only in plan Status. Validate, give the exact files and paste the prompt before the goal. A handoff never supplies operational approval.
