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
