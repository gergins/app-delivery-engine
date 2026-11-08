# Universal Visual Workbench — Perspective and Capability Catalogue v0.4

Status: researched candidate register, not a claim these 60 views are implemented. 2026-11-08.

## Neutral foundation
Project, goal, item, artifact, relationship, evidence, actor/authority, state/revision, event, decision, checkpoint, handoff and policy. A *perspective* filters and renders shared objects; a *capability* performs an operation; a *method* recommends a working approach; a *resource* provides a means of execution. None is permanently privileged. BDD, continuity, open source and Fincept are optional examples.

## 60 candidate perspectives / 12 families
### Direction & understanding
- Goals & outcomes
- Problems & needs
- Context & constraints
- Stakeholders & actors
- Strategy & alternatives

### Exploration & discovery
- Research
- Open-source exploration
- Reverse engineering
- Competitive benchmarking
- Opportunity discovery

### Structure & relationships
- Capability catalogue
- Components & elements
- Traceability graph
- Dependency mapping
- Data & integration mapping

### Definition & specification
- Requirements
- Behavior & scenarios
- Rules & policies
- Contracts & interfaces
- Acceptance & readiness

### Design & simulation
- Experience & journeys
- Screen & navigation design
- Accessibility & inclusion
- Prototype & simulation
- Live preview & comparison

### Planning & coordination
- Roadmap & milestones
- Task & work management
- Prioritization
- Responsibility & ownership
- Resources & budgets

### Execution & engineering
- Implementation
- Automation & agents
- Environment & runtime
- Integration & interoperability
- Debugging & repair

### Verification & assurance
- Tests & validation
- Evidence & provenance
- Security & privacy
- Performance & reliability
- Quality & readiness review

### Knowledge & decisions
- Knowledge library
- Decision records
- Methods & skills registry
- Lessons & failure patterns
- Assumptions & uncertainty

### Continuity & collaboration
- Resume & recovery
- Review & feedback
- Handoffs & transitions
- Communication & coordination
- History & comparisons

### Operations & evolution
- Deployment & releases
- Monitoring & observability
- Incidents & recovery
- Usage & outcome measurement
- Maintenance & evolution

### Intelligence & possibility
- Method selection
- Resource optimization
- Gap & contradiction discovery
- Experiments & counterfactuals
- Learning & adaptation

## Cross-cutting reusable capabilities
- Perspective registry with manifest metadata, applicability, inputs/outputs, required links, permissions, version and evidence.
- Select, pin, customize, compose, compare, save and share perspectives; support table, board, timeline, map/graph, canvas, preview, document, checklist and activity feed.
- Stable scoped IDs and typed directional edges across observed elements, capabilities, requirements, screens, data, implementations, tests, results, decisions and handoffs.
- Query impact both directions: what depends on this and what is affected if this changes?
- Import versioned sources safely; show completeness, source lineage, confidence and runtime verification gaps.
- Handoff gate rules proportional to stakes; require explicit review/approval where necessary; visible missing prerequisites.
- Actual executable preview and screenshot/trace evidence, not synthetic UI passed off as working implementation.
- Recover last meaningful item and drafts; configurable home so Continuity is available but not forced.
- Catalog methods (outcome, problem, research, capability, design, behavior/BDD, data, evidence, TDD, risk, experiment etc) as optional profiles.
- Resource selector evaluates open-source, internal, vendor, human, deterministic/AI/hybrid under verifiable cost/fitness/safety.
- Accessibility: visual-first legibility, keyboard navigation, focus, text labels and visual notifications.
- History/provenance/permissions/status: distinguish proposed, observed, reviewed, approved, implemented, tested, deployed, measured.
- Prioritize small complete vertical slices over generating empty pages for every perspective.

## Overlooked items / anti-failure checks
- Fact vs hypothesis vs proposal vs verified result; many-to-many relationships and contradictory evidence.
- Screens with no capability mapping, capabilities with no observed screen, tests with no requirement, requirements with no test.
- Change impact, stale evidence, source drift and requirements supersession.
- External data source freshness, security/licensing, accessibility, nonfunctional requirements.
- Real world activity tracking vs UI screen completion; can complete objective without passing through every perspective.
- Multi-device and multi-agent conflict resolution; branch/worktree isolation and permissions.
- Recovery from failed import, interrupted work and missing source; preserve previous valid checkpoint.
- Explanation for selected method/resource, plus easy manual override.
- Negative paths, permissions, data contracts, concurrency, rollback and support/operability.
- Trace-to-preview connection: click an item and see actual implementation state and latest validated revision.

## Implementation priority
P0: perspective registry and unified item graph, 6 versatile layouts, import + evidence, selected item detail, links/unknown mapping, configurable home and resume.
P1: requirements and acceptance, review/handoff, real runnable preview with tests and exact revision, planning and resource/method selector.
P2: observability, cross-project learning, advanced graphs, role/approval management, ecosystem plugins, simulations, metrics and large-scale collaboration.
Build a complete small slice before multiplying pages.

## Research evidence (discovery, not adoption)
- GitHub Projects multiple configurable table/board/roadmap views: https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project
- Backstage plugin catalog, catalog links, search and templates: https://backstage.io/docs/overview/technical-overview/
- Plane optional project modules and saved views: https://docs.plane.so/projects/project-settings
- Tuleap requirements-to-tests traceability: https://www.tuleap.com/requirements-management/
- Storybook interaction/preview testing: https://storybook.js.org/docs/writing-tests/interaction-testing
- OpenTelemetry traces with linked spans and status: https://opentelemetry.io/docs/concepts/signals/traces/
- Codex isolation with worktrees and reviews: https://openai.com/index/introducing-the-codex-app/
Do not treat marketing pages or the existence of a feature as acceptance evidence of suitability. Review licenses, deployment architecture, maintenance, security, and keyboard/a11y separately before adoption.
