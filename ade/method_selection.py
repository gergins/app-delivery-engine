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
