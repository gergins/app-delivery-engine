"""Normalize caller-fetched GitHub PR and Actions evidence without network writes.

Caller must obtain the objects directly from the GitHub API/connector at resume
time. This is NOT an independently trusted attestation: inputs may be forged,
GitHub state can change immediately afterward, and approvals are NEVER granted.
"""
import re

SHA = re.compile(r"[0-9a-f]{40}\Z")
RUN_STATES = frozenset({"queued", "in_progress", "completed", "waiting", "requested", "pending"})


def reconcile_github_snapshot(pr, workflow_runs, expected_head=None):
    """Fail closed on missing, conflicting or stale exact-PR-HEAD evidence.

    Returns a snapshot accepted by recommend_next_work; no authority to execute
    follows. Requires actual PR fields head_sha, state, draft and URL plus
    workflow runs with head_sha, status, conclusion, event, id and html_url.
    Only pull_request CI runs are accepted; push checks are not substituted.
    """
    if type(pr) is not dict or type(workflow_runs) is not list:
        raise ValueError("Expected externally fetched PR and Actions responses")
    head = pr.get("head_sha")
    if (type(head) is not str or SHA.fullmatch(head) is None
            or type(pr.get("url")) is not str
            or not pr["url"].startswith("https://github.com/")
            or pr.get("state") != "open" or type(pr.get("draft")) is not bool):
        return {"decision": "STOP", "reason": "unverified-pr-state"}
    if expected_head is not None and expected_head != head:
        return {"decision": "STOP", "reason": "head-diverged", "head_sha": head}
    matches = []
    stale = []
    for run in workflow_runs:
        if type(run) is not dict:
            raise ValueError("Malformed GitHub workflow record")
        if run.get("event") != "pull_request":
            continue
        run_sha = run.get("head_sha")
        if type(run_sha) is not str or SHA.fullmatch(run_sha) is None:
            return {"decision": "STOP", "reason": "unverifiable-workflow-sha"}
        if run_sha != head:
            stale.append(run_sha)
            continue
        if (type(run.get("id")) is not int
                or type(run.get("html_url")) is not str
                or not run["html_url"].startswith("https://github.com/")
                or run.get("status") not in RUN_STATES):
            return {"decision": "STOP", "reason": "unverifiable-workflow"}
        matches.append(run)
    if not matches:
        return {"decision": "STOP", "reason": "no-exact-head-run",
                "head_sha": head, "stale_run_count": len(stale)}
    # Duplicate runs are not taken as a success unless *all* exact-head runs
    # complete successfully. One failure or pending run blocks promotion.
    if any(r["status"] != "completed" for r in matches):
        status, tested = "pending", None
    elif any(r.get("conclusion") != "success" for r in matches):
        status, tested = "failure", None
    else:
        status, tested = "success", head
    return {"decision": "RECONCILED", "remote_verified": True,
            "head_sha": head, "tested_sha": tested, "ci_status": status,
            "workflow_urls": sorted({r["html_url"] for r in matches}),
            "pr_url": pr["url"], "pr_draft": pr["draft"],
            "stale_run_count": len(stale),
            # Fail closed: a GitHub PR snapshot cannot convey user permission
            # to merge, deploy, spend, grant access or sign security assurance.
            "approvals": {"merge": False, "deploy": False,
                          "production_credentials": False},
            "authority": "no-authorization-derived",
            "caveat": "caller-supplied-GitHub-responses-not-cryptographically-attested"}
