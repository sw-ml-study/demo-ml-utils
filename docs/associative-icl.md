# Frozen Associative ICL

`just associative-icl` demonstrates inference-time adaptation without parameter
updates. The frozen deployment vector `[1,0,0]` supplies a bias-only baseline.
For query `q`, context input `x`, label `y`, and frozen prediction `f(x)`, the
teaching mechanism adds `dot(q,x) * (y-f(x))`.

Zero-shot predictions `[1,1,1]` have MSE `152/3`. The first context example
identifies only the x1 residual and produces `[5,1,5]` at MSE 24. Adding the
orthogonal x2 example produces `[5,7,11]` at MSE zero. Printed similarity and
contribution matrices explain every term; exact before/after fingerprints prove
the deployment vector never changes.

MLPL owns the kernel, residual composition, predictions, loss, fingerprints,
budgets, and deterministic report. Native code supplies bounded I/O, numeric
arrays, and generic JSON. Context/query counts, association work, similarity,
contribution, prediction, source/report bytes, and JSON complexity are bounded.

This is not transformer self-attention, tokenization, learned key/query/value
projections, a language model, or evidence of production ICL quality. It is a
small inspectable example of outputs changing from context while parameters do
not—the defining distinction this saga needs to demonstrate.
