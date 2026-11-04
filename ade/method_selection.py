"""Deterministic, advisory selection of minimum delivery controls.

This is a decision aid, not a security assessor or autonomous agent. It combines
proven practices without inventing a framework or bypassing required approvals.
"""
from dataclasses import dataclass

KINDS = frozenset({"new-slice", "bugfix", "refactor", "schema-change",
                   "integration", "release-preparation"})
RISKS = frozenset({"identity", "payment", "personal-data", "external-provider",
                   "migration", "concurrency", "public-exposure"})
BASE = (
    "inspect-current-repository-pr-and-evidence",
    "define-bounded-change-and-acceptance-criteria",
    "reuse-existing-mechanisms",
    "implement-smallest-reviewable-change",
    "run-negative-and-positive-regressions",
    "verify-exact-head-ci-and-logs",
    "record-gaps-in-existing-pr-and-handoff",
)
KIND_CONTROLS = {
    "new-slice": ("verify-runnable-ui-api-data-journey",),
    "bugfix": ("reproduce-defect-first", "keep-regression-test"),
    "refactor": ("characterize-existing-behavior", "verify-no-behavior-drift"),
    "schema-change": ("versioned-additive-migration", "test-upgrade-rollback-restore"),
    "integration": ("contract-and-failure-mode-tests", "verify-real-provider-before-live-claims"),
    "release-preparation": ("security-privacy-a11y-operations-review", "recovery-and-rollback-rehearsal"),
}
RISK_CONTROLS = {
    "identity": ("deny-unverified-identity", "test-revocation-session-and-privilege-boundaries",
                 "require-real-idp-proof-for-live-identity-claims"),
    "payment": ("test-idempotency-webhooks-and-reconciliation", "review-merchant-legal-controls"),
    "personal-data": ("privacy-retention-access-and-redaction-review",),
    "external-provider": ("adapter-contract-failure-and-outage-tests", "document-provider-credentials-owner"),
    "migration": ("versioned-additive-migration", "test-upgrade-rollback-restore"),
    "concurrency": ("test-competing-writers-and-restart",),
    "public-exposure": ("threat-model-and-independent-security-review", "require-deployment-authorization"),
}
STOP_GATES = (
    "no-automatic-merge",
    "no-automatic-deployment-or-public-hosting",
    "no-production-credentials-or-spending",
    "no-review-policy-or-ci-bypass",
    "no-unverified-live-provider-claims",
)


def select_method(kind, risks=()):
    """Return a stable reviewable method; reject unknown inputs fail-closed.

    Unknown risk flags are not silently treated as low-risk. No risk weights or
    automatic authorization decisions are generated.
    """
    if type(kind) is not str or kind not in KINDS:
        raise ValueError("Unknown task kind")
    if type(risks) not in (tuple, list, set, frozenset):
        raise ValueError("Risks must be an explicit collection")
    if any(type(r) is not str or r not in RISKS for r in risks):
        raise ValueError("Unknown or malformed risk flag")
    selected = sorted(set(risks))
    steps = []
    for step in BASE + KIND_CONTROLS[kind] + tuple(
        item for risk in selected for item in RISK_CONTROLS[risk]
    ):
        if step not in steps:
            steps.append(step)
    return {"method_version": "1.0", "kind": kind, "risks": selected,
            "controls": steps, "stop_gates": list(STOP_GATES),
            "evidence_required": ["repository", "branch", "exact_commit_sha",
                                  "workflow_url", "completed_ci_result", "remaining_risks",
                                  "review_and_approval_status"],
            "status": "advisory-only"}

# Evidence reuse is an advisory decision, NEVER an authorization to bypass CI,
# branch protection, required checks, security review or release approval.
EVIDENCE_KEYS = frozenset({"behavior", "result", "commit_sha", "environment",
                           "dependencies", "scope", "evidence_url"})
HIGH_CONSEQUENCE = frozenset({"identity", "payment", "personal-data",
                              "migration", "concurrency", "public-exposure"})


def assess_evidence_reuse(*, behavior, changed_scopes, current_dependencies,
                          environment, evidence, risks=()):
    """Conservative explicit-input decision; does not discover impacts itself.

    A caller must establish the complete impacted scope using code review and
    dependency analysis. A passing past test is reusable only for an unchanged
    behavior and precisely matched dependencies/environment. Required current
    CI gates and approvals remain independent of this decision.
    """
    if type(behavior) is not str or not behavior.strip():
        raise ValueError("Behavior must be a nonempty string")
    if type(changed_scopes) not in (list, tuple, set, frozenset) or any(
            type(s) is not str or not s.strip() for s in changed_scopes):
        raise ValueError("Changed scopes must be explicit strings")
    if type(current_dependencies) is not dict or any(
            type(k) is not str or type(v) is not str or not k or not v
            for k, v in current_dependencies.items()):
        raise ValueError("Dependencies must be a known name/version mapping")
    if type(environment) is not str or not environment.strip():
        raise ValueError("Environment required")
    if type(risks) not in (tuple, list, set, frozenset) or any(
            type(r) is not str or r not in RISKS for r in risks):
        raise ValueError("Unknown or malformed risk flag")
    if type(evidence) is not dict or not EVIDENCE_KEYS.issubset(evidence):
        return _evidence_decision("targeted-verification", "missing-evidence")
    if (type(evidence["dependencies"]) is not dict
            or type(evidence["scope"]) not in (list, tuple, set, frozenset)
            or any(type(s) is not str for s in evidence["scope"])):
        return _evidence_decision("targeted-verification", "invalid-evidence-shape")
    if any(type(evidence[k]) is not str or not evidence[k].strip()
           for k in ("behavior", "result", "commit_sha", "environment", "evidence_url")):
        return _evidence_decision("targeted-verification", "incomplete-provenance")
    if evidence["result"] != "passed":
        return _evidence_decision("targeted-verification", "no-passing-evidence")
    if behavior != evidence["behavior"] or behavior not in evidence["scope"]:
        return _evidence_decision("targeted-verification", "behavior-not-covered")
    if set(changed_scopes) & set(evidence["scope"]):
        return _evidence_decision("expanded-verification", "tested-scope-changed")
    if evidence["dependencies"] != current_dependencies:
        return _evidence_decision("expanded-verification", "dependency-drift")
    if evidence["environment"] != environment:
        return _evidence_decision("targeted-verification", "environment-drift")
    if set(risks) & HIGH_CONSEQUENCE:
        return _evidence_decision("targeted-verification", "high-consequence-risk")
    return _evidence_decision("reuse-prior-evidence", "unchanged-covered-behavior")


def _evidence_decision(decision, reason):
    return {"decision": decision, "reason": reason, "status": "advisory-only",
            "current_ci_required": True, "approval_gates_unchanged": True,
            "dependency_impact_must_be_human_verified": True}
