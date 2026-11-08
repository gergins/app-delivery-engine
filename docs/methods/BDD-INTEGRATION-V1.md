# Behavior-Driven Development integration v1

Status: proposed operating method. Reference: https://cucumber.io/docs/bdd/

## Placement
BDD is a selectable working **perspective** across discovery, formulation and automation. It complements outcome-, research-, requirements-, design- and test-driven methods; it is not a replacement for them and is not mandatory for every simple task.

## When to apply
Use BDD where observable behaviors, cross-role rules, edge cases or acceptance criteria materially improve shared understanding and verification. Do not force Gherkin onto straightforward documentation or low-risk refactors.

## Discovery
From research evidence and requirements, collect concrete user examples; identify actors, preconditions, business rules, exceptional paths, permissions, failures and unresolved assumptions. Preserve source references and distinguish facts from proposed behavior. Challenge assumptions with contrasting examples.

## Formulation
For each behavior:
- stable scenario ID and feature/capability/requirement references;
- business-readable **Given / When / Then**, describing externally observable outcomes, not implementation details;
- expected error, recovery, accessibility, concurrency and security behavior where relevant;
- unambiguous data examples and acceptance result;
- owner, review state, provenance and revision.

## Automation and evidence
Connect approved scenarios to appropriately scoped checks (unit, contract, API, UI/browser), avoiding excessive UI-only tests. Tests must fail meaningfully before implementation when possible, and report exact commit SHA, environment, inputs and result. Run tests on the actual app where the scenario requires it. Tag unautomated scenarios as manual or pending; do not call them passing.

## Handoff gate
A behavior handoff contains scenario inventory, linkage coverage, open questions, conflicts, approved acceptance examples, automation assignments and evidence. Incomplete critical scenarios block readiness; low-risk gaps may be accepted explicitly. No self-merging or deploying.

## Example (synthetic camping booking)
```gherkin
Feature: Pitch booking availability
  As a camper
  I want only reservable pitches shown
  So that I cannot double-book a pitch

  Scenario: Confirm an available pitch
    Given a pitch is available for the selected three nights
    When the camper confirms the reservation
    Then exactly one confirmed booking exists
    And that pitch is no longer bookable for overlapping dates
    And a confirmation is visible

  Scenario: Reject a concurrent overlapping reservation
    Given one confirmed reservation exists for the pitch and dates
    When a second camper attempts overlapping dates
    Then no second confirmed booking is created
    And the camper sees an available alternative or a clear explanation
```

## Cross-perspective trace contract
`researchFindingId -> capabilityId -> requirementId -> scenarioId -> screenIds/APIIds -> testIds -> evidenceIds`.

For any selected scenario show: why it exists, exact requirement, relevant screens, implementation owner, test status, last verified revision, missing links and one next action. Follow the same stable IDs when switching perspective so a user never loses position.

## Definition of ready / done
**Ready for implementation**: key behaviors agreed, critical counterexamples identified, requirement trace established, feasibility and access constraints stated, open risks acknowledged.

**Verified done**: behavior implemented in running system, appropriate real tests passed on exact revision, evidence available to inspect, remaining caveats clear. Never substitute passing Gherkin syntax checks for working behavior.

## Risks
Over-specifying scenarios, treating BDD as just a test framework, mismatching UI and domain semantics, stale scenarios after requirement changes, synthetic evidence mistaken for real validation, and unreviewed generated acceptance criteria.

## Reuse-first choices
Start with Markdown/Gherkin files, existing test tools and project repository. Adopt Cucumber only if executable feature-file workflows add real value; do not introduce infrastructure for its own sake.
