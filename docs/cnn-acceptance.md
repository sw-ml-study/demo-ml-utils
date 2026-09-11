# Convolution-from-equations acceptance

Status: accepted. Six rungs are runnable in the default gate on stable
`mlpl-repl 0.22.0`, build `4ca2a6ba`.

```sh
just cnn-ladder      # the six rungs, narrated
just cnn-contract    # the executable contract
just cnn-formula     # equation provenance
```

## What each rung proves

| Rung | Claim | Evidence |
|---|---|---|
| 1 `01_dot_product` | One summation is one reduction | `1*4 + 2*5 + 3*6 = 32`, asserted |
| 2 `02_convolution_1d` | A shifted index is a windowed axis | A first-difference kernel on a ramp gives `-2` at all six positions |
| 3 `03_convolution_2d` | Two summations are one reduction over two axes | The hand-computed `-6` edge response at every valid cell |
| 4 `04_multichannel_convolution` | Three summations are one reduction over three axes | Four spellings bit-identical; `conv2d` parity |
| 5 `05_convolution_layer` | `conv2d` is not magic | Pre-activation equals oracle plus bias; `relu` clears 12 negatives |
| 6 `06_learned_kernel` | The contraction is differentiable | Teacher kernel recovered to 1.9e-9, and a case where it is not |

Rung 4 is the payload. It expresses one contraction four ways — the nested
transliteration, the collapsed multi-axis reduction, reduction by axis name,
and im2col `matmul` — and proves all four produce identical results.

## Oracle policy

`conv2d` is an independent oracle, never an implementation. Agreement is
asserted at two different standards, and the difference is deliberate:

- **Integer inputs: exact.** Maximum absolute difference 0.
- **Float inputs: a stated 1e-9 tolerance.** Observed 1.4e-14. Three chained
  reductions accumulate in a different order from one fused builtin, so
  bit-exactness is not claimed. The im2col spelling contracts in one `matmul`
  and does agree exactly, which is reported as a property of that spelling
  rather than generalized.

An earlier draft of this repository's documentation claimed a 172x performance
deficit against `conv2d`. That figure described one broadcast workaround, not
the language, and was withdrawn: the im2col spelling runs at 1.198 ms against
`conv2d` at 1.230 ms on an `[8,32,32]` input with `[16,8,3,3]` filters.

## Adversarial and boundary cases

Each fails closed with a named error, asserted in `tests/cnn-convolution.mlpl`:

| Case | Behavior |
|---|---|
| Window larger than the input | `Err` — conv window is larger than the input it slides over |
| Rank-2 input where rank-3 required | `Err` — names the expected shape |
| Rank-2 kernel where rank-3 required | `Err` — names the expected ranks |
| Unknown axis name | `Err` naming the axis and the available labels |
| Window exactly the input size | **Succeeds** with one output position; a boundary, not an error |

Gradient correctness is verified against central differences rather than
assumed from a plausible shape, with a guard rejecting an all-zero gradient
that would satisfy the comparison vacuously.

## Determinism

`just cnn-ladder` produces byte-identical output across runs. All fixtures are
generated in-source from `range` and seeded `randn`; nothing is read from disk
and no model is downloaded.

## The capability trail

These demos were the forcing function for six upstream gaps, recorded in
[the blocker record](sw-mlpl-blocker.md) and gated by `catalog/probes.tsv`
through `just array-capabilities`.

| Gap | State |
|---|---|
| C1 general sliding windows | shipped |
| C2 trailing-axis rank broadcasting | shipped |
| C3 multi-axis reduction | shipped |
| C4 reduction over a vector of axis *names* | **open**, `LIBRARY_GAP` closed downstream |
| C5 `compress` preserving axis labels | shipped |
| C6 broadcast backward on the autograd tape | shipped |

C4 is worked around by `u:conv_axis_indices`, which resolves labels against
`labels(x)` and passes the integer vector `reduce` already accepts. Because it
is expressible in ordinary MLPL it is not a language blocker, and this
repository no longer requests it as a prerequisite.

The probe gate fails closed in both directions: a capability *appearing* is
drift needing reconciliation, not good news to absorb quietly. It caught every
one of C2, C3, and C6 landing, and twice caught probes of mine that pinned a
weaker proxy than the requirement and so went green while the thing actually
wanted still failed.

## Attribution

Zhao, Y.; Wang, D.; Wang, L.; Liu, P. "A Faster Algorithm for Reducing the
Computational Complexity of Convolutional Neural Networks". *Algorithms* 2018,
**11**(10), 159. DOI `10.3390/a11100159`. CC BY 4.0.

**Only Section 2.1, Equation (1) is implemented** — the definition of a
convolutional layer output. The paper's actual contribution, an algorithm
combining Winograd minimal filtering with the Strassen algorithm reported to
save 75% of VGG runtime, is **not implemented here** and no demo implies
otherwise.

The equation was verified by reading the paper directly, not from the
discussion transcript that prompted this work. That reading settled four things
that had been assumed: the limits are 1-based; the kernel is unflipped, so
Equation (1) defines cross-correlation; the equation contains no bias or
activation; and the paper reserves uppercase `X`, `Y`, `W` for whole feature
maps.

## Limitations

- **Teaching scale.** Inputs are at most `[8, 32, 32]`. No claim is made about
  large images, batching, or accelerator execution.
- **Forward and single-kernel training only.** Rung 6 recovers one kernel by
  gradient descent. This is not a trained network, and there is no
  multi-layer backpropagation demo.
- **Stride and padding are fixed at 1 and 0.** The `windows` builtin accepts
  strides; the demos do not exercise them.
- **Cross-correlation, not flipped-kernel convolution.** Named rather than
  inherited silently, per [the notation rules](math-notation.md).
- **Rung 6's recovery is conditional.** On a linear ramp the loss reaches
  3.9e-19 while the kernel is wrong by 1.13, because the receptive fields are
  linearly dependent. This is kept in the demo deliberately: low loss is
  evidence about the data fitted, not proof of recovering the function behind
  it.
