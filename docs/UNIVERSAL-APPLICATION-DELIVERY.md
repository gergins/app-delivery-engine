# Universal application delivery — product-independent operating contract

**Status:** proposed on review branch; not a new framework or mandatory workflow.

## Purpose
ADE supports delivery of useful, working applications across domains, interfaces and technologies. Games (Snake), bookings, communications, business operations, learning, commerce, creative tools, scientific applications and unknown future categories are **examples**, not architecture boundaries.

## Adaptive delivery
Choose the smallest effective approach based on user outcome, complexity, consequence, accessibility, resources and evidence:
1. Understand intent and distinguish the requested product from an app-builder platform or engineering control panel.
2. Identify essential user journeys, constraints, assumptions and overlooked needs; do not require an exhaustive questionnaire.
3. Reuse maintained, compatible open-source or proven existing capabilities when they reduce total cost and risk.
4. Choose architecture to fit the app: static page, local-first app, client/server, realtime service, mobile, distributed system or other suitable shape. No universal stack is mandatory.
5. Deliver a **running, inspectable vertical slice** with real interaction before expanding infrastructure.
6. Verify proportionately: unit tests, integration tests, end-to-end journeys, accessibility, security, privacy, reliability and operational evidence as applicable.
7. Present a browser/device preview and a clear path to feedback; distinguish source-created, locally-tested, CI-tested and deployed.
8. Preserve source, evidence, reversibility and explicit human approval for consequential actions.

These are judgment considerations, not required stages for every task. A trivial utility may need one HTML file. A critical communications service requires deeper safety, reliability and assurance.

## Reusable capability categories
- **Intent and product definition:** goal, user journeys, acceptance criteria, uncertainty and blind spots
- **UX and accessibility:** visual-first interaction, keyboard/touch/screen-reader/sign-language-aware interfaces as appropriate
- **Application foundations:** state, routing, data validation, error handling, persistence and configuration
- **Domain behavior:** explicit rules and state machines where useful, independently testable logic
- **Integrations:** APIs, authentication, payments, media, realtime, telephony, maps and notifications only when justified
- **Quality:** deterministic tests, end-to-end browser flows, security and privacy controls, observability appropriate to risk
- **Delivery:** reproducible builds, preview, evidence, rollback, release gates and owner approval
- **Learning:** extract reusable patterns only after real evidence, avoiding premature abstraction

## Reuse policy
A capability must declare its purpose, supported contexts, dependencies, assumptions, limitations, provenance, license and verification status before it is treated as proven. An example implementation is **not** automatically a universal abstraction.

## Anti-patterns
- Treating Snake or any first demo as the ADE product architecture.
- Requiring every app to use the same stack, database, backend, agents, or CI workflow.
- Producing a dashboard or paperwork instead of the application the user asked to experience.
- Generalizing from a single successful example without cross-domain evidence.
- Claiming an app is verified when only source files or test specifications exist.
- Automatically merging, deploying, spending or handling production secrets without approval.

## Cross-domain validation
Test the delivery method against at least three materially different slices: a static interactive game, a transactional booking flow, and a realtime/accessibility-sensitive communication flow. Keep their product repositories separate. Evaluate real behavior, total complexity, cost and failure modes. Do not promote a generic abstraction until the differences and commonalities are observed.
