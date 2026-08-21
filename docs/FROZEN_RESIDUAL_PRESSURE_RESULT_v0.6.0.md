# Frozen Residual Pressure Result — v0.6.0

The frozen Family B Pressure-vs-Control decomposition was run with 400 matches per player order and seed 75001, using the unchanged v0.5 policy hash.

## Result

Pressure decisive win rate remained **0.8216** (585 Pressure wins, 127 Control wins, 88 draws).

The residual advantage is not explained primarily by immediate Pressure re-engagement after punishment:

- Pressure re-engagement after a Control hit: **0.4519**
- Pressure re-engagement after a successful Control defense: **0.2343**

Instead, Family B Control shows weak defensive and spatial recovery behavior under sustained Pressure:

- defense rate versus Pressure attacks: **0.2681**
- defensive-action rate during close threat: **0.3318**
- distance-gain rate during Pressure threat: **0.0058**
- distance-loss rate during Pressure threat: **0.2407**
- post-sustained-threat spatial recovery rate: **0.0305**
- damage taken per close-threat tick: **0.4880**

During sustained close-threat runs, Control dealt **1.9488** damage per match but received **2.1363**, leaving the exchange slightly Pressure-favorable even after the v0.5 counter-window intervention.

## Interpretation

The v0.5 counter recognition rule fixed one specific punish failure but did not address the larger state-selection problem. Family B Control often fails to enter a defensive response when Pressure attacks, and after sustained close threat it almost never restores distance. The evidence therefore supports a future *single prospective defensive-state / positional-recovery intervention* more strongly than another counter-damage or attack-strength change.

This result does not authorize construct recovery, does not change the frozen competitiveness window, and does not justify post-hoc tuning of the v0.6 run.
