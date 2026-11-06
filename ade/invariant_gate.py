"""Conservative validator for caller-supplied invariant evidence.

This does not find omitted decisions, run F0, authenticate approval or verify CI.
It grants no authority.
"""
from datetime import datetime


def _time(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be an ISO string")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("invalid timestamp") from error
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timestamp must contain timezone")
    return result


def _required(row, fields):
    if not isinstance(row, dict):
        raise ValueError("record must be an object")
    for field in fields:
        if field not in row or row[field] is None or row[field] == "":
            raise ValueError("missing " + field)


def assess_invariant_records(*, decisions, rungs, ask="semantic"):
    """Check chronology and rung claims supplied by the caller, fail closed."""
    if ask not in ("semantic", "all", "delegated"):
        raise ValueError("unknown ASK policy")
    if not isinstance(decisions, list) or not isinstance(rungs, list) or not rungs:
        raise ValueError("decisions and nonempty rungs must be lists")

    seen = set()
    for row in decisions:
        _required(row, ("id", "classification", "proposed_at",
                        "first_dependent_change_at", "status"))
        if not isinstance(row["id"], str) or not row["id"] or row["id"] in seen:
            raise ValueError("duplicate or malformed decision ID")
        seen.add(row["id"])
        if row["classification"] not in ("semantic", "nonsemantic"):
            raise ValueError("unknown decision classification")
        if _time(row["proposed_at"]) >= _time(row["first_dependent_change_at"]):
            raise ValueError("decision not declared before dependent change")
        approval_needed = ask == "all" or (
            ask == "semantic" and row["classification"] == "semantic")
        if approval_needed:
            _required(row, ("owner", "approved_at", "approval_reference"))
            if row["status"] != "approved":
                raise ValueError("unapproved decision")
            if not (_time(row["proposed_at"]) <= _time(row["approved_at"])
                    < _time(row["first_dependent_change_at"])):
                raise ValueError("approval not before dependent change")
        elif row["status"] not in ("proposed", "approved", "rejected", "superseded"):
            raise ValueError("unknown status")

    for index, rung in enumerate(rungs):
        _required(rung, ("id", "entry", "artifact", "evidence_revision",
                         "checks_passed", "negative_checks_passed", "decision_refs"))
        if rung["id"] != "F" + str(index):
            raise ValueError("rungs must be ordered F0...Fn")
        if not isinstance(rung["decision_refs"], list) or any(
                ref not in seen for ref in rung["decision_refs"]):
            raise ValueError("unknown decision reference")
        if rung["checks_passed"] is not True or rung["negative_checks_passed"] is not True:
            raise ValueError("rung checks not green")
        if not isinstance(rung["evidence_revision"], str) or not rung["evidence_revision"].strip():
            raise ValueError("missing revision")
        if index == 0:
            if rung.get("running_spine_verified") is not True or rung.get("stubs_disclosed") is not True:
                raise ValueError("F0 real spine / stubs not attested")
        else:
            if rung.get("predecessor_ids") != ["F" + str(n) for n in range(index)]:
                raise ValueError("missing predecessor regression coverage")
            if rung["evidence_revision"] != rungs[0]["evidence_revision"]:
                raise ValueError("rungs verified against different revisions")

    return {"decision": "records-consistent", "status": "advisory-only",
            "independent_evidence_required": True, "approval_granted": False,
            "rungs_checked": len(rungs), "decisions_checked": len(decisions)}
