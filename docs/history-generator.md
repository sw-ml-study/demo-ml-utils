# Source Bandit History Generator

`just history-generator` runs deterministic UCB1 on the two source tasks only.
Task 401 learns arm 0 with actions `[0,1,0,0]`; task 402 learns arm 1 with
`[0,1,1,1]`. Each earns three rewards with regret one.

The report retains actions, rewards, cumulative reward/regret, source task IDs,
reward tapes, generator identity, and explicit held-out task IDs. Task 501 is
never evaluated during generation. Task, record, history, reward, JSON, and
output budgets fail closed.

These are offline source-learner histories, not ICRL. The next step may train a
history-conditioned policy from them; only later can a frozen policy adapt from
held-out reward context at deployment.
