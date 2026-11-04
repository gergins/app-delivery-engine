# Benchmark-to-Ownership Policy v1

**Mandate:** become independent of external frameworks where it creates measurable value, not independent of every external library, protocol or cloud service. The Engine owns the **delivery method, engineering contracts, architectural decision process, evidence, continuity, release gates and operational knowledge**. Product repos own application logic, data, runtime and selected providers.

## Three small registries, not a new platform

1. **Benchmark registry:** append a record for a verified experiment: application/archetype, exact commit and CI, tested capability and boundaries, success/failure metrics, negative cases, version/license of external mechanisms, confidence and next experiment. Missing evidence = not proven.
2. **Capability registry:** for each reusable mechanism, identify owner, interface, lifecycle stage, applicability, exclusions, real implementation status (`candidate`, `benchmarked`, `adopted`, `deprecated`), tests, docs, risk/approval requirements and source benchmark links. Capabilities must not be promoted merely because code exists.
3. **Engineering lessons registry:** record observed failure, root cause, counterexample, mitigation, regression test, affected methods and whether a second app reproduced it. Every lesson needs falsifiable evidence; never build a feedback loop that automatically changes security policies or creates PRs.

Registries start as **version-controlled documentation and small deterministic schemas**. Do not build a database, graph store or knowledge agent until actual cross-app query/reuse needs are demonstrated.

## Safe-to-remove dependency decision

Consider replacing an external tool/framework **only if** (a) a capability is essential and stable, (b) compatibility/security/license risks are understood, (c) the replacement is demonstrably smaller/better for real use, (d) independent tests, threat analysis, operations and rollback/parallel migration exist, and (e) an accountable owner approves the transition. Compare maintenance burden, breaking changes, security posture, lifetime cost, portability and opportunity cost. Retain Python, GitHub, PostgreSQL, WebRTC/SIP, mature IdPs and other proven tools unless a specific evidenced problem justifies replacement. **Never recreate a security-critical protocol implementation simply to claim independence.**

## Evidence-driven ownership milestones

- **O0 — Govern:** one independent repo, AGENTS.md operating contract, risk-aware method selection, stop gates and exact-HEAD CI.
- **O1 — Bootstrap & continuity:** deterministic offline scaffold and a common startup verifier that fails closed if essential files/state are missing; scenario benchmark with an unfamiliar agent resuming a generated app. Repo creation over GitHub is a separately authorized adapter, not part of offline scaffolding.
- **O2 — Lifecycle registry:** trace an idea to requirements, ADR, acceptance, tests, PR evidence, review and undeployed release candidate across two different app archetypes.
- **O3 — Verified reusable capabilities:** extract only mechanisms proven in at least two separate applications; keep provider adapters optional and swappable.
- **O4 — Controlled automation:** agent orchestration, recovery and continuous improvement only after deterministic startup, verified permissions, and independent security review.
- **O5 — Trusted delivery:** release/ops readiness with accountable humans, credentials, platform deployment approvals, rollback and incident response. No inference of authorization from green CI.

**Stop condition:** if a benchmark reveals an essential unmet constraint (e.g. real identity provider proof or independent security signoff), record `BLOCKED`. Do not replace the constraint with an agent assertion or a synthetic green test.

## Decision hierarchy

User's explicit restrictions and required independent authority > security/privacy/legal and repository policies > verified state/data invariants > accepted product requirements > chosen methods > optimization of time/effort. If tradeoffs conflict, escalate and describe alternatives rather than silently choosing convenience.

## Agent startup

Read this policy, `AGENTS.md`, the Senior Engineering Contract, the current application `project.yaml`, `delivery/current-state.yaml` and `docs/decisions/`, then invoke the repository's deterministic startup verifier. It validates declared state and documentation; it **cannot** independently authenticate GitHub's newest HEAD or CI status. Verify those remotely before reporting success or promoting a milestone.

**A generated repository is not a completed application.** Production readiness is always a separate evidenced review and approval.
