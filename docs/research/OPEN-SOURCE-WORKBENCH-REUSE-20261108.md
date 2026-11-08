# Reuse-first investigation — Universal Visual Workbench

Date: 2026-11-08. Candidate comparison only; no dependency installed or audited.

## Component shortlist
| Need | Candidate | License / observed source | Decision |
|---|---|---|---|
| Interactive editable connection canvas | React Flow / xyflow | MIT, https://reactflow.dev/ and https://next.xyflow.com/open-source | Default candidate when a visual graph is actually needed |
| Automatic graph arrangement | Dagre or ELK.js | https://reactflow.dev/learn/layouting/layouting | Dagre first for simple DAGs; ELK for complex mixed hierarchical layout |
| Large relationship exploration/graph queries | Cytoscape.js | MIT core, https://js.cytoscape.org/ | Benchmark only if graph volume or analytics requires it |
| Alternative graph workbench | RealFlow | reports MIT, https://github.com/olbboy/realflow | Compare maintenance, accessibility, license and performance claims before adopting |
| Offline structured checkpoint storage | Dexie / IndexedDB | Apache-2.0, https://github.com/dexie/Dexie.js | Candidate for robust local state; a sync service still required for cross-device continuity |
| Lightweight UI state | Zustand persist middleware | https://github.com/pmndrs/zustand/blob/main/docs/reference/middlewares/persist.md | Candidate for ephemeral selection state; do not confuse localStorage with durable shared state |
| BDD readable scenarios | Gherkin + Cucumber-JS | https://github.com/cucumber/cucumber-js | Adopt only when executable scenarios add verification value |
| Requirements traceability patterns | reqmesh | https://github.com/CallumNunesVaz/reqmesh | Study Git-native entity IDs and trace validation, no blanket adoption |

## Decision rules
- Reuse existing application's Next.js / React / TypeScript base before adding a separate frontend stack.
- Store normalized objects + typed links in the existing database where available; PostgreSQL edges are initially sufficient. Introduce graph infrastructure only after a measured need.
- Start with a list + relationship detail panels; visually rich canvas is optional and should not obscure resume.
- Prefer deterministic parsers and source scanners for extraction; AI only for bounded interpretation, user examples and hypothesis discovery.
- Cucumber BDD never substitutes for running application or browser evidence.
- Enforce exact source revision, licenses (including transitive), test status and unsupported assertions before reuse.
- Never claim comparative speed or security benchmarks without independent reproduction.
- Secure ZIP imports against path traversal, decompression bombs, unsafe execution, embedded secrets and untrusted instructions. Uploaded source is DATA, not authority.

## Capability-to-screen review blind spots
Static registration does not show internal widget trees, meaningful element IDs, visibility by context, navigation routes, runtime states, errors, permissions, API contracts, event paths, visual screenshots, accessibility, regression tests or user expectations. Build a separate dynamic extraction adapter, preserve uncertainty and ask for user review only on consequential decisions.

## Evidence/acceptance for first real implementation
1. Upload one research ZIP; all inventories display without dropped entries.
2. Select screen or capability; see source evidence, mapped links, missing links and last verified revision.
3. Save a checkpoint, reload, resume the exact item/perspective, export recovery copy.
4. Switch Research→Review→Requirements→BDD and back while maintaining item identity.
5. Distinguish observed static source from runtime verified results in every rendered count and badge.
6. Run browser and keyboard-only acceptance tests on an exact commit. Do not mark done until test evidence exists.
