# Registry → ADE read-only integration trial

**State:** Proposed integration, draft only. No deploy, merge, source authentication or approval grant.

## Boundary

The Engineering Knowledge Registry is private; ADE is public. Do **not** commit
private registry contents, credentials or temporary download URLs into ADE.
The bridge accepts an externally supplied JSON snapshot with the Registry's
existing `registry/capabilities.json` record schema. It does not contact GitHub.
The source repository and **full immutable commit SHA** are required as metadata,
but this does not authenticate the bytes. The operator must verify the snapshot
against the named commit through their authorized GitHub access.

The bridge reuses ADE's existing `select_method`; it does not duplicate
the Registry's planner, implement security approvals or change method policy.
Unknown dependencies, malformed records, duplicate IDs, cycles, missing
provenance evidence for source-verified claims, and unknown risk flags fail closed.
Validated capabilities remain *proposals*, not implemented features.

## Disposable test (public/synthetic)

```sh
python -m unittest tests.test_registry_bridge -v
python -m unittest discover -s tests -v
```

## Authorized cross-repository trial (not CI-authorized yet)

1. Independently obtain `registry/capabilities.json` from
   `gergins/engineering-knowledge-registry` at a full pinned SHA through an
   authorized GitHub connector; verify the actual blob and revision.
2. Keep the snapshot outside the ADE repository and outside public logs.
3. Run:

```sh
python -m ade.registry_bridge /secure/path/capabilities.json \
  /secure/path/camping-brief.json \
  --source-commit FULL_VERIFIED_40_CHARACTER_SHA \
  --kind integration --risk concurrency
```

4. Compare selected capabilities and method controls with manual Registry
   analysis. Test missing dependency, stale source, bad schema and cycle cases.
5. Reconcile ADE exact-HEAD CI and perform independent review before adopting
   this interface. Neither a green test nor a manually supplied SHA means
   the private Registry bytes were authenticated.

## Acceptance

- Public CI verifies the *synthetic consumer contract* at the exact ADE HEAD.
- An authorized private-source trial independently checks snapshot provenance,
  validates current Registry semantics and reports consumer compatibility.
- Approval, release and any CI credentials remain separately controlled.
