# pcc-micro-fighter

A deliberately tiny 1v1 fighting-game laboratory for testing whether PCC-like strategic mechanisms survive when **space and threat range** are introduced.

This is not a conventional fighting game and not a PCC confirmation. v0.5.0 is a deterministic headless simulator designed to minimize confounds.

## Why this environment?

Poker, Liar's Dice, and repeated RPS are abstract decision environments. Micro-Fighter adds a new ingredient: spatial control. Pressure can therefore be tested as literal commitment and space compression rather than only betting/escalation.

## Actions

Every policy uses the same five actions:

`advance`, `retreat`, `attack`, `guard`, `evade`

No action is named Pressure, Control, or Chaos.

## Install

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

## Simulate one match

```bash
python -m pcc_micro_fighter simulate --p0 pressure --p1 control --seed 17
```

## Pairwise smoke sweep

```bash
python -m pcc_micro_fighter sweep --matches-per-order 100 --output validation/pairwise-sweep.json
```

See `docs/RULESET.md`, `docs/MEASUREMENT_CONTRACT.md`, and `docs/VALIDATION_ROADMAP.md`.


## v0.2 competitiveness gate

Two independently structured synthetic policy families are now included. Before construct recovery, run the frozen no-trivial-domination gate:

```bash
python -m pcc_micro_fighter competitiveness
```

Every P/C/Chaos pair is evaluated in both player orders. A matchup is considered competitive only when the decisive win rate lies in `[0.30, 0.70]`. **No dominance cycle is required.** See `docs/COMPETITIVENESS_PROTOCOL.md`.


## Frozen v0.2 result

The first two-family competitiveness gate **failed** and is retained without policy retuning. Family A passed 0/3 pairwise competitiveness checks; Family B passed 1/3. The failure means the current micro-fighter policies are not yet a suitable laboratory for confirmatory construct recovery. See `docs/FROZEN_COMPETITIVENESS_RESULT_v0.2.0.md`.

## v0.3 Pressure-dominance decomposition

The frozen v0.2 policies were decomposed without retuning. Pressure produced more attributable spatial compression, more in-range attack opportunities, and more next-tick defensive/retreat responses in all four Pressure-vs-Control/Chaos family matchups. However, damage conversion did not replicate: Family A Control still defeated Pressure decisively. A compact-arena replay showed that removing most initial approach distance barely changed Pressure win rates, so the imbalance is not simply an arena-access artifact. See `docs/FROZEN_PRESSURE_DOMINANCE_RESULT_v0.3.0.md`.
## v0.4 frozen threat-conversion decomposition

The v0.4 diagnostic keeps the v0.2 policies unchanged and asks why Family A Control defeats Pressure while Family B Control is overwhelmed. It decomposes successful defense, counter-window creation, next-tick punishment, attack-opportunity conversion, cooldown punishment, positional recovery, and damage received per Pressure threat tick.

The frozen result points to **defense-to-counter conversion** as the key family difference: Family A Control both defends more incoming attacks and converts substantially more surviving counter windows into landed hits. Family B Control often creates a window but rarely takes or lands the counter. This is a descriptive mechanism result, not construct-recovery evidence.

Run it with:

```bash
python -m pcc_micro_fighter threat-conversion
```

See `docs/THREAT_CONVERSION_DECOMPOSITION_PROTOCOL.md` and `docs/FROZEN_THREAT_CONVERSION_RESULT_v0.4.0.md`.


## v0.5 prospective Family B Control counter intervention

The v0.4 decomposition justified one prospective policy change: Family B Control now recognizes a successful public guard/evade against an in-range opponent attack as a one-tick cooldown punish window and immediately attacks when its own attack cooldown is clear. No other policy or engine rule changes.

The original v0.2 competitiveness gate was rerun unchanged. Family B Pressure-vs-Control moved from `0.931` to `0.821` Pressure decisive win rate, while Control-vs-Chaos remained competitive (`0.484`). The full gate still fails, so this is a **partial mechanistic improvement, not a successful rebalance**, and construct recovery remains blocked.

Run the frozen intervention evaluation with:

```bash
python -m pcc_micro_fighter control-counter-intervention
```

See `docs/PROSPECTIVE_CONTROL_COUNTER_INTERVENTION_v0.5.0.md` and `docs/FROZEN_CONTROL_COUNTER_INTERVENTION_RESULT_v0.5.0.md`.

## v0.6 residual Pressure decomposition

After the v0.5 counter-window intervention improved but did not balance Family B Pressure-vs-Control, v0.6 freezes a descriptive residual-mechanism analysis. The result points away from repeated Pressure re-engagement and toward a broader defensive-state / spatial-recovery weakness in Family B Control: it defends only about 27% of Pressure attacks and regains distance after only about 3% of sustained close-threat sequences. See `docs/RESIDUAL_PRESSURE_DECOMPOSITION_PROTOCOL.md` and `docs/FROZEN_RESIDUAL_PRESSURE_RESULT_v0.6.0.md`.

## v0.7 prospective sustained-threat recovery intervention

The v0.6 residual decomposition motivated one prospective Family B Control rule: after two consecutive close-range opponent `advance`/`attack` actions, defend an immediate attack or retreat after an advance, while preserving the v0.5 punish-window priority.

The unchanged competitiveness gate produced a retained **negative intervention result**. Family B Pressure-vs-Control worsened from `0.821` to `0.979` Pressure decisive win rate. Control-vs-Chaos remained competitive at `0.408`.

This rules out the simple deterministic defense/retreat response as a justified balancing mechanism. No second v0.7 tuning step is allowed, and construct recovery remains blocked.

Run the frozen evaluation with:

```bash
python -m pcc_micro_fighter control-recovery-intervention
```

See `docs/PROSPECTIVE_CONTROL_RECOVERY_INTERVENTION_v0.7.0.md` and `docs/FROZEN_CONTROL_RECOVERY_RESULT_v0.7.0.md`.
