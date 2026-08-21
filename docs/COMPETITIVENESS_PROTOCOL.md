# Frozen competitiveness protocol — v0.2.0

## Purpose

Before construct-recovery experiments, test whether the provisional synthetic mechanisms are usable as a comparison laboratory rather than trivially dominated caricatures.

This is **not** a PCC confirmation test and does **not** require a rock-paper-scissors dominance cycle.

## Independent policy families

- **Family A** preserves the compact conditional policies introduced in v0.1.0.
- **Family B** is independently structured around scored actions, recent-transition responses, and value-bounded anti-repeat diversification. Family B does not call, subclass, or parameterize Family A policies.

The shared game engine and legal action set are intentionally identical.

## Frozen evaluation

For each family separately, evaluate:

- Pressure vs Control
- Pressure vs Chaos
- Control vs Chaos

Each matchup is run in both player orders with fresh deterministic seeds. Draws are reported separately. The competitiveness criterion uses decisive matches only.

A matchup is competitive when either named side has a decisive win rate in the interval **[0.30, 0.70]**. Because the opposite side is `1 - rate`, this is symmetric.

The whole protocol passes only if all three matchups pass in **both** independently coded families.

## Non-goals

The protocol does not:

- require a particular winner in any matchup;
- require Pressure → Chaos → Control → Pressure;
- tune policies after observing the frozen run;
- claim construct validity from competitiveness alone.

A failure is retained as evidence that the corresponding synthetic laboratory is not yet balanced enough for confirmatory construct recovery.
