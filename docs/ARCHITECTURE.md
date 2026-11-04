# Milestone 0: minimum viable application delivery

The system is independent of previous Factories. It owns no application runtime.

## Boundaries
- **Specification:** strictly validated JSON, version 1.0.
- **Planner:** deterministic, read-only file plan.
- **Generator:** offline and fail-closed. Existing destinations are never overwritten.
- **Product:** generated files belong to each independent application repository.
- **Delivery:** GitHub Actions builds and tests against the candidate commit.
- **Approval:** merges, deployments, credentials, and public release require separate authorization.

## Source-learning policy
Research open-source implementations by exact version and provenance; record license, alternative options, failure modes and an executable acceptance test before adopting a mechanism. Do not copy third-party code into generated apps without a licensing review.

## Scope exclusions
No agent autonomy, external repository provisioning, arbitrary shell commands, production-grade authentication, deployment, database, or networking. A generated demo is not a production application.

## Next acceptance benchmark
An independently owned application repo must show a real user journey with UI/API/data as appropriate, negative tests, accessibility checks, and exact-head evidence. Add adapters only in response to demonstrated need.
