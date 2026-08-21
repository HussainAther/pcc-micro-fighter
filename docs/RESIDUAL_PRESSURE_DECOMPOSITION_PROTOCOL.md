# Residual Family B Pressure Decomposition Protocol — v0.6.0

## Question

After the prospectively justified v0.5 defense-to-counter intervention moved Family B Pressure-vs-Control toward competitiveness but did not clear the frozen gate, what residual mechanism still sustains Pressure's advantage?

## Frozen boundary

No policy or engine parameter is changed for this diagnostic. The expected `policies.py` SHA-256 is the frozen v0.5 hash recorded by the prior intervention release.

The primary matchup is Family B Pressure vs Family B Control, balanced over both player orders with 400 matches per order and seed 75001.

## Prespecified diagnostics

The decomposition measures:

- Control defense frequency against Pressure attacks;
- consecutive close-range Pressure threat runs;
- Control retreat, distance gain, and distance loss during Pressure threat ticks;
- Control spatial recovery within two ticks after sustained close-threat runs;
- damage taken and dealt during sustained close-threat runs;
- Control hit rate during close threat;
- Pressure re-engagement on the next tick after a Control hit;
- Pressure re-engagement on the next tick after a successful Control defense.

A **Pressure threat tick** is a tick on which Pressure chooses `advance` or `attack`. A **close threat tick** additionally requires post-resolution distance to be within attack range. A **sustained close-threat run** contains at least two consecutive close threat ticks.

This is an explanatory decomposition, not a construct-validity or competitiveness acceptance test. No threshold may be used to tune the current run after observing the output.
