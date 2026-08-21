# Validation artifacts

## `competitiveness.json` — v0.2.0 frozen result

The first prospectively specified two-family competitiveness gate **failed**. The result is retained unchanged.

- Family A: 0/3 pairwise matchups competitive.
- Family B: 1/3 pairwise matchups competitive.
- No dominance cycle was required.
- Construct recovery is not authorized by this result.

See `docs/COMPETITIVENESS_PROTOCOL.md` and `docs/FROZEN_COMPETITIVENESS_RESULT_v0.2.0.md`.

## `pairwise-sweep.json` — v0.1.0 smoke artifact

Engineering-only initial pairwise diagnostics from the first policy family. It predates the frozen v0.2 competitiveness gate and is not construct-validity evidence.

- `pressure-dominance-decomposition.json`: frozen v0.3 diagnostic of space capture, attack opportunity, delayed defensive forcing, damage conversion, and compact-arena dependence.
## `threat-conversion-decomposition.json` — v0.4.0 frozen result

Frozen descriptive Pressure-vs-Control decomposition of defense success, counter-window creation/use, landed punishment, cooldown punishment, positional recovery, and damage conversion. The result identifies a strong Family A vs Family B split in defense-to-counter conversion. It does not modify policies or authorize construct recovery.

