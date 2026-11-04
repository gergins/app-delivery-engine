# Lifecycle Benchmark — Camping Booking baseline (first archetype)

**As of 2026-11-03.** Product source: `gergins/camping-booking`, existing draft PR #1, branch `feat/m4-camping-reservations`. This is an **evidence-based partial appraisal** of one transactional/tenant-sensitive app, not a complete audit or proof that the Engine built its whole lifecycle. Source code and user decisions remain in the product repository, not copied here.

Ratings follow [Application Lifecycle Benchmark v1](APP-LIFECYCLE-BENCHMARK-V1.md): PASS / PARTIAL / BLOCKED / NOT STARTED / NOT APPLICABLE. A stage rated PASS is limited to its **specified benchmark slice**, not all conceivable production requirements. Unverified status is never promoted to PASS simply because the tests are green.

| Stage | Evidence seen | Current rating | Exact gap to evaluate next |
| --- | --- | --- | --- |
| 0. Idea intake | Application intent (campground booking) established in repo/docs | PARTIAL | Independently accepted problem brief, users/outcome/non-goals and ownership |
| 1. Value/feasibility | Working demonstration; hosting and costs compared conceptually | PARTIAL | User validation, commercial viability, operating cost scenario and alternatives |
| 2. Requirements/scope | README milestone narratives, policies, internal integration tests | PARTIAL | Requirements→acceptance traceability and explicit accessibility/nonfunctional targets |
| 3. Architecture/design | Tenant/schema/session boundaries, Keycloak/SQLite and PostgreSQL experiment, ADR-like decision gate | PARTIAL | Reviewed end-to-end target architecture and full PG migration design |
| 4. Implementation plan | Ordered M4–M8 roadmap, PR/CI handoffs | PARTIAL | Dependencies and each gate's full accepted product requirements |
| 5. Implementation | Runnable local/demo UI, API, SQLite; opt-in customer browser flow; bounded PostgreSQL booking adapter | PASS for prototype | Complete PostgreSQL-backed customer hold, cancellation, audit, gateway/session and worker |
| 6. Verification | Unit+Flask+Chromium, actual disposable Keycloak, PostgreSQL direct SQL bypass and concurrency tests | PARTIAL | Production-like external HTTPS IdP/JWT adversarial suite, migration/restore, full PG app E2E, a11y audit |
| 7. Independent review | Review/security responsibility and gates documented | BLOCKED | Assigned distinct qualified reviewer and completed review evidence; no self-signoff |
| 8. Release candidate | No approved full build/artifact/operations bundle | NOT STARTED | Immutable release artifact, SBOM, licenses, documentation, restore/rollback, privacy/a11y/security signoffs |
| 9. Deployment decision | One-provider DigitalOcean preference; no authorization/provisioning | BLOCKED | Reviewed staging topology, migration, total cost and explicit approval; production later |
| 10. Operations | Prototype expiry worker and offline SQLite backup/recovery tests | PARTIAL | Alerting, incident owner, real PG recovery/restore, SLO, runbook and observed operations |
| 11. Learning/retirement | Cross-agent AGENTS.md, method selector, reusable boundary candidates | PARTIAL | Cross-application validation, explicit lesson provenance and no premature framework promotion |

**Risk dimensions not averaged:** identity = partial; tenant isolation = partial; real PostgreSQL concurrency/exclusion = passed *for isolated confirmed booking slice only*; privacy/accessibility = unreviewed; backup/restore = SQLite-only bounded; release security authority = blocked; customer/business acceptance = unverified.

### Concrete repeatable benchmark tasks
- Start from a new brief and produce a justified minimal runnable feature with tests and traceable acceptance criteria.
- Take a broken/open PR, reproduce failure and resolve without additional duplicate PRs; verify exact HEAD.
- Integrate a real nonproduction external provider and compare mock-only versus protocol proof.
- Demonstrate cancellation/expiry and no-overlap under concurrent direct database writes.
- Resume after another conversation/tool/agent has changed the branch, detect drift and hand off accurately.
- Produce a release-candidate manifest that **stops at approval** if required independent review or full recovery is missing.

### Why another application is essential

Camping Booking is unusually transaction-heavy. A second independent app should exercise content/admin CRUD, workflows, permissions, accessible UI, reporting and release preparation with a different risk profile. Until then, **do not** claim that the current method-selection rules cover all app types. Extract a shared engine feature only if the second benchmark identifies the same verified gap and the contract is smaller than keeping the solution app-specific.

**Evidence source:** latest Camping Booking PR #1 and exact-SHA CI; latest Engine PR #1 and its CI. This scorecard intentionally does **not** automatically revise itself as GitHub changes; every future reviewer must recheck actual state and cite the exact tested SHA when updating a rating.
