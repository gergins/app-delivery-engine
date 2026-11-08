# Snake — smallest reusable browser application slice

A dependency-free static browser app with a pure state-transition module and Node's built-in test runner.

## Run
Serve this folder using any static HTTP server, e.g. `python -m http.server 8000` from `examples/snake`, then open http://localhost:8000. ES modules may not load when opening `index.html` directly with `file://`.

## Test
`node --test examples/snake/snake-core.test.mjs` from repository root (Node 18+).

## Reusable capabilities demonstrated
- Pure domain state machine, separate from browser rendering.
- Deterministic injectable randomness for tests.
- Keyboard, on-screen buttons and swipe input.
- Accessible status and focus-visible controls.
- Browser-only delivery without backend, auth, database or third-party packages.
- Minimal tests for movement, scoring, spawning and collision.

## Boundaries
This is an **example and capability reference**, not a universal game framework or new ADE platform. The original Snake artifact is separate; this implementation is a compact demonstration. No CI claim until GitHub Actions runs; no browser interaction claim until browser-tested. No auto-merge/deploy.
