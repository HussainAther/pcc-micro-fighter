# Frozen competitiveness result — v0.2.0

## Status

**Competitiveness confirmed: false.**

The prespecified `[0.30, 0.70]` decisive-win-rate gate was evaluated once using 400 matches per player order, fresh seed `42001`, and the two independently structured policy families. No policy or threshold was changed after observing the result.

## Family A

| Matchup | First-mode decisive win rate | Competitive? |
| --- | ---: | :---: |
| Pressure vs Control | 0.000 | no |
| Pressure vs Chaos | 0.900 | no |
| Control vs Chaos | 0.861 | no |

Family A therefore contains strong dominance structure and is not suitable for construct-recovery confirmation in its present form.

## Family B

| Matchup | First-mode decisive win rate | Competitive? |
| --- | ---: | :---: |
| Pressure vs Control | 0.931 | no |
| Pressure vs Chaos | 0.863 | no |
| Control vs Chaos | 0.441 | yes |

Family B improves one matchup substantially, but its Pressure mechanism still dominates both alternatives.

## Interpretation

The result does **not** falsify PCC. It falsifies the narrower engineering claim that these provisional micro-fighter policy implementations form a sufficiently non-trivial comparison laboratory under the frozen gate.

No cycle was required, so failure cannot be attributed to absence of a poker-like dominance topology. The immediate scientific/engineering problem is mechanism calibration: the spatial game currently allows the provisional Pressure policies to convert distance-closing and attack threat into too much direct value, while Family A Control also overwhelms Family A Chaos.

Construct recovery remains blocked until a future, prospectively specified policy revision is evaluated under a new frozen competitiveness protocol. The v0.2 result must remain as the baseline failure rather than being overwritten.
