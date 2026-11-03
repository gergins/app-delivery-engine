# From minimal generator to useful delivery tool — guiding principles and milestones

**Decision:** Validate ease of use and delivery of an actual working application **before** investing in templates, dashboards or intelligent orchestration. Existing `web-list` generates a functioning local HTTP/UI/SQLite list app with Chromium checks, while `bootstrap` generates requirements and safety/continuity files. **These are two different paths today.** Benchmark the existing usable app first, then connect their strongest mechanisms through one small opt-in workflow. Do not claim they are already unified.

## Guiding principles

1. **Working user outcome is the north star.** A plausible codebase is not a delivered application. Every milestone produces something a person can run, use, evaluate or confidently reject.
2. **Prefer fewer steps and concepts.** One documented command to create, one to run, one to test, one to inspect current status. Avoid requiring the user to understand the Engine's internals.
3. **Make failures legible.** Clear validation, environment prerequisites, error exits, local/remote evidence boundary and safe recovery instruction. Never emit false-ready status.
4. **Choose methods proportionate to risk.** Offline task list needs no Keycloak or PostgreSQL; multi-tenant booking and VRS have identity, concurrency, accessibility and operational gates.
5. **Separate product from delivery infrastructure.** Each app has its own repo, interfaces and dependencies; Engine owns reusable method, startup, verification and handoff.
6. **Evidence before intelligence.** Verify real browser actions and saved data, exact source/CI, negative cases, and whether a different developer can resume.
7. **Single source of truth.** GitHub holds code/PR/reviews/CI; local metadata is a cached planning and continuity view, not approval evidence.
8. **Default to read-only/low-risk.** Inspect and preview before changing; no overwrite, silent repository creation, spending, real secrets, public deployment or merge.
9. **Extract only demonstrated reuse.** Compare two distinct applications and maintain a counterexample before raising a capability from candidate to adopted.
10. **Minimize lifetime cost, not just code volume.** Measure onboarding, rework, CI duration, bugs, dependency maintenance, accessibility and operational burden.
11. **Human authority stays explicit.** A valid test or model recommendation does not authorize sensitive actions; separate author and reviewer where needed.
12. **Continuity is a feature.** New conversation, Work, Codex or human should discover current stage, risks, exact SHA, blocker and one next permissible action.

## Product delivery sequence and readiness gates

| Milestone | Deliverable | Exit/readiness test |
| --- | --- | --- |
| D0 — inspect baseline | Existing generator, CLI, working app profile, tests, usability baseline | Confirm what really runs, identify current UX friction and limitations |
| D1 — prove one useful app | Generate existing `web-list`, run its HTTP server, add/list/update where supported, persist, restart, real-browser test | Actual user journey works with no manual code repair, source/CI evidence captured |
| D2 — simplify first run | One minimal command or guided CLI: `new → test → run → status`, README quick start, clear errors | Independent user/agent can complete without reading Engine source |
| D3 — unify continuity | Merge requirements-first bootstrap with generated working-app *option*, retain safety gates and acceptance | One project has proper AGENTS/requirements/state and an actually runnable app; no false approval |
| D4 — GitHub handoff | Approved repository creation adapter + exact SHA/CI checks + state reconciliation | Work/Codex resumes from GitHub without duplicate PR, missing evidence or wrong next step |
| D5 — lifecycle quality | Requirements→tests tracing, a11y/security/privacy risk checks, migration and recovery as applicable | All relevant checks pass; blocked critical dimensions never averaged away |
| D6 — release-ready candidate | Versioned artifact, license/SBOM, run instructions, restore/rollback and reviewed risk ledger | Independently inspected **undeployed** candidate meets product-specific release gates |
| D7 — optional interfaces | Read-only dashboard, IDE/agent interface or workflow automations | Proven reduction in confusion/rework without duplicate status implementation |
| D8 — controlled automation | Trusted worker identity, policy, budgets, idempotency, cancellation/recovery | Security and operations independently reviewed; explicit action approvals still enforced |

**Status on 2026-11-03:** D0 has inspectable code and CI; D1 has an automatically tested browser/HTTP/SQLite **web-list benchmark**, but usability with a fresh human/agent is not yet measured; D2–D8 not claimed complete. Bootstrap M1 is a *requirements-only starter*, not yet the integrated working app.

## Ease-of-use benchmark (small and falsifiable)

Use a fresh checkout/CI runner and **an unfamiliar second agent or human**. Give only the README and a brief (“I want a local task list”). Measure:

- **Time to first useful browser action:** elapsed time from checkout to creating a saved item and seeing it after restart. Record actual time; don't invent a target from one run.
- **Commands and manual edits required:** count invocations, package installs, files edited, prompts/decisions, errors encountered and unexplained concepts.
- **Functional success:** create/list/persist/restart, edit/delete only if supported; test negative invalid entries and browser accessibility basics. Don't present unsupported actions as shipped.
- **Continuity:** at a random interruption, new Work/Codex/human reads GitHub, correctly reports active milestone, limitations, next action, and approval gates.
- **Evidence accuracy:** exact generated version and source commit; CI URL and browser tests; no “production-ready” claim.
- **Maintainability:** code size, dependency count, test fragility/flakiness, runbook coverage and why any template addition is necessary.
- **Accessibility/usability:** keyboard-only path, labels, focus, screen readers where possible, narrow viewport and clear error states.

Store the benchmark result with numeric observations, blockers and one next change in the registry. A single synthetic CI pass proves technical function, not independent human usability.

## First measurable case — existing web-list

Generate via `python -m ade examples/web-list.json <new-empty-directory>`. The existing Engine CI generates a functional local web-list application, verifies HTTP and persistent SQLite behavior, and exercises the browser with Chromium. **Inspect its actual user-facing commands and actions before announcing specific CRUD operations.** Capture an onboarding transcript and fresh agent experience next. Avoid changing frameworks until the test proves a friction point.

## Automated first-run evidence — bounded technical result

New `tests/test_first_run_benchmark.py` verifies the existing `web-list` profile in a fresh temporary directory: generate, start a real Python HTTP process, save through API, stop/start the server, read the original item from SQLite, and confirm **zero generated Python/HTML/JS edits**. This is an automated synthetic onboarding surrogate, **not an actual unfamiliar human or independent agent usability assessment**.

The initial GitHub CI observation at `1974759d92345a714f67835d7d398022e47269e1` was **0.242 s measured inside the CI test** for generation plus two server starts, save and persistence; **9 files generated, 2 server starts, zero source edits**, and pass. This is an observed benchmark datapoint, not a guaranteed user timing, a whole setup/installation time or an independently validated UX score. Exact source logs: https://github.com/gergins/app-delivery-engine/actions/runs/41699536583 . Repeat on final HEAD and across fresh human/agent sessions before setting thresholds.

## Suggested first simplification (if benchmark exposes friction)

Provide a concise task-oriented CLI:
```text
ade new <brief> --preview
ade new <brief> --output <path>        # local, explicit and non-overwriting
ade test <path>                         # only known safe tests
ade run <path>                          # local development only
ade status <path>                       # local preflight plus remote evidence if accessible
```
These commands are **proposed**, not currently implemented. Add one at a time with tests and a truthfully updated `registry/commands.json`. Internally route all interfaces through one validation, permission, execution and evidence contract.

## Decision rules: stop, continue, simplify, automate

- **STOP** if essential scope, safety, migration, credential ownership or approval gate is missing.
- **CONTINUE** when a bounded next action is accepted, source/current HEAD verified, and the test environment is safe.
- **SIMPLIFY** when a second user/agent repeats a confusing step or tool that could be a documented command.
- **AUTOMATE** only after recurrence, measured time saved and negative/failure cases justify a common mechanism.
- **DEFER** dashboard, provider adapters, LLM planner, large admin templates or autonomous workers until the existing one-app delivery path is straightforward and repeatable.

## Current risk-based application comparison

Camping Booking: multi-tenant booking, OIDC, PostgreSQL migration, concurrency and recovery require stricter staged gates. Life Services Hub: offline personal-task demo validates a lightweight path. The Engine should **reuse the delivery decisions and evidence standards**, not copy their runtime architectures.

## Next implementation candidate

Conduct a fresh second-agent first-run benchmark against `web-list` before adding a new template. If onboarding friction is reproducible, implement the smallest `ade new/test/run/status` improvement in the existing draft PR, verify exact HEAD, then repeat. A portfolio dashboard is only justified after statuses are trustworthy and measurable users struggle to see them from existing GitHub/CLI views.
