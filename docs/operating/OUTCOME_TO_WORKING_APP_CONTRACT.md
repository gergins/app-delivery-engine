# Outcome-to-Working-App Operating Contract (OWAC)

**Version:** 1.0.0 (proposal, reusable baseline)  
**Date:** 2026-11-08  
**Status:** Saved reference specification; not deployed, not adopted by any repository automatically.  
**Scope:** Any AI-assisted or conventional application delivery workflow; initial validation target: synthetic camping booking demonstration.  
**Guiding principle:** Select the least complex, least expensive *verified capable* route to a working outcome, while preserving responsibility, evidence, safety, accessibility, and human authority.

## 1. Purpose and definition of success

Turn a human intention into a functioning, testable, browser-accessible application increment. Do **not** equate a generated codebase, successful agent message, passing static checks, or an unstarted preview with success.

**Outcome achieved only if:** (1) acceptance criteria are demonstrably met, (2) the actual app starts and critical journeys work in a real browser, (3) applicable nonfunctional guardrails are checked, (4) evidence is tied to an exact code revision and environment, (5) remaining limitations are disclosed, and (6) review is possible through a usable preview or the concrete reason a preview cannot be delivered is reported. Any production release requires separate explicit authority.

## 2. Drivers and precedence

- **Outcome-driven (primary):** Optimize for user-visible verified usefulness, not output volume.
- **Operating-contract-driven (governance):** Enforce boundaries and decision rules at every stage, including who may do what.
- **Intent-driven (intake):** Translate informal requests into user journeys and testable results; avoid over-specification.
- **Capability/reuse-driven (selection):** Prefer qualified existing components, frameworks, services, and deterministic methods before custom implementation.
- **Verification-driven (completion):** Trust runtime evidence and tests, not agent assertions.
- **Visual/experience-driven (handoff):** Deliver a clickable app to the user as early as feasible.
- **Problem/feedback-driven (repair):** Diagnose and resolve failures without repeatedly transferring small work to the user.
- **Resource-driven (cross-cutting):** Minimize total cost of implementation, operation, tokens, integration, maintenance and verification, not merely a single model call.

These are **roles rather than mandatory separate agents or rigid sequential phases**. Use only the roles needed for the particular job.

## 3. Required inputs and default assumptions

Input: user intention (natural language, screenshot, sketch, link or brief), repository and existing project context if available, target audience, constraints and authorization. Inspect a project's `AGENTS.md`, startup protocol, current state, tests and project-specific contracts before making changes. Never invent permissions or existing infrastructure.

For unspecified choices, select reversible, conservative defaults and record the assumption. Ask a question *only* when ambiguity materially changes safety, expenditure, data exposure, outcome or irrevocable architecture. Otherwise implement the smallest safe coherent slice and reveal assumptions in the handoff.

## 4. Responsibility and authority matrix

| Area | Automation may do without repeated approval | Must request explicit authorization |
|---|---|---|
| Explore | Read code, analyze requirements, compare solutions, review public documentation and licenses | Access unavailable private systems or protected information |
| Build | Modify permitted feature branches/workspaces, add tests, create preview fixtures, fix ordinary defects | Merge to protected branches, destructive resets, alter unrelated repositories |
| Runtime | Start local or approved preview services, use synthetic test data, inspect logs | Public/production deployment, billing changes, paid subscriptions |
| Data | Create reversible local synthetic records, sanitize test evidence | Read/export live customer data, run irreversible migrations or data deletion |
| Security | Run authorized read-only or non-destructive checks, report findings | Disable controls, expose secrets, authorize high-risk operations |
| Decisions | Choose reversible implementation details within accepted constraints | Change material scope, legal commitments, user-facing business policy or ownership |

Human approval is an **authority gate**, not a request to micromanage every build/test/retry step. Stop or isolate the affected action if permission is absent; do not silently expand authority.

## 5. Minimal operating loop

1. **Understand:** Identify target user, core job, expected visible behavior, constraints, assumptions and one high-value journey.
2. **Contract:** Write measurable acceptance checks plus a short list of safety, accessibility, privacy and reliability guardrails.
3. **Discover/select:** Inspect existing project and proven open-source/product capabilities; compare use-as-is, configure, integrate, wrap, build, and do-nothing options. Record the decision only where consequential.
4. **Implement:** Make smallest coherent vertical slice, including UI, backend/data integration where needed, and test data.
5. **Run:** Start real application in an accessible execution environment (prefer cloud/browser where appropriate). Confirm HTTP route, visual interaction and actual persistent behavior as applicable.
6. **Verify:** Execute automated checks plus browser-level tests for core user journey; capture exact revision, command/run status, screenshots or videos when allowed, and logs.
7. **Diagnose/repair:** On failure, reproduce, identify cause, make smallest safe correction, rerun relevant tests; cap retries and escalate when progress stalls.
8. **Hand off:** Present preview URL/access instructions, features exercised, evidence, known limitations, changes, and one meaningful next user decision.
9. **Preserve:** Keep an auditable continuity record and reusable validated lessons; do not claim future monitoring without automation actually configured.

**Fast path:** For simple changes, combine steps and use deterministic tooling. There is no requirement for an agent swarm, separate service, large dashboard or lengthy report.

## 6. Selection policy (universal responsibility and resource optimization)

Choose among: no action, direct answer, deterministic script, configuration, existing OSS/service, specialized AI model, general AI model, human, or hybrid. A cheaper candidate is eligible **only if** it satisfies functional, security, license, maintainability, integration, verification and accessibility requirements. Total cost of ownership and failure/rework cost matter more than call price.

Decision heuristic:

1. Eliminate unsafe, unauthorized, unmaintained/unfit, or unverifiable candidates.
2. Reuse existing project capability if adequate; avoid duplicate systems.
3. Prefer deterministic operations for exact repeatable work.
4. Select the most economical *capable* model or method for the remaining uncertain/creative steps.
5. Use an independent verifier for consequential claims where proportionate.
6. Reevaluate if evidence or constraints change.

The **system-level solution** is the primary optimization unit; task-level and per-model routing are optional sub-decisions. Do not optimize one component at the expense of the whole workflow.

## 7. Executable outcome contract format

Store per project or slice as `delivery/outcome-contract.yaml` (example below); schema validation may be implemented later. Fields are illustrative, not a claim that tooling currently consumes them.

```yaml
contract_version: "1.0.0"
id: "camping-booking-synthetic-mvp"
status: "proposed"
intent: "As a camper, book and cancel an available pitch in a browser"
users: ["camper"]
outcome:
  description: "Complete synthetic booking-to-cancellation journey"
  must_demonstrate:
    - "Search three-night availability for selected dates and guests"
    - "See pitch suitability, availability, and total price before booking"
    - "Create a synthetic reservation with unique confirmation"
    - "Retrieve reservation and see accurate status"
    - "Cancel reservation and see inventory/status updated consistently"
constraints:
  synthetic_data_only: true
  accessible_browser_interactions: true
  no_public_deploy_without_approval: true
  no_merge_without_approval: true
  no_spend_without_approval: true
  preserve_rollback: true
  respect_existing_repo_contracts: true
verification:
  require_exact_revision: true
  require_running_app: true
  require_browser_e2e: true
  require_booking_overlap_prevention: true
  require_keyboard_journey: true
  require_error_state_check: true
  require_critical_tests_pass: true
  report_unverified_checks: true
autonomy:
  ordinary_repair_allowed: true
  max_identical_failure_retries: 2
  escalate_on: ["missing_permission", "unsafe_action", "irreversible_change", "unknown_live_data", "blocked_runtime", "repeated_identical_failure"]
handoff:
  preview_or_blocker: true
  user_journey_evidence: true
  exact_revision: true
  known_limitations: true
  next_decision: true
```

Do not hard-code these thresholds globally; projects may adjust with explicit reasoning.

## 8. Lifecycle and exception handling

State transitions: `INTAKE -> CONTRACTED -> SELECTED -> BUILDING -> RUNNING -> VERIFYING -> REVIEW_READY`; any stage may move to `BLOCKED`, `NEEDS_AUTHORIZATION`, or `FAILED_VERIFICATION`. From `VERIFYING`, recoverable defects return to `BUILDING`; verified success alone moves to `REVIEW_READY`. `REVIEW_READY` **does not mean** `APPROVED_FOR_RELEASE`. Only authorized user decision may permit merge/deployment. Preserve traceable state and reason codes; don't invent successful states.

Repair budget: retry a failing operation only with a causal change; stop after two identical failures or earlier when no safe progress is possible. Summarize blocker, attempted fixes, smallest required human decision and safe rollback. If CI is unavailable, local results may be labeled as partial evidence, **never** CI pass.

## 9. Verification pyramid and evidence bundle

- **Static:** lint, type check, schema validation, dependency/license review, relevant security checks.
- **Component/integration:** business invariants, API contracts, database behavior, tenant isolation where applicable.
- **Browser E2E:** navigate via actual UI, verify rendered states and back-end effects, including keyboard access.
- **Negative paths:** invalid inputs, expired holds, duplicate booking attempts, authorization denial, cancellation edge cases, reconnect/timeout where relevant.
- **Operational:** startup, data setup, rollback, environment limitations, logging without secrets.

Evidence bundle per slice: exact commit SHA, branch, environment, commands/results, test artifacts, browser proof, timestamps, selection rationale when material, known gaps, approval status. Do not declare “done” from code review or screenshots alone.

## 10. Visual-first handoff

Show the live interactive preview first where possible. Accompany with a short plain-language explanation: what works, what to click, what was tested, what is still missing, and whether anything requires approval. Prefer one focused user decision over a backlog of tiny confirmations. Provide useful accessibility defaults: keyboard navigation, legible text, visible status and error messages, captioned/textual alternatives to audio feedback, and no audio-only instructions.

A preview must be labeled *synthetic*, *private*, or *public* based on actual environment; never claim a publicly reachable URL or session unless verified.

## 11. Project integration contract

**Portable files:**

- `docs/operating/OUTCOME_TO_WORKING_APP_CONTRACT.md` — this policy (copy/version, do not silently replace existing policies).
- `delivery/outcome-contract.yaml` — project/slice-specific executable acceptance declaration.
- `delivery/current-state.yaml` — latest verified state and next action.
- `delivery/evidence/` — evidence manifests/artifact links (avoid secrets and unneeded personal data).

On startup: read applicable `AGENTS.md`, requirements, current-state and project-specific contract; resolve conflicts by safety, higher-authority rules, and explicit human authorization. Existing project decisions stay intact unless explicitly revised. Store changes on authorized branch with rollback, and use PR/evidence workflows as applicable. No silent cross-repository updates.

## 12. Initial proof / test protocol

**Candidate:** existing camping-booking app. **Objective:** synthetic camper booking and cancellation through a browser, not a new automation platform. **Procedure:** inspect repo and environment; pick smallest existing path; ensure a realistic data fixture; run full app; verify availability, suitability, price, reservation, retrieval, cancellation; automatically repair ordinary failures; demonstrate keyboard flow; generate evidence bundle; present preview; ask user only for consequential feedback/approval.

**Pass:** a user can navigate the essential flow in the working preview and critical acceptance checks are evidenced against exact revision.  
**Partial:** code or tests work but browser journey or preview is not demonstrated; label exactly what remains.  
**Fail/block:** unsafe, unverified, non-running or unavailable environment; report without disguising as completion.

## 13. Health measures and anti-patterns

Useful metrics: time from idea to first usable preview, verified journey completion rate, automated repair success, user interventions per slice, total cost per accepted outcome, regression rate, accessibility defects, evidence completeness. Baselines must be measured, not fabricated.

Avoid: agent-count as productivity metric; repeated approval for trivial fixes; optimizing cheapest token while increasing total rework; copying unvetted OSS; treating mockups as running apps; declaring CI green without actual run; building elaborate registries before showing working product; cross-repo edits without authority; sacrificing clarity for maximum autonomy.

## 14. Reuse and change control

This contract is **domain-independent** and proportional: reuse its selection and evidence principles in other workflows but activate app-specific checks only for application delivery. Adapt via a project-specific profile rather than copying the whole methodology into every action. Maintain semantic versions and a brief changelog; incompatible governance changes require approval. This file is a durable draft/reference, **not** proof of engineering implementation.

### Changelog
- **1.0.0 — 2026-11-08:** Initial reusable baseline: drivers, operating authority, minimal loop, system-level resource selection, example outcome YAML, evidence, browser handoff, lifecycle, pilot.