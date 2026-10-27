# Native role routing

Select the active project's required specialist before a generic role. Confirm the role exists in the session and inspect its native definition before relying on model or tool behavior.

| Task | Bundled Claude role | Boundary |
| --- | --- | --- |
| External research or fresh independent challenge | `worker-researcher` | Source reads and web tools; no shell or edits. |
| Read-only diagnosis or independent review | `worker-investigator` | Source reads/search only. |
| Skill content, lifecycle or metadata | `skills-author-worker` | Assigned files and static checks. |
| Implementation or integration | `opus-worker` | Explicit file ownership and focused checks. |

These definitions live in the configuration repository's `agents/` directory and install under `~/.claude/agents/` or `<project>/.claude/agents/`. They use `model: inherit`. Preserve the root model and do not pass an override merely to change worker cost. A recipient may deliberately configure an available model in native metadata after reviewing account compatibility.

Supply only the relevant skill paths, why they apply, dependency results and acceptance. The parent supplies research CLI results to the no-shell researcher. Workers are leaves; the parent alone dispatches and integrates. Policy prose does not establish native enforcement. Restart after installation and inspect `/agents`; report unavailable roles rather than inventing them.
