# Split and Lift-Inspired Grouped Learning

Run `just split-lift` to compare one global mean-offset model with one fitted
model per region. Region 1 has offset 2 and region 2 has offset 8. Their
held-out inputs are both 10, so the correct targets are 12 and 18.

Split is demonstrated by explicit train/evaluation identities and a leakage
check before fitting. Lift is demonstrated operationally: the same fitting
computation is applied once per group, producing aligned group parameters.
The global model learns offset 5 and predicts `[15, 15]` (MSE 9); grouped
models learn `[2, 8]` and predict `[12, 18]` (MSE 0).

The demo first fits both groups explicitly, then uses a bounded `sl_fit_all`
helper and proves exact parameter/prediction parity. The helper is intentionally
called grouped fit rather than `experiment.lift`: its concrete name explains
what it does, while a generic Lift wrapper has not yet earned enough reuse to
improve the MLPL program.

All fitting and evaluation are pure MLPL. Empty groups, duplicate or leaking
IDs, misaligned columns, unknown evaluation groups, and resource-budget
violations fail closed. No cross-repository blocker was found.
