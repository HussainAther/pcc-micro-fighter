# Frozen Pressure-dominance decomposition result — v0.3.0

The v0.2.0 policies and v0.2 competitiveness thresholds were not changed for this diagnostic.

## Result

Three candidate Pressure mechanisms showed the expected directional difference against both Control and Chaos in both independently coded policy families:

- **space capture**: Pressure-minus-opponent spatial compression was positive in all four matchups;
- **attack-opportunity generation**: Pressure used more in-range attacks in all four matchups;
- **delayed defensive-response forcing**: opponents were more likely to guard, evade, or retreat on the tick after a Pressure threat in all four matchups.

**Damage conversion did not replicate.** Family A Control defeated Pressure decisively even though Pressure still produced more compression, in-range attacks, and delayed defensive responses. Pressure-minus-Control net damage in Family A was approximately `-2.43` per match.

Against Family A Chaos and both Family B opponents, Pressure converted its greater threat volume into large positive net-damage differences.

## Compact-arena diagnostic

Starting the fighters adjacent (arena `[0, 3]`) did **not** systematically reduce Pressure's decisive win rate. Mean change across the four matchups was approximately `-0.004`, with changes ranging from about `-0.021` to `+0.008`.

Therefore the v0.2 imbalance is not well explained by the initial approach distance alone.

## Interpretation

The current Micro-Fighter Pressure policies appear to reliably create **threat volume**:

`space compression -> in-range attack opportunity -> defensive-response forcing`

But threat volume is not sufficient for victory. Family A Control demonstrates a counterexample: it can absorb/punish that pressure and reverse the damage outcome.

The most prospectively justified v0.4 engineering question is therefore not "reduce forward movement until win rates balance." It is to examine **threat conversion and defensive counter-value**—especially why Family A Control turns Pressure's high threat exposure into a losing exchange while Family B Control does not.

No PCC construct-recovery claim follows from this diagnostic.
