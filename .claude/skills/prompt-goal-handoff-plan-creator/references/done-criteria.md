# Done criteria

Read this when writing the plan premise, goal, prompt's completion section or a stage's acceptance. This is an adopted rubric, not an empirical performance claim; see [evidence.md](evidence.md).

## Observable completion

Each criterion states the end behavior or artifact, the existing or explicitly planned proving check, its expected result, the environment/revision/data it covers and where actual evidence will be recorded. Three to seven criteria often make a readable goal; use the number the actual requirements need.

The requested outcome is complete only when each criterion has valid evidence for the delivered version. A plan, worker report, assertion or command for another environment does not establish it. A request whose deliverable is a plan can be completed by a checked plan; an implementation request needs its implementation acceptance.

## Proof levels

| Level | Establishes |
| --- | --- |
| Static | Declared shape, metadata, syntax, links and lint. |
| Fixture | Behavior for controlled inputs under stated assumptions. |
| Integration | Actual producers and consumers work together. |
| Operational | Behavior in the required host, account or device. |
| Release | The promised result is available to its intended users. |

Name the level required by each criterion. A lower level does not substitute for a higher promised level, and a goal should not require release proof when release is outside the request.

## False passes

Do not claim done from an empty ready queue, exhausted budget, a narrowed/substituted outcome, special-cased outputs, a skipped or weakened required check, fixtures standing in for a promised live environment, an unstarted command, or a passing subset. Show the actual command, exit status and deciding output when a command supplies the proof. An explicit user amendment can change acceptance; a worker or summary cannot.

## Goal writing

Open with purpose in the user's words, then number the observable end-state criteria. Name constraints and material false passes briefly. Keep the entire goal under 4,000 characters, without frontmatter or a wrapper heading. Point to the absolute installed plan.md path as the progress record, not a source of new requirements.

Example criterion: Users can export the selected records to a CSV with the documented columns; the named integration check passes on the target revision and a representative exported file matches the expected records. Replace the check with a real command from that project.

## Stop states

DONE means all requested criteria have valid evidence. BLOCKED names the missing prerequisite and affected work after independent authorized work is finished. NEEDS DECISION states the material question, options, recommended default and dependent action. IMPOSSIBLE requires supporting evidence. A stop state cannot quietly relabel an incomplete outcome as complete.

## Handoff completion

The handoff skill is complete when its requested bundle exists, its checker and affected plan-library validation pass, its lineage/index are consistent and the user has exact paths and paste order. This proves the handoff artifact, not delivery of the work it carries.
