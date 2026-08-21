# Frozen threat-conversion result — v0.4.0

## Status

This is a frozen descriptive mechanism result. It does **not** confirm construct recovery or competitiveness, and no policy or engine parameter was changed after observing the run.

Default design: 400 matches per player order per family, seed `64001`, Pressure vs Control only, seat/order balanced.

## Primary result

The opposite Pressure-vs-Control outcomes from v0.2 reproduce:

- Family A Pressure decisive win rate: **0.0000**
- Family B Pressure decisive win rate: **0.9375**

The exchange decomposition identifies a much more specific family difference than raw threat generation.

| Control metric | Family A | Family B | A - B |
|---|---:|---:|---:|
| Successful defense / opponent attack | 0.5918 | 0.2384 | 0.3534 |
| Counter-window creation | 0.9800 | 0.8171 | 0.1629 |
| Counter attack take rate | 0.3542 | 0.0208 | 0.3333 |
| Counter hit / window | 0.2227 | 0.0089 | 0.2138 |
| Cooldown punishment hit rate | 0.1445 | 0.0054 | 0.1390 |
| Damage / attack opportunity | 0.2864 | 0.2913 | -0.0050 |
| Damage received / Pressure threat tick | 0.2374 | 0.4476 | -0.2102 |
| Net damage / match | 1.2500 | -1.6400 | 2.8900 |

## Interpretation

Family A Control's advantage is concentrated in **defense-to-counter conversion**:

1. It successfully defends a much larger share of incoming Pressure attacks.
2. It usually retains a valid counter window after those defenses.
3. It takes roughly one third more of those counter windows than Family B Control.
4. Most importantly, it lands counters in about **22.3%** of windows, compared with only **0.9%** for Family B.
5. Family A therefore receives far less damage per Pressure threat tick even though v0.3 showed that Pressure generates spatial compression and threat volume in both families.

Raw attack-opportunity efficiency is *not* the distinguishing explanation: Control damage per attack opportunity is nearly identical between families (0.2864 vs 0.2913). The family split instead appears to arise from **when Control chooses to convert defense into punishment**.

This supports a prospectively justified next intervention targeting Family B Control's defense-to-counter transition, rather than changing arena size, attack damage, or Pressure aggression to tune win rates directly.
