# App Delivery Engine — agent and contributor agreement

Applies to ChatGPT, ChatGPT Work, Codex, assistants, and human contributors. The repository and existing draft PR are authoritative; past conversations are not.

1. Read `README.md`, `docs/ARCHITECTURE.md`, `docs/METHOD-SELECTION-V1.md`, active PR and CI evidence before editing.
2. Read [Senior Engineering Operating Contract v1](docs/SENIOR-ENGINEERING-CONTRACT-V1.md), including the **observable pragmatic staff-engineer traits and seven-field decision record**: assess architecture, tradeoffs, overlooked risks, tests, operations, user outcomes and clean handoffs; do not equate a green test with readiness.
   Before claiming any idea-to-release capability, read [Application Lifecycle Benchmark v1](docs/APP-LIFECYCLE-BENCHMARK-V1.md), classify the lifecycle stage and verify real artifacts/approval gates. A task-level method selector is not an end-to-end product lifecycle.
3. Select **one** bounded task kind and all known risks using `ade.method_selection.select_method`. This is a decision aid: unknown or disputed risks require human review, never automatic minimization.
4. Compose the core delivery controls and the task/risk-specific controls; never pick a weaker methodology to save effort. Prefer minimal vertical slices, existing code/tests, deterministic generation and proven licensed mechanisms.
5. Run positive, failure, security-boundary and relevant concurrency/restart tests. Verify source against exact commit SHA and complete GitHub Actions logs. Do not infer success without actual evidence.
6. Keep changes in the existing draft PR where possible. Document any justified exceptions. Every app owns its runtime and product logic; do not import whole external orchestration frameworks.
7. GitHub is the handoff: record milestone, decisions, code paths, commit SHA, CI URL/results, outstanding risks, approvals and exact next action. Other agents must read this handoff before continuing.
8. **Stop at governance gates.** Do not merge, deploy, publish, use production credentials, spend money, invite external reviewers, change branch protection/approval policy or bypass security checks without explicit authorization.
9. Never claim mocked OAuth tests establish a live IdP, that a green unit test means production ready, or that a self-review is independent authority.
10. Do not automatically promote code from a single benchmark. Compare multiple application implementations, verify reuse value, licensing, risks and negative tests before extracting shared mechanisms.
11. **Infrastructure neutrality:** The App Delivery Engine must not require DigitalOcean, Supabase or any specific cloud/database provider. Application repositories own hosting choices, credentials, deployment manifests and runtime adapters. Preserve swappable contracts and never infer approval to provision infrastructure from a passing test or an application-level provider preference.

## Ease-of-use and working-application priority

Read [Delivery Usability Milestones](docs/DELIVERY-USABILITY-MILESTONES-V1.md) before adding templates, dashboards, orchestrators or more AI intelligence. **First prove a real usable application**, measure fresh-user first-run steps, and preserve exact-HEAD browser/data tests. Prefer fixing observed friction in the existing `web-list` generator over adding a new framework. Do not confuse a requirements-only bootstrap with a working application. Statuses D0–D8 are evidence-based stage gates, not automatic permissions.

## Multi-interface architecture and truthful commands

Before adding a new CLI, script, agent skill, API or dashboard action, read [Delivery Engine Architecture v1](docs/DELIVERY-ENGINE-ARCHITECTURE-V1.md) and [registered commands](registry/commands.json). Every interface must share one set of validated command contracts, authority checks, execution rules and evidence. The current catalog lists only genuine existing operations; proposed workflow names are **not** executable. Do not create a second approval system or invent a dashboard-only source of truth. Start with read-only preflights and benchmark UI usefulness before building a dashboard.

## Mandatory bootstrap, continuity and ownership policy

Read [Benchmark-to-Ownership Policy](docs/BENCHMARK-TO-OWNERSHIP-POLICY.md) before deciding to replace a dependency or promote product-specific code. Evidence must be recorded in `registry/benchmarks.json`, `registry/capabilities.json` and `registry/lessons.json` with real provenance; never assign independent approval to an AI.

For a **new application idea**:
1. Validate a strict brief and run `python -m ade.bootstrap_cli plan examples/vrs-bootstrap.json` (substitute a reviewed product brief). Do not create an actual GitHub repository or spend money without authorization.
2. Run `python -m ade.bootstrap_cli create <approved-brief.json> <new-empty-local-directory>`. It must never overwrite existing files.
3. Open the new `AGENTS.md`, `project.yaml`, `delivery/current-state.yaml`, decisions, risk register and acceptance criteria, then execute `python tools/startup.py`.
4. A STOP is a valid safety outcome. Ask for explicit requirements approval before implementation. A local CONTINUE is only a preflight; GitHub HEAD/CI/review must be separately checked.
5. Next independent Work/Codex/human contributor must repeat startup. No agent may edit delivery evidence to fake remote CI success, merge/deploy approvals or reviewer authority.

Bootstrap is an **offline starter**, not a ready VRS implementation or an automated GitHub repository creator. Follow [Bootstrap & Continuity M1](docs/BOOTSTRAP-CONTINUITY-M1.md) and the senior engineering contract. Maintain provider neutrality and keep telecom/media implementations in app repositories.

Current work: `gergins/app-delivery-engine`, draft PR #1, branch `feat/m0-minimal-app-delivery`; inspect current HEAD and CI for latest state. Read [the documentation map](docs/INDEX.md) and [recovery benchmark](docs/RECOVERY-CROSS-APP-EVIDENCE-V1.md) before expanding capabilities. Prefer verifying the existing recovery path and improving actual first-run usability over new orchestrators.

The senior engineering contract is advisory, not a substitute for CI, independent review or explicit authority. Continue to use the exact existing approval stop gates.
