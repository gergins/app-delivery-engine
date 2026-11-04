# Delivery Method Selection v1 — small, evidence-led and risk-aware

## Mission
Choose the smallest suitable delivery workflow for each application task, then combine **complementary** controls rather than install multiple orchestration frameworks. Selection is an advisory, deterministic decision record, **not** a self-authorizing security reviewer.

## Selection rules
1. Inspect the actual product repository, existing blueprints/PRs and relevant tests first. Determine exactly one task kind: `new-slice`, `bugfix`, `refactor`, `schema-change`, `integration` or `release-preparation`.
2. Declare all applicable risk signals: `identity`, `payment`, `personal-data`, `external-provider`, `migration`, `concurrency`, `public-exposure`. Unknown risks must be escalated and the selector updated/tested rather than silently treated as harmless.
3. Call `ade.method_selection.select_method(kind, risks)`. The result composes baseline checks, kind-specific acceptance and risk overlays with no duplicates. Add domain-specific tests in the product repository; the engine does **not** prescribe the technology stack or write the application.
4. Follow the returned control IDs. Require test logs and exact-HEAD CI confirmation; do not interpret an absent run or mock identity flow as live provider assurance.
5. Finish with a concise recorded handoff in the existing PR/issue: source commit SHA, workflow/job URL and result, tests, limitations, open external approvals and precise next step.

## Example
```python
from ade.method_selection import select_method
plan = select_method("integration", ["identity", "external-provider", "concurrency"])
print(plan)
```

This chooses an **integration contract + negative authentication boundary + competing request tests**, while still requiring an external IdP proof before making a live identity claim. It does not create an IdP, grant access or deploy.

## Workflow by task category
- New feature: user journey + minimal runnable UI/API/data slice, useful failure/empty states and browser check if interactive
- Bug: reproduce failure before change; smallest repair and permanent regression
- Refactor: characterize existing behavior first, preserve public interfaces, compare results
- Schema: versioned migration, checksum, backup/restore rehearsal, old-record compatibility
- Integration: provider contract and failure states, credential ownership, simulated vs real evidence clearly separated
- Release: privacy/a11y/security/ops threat review, independent approval and documented rollback

## Universal stop conditions
Never merge, deploy, enable public access, authorize spending, use production secrets, change review policies or declare independent signoff automatically. A risk overlay adds verification; it does not relax this baseline. If a required external authority or live provider environment is missing, complete only the safe preparation and record the gate.

## Rollout to other tools and people
- Put a short `AGENTS.md` in each application repo referring to this document and its current product PR; Codex and agents should read it explicitly.
- In ChatGPT Work and normal conversations, ask the assistant to open `AGENTS.md` and this document from GitHub **before editing**. Work/Codex chat memory is not the authoritative source.
- Keep one source of truth in GitHub. Avoid duplicate manuals/PRs and do not copy this entire engine into applications.
- Before making this a mandatory automation or release gate, benchmark at least two distinct app types and perform independent review of the selector, omissions and risk mappings.

## What remains unproven
This is an initial narrow method-selection core. It does not assess semantic task risk automatically, prove design fitness, control agent execution, enforce CI policy remotely or guarantee delivery quality. Formal decision ownership, risk taxonomy expansion, skill/version provenance, review separation and an automated agent harness are later evidence-driven decisions.


## Evidence-Based Adaptive Verification — bounded trial (2026-11-04)
Preserved rollback: `backup/pre-evidence-based-adaptive-verification-20261104`, original head `e71c3ed044c943848feaeb806f6addd66757b6f8`.

Use `ade.method_selection.assess_evidence_reuse` only **after** a senior developer has established the complete affected scope and relevant transitive dependencies. The function takes an explicit prior test record (behavior, passing result, commit, evidence URL, covered scopes, exact dependency map and environment). It does not inspect GitHub, compute dependency graphs, independently authenticate CI results or authorize skipped required checks.

- **Reuse prior evidence:** same covered behavior, no changed overlapping scope, identical dependency versions/environment and no declared high-consequence risk. This avoids rerunning *unnecessary optional* suites; required current-commit CI still runs.
- **Targeted verification:** uncovered behavior, missing/failed evidence, changed environment or high-consequence risk without confirmed changed scope. Run relevant checks and capture new evidence.
- **Expanded verification:** changed covered scope or dependency drift. Analyze affected contracts, integration and user journeys; add required negative/recovery tests.
- **Unknowns:** invalid risk input raises; incomplete evidence never qualifies. The human must ensure all transitive consumers and semantic changes were captured; omission makes the advisory decision unsafe.

Before recommending reuse, inspect provenance at the original test commit and confirm test logic, environment, fixture data, dependency graph and acceptance criteria still apply. Do not use this helper as an independent security assessment. A past successful run does not prove the new HEAD passed. Branch rules, required CI, risk-specific reviews, human approvals, merge and deployment stops remain unchanged.

**Benchmark before promoting:** compare existing full workflow with the advisor on real low/medium/high-risk changes. Measure CI time, feedback latency and deliberately seeded regression detection (including counterexamples where reuse must be rejected). Do not create a separate orchestration system or silently reduce .github/workflows/verify.yml.


## M1 evidence-reuse benchmark — measured scope and promotion rules (2026-11-04)

The bounded test lives in `tests/test_adaptive_evidence_benchmark.py`. It uses the existing app generator and ephemeral test directories (no real user data, no external provider or credentials). Four cases exercise:
1. unchanged CLI behavior with documentation-only scope, allowing advisory reuse while retaining mandatory current-HEAD CI;
2. generated CLI behavior mutation (`transform` stops trimming), requiring expanded verification and proving an actual generated test rejects the mutant;
3. generated web-list API input-validation mutation, requiring expanded verification and proving a real HTTP/SQLite generated test rejects the mutant;
4. transitive runtime dependency change and missing evidence metadata, both refusing reuse.

**What this establishes if exact-HEAD CI passes:** the current advisor recognizes these explicitly supplied scenarios and the two generated-app regressions detect injected defects. It does not infer impacted scopes, prove real booking/auth/tenant isolation, validate GitHub evidence URLs, measure user outcomes, or independently authorize CI omission. The concurrency risk label in the web-list scenario demands caution; the injected mutation is *input validation*, not a concurrency defect.

**What remains to measure:** paired CI execution time, runner cost, flaky retries and defect-detection rates under selected vs baseline testing across two distinct real app repositories. Current workflow deliberately remains fully enabled. Do not claim a saving from four green benchmark cases; collect comparable timed results and run a genuinely nontrivial dependency/authorization counterexample before promoting automatic skipping.

**Rollback for this milestone:** `backup/pre-evidence-adaptive-benchmark-m1-20261104`, commit `d86221e545376c4d2421631e83ae34d1fc6cbb8a`. Earlier rollback `backup/pre-evidence-based-adaptive-verification-20261104` remains. Preserve both before any scope expansion. Draft PR #1 only; no merge/deployment.
