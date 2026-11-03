# Documentation map, verified capabilities, and engineering decisions

**Source of truth:** repository code, PR reviews, exact-commit CI and approved product decisions. This index is not proof that a planned capability is implemented. Read [AGENTS.md](../AGENTS.md) first. When returning after a lost browser/session, use [Continuity & Next Work](CONTINUITY-NEXT-WORK-V1.md).

## Start here by task

| Need | Existing authoritative document | Current reality |
| --- | --- | --- |
| Get a useful app running | [README quick start](../README.md), [Delivery usability milestones](DELIVERY-USABILITY-MILESTONES-V1.md) | Existing local web-list UI/API/SQLite generator, not production |
| Start an application idea | [Bootstrap continuity](BOOTSTRAP-CONTINUITY-M1.md), [AGENTS](../AGENTS.md) | Offline requirements-first starter, not a working VRS or online repo creator |
| Resume a lost/interrupted session | [Continuity & next work](CONTINUITY-NEXT-WORK-V1.md), [Handoff](HANDOFF.md) | Offline startup + pure GitHub response reconciliation/selector; no remote fetch/attestation integration yet |
| Choose engineering methods | [Method selection](METHOD-SELECTION-V1.md), [Senior engineer contract](SENIOR-ENGINEERING-CONTRACT-V1.md) | Advisory risk-specific method only |
| Choose architecture, interfaces, commands | [Architecture](DELIVERY-ENGINE-ARCHITECTURE-V1.md), [command registry](../registry/commands.json) | Most unified commands/adapters remain design proposals |
| Review complete application lifecycle | [Lifecycle benchmark](APP-LIFECYCLE-BENCHMARK-V1.md) | Acceptance/evidence gates documented, not automated end-to-end |
| Evaluate reusable patterns | [Benchmark-to-ownership policy](BENCHMARK-TO-OWNERSHIP-POLICY.md), [capability registry](../registry/capabilities.json), [lessons](../registry/lessons.json) | Limited records; never infer adoption from an experiment |
| Evaluate a particular app | [Camping benchmark](BENCHMARK-CAMPING-BASELINE-V1.md), [Life Services Hub benchmark](BENCHMARK-LIFE-SERVICES-HUB-V1.md), [VRS reference](VRS-REFERENCE-WORKFLOW.md) | App-specific checks, not universal Engine guarantees |

## Verified delivery chain and gaps

The chain to prove is **brief → owner-accepted requirement → bounded runnable slice → tests → exact HEAD CI → review → usable preview → recoverable handoff → next decision**.

| Link | Existing mechanism | Evidence still needed / gap |
| --- | --- | --- |
| Brief to scope | bootstrap strict JSON | Product owner accepts measurable requirement and non-goals |
| Scope to runnable app | separate web-list generator | Unified opt-in path with bootstrap, *without* hidden scope changes |
| Runnable app to tests | synthetic HTTP/SQLite/browser exercises | Fresh contributor usability, keyboard/a11y assessment, negative failures |
| Tests to trusted evidence | pinned Actions + SHA assertion | Workflow success for the **current** candidate HEAD, job logs, trustworthy source linkage |
| Evidence to review | AGENTS/contract and PR | Real reviewer identity and approvals; not a fabricated JSON boolean |
| App to preview | local HTTP server | Accessible, reproducible independent preview; no deployment implied |
| Interruption to resume | generated startup + pure reconciliation | Live GitHub read adapter, branch/PR drift detection, stable work checkpoints |
| Resume to next slice | pure deterministic selector | Provenance-backed survey and comparisons across at least two apps |
| Release candidate to operations | lifecycle documentation | App-specific backups, restore, rollback, threat model, cost, owner and human gate |

## Senior-engineering decision rules

1. **Inspect before inventing.** Check current code, PRs, CI logs and actual user journey. A failed test or unverified state outranks a new feature.
2. **Prioritize impact and prerequisites.** Repair security/data loss/recovery, then broken tests or blocked accepted outcomes. Prefer the smallest coherent vertical slice; do not optimize individual component neatness at the cost of the user journey.
3. **End-to-end means behavior, not breadth.** A slice is complete only when a person can perform its accepted task, data/state survives the required lifecycle, negative cases are tested, evidence matches source HEAD, and the next contributor can resume. It does not imply all product features or production readiness.
4. **Define a stopping point.** Stop adding capability when the accepted outcome is met and verified, incremental user value is low, or further work requires owner/reviewer/provider approval. Do not keep polishing because the backlog is nonempty.
5. **Add a shared Engine mechanism only with evidence.** Require (a) the same demonstrated gap across two different apps or a critical common security invariant, (b) a reproducible failure, (c) less lifetime complexity than a local workaround, (d) tests, documentation, license review, (e) an owner and maintenance strategy. Otherwise keep the fix app-local.
6. **Usability is a release input, not optional decoration.** Measure first-run commands/manual edits, understanding of errors, browser task success, keyboard/focus/labels and independent handoff; avoid claiming that synthetic automation measures human usability.
7. **Explicitly defer** speculative multi-agent orchestration, rich admin dashboards, dozens of templates, generic cloud provisioning, autonomous merge/deploy and complex workflow languages until a demonstrated repeated user bottleneck justifies them.
8. **Preserve authority and evidence boundaries.** Local JSON and model suggestions never authorize account changes, production credentials, payments, merge, deployment, external review or security signoff.

## Next engineering milestone

**P0:** Verify current draft PR CI; if failing, repair root cause. Integrate *read-only* GitHub PR/Actions fetching with snapshot reconciliation and next-work selection. Exercise interruption on Camping Booking and a different app. Record whether recovery chose the right next step and whether it avoided duplicate PRs. Until real GitHub fetch+integration is proven, call this **pure reconciliation contract**, not autonomous recovery.

Do not create new documents or layers for merely synonymous concepts. Consolidate existing overlapping docs before building another interface.
