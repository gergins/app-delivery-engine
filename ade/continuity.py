"""Advisory, read-only next-work selection from externally verified project facts.

This module never queries GitHub, grants authority, or writes state. A caller must
first reconcile branch/PR/CI with the remote source of truth.
"""
from dataclasses import dataclass

ALLOWED = frozenset({"security", "broken-ci", "data-integrity", "recovery",
                     "blocked-dependency", "unfinished-slice", "new-slice",
                     "documentation", "optimization"})
ORDER = {"security": 0, "data-integrity": 1, "recovery": 2,
         "broken-ci": 3, "blocked-dependency": 4, "unfinished-slice": 5,
         "new-slice": 6, "documentation": 7, "optimization": 8}
GATES = ("merge", "deploy", "production-credentials", "paid-infrastructure",
         "external-review", "review-policy-change")


def recommend_next_work(snapshot, candidates):
    """Return a deterministic proposal, or STOP when facts are not trustworthy.

    snapshot: remote_verified (bool), head_sha (40 hex), tested_sha (40 hex or
    None), ci_status (success/failure/pending/missing), approvals (mapping).
    candidates: [{id, kind, description, dependency_ready, evidence_ref}].
    No scoring by LLM, no silent authorization, no side effects.
    """
    if type(snapshot) is not dict or type(candidates) is not list:
        raise ValueError("Expected snapshot object and candidate list")
    head = snapshot.get("head_sha")
    if (snapshot.get("remote_verified") is not True
            or type(head) is not str or len(head) != 40
            or any(ch not in "0123456789abcdef" for ch in head)):
        return {"decision": "STOP", "reason": "remote-head-not-verified",
                "next_action": "Inspect actual GitHub branch/PR/HEAD and workflow logs."}
    status = snapshot.get("ci_status")
    if status not in ("success", "failure", "pending", "missing"):
        return {"decision": "STOP", "reason": "unknown-ci-status",
                "next_action": "Reconcile CI status against exact remote HEAD."}
    if status == "success" and snapshot.get("tested_sha") != head:
        return {"decision": "STOP", "reason": "stale-ci-evidence",
                "next_action": "Verify CI on the current exact HEAD."}
    if status in ("pending", "missing"):
        return {"decision": "STOP", "reason": "ci-unverified",
                "next_action": "Inspect or run CI for the current exact HEAD."}
    if type(snapshot.get("approvals")) is not dict:
        return {"decision": "STOP", "reason": "missing-approval-ledger",
                "next_action": "Read GitHub review and approval state."}
    verified = []
    seen = set()
    for item in candidates:
        if type(item) is not dict or set(item) != {
                "id", "kind", "description", "dependency_ready", "evidence_ref"}:
            raise ValueError("Malformed candidate")
        identifier, kind = item["id"], item["kind"]
        if (type(identifier) is not str or not identifier.strip()
                or identifier in seen or kind not in ALLOWED
                or type(item["description"]) is not str
                or not item["description"].strip()
                or type(item["dependency_ready"]) is not bool
                or type(item["evidence_ref"]) is not str
                or not item["evidence_ref"].strip()):
            raise ValueError("Invalid or duplicate candidate")
        seen.add(identifier)
        if item["dependency_ready"]:
            verified.append(item)
    if not verified:
        return {"decision": "STOP", "reason": "no-ready-candidate",
                "next_action": "Inspect dependencies, accepted scope, and unrecorded blockers."}
    selected = min(verified, key=lambda x: (ORDER[x["kind"]], x["id"]))
    if status == "failure" and selected["kind"] not in (
            "security", "data-integrity", "recovery", "broken-ci"):
        return {"decision": "STOP", "reason": "failing-ci-needs-diagnosis",
                "next_action": "Diagnose failing exact-HEAD CI before feature work."}
    return {"decision": "RECOMMEND", "reason": "priority-and-dependency-order",
            "candidate_id": selected["id"], "kind": selected["kind"],
            "description": selected["description"],
            "evidence_ref": selected["evidence_ref"], "head_sha": head,
            "authorization": "advisory-only",
            "protected_actions": list(GATES)}
