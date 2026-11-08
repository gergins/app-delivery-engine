# Universal Visual Workbench v0.3 — adaptive operating model

**Status:** design + offline example prototype only. Continuity is a cross-cutting capability, not a permanent mode or architecture center. Fincept is an example dataset, never a domain dependency.

## Outcome
The user can close and return to any project and immediately see the precise last working item, purpose, evidence, unfinished thinking, review state, next action and contextual navigation. No manual reconstruction from conversations, branches, screen lists or files.

## Neutral workspace core and adaptable capabilities
The workspace is organized around projects, goals, work items, artifacts, evidence, relationships, decisions, permissions and checkpoints—not Continuity, BDD, open source, application development or any one methodology. Continuity is an always-available service for resuming/recovering work, not the permanent landing view or mandatory stage. The user's preferred home can be an overview, canvas, active task, portfolio, plan or resume. Each is an optional perspective. Open-source exploration, reverse engineering, research, review, planning, requirements, behavior, design, building, verification, discovery and unknown future categories are equally eligible capabilities, enabled according to the goal.

## Adaptive method and resource selection
Methods are registered options, not hardwired pipeline stages. Examples: outcome-driven, problem-driven, research-driven, evidence-driven, requirements-driven, behavior-driven/BDD, design-driven, test-driven/TDD, model-driven, data-driven, risk-driven, capability-driven and experiment-driven. Combine or skip them proportionately. The workspace should explain why a method is recommended and let the user override it without losing source context.

Resources are also a selectable catalog: open source, internal reusable capabilities, commercial services, APIs, deterministic tools, AI, human expertise and custom building. Compare fitness, license, provenance, security, cost, maintenance, integration effort, accessibility and verification, rather than assuming open source always wins.

Use the SAME stable work item identifier in all perspectives. Navigating from evidence to capability, requirement, user journey, UI component, API, test, decision, risk, plan or opportunity must preserve the anchor and a return path. Support deep-linking to work item + artifact + anchor. Distinguish last visited place from last meaningful unfinished item.

## Universal object types
Project, SourceSnapshot, SourceFile, Evidence, Screen, Component, Element, Control, Capability, Flow, Actor, Requirement, BehaviorScenario, UIState, API, DataModel, Test, VerificationResult, Risk, Gap, Opportunity, Decision, Dependency, Plan, Task, Handoff, Checkpoint, Lesson.

Each object: stable ID, type, scoped project, evidence/provenance, lifecycle status, inferred-vs-observed-vs-verified classification, timestamp, revision, relationships, responsible authority and open questions. Relationships must be directional and typed (implements, observedIn, dependsOn, derivedFrom, verifiedBy, conflictsWith, candidateFor, supersedes, etc.). Preserve unknown and unmapped as first-class states.

## Import & extraction workflow
1. Import a repository, versioned archive, document set, screenshot or project fixture in a sandbox.
2. Inventory breadth by files, code symbols, screen registrations, API contracts, database tables, integrations, workflows, tests and metadata.
3. Create separate registers: raw extracted elements, interpreted capabilities, actual screens, actual controls, user journeys, cross-element links, hypotheses and gaps.
4. Build evidence pointers to exact source revision + file/line; annotate dynamic/runtime unknowns.
5. Present coverage: counts by object type, unmapped items, missing links, contradictions, licenses, security assumptions and runtime-untested findings.
6. Allow review and curation into approved requirements and BDD only after source confidence is differentiated.
7. Handoff a versioned graph slice plus decisions, acceptance rules, evidence, unresolved questions, blockers and recommended next action.

## Fincept sample extraction (2026-11-08)
User-provided ZIP: Fincept_Research_Extraction(2).zip.
Source: https://github.com/Fincept-Corporation/FinceptTerminal
Commit: 623c61db169ea550b4351dd6a7fb69fb608ba2cc
From extracted summary: 3,459 tracked files, 52 registered screen IDs, 23 CURATED capabilities, 13 proposed gaps, 15,053 Python symbols, 447 literal MCP names, 104 literal workflow node IDs, 111 SQL declarations, 6,851 C++ include edges.
23 capabilities point to 18 distinct screen IDs. Therefore 34 screen registrations have no DIRECT curated capability mapping. This is coverage status, not an assertion that those screens are empty or missing features.
The extraction reports 1,157 Python AST parses with 0 parse errors, but native build and UI tests NOT RUN. Neither 15,053 symbols nor 447 tool names represent independently validated user-facing capabilities.

## Key screen features
- Customizable home, with accessible resume/restore affordance showing exact item, last active perspective and editable next action; resume must be discoverable but need not dominate every screen.
- Source-backed capability register, filter, source links and static source-to-screen mapping.
- Full registered screen inventory with visible nonmapped cases.
- Graph or adjacency view for source → component → capability → requirement → behavior → UI → API/data → test → evidence; user can open any node.
- Review queue for evidence claims and unresolved gaps.
- Planning perspective with readiness gating and risk/decision visibility.
- Behavior/BDD perspective as ONE optional branch of the same graph, not a separate product.
- Provenance, lifecycle, access and real-world verification always visible.

## Recovery, trust and accessibility
Durable versioned checkpoints and conflict resolution; multi-device sync only after backend is proven. Local storage is an offline demo fallback, not durable cross-device sync. Clear visually encoded status plus text (never color alone); keyboard and screen-reader accessible; responsive mobile/tablet; signing-video-friendly layouts where applicable; visual alerts, no audio-only cues. Saved progress must not be mistaken for evidence or approval.

## MVP priorities
P0: real item import, stable IDs, user-chosen default view, accessible resume and recovery, source evidence, screen/capability mapping, unknown markers.
P1: review and planning handoffs, accessible graph, dynamic runtime capture, scenario/test traceability.
P2: source adapters, cross-device synchronization, multi-project permissions and automation.
Do not add elaborate workflow engines or proprietary graph databases just to draw links; prove a working vertical slice first.

## Example prototype (outside GitHub PR)
Created browser-only offline HTML prototype v0.2, research JSON and generic schema. Syntax and embedded data counts checked. Runtime browser usability, accessibility and end-to-end behavior remain unverified; prototype files were supplied in this conversation, not committed by this document.
