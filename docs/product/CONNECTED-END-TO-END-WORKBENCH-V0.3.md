# Connected End-to-End Workbench Contract v0.3

Status: prototype and proposed integration. Fincept is a fixture, not an architectural dependency. The neutral core is goals, projects, artifacts, items, relations, evidence, authority and checkpoints. Continuity, BDD, open-source discovery, planning, design, review and all driven methods are optional/selectable capabilities.

## Non-negotiable trace chain
Project → goal/outcome → source snapshot → observed element/component → interpreted capability → requirement → acceptance example / scenario (BDD optional) → screen/UI state → API / data / domain event → implementation artifact → test / environment → evidence → decision and handoff. Every item has stable scoped ID, kind, provenance, lifecycle status, accountable owner and exact source/build revisions where applicable. Typed directional edges include derivesFrom, mapsTo, implementedBy, testedBy, dependsOn, blockedBy, conflictsWith, approvedBy and supersedes. Unmapped and unknown are first-class.

## Visibility and integrity
Do not confuse source-registered screens with demonstrated UI; extracted symbols with verified capabilities; drafted requirements with approved requirements; synthetic mock with running app; recorded test URL with a passing test; passing test with deployment authorization. Make all transitions reviewable with details, evidence and unanswered questions.

## Slice readiness
**Research→requirements:** pinned evidence, capability purpose, screen/source mapping or explicit unmapped status, review acknowledgement, provenance and open questions.
**Requirements→first executable slice:** concrete actor and task, minimal happy path + consequential error path, observable acceptance, data/permissions, dependencies, risks and approval of scope; BDD may be used but is not mandatory.
**Build→verification:** actual implementation at exact commit, runnable test fixtures, real browser interaction, reproducible environment and matching tests.
**Verification→handoff:** reviewed results/screenshots/trace, tested exception and accessibility behavior, documented gaps, suitable approval, rollback/continuity. No automatic merge/deploy/spend.

## Visual iteration and previews
0. Research/extraction viewer (static evidence only).
1. Clearly labeled synthetic wireframe/screen mock; show selected requirement and missing links.
2. Isolated component states using Storybook where valuable.
3. Real app in local or ephemeral preview (Next.js dev server / Vite as appropriate); seed synthetic data, no live money/brokers.
4. Playwright browser screenshot/trace and console log linked to scenario + exact commit.
5. Ephemeral PR-specific review preview behind access controls. Promotion only after gate checks/authorization.
Every preview exposes type, environment, app revision, data provenance, verified status, interactions and a quick return to linked requirement or decision.

## Available prototype v0.3 (conversation artifact, not yet committed as app)
Offline single-page HTML visual workbench, with real static extracted Fincept fixture. Implements: selectable views and methods, 23-capability inventory, source/screen trace, drafted requirement + acceptance + optional scenario, reviewed flag, requirements readiness, synthetic mock interaction, manual implementation/test claim fields, checkpoint notes, JSON handoff export. JavaScript syntax check passed; Chromium Playwright verified UI render, navigation, requirement-to-trace propagation, review gate, mock interaction and screenshot. Normal URL navigation blocked by test environment, so set_content was used; browser restart/export and real integration not independently verified.

## Next first-slice implementation
Build safe import parser and normalized Postgres records/typed links; render actual evidence-linked source→capability→requirement→screen→implementation→test graph; persist exact user return context with revisions and conflict detection. Show side-by-side running isolated app preview and source-backed acceptance matrix. Verify using Playwright at exact HEAD. Open-source reuse: React Flow if graph editing adds value; Storybook for components; Playwright for reproducible UX evidence; existing React/Next.js and Postgres preferred. Never introduce infrastructure without measured need.

## Test fixture notes
Fincept sample extraction source revision 623c61db169ea550b4351dd6a7fb69fb608ba2cc; 23 curated capabilities, 52 registered screen identifiers, 13 proposed gaps. Static structure, not proven runtime behavior.
