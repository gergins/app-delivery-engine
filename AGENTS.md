# App Delivery Engine — agent and contributor agreement

Applies to ChatGPT, ChatGPT Work, Codex, assistants, and human contributors. The repository and existing draft PR are authoritative; past conversations are not.

1. **Start with the smallest relevant context:** inspect the active repository/branch/PR, changed code, applicable tests and current GitHub evidence. Use this file as the entry point; open the relevant sections of `README.md`, [documentation map](docs/INDEX.md), architecture or method guidance **only when the task depends on them**. Do not read every document for a trivial edit.
2. Apply the [Senior Engineering Operating Contract v1](docs/SENIOR-ENGINEERING-CONTRACT-V1.md) proportional to the task: own the accepted user outcome, examine meaningful alternatives, test the complete relevant behavior and leave a verifiable handoff. Read the [Application Lifecycle Benchmark v1](docs/APP-LIFECYCLE-BENCHMARK-V1.md) for cross-stage, release or idea-to-delivery claims; task-level method selection alone is not lifecycle readiness.
3. Select **one** bounded task kind and all known risks using `ade.method_selection.select_method`. This is a decision aid: unknown or disputed risks require human review, never automatic minimization.
4. Compose the core delivery controls and the task/risk-specific controls; never pick a weaker methodology to save effort. Prefer minimal vertical slices, existing code/tests, deterministic generation and proven licensed mechanisms.
5. Run positive, failure, security-boundary and relevant concurrency/restart tests. Verify source against exact commit SHA and complete GitHub Actions logs. Do not infer success without actual evidence.
6. Keep changes in the existing draft PR where possible. Document any justified exceptions. Every app owns its runtime and product logic; do not import whole external orchestration frameworks.
7. GitHub is the handoff: record milestone, decisions, code paths, commit SHA, CI URL/results, outstanding risks, approvals and exact next action. Other agents must read this handoff before continuing.
8. **Stop at governance gates.** Do not merge, deploy, publish, use production credentials, spend money, invite external reviewers, change branch protection/approval policy or bypass security checks without explicit authorization.
9. Never claim mocked OAuth tests establish a live IdP, that a green unit test means production ready, or that a self-review is independent authority.
10. Do not automatically promote code from a single benchmark. Compare multiple application implementations, verify reuse value, licensing, risks and negative tests before extracting shared mechanisms.
11. **Infrastructure neutrality:** The App Delivery Engine must not require DigitalOcean, Supabase or any specific cloud/database provider. Application repositories own hosting choices, credentials, deployment manifests and runtime adapters. Preserve swappable contracts and never infer approval to provision infrastructure from a passing test or an application-level provider preference.


## Universal engineering invariants (proposed, review branch)

For consequential design or implementation decisions, consult [Universal Engineering Invariants Contract v1](docs/UNIVERSAL-ENGINEERING-INVARIANTS-V1.md) alongside the existing senior-engineering contract. **Declare under-determined semantic or interface decisions before dependent code**, link each decision to the existing PR/decision record (not a second ledger), and under `ASK=semantic` seek the actual authorized owner's resolution before implementing the affected meaning. Unrelated, delegated work may proceed.

Before feature work, establish the F0 runnable entry-to-artifact spine and its evidence; expand F1…Fn only while cumulative acceptance/negative checks remain green at the same exact HEAD. The pure `ade.invariant_gate.assess_invariant_records` checks **caller-supplied** decision/rung records; its tests are included in ordinary `python -m unittest discover -s tests -v`. It cannot discover missing decisions, authenticate approvals, run the F0 browser path, or replace CI/security/review approval. These checks remain **advisory** and introduce no new mandatory PR gate or authority.

## Required senior-engineering decision loop

For each meaningful milestone, **own the user outcome within delegated authority**, not just the requested code edit. Apply [Product ownership, discovery and continuous engineering judgment](docs/SENIOR-ENGINEERING-CONTRACT-V1.md#product-ownership-discovery-and-continuous-engineering-judgment):

1. **UNDERSTAND / DISCOVER:** verify the intended user journey, current code and observed friction; explicitly separate facts, assumptions and missing failure/accessibility/operational scenarios.
2. **COMPARE / DECIDE:** evaluate finish, repair, reuse, simplify, build, defer or stop. Select one bounded, dependency-aware slice by user value, risk, effort, reversibility and lifetime cost; state the rejected alternative and why.
3. **HYPOTHESIZE / DELIVER:** define a falsifiable user-facing acceptance condition, then implement the smallest complete UI/API/data/operations seam as applicable, with negative paths.
4. **VERIFY / LEARN:** test real behavior at the appropriate assurance level, inspect exact-HEAD CI, capture usability feedback when feasible and revise decisions when evidence contradicts assumptions.
5. **ACCEPT / REPAIR / DEFER / STOP:** declare the quality bar (demo, internal trial or release candidate), residual defects/technical debt, specific reason to continue or stop, next permitted action and human approval boundary.

Use the **existing seven-field decision record and current PR handoff**; do not create a second status document, new workflow or artificial approval gate. A mock/CI success is not user acceptance, a finished isolated component is not a completed journey, and advisory instructions are not enforceable authority checks.

**Permission-aware autonomy:** within an already authorized work scope, inspect, reason, run disposable/synthetic local tests and propose focused repairs without repeatedly requesting approval for every harmless step. Before any mutation, confirm its scope and prior authorization. Do not infer authorization for repository creation, branch/PR changes outside the accepted scope, merging, deploying, spending, production secrets, external reviewers or protection changes. Unclear or consequential operations stop for the actual owner; a local PASS never grants new authority.

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

## Engineering collaboration v1 — select the smallest useful discussion

Use the existing decision record and PR handoff; do **not** create an agent council, separate discussion service, meeting requirement, or additional approval authority. The accountable technical lead is the decision integrator within delegated scope, and the implementer remains responsible for verifiable results.

- **FAST:** A bounded, reversible, understood edit with ordinary risks: senior engineer implements and verifies without convening roles.
- **REVIEW:** Conflicting technical choices, a cross-component failure, or material user-facing uncertainty: senior engineer + technical lead + only the specialist relevant to the risk (such as UX/accessibility, QA/concurrency, security or operations). Get independent *perspectives*, not simulated independent signoff.
- **COUNCIL:** Consequential architecture/product trade-off or unresolved conflicting recommendations: technical lead frames the problem and options, relevant specialists challenge assumptions, and the actual authorized owner decides anything beyond delegated authority. Stop at existing governance gates.

Discussion contract: state observed facts and uncertainties; invite distinct falsifiable alternatives; compare smallest viable solution, user impact, correctness, reversibility, cost and evidence; name a single decision owner; record recommendation, dissent if material, decisive test and stop condition in the **existing seven-field record**. Timebox by decision sufficiency: if no new evidence emerges, stop debating and perform the lowest-risk reversible experiment or escalate. Never manufacture quotes from real engineers. A “DHH-inspired simplicity critique” is a perspective derived from published engineering principles, not participation, endorsement or security authority by David Heinemeier Hansson.

On the Camping Booking trial, compare finishing one accessible availability → booking → confirmation → cancellation journey with spending further effort on generalized migration/architecture. Verify server-side conflict prevention under concurrent reservations, ownership, durable persistence, cancellation recovery, negative paths and browser use at the appropriate scope; defer unrelated payment/reporting work. Do not claim the journey or CI passed without tested exact-HEAD evidence. Measure whether the collaboration reduced decision turnaround or rework versus the ordinary path; remove it if it adds discussion overhead without observed benefit.
