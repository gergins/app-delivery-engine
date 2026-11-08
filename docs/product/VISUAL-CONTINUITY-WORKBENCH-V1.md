# Visual Continuity Workbench v1 — Product contract

Status: review proposal; not an implemented or deployed production system.

## Outcome
On opening a project, the user sees exactly where they stopped, why it matters, the active artifact, and one obvious way to continue. The user must not reconstruct context from chat transcripts, GitHub trees or disconnected tools.

## Core guarantees
1. **Resume, not browse**: one-click resume opens the last meaningful item, not simply the last page visited.
2. **Universal approach**: research, reverse engineering, requirements, BDD, design, build, test, learning and future approaches are perspectives on shared work items, not isolated silo folders.
3. **Identity and traceability**: stable work-item IDs connect purpose → source/evidence → capability → requirement → behavior scenario → screen/API → test → verified outcome.
4. **Visual clarity**: stage map, clear active location, context breadcrumbs, progress with known/unknown states, accessible text, keyboard navigation, and evidence preview.
5. **Durability**: save active project, perspective, item ID, pane/tab, scroll or anchor position, drafts, checkpoints, pending handoff, artifact version and time. Persist to durable storage; local browser storage alone is insufficient for production.
6. **Evidence provenance**: distinguish observed, inferred, proposed and verified information; source commit, file/line, license, confidence and timestamp where possible.
7. **No false completion**: status updates and handoffs require the relevant evidence; never mark unverified items done.
8. **Safe authority**: no automatic merge/deploy/spend/destructive actions; record approval requirements.
9. **Minimal first slice**: continue location + linked item perspectives + saved checkpoint before adding general dashboards.

## Minimum data contract
- project: id, repository reference, access policy, current item, updatedAt
- workItem: stable id, title, kind, purpose, status, owner, blockers, nextAction
- context: perspective, selected workItemId, artifactRef, anchor/selection, tab/panels, draftRef, savedAt, revision
- relationship: fromId, toId, type, source, confidence, status
- evidence: source URI/commit/file/line or screenshot ref, observedAt, verification result, authority
- checkpoint: who, when, project revision, exact context, what changed, open questions, next step, recoverability
- handoff: source and destination stage, item IDs, accepted evidence, unresolved risk, gate status, reviewer, version

## Main screens
1. **Return home**: last project + resume CTA + current item + next action + warnings.
2. **Journey map**: research → requirements → behavior → design → implementation → verification; branching allowed, not a rigid waterfall.
3. **Item workspace**: selected capability/requirement with linked artifacts across all approaches.
4. **BDD pane**: readable journeys and scenarios, source requirement, automation status, failing/passing evidence.
5. **Checkpoints**: browsable, revisioned recovery history, including interruptions.
6. **Handoff review**: scope, readiness, dependencies, unanswered questions, explicit approval where necessary.

## Acceptance scenarios
- Given an interrupted research session, when the user reopens the project, then the exact capability and pending action reopen.
- Given a requirement was linked to a behavior scenario, when viewed from either perspective, then both see the same stable relationship.
- Given no browser-test evidence, when a task claims completion, then status remains unverified.
- Given a malformed, stale or conflicting checkpoint, when restoring, then preserve the prior valid version and show a recovery option.
- Given a keyboard-only user, when navigating the workbench, then all core resume, select, save and review operations are reachable, with visible focus.
- Given a multi-device session, when another device changes a work item, then revisions are detected and neither edit is silently lost.

## Deliberately out of scope for first vertical slice
Custom cross-project search engine, autonomous workflow orchestration, production auth, sync service, automatic GitHub writes or CI gates. Build only after verified user need and existing-component reuse analysis.

## Demonstration
The accompanying local browser prototype is a **demo only** with browser-local state and synthetic examples. It is not evidence of connected or durable project synchronization.
