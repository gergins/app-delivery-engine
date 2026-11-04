# VRS application — illustrative lifecycle and independent product repository

**Purpose:** example for method-selection and bootstrap only. Do not confuse this with an implementation or permission to replace the user's existing VRS repositories. Inspect all relevant existing VRS repos and current work before deciding whether a new GitHub repository is actually needed. Avoid duplicate source of truth.

## Example owner workflow

1. **Idea / discovery**: validate affected users and accessibility needs with Deaf callers, interpreters and service authorities. Document successful call outcome, success metrics, non-goals, technical/telecom jurisdiction, privacy, emergency handling and procurement restrictions. Escalate unknown regulation.
2. **Define one demonstrator**: a synthetic Deaf caller and interpreter join a virtual room; optional third-party/hearing test participant is simulated in browser. Define a11y acceptance (visible alerts, focus, captions/RTT where relevant, sign-language-first video, keyboard/mobile experience). No real SIP/PSTN or emergency calls.
3. **Select method**: lifecycle stage = accepted requirements then minimal implementation; task = `new-slice`; risk flags = identity, personal data, external provider, concurrency, public exposure. Domain add-ons: real-time media, queue fairness, accessibility, reconnect reliability and telecom/emergency constraints require reviewed acceptance. No generic coding model should silently omit these.
4. **Review architecture**: assign bounded responsibilities: web caller UI, interpreter UI, operator UI; ingress signaling; queue reservation; authoritative session orchestration; presence; media provider adapter; future SIP/PSTN adapter. Contract each state machine and event ordering before distributed deployment. Do not run microservices until tested traffic/team needs justify them.
5. **Implement**: one vertical browser flow with fake users and no live telephone calls. Tests: two/three-party joins, permission denial, role changes, reconnect, offer expiry, concurrency, accessibility, camera refusal, network loss and idempotent recovery. Run real browser WebRTC/media tests against a supported nonproduction media provider only with approved controls.
6. **Review**: exact SHA unit/browser/provider CI and security/privacy/accessibility design review; collect negative tests, event traces and known limitations. No source-code self-review counts as independent authority.
7. **Handoff**: record milestone, acceptance, live vs mocked evidence, current PR, SHA, CI URLs, blockers, next bounded step in GitHub. Work/Codex must run startup and use the same verified contract.
8. **Later**: queue fairness/dispatcher override, interpreter workforce controls, media SFU reliability, SIP/PSTN adapters, audit/data minimization, regional compliance, support/incident, recording consent, emergency routing if authorized. Real public relay service requires telecom/legal/security and Deaf-led accessibility signoff.

## Proposed **application repository** layout (not a demand to create all folders)

```text
vrs-app/
  AGENTS.md
  project.yaml
  delivery/
    current-state.yaml
    approvals.json
    evidence.json
    decision-log.json
  docs/
    product/requirements.md
    product/journeys.md
    product/vrs-invariants.md
    architecture/overview.md
    architecture/state-machines.md
    decisions/0001-initial-constraints.md
    security/risk-register.md
    quality/acceptance.md
    operations/release-readiness.md
  apps/
    caller-web/                 # only when implementing caller slice
    interpreter-web/            # later, when justified
    operator-web/               # later, when justified
  services/
    signaling-api/              # may start combined in one app process
    queue-engine/
    session-orchestrator/
    presence-service/
    media-router/
    telephony-gateway/          # future, approval gated
  packages/
    contracts/                  # typed API/events and state machines
    accessibility/
    telemetry/
  adapters/
    media/                      # optional LiveKit/Janus/etc
    telephony/                  # future provider-agnostic SIP/PSTN
  tests/
    contract/
    browser/
    security/
    recovery/
  tools/
    startup.py
  .github/workflows/
```

The **initial generated starter has only requirements/AGENTS/state/CI**, not all the application files above. Folders are added on the first accepted need. Product services own runtime implementations and deployment manifests. The Engine owns only reusable delivery contracts, benchmarks, quality gates and continuity.

## Reusable commands versus product scripts

Engine-level: `repo.bootstrap.plan`, `method.select`, `repo.continuity.start`, future `test.plan`, `ci.verify`, `release.assess`. All use one policy and evidence model. A VRS product may have small scripts to run an isolated signaling server, create synthetic participants, capture browser join/reconnect test evidence and validate event schemas. Those scripts remain in the VRS repo; extract to Engine only after a different app demonstrates a reusable need. No script may silently start a public relay, real PSTN connection, spend money or invoke production credentials.

## Real-world stopping examples

- **Unknown emergency-call legal obligations** → STOP and request qualified review, not guess behavior.
- **Caller can join but reconnect lost queue state** → FAIL tests, repair session state before broadening scope.
- **WebRTC mock passes, actual media provider never tested** → PARTIAL, not live-service-ready.
- **Worker claims CI passed but HEAD changed** → STOP, rerun exact HEAD.
- **Product owner asks to release** → assess acceptance/recovery/security/telecom approvals, then explicitly ASK before deployment.
- **Another chat/Codex resumes** → run startup, reconcile GitHub and current PR, select next bounded method, report evidence and gaps before editing.
