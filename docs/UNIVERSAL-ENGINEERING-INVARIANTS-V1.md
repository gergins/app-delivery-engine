# Universal Engineering Invariants Contract v1.0 (proposed)

**Status:** Proposed for review; normative guidance, not yet an automated enforcement mechanism.  
**Scope:** Human contributors, ChatGPT, Codex, autonomous agents, application delivery, research, data, AI systems, and other engineering work.  
**Integration:** Supplements rather than supersedes `AGENTS.md`, `docs/SENIOR-ENGINEERING-CONTRACT-V1.md`, existing method selection, security gates, and repository-specific policy. Where policy conflicts, apply the stricter safety/authority rule and record the conflict; do not silently weaken an existing control.  
**Authority:** A passing check, green CI, or AI reviewer never authorizes merge, deploy, spend, production changes, security approval, or other restricted actions.

## Execution protocol

1. **Discover** the user outcome, current repository reality, evidence, dependencies, unknowns, and applicable risk/authority boundaries.
2. **Declare** consequential under-determined choices *before* dependent code, schemas, tests or documentation. Resolve semantic ambiguities through authorized decisions when `ASK=semantic`.
3. **Reuse** by inspecting existing in-repo and maintained open-source solutions, licenses, security, integration cost, maintainability, and vendor independence.
4. **Build F0**, an actual executable path from a real entry point to a real observable artifact or outcome; stubs may exist *inside* this path and must be labeled.
5. **Add one capability rung at a time**, with explicit predecessor dependencies, acceptance and negative-case checks, and cumulative non-regression evidence.
6. **Verify** contracts, integration boundaries, meaningful test failures, accessibility, security, privacy, observability, and rollback as relevant to risk.
7. **Learn and preserve** the precise change, provenance, decisions, test evidence, observed failures, reusable mechanisms, and remaining unknowns.
8. **Re-enter** discovery/decision/reuse whenever new evidence changes meaning, assumptions, dependencies, risks or authority.

Do not turn this protocol into serial bureaucracy: parallelize independent discovery and tests; gate only the work affected by unresolved consequential decisions. For a trivial, safe, reversible edit, a short record may satisfy the protocol.

## Normative invariants

**I0 — Outcome before implementation.** Name intended user, actual problem, observable result, boundaries and acceptance criterion. If the outcome is not testable, define a falsifiable preliminary hypothesis rather than presenting it as settled.

**I1 — Declare before acting.** The instant an under-determined choice changes meaning, interfaces, persisted data, observable user behavior, permission, risk, or externally relied-on behavior, add a decision-ledger row **before** dependent implementation. Do not backfill a ledger after code as though it were a contemporaneous decision. Under `ASK=semantic`, the proposed row becomes a question to the authorized decision owner; block dependent work until resolution. Unrelated work may continue. A missing or ambiguous owner is a stop condition, not approval by default.

**I2 — Discover before building.** First inspect implemented in-repo capabilities and credible maintained open-source options; compare fitness, license, provenance, maintenance, security, interoperability, reversibility, infrastructure and total lifecycle cost. Reuse, adapt, or wrap when justified; build only where an explicit gap remains. Do not download, execute or trust upstream code merely because it is popular.

**I3 — Spine before features.** F0 is the thinnest runnable walking skeleton: **real entry → actual system seam → real artifact / observable outcome**, with internal stubs explicitly declared. It must run with reproducible evidence before adding feature rungs. A UI-only static demonstration or a passing unit test cannot be represented as a working system path unless the stated outcome is itself UI-only.

**I4 — One verified rung at a time.** Every F1…Fn declares a capability, owner, dependency, changed contracts, acceptance examples, negative case(s), evidence and rollback/recovery expectations. Its checks AND all earlier applicable checks must remain green against the same exact revision. A deliberate behavioral change requires an explicit versioning/migration/acceptance decision, not rewriting an earlier test silently.

**I5 — Contracts before integration.** Identify producers/consumers, interface schema, semantic meaning, auth, errors, versioning, idempotency, timeouts, failure modes, compatibility and migration when applicable. Run consumer or integration contract checks before relying on compatibility. A typed interface alone is not evidence of equivalent meaning.

**I6 — Evidence over assertion.** Label information as observed fact, source-backed claim, hypothesis, assumption, proposed decision, approved decision, simulated result, or verified result. Evidence includes source/date, environment, exact tested revision, commands/checks, results and limits. Never convert a mock, reconstruction, stale CI, self-review or absent evidence into proof of production readiness.

**I7 — Fail safely.** On missing critical evidence, unresolved authority, security or data risk, stop the affected operation safely, preserve state, and explain what unlocks it. Define rollback and recovery paths before consequential modifications; never silently bypass failed checks, change protections, or self-grant approval.

**I8 — Validate independently.** Challenge assumptions and test correctness with representative positive/negative cases, known-bad mutations or counterexamples, cross-component checks, accessibility, security, privacy and usability evidence proportional to risk. An AI adversarial perspective is not independent human security signoff. Validate the ability of an acceptance test to detect incorrect behavior.

**I9 — Optimize verified value.** Optimize for useful, validated outcomes and maintainable simplicity, not number of agents, lines of code, tests or dashboards. Minimize token, compute, CI, infrastructure, review and maintenance costs without weakening meaningful gates. Track when orchestration costs more than it saves and retire unnecessary mechanisms.

**I10 — Preserve and learn.** Store decisions, provenance, reusable mechanisms, limitations, failures, repairs, confidence and counterexamples in versioned handoff/evidence artifacts. Feed lessons into future method selection only after validation; do not automatically promote a pattern from one application to a universal dependency.

**I11 — Search beyond the known.** Intentionally seek hidden assumptions, unknown unknowns, contract mismatches, contradictory evidence, user-journey gaps, silent failures, coupled dependencies, emergent interactions and alternatives to doing the work. Record discovered risks with an experiment or disposition; do not claim an exhaustive search.

**I12 — Keep human authority explicit.** Record decision owner, delegation, permission boundary and approval evidence. Agents may investigate, suggest, implement and test inside authorized scope only. Independent review, final product-semantic arbitration, merge, deploy, purchase, production credential access and security-policy changes require actual designated authority when not expressly delegated.

## ASK policy and semantics

- **`ASK=semantic`** (recommended for consequential product behavior): request approval for every unresolved ambiguity that changes meaning, user-visible promise, data interpretation, permissions, financial commitment or cross-system behavior. The *ledger row* defines the question, alternatives, impact, suggested safe default, owner and blocked dependencies. No silently chosen semantic defaults.
- **`ASK=all`**: also ask about otherwise delegable nonsemantic choices; may impose substantial overhead.
- **`ASK=delegated`**: allow explicitly delegated, low-impact reversible choices, but still record consequential semantic ambiguities and respect existing approval boundaries. Never infer delegation from silence.
- **`ASK` unset**: use the existing repository/owner policy; do not silently assume that silence authorizes consequential semantics.

**Classification:** Semantic includes changes to user-facing meaning, data meaning, contracts, authorization, settlement, security promises, accessibility behavior, and business rules. Nonsemantic includes truly equivalent refactoring or presentation details with no material effect. If unsure, classify as semantic until checked. A test filename, stub value or UI label can itself encode a semantic decision.

## Decision ledger — required *before* dependent work

Use the existing repository decision record or PR handoff; do not create a parallel approval system. Represent at least:

| Field | Required content |
|---|---|
| ID / created_at | Stable row identity, time proposed (not retroactive) |
| Trigger / context | Exact ambiguity, user outcome and where encountered |
| Classification / impact | Semantic or nonsemantic; affected UI, API, data, policy, tests, consumers |
| Options / suggested path | Real alternatives, tradeoffs, reversibility, why a default is/isn't safe |
| Source / confidence | Observation, provenance, assumptions, uncertainty |
| Owner / ASK mode | Authorized resolver and whether this blocks |
| Dependencies | Work, interfaces and acceptance checks blocked by this row |
| Resolution | Pending/approved/rejected/superseded, who decided, when, decision evidence |
| Verification | How to prove implementation matches approved meaning |

**Ordering guarantee:** A row's proposal timestamp must precede the first dependent change; approval must precede the dependent change under `ASK=semantic`. An after-the-fact reconstruction is a changelog and must be labeled that way. If discovered late: stop, record the violation, assess affected work and obtain resolution before continuing; do not falsify chronology.

## F0 and rung acceptance protocol

**F0 preconditions:** outcome/entry/artifact known; unresolved semantic decisions affecting F0 addressed; applicable trust boundaries named; reusable starting point evaluated.

**F0 pass:** start/run instructions reproduce the real entry-to-artifact path; artifact is inspectable; stubs and synthetic providers declared; at least one representative success and failure check are demonstrated; test evidence is tied to an exact revision. An F0 can still be labeled a prototype and must not imply release readiness.

**Every later rung:** define `id`, user capability, dependencies, interfaces, semantic decision references, acceptance/negative examples, changed paths, checks, failure/rollback condition, and actual evidence. Earlier rung checks remain active unless an approved semantics change explicitly supersedes them with migration evidence.

**Quality gates:** Tests cannot prove a behavior if they do not fail on representative wrong behavior; verify this with known-bad input/mutation where proportionate. Differentiate static check, unit, integration, browser, real provider, human usability and production evidence.

## Stop, authority and truthfulness rules

- **BLOCK DEPENDENT WORK:** unresolved semantic row with `ASK=semantic`; unknown authorized decision owner; missing critical security/privacy/accessibility contract; incompatible interface with no approved migration.
- **REPAIR:** failing earlier rung; evidence/test mismatch; F0 is a simulated façade presented as real; discovered missing ledger chronology.
- **DEFER:** useful but unproven additional feature, platform extraction or automation with no current acceptance need.
- **STOP / ESCALATE:** merge, deployment, permissions, external invitations, spending, production credentials, data deletion or security signoff without owner authorization.
- **DONE for this slice:** exact-revision evidence demonstrates the bounded acceptance; residual limitations and next owner are clearly recorded. This is not equivalent to production approval.

## Minimum inspectable handoff

Include: outcome, scope and base/head refs; proposed and approved decisions with chronology; reused or rejected alternatives; F0/rung coverage; tests and meaningful negative cases; exact SHA and CI URLs when available; evidence limits; risks and recovery; unresolved blockers; authority/approval; next smallest permitted action.

## Adoption and precedence

1. Introduce this as **proposed** guidance on a review branch; assess overlap with existing contracts before promotion.
2. Reference the common contract from agent startup instructions **after review**, without duplicating a second decision ledger or status system.
3. Add automated gates incrementally: pre-change decision linkage; schema/contract validation; F0 smoke path; cumulative rung checks; exact-HEAD evidence validation. Describe absent gates as *not implemented*.
4. A repository can tailor risk level, tooling and acceptance evidence, but cannot silently waive consequential semantics, truthful reporting, existing authority, or safety stops.
5. Version on semantic changes, link rationale and migration instructions, and preserve prior versions and approved decisions.

## Worked examples

- **Camping booking:** whether 'available' means temporary hold or committed inventory is a semantic decision. Under `ASK=semantic`, record the row and ask before implementing availability/checkout state; verify concurrent booking and recovery.
- **VRS:** whether a dropped call returns a Deaf user to the old position in queue is a semantic service promise. Resolve ownership and failure contracts before implementing reconnection logic.
- **Engineering registry:** whether a Codex recommendation is 'verified', 'candidate', or 'approved' changes displayed meaning. Record and resolve before using that classification; F0 stores/retrieves an explicitly sourced candidate.
- **Accessibility:** what an interpreter or Deaf user sees when captions fail can change communication semantics and requires an explicit failure policy.

**This contract documents intended behavior; it does not attest that any integration, enforcement, CI or rollout has happened.**

## Implementation decision ledger (recorded before dependent code)

**INV-IMPLEMENT-001 — Initial enforceable slice; proposed and delegated for this bounded PR (2026-11-06)**

- **Trigger:** Owner requested implementation/validation of the proposed invariants on the existing review branch.
- **Classification:** Nonsemantic technical implementation; no change to product-facing behavior, existing permission boundaries, or the definition of approval. Do not infer this selection grants future semantic approvals.
- **Alternatives:** (A) new CI workflows and mandatory repository-wide policy (rejected: broad and disruptive); (B) pure standard-library validator called from existing test discovery (selected: small, reversible); (C) documentation only (rejected: no enforceable behavior).
- **Resolution and scope:** Add a *pure advisory gate* for caller-provided decision and rung manifests; fail closed on malformed chronology, missing semantic approval under ASK=semantic, missing/unverified F0, and broken predecessor rung checks. Supply positive and known-bad tests, without changing existing workflows, agents, app runtime or CI permission policy. This validates only supplied records and **cannot discover omitted decisions, verify a real execution path or authenticate approval identities/CI by itself**.
- **Owner/authority:** Existing owner request to implement the contract within a draft PR; no merge, deployment, mandatory policy or semantic product decision delegated.
- **Blocked dependencies:** New implementation must preserve these constraints, and new acceptance test cases must explicitly demonstrate rejection conditions.
- **Verification:** Python stdlib unittest discovery and exact-HEAD CI if available; report local/remote status separately. Revisit and ask if a semantic meaning, approval policy or automated mandatory CI gate must change.

**INV-IMPLEMENT-002 — Startup integration and test tightening (2026-11-06)**

- **Trigger:** Owner requested continuation after first exact-HEAD green test; reviewers need a discoverable entry path rather than a detached contract document.
- **Classification:** Nonsemantic additive documentation and verification integration. No changes to approval authority, default ASK mode, runtime behavior, or mandatory workflow requirements.
- **Alternatives:** Introduce a new CI job or status check (deferred: scope/approval policy implications); duplicate a second policy in AGENTS (rejected: drift); link the contract from existing startup guidance and test discovery (selected: smallest reversible integration).
- **Scope and resolution:** Link this contract and the pure validator from `AGENTS.md` and documentation index; ensure its test module remains picked up by existing unittest discovery; improve known-bad tests only where behavior is already defined. This **does not make supplied-record validation a mandatory gate for every PR** and does not inspect approval references or real-world F0 evidence.
- **Authority:** Owner authorized bounded continuation on existing draft PR; no semantic product changes, merge, deployment or security approval.
- **Verification:** Exact-HEAD existing CI, negative-case unit tests, PR diff and documentation review. If mandatory repository-wide gates are desired, decide separately under an explicit semantic authority record.

**INV-IMPLEMENT-003 — M1 exact-HEAD evidence composition (2026-11-06)**

- **Trigger:** Owner authorized M1 after the contract/startup CI passed. Current validator trusts supplied pass flags and revision strings and does not compose existing GitHub reconciliation.
- **Class:** Nonsemantic, additive read-only assurance helper; no changes to product meaning, ASK authority, enforcement policy or release gates.
- **Choices:** (A) new GitHub API/CI implementation (rejected: duplicates existing `ade.github_readonly` and `ade.github_reconcile`); (B) make all PRs mandatory (deferred: policy/authorization implications); (C) compose existing reconciled exact-HEAD snapshot with record validator (selected).
- **Scope:** Add `assess_invariant_evidence` using caller-provided GitHub snapshot already reconciled by existing code, require exact matching tested SHA and success, reject unknown/missing CI, stale/untrusted snapshots, and require explicit external evidence references for acceptance claims; keep authority false. Add negative tests. Do not modify external systems or claim authenticated approval, missing-decision discovery, true F0 execution or cryptographic attestation.
- **Owner:** Bounded M1 development permission in existing draft PR; mandatory repository policy and semantic changes remain subject to separate authorization.
- **Acceptance:** New tests reject stale, pending, failed, malformed or incomplete evidence; existing tests remain green; exact-HEAD workflow evidence is checked separately.
