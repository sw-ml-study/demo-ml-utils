# Bandit History Contract

`just bandit-contract` validates a deterministic two-arm, four-round fixture
with source task IDs `401`–`402` and disjoint held-out ID `501`. Histories carry
actions, observations, rewards, cumulative rewards, and regret.

Fixed greedy chooses arm 0, earns zero, and accumulates regret 4. Deterministic
UCB1 explores each arm, then earns three rewards with regret 1. Both are tagged
`programmed-baseline` with `icrl_claim: 0`: explicit adaptive algorithms are not
a trained frozen history-conditioned policy and are not labeled ICRL.

MLPL owns validation, policy execution, tape lookup, metrics, budgets, and
tagged JSON. Native code supplies bounded I/O and numeric primitives. This tiny
deterministic contract is not a stochastic benchmark or production evaluation.
