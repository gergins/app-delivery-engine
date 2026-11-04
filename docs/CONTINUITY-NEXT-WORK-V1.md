# Recovery and Next-Best-Work Contract v1

**Status:** bounded read-only reconciliation, GitHub lookup CLI and advisory next-work selection on draft PR #1. This is not an autonomous coding worker, fully trusted attestation, or evidence of production readiness.

## Goal

An interrupted or returning contributor (ChatGPT, Work, Codex, human) can recover the actual state **without needing the previous conversation**. Work must be safe when the browser closes, network disconnects, laptop shuts down, or an agent is replaced. Never assume a graceful shutdown or claim unsaved local edits survive.

## Resume protocol (read-only until scope is verified)

1. Identify exact application repository and approved scope; read AGENTS.md and current delivery state.
2. Fetch live branch, HEAD SHA, PR, reviews, CI conclusion/logs, issues and committed decisions from GitHub. If remote access fails, mark state **unknown** rather than reusing stale success.
3. Compare checkpoint to GitHub: detect branch/head drift, stale CI, inconsistent approvals, duplicate PRs, interrupted operations and concurrent writers. Treat uncommitted state as unverified unless recovered from the original workspace.
4. Survey defects, security/data integrity and recovery failures, CI, blocked dependencies, incomplete accepted work, next user-visible slice, documentation and optimization. Each candidate needs an exact artifact reference and dependencies.
5. Select next work using the smallest justified risk-aware step. The current pure function `ade.continuity.recommend_next_work(snapshot, candidates)` is only an advisory offline selector: it **requires externally verified facts** and cannot authenticate its own input.
6. Record rationale, impact, risk, tests, expected HEAD, permitted changes and explicit stop gates. Execute only a previously authorized bounded task; never infer authority from a recommendation.
7. Verify positive/negative tests, exact HEAD CI, review and artifacts before updating completion state.
8. Commit a small human/agent-readable handoff: last verified SHA, objective, completed/incomplete tasks, evidence URLs, open blockers, prior decisions, one next action, and who is allowed to decide.

## Durable checkpoint schema (application-owned)

Use existing `delivery/current-state.yaml`, `delivery/evidence.json`, `delivery/approvals.json` and decision documents. Do not introduce another authority store. Future versioned fields should include:
- `repo`, `branch`, `pr`, `observed_head_sha`, `observation_timestamp`, `remote_verified`.
- `milestone`, `status`, `accepted_scope`, `next_action`, `blocking_dependencies`.
- `tested_sha`, `ci_conclusion`, `workflow_url`, `test_scope`, `known_limits`.
- `candidate_id`, `kind`, `evidence_ref`, `dependency_ready`, `rationale`.
- `approval_references` sourced from actual human/GitHub authorizations, not booleans fabricated by AI.
- `pending_operation` with idempotency key, expected HEAD and recovery procedure for future write-enabled adapters.

Never put credentials or personal data in the checkpoint. Do not mark completion when the evidence is merely stored in editable JSON.

## Priority rule

Security boundary and data integrity > recoverability > failing CI > blocked dependency > unfinished accepted slice > new slice > documentation > speculative optimization. Overrides require visible rationale and authorized owner, particularly for emergencies and high-risk changes. Prefer repair over additional features when the known state is unhealthy. No ready candidate means STOP and investigate rather than invent work.

The read-only inspection command `python -m ade.github_readonly owner/repository PR_NUMBER` fetches the current PR and PR-triggered workflow metadata from GitHub's API (public access or caller-provided `GITHUB_TOKEN`). It refuses incomplete responses and cannot independently validate the user's authority or project scope. A CLI result is a point-in-time observation; re-check HEAD before any write. Do not persist or display the token. The selector checks verified remote SHA format, exact tested SHA for claimed successful CI, recognized CI states, presence of an approval ledger, unique referenced candidate IDs, dependency readiness and a fail-closed gate for feature work while CI is failing. It does **not** query GitHub, assign risk by semantics, inspect code, authorize actions, or perform work. Invalid candidate input raises an error rather than silently downgrading risk.

## Required interruption benchmarks

- Return after browser close/lost internet with a changed remote HEAD.
- Stale CI success from an earlier commit.
- Missing/failed GitHub workflow or GitHub API unavailable.
- Work interrupted before commit; partial or conflicting edits.
- Two contributors recommending or executing the same task.
- Existing PR plus duplicate proposed PR.
- Missing owner acceptance or reviewer authority.
- Successful slice with a remaining high-risk blocker.

Acceptance: next contributor reconstructs the truthful current status, refuses stale proof, chooses a justifiable next action, and avoids duplicated/unauthorized writes. Measure incorrect completion claims, duplicate PRs, recovery time, and missed blockers across Camping Booking and another different application. **These are future integration benchmarks, not passed claims.**

## What to implement next

Verify exact-HEAD CI of the GitHub lookup/reconciliation tests, then prove a real return-to-work scenario on Camping Booking and Community Picks: fetch PR and complete CI evidence; verify unchanged HEAD, inspect reviews, issue dependencies and decisions, build candidates, and record the correct next action. The lookup does **not** retrieve job logs, issue priorities, branch protections, human permission or full review state. Those must be inspected separately before making a readiness claim. Only afterward consider any write-enabled execution, scheduling or an admin dashboard.

No merge, deployment, account provisioning, paid infrastructure, production secrets or external reviewer access is authorized by this document.
