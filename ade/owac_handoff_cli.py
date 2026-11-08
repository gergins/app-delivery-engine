"""Offline consumer CLI for a Registry method-selection output.

No GitHub fetch, remote execution, authentication, or permission grant.
Provided Registry JSON is untrusted until independently authenticated.
"""
import argparse
import json
from pathlib import Path

from ade.owac_method import OWAC_ID, EXPECTED_REPO, recommend_owac


def compose_selection(*, selection, record, source_commit, kind, risks=()):
    """Reject unmatched or malformed selection; preserve ADE stop gates."""
    if type(record) is not dict:
        raise ValueError("Method record must be an object")
    if type(selection) is not dict or selection.get("selection_engine") != "deterministic-phrase-matching-v1":
        raise ValueError("Unsupported selection output")
    methods = selection.get("methods")
    if type(methods) is not list:
        raise ValueError("Selection methods must be a list")
    matches = [m for m in methods if type(m) is dict and m.get("id") == OWAC_ID]
    if len(matches) != 1 or selection.get("unmatched") is not False:
        raise ValueError("Exactly one selected OWAC method is required")
    matched = matches[0]
    if (matched.get("version") != "1.0.0" or matched.get("status") != "proposed"
        or matched.get("does_not_authorize_execution") is not True
        or matched.get("source_url") != record.get("provenance", {}).get("canonical_contract_url")
        or type(matched.get("matched_phrases")) is not list
        or not matched["matched_phrases"]):
        raise ValueError("Selected method does not match the validated record")
    return recommend_owac(method_record=record, selected_method_id=OWAC_ID,
                          source_repo=EXPECTED_REPO, source_commit=source_commit,
                          kind=kind, risks=risks)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only Registry OWAC -> ADE controls")
    parser.add_argument("--selection", type=Path, required=True,
                        help="Registry method-select JSON output (independently verified)")
    parser.add_argument("--method-record", type=Path, required=True,
                        help="Registry OWAC method record (independently verified)")
    parser.add_argument("--source-commit", required=True,
                        help="Exact immutable 40-character Registry source revision")
    parser.add_argument("--kind", required=True,
                        help="Existing ADE engineering task kind, e.g. new-slice")
    parser.add_argument("--risk", action="append", default=[],
                        help="Explicit ADE risk flag; repeat for multiple risks")
    args = parser.parse_args(argv)
    try:
        record = json.loads(args.method_record.read_text(encoding="utf-8"))
        selection = json.loads(args.selection.read_text(encoding="utf-8"))
        result = compose_selection(selection=selection, record=record,
                                   source_commit=args.source_commit,
                                   kind=args.kind, risks=args.risk)
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
