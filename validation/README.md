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


## `control-counter-intervention-v0.5.0.json` — prospective single-mechanism intervention

Reruns the unchanged v0.2 competitiveness gate after modifying only Family B Control's recognition of a successful-defense cooldown punish window. The target Pressure-vs-Control matchup improved but remained noncompetitive; Control-vs-Chaos remained competitive. Construct recovery remains blocked.

`competitiveness-v0.5.0.json` is the raw unchanged-gate output for the v0.5 policy state.

- `residual-pressure-decomposition.json`: frozen v0.6 Family B residual Pressure diagnostic after the v0.5 Control counter-window intervention.

## `control-recovery-intervention-v0.7.0.json` — prospective sustained-threat intervention

Reruns the unchanged v0.2 competitiveness gate after one Family B Control change motivated by v0.6: recognition of sustained close Pressure with defense against attacks and retreat after advances. The target Pressure-vs-Control matchup worsened, while Control-vs-Chaos remained competitive. The negative result is retained and construct recovery remains blocked.

`competitiveness-v0.7.0.json` is the raw unchanged-gate output for the v0.7 policy state.

- `retreat-backfire-decomposition.json`: frozen v0.8 comparison explaining why the rejected v0.7 retreat rule backfires relative to v0.5.


## `effective-chaos-validation-v0.9.0.json` — frozen effective-Chaos result

Tests predictable competent, state-aware random, and effective-Chaos candidate policies against neutral and a fixed adaptive exploiter. All four prespecified checks pass, but the fixed exploiter did not outperform the predictable baseline, so exploiter calibration remains an explicit limitation. The random baseline is more entropic than the effective-Chaos candidate while being far less competitively adequate, directly supporting the distinction `Chaos != randomness`. This remains mechanism evidence rather than full construct recovery.
