# Effective Chaos validation protocol (v0.9.0)

Status: **frozen before the default evaluation**.

## Purpose

Test whether a spatial-combat Chaos candidate can be distinguished from both
(1) a predictable competent policy and (2) a state-aware random policy.

The experiment treats **Chaos as distinct from randomness**. High action entropy
is necessary evidence of unpredictability, but it is not sufficient. A Chaos
candidate must also preserve competitive value and resist a fixed adaptive
exploiter.

## Policies

The experiment defines four new evaluation-only policies. They do not modify the
frozen Pressure/Control/Chaos policies used by prior releases.

- `predictable_competent`: simple, low-entropy state-competent baseline.
- `state_random`: state-aware random baseline.
- `effective_chaos`: value-bounded diversified policy with anti-repeat behavior.
- `adaptive_exploiter`: fixed public-history transition learner used only as an opponent.

No policy is tuned after the default evaluation is observed.

## Design

For each focal policy (`predictable_competent`, `state_random`, `effective_chaos`):

1. play 400 matches per player order against the existing neutral baseline;
2. play 400 matches per player order against the fixed adaptive exploiter;
3. balance both player orders;
4. use deterministic fresh seeds beginning at 97001.

No human data are involved.

## Measurements

- `conditional_action_entropy`: normalized first-order conditional entropy of the
  focal policy's actions, in [0, 1].
- `neutral_decisive_win_rate`: focal decisive win rate against neutral.
- `neutral_mean_health_margin`: focal final health minus opponent final health.
- `exploiter_decisive_win_rate`: focal decisive win rate against adaptive exploiter.
- `exploiter_mean_health_margin`: focal final health minus exploiter final health.
- `exploitability_health_loss`: neutral mean health margin minus exploiter mean
  health margin. Lower values indicate less exploitable performance degradation.

## Prespecified checks

The effective-Chaos candidate passes only if all checks hold:

1. **unpredictability**: conditional entropy is at least 0.10 above the predictable baseline;
2. **value over randomness**: neutral health margin is at least 0.50 above the random baseline
   OR neutral decisive win rate is at least 0.10 above the random baseline;
3. **adaptive resistance**: exploitability health loss is at least 0.25 smaller than the
   predictable baseline's loss;
4. **non-random adequacy under exploitation**: exploiter health margin is at least 0.50
   above the random baseline OR exploiter decisive win rate is at least 0.10 above random.

A random policy can therefore have maximal entropy and still fail.

## Interpretation boundary

Passing supports a game-specific **effective unpredictability** mechanism in this
synthetic micro-fighter. It does not establish a universal Chaos scalar, human
construct validity, or the poker dominance cycle.

Failure is retained as evidence. The thresholds and policies are not changed in
this release after the frozen default evaluation.
