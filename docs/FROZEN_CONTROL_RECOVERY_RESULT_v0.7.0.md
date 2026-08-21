# Frozen Family B Control sustained-threat recovery result — v0.7.0

## Frozen result

The prospectively specified v0.7 sustained-threat defense/recovery intervention **did not improve competitiveness**.

The original v0.2 competitiveness protocol was rerun unchanged with 400 matches per player order, seed 42001, and the same `[0.30, 0.70]` decisive-win-rate window.

### Target matchup

Family B Pressure vs Control:

- v0.5 Pressure decisive win rate: `0.821`
- v0.7 Pressure decisive win rate: `0.979`
- change: `+0.158`
- competitive after intervention: **no**

The target matchup moved substantially **away** from the competitiveness window.

### Collateral matchup

Family B Control vs Chaos:

- v0.5 Control decisive win rate: `0.484`
- v0.7 Control decisive win rate: `0.408`
- change: `-0.077`
- remained competitive: **yes**

## Interpretation

The v0.6 decomposition correctly identified low defensive frequency and weak spatial recovery as descriptive features of Family B Control under Pressure, but the simple deterministic policy response tested here is **not a successful corrective mechanism**.

In particular, automatically retreating after sustained close-range `advance` sequences appears to sacrifice initiative/value rather than producing useful recovery under the frozen engine. The retained negative result therefore rules out this specific intervention rule as a justified balancing change.

No second post-result adjustment is introduced in v0.7. Construct recovery remains blocked.

## Scientific boundary

This is a synthetic policy-engineering result. It is not evidence that the PCC Control construct itself fails in spatial games. It shows that one prospectively motivated implementation of sustained-threat recognition worsened the target policy matchup.
