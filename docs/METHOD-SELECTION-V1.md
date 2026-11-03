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
