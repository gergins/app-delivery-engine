"""Provider-independent, read-only agent work-order admission for existing app PRs.

A GitHub evidence snapshot is not execution authority. This module prepares
a structured handoff for a separately authorized Work/Codex/human implementer.
It neither calls an LLM nor writes to a remote repository.
"""
import argparse
import json
import re

from .github_readonly import inspect_pull_request
from .method_selection import select_method

REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")


def prepare_work_order(*, repository, pr_number, task, acceptance, kind,
                       risks, snapshot):
    if type(repository) is not str or not REPO.fullmatch(repository):
        raise ValueError("Invalid repository")
    if type(pr_number) is not int or not 1 <= pr_number <= 1000000:
        raise ValueError("Invalid PR number")
    if (type(task) is not str or not 10 <= len(task.strip()) <= 1000
            or any(ord(c) < 32 for c in task)):
        raise ValueError("A bounded written task is required")
    if (type(acceptance) is not list or not 1 <= len(acceptance) <= 10
            or any(type(v) is not str or not 5 <= len(v.strip()) <= 300
                   or any(ord(c) < 32 for c in v) for v in acceptance)):
        raise ValueError("Explicit testable acceptance required")
    method = select_method(kind, risks)
    if type(snapshot) is not dict or snapshot.get("repo") != repository or snapshot.get("pr_number") != pr_number:
        raise ValueError("GitHub evidence must match target PR")
    head = snapshot.get("head_sha")
    if type(head) is not str or not SHA.fullmatch(head):
        raise ValueError("Exact PR head required")
    # A failed or absent CI can still be investigated via a work order,
    # but NEVER declare it verified or permit feature promotion.
    if snapshot.get("decision") != "RECONCILED":
        return {"decision": "STOP", "reason": "unreconciled-pr-state",
                "repository": repository, "pr_number": pr_number,
                "approval_granted": False}
    return {
        "schema_version": "1.0",
        "decision": "PREPARED_NOT_DISPATCHED",
        "repository": repository,
        "pr_number": pr_number,
        "expected_head_sha": head,
        "task": task.strip(),
        "acceptance": [x.strip() for x in acceptance],
        "method": method,
        "ci_status_at_admission": snapshot.get("ci_status"),
        "source": "live-github-read-only-snapshot",
        "required_agent_actions": [
            "read repository AGENTS.md and the actual current PR",
            "compare actual PR HEAD against expected_head_sha; STOP on drift",
            "inspect nearby implementation and existing tests before changing code",
            "implement only the bounded approved scope in the existing draft branch",
            "add positive and negative regressions",
            "verify exact-final-HEAD CI and job logs; STOP if jobs never execute",
            "record tested SHA, workflow URL, residual risks and reviewer requirements",
        ],
        "authority": {
            "dispatch": False, "merge": False, "deploy": False,
            "spend": False, "independent_signoff": False,
        },
        "limits": [
            "This command does not initiate Codex or any autonomous agent",
            "Remote read and CI metadata are not independent code verification",
            "CI failure requires diagnosis, not a verification success claim",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prepare read-only ADE coding-agent handoff")
    parser.add_argument("repository")
    parser.add_argument("pr", type=int)
    parser.add_argument("--task", required=True)
    parser.add_argument("--acceptance", action="append", required=True)
    parser.add_argument("--kind", default="integration")
    parser.add_argument("--risk", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        snapshot = inspect_pull_request(args.repository, args.pr)
        order = prepare_work_order(
            repository=args.repository, pr_number=args.pr, task=args.task,
            acceptance=args.acceptance, kind=args.kind, risks=args.risk,
            snapshot=snapshot)
    except (ValueError, OSError):
        order = {"decision": "STOP", "reason": "invalid-input-or-unverified-source",
                 "approval_granted": False}
    print(json.dumps(order, indent=2, sort_keys=True))
    return 0 if order["decision"] == "PREPARED_NOT_DISPATCHED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
