# Adopt the research and planning framework

Connect one existing project to shared research and plans, then use the same setup for additional projects. You need Claude Code and Python 3.11 or newer for the bundled tools.

## 1. Put the libraries in a shared home

Copy the complete `llm-plan-links/` and `llm-research-links/` folders to `~/llm-plan-links/` and `~/llm-research-links/`. Include hidden files and empty directory scaffolds. If those locations already contain libraries, compare and merge the contents before proceeding.

Keep research findings in the research library and project intent, decisions and progress in the plan library. Your application source stays in its existing repository.

## 2. Add the Claude skills

For use across projects, merge this kit's `.claude/skills/` into `~/.claude/skills/`. Merge the shared conventions from [.claude/CLAUDE.md](.claude/CLAUDE.md) into your existing `~/.claude/CLAUDE.md`. Compare files with matching names before replacing them.

For use in one project, put the skills in that project's `.claude/skills/`, and merge the shared conventions into its root `CLAUDE.md` instead. Keep the two libraries at their shared locations.

Copy whole skill folders so their references, templates and scripts stay together. The [skill index](.claude/skills/INDEX.md) explains the eight workflows.

If you choose different library locations, update paths in the copied instructions and skills. Relative links between `.claude/` and the libraries assume they are siblings. For a project-local installation with libraries in your home directory, replace those library links with the installed paths.

## 3. Connect your first project

Open Claude Code in the source project you want to work on. Use the [project instruction template](llm-plan-links/scripts/templates/project-CLAUDE.md.template) to add the research and planning routes to its existing `CLAUDE.md`. Fill in the actual project purpose, stack, entrypoints, build and test commands, library paths and project boundaries.

Register the project in the plan library's `projects.json` and `projects.md`, then create its plan folder and `ROLES.md`. The [registration instructions](llm-plan-links/README.md#register-any-active-project) specify the fields and directory scaffold. `ROLES.md` points to the project's current plans so the next session knows where to resume.

You can ask Claude to make these setup edits. Replace the placeholders in this request with your paths:

```text
Connect this project to the research and planning framework at <kit-path>. The installed libraries are <plan-library-path> and <research-library-path>. Read their setup instructions, register this source repository in the plan library, and create its plan folder and empty ROLES index. Merge the library routes into this project's CLAUDE.md while preserving its existing instructions. Report the files changed and any remaining setup steps.
```

The bundled `starter-example` plan and R-0001 research finding show the file formats. Use your own project registration and evidence for actual work.

## 4. Start with one real task

Start a fresh Claude Code session in the connected project after installing the skills. Use `/memory` to inspect the loaded instructions, then invoke a relevant skill.

Choose a task with a concrete outcome. For a decision that needs research, start with:

```text
/web-research Investigate <question> to help decide <decision>. Search the shared research library first, investigate the remaining gaps, and retain reusable findings with their sources.
```

When you are ready to plan implementation, ask:

```text
Create a plan for <outcome> in this project's registered plan-library folder. Define done, cite relevant research findings, and update ROLES.md with the next action. Wait for my implementation request after presenting the plan.
```

Review the plan, then ask Claude to implement it. During implementation, keep decisions and progress in the plan and reusable evidence in the research library. Routine small edits can proceed directly without a durable plan.

## 5. Resume the work in another session

Before switching sessions, request:

```text
/prompt-goal-handoff-plan-creator Create a continuation handoff for this project's current work, including completed changes, remaining work, constraints and the next executable action.
```

Open the resulting bundle and paste `prompt.md` into the new session first, followed by `goal.md`. The bundle's `plan.md` holds the current state.

To adopt the framework in another project, repeat the project connection step with a new registration. Reuse the installed skills and shared libraries.

[Browse the skills](.claude/skills/INDEX.md) · [Research library guide](llm-research-links/README.md) · [Plan library guide](llm-plan-links/README.md) · [All files](FILES.md)
