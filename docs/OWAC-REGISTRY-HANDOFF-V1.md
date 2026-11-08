# OWAC reusable method handoff — proposal

**Status:** Read-only candidate on a stacked draft branch. This is not an installed application-building agent and does not authorize execution or release.

## Existing responsibilities remain separate

- **Engineering Knowledge Registry** discovers reusable approaches. Method record `method-outcome-to-working-app-v1` identifies OWAC and links its versioned canonical contract.
- **App Delivery Engine** retains local engineering authority and risk controls through `ade.method_selection.select_method`, its existing senior engineering contract and its existing application delivery workflows.
- **OWAC contract** defines the expected user outcome: a genuinely running, accessible, browser-tested application with exact-revision evidence, or a clearly reported blocker.

## How to consume a registry recommendation

1. Independently retrieve and verify the private registry method record at an exact commit. A commit SHA supplied by a caller is an identifier, not authentication.
2. Confirm `id=method-outcome-to-working-app-v1`, `kind=methods`, `version=1.0.0`, `status=proposed`, provenance and existing stop gates.
3. If the user is actually requesting app delivery, call `ade.owac_method.recommend_owac` with the verified record, the selected method ID, the source repo/SHA, and **explicit** ADE task kind and risk flags.
4. Compose the returned advisory suggestion with the existing project-specific operating contract. The Engine's own controls stay authoritative; an unknown risk must fail closed.
5. Deliver only within separately authorized scope. The recommendation cannot build an application, authenticate source, approve production, merge, deploy, spend money, or replace browser validation.

Example (synthetic, not a live fetched Registry record):

```python
from ade.owac_method import recommend_owac

proposal = recommend_owac(
    method_record=verified_method_record,  # caller must obtain and verify
    selected_method_id="method-outcome-to-working-app-v1",
    source_repo="gergins/engineering-knowledge-registry",
    source_commit=verified_exact_commit_sha,  # immutable, independently checked
    kind="new-slice",
    risks=("concurrency",),
)
assert proposal["approval_granted"] is False
assert proposal["execution_authorized"] is False
```

## Verification contract

Run at the **exact candidate branch HEAD**:

```sh
python -m unittest tests.test_owac_method -v
python -m unittest discover -s tests -v
```

Inspect completed GitHub Actions and negative permission tests separately. Local test results are not CI or independent approval. Browser preview, actual application acceptance, and end-to-end registry snapshot fetching are **not implemented in this adapter**.

## Reuse pointers

- Canonical OWAC operating contract: https://github.com/gergins/app-delivery-engine/pull/8
- Registered method: https://github.com/gergins/engineering-knowledge-registry/pull/6
- Registry method selector: https://github.com/gergins/engineering-knowledge-registry/pull/7
- Existing ADE selector: `ade/method_selection.py`
- Existing ADE capability bridge: `ade/registry_bridge.py`

Keep this as one narrow adapter. Do not duplicate the registry's selector or the Engine's task/risk controls.
