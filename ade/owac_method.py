"""Read-only OWAC method handoff from an explicitly supplied Registry record.

No network calls, trust attestation, execution, or approval. The caller must
obtain and authenticate the pinned private Registry record independently.
"""
import re

from ade.method_selection import select_method

EXPECTED_REPO = "gergins/engineering-knowledge-registry"
OWAC_ID = "method-outcome-to-working-app-v1"
SHA = re.compile(r"[a-f0-9]{40}\Z")


def recommend_owac(*, method_record, selected_method_id, source_repo,
                   source_commit, kind, risks=()):
    """Compose a registry-recommended OWAC with ADE's existing risk controls.

    A supplied match is advisory, never authenticated evidence or authority.
    This does not fetch, select semantically, execute, or approve anything.
    """
    if source_repo != EXPECTED_REPO or type(source_commit) is not str or not SHA.fullmatch(source_commit):
        raise ValueError("Pinned trusted-source identity required")
    if type(method_record) is not dict or selected_method_id != OWAC_ID:
        raise ValueError("Unsupported method selection")
    if method_record.get("id") != selected_method_id or method_record.get("kind") != "methods":
        raise ValueError("Method identity and kind mismatch")
    if method_record.get("version") != "1.0.0" or method_record.get("status") != "proposed":
        raise ValueError("Unexpected method version or maturity")
    provenance = method_record.get("provenance")
    if type(provenance) is not dict or type(provenance.get("canonical_contract_url")) is not str:
        raise ValueError("Missing canonical provenance")
    url = provenance["canonical_contract_url"]
    if not url.startswith("https://github.com/gergins/app-delivery-engine/blob/"):
        raise ValueError("Unexpected contract source")
    authority = method_record.get("authority")
    if type(authority) is not dict or any(authority.get(key) is not True for key in
             ("no_automatic_merge", "no_automatic_deploy", "no_unapproved_spend")):
        raise ValueError("Method cannot weaken operating authority")
    # The existing ADE selector remains the sole source of task/risk controls.
    controls = select_method(kind, risks)
    return {
        "status": "advisory-only",
        "method": {"id": selected_method_id, "version": method_record["version"],
                   "contract_url": url, "registry_status": method_record["status"]},
        "registry_source": {"repository": source_repo, "commit": source_commit,
                            "authenticated_by_this_function": False},
        "delivery_controls": controls,
        "outcome_acceptance": "Real running user journey plus exact-revision evidence; not a code-only completion claim",
        "required_handoff": ["running_preview_or_verified_blocker", "browser_journey_evidence",
                             "exact_revision", "unresolved_risks", "approval_status"],
        "approval_granted": False,
        "execution_authorized": False,
        "limitations": ["Caller-selected method and pinned SHA are not independently authenticated",
                        "This adapter does not run a build or a browser test",
                        "User or project policy must separately authorize consequential actions"],
    }
