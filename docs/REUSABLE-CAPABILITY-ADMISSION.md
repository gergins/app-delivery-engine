# Reusable capability admission — lightweight decision record

This is a checklist to apply **only when proposing to promote a pattern** from an example into ADE-wide reusable infrastructure.

1. **Problem:** What repeated delivery problem does it solve? Which different application types actually need it?
2. **Evidence:** Which working applications demonstrate the need? What tests, screenshots, traces or user outcomes exist?
3. **Existing alternatives:** Which maintained open-source or ADE capabilities were considered? License, security and maintenance tradeoffs?
4. **Boundary:** What is generic versus product-specific? What must remain configurable or swappable?
5. **Cost:** What dependency, complexity, integration, maintenance and migration burden does it add?
6. **Validation:** What contract, integration and real-world tests demonstrate portability? What fails?
7. **Decision:** adopt, adapt, keep as example, defer or reject. Record owner, date and rollback path.

**Snake-specific conclusion:** the pure state transition pattern and input-adapter separation are promising examples; a general-purpose game engine is **not** justified. Booking transactionality and realtime VRS need different foundations. Do not add dependencies or new services solely to unify them.

**Evidence labels:** proposed / implemented / locally tested / CI verified / browser verified / production observed. Do not advance a label without matching evidence.
