# M0–M2 focused delivery and reusability audit (2026-11-03)

## Scope and evidence
Examined the source on draft PR #1 in `gergins/app-delivery-engine`, its generator, opt-in web-list profile, tests and GitHub workflow. Baseline M2 SHA `b17eaa02c55bc0bbdce322ffcf1373bfd093f16b` had successful CI run 41629788962: 12 engine tests, 2 legacy generated tests, 2 generated HTTP/SQLite tests and 1 Chromium UI-to-API-to-SQLite/reload test. Separate independent application benchmark is in `gergins/community-picks-delivery-benchmark` draft PR #1 (SHA `c939b43e89be15e3d904f92803690b8799966444`, successful run 41629084098).

## Decision
**Reusable for multiple instances of one application category (local web-list) and one initial echo scaffold only.** It is not an arbitrary application generator, a deployment engine, or a production-ready platform. No new orchestrator, framework or capability registry is justified. Existing M1 product code stays in its independent repository.

## Findings
1. **Functional reusability**: M2 profile is deterministic and driven by a validated schema. New regression checks generate two distinct, isolated application directories and manifests; generation refuses to overwrite destinations. Keep this as an explicit capability boundary.
2. **Potential complexity growth**: web-list profile has embedded server, HTML, JavaScript and tests in a single template module. For the two supported profiles this is acceptable; split into separate versioned template assets only if ongoing modifications or multiple profiles show demonstrated maintenance problems.
3. **Coverage**: Existing HTTP/SQLite/browser flow tests pass. The extra two-app test broadens proof of isolation but does not establish general app compatibility. Add more app types only after an actual independent requirement.
4. **CI provenance**: Existing workflow runs read-only, checks exact source SHA and uses `persist-credentials: false`. However the actions use floating major tags `actions/checkout@v4`, `actions/setup-python@v5`; pin reviewed action commit SHAs and assess supported Node runtime as a separate minimal CI hardening step before treating the pipeline as a production trust boundary.
5. **Production security**: local-only binding avoids remote exposure under ordinary use, but there is no auth, production CSRF/rate-limit policy, schema migration/backup process or independent security audit. No external deployment permitted based on these tests.
6. **UI/accessibility**: semantic labels, live status and keyboard focus styles are present. Automated browser success does **not** replace keyboard/screen-reader testing or independent accessibility assessment.
7. **Failure behavior**: destination overwrite prevention and invalid-input tests exist. Interrupt/power-loss durability, symlink races, concurrent builds and trusted remote worker identity are not proven. Keep generator offline; never claim safe autonomous remote execution.
8. **Delivery throughput**: M1 was manually assembled and uploaded; M2 can generate a working local application from a spec. No automatic creation of app repositories, dependency-driven delivery planning or cross-app upgrades have been demonstrated.

## Priority
- **P0 now**: keep branch draft, verify new multi-app regression at exact HEAD, record evidence. No additional architecture.
- **P1 before production delivery**: reviewed immutable CI action pins, appropriate independent security/accessibility reviews, protected merge controls and isolation tests if remote execution is introduced.
- **P2 on demonstrated demand**: broader data models, additional app profiles, repository provisioning, template asset refactor, operational metrics.

## Stop criterion
For M2, a passing exact-HEAD CI run with both original and web-list tests, two-app isolation tests, browser persistence test, and accurately documented limitations is sufficient. Stop expanding and seek separate approval before merge or deploy.

## CI hardening follow-up (2026-11-03)

Replaced floating action references in the existing `.github/workflows/verify.yml` without changing its test stages or permissions.

- `actions/checkout@v7.0.1` resolved using the official GitHub tag to commit `3d3c42e5aac5ba805825da76410c181273ba90b1`.
- `actions/setup-python@v7.1.0` resolved using the official GitHub tag to commit `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`.
- Inspected both release `action.yml` files: both declare `runs.using: node24`.
- Official release tags/references from the GitHub Actions repositories were read directly. Full independent supply-chain audit of those upstream source commits is **not claimed**.
- Workflow still has read-only `contents: read`, disabled persistent checkout credentials, and an exact candidate HEAD assertion.
- The test run on the new SHA must be checked separately. No merge/deployment is authorized.
