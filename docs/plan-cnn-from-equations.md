# Plan — convolution from equations

## The demo

A five-rung ladder that carries one published equation down to executable MLPL
and back up to a native oracle, showing at each rung that the mathematics and
the code are the same object.

```text
demos/cnn/
    01_dot_product.mlpl            y = sum_i w_i x_i
    02_convolution_1d.mlpl         y_x = sum_u w_u x_{x+u}
    03_convolution_2d.mlpl         y_{x,y} = sum_u sum_v w_{u,v} x_{x+u,y+v}
    04_multichannel_convolution.mlpl   the Zhao et al. triple sum
    05_convolution_layer.mlpl      Y = relu(W * X + b), checked against conv2d
```

The source equation is Zhao, Wang, Wang & Liu, "A Faster Algorithm for Reducing
the Computational Complexity of Convolutional Neural Networks" (2018), §2.1:

$$ y_{r,x,y} = \sum_{q=1}^{Q} \sum_{u=1}^{M_w} \sum_{v=1}^{N_w}
   w_{r,q,u,v}\; x_{q,x+u,y+v} $$

Rung 4 is the payload. Rungs 1-3 exist so that the reader arrives at it already
knowing that a summation is a reduction, and rung 5 exists so the reader leaves
knowing that `conv2d` is not magic.

Each rung shows the same computation three times: the equation, the mechanical
transliteration (one nested `reduce` per sigma), and the array-oriented
collapse (one reduction over three axes). The point of the third form is that
the three sigmas were never three concepts.

## Why this is honest

Every rung is checked two ways.

- **Against arithmetic.** The 4x4 ramp and vertical-edge kernel from the
  research note produce -6 at the upper-left output cell by hand. The demo
  asserts that value.
- **Against the native oracle.** `conv2d(input, filters, stride, padding)`
  already exists in MLPL and is not used to implement anything here. It is an
  independent implementation, so agreement is evidence rather than tautology.

Both checks were run during planning on `mlpl-repl 0.21.0` build `7a9c4ceb`.
A `[2,5,5]` input against `[3,2,2,2]` filters reproduces `conv2d` exactly
(max absolute difference 0), and an `[8,32,32]` input against `[16,8,3,3]`
filters agrees to 1.42e-13. The float residual is float accumulation order, and
the demo reports it as a tolerance rather than claiming bit-exactness.

An earlier draft of this plan reported a 172x runtime gap and 1,036,800 cells
of replicated kernel. Both figures came from a `table`-tiling workaround and
were wrong about the language. The im2col spelling —
`matmul(reshape(windows(x, [kh, kw]), [oy * ox, c * kh * kw]), flatten(kernel))`
— runs in 1.198 ms against native `conv2d` at 1.230 ms on the same
`[8, 32, 32]` case, replicates nothing, and agrees exactly rather than to a
tolerance.

The demo therefore has no performance apology to make. It reports the cost of
each spelling honestly, including the slow one, because the difference between
them is itself instructive: three chained reductions accumulate differently
from one `matmul` contraction, which is why only the latter is bit-exact.

## Rendering the mathematics

The math has to survive four destinations, and no single notation serves all
four. The demo carries it in one place and derives the rest.

**Source of truth: the `@formula` annotation.** MLPL preserves arbitrary
`@word` annotations as data readable through `annotations(name)`, verified
during planning:

```mlpl
@formula "y[r,x,y] = \\sum_q \\sum_u \\sum_v W[r,q,u,v] X[q,x+u,y+v]"
@ascii   "y[r,x,y] = SUM_q SUM_u SUM_v W[r,q,u,v] * X[q,x+u,y+v]"
def u:cnn_cell(kernel, patch) {
    "Contract one kernel against one patch.";
    reduce(:add, kernel * patch)
}
```

The LaTeX round-trips intact. Because it lives next to the implementation and
is readable at runtime, the equation cannot silently drift from the code, and
the demo can print both together as its own evidence of correspondence.

**Terminal output: Unicode, not LaTeX.** A UTF-8 terminal renders
`y[r,x,y] = Σ_q Σ_u Σ_v  W[r,q,u,v] · X[q,x+u,y+v]` correctly, verified from
MLPL `print`. Bracket-index notation is used rather than typeset subscripts,
because bracket indices are what the array language actually does — the
notation degrades toward the code rather than away from it. The `@ascii`
annotation is the fallback for a terminal that cannot render `Σ`.

**Documentation: GitHub LaTeX.** GitHub markdown typesets `$$...$$` natively,
so `docs/` uses the paper's own notation, as this file does above. No build
step, no checked-in images.

**Web viewer: typeset from the IR.** Upstream `sw-mlpl` already ships an
MLPL-expression-to-LaTeX converter feeding MathJax for its 3D inspector's
derivation view (`pages/js/derivation_latex.js`), and this repository already
has the renderer-neutral scene IR and dependency-free `viewer/` client from
Saga 4. The formula string rides in the scene IR as a field and the client
typesets it. This needs no upstream language work and reuses two existing
mechanisms.

Pre-rendered images checked into `docs/` are explicitly rejected. This
repository's demos are self-checking, and a static PNG of an equation is the
one artifact in the pipeline that cannot be verified against the code it
claims to describe. An optional upstream `svg(formula, "formula")` renderer
would be a nicer fifth destination, but it is a convenience, not a blocker, and
it is not requested in [the blocker record](sw-mlpl-blocker.md).

## What blocks the readable version

The demo is implementable today and was prototyped end to end. What is missing
is the ability to write it so that it reads like the equation, which is the
entire thesis. Five expressiveness gaps are pinned by probes and specified in
[the blocker record](sw-mlpl-blocker.md): a general sliding-window
rearrangement, trailing-axis rank broadcasting, multi-axis reduction,
named-axis parity for higher-order `reduce`, and a label-dropping defect in
`compress`.

The target line the demo is written toward is:

```mlpl
y = reduce(:add, windows(x, [kh, kw]) * w, ["channel", "kernel_y", "kernel_x"])
```

against what the same computation currently requires:

```mlpl
p     = u:windows3d(x, kh, kw);                       # 25 lines of scaffolding
tiled = reshape(table(:mul, ones([oh * ow]), flatten(k)), [oh, ow, c, kh, kw]);
y     = reduce(:add, reduce(:add, reduce(:add, p * tiled, 4), 3), 2)
```

Both versions ship. The scaffolded one is the current implementation; the
target one is the documented goal, and each rung is rewritten as the
corresponding capability lands. The gap between them is itself the demo's
argument for why the language work matters, so the scaffolding is retained as
an exhibit rather than deleted.

Upstream has scheduled the five gaps across four phases, so the rewrite is
staged rather than a single flip. C5 and C1 shipped together in commit
`476e9bf4`: labeled trimming no longer needs a `relabel`, and the 25-line
window construction is now one `windows` call. C3 and C4 collapse the nested
reduces to one named-axis reduction; C2 removes the kernel replication.

All five rungs, including the weighted triple sum, are implementable at
`476e9bf4`. C2 and C3/C4 change how they read, not whether they run. Phase
state is pinned by build commit rather than version string, because C5 shipped
inside 0.21.0 rather than the scheduled 0.21.1, and commit `476e9bf4` was
released as 0.22.0 and then backed down with identical content. The headline
line needs C1 through C4 together, so the demo reaches its target spelling when
Phase 4 lands. The phase-to-probe mapping and the commit-pinning rule are
recorded in [the blocker record](sw-mlpl-blocker.md).

## Positioning

### Against the other repositories

`demo-linear-algebra` owns the mathematical curriculum — vectors, matrices,
factorizations, PCA, least squares — and `demo-ml-microscope` owns lesson
timelines of intermediate values. Convolution touches both, and the question of
where it belongs is real.

It belongs here because of what it is checked against. In
`demo-linear-algebra` a convolution lesson would be verified against
arithmetic, and would be one more entry in a curriculum that already runs from
LA01 to LA20. Here it is verified against `conv2d` and, more importantly,
against the tensors this repository already reads out of real files. That is a
different claim, and it is this repository's claim.

If a broader convolution curriculum is wanted later — separable kernels,
dilation, transposed convolution, pooling arithmetic — that is
`demo-linear-algebra` or a future `demo-signal-processing`, and this demo is
its executable prerequisite rather than its competitor.

### Against the other demos in this repository

Every existing demo here works from the outside in. `safetensors-catalog` names
tensors, `gguf-slice` decodes their bytes, `simple-q4` quantizes their values,
`tensor-city` renders their shapes, `checkpoint-to-safetensors` moves them
between containers. All of it is correct and none of it ever asks what the
numbers compute. A `[16, 8, 3, 3]` tensor is, to every current demo, a shape and
a byte range.

This demo says what that shape means. It is the first one where the catalog's
`[C_out, C_in, kH, kW]` stops being metadata and becomes an operator contracted
against a patch. That completes the repository rather than extending it
sideways, and it does so at the same teaching scale and with the same
self-checking standard as the rest.

Three concrete compositions follow, and they are the reason this is a
`demo-ml-utils` demo rather than a curriculum lesson:

- **Quantization gets a semantic error metric.** `simple-q4` and
  `symmetric-roundtrip` currently report RMSE, maximum error, and cosine on raw
  tensor values. None of those answers the question a practitioner actually
  asks, which is how much the layer's *output* moves. Running a real conv layer
  before and after quantizing its kernel converts a numeric error into an
  observable output drift. That measurement is not available anywhere in the
  repository today.
- **Visualization gets an operator to show.** The scene IR renders
  distributions and surfaces of tensor values. A conv kernel has structure —
  edge detectors, blur kernels — that a histogram cannot show and a patch
  contraction can.
- **The format demos get a payoff.** Reading a conv kernel out of a real
  Safetensors or GGUF file with the existing bounded readers and running it as a
  layer closes the loop from byte range to arithmetic, using only demos that
  already exist.

The demo is nonetheless standalone and deterministic on generated fixtures, per
repository rules. The compositions above are follow-on steps, not
prerequisites, and none of them may be claimed until they are runnable.

### What this demo must not claim

- It is not a CNN implementation or a training path. It is also not a
  performance claim in either direction: the im2col rung matches `conv2d` on
  the measured case, which is reported as one measurement on one shape, not as
  a general benchmark.
- It does not claim `conv2d` is unnecessary. It uses it as the oracle.
- It does not claim large-input support. Budgets are teaching-scale and the
  memory cost of the broadcast workaround is reported, not hidden.
- It does not claim to be the paper's contribution. Zhao et al. describe a
  *faster* algorithm; this demo implements only their §2.1 definition, and the
  attribution says which part is used and which is not.

## Saga shape

Proposed as Saga 13, after the active Agentrail sagas close. Six steps:

1. `convolution-capability-probes` — pin C1-C5 as probes with catalog entries,
   and record the measured broadcast and runtime costs.
2. `reduction-ladder` — rungs 1-3, hand-checked goldens, both spellings.
3. `multichannel-convolution` — rung 4 against the `conv2d` oracle, with the
   axis-label version and the tolerance policy.
4. `convolution-layer` — rung 5 with bias and activation, plus `pool2d`
   agreement if the shape arithmetic stays honest.
5. `formula-provenance` — `@formula` round-trip, terminal and IR rendering, and
   the scene-IR formula field consumed by `viewer/`.
6. `cnn-acceptance` — adversarial shapes, budget failures, attribution,
   limitations, catalog and documentation updates, and the reconciliation rule
   that rewrites each rung as C1-C5 land.

Gate: open. No upstream capability is required to start, because the demo runs
today. The blocker record governs how each rung is rewritten, not whether the
saga can begin.

Two adjacent items stay outside this saga. Trainable convolution, unlocked by
the upstream `autograd(windows)` work at 0.24.0, is a separate saga with its
own evidence obligations — finite-difference gradient checks, a training
trajectory, a stopping rule — and is gated on this forward ladder being
accepted first. A live-site convolution page is a rendering target for the
accepted `demos/cnn/` sources, not a second implementation of them; the
ownership boundary is argued in the blocker record and needs an explicit
decision before upstream Phase 6 starts.
