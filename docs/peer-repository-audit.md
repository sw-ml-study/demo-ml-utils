# Neighbor Repository Copyright, License, and Agent Guidance Audit

Audit date: 2026-08-08. Scope: Git repositories directly under `..`, all of
which had a latest commit or checkout metadata update on 2026-08-07 or
2026-08-08. “Explicit” means a declaration in the repository itself, not an
organization-level default or a wiki link to another repository.

| Repository | Copyright | License | Agent guidance | Finding |
|---|---|---|---|---|
| `demo-algorithms` | `COPYRIGHT`, README | MIT `LICENSE`, README | `AGENTS.md` with generated AgentRail briefing | Complete; primary current demo template |
| `demo-combinators` | `COPYRIGHT`, MIT notice | MIT `LICENSE` | `AGENTS.md` | Files are explicit; README does not surface them |
| `demo-funtional-pipelines` | none found | none found | `AGENTS.md` with AgentRail rules | Missing explicit copyright and license; repository name also contains the existing `funtional` spelling |
| `demo-memory` | `COPYRIGHT`, README | MIT `LICENSE`, README | `AGENTS.md` with generated AgentRail briefing | Complete |
| `sw-mlpl` | `COPYRIGHT`, README | MIT `LICENSE`, README | `AGENTS.md` and `CLAUDE.md` | Complete; two instruction targets are project-specific, not a requirement for demos |
| `sw-mlpl.wiki` | none found | no local license file or declaration | no `AGENTS.md` or `CLAUDE.md` | Missing explicit local copyright/license and agent guidance; a page links to `sw-mlpl` terms but does not state that they govern the wiki |
| `demo-ml-utils` (before this audit) | none | none | none | Remediated by this bootstrap |

## Applied here

This repository adopts the neighboring projects’ `Copyright (c) 2026 Michael
A Wright` notice and MIT license. Its README links both authoritative files.

Agent guidance combines the generated AgentRail briefing with relevant demo
rules: TDD, thin task-runner entry points, pure MLPL logic separated from
effects, no implicit upstream edits, explicit binary/security boundaries,
bounded-memory evidence, and layer-attribution for native/external work.
Only `AGENTS.md` is targeted to avoid duplicated guidance.

This audit does not change neighboring repositories. Their gaps require a
separate, explicitly scoped update.
