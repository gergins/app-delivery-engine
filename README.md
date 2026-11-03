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

## Method-selection v1 (advisory)

Read [AGENTS.md](AGENTS.md) and [delivery method selection](docs/METHOD-SELECTION-V1.md) before using Work, Codex or another assistant to modify a product. `ade.method_selection.select_method(kind, risks)` composes the existing minimum delivery practice with task- and risk-specific verification controls and universal stop gates; no autonomous release or risk classification is claimed. Existing GitHub workflows and PR approvals remain the enforcement source. See the draft PR's exact-HEAD CI evidence before adoption.
