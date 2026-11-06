# ADE first real product delivery trial — Camping Booking (2026-11-06)

## Scope and outcome

Use a **real product repo**, not the ADE generic list fixture. Target:
`gergins/camping-booking`, existing draft PR #1, branch
`feat/m4-camping-reservations`.

Task: prevent a customer from creating a second pending temporary hold before
confirming or cancelling the first; keep the existing booking journey and
authorization controls intact. The selected method is `bugfix` with
`concurrency` risk. No new API, database migration, account, payment or
production service.

## Execution evidence

This change was implemented through connected GitHub editing tools in the
Camping Booking repository, not by a worker launched from ADE.

- Product code: `app/customer_app.js`
- Browser regression: `tests/test_customer_browser.py`
- Exact committed product HEAD: `ac8bdedf60b0b4d23fac86cacb5aec2f9f7088a1`
- Existing PR: https://github.com/gergins/camping-booking/pull/1
- CI: https://github.com/gergins/camping-booking/actions/runs/42281706421
- Result: **not verified**. CI failed before any of its three jobs ran a step.
  Previous product HEAD also had pre-step failures. No product browser-test pass
  or production readiness is claimed.

## Reusable ADE handoff path

ADE's `ade.agent_handoff` now produces a versioned, bounded,
machine-readable work order from real read-only PR and CI state. Run in a
trusted checkout with GitHub read access:

```powershell
python -m ade.agent_handoff gergins/camping-booking 1 --kind bugfix --risk concurrency --task "Prevent a second customer hold until the pending hold is resolved" --acceptance "Customer receives clear feedback when another hold is pending" --acceptance "Existing confirm and cancellation browser journey remains intact"
```

For private repository access, a separately configured read-only
`GITHUB_TOKEN` may be required. Do not store it in ADE source, browser input,
log output or a generated work order.

This command does **not** dispatch an agent, edit code, verify full CI job logs
or grant approval. It is a safe bridge between manual/conversation-driven
engineering and a future separately authorized Codex/Work execution adapter.
A work order is not test evidence.

## Next acceptance and constraints

1. Resolve product GitHub Actions admission failure without disabling any
   jobs, protections or security requirements.
2. Execute customer Chromium browser regressions on the **exact final head**;
   inspect actual logs and job conclusions.
3. Review the semantic UX choice for active holds and run a negative
   cancellation/confirmation scenario.
4. Only after evidence: assess whether the reusable agent-work-order interface
   improves coordination on at least one second genuinely distinct app.
5. No merge, deploy, external reviewer invitation, real credentials or
   infrastructure spend without explicit approval.

This is one product feature, not proof that ADE can autonomously develop any
application. Keep the agent execution boundary explicit.
