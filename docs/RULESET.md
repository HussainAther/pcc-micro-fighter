# Frozen v0.1 Ruleset

The initial laboratory uses simultaneous discrete ticks in a one-dimensional arena embedded in a top-down-ready coordinate model.

- arena coordinates: 0..6
- starting positions: 1 and 5
- starting health: 5
- attack range: distance <= 1
- attack damage: 1
- attack cooldown: 1 tick
- evade cooldown: 1 tick
- maximum match length: 80 ticks
- identical fighter capabilities
- no combos, projectiles, equipment, character stats, stamina, animation timing, or hidden information

Movement and actions are chosen simultaneously. `guard` and `evade` block an incoming in-range attack in v0.1. The intentionally small ruleset is meant to isolate spatial competitive mechanisms before adding richer dynamics.
