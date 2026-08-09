# Manual Linear Fine-Tuning

`just linear-fine-tune` demonstrates actual parameter-updating adaptation on
the deterministic dataset from the [shared adaptation contract](adaptation-contract.md).
Four training examples follow `y = 1 + 2*x1 + 3*x2`; three disjoint held-out
examples test whether the learned rule generalizes.

The model has three parameters: bias, weight 1, and weight 2. Starting at
`[0,0,0]`, MLPL explicitly computes predictions, errors, mean squared loss,
and the batch gradient:

```text
dL/db   = 2 * mean(error)
dL/dwj  = 2 * mean(error * xj)
theta'  = theta - learning_rate * gradient
```

With learning rate `0.2` and 60 updates, the parameters become approximately
`[1.0272,1.9780,2.9762]`. Training MSE falls from `15.5` to about `0.000281`.
The no-training held-out baseline predicts `[0,0,0]` with MSE `65`; the tuned
model predicts close to `[5,7,11]` with MSE about `0.00162`. The demo prints
selected loss and gradient-norm points so the trajectory, not merely the final
score, is visible.

The run schema is `sw-ml-study.linear-fine-tuning`, version 1. It records
initial/final parameters and fingerprints, all losses and gradient norms,
targets and before/after predictions, update count, learning rate, tolerance,
stopping reason, dataset summary, and implementation attribution. Here the run
stops at `max_steps`; tolerance stopping is an explicit alternative.

MLPL owns the model, squared objective, manually derived gradients, optimizer,
stopping policy, held-out comparison, fingerprints, budgets, and report
round-trip. Native code supplies bounded dataset I/O, numeric array primitives,
and generic JSON. No autodiff, external framework, GPU, or model runtime is
used.

Learning rate, requested steps, iterations, predictions, gradients,
parameters, loss, curve points, dataset size, fingerprint, JSON elements, and
output bytes are bounded. Non-finite/over-budget intermediate values fail.
Tests reject an excessive learning rate before updates, wrong parameter shape,
and insufficient step/iteration/parameter/curve/output budgets.

For N examples, F features, and U updates, logical training work is O(U*N*F)
and the retained trajectory is O(U). The complete tiny dataset, parameters,
loss curve, gradients, predictions, JSON, and decoded report coexist in memory;
this is an inspectable teaching demo, not large-model fine-tuning.
