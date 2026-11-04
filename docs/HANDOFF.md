# Continuity and collaborator handoff

Repository: gergins/app-delivery-engine
Milestone: M0 offline generator and CI baseline
Default branch: main
Working branch: feat/m0-minimal-app-delivery

## Start here
1. Read README.md and docs/ARCHITECTURE.md.
2. Inspect open PRs and current branch before changing anything.
3. Run `python -m unittest discover -s tests -v`.
4. Generate: `python -m ade examples/demo.json /tmp/demo-app` (destination must not exist).
5. Run generated tests in that destination.
6. Record the exact commit SHA, test output, open gaps, and next bounded task.

## Safety and coordination
One accountable work owner; avoid overlapping file edits. Do not merge or deploy without approval. Do not infer CI passed merely because a workflow exists. Never store secrets in repository files. Open-source reuse requires source, version, license and test evidence.

## Current limitations
Only standard-library Python offline scaffolding. No live application delivery, remote execution, or production security guarantees. This handoff is updated with each milestone.
