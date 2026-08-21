# Pressure dominance decomposition protocol

## Question

Why do the frozen v0.2.0 Pressure policies dominate large parts of the Micro-Fighter competitiveness grid?

This is a diagnostic experiment. It does **not** rebalance the policies and does not test PCC construct recovery.

## Frozen candidate mechanisms

For Pressure versus Control and Pressure versus Chaos, separately in policy Families A and B, measure:

1. **Space capture** — distance reduction attributable to ticks on which the focal fighter chose `advance`.
2. **Attack-opportunity generation** — rate of focal `attack` actions executed at distance <= 1 after simultaneous movement.
3. **Defensive-response forcing** — probability that the opponent chooses `guard`, `evade`, or `retreat` on the tick immediately following a focal `advance` or `attack` threat.
4. **Damage conversion** — net damage and damage per threat tick.

All comparisons use both player orders and fresh deterministic seeds. The v0.2.0 policies are frozen.

## Compact-arena diagnostic

The same policy matchups are replayed on arena `[0, 3]`, where starting positions are adjacent (distance 1). This removes most of the initial approach problem without changing policy code or combat rules.

A reduction in Pressure win rate under this replay is evidence that access to/creation of close range contributes to the original advantage. It is not by itself a causal estimate of a single mechanism because policy state visitation also changes.

## Interpretation rule

This protocol does not declare a new PCC confirmation. Candidate mechanisms are called *directionally replicated* only when Pressure's metric exceeds its opponent's against both Control and Chaos in both independently coded policy families. Nulls and family splits are retained.
