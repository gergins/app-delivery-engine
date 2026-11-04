# Lifecycle Benchmark — Life Services Hub (second archetype)

**Evidence basis:** read-only inspection of `gergins/live-services-hub` `main`, README, `index.html`, `src/tasks.mjs`, Node tests, Playwright config, GitHub Actions workflow, and historical merged PR #2. This app is intentionally different from Camping Booking: **static client-side task management, not multi-tenant transactional checkout**. No changes were made to Life Services Hub in this benchmark.

**Verified historical evidence:** merged PR #2 head `11b97e360f760701c0da42d368765d962fdf8e41`; its exact-head pull-request workflow run [41337482878](https://github.com/gergins/live-services-hub/actions/runs/41337482878) completed SUCCESS. PR #2 merged at `20c20206a343e4466305cb368d5b3aa05e163e91`. Historical CI success is **not** evidence that a newly edited `main` has fresh CI; this document does not claim the app was deployed.

## What this benchmark actually covers

- A user can create a task, assign a due date, mark complete/undo, and delete it through semantic HTML controls. Node domain tests check validation/order/corrupt persisted data; a real Chromium test checks UI actions and browser persistence.
- The app is local-only, without server authentication, shared family access, tenant data, remote backup, sensitive document handling, reminders, payment, hosting or operational service.
- The delivery workflow shows a runnable **minimal vertical slice and simple reversible architecture**: static `index.html`, pure `src/tasks.mjs`, browser `localStorage`, `node --test` and Playwright CI.
- Its workflow uses `actions/checkout@v4` and `actions/setup-node@v4` tags rather than immutable action SHAs. That is a supply-chain hardening gap before it can be promoted as a security-sensitive template, not a reason to impose an entire delivery framework on this low-risk prototype.
- There is no `AGENTS.md` on `main` at inspection time. AI handoff instructions should be referenced from the Engine or supplied in a bounded future PR, not presumed present.

## Lifecycle stage ratings (bounded evidence)

| Stage | State | Evidence / gap |
| --- | --- | --- |
| Idea intake | PARTIAL | Simple tasks/important-dates outcome clear; target audience, value proposition and success metrics not validated |
| Feasibility/value | PARTIAL | Runnable local demo confirms technical feasibility, not market/product viability |
| Requirements & acceptance | PARTIAL | README acceptance and tests cover task lifecycle; future requirements (families, documents, reminders) remain undefined |
| UX and architecture | PARTIAL | Simple semantic accessible-looking UI, pure domain core; no measured accessibility audit or production architecture |
| Planning & implementation | PASS for prototype | Single small working slice, no unnecessary backend/framework or cloud |
| Verification | PASS for prototype | Historical Node+Chromium exact PR HEAD workflow; no security/production claims |
| Independent review | BLOCKED for release | PR merged does not establish independent security/privacy/a11y approval |
| Release-ready deliverable | NOT STARTED | No app server, backend auth, backup, operations, SBOM/license/provenance release evidence |
| Deployment authorization | NOT STARTED | No deployment request, hosted preview or approval in this inspected scope |
| Operations/maintenance | NOT STARTED | Local browser-only; data loss/recovery and future sync are not addressed |
| Retirement / learning | PARTIAL | Supports minimal-vertical-slice and provenance lesson; limited cross-app evidence |

## Cross-application decision: what to promote and what not to promote

| Mechanism | Camping Booking observation | Life Services Hub observation | Engine decision |
| --- | --- | --- | --- |
| Minimal runnable UI/API/data vertical slice | Works but needs serious auth/storage protocols | Works with only HTML + pure JS | **RETAIN** as universal principle; implementation remains app-specific |
| Domain logic separated from UI | Booking policies and transactional boundaries | Pure task domain module | **RETAIN** as guidance; no framework required |
| Positive/negative domain regressions | Security, concurrency and expiry are essential | Validation/corrupt storage are essential | **RETAIN** risk-aware test choice, not one fixed suite |
| Real browser journey | Flask and booking UI | Static browser localStorage workflow | **RETAIN** for user-facing apps |
| Exact-head CI and evidence handoff | Essential for many code updates | Historical exact PR HEAD check only; workflow pinning incomplete | **RETAIN**, harden CI trust but avoid heavyweight factory |
| PostgreSQL, Keycloak and multi-tenant constraints | Required by Camping Booking's actual risks | Not applicable to client-only task demo | **DO NOT PROMOTE** to universal Engine dependencies |
| Managed cloud provisioning | Future DigitalOcean product decision | No deployment needed for local prototype | **DO NOT PROMOTE** provider dependency |
| AI agent/repository handoff | Current AGENTS.md plus CI and PR evidence | No main-branch AGENTS.md; merged PR history | **CANDIDATE:** lightweight handoff contract; test interruptions before automating |
| Full independent audit | Needed prior to sensitive public deployment | Not automatically required for purely offline local demo | **SELECT BY RISK**, never universal yes/no |

## Measurable next benchmark

1. Add a new **low-risk functional change** to a second application's existing branch under explicit authorization; compare PR count, test coverage and breakage before/after. No need for mandatory full factory.
2. Simulate a **cross-agent handoff**: a second agent reads `AGENTS.md`/PR, selects method + stage, reports current SHA and missing permissions; compare drift and duplicate work.
3. Validate release-candidate checks that make sense for a static offline product (asset identity, accessibility, local data-loss notice, license/provenance), without pretending it requires Keycloak or payments.
4. Compare effort/cost and false positives for method selection in both archetypes before implementing a planner, stage orchestrator or policy compiler.

**Conclusion:** The second archetype strengthens support for *selecting* methodology by real context and lifecycle stage, not copying the Camping Booking stack. Neither app demonstrates the full idea-to-production lifecycle. The most valuable next Engine feature is an **inspectable lifecycle evidence and handoff manifest**, but defer implementation until one handoff benchmark demonstrates the gap and a minimal schema wins over another static document.
