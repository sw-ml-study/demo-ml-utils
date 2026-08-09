# Held-Out Frozen-Policy ICRL Rollout

`just icrl-rollout` uses the source-trained frozen artifact on held-out task
501. After explore-each-arm actions `[0,1]`, growing reward difference makes the
policy choose arm 1 twice more: total reward 3, regret 1.

Empty and reward-ablated context instead produce `[0,1,0,0]`, reward 1, and
regret 3. Shuffling is invariant because this teaching policy uses cumulative
reward difference rather than order. Exact fingerprints prove zero deployment
parameter updates; held-out records used during offline training remain zero.

This demonstrates bounded reward-context adaptation by a frozen distilled
policy. It is not a transformer, LLM, or claim that order never matters in
production ICRL.
