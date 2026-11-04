"""Advisory learning loop over externally verified delivery observations.

No model training, automatic code edits, GitHub calls or approval authority.
Caller must establish that observations are real, current, non-sensitive and
independent. This is a conservative cross-application promotion *candidate*.
"""
from collections import defaultdict
import re

SHA = re.compile(r"^[0-9a-f]{40}$")
KINDS = frozenset({"reliability", "accessibility", "security", "efficiency",
                   "usability", "maintainability", "recovery"})
DECISIONS = frozenset({"propose", "defer", "stop"})


def recommend_learning(observations):
    """Return bounded, deterministic candidates; never implement suggestions.

    Evidence is caller-verified, and all fields are required. Repeated samples
    from one repository count as a single application for cross-app promotion.
    Savings or improved quality are not claimed without before/after evidence.
    """
    if type(observations) is not list:
        raise ValueError("Observations must be a list")
    by_key = defaultdict(list)
    ids = set()
    for item in observations:
        if type(item) is not dict or set(item) != {
                "id", "repository", "commit_sha", "evidence_url",
                "category", "mechanism", "finding", "verified", "outcome"}:
            raise ValueError("Invalid observation schema")
        if (any(type(item[k]) is not str or not item[k].strip() for k in (
                "id", "repository", "commit_sha", "evidence_url", "category",
                "mechanism", "finding", "outcome"))
                or item["id"] in ids
                or not SHA.fullmatch(item["commit_sha"])
                or item["category"] not in KINDS
                or item["outcome"] not in ("failure", "success", "unknown")
                or type(item["verified"]) is not bool
                or "/" not in item["repository"]
                or not item["evidence_url"].startswith("https://github.com/")):
            raise ValueError("Invalid observation fields")
        ids.add(item["id"])
        if item["verified"] and item["outcome"] != "unknown":
            by_key[(item["category"], item["mechanism"])].append(item)
    output = []
    for (category, mechanism), items in sorted(by_key.items()):
        repositories = sorted({x["repository"] for x in items})
        # Repetition within a single app is useful but not proof of
        # generalization. No promotion directly from a single app.
        cross_app = len(repositories) >= 2
        output.append({
            "category": category, "mechanism": mechanism,
            "evidence_ids": sorted(x["id"] for x in items),
            "repositories": repositories,
            "decision": "propose" if cross_app else "defer",
            "reason": "cross-app-observations-require-controlled-trial"
                      if cross_app else "single-app-evidence-insufficient",
            "next_action": "Compare against baseline and negative counterexamples; seek review"
                           if cross_app else "Observe a genuinely distinct app before promotion",
            "may_modify_pipeline": False,
            "may_reduce_required_tests": False,
            "status": "advisory-only",
        })
    return {"schema_version": "1.0", "proposals": output,
            "unverified_observations_ignored": sum(
                not x["verified"] or x["outcome"] == "unknown"
                for x in observations)}
