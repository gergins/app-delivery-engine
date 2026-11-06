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


def assess_invariant_evidence(*, decisions, rungs, github_snapshot, ask="semantic"):
    """Compose the existing GitHub reconciliation with supplied invariant records.

    The caller must fetch the PR and workflow runs using an authorized read-only
    route and call github_reconcile/readonly. A caller can still forge these
    objects; this pure function cannot authenticate GitHub, tests, reviewers,
    timestamps or approvals and must never grant release authority.
    """
    from .github_reconcile import SHA

    if type(github_snapshot) is not dict:
        raise ValueError("missing GitHub snapshot")
    head = github_snapshot.get("head_sha")
    if (github_snapshot.get("decision") != "RECONCILED"
            or github_snapshot.get("remote_verified") is not True
            or github_snapshot.get("authority") != "no-authorization-derived"
            or type(head) is not str or SHA.fullmatch(head) is None
            or github_snapshot.get("tested_sha") != head
            or github_snapshot.get("ci_status") != "success"):
        raise ValueError("missing successful exact-HEAD CI evidence")
    urls = github_snapshot.get("workflow_urls")
    if (type(urls) is not list or not urls
            or any(type(url) is not str
                   or not url.startswith("https://github.com/")
                   for url in urls)):
        raise ValueError("missing CI links")
    if not isinstance(rungs, list):
        raise ValueError("invalid rungs")
    for rung in rungs:
        if type(rung) is not dict or rung.get("evidence_revision") != head:
            raise ValueError("rung not checked at exact PR HEAD")
        refs = rung.get("evidence_refs")
        if (type(refs) is not list or not refs or any(
                type(ref) is not str or not ref.startswith("https://github.com/")
                for ref in refs)):
            raise ValueError("missing inspectable rung evidence references")
    assessment = assess_invariant_records(decisions=decisions, rungs=rungs, ask=ask)
    return {**assessment, "ci_status": "success",
            "exact_head_sha": head,
            "ci_evidence_urls": list(urls),
            "authority": "no-authorization-derived",
            "evidence_limit": "caller-supplied-snapshot-and-attestations-not-authenticated"}


def assess_rung_job_steps(*, invariant_assessment, rungs, workflow_run_id, jobs):
    """Match explicitly named rung checks against read-only GitHub job metadata.

    Caller must obtain jobs from the exact workflow run independently. Step name
    matching is evidence of execution, NOT proof of test semantics or identity.
    """
    if (type(invariant_assessment) is not dict
            or invariant_assessment.get("decision") != "records-consistent"
            or invariant_assessment.get("ci_status") != "success"
            or invariant_assessment.get("approval_granted") is not False
            or type(invariant_assessment.get("exact_head_sha")) is not str
            or type(workflow_run_id) is not int or workflow_run_id <= 0
            or type(jobs) is not list or not jobs
            or type(rungs) is not list or not rungs):
        raise ValueError("missing prior exact-HEAD verification or workflow jobs")

    matched = {}
    for job in jobs:
        if (type(job) is not dict or type(job.get("id")) is not int
                or type(job.get("run_id")) is not int
                or job["run_id"] != workflow_run_id
                or job.get("status") != "completed"
                or job.get("conclusion") != "success"
                or type(job.get("steps")) is not list):
            raise ValueError("incomplete or mismatched GitHub job")
        for step in job["steps"]:
            if type(step) is not dict or type(step.get("name")) is not str:
                raise ValueError("malformed job step")
            name = step["name"]
            if name in matched:
                raise ValueError("duplicate step names cannot anchor rung proof")
            matched[name] = step

    checked = {}
    for rung in rungs:
        if (type(rung) is not dict
                or rung.get("evidence_revision") != invariant_assessment["exact_head_sha"]
                or type(rung.get("id")) is not str
                or type(rung.get("evidence_steps")) is not dict):
            raise ValueError("missing rung step mapping")
        steps = rung["evidence_steps"]
        if set(steps) != {"positive", "negative"}:
            raise ValueError("positive and negative step names required")
        pos, neg = steps["positive"], steps["negative"]
        if (type(pos) is not str or type(neg) is not str
                or not pos or not neg or pos == neg):
            raise ValueError("distinct named positive/negative checks required")
        for name in (pos, neg):
            step = matched.get(name)
            if (step is None or step.get("status") != "completed"
                    or step.get("conclusion") != "success"):
                raise ValueError("rung step absent, pending or failed: " + name)
        if rung["id"] in checked:
            raise ValueError("duplicate rung ID")
        checked[rung["id"]] = {"positive": pos, "negative": neg}

    if len(checked) != invariant_assessment.get("rungs_checked"):
        raise ValueError("rung coverage differs from prior assessment")

    return {"decision": "step-names-matched", "status": "advisory-only",
            "exact_head_sha": invariant_assessment["exact_head_sha"],
            "workflow_run_id": workflow_run_id, "matched_rungs": checked,
            "approval_granted": False,
            "evidence_limit": "caller-supplied-metadata-and-step-names-not-test-semantics"}
