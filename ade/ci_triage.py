"""Minimal, read-only first-failure localization from externally fetched CI data.

This function does not authenticate GitHub, fetch logs, infer billing failure,
grant authority or change CI. It only classifies an observable failure phase.
"""


def classify_first_failure(*, previous_jobs, failed_jobs, workflow_changed):
    """Classify exact-commit job observations; fail closed on missing inputs.

    Each job must have name, conclusion, runner_name, steps. Provide first failing
    commit jobs, not later failures. Caller must verify SHA and compare workflow
    blobs independently. 'pre-step-unknown' is not a diagnosed root cause.
    """
    if type(workflow_changed) is not bool:
        raise ValueError("Workflow diff status must be explicit")
    if type(previous_jobs) is not list or type(failed_jobs) is not list:
        raise ValueError("Job collections required")
    if not previous_jobs or not failed_jobs:
        return _decision("insufficient-evidence", "missing-jobs")
    for jobs in (previous_jobs, failed_jobs):
        seen = set()
        for job in jobs:
            if type(job) is not dict or set(job) != {
                    "name", "conclusion", "runner_name", "steps"}:
                raise ValueError("Malformed job record")
            if (type(job["name"]) is not str or not job["name"].strip()
                    or job["name"] in seen
                    or job["conclusion"] not in ("success", "failure", "cancelled", "skipped")
                    or type(job["runner_name"]) is not str
                    or type(job["steps"]) is not list):
                raise ValueError("Invalid job metadata")
            seen.add(job["name"])
    if any(j["conclusion"] != "success" or not j["runner_name"] or not j["steps"]
           for j in previous_jobs):
        return _decision("insufficient-evidence", "previous-pass-not-established")
    if not any(j["conclusion"] == "failure" for j in failed_jobs):
        return _decision("insufficient-evidence", "no-failed-job")
    no_steps = all(not j["steps"] for j in failed_jobs)
    no_runner = all(not j["runner_name"] for j in failed_jobs)
    if no_steps and no_runner:
        return _decision(
            "pre-step-unknown",
            "failure-before-recorded-steps",
            workflow_changed=workflow_changed,
            next_owner="repository-actions-operator",
            next_evidence="pre-step-job-error-banner-or-check-annotation")
    if any(j["conclusion"] == "failure" and j["steps"] for j in failed_jobs):
        return _decision(
            "step-execution-failure",
            "inspect-first-failing-step",
            workflow_changed=workflow_changed,
            next_owner="ci-maintainer-or-component-owner",
            next_evidence="first-failing-step-name-and-log")
    return _decision("mixed-or-incomplete", "job-metadata-needs-review",
                     workflow_changed=workflow_changed)


def _decision(phase, reason, *, workflow_changed=None, next_owner=None,
              next_evidence=None):
    return {"phase": phase, "reason": reason,
            "first_failure_workflow_changed": workflow_changed,
            "next_owner_role": next_owner, "next_evidence": next_evidence,
            "root_cause_confirmed": False, "may_change_ci": False,
            "may_skip_required_tests": False, "status": "advisory-only"}
