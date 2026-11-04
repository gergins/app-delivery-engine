"""Explicit read-only GitHub REST lookup for PR continuity; never mutates state.

Requires network only when called. Default behavior uses public API, or an
already-provided GITHUB_TOKEN environment variable for private repository read.
No token is written to disk or printed. Use only on a trusted runner.
"""
import argparse
import json
import os
import re
import urllib.error
import urllib.request
from urllib.parse import urlencode, urlparse

from .github_reconcile import reconcile_github_snapshot

_REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
_SHA = re.compile(r"[0-9a-f]{40}\Z")
_API = "https://api.github.com"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("GitHub API redirect refused")


def _json_get(url, *, token=None):
    if (urlparse(url).scheme != "https"
            or urlparse(url).netloc != "api.github.com"):
        raise ValueError("Only api.github.com HTTPS read operations are allowed")
    headers = {"Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28",
               "User-Agent": "app-delivery-engine-readonly/1"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(url, headers=headers, method="GET")
    opener = urllib.request.build_opener(_NoRedirect())
    with opener.open(request, timeout=15) as response:
        raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("GitHub response exceeds safe bound")
    return json.loads(raw)


def inspect_pull_request(repo, number, *, fetch=None):
    """Read PR and exact-head PR-triggered Actions. Caller must re-check HEAD.

    fetch is an injectable URL->JSON function for no-network tests. Failures
    propagate and must be treated as STOP; stale cached snapshots are unsafe.
    """
    if (type(repo) is not str or not _REPO.fullmatch(repo)
            or any(segment in (".", "..") for segment in repo.split("/"))):
        raise ValueError("Invalid repository owner/name")
    if type(number) is not int or not 1 <= number <= 1_000_000:
        raise ValueError("Invalid PR number")
    if fetch is None:
        token = os.environ.get("GITHUB_TOKEN")
        fetch = lambda url: _json_get(url, token=token)
    api = _API + "/repos/" + repo
    item = fetch(api + "/pulls/" + str(number))
    if type(item) is not dict or type(item.get("head")) is not dict:
        return {"decision": "STOP", "reason": "unverifiable-pr-response"}
    head = item["head"].get("sha")
    if type(head) is not str or _SHA.fullmatch(head) is None:
        return {"decision": "STOP", "reason": "unverifiable-head-sha"}
    pr = {"head_sha": head, "state": item.get("state"),
          "draft": item.get("draft"), "url": item.get("html_url")}
    query = urlencode({"event": "pull_request", "head_sha": head, "per_page": 100})
    result = fetch(api + "/actions/runs?" + query)
    if (type(result) is not dict or type(result.get("workflow_runs")) is not list
            or type(result.get("total_count")) is not int):
        return {"decision": "STOP", "reason": "unverifiable-ci-response"}
    runs = result["workflow_runs"]
    if result["total_count"] > len(runs):
        return {"decision": "STOP", "reason": "ci-results-incomplete",
                "head_sha": head}
    # Re-read current PR to catch a branch push during CI lookup. This is a
    # read-only best-effort drift check, not a lock or atomic GitHub snapshot.
    final_item = fetch(api + "/pulls/" + str(number))
    if (type(final_item) is not dict or type(final_item.get("head")) is not dict
            or final_item["head"].get("sha") != head):
        return {"decision": "STOP", "reason": "head-changed-during-inspection",
                "observed_head_sha": head}
    if (final_item.get("state") != item.get("state")
            or final_item.get("draft") != item.get("draft")):
        return {"decision": "STOP", "reason": "pr-state-changed-during-inspection"}
    normalized = reconcile_github_snapshot(pr, runs, expected_head=head)
    if normalized.get("decision") == "RECONCILED":
        normalized["retrieval"] = "github-rest-read-only"
        normalized["repo"] = repo
        normalized["pr_number"] = number
        normalized["source_limit"] = (
            "PR/CI snapshot only; reviews, logs, issue dependencies and "
            "branch changes after retrieval still require checking")
    return normalized


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only GitHub PR continuity inspection")
    parser.add_argument("repository", help="owner/repository")
    parser.add_argument("pr", type=int)
    args = parser.parse_args(argv)
    try:
        result = inspect_pull_request(args.repository, args.pr)
    except (ValueError, OSError, urllib.error.URLError, json.JSONDecodeError):
        # Never print token, response bodies or confidential error details.
        result = {"decision": "STOP", "reason": "remote-github-retrieval-failed"}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["decision"] == "RECONCILED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
