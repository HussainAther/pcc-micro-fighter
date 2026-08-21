# Prospective Family B Control counter-window intervention — v0.5.0

## Purpose

Version 0.4.0 identified a specific Family B Control failure mode under the frozen Pressure-vs-Control comparison: successful defenses often created concrete one-tick punish windows, but Family B Control almost never converted those windows into landed counters. The v0.5 intervention changes exactly one decision rule to test whether that mechanism explains part of the v0.2 competitiveness failure.

## Frozen intervention

Only `ControlPolicyB` is changed.

When all of the following public-state conditions hold:

1. the previous opponent action was `attack`;
2. Family B Control's previous action was `guard` or `evade`;
3. current distance is within attack range (`distance <= 1`); and
4. Family B Control's own attack cooldown is clear;

Family B Control selects `attack` immediately.

Under the frozen engine, the previous `guard`/`evade` prevents the opponent attack from landing, and a previous opponent `attack` places that opponent on its one-tick attack cooldown. Because neither `attack`, `guard`, nor `evade` changes position, current in-range distance also implies the defended attack resolved in range. The intervention therefore uses only public history and current legal state; it adds no hidden information.

## Explicit non-changes

The following remain unchanged:

- Family A policies;
- Family B Pressure and Chaos policies;
- all engine rules, damage, cooldowns, arena geometry, health, and match length;
- the v0.2 competitiveness seeds and 30%–70% decisive-win-rate acceptance window;
- the requirement to balance both player orders;
- the rule that no PCC dominance cycle is required.

No second policy adjustment is permitted after inspecting the v0.5 competitiveness result.

## Evaluation

The original v0.2 competitiveness protocol is rerun unchanged using the modified Family B Control policy. The frozen v0.2 result remains retained as the baseline and is not overwritten.

This is a mechanistically justified intervention test, not construct recovery and not evidence from human data.
