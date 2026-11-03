# App Delivery Engine

A clean-sheet, evidence-led application delivery system.

**Status:** Milestone 0 bootstrap only. All implementation work must happen on review branches, with tests and verified evidence before merge. This project is independent of earlier engineering systems.

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
