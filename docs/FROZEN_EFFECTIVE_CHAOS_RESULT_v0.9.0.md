# Frozen effective Chaos result — v0.9.0

Status: **completed and retained**.

The v0.9 experiment tested a predictable competent baseline, a state-aware random
baseline, and a value-bounded effective-Chaos candidate against both the existing
neutral policy and a fixed adaptive public-history exploiter.

## Result

All four prespecified checks passed.

| Policy | Conditional entropy vs neutral | Decisive win rate vs neutral | Mean health margin vs neutral | Decisive win rate vs exploiter | Mean health margin vs exploiter |
|---|---:|---:|---:|---:|---:|
| predictable competent | 0.323 | 0.500* | 0.000 | 0.500* | 0.000 |
| state-aware random | **0.933** | 0.031 | -2.609 | 0.543 | 0.536 |
| effective Chaos | 0.878 | **0.418** | **-0.273** | **0.899** | **2.329** |

`*` The predictable baseline produced only draws in these two symmetric/fixed
matchups, so the reported decisive win rate defaults to 0.5 when there are no
decisive outcomes.

The important falsification is that the random baseline had **higher conditional
action entropy** than the effective-Chaos candidate while having far worse value
against the neutral opponent. Thus raw randomness/entropy is not sufficient for
the Chaos construct in this environment.

The effective-Chaos candidate met the frozen requirements for:

1. higher unpredictability than the predictable baseline;
2. preserved value relative to the random baseline;
3. reduced performance degradation relative to the predictable baseline under the
   fixed adaptive exploiter;
4. preserved value relative to random under exploitation.

## Interpretation

This is the first Micro-Fighter result providing **provisional support** for a game-specific effective-Chaos mechanism:

`unpredictability × strategic adequacy`.

It does not establish a universal Chaos scalar. Importantly, the fixed adaptive exploiter did not outperform the predictable baseline (that matchup was all draws), so exploiter calibration remains a limitation and should be strengthened prospectively before this result is promoted to full construct recovery. The exploiter is one fixed
synthetic learner, and Micro-Fighter's broader competitiveness gate remains
unresolved for the original P/C/Chaos families. The result should therefore be
used as mechanism evidence, not as full cross-family construct recovery.

No human data were used.
