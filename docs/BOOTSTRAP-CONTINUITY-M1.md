# Application Bootstrap & Continuity — M1 benchmark

## Chosen first proof (without creating a public repository)

A user gives an idea such as a VRS (Video Relay Service). The Engine should create **a deterministic, inspectable offline repository starter** containing the product brief, architecture questions, risks, decisions, delivery state, approvals, verification and agent startup rules. Another ChatGPT conversation, Work, Codex or human clone should run one common command, inspect the source of truth, and know **why to continue, stop or request explicit authorization**. A real GitHub repo creation/permissions adapter is later, separately authorized work. **This milestone does not create a VRS service or GitHub repository.**

Run from the **App Delivery Engine** checked-out source:

```bash
python -m ade.bootstrap_cli plan examples/vrs-bootstrap.json
python -m ade.bootstrap_cli create examples/vrs-bootstrap.json /tmp/my-vrs-starter
cd /tmp/my-vrs-starter
python tools/startup.py
python -m unittest discover -s tests -v
```

Expected initial `startup.py` result: **STOP (exit 2)**, because requirements, safety and minimum vertical-slice acceptance have not been approved. A STOP is the correct **passing** bootstrap benchmark, not failed application delivery.

The starter uses strict `JSON` formatted `project.yaml` and `delivery/current-state.yaml`, a syntax-compatible subset of YAML 1.2. This avoids adding a YAML runtime dependency. Future YAML-based input must be explicitly validated, not interpreted with unsafe deserializers.

## Generated repository contract

| File / folder | Why it exists |
| --- | --- |
| `AGENTS.md` | Portable instructions and authority boundaries for Work, Codex, humans and other agents |
| `project.yaml` | Versioned product identity, users, problem, outcome, explicit risks and runtime state |
| `docs/product/requirements.md` | Pending acceptance of scope, users, outcomes and nonfunctional constraints |
| `docs/product/vrs-invariants.md` (VRS only) | Media, session, queue, reconnect, telecom/emergency, access and privacy guardrails |
| `docs/architecture/overview.md` | Build/reuse/defer, service/data ownership, interface and failure-mode questions |
| `docs/decisions/0001-initial-constraints.md` | Proposed ADR, not silently approved |
| `docs/quality/acceptance.md` | Testable behavior, a11y/negative/operability checks |
| `docs/security/risk-register.md` | Risks with named owners and negative verification to be resolved |
| `delivery/current-state.yaml` | One current milestone, stage, gate, next action and unverified SHA/CI status |
| `delivery/decision-log.json`, `delivery/approvals.json` | Traceability, no fabricated approval; all external actions default false |
| `delivery/evidence.json` | Tests, SHA, workflow URL, reviewer evidence; unverified by default |
| `delivery/method-selection.json` | Snapshot of relevant task-specific and risk-specific controls from Engine v1 |
| `tools/startup.py` | Deterministic **read-only** startup verifier, exit 0 local CONTINUE or exit 2 STOP |
| `tests/test_startup.py` and CI | Verifies the deliberate initial STOP gate, missing files and unsupported claims |
| `docs/operations/release-readiness.md` | Explicitly NOT READY until review and approved release artifacts |
| `README.md`, `.gitignore` | Practical entry points and protection against accidental secret commits |

A new repository must not get fictional implementations or production claims just to make the scaffold look complete. New application code is created only in subsequent accepted vertical-slice milestones. Keep product-specific data/media/telephony/hosting adapters outside the Engine.

## Agent startup and state machine

1. Run `python tools/startup.py` at repository root.
2. The verifier reads essential files and checks schema/project identity, milestone, evidence/authority claims.
3. **STOP** on absent files, inconsistent state, unapproved requirements, unsupported completion, suspicious approval claims or missing authorization. Do not edit unrelated code to bypass.
4. **CONTINUE** is only a *local preflight*; agents must inspect current GitHub HEAD, PR, branch protections, CI, user decision record and code before taking actions. It is not proof of permission to merge/deploy.
5. **ASK** when the next action needs a product decision, security authority, paid infrastructure, credentials, merge, review or deployment. No CLI can approve on the human's behalf.
6. Record new evidence in the existing PR and explicit `delivery/current-state.yaml`; preserve tested source SHA. Another agent should not rely on conversations alone.

The **fail-closed preflight is executable**, but we do not yet enforce agent attention mechanically across all tools. This requires a future GitHub-native permissioned workflow. An AI could ignore markdown; repository branch protections and GitHub checks are distinct enforcement layers. Do not claim otherwise.

## Security/limits and follow-on milestones

**M1 (current):** offline deterministic bootstrap + startup STOP benchmark on VRS, no overwrite or network writes. Negative tests must reject traversal, unknown risks, malformed decisions and unsupported CI completion.

**M2:** real cross-agent handoff: one agent generates the starter, a different session retrieves it and correctly reports stage, risk, next action and stop gates, with no duplicate PR or hallucinated evidence.

**M3:** opt-in GitHub repo creation under explicit account authorization and approved repository namespace/visibility, with idempotency and least-privilege token; never auto-create repos from an idea without confirming intended source ownership.

**M4:** proven lifecycle evidence/benchmark/capability/lessons registries, chosen by cross-app evidence; do not create heavy database.

**M5:** candidate release manifest generator (undeployed) and policy-check integration, reviewed for spoofed evidence, fail-open branches and agent bypass.

**M6:** independently reviewed automation of low-risk worker execution and learning; no self-assigned security authority.

Other required checks before deployment are product-specific. A VRS service would need Deaf-led accessibility acceptance, legitimate telecom/PSTN/emergency policies, provider security review, incident/reconnect SLOs and appropriate legal/regulatory signoff.

## Choosing a method for VRS

At idea intake, select **product discovery, feasibility and requirements** (no code). Once a specific minimal accessible call journey is accepted, select `new-slice` with `identity`, `personal-data`, `external-provider`, `concurrency`, `public-exposure` overlays; separately escalate real-time media quality, telecom and accessibility controls that current selector lacks. First benchmark: a **simulated three-party WebRTC call flow with no PSTN or emergency service**, with browser and reconnect tests; only later add real SIP/PSTN and carrier protocols after external requirements/owners are accepted. A mock signaling demo is not a regulated operational relay service.
