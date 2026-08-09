# Frozen-Base Low-Rank Adapter

`just low-rank-adapter` demonstrates the mechanism behind low-rank
parameter-efficient adaptation on a tiny inspectable model. It is motivated by
[LoRA](https://arxiv.org/abs/2106.09685), but it is not production-scale LLM
fine-tuning and does not claim LoRA framework compatibility.

The model maps bias-augmented `[1,x1,x2]` inputs to two outputs `[y,-y]`.
Its frozen base is a 2x3 zero matrix with six parameters. A rank-one update is
factored as `delta = B*A`, where B is 2x1 and A is 1x3. Five factor values are
trainable; the six base values remain byte-for-byte equivalent under the
contract's canonical fingerprint.

MLPL explicitly applies the chain rule. For the loss gradient with respect to
the merged update `G = dL/ddelta`:

```text
dL/dB = G * transpose(A)
dL/dA = transpose(B) * G
```

The demo starts B at `[0.1,-0.1]` and A at `[0.5,0.5,0.5]`, then performs 126
batch updates at learning rate `0.05` before reaching tolerance. The merged
matrix becomes approximately:

```text
 1.0052   1.9954   2.9962
-1.0052  -1.9954  -2.9962
```

Training MSE falls below `0.00001` and held-out MSE below `0.00006`.
Factorized inference `X*base^T + (X*A^T)*B^T` is compared with merged inference
`X*(base+B*A)^T` on training and evaluation examples. Both parity errors must
remain within the configured floating tolerance.

The implementation accepts rank one or two. For this deliberately tiny base,
rank one trains five versus six full parameters—a reduction of only one—and
stores eleven values including the frozen base. Rank two trains ten values and
is less parameter-efficient than full tuning. The demo prints this counter-
example rather than implying low rank is automatically smaller; LoRA's strong
efficiency appears for large matrices where `r*(input+output)` is far below
`input*output`.

MLPL owns target design, factor validation/accounting, delta and merge,
manual gradients, optimization, stopping, fingerprints, parity, held-out
evaluation, budgets, and tagged report validation. Native code supplies
bounded dataset I/O, numeric/matrix primitives, and generic JSON.

Ranks, base/adapter parameters, design elements, learning rate, steps,
iterations, gradient/parameter/loss magnitude, parity, curve points, JSON, and
output are bounded. Logical work for N examples, input I, output O, rank R,
and U updates is O(U*N*(I*O + R*(I+O))); all teaching data, factors, curves,
predictions, and reports coexist in memory.
