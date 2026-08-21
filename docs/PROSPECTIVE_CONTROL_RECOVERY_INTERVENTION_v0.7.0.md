# Prospective Family B Control sustained-threat recovery intervention — v0.7.0

## Purpose

Version 0.6.0 found that the residual Family B Pressure advantage after the v0.5 counter-window fix was associated with low defensive frequency and almost no spatial recovery during sustained close threat. This release tests one prospectively specified public-history response rule and then reruns the original v0.2 competitiveness gate unchanged.

## Frozen intervention

Only `ControlPolicyB` is changed.

The existing v0.5 successful-defense punish rule retains priority.

Otherwise, when all of the following hold:

1. current distance is within attack range (`distance <= 1`);
2. the opponent's two most recent public actions are each `advance` or `attack`;

Family B Control interprets the state as sustained close Pressure.

- If the most recent opponent action is `attack`, Control selects `evade` when its evade cooldown is clear, otherwise `guard`.
- If the most recent opponent action is `advance`, Control selects `retreat`.

This rule uses only current public state and public action history. It does not inspect latent PCC labels, hidden state, future actions, or outcome information.

## Explicit non-changes

The following are unchanged:

- all Family A policies;
- Family B Pressure and Chaos;
- engine rules, damage, cooldowns, health, geometry, and match length;
- the v0.5 counter-window intervention;
- the v0.2 competitiveness seed and `[0.30, 0.70]` decisive-win-rate acceptance window;
- player-order balancing;
- the rule that no PCC dominance cycle is required.

No second policy adjustment is allowed after the v0.7 competitiveness result is inspected.

## Evaluation

The original competitiveness protocol is rerun with `400` matches per player order and seed `42001`. The primary comparison is Family B Pressure-vs-Control relative to the frozen v0.5 intervention result. Family B Control-vs-Chaos is retained as a collateral check.

A result may improve, worsen, or leave competitiveness unchanged. None of those outcomes authorizes post-hoc tuning in this release.
