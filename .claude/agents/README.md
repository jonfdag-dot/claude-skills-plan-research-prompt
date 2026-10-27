# Native workers

| File | Use | Available tool boundary |
| --- | --- | --- |
| [worker-researcher.md](worker-researcher.md) | Bounded external research or a fresh challenge. | Read, Glob, Grep, WebSearch and WebFetch; no shell or file mutation tools. |
| [worker-investigator.md](worker-investigator.md) | Read-only diagnosis or independent review. | Read, Glob and Grep; no shell or file mutation tools. |
| [opus-worker.md](opus-worker.md) | A bounded implementation task. | Read, search, shell and editing tools, subject to the session's permissions. |
| [skills-author-worker.md](skills-author-worker.md) | Skill authoring and static checks. | Read, search, shell and editing tools, subject to the session's permissions. |

All workers use `model: inherit`. The historical implementation-role name does not pin a model. Choose a sufficiently capable parent for consequential research; if you want a fixed model, select an available native alias or model ID deliberately and verify it against your installation. No call-site downgrade or extra paid model experiment is assumed.

Workers do not preload a skill roster. The parent names relevant skill paths and supplies the library CLI results a no-shell worker needs. Leaf behavior is policy guidance; the listed native tool allowlists constrain tool access. The definitions do not install a spawn hook, change approval settings, or guarantee isolation of external side effects.

After merging these definitions, start a new session and inspect `/agents`. Give one worker a bounded question with a clear done condition. The parent reads the decisive evidence, integrates the result and owns any library writes.
