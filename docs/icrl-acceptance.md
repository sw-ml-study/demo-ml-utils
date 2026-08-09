# ICRL Acceptance Report

`just icrl-acceptance` closes the bounded ICRL saga. It emits versioned
`sw-ml-study.icrl-history-ir` evidence for canonical, empty-context, shuffled,
and reward-ablated held-out rollouts. Each carries aligned actions, rewards,
features, probabilities, context lengths, cumulative reward, and regret.

Acceptance requires byte-identical rebuilds, exact canonical actions and reward,
zero held-out offline records, identical deployment fingerprints, and zero
deployment updates. It rejects malformed/non-finite data and exhausted round or
output budgets. Atomic publication verifies exact bytes and parsed semantics;
pre-write failure preserves the destination.

Native code supplies bounded I/O, numeric primitives, tagged JSON, and atomic
replacement. MLPL owns source training, frozen rollout, controls, metrics, IR,
budgets, and semantic acceptance. Optional external LLM corroboration is not a
default dependency or acceptance authority.

This proves the tiny deterministic mechanism, not transformer/LLM behavior,
provider reproducibility, privacy, or general bandit performance.
