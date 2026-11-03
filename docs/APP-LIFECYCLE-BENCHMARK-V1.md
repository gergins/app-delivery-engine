# Evidence-led Application Lifecycle Benchmark v1

**Purpose:** Evaluate whether a minimal, reusable App Delivery Engine can take an *idea* to a **release-ready, inspectable application deliverable**, without mistaking AI-generated code for delivered product. This is a **benchmark contract and roadmap**, not a claim that those capabilities already exist. GitHub code, issue/PR state, immutable commit tests and named human approvals are the evidence source.

## Why this sequence

Recent Camping Booking milestones demonstrated a repeating pattern:
- Beginning with a runnable user journey exposed practical needs that speculative orchestration could not prove.
- The same app required operator/customer authorization, migrations, booking races, hold expiry, real OIDC, and a separate PostgreSQL benchmark, each uncovered as evidence justified the next step.
- CI needed **exact-commit** and **actual protocol/browser/database** tests; mocks alone were insufficient.
- A PostgreSQL booking adapter test was useful but **did not** mean that sessions, holds, cancellations and recovery had migrated.
- GitHub handoffs worked best when one existing PR documented accepted work, remaining gaps and an exact next action.
- Provider choices belong to each app, not to the Engine; external credentials, independent review and deployment are approval gates.

Therefore **do not build an autonomous end-to-end production factory yet**. Prove each lifecycle transition and promote only mechanisms that recur across *different* application types. A failed/blocked stage must preserve work and context rather than produce more infrastructure.

## Lifecycle stage gates and minimum evidence

| Stage | Required decision/evidence | Failure or stop condition | Reusable engine candidate |
| --- | --- | --- | --- |
| 0. Idea intake | Problem, intended users, outcome, explicit non-goals, assumptions and owner | No coherent user problem or conflicting goals → clarification/low-risk research | Intake contract and unresolved-assumption ledger |
| 1. Validation & feasibility | Alternative solutions, simplest way to validate user value, business/regulatory viability and cost envelope | Value unproven → mock, prototype or stop; don't build a platform | Opportunity/feasibility decision record |
| 2. Requirements & scope | Personas, key journeys, functional and nonfunctional requirements, acceptance cases, risks, accessibility/privacy needs | Missing safety-critical requirement → block implementation | Versioned spec, traceability and scope guard |
| 3. Architecture & design | Build/reuse/defer tradeoffs, interface/data ownership, tenant/auth boundaries, deployment independence, ADRs, diagrams where helpful | Irreversible or unsafe decision without review → stop | Risk-aware ADR and design-review evidence |
| 4. Plan & readiness | Dependency-ordered milestones, size/priority, tests and environment setup, acceptance definition | Missing secure test environment or accountable owner → bounded safe prep | Planner and readiness preflight |
| 5. Implementation | Small runnable UI/API/data journey, accessibility, license/provenance, negative cases, reversible changes | Unreviewable size or blind framework replacement → reduce slice | Deterministic generation + bounded coding |
| 6. Verification | Unit/contract/integration/browser/provider/database/concurrency/security/restore checks selected by actual risks; exact-HEAD evidence | Missing tests, flaky/failed CI, wrong SHA or mock-only evidence for live claim → fail closed | Test selection and evidence collection |
| 7. Review | PR review, security/privacy/a11y/operational review proportional to risk, author/reviewer separation and tracked findings | Required authority absent, high-severity issue unresolved → block promotion | Review checklist + explicit approval ledger |
| 8. Release candidate | Artifact identity/version, reproducible build, data migrations, SBOM/licenses, docs, monitoring, backups, rollback, incident owner, acceptance/demo | No rollback, production secrets, contract/ops mismatch → not release-ready | Release readiness manifest, not autonomous deploy |
| 9. Deployment decision | Target host/DB/domain/region/cost, staged rehearsal, independent checks and user authorization | No explicit approval → no provisioning/merge/deploy | Provider-neutral deployment interface/approval gate |
| 10. Operations & maintenance | SLIs/SLOs, incidents, support, observability, upgrades, vulnerability response, backup/restore tests | Unowned operations or expired evidence → halt changes/escalate | Post-release continuity and defect loop |
| 11. Learning/retirement | Outcome metrics, accepted defects, costs, reuse candidates, sunset/data export/delete | No evidence of reuse → keep app-specific; don't extract | Evidence-based improvement and lifecycle closure |

**Release-ready** means a reproducible, inspected candidate with remaining risks disclosed and all applicable gates passing; it is not the same as deployed, commercially compliant, externally audited or guaranteed faultless.

## Repository scenarios that must be handled before claiming end-to-end capability

1. **New repo:** empty/missing README, no workflow, branch rules or credentials; minimal first vertical slice, safe initialization and basic CI.
2. **Existing healthy repo:** read branch, tests, ADRs and open PRs; reuse current infrastructure, deliver scoped change.
3. **Existing broken repo:** failing build, stale deps, failing tests, drifted schemas; reproduce and stabilize smallest blocking defect before feature work.
4. **Partial prior work:** interrupted conversation/work mode, conflicting commits, disconnected user context, unsaved evidence; recover GitHub state and compare current HEAD.
5. **PR sprawl/duplicates:** overlapping or superseded branches/issues; preserve unique findings, avoid new PR, never close without authorization.
6. **Concurrent workers/agents:** conflicting edits, wrong branch, lost lock, duplicate actions, out-of-order work; ownership and idempotent operations.
7. **Bad requirements or design:** ambiguous user journey, wrong architecture, hidden regulatory constraint, unaffordable dependency; seek smallest falsifiable prototype or redesign.
8. **Changed scope:** new feature intersects identity, payment, migration or tenant boundaries; reclassify risk and update tests/acceptance.
9. **Cross-platform:** Linux/Windows/macOS where relevant, browser/mobile accessibility, localization; don't assume a single CI runner proves all.
10. **External systems:** test fixture vs real API/protocol, network outage, provider change, quota, secret rotation and dependency license review.
11. **Data evolution:** zero-downtime-compatible schema, old-record reconciliation, concurrent writers, restoration and recovery, no silent deletion.
12. **Security incident:** leaked token, untrusted PR, dependency compromise, unauthorized access; stop sensitive execution and escalate.
13. **CI failure or absence:** no workflow run, flaky browser, dependency installation/billing issue, wrong HEAD; don't report green, capture blocker and retry narrowly.
14. **No independent reviewer:** can deliver documented prototype/internal test evidence, cannot claim required external signoff or production release.
15. **Merge/release request:** inspect branch protection, tests, owners, approvals, rollback, secrets; ask affirmative decision before action.
16. **Deployment target not chosen:** preserve provider-neutral interfaces, compare cost/region/recovery; do not provision by implication.
17. **Post-release incident:** degraded service, failed migration, stuck jobs, customer complaint, alert storms; rollback/recover under authorized operations.
18. **Handoff to another agent or new day:** exact ref/commit, changed files, tests, known risks, approvals, one next action; continue without hallucinated progress.
19. **Budget/resource pressure:** high CI cost, huge context, excessive PRs, redundant tools; cut unnecessary steps while retaining risk-critical assurance.
20. **Completion/retirement:** user acceptance, maintenance ownership, data export/retention, remove temporary privileges, archive evidence.

## How to benchmark without building the whole engine

Run **two different application archetypes**, starting with the [Camping Booking evidence scorecard](BENCHMARK-CAMPING-BASELINE-V1.md). First Camping Booking (transactional, OIDC, tenant data) and a second independent app (e.g. a content/admin or scheduling product). For each, assess staged evidence with:
- `PASS`: real artifacts and exact HEAD tests support the stage.
- `PARTIAL`: bounded slice passes but materially important functions, platforms or negative paths remain.
- `BLOCKED`: unresolved security, identity, approvals, dependencies or infrastructure.
- `NOT STARTED`: no artifact/evidence.
- `NOT APPLICABLE`: justified with owner/reviewer rationale, never automatic convenience.

Score **separately**, not as an average that masks a security failure: user-visible working journey; requirement traceability; architecture and tenancy; reliability/concurrency; accessibility; security/privacy; migration/recovery; independent review; release/ops readiness; cost and handoff quality. A single blocked critical dimension prevents a release-ready conclusion regardless of other scores.

Proposed measurable benchmark cases: new app from a validated brief, add a role-protected admin flow, migrate a real schema, fix a failing PR without multiplying PRs, resume after interruption, verify OIDC against real provider, and prepare a deployable *but undeployed* release candidate. Store baseline effort, defects/rework, PR count, CI duration/flakiness, escaped edge cases and human review burden; choose targets from observed data, not invented goals.

## Dynamic method selection and precedence

Select the lifecycle stage **and** task kind/risk using the current `ade.method_selection.select_method`; current selector only covers engineering task kinds and is **advisory**. No lifecycle automation is implemented. When controls overlap, combine them once; when they conflict, follow the stronger safety/approval/data requirement and document the decision. Highest precedence: user approval restrictions, security/legal/privacy controls, repository contracts and verified state. A faster method must never downgrade identity, payment, tenant or operational risk.

**Engine should eventually provide:** stateful lifecycle manifest; stage-specific acceptance/evidence schemas; traceability from requirements→code→tests→release; explicit risk and owner decision log; orchestration/resume; provider-neutral build/release artifact; independent review hooks and release stop gates.

**Do not build yet:** a large autonomous orchestrator, custom CI runner, replacement Git hosting, self-appointed security authority, default cloud deployment adapters or a universal admin backend. First demonstrate gaps in at least two archetypes and benchmark their resolution. Implement the smallest recurring mechanism and rerun the same tests.

## Agent handoff rule

In every new conversation/Work/Codex session, open this document and `docs/SENIOR-ENGINEERING-CONTRACT-V1.md`, the relevant application's `AGENTS.md`, latest PR and CI. Then state: **current stage, actual status, risk flags, what evidence exists, what's missing, intended smallest next action, approval stop gates**. Do not restate a false completion claim from a prior chat.

This specification is itself a **documented benchmark design**, not a validated end-to-end delivery capability. Promote to an enforced workflow only after cross-app evidence and explicit authorization.
