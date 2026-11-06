# App Delivery Engine

A clean-sheet, evidence-led application delivery system.

**Status:** early-stage delivery Engine, with implementation on draft review branches. The default branch does not necessarily contain the draft's working-app and continuity code. Always inspect the active PR and its exact-HEAD CI before claiming a capability is verified. No merge or deployment is implied.

**Navigate:** [Documentation index and capability gap map](docs/INDEX.md) · [Interruption recovery and next work](docs/CONTINUITY-NEXT-WORK-V1.md) · [Registered executable operations](registry/commands.json).

## Principles
- Reuse proven open-source mechanisms before inventing custom infrastructure.
- Start with a minimal runnable vertical slice.
- Keep every product in its own repository.
- Validate specifications and use deterministic, fail-closed generation.
- Use GitHub-native checks, immutable commit evidence, and explicit review.
- Never deploy, merge, or use production credentials automatically.
- Extract generalizable lessons only after evidence and license review.

## Development
See the first milestone branch and draft PR for the generator, tests and delivery workflow.

## M8: Build a real local application through ADE

Start the **App Builder** from the Engine repository:

```powershell
cd C:\ade-engine
git switch feat/registry-advisory-bridge-20261106
git pull --ff-only
python -m ade.control_center
```

Open **http://127.0.0.1:8766/** and use the **App Builder** panel.
Enter a project name, a simple idea and a new folder slug. Click
**Review engineering plan**, inspect its limitations, check the explicit
local-creation approval, then click **Create and test project**.

ADE creates a separate project under your Windows user profile in
`ADE-Projects/<slug>` (on Windows normally
`C:\Users\<your-user>\ADE-Projects\<slug>`). It generates actual
UI/API/SQLite code, requirements and continuity files, then runs the
generated application's API smoke tests. The dashboard prints the
PowerShell command to start the created application locally on port 8000.

This first builder supports **only a generic single-user offline list**
and does **not** turn an arbitrary idea into a fully functioning
domain-specific product. Any other business logic, authentication,
payments, booking, video calls or deployment requires a separate reviewed
engineering milestone. This is deliberately not an LLM coding agent.
No project is created on plan; creation requires confirmation of an
unchanged plan and refuses to overwrite an existing directory.

Created projects are persistent local files, separate from ADE itself.
The Control Center remains a versioned ADE tool; update it with Git.
The M8 workflow is in a draft PR pending review, not merged or deployed.

## ADE Engineering Control Center (actual Engine interface)

The local read-only control center is the **ADE interface**, unlike the generated
items-list demo. It displays the real command catalog and can inspect a chosen
GitHub pull request and exact-HEAD CI using ADE's existing read-only connector.

From the ADE repository root:

```powershell
python -m ade.control_center
```

Open **http://127.0.0.1:8766**. Press Ctrl+C to stop. The dashboard listens
only on localhost, performs no background polling, and does not run code,
automatically merge, deploy, spend, or grant approvals. Private repository
inspection requires an explicitly configured read-only `GITHUB_TOKEN` environment
variable; never put credentials in the browser or the Git repository.
Unknown/missing CI evidence results in STOP, not a green status.

**Persistence:** ADE source code is versioned in GitHub and remains executable
in each local checkout. Pull reviewed changes to update the installed code;
the dashboard is not a one-time generated artifact or an automatically installed
Windows service. Generated apps remain separate directories with their own
data. This is a minimal M7 control interface, not full autonomous delivery.

## Execute ADE in one command (local demonstration)

From this draft branch with Python 3.11 or newer, use a new destination directory:

```powershell
python -m ade.demo .\my-ade-demo --serve
```

This generates a **generic offline list app** with its product handoff, runs its
API smoke tests, then serves a local UI at **http://127.0.0.1:8000**. It stores
SQLite data in the generated directory. Stop with Ctrl+C. To start again
without overwriting the project:

```powershell
cd .\my-ade-demo
python -m app.server
```

Run `python -m ade.demo .\my-ade-demo` without `--serve` to generate and verify
without starting a server. The destination **must not already exist** and its
parent must exist. No account, token, Docker, cloud provider or Registry access
is needed for this demo. This is not a working VRS or camping booking product;
product approval and remote CI review remain separate.

For Registry-assisted engineering planning, use
`python -m ade.registry_bridge --help` with a separately verified private
Registry snapshot. The local starter can run independently of the Registry.

## Quick start: working web-list application (local only)

This is the **runnable** path. It is distinct from the requirements-only bootstrap below. From an Engine checkout with Python 3.11:

```bash
python -m ade examples/web-list.json /tmp/my-first-list
cd /tmp/my-first-list
python -m unittest discover -s tests -p test_app.py -v
python -m app.server
```

Open **http://127.0.0.1:8000** in a browser. Create an item, then stop the server with Ctrl+C, run `python -m app.server` again from the same generated directory, and check that the saved item remains. Do not delete that directory between starts: it contains the local SQLite data. Choose a different **new, nonexistent** output directory if `/tmp/my-first-list` already exists; generation intentionally refuses overwrite. On Windows PowerShell use a suitable local path such as `my-first-list` instead of `/tmp/my-first-list`.

**Verify the complete path:** the Engine's GitHub Actions workflow also exercises Chromium browser interactions and SQLite persistence on disposable data. This is a development demonstration, not a hosted service, production-ready application, or independently measured onboarding. The new app is not automatically placed in its own GitHub repository. Read [Delivery Usability Milestones](docs/DELIVERY-USABILITY-MILESTONES-V1.md) for what remains unproven.

## Method-selection v1 (advisory)

Read [AGENTS.md](AGENTS.md) and [delivery method selection](docs/METHOD-SELECTION-V1.md) before using Work, Codex or another assistant to modify a product. `ade.method_selection.select_method(kind, risks)` composes the existing minimum delivery practice with task- and risk-specific verification controls and universal stop gates; no autonomous release or risk classification is claimed. Existing GitHub workflows and PR approvals remain the enforcement source. See the draft PR's exact-HEAD CI evidence before adoption.

## Application lifecycle benchmark (idea to release-ready)

[Application Lifecycle Benchmark v1](docs/APP-LIFECYCLE-BENCHMARK-V1.md) covers ideation, validation, requirements, architecture, implementation, tests, independent review, release candidacy, deployment decision and operations. It inventories repository failure/recovery/handoff scenarios and defines evidence gates for benchmarking two different apps. **This is a benchmark plan, not a completed autonomous production delivery engine.** Read [Senior Engineering Operating Contract](docs/SENIOR-ENGINEERING-CONTRACT-V1.md) for the decision and oversight style expected from Work/Codex.

## Application Bootstrap & Continuity (M1 — offline benchmark)

The Engine can generate a **requirements-first independent application repository starter**, including `AGENTS.md`, `project.yaml`, `delivery/current-state.yaml`, requirements, proposed ADR, risk register, acceptance plan, evidence/approvals, generated GitHub CI, and `tools/startup.py` for read-only agent entry checks.

```bash
python -m ade.bootstrap_cli plan examples/vrs-bootstrap.json
python -m ade.bootstrap_cli create examples/vrs-bootstrap.json /tmp/my-vrs-starter
cd /tmp/my-vrs-starter
python tools/startup.py     # Expected STOP (2): scope is unapproved
python -m unittest discover -s tests -v
```

This builds no actual VRS signaling/media/telecom application, creates no GitHub repository, makes no network calls, and cannot grant permissions. It preserves the *decision and handoff contract*, not agent autonomy. See [Bootstrap & Continuity M1](docs/BOOTSTRAP-CONTINUITY-M1.md).

**Ownership doctrine:** [Benchmark-to-Ownership Policy](docs/BENCHMARK-TO-OWNERSHIP-POLICY.md). Initial `registry/benchmarks.json`, `registry/capabilities.json` and `registry/lessons.json` contain provenance and explicit limitations. Remain dependent on mature external protocols and tools where replacing them brings no verified value; the Engine owns the process and contracts, not every implementation.

## Make delivery genuinely easy

[Guiding principles, delivery sequence and readiness criteria](docs/DELIVERY-USABILITY-MILESTONES-V1.md): benchmark the existing generated `web-list` app's first-run user experience, tests, SQLite persistence and browser journey. Measure commands, time, manual edits and handoff drift before introducing extra templates, dashboards or AI orchestrators. The working-app generator and requirements-only bootstrap are currently **separate capabilities**. Both are useful; the next evidenced design must reconcile them without pretending the product is release-ready.

## Resume after an interruption

Read [the recovery protocol](docs/CONTINUITY-NEXT-WORK-V1.md) and inspect the **live** GitHub PR HEAD, exact-HEAD workflow runs, review state, blockers and committed decisions. The pure `ade.github_reconcile.reconcile_github_snapshot` and `ade.continuity.recommend_next_work` helpers operate on caller-supplied objects; they do **not** fetch GitHub, authenticate evidence, change source files, or authorize actions. If the remote facts are unavailable or stale, stop and investigate instead of assuming success. The full verified delivery chain and explicit add-versus-defer criteria are in [docs/INDEX.md](docs/INDEX.md).

## One project with both handoff documents and a working local demonstration

For a reviewed **low-risk general/offline-tasks** brief, use the explicit opt-in working profile:

```bash
python -m ade.bootstrap_cli plan examples/offline-list-brief.json --working-web-list
python -m ade.bootstrap_cli create examples/offline-list-brief.json /tmp/my-project --working-web-list
cd /tmp/my-project
python -m unittest discover -s tests -p test_app.py -v
python tools/startup.py     # Expected STOP until the product scope is approved
python -m app.server        # Runs ONLY the local generic list demo
```

Open http://127.0.0.1:8000. Chromium browser regressions are installed and run in the generated project's GitHub CI, not required for the dependency-free local API smoke test. The `AGENTS.md`, requirements, decisions, risks and continuity files coexist with the runnable UI/API/SQLite demonstration. A STOP from startup is a **correct approval outcome** and does not block manual inspection of the local demonstration. The profile must not be used to pretend VRS, payments, multi-tenant booking or other high-risk domain logic is implemented. The existing default bootstrap remains requirements-only. A fresh-human usability benchmark and authorized live cross-repo recovery test remain incomplete.
