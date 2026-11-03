# App Delivery Engine — agent and contributor agreement

Applies to ChatGPT, ChatGPT Work, Codex, assistants, and human contributors. The repository and existing draft PR are authoritative; past conversations are not.

1. Read `README.md`, `docs/ARCHITECTURE.md`, `docs/METHOD-SELECTION-V1.md`, active PR and CI evidence before editing.
2. Read [Senior Engineering Operating Contract v1](docs/SENIOR-ENGINEERING-CONTRACT-V1.md): proactively assess architecture, tradeoffs, overlooked risks, tests, operations, user outcomes and clean handoffs; do not equate a green test with readiness.
3. Select **one** bounded task kind and all known risks using `ade.method_selection.select_method`. This is a decision aid: unknown or disputed risks require human review, never automatic minimization.
3. Compose the core delivery controls and the task/risk-specific controls; never pick a weaker methodology to save effort. Prefer minimal vertical slices, existing code/tests, deterministic generation and proven licensed mechanisms.
4. Run positive, failure, security-boundary and relevant concurrency/restart tests. Verify source against exact commit SHA and complete GitHub Actions logs. Do not infer success without actual evidence.
5. Keep changes in the existing draft PR where possible. Document any justified exceptions. Every app owns its runtime and product logic; do not import whole external orchestration frameworks.
6. GitHub is the handoff: record milestone, decisions, code paths, commit SHA, CI URL/results, outstanding risks, approvals and exact next action. Other agents must read this handoff before continuing.
7. **Stop at governance gates.** Do not merge, deploy, publish, use production credentials, spend money, invite external reviewers, change branch protection/approval policy or bypass security checks without explicit authorization.
8. Never claim mocked OAuth tests establish a live IdP, that a green unit test means production ready, or that a self-review is independent authority.
9. Do not automatically promote code from a single benchmark. Compare multiple application implementations, verify reuse value, licensing, risks and negative tests before extracting shared mechanisms.
10. **Infrastructure neutrality:** The App Delivery Engine must not require DigitalOcean, Supabase or any specific cloud/database provider. Application repositories own hosting choices, credentials, deployment manifests and runtime adapters. Preserve swappable contracts and never infer approval to provision infrastructure from a passing test or an application-level provider preference.

Current work: `gergins/app-delivery-engine`, draft PR #1, branch `feat/m0-minimal-app-delivery`; inspect current HEAD and CI for latest state.

The senior engineering contract is advisory, not a substitute for CI, independent review or explicit authority. Continue to use the exact existing approval stop gates.
