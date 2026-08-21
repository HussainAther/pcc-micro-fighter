# Threat conversion and defensive counter-value decomposition — v0.4.0

## Purpose

The frozen v0.2 competitiveness gate showed opposite Pressure-vs-Control outcomes across the two independently structured policy families. The v0.3 decomposition then showed that Pressure creates spatial compression, attack opportunities, and delayed defensive responses in both families, so raw threat generation alone does not explain the divergence.

This v0.4 diagnostic asks a narrower question: **why does Family A Control convert Pressure exposure into winning exchanges while Family B Control is overwhelmed?**

The policies and engine are not changed for this experiment.

## Frozen primary comparison

Only the Pressure-vs-Control matchup is primary. Both player orders are balanced. The default run uses 400 matches per order per family and fresh deterministic seed `64001`.

## Prespecified exchange metrics

The decomposition reports:

1. **Attack opportunity** — the fighter is within attack range after simultaneous movement and its reconstructed attack cooldown is zero before the action.
2. **Attack take rate** — attack attempts divided by attack opportunities.
3. **Hit conversion per attack** — landed hits divided by attack attempts.
4. **Damage per attack opportunity** — total damage dealt divided by attack opportunities.
5. **Defensive response rate** — guard/evade responses to opponent attacks.
6. **Successful defense** — guard/evade against an incoming attack with no hit received.
7. **Counter window** — a successful defense that leaves the fighters in attack range with a surviving next tick. Because the attacker just attacked, that next tick occurs while the attacker is on attack cooldown.
8. **Counter attack take rate** — next-tick attacks divided by counter windows.
9. **Counter hit rate** — landed next-tick counters divided by counter windows and, separately, by attempted counters.
10. **Cooldown punishment** — next-tick landed attacks during windows created by an opponent attack.
11. **Positional recovery after defense** — successful defenses followed by increased distance on the next resolved tick.
12. **Damage received per opponent threat tick** — damage taken divided by opponent `advance`/`attack` ticks.

## Status rule

This is a **descriptive mechanism decomposition**, not a construct-validity or competitiveness confirmation. No threshold is used to declare PCC support, and no policy or engine change is permitted after observing the result within this release.

A later revision may make one prospectively justified intervention only after this decomposition identifies a concrete exchange-conversion mechanism.
