# Retreat-backfire decomposition protocol (v0.8.0)

## Question

Why did the prospectively frozen v0.7 Family B Control recovery rule worsen the Pressure-vs-Control matchup relative to the accepted v0.5 Control policy?

This experiment is diagnostic only. It does not change any policy, engine rule, damage value, arena geometry, or competitiveness threshold.

## Frozen comparison

The same Family B Pressure policy is compared against:

- **v0.5 Control comparator:** the v0.5 punish-window rule, without the later sustained-threat recovery rule.
- **v0.7 Control target:** the current policy containing both the v0.5 punish rule and the rejected v0.7 sustained-threat rule.

Both player orders are balanced and the same seed schedule is used.

## Prespecified mechanisms

1. **Initiative forfeiture.** At v0.7 retreat-trigger events, estimate how often a close-range attack opportunity was plausibly available rather than retreat being the only useful action.
2. **Free re-entry.** After retreat genuinely increases distance, measure whether Pressure immediately advances back into threat range on the next tick.
3. **Boundary / resolution saturation.** Measure retreat attempts that fail to increase distance at all.
4. **Defensive displacement persistence.** After retreat gains distance, measure whether separation remains above attack range for the following two ticks.

The diagnostic thresholds are descriptive and fixed before evaluating the default run:

- initiative-forfeiture proxy rate >= 0.50;
- immediate free re-entry rate given successful distance gain >= 0.25;
- ineffective-retreat rate >= 0.20;
- two-tick displacement persistence given successful distance gain < 0.50.

No single mechanism is required to explain the entire win-rate regression. Multiple mechanisms may coexist.

## Scientific boundary

This test is about whether spatial Control in a minimal fighting environment is better characterized as **value-sensitive regulation of initiative and distance** rather than simple movement away from threat. It is not a claim that PCC is validated in fighting games.
