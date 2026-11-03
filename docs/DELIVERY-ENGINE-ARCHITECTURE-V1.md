# Delivery Engine — unified execution & interface architecture (proposal v1)

**Status:** architectural target and benchmark plan, NOT a claim that all modules exist. Existing Engine has `ade.generator`, `ade.bootstrap`, `ade.method_selection`, a draft cross-agent contract, documentation registries and GitHub Actions evidence. Do not build a large agent orchestration service or dashboard before proving an immediate need.

## Architectural principle

Multiple entry points (CLI, scripts, ChatGPT Work, Codex, GitHub Actions, a future dashboard/API, human engineers) must use the **same application command contracts and the same authorization/verification state model**. Interface-specific helpers may render data but must not independently implement approvals, execution logic or invented statuses. GitHub remains authoritative for repository content, PRs, reviews and CI. The Engine can coordinate these through permissioned adapters but must not pretend a local YAML file equals remote approval.

```text
User / Work / Codex / Human / CI / (later) Web dashboard
                         |
                    Command API
                         |
    Input validation + product state + method/risk selection
                         |
           Policy / authority decision gate
                         |
      Planner (dry run) + capability/benchmark lookup
                         |
     Trusted execution adapter (idempotent, bounded scope)
           /                 |                 \
   local read-only       GitHub tools        CI/test adapters
                         |
           Evidence attestation & reconciliation
                         |
       State/handoff + trace/metrics + approval gate
                         |
        Next bounded milestone / STOP / ASK / CONTINUE
```

Not every command needs a worker. First implement **pure read-only plan and status** commands. Mutating commands must use explicit schema, a dry-run plan, expected prior HEAD, idempotency key, actor/role and bounded filesystem/repository scope; enforce write permissions server-side. Never let a generative agent be the authorization source.

## Command inventory (target capabilities, not automatically implemented)

| Group | Example stable commands | Preconditions / evidence |
| --- | --- | --- |
| Repository | `repo.inspect`, `repo.bootstrap.plan`, `repo.bootstrap.create`, `repo.recover` | Existing/new state checked; remote create separately authorized |
| Product | `product.brief.validate`, `requirements.trace`, `scope.check` | Owner-accepted product decisions, no speculative completion |
| Engineering method | `method.select`, `risk.classify.review`, `architecture.compare`, `adr.propose` | Risk overlays explicit; high-risk classifier advisory |
| Delivery | `milestone.plan`, `change.prepare`, `test.plan`, `ci.verify`, `pr.review` | Bounded scope, exact commit, test/review artifacts |
| Data & integration | `schema.inventory`, `migration.preflight`, `protocol.benchmark`, `restore.rehearse` | Read-only first, real providers only in approved sandbox |
| Release & operations | `release.assess`, `artifact.verify`, `deploy.plan`, `incident.recover` | Independent signoff where required; no auto-deployment |
| Knowledge | `benchmark.record`, `capability.evaluate`, `lesson.propose`, `lesson.validate` | Provenance, tests, licenses, external counterexamples |
| Continuity | `session.start`, `handoff.write`, `state.reconcile`, `approval.request` | Compare declared vs actual GitHub state; no fake approvals |

**Currently implemented pieces:** offline `python -m ade.bootstrap_cli plan/create`, `python -m ade <spec> <destination>`, deterministic `ade.method_selection.select_method`, generated `python tools/startup.py`. Other names above are proposed *contracts*, not runnable commands today.

## Workflow inventory (reusable recipes)

| Recipe | Entry, steps, and outcome |
| --- | --- |
| Idea → ready to implement | Idea intake → feasibility/value → accessible user journey → constraints/risks → requirements review → architecture decision → accepted M1 slice or STOP |
| New app bootstrap | Validate brief → preview plan → owner/namespace decision → offline generation → check required files → CI → optional approved GitHub repo creation → blocked/ready state |
| Existing repo takeover | Inspect actual branch/PR/HEAD → read AGENTS/ADRs/state → run preflight → identify duplicated work → select task/risks → smallest change |
| Feature vertical slice | Acceptance → API/UI/data seam → implementation → negative/browser tests → exact-HEAD CI → updated handoff |
| Defect / broken PR | Reproduce → isolate root cause → fix smallest verified defect → regression → rerun same exact HEAD → record residual risk |
| Schema migration | Read-only inventory → owner/source checks → PostgreSQL contract → synthetic migration → reconciled row hashes → backup/restore → reviewed cutover plan |
| External identity | Simulated unit tests → real disposable provider → forged-state/negative tests → hardened endpoint/credential owner → independent review |
| Release candidate | Trace requirements→tests→artifact → security/license/privacy/a11y/ops → recovery → independent approval → release-ready manifest (not deployment) |
| Handoff/recovery | Compare committed state vs remote GitHub → detect divergence/unverified CI → preserve work → STOP/CONTINUE/ASK → one next action |
| Lessons promotion | Observe in app → reproduce and measure → test counterexample in second app → license/economic review → propose minimal shared contract |

## Logical operation lifecycle

For a command: `RECEIVED → VALIDATED → PLANNED → AUTHORIZED → EXECUTING → VERIFYING → EVIDENCED → COMPLETE`. Distinct terminal states: `STOPPED`, `BLOCKED`, `RETRYABLE_FAILURE`, `FAILED`, `CANCELLED`. Store a causal trace: command ID, input hash, caller identity, repository, expected HEAD, method/risk policy version, scope, approval references, started/ended timestamps, exact tested SHA, CI workflow URL, artifact hashes and remaining risk. Secrets and PII must not be logged.

Every command declares: read vs write vs external/paid effect; required permission; expected inputs/output schema; prerequisites; allowed capabilities; idempotency/retry rule; timeout/cost budget; rollback/compensation; evidence rule; audit redaction; approval conditions; cancellation behavior. No ad hoc shell execution as a generic privileged command.

## Minimal suggested repository structure — grow on verified need

```text
app-delivery-engine/
  AGENTS.md
  README.md
  ade/
    generator.py                # existing
    bootstrap.py                # existing
    bootstrap_cli.py            # existing
    method_selection.py         # existing
    commands/                  # future: typed contracts and dispatch
    policy/                    # future: authoritative policy/approval checks
    workflows/                 # future: composable stage recipes
    execution/                 # future: bounded trusted worker adapters
    evidence/                  # future: sha/CI/review verification
    continuity/                # future: actual remote state reconciliation
    adapters/                  # future: GitHub, test env and providers
  contracts/                   # future: versioned JSON schemas
  registry/
    benchmarks.json             # existing first records
    capabilities.json           # existing first records
    lessons.json                # existing first records
  blueprints/                  # future: reusable application archetypes
  examples/
    vrs-bootstrap.json          # existing, requirement-only
  docs/
    BENCHMARK-TO-OWNERSHIP-POLICY.md
    SENIOR-ENGINEERING-CONTRACT-V1.md
    APP-LIFECYCLE-BENCHMARK-V1.md
    DELIVERY-ENGINE-ARCHITECTURE-V1.md
  tests/
  .github/workflows/
```

Do **not** create every empty folder now. A target tree documents boundaries but is not a reason to create stubs.

## Interfaces: build order and responsibilities

1. **CLI & Python API:** stable, documented commands with deterministic JSON output; read-only `plan/status/preflight` first. Local scripts are useful for reproducible migration inventory, tests, and evidence packaging.
2. **GitHub Action / CI adapter:** exact-HEAD checks, artifact/test/evidence attestation, signed or permissioned approval/branch rules. Source of truth remains GitHub.
3. **Agent interface:** a machine-readable command catalog + AGENTS.md + per-repo startup. Work and Codex call the same command API when available. Markdown alone is NOT enforcement; remote mutating actions must respect GitHub/tool permissions.
4. **Small developer dashboard:** read-only first (portfolio, repo/milestone, current PR/HEAD, failing CI, blockers, approval needs, evidence completeness, handoff and cost). Render backend state, never store another conflicting project status. Later write operations only through the same protected command API.
5. **Optional SDK/API:** for external human/agent integrations after verifying access controls, audit trails and idempotency across two applications.

## Dashboard inventory and overlooked engineering capabilities

- Portfolio view: applications by lifecycle stage, owner, last verified commit, status confidence, costs and blocked approvals.
- Product view: goals, acceptance traceability, user journeys, accessibility findings and milestone dependencies.
- Engineering: PR/CI/review evidence, failures, flaky tests, branch divergence, cross-agent handoffs and pending drift.
- Architecture: ADRs, service boundaries, data ownership, provider dependencies, licenses/SBOM and threat models.
- Operations: migration/recovery status, secrets owner without secrets, backups, incident readiness, SLO and dependency health.
- Governance: approval provenance, separation-of-duties, least privilege, release policy version, independent review status.
- Budget: CI minutes, agent tokens/usage, infra cost forecast and regression effort. Set budgets and fail closed on unexpected spending.
- Knowledge: benchmark/capability/lesson registry with provenance and measured adoption value.

Often overlooked: source-of-truth reconciliation, permissioned actor identity, immutable approval/audit evidence, stale-cache handling, duplicate command execution, concurrency control, compensation of external side effects, secrets redaction, data residency, cancellation/restart, migration and recovery, accessibility, licensing/supply chain, false-green tests, generated code ownership, failure visibility, change impact analysis, and deprecation/retirement. These are **requirements and candidates**, not all implemented features.

## Decision: what to build now

**Current priority:** a shared read-only `status/preflight` contract over the existing bootstrap + exact-GitHub CI evidence, and the minimum evidence schema to drive a future UI. **Not yet:** an autonomous worker orchestration fabric or elaborate dashboard. Benchmark agent resumption on two app types and measure duplicate PRs, time to correct next step, false-green claims and gate violations before implementing execution/policy services. Only add shared infrastructure when repeated real work demonstrates the gap.

### Product example: VRS workflow selection

VRS starts in discovery/requirements, not telephony code. Accept Deaf-led accessible three-party journey, security/privacy and regulatory boundary decisions. Then select `new-slice` with identity/personal-data/external-provider/concurrency/public-exposure risks; prototype authorized three-party WebRTC signaling/media with browser/reconnect tests and **no PSTN/emergency carrier exposure**. Later validate queue/session/orchestrator state, interpreter assignment fairness, media/SFU and SIP/PSTN adapters, accessibility, audit and provider failure modes. Require named independent expertise for telecom/emergency/legal security gates. App-specific VRS modules remain in its own repository; the Engine supplies methodology, approved command contracts and evidence.

### Adoption gates

An implementation must pass a meaningful benchmark in one app, survive a different app's counterexample, show license/security cost and maintenance value, and have owner/reviewer acceptance before entering the capability registry as `adopted`. Source code alone or a green mock test does not constitute universal capability.
