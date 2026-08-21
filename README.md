# pcc-micro-fighter

A deliberately tiny 1v1 fighting-game laboratory for testing whether PCC-like strategic mechanisms survive when **space and threat range** are introduced.

This is not a conventional fighting game and not a PCC confirmation. v0.2.0 is a deterministic headless simulator designed to minimize confounds.

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
