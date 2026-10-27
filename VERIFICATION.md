# Export verification

The checks below cover the delivered starter, not the recipient's future installation. Native Claude activation and recipient-specific permissions remain manual checks. The public distribution tracks all three components in one Git repository; the structural checks below cover the shipped files.

| Check | Observed result |
| --- | --- |
| Plan library validator | Passed. |
| Plan role reader and relative source-root example | Resolved the illustrative role to its main file and actual reading paths. |
| Planning regression suite | 129 tests passed. |
| Research library validator | Passed after adding the local starter-format example. |
| Research regression suite | 67 tests passed. |
| Research CLI retrieval | Domain labels, bounded find and show resolved R-0001; named topic check passed. |
| Skill metadata | All nine SKILL.md entrypoints passed the bundled quick validator. |
| Python syntax | All shipped Python files parsed. |
| Local Markdown links and fences | Checked after all documentation and references were written. |
| Privacy/content screening | Checked for source-machine username, personal project/repository names, private absolute homes, secret-like values and excluded runtime state. No matching content retained. |
| Git layout | One parent repository includes all three component directories as regular tracked files, with no nested repositories or gitlinks. |
| Relocation | Extracted archive validators and the sample role resolution passed from a temporary location. |
| ZIP | Contains the full hidden .claude tree and both libraries; Git metadata and runtime caches excluded; CRC checked. |

The export uses adapted copies and generic examples. Original live repositories and installed configuration were left unchanged. The research sample's Checked UNKNOWN is deliberate: it documents local format and implies no external inspection. The tests and validators establish structure and tool behavior, not factual truth or model compliance.

After installing, start a fresh local Claude session, inspect `/memory` and `/agents`, and invoke a relevant skill. That recipient-specific discovery, permission and model-availability check remains manual. Review paths before merging with an existing setup.
