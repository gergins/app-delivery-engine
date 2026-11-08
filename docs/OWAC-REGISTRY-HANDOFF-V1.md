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

## Executable offline selector-to-ADE handoff

The existing Registry's `python engine/registry.py method-select "Build an app"` prints a JSON suggestion. After the caller has separately verified a private Registry checkout and immutable source revision, write that output to a local JSON file (do **not** paste credentials). Then compose it with ADE's existing task/risk controls:

```sh
python -m ade.owac_handoff_cli \
  --selection /safe/local/selection.json \
  --method-record /safe/verified-registry/registry/methods/owac-v1.json \
  --source-commit FULL_40_CHARACTER_VERIFIED_REGISTRY_SHA \
  --kind new-slice --risk concurrency
```

Replace placeholders with actual authenticated local paths and commit. The CLI deliberately does not contact GitHub, check external authority, provision a Codespace or run the app. It rejects missing/unmatched/mismatched method recommendations, invalid revisions, unsupported kinds/risks and weakened governance. All successful outputs remain `advisory-only` and `execution_authorized: false`.

Run `python -m unittest tests.test_owac_handoff_cli -v` and the full repository suite. Exact-HEAD GitHub Actions and review must be checked before any adoption. For the first product proof, prefer the existing `gergins/camping-booking` feature branches: do not create a second booking application or expose the private preview. Its latest checked private preview revision has no demonstrated real GitHub OAuth login or user-visible browser acceptance; distinguish fake-provider browser tests from real identity and human usability.

