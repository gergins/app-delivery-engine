# Interruption recovery: first cross-application observation (2026-11-03)

**Status:** GitHub connector inspection of two independent draft application PRs, not a claim that Engine's new CLI was run against both apps. This is a manually reconciled baseline for future end-to-end acceptance.

| Case | GitHub PR and observed PR HEAD | Exact-SHA workflow observed | What differs | Recommended next work |
| --- | --- | --- | --- | --- |
| Camping Booking | [PR #1](https://github.com/gergins/camping-booking/pull/1) at `d4857e460b589cb7f26da5f5525dbc62dbe8ca77` | [run 41701452408](https://github.com/gergins/camping-booking/actions/runs/41701452408), completed success; three job groups succeeded: real disposable OIDC + PostgreSQL integration, PostgreSQL and migration reconciliation, app unit/HTTP/browser/security/recovery tests | Complex multi-tenant booking, state transitions, migration and identity | Inspect latest current HEAD and the scope/restore gaps; prioritize remaining synthetic restore/rollback proof and unsupported legacy records before adding marketplace features. This is a proposal subject to current repository evidence. |
| Community Picks | [PR #1](https://github.com/gergins/community-picks-delivery-benchmark/pull/1) at `c939b43e89be15e3d904f92803690b8799966444` | [run 41629084098](https://github.com/gergins/community-picks-delivery-benchmark/actions/runs/41629084098), completed success; exact-source SHA, Python HTTP/SQLite and Chromium UI→API→SQLite steps succeeded | Minimal local standalone suggestion-list app with persistence, no identity/payment | Inspect recent drift and explicitly validate a fresh human/agent first-run plus accessible keyboard behavior; avoid adding an unnecessary booking-specific framework. |

## What the evidence supports

- Both applications have separately owned repositories, draft PRs and recorded exact-SHA CI runs with successful job steps at the observed heads.
- No source, PR, approval, or deployment was changed in either application during this benchmark.
- The next-step recommendations depend on distinct risk and user value; the engine should **not** automatically prescribe the same next feature for both.
- The new Engine components `ade.github_readonly.inspect_pull_request`, `ade.github_reconcile.reconcile_github_snapshot` and `ade.continuity.recommend_next_work` are implemented on its draft branch with mock-based tests, but their live cross-repository end-to-end wiring is **not yet proven**. GitHub connector inspection is independent external evidence, not a successful CLI execution.

## Still missing before claiming uninterrupted end-to-end recovery

1. Verify the Engine's tests and browser workflow at its *final exact PR HEAD*, not an earlier passing commit.
2. Run the actual CLI against both application PRs in an authorized environment with GitHub API read access, then compare the returned head/CI evidence with independent connector observations.
3. Simulate an actual interruption and changing HEAD; inspect issues, dependencies, reviews, branch protection and actual job logs before deriving acceptance status. Current CLI only reads PR and workflow metadata.
4. Ensure every recommendation has a source reference and explicit uncertainty; no automatic merge, deploy, paid service, independent signoff or user-scope approval.
5. Measure false-green claims, duplicate PR creation, time and manual steps to resume, and whether the recommended slice advances a complete user task.

## Decision and next slice

Prefer **verification and practical resumption** over more documentation, a dashboard or a general worker orchestration system. First make the existing read-only resume path reliable. Then unify requirements bootstrap with the already runnable web-list generator as a bounded opt-in application starter, with a fresh-user usability benchmark. Promote shared mechanisms only when the two different apps demonstrate value.

**Stop rule:** If exact-HEAD CI fails, repair that verified regression before any new Engine feature. If external GitHub access or review state is unavailable, record STOP rather than invent approval or evidence.
