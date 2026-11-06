"""Read-only, advisory bridge for an explicitly supplied Registry snapshot.

A pinned SHA is an identifier, NOT authentication of a private GitHub source.
The caller must independently fetch and verify source provenance. No network,
remote mutations, permission decisions or executable instructions.
"""
import argparse
import json
import re
from pathlib import Path

from ade.method_selection import select_method

SHA = re.compile(r"[0-9a-f]{40}\\Z")
ID = re.compile(r"[a-z][a-z0-9-]*\\Z")
FIELDS = {"id", "name", "domain", "description", "keywords", "depends_on",
          "evidence", "source_status", "maturity"}


def assess_snapshot(*, records, source_repo, source_commit, brief, kind, risks=()):
    """Validate a Registry-shaped snapshot and return a reproducible advisory plan."""
    if source_repo != "gergins/engineering-knowledge-registry":
        raise ValueError("Unrecognized source owner")
    if type(source_commit) is not str or not SHA.fullmatch(source_commit):
        raise ValueError("An immutable 40-character source commit is required")
    if type(records) is not list or not records:
        raise ValueError("Registry records must be a nonempty list")
    by_id = {}
    for record in records:
        if type(record) is not dict or not FIELDS.issubset(record):
            raise ValueError("Missing Registry capability fields")
        key = record["id"]
        if type(key) is not str or not ID.fullmatch(key) or key in by_id:
            raise ValueError("Invalid or duplicate capability ID")
        if (any(type(record[k]) is not str or not record[k].strip()
                for k in ("name", "domain", "description", "evidence"))
                or record["source_status"] not in ("synthesized", "source-verified")
                or record["maturity"] not in ("L0", "L1", "L2", "L3", "L4", "L5", "L6")):
            raise ValueError("Invalid capability metadata")
        if (record["source_status"] == "source-verified"
                and (type(record.get("source_evidence")) is not str
                     or not record["source_evidence"].strip())):
            raise ValueError("Source verification claim lacks evidence")
        for field in ("keywords", "depends_on"):
            value = record[field]
            if (type(value) is not list or
                    any(type(x) is not str or not x.strip() for x in value) or
                    len(set(value)) != len(value)):
                raise ValueError("Malformed keywords or dependency list")
        by_id[key] = record
    for key, record in by_id.items():
        if any(dep not in by_id for dep in record["depends_on"]):
            raise ValueError("Unresolved capability dependency")
    visited, active = set(), set()

    def visit(key):
        if key in active:
            raise ValueError("Cyclic capability dependency")
        if key in visited:
            return
        active.add(key)
        for dependency in by_id[key]["depends_on"]:
            visit(dependency)
        active.remove(key)
        visited.add(key)

    for key in sorted(by_id):
        visit(key)
    if type(brief) is not dict or type(brief.get("description")) is not str or not brief["description"].strip():
        raise ValueError("Nonempty project description required")
    requirements = brief.get("requirements", [])
    if type(requirements) is not list or any(type(x) is not str for x in requirements):
        raise ValueError("Requirements must be strings")
    tokens = set(re.findall(r"[a-z0-9-]+", " ".join([brief["description"]] + requirements).lower()))
    direct = {key for key, record in by_id.items()
              if any(word.lower() in tokens for word in record["keywords"])}
    selected = set()

    def include(key):
        if key in selected:
            return
        for dependency in by_id[key]["depends_on"]:
            include(dependency)
        selected.add(key)

    for key in sorted(direct):
        include(key)
    method = select_method(kind, risks)
    return {
        "status": "advisory-only",
        "source": {"repository": source_repo, "commit": source_commit,
                   "source_authenticated": False, "snapshot_validated": True},
        "capabilities": [
            {"id": key, "reason": "keyword" if key in direct else "dependency",
             "evidence_required": by_id[key]["evidence"],
             "source_status": by_id[key]["source_status"],
             "maturity": by_id[key]["maturity"]}
            for key in sorted(selected)],
        "unmatched": len(by_id) - len(selected),
        "method": method,
        "limitations": [
            "Caller-provided snapshot is not an authenticated GitHub fetch",
            "Keyword matching is incomplete; missing capabilities require review",
            "Capability criteria do not prove implementation or source verification",
            "No security signoff, merge, deployment or spending authority"
        ],
        "approval_granted": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only Registry to ADE advisory bridge")
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("brief", type=Path)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--kind", required=True)
    parser.add_argument("--risk", action="append", default=[])
    args = parser.parse_args(argv)
    result = assess_snapshot(
        records=json.loads(args.snapshot.read_text(encoding="utf-8")),
        source_repo="gergins/engineering-knowledge-registry",
        source_commit=args.source_commit,
        brief=json.loads(args.brief.read_text(encoding="utf-8")),
        kind=args.kind, risks=args.risk,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
