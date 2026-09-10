# sw-MLPL array-expressiveness blocker record for convolution from equations

## Status

Partially shipped on build `2b365ab1`. C5, C1, and C3 are verified fixed. C2 is
**demoted from a blocker to `ERGONOMICS_ONLY`** (see below). C4 is **reclassified from
`LANGUAGE_EXPRESSIVENESS_GAP` to `LIBRARY_GAP`**: a single axis name is
accepted, a vector of names is not, but the vector form can be built in
ordinary MLPL downstream.

`just array-capabilities` reports the live state, and the same check runs in the
default gate. `catalog/probes.tsv` declares each probe's expected result, so a
capability change fails the gate rather than passing silently. Five gaps are
pinned by executable probes against the configured binary.

Baseline when the gaps were promoted:

```text
mlpl-repl 0.21.0
Commit: 7a9c4ceb
Timestamp: 2026-09-09T13:22:50-0700
```

Binary on which `probes/compress-label-preservation.mlpl` (C5) first exited
zero:

```text
mlpl-repl 0.21.0
Commit: 274c9133
```

Binary on which `probes/sliding-windows.mlpl` (C1) first exited zero:

```text
mlpl-repl 0.21.0
Commit: 7f2c4e99
```

Current pinned binary, carrying C5 and C1:

```text
Commit: 476e9bf4
```

Probe state at this pin: C5 and C1 exit zero, C2/C3/C4 exit nonzero, and
`probes/convolution-reference.mlpl` exits zero.

That bump was premature and was backed down. The dev channel rebuilt the same
content as commit `f4485823`, re-verified here with an identical probe state.
`476e9bf4` is retained above as the commit on which C1 was first observed;
`f4485823` is the build all measurements in this record were taken on.

Upstream separately named `d93592d7` as the commit to pin. The binary available
here resolves to `f4485823`, so this record pins what it actually observed and
measured. The two should be reconciled the next time the local build is
refreshed; probe state is the authority, and `just array-capabilities` reports
it.

Upstream reported the C5 fix as commit `c85cff0d`. The locally built binary
resolves to `274c9133`, which is a later build carrying the fix. This record
pins the commit actually observed, because the version string alone does not
distinguish these builds -- see the pinning rule below.

None of these gaps blocks *correctness*. The planned
[CNN-from-equations demo](plan-cnn-from-equations.md) was prototyped end to end
on this binary and reproduces the native `conv2d` oracle exactly on integer
inputs and to 1.42e-13 on floats. Every gap below is therefore promoted under
the repository's `LANGUAGE_EXPRESSIVENESS_GAP` label, not
`NATIVE_CAPABILITY_GAP`, and one (C5) is an outright defect.

This distinction matters because the demo's entire thesis is that MLPL can
preserve the relationship between a published equation and executable code. A
demo that reaches the right number through twenty-five lines of `rotate`,
`compress`, `concat`, `reshape`, and `transpose_axes` scaffolding disproves its
own claim. Readability *is* the deliverable here, so an expressiveness gap is a
blocking gap, exactly as `docs/sw-mlpl-blockers.md` in `demo-linear-algebra`
requires: a planned lesson that cannot be expressed *readably* with honest
numerical behavior is blocked.

## Owning repository

`../sw-mlpl` must implement every item. It owns array rank and broadcasting
semantics, the reduction builtins, axis-label propagation, builtin
registration, and interpreter/compiler parity. This repository consumes an
explicitly selected `mlpl-repl` binary and does not modify `../sw-mlpl`.

`demo-ml-utils` owns the downstream demos, probes, fixtures, catalog entries,
and acceptance evidence once the capabilities ship.

## The equation under test

Zhao, Wang, Wang & Liu (2018), §2.1, defines one convolutional-layer output as

$$ y_{r,x,y} = \sum_{q=1}^{Q} \sum_{u=1}^{M_w} \sum_{v=1}^{N_w}
   w_{r,q,u,v}\; x_{q,x+u,y+v} $$

The array-language reading is that the three summations are not three
concepts. They are one reduction over three axes of one product. The target
spelling is therefore:

```mlpl
patches = windows(x, [kh, kw])
y = reduce(:add, patches * w, ["channel", "kernel_y", "kernel_x"])
```

Every gap below is a place where current MLPL cannot write that line.

## C1 — general sliding-window rearrangement — SHIPPED

Probe: `probes/sliding-windows.mlpl`, exits zero as of commit `7f2c4e99`.
Behavior when promoted: `error: unknown function: windows`.

### Frozen axis contract

`windows(x, sizes)` emits `[out_y, out_x, C, kh, kw]` — window axes trailing.
A kernel shaped `[channel, kernel_y, kernel_x]` therefore aligns by trailing
position and needs no `transpose_axes`, which is the property that makes the
C2 rewrite a one-line change. Upstream pins this with the test
`multi_channel_2d_lays_out_for_kernel_alignment` so it cannot drift.

Verified downstream against the reference construction on a `[2, 5, 5]` input
with a 3-by-3 window: identical shape `[3, 3, 2, 3, 3]` and max absolute
difference 0, element for element. `probes/convolution-reference.mlpl` encodes
the same ordering and continues to exit zero.

MLPL already ships three special cases of this one rearrangement:

| Builtin | Window shape | Stride | Overlap |
|---|---|---|---|
| `patchify(x, P)` | `P` by `P` | `P` | none |
| `shift_pairs_x(ids, n)` | `n` | `n + 1` | none |
| `conv2d(input, filters, stride, padding)` | `kH` by `kW` | `stride` | yes, but fused into the contraction and not observable |

None exposes an overlapping window *as a value*. The general primitive is what
makes the paper's `x_{q,x+u,y+v}` subscript expressible; without it the
subscript becomes control flow.

A rank-2 `windows` can be assembled today from `rotate` for the shift,
`compress` twice for the valid region, `concat` for accumulation, `reshape`
for the axis split, and `transpose_axes` for the final permutation. The
prototype is 25 lines with a doubly-nested `while`, and it costs
`O(kh * kw)` full-array copies. That is the scaffolding the demo exists to
avoid showing.

Required behavior:

```text
windows(x, sizes[, strides]) -> sliding windows over the trailing axes
```

The contract must define the output axis order, whether window axes are
leading or trailing, stride and dilation defaults, behavior when a window does
not fit, the label assigned to generated axes, and whether the result is a view
or a copy. Acceptance fixtures should cover rank-1 and rank-2 inputs, window
size equal to the axis length, window size larger than the axis (an error, not
an empty result), non-unit strides, and a leading channel axis that is not
windowed.

The same abstraction serves cellular automata, finite-difference stencils,
moving-window statistics, and signal processing, so this is not a CNN
convenience.

## C2 — trailing-axis rank broadcasting — DEMOTED TO `ERGONOMICS_ONLY`

Probe: `probes/rank-broadcast.mlpl`, still exits nonzero. Current behavior:
`error: mul: expected [2, 2, 3, 3], got [3, 3]`.

### Correction: the original cost analysis was wrong

This record first measured C2's cost using a `table`-tiling workaround and
reported a 172x runtime gap against native `conv2d` plus 1,036,800 replicated
f64 cells. Both figures were properties of that particular workaround, not of
the language. Upstream pointed out the im2col spelling, which needs no
broadcasting at all:

```mlpl
cols = reshape(windows(x, [kh, kw]), [oy * ox, c * kh * kw]);
y    = matmul(cols, reshape(kernel, [c * kh * kw]))
```

Measured on build `f4485823`, `[8, 32, 32]` input against `[16, 8, 3, 3]`
filters:

| Form | Time | Replicated cells | Agreement with `conv2d` |
|---|---|---|---|
| `table`-tiling | 211.3 ms | 1,036,800 | 1.42e-13 |
| `matmul` im2col | 1.198 ms | 0 | exact |
| native `conv2d` | 1.230 ms | — | — |

The array path is at parity with the native builtin and is exact rather than
tolerance-bounded, because `matmul` contracts in one pass instead of
accumulating through three reductions.

C2 is therefore not a blocker and never was. It remains worth shipping so the
*mechanical transliteration* rung can be spelled directly, but no rung is
gated on it and no performance claim depends on it. The demo's headline
performance story is parity with `conv2d`, not a teaching-path deficit.

Scalar broadcasting works. Rank broadcasting does not: elementwise operators
require identical shapes. The convolution's shared kernel must therefore be
replicated to full patch shape before multiplication. The working idiom found
during prototyping is an outer product:

```mlpl
tiled = reshape(table(:mul, ones([oh * ow]), flatten(k)), [oh, ow, c, kh, kw])
```

This is unreadable, and on an `[8, 32, 32]` input with `[16, 8, 3, 3]` filters
it materializes 1,036,800 f64 cells of replicated kernel — 8.3 MB — purely to
satisfy a shape rule. But it is one way to write the product, not the only one,
and the correction above shows the im2col spelling avoids the replication
entirely. The cost belongs to this idiom, not to the missing broadcast.

Desired behavior: NumPy/PyTorch-style trailing-axis broadcasting for
elementwise operators, where a size-1 or absent leading axis expands. The
contract must state how axis labels combine when ranks differ, since a labeled
`[out_y, out_x, channel, kernel_y, kernel_x]` meeting a labeled
`[channel, kernel_y, kernel_x]` should align by trailing position and validate
the shared names. Mismatches must keep the existing structured
`ShapeMismatch { op, expected, actual }` diagnostic that renders both labeled
shapes.

Acceptance must cover rank-1 against rank-2, size-1 axes expanding, an
incompatible trailing axis, and a label collision between aligned axes.

## C3 — multi-axis reduction — SHIPPED

Probe: `probes/multi-axis-reduce.mlpl`, exits zero as of build `2b365ab1`.
Behavior when promoted: `error: unsupported: reduce: axis must be a scalar,
got rank 1`. The probe now asserts that the one-call form agrees with nested
single-axis reduction rather than merely running.

```mlpl
reduce(:add, patches, [2, 3, 4])
```

Today the triple sum must be written as three nested calls:

```mlpl
y = reduce(:add, reduce(:add, reduce(:add, weighted, 4), 3), 2)
```

Read outward-in, in reverse order, with bare integers whose meaning depends on
an axis order the reader has to reconstruct. This is the single most direct
loss of correspondence with the source equation, because the equation's three
sigmas are adjacent and order-independent while the code's three calls are
nested and order-dependent.

Required behavior: `reduce(:op, a, axes)` accepting a rank-1 axis vector,
reducing all named axes in one pass, with the result rank reduced by the count
of distinct axes. Duplicate or out-of-range axes must error loudly. The same
extension applies to `reduce_add` and `reduce_mul`.

## C4 — named-axis parity for higher-order reduce — PARTIALLY SHIPPED

Probe: `probes/named-axis-reduce.mlpl`, still exits nonzero.

`reduce(:add, M, "feat")` now works, closing the original single-name
asymmetry. A vector of axis *names* does not:

| Spelling | State |
|---|---|
| `reduce(:add, P, [2, 3, 4])` | shipped with C3 |
| `reduce(:add, P, "channel")` | shipped |
| `reduce(:add, P, ["channel", "kernel_y", "kernel_x"])` | **open** |
| `reduce_add(P, ["kernel_y", "kernel_x"])` | **open** |

### Reclassified to `LIBRARY_GAP`: this repository can fix it

The repository's escalation contract reserves `LANGUAGE_EXPRESSIVENESS_GAP`
for what ordinary MLPL cannot express. Name-to-index resolution is expressible,
so C4 does not qualify. A helper resolves labels against `labels(x)` and hands
`reduce` the integer vector it already accepts:

```mlpl
idx = u:axis_indices(patches, "channel,kernel_y,kernel_x")?;
y   = reduce(:add, weighted, idx)
```

Verified downstream: resolves to `[2, 3, 4]`, agrees exactly with the integer
form, and an unknown name returns
`Err("unknown axis name 'nope' in out_y,out_x,channel,kernel_y,kernel_x")`.

Two constraints shape that helper, both worth reporting upstream as
`ERGONOMICS_ONLY` observations rather than requirements:

- A **string list cannot be a user-defined function parameter**, already noted
  in [the upstream contract](upstream-contract.md). The names therefore arrive
  comma-joined and are split inside.
- **`tally` rejects a string list** (`expected an array value, got a string`),
  so a string list's length cannot be measured. Both walks instead terminate on
  the `Err` from an out-of-range `list_get`. String lists are consequently
  second-class: indexable but not measurable.

Neither blocks the demo. Shipping C4 upstream would still be worth it for
consistency — `reduce_add` and `reduce` should agree, and an axis-name vector
is the spelling the equation deserves — but this record no longer asks for it
as a prerequisite.

### The first version of this probe was wrong

It tested only the single-name form. When that shipped, the gate reported C4
as met while the target line this record actually asks for still failed. The
probe has been rewritten to pin the vector-of-names form.

The lesson generalizes: a probe must encode the requirement, not a weaker
proxy for it, or it will report success at the moment it stops being useful.
Every probe in `catalog/probes.tsv` should be readable as the sentence the
blocker record is asking upstream to make true.

Combined with C3, the target is a rank-1 string vector of axis names:

```mlpl
y = reduce(:add, patches * w, ["channel", "kernel_y", "kernel_x"])
```

At which point the source says *sum over channel, kernel_y, kernel_x* and the
reader never needs to recover what `q`, `u`, and `v` meant. This is the one
place where the MLPL spelling is arguably clearer than the mathematics, which
is the strongest available argument for the language.

Required behavior: every axis argument that accepts an integer must accept an
axis label, and every form that accepts one axis must accept a vector of them.
A name absent from the value's labels must error loudly and name the available
labels.

## C5 — `compress` discards axis labels (defect) — SHIPPED

Probe: `probes/compress-label-preservation.mlpl`, exits zero as of commit
`274c9133`. Behavior when promoted: `rotate` preserved `image_y,image_x` while
`compress` returned `,`. Both now return `image_y,image_x`.

Verified end to end: axis labels survive `rotate` followed by two `compress`
trims, and `reduce_add(trimmed, "image_x")` resolves the name on the result.
The post-trim `relabel` the window construction needed is no longer required.

`compress(mask, a, axis)` removes *slices* along one axis. It changes no axis's
identity or meaning, so labels should survive exactly as they survive `rotate`,
which the probe demonstrates they do. Dropping them looks like an oversight
rather than a decision.

The consequence is concrete: trimming a shifted image to its valid convolution
region erases the very `[image_y, image_x]` names the labeled-axis version of
the demo is built on, forcing a `relabel` after every trim.

Shipped behavior: `compress` propagates the input's axis labels unchanged.
`reshape` clearing labels is correct and separate — it genuinely changes axis
identity, and `reshape_labeled` already covers the deliberate case.

## What is explicitly not requested

- No CNN-specific builtin. `conv2d` already exists and the demo uses it as an
  independent oracle, not as an implementation. Adding `conv3d`, padding
  helpers, or layer sugar would defeat the demo's purpose.
- No native performance work, and no `PERFORMANCE_ONLY` item at all. The
  array-expressed convolution already matches `conv2d` on the measured case
  when written as an im2col `matmul`. An earlier draft of this record claimed
  a 172x deficit; that figure described one workaround and has been withdrawn.
- No autograd extension. The demo is forward-only. Whether `windows` is
  differentiable is an upstream design question, not a downstream requirement.

## Downstream acceptance evidence

| Gap | Probe | Expected once shipped |
|---|---|---|
| C1 | `probes/sliding-windows.mlpl` | **Met at `7f2c4e99`**; matches the `rotate`/`compress` reference construction exactly |
| C2 | `probes/rank-broadcast.mlpl` | Exits zero; product equals the im2col `matmul` reference. Ergonomic only: no rung is gated on it |
| C3 | `probes/multi-axis-reduce.mlpl` | **Met at `2b365ab1`**; asserts equality with nested single-axis reduction |
| C4 | `probes/named-axis-reduce.mlpl` | Exits zero for a vector of axis names; equals the integer-axis form |
| C5 | `probes/compress-label-preservation.mlpl` | **Met at `274c9133`**; labels match `rotate` |

C2, C3, and C4 currently exit nonzero, so an upstream implementation announces
itself by changing the gate. C5 and C1 have flipped. `catalog/probes.tsv`
encodes each expectation and `scripts/check-capability-probes` enforces it in
the default gate, so a flip cannot pass unnoticed in either direction.

## Upstream phased delivery

`sw-mlpl` accepted these gaps and scheduled them as follows. This table is the
reconciliation key: when a release lands, the named probes must flip and the
named rungs are rewritten in the same step.

| Phase | Release | Gaps | Probes flipped | Downstream effect | State |
|---|---|---|---|---|---|
| 1 | `476e9bf4` | C5 | `compress-label-preservation` | Labeled-axis trimming stops needing a `relabel` after every `compress` | **shipped** |
| 2 | `476e9bf4` | C1 | `sliding-windows` | `u:conv_windows` (25 lines) collapses to one `windows` call | **shipped** |
| 3a | `2b365ab1` | C3 | `multi-axis-reduce` | Three nested reduces collapse to one call over `[2, 3, 4]` | **shipped** |
| 3b | optional | C4 | `named-axis-reduce` | That one call takes axis names instead of integers | reclassified `LIBRARY_GAP`; fixed downstream |
| 4 | later | C2 | `rank-broadcast` | The transliteration rung spells its product directly | open, ergonomic |

The demo's headline line needs C1, C2, C3, and C4 together, so it reaches its
target spelling only once Phase 4 lands, not before:

```mlpl
y = reduce(:add, windows(x, [kh, kw]) * w, ["channel", "kernel_y", "kernel_x"])
```

Phases 2 and 3 each remove a distinct piece of scaffolding and are independently
worth rewriting for. Phase 1 is independent of the ladder entirely and should
land whenever it is ready.

### Pin by commit, not by version string

Version labels have moved independently of content twice during this work.

1. C5 was scheduled as 0.21.1 but shipped inside 0.21.0, because patch fixes
   ride the existing version. Two binaries labeled `mlpl-repl 0.21.0` —
   `7a9c4ceb` and `274c9133` — therefore differ in observable array semantics.
2. Commit `476e9bf4` was released as 0.22.0, then the bump was identified as
   premature and backed down to 0.21.x with byte-identical content. The same
   build carries two different version strings over its lifetime.

The first case is one version spanning different behavior; the second is one
behavior spanning different versions. Together they rule the version string out
as an identifier for any capability claim.

Consequently this repository pins the build commit, never the version string,
for every array-expressiveness claim. The phase table above is that pin, and it
names releases only where upstream has actually tagged one. A probe flip must
be recorded here with the commit on which it was observed, in the same step as
the rung rewrite. Probe exit codes, not version numbers, are the authority on
what a given binary can do.

`docs/capabilities.md` covers binary-format capabilities probed by
`just capabilities` and is not the right home for these pins; it is re-pinned
once at Saga 13 step 1, when the C1-C4 probes gain catalog entries.

### Resolved: rung 4 ships now

Upstream twice advised staging the demo as reduce-only patch sums until C2
shipped. That advice is withdrawn and the position is settled: the weighted
convolution runs today, and the im2col spelling above makes it exact and as
fast as the native builtin.

This matters for sequencing. Rung 4, the paper's triple sum, is the demo's
payload; rungs 1-3 exist to reach it. A reduce-only staging would have shipped
a box-filter demo and postponed the equation the demo is named for.

The ladder now ends better than planned, because both spellings are real and
verifiably equal:

| Rung | Spelling | Status |
|---|---|---|
| Mechanical transliteration | nested `reduce` per summation | runs today; C2/C3/C4 improve how it reads |
| Array collapse | one reduction over three axes | needs C3/C4 to spell directly |
| Optimized implementation | `matmul` over im2col columns | runs today, exact, native-speed |
| Native oracle | `conv2d` | independent check |

That is exactly the progression the research note asked for — paper equation,
literal implementation, array-oriented simplification, optimized
implementation — with every step checked against the next.

### Both repositories build convolution demos, deliberately

An earlier version of this section recorded an exclusive ownership boundary —
this repository owning `demos/cnn/` with the live site rendering a vendored
copy. That was proposed here and relayed between agents; the repository owner
did not agree to it, and it is withdrawn.

The settled position is that convolution demos belong in **both** places,
because they answer different questions:

| | `sw-mlpl` live demos and literate docs | `demo-ml-utils` `demos/cnn/` |
|---|---|---|
| Audience | Someone evaluating the language | Someone working with model artifacts |
| Shows | `windows`, `reshape`, `matmul`, `svg` earning their place | What the tensors in a checkpoint actually compute |
| Form | Browser-runnable, literate derivation | Terminal demos in the repository gate |
| Ends at | The im2col one-liner | Quantization drift and kernels read from real files |

Duplication of the equation and the im2col spelling is expected and fine. The
thing to protect is not exclusivity but agreement: both sides use Zhao et al.
(2018) section 2.1, the hand-checked -6 edge-filter cell, and `conv2d` as the
oracle. If those ever disagree, one of them is wrong.
`probes/convolution-reference.mlpl` pins them on this side.

### Phases outside this record

Upstream additionally scheduled two items this repository did not request.

**Phase 5, `autograd(windows)` with a scatter-add backward.** The blocker
record explicitly excludes autograd, because the convolution demo is
forward-only. This is a real capability and a reasonable upstream choice, but it
is not a prerequisite for anything planned here and Saga 13 must not silently
absorb it. A trainable convolution is a different demo with different evidence
obligations — gradient checks against finite differences, a training
trajectory, a stopping rule — and belongs in its own saga, gated on 0.24.0,
after the forward ladder is accepted.

**Phase 6, live-site demos.** A minimal `windows` example such as the moving
average is properly upstream's: it documents the primitive, and the language
reference should carry it. The `convolution-from-the-equation` item is the
overlap. That ladder, its `conv2d` oracle, its hand-checked goldens, and its
attribution are Saga 13's deliverable, and two independent implementations of
it will drift. The boundary this repository proposes is that upstream owns the
primitive's own documentation and any short example of it, and that a live-site
convolution page renders the accepted `demos/cnn/` sources from here rather
than reimplementing them. That keeps one set of goldens and one attribution.
This is a coordination question, not a claim of ownership, and it needs an
explicit decision before Phase 6 starts.

`probes/convolution-reference.mlpl` is the companion known-good result. It
exits zero on the current binary and asserts the hand-checked -6, exact integer
parity against `conv2d`, and float parity inside a stated tolerance, using the
scaffolding each gap forces. It is the reference every "expected once shipped"
row is checked against, and it doubles as the measured record of what the
workarounds cost. The demo ships against the current binary using the
documented scaffolding, and each rung is rewritten to the target spelling as the
corresponding capability lands — the scaffolding version is retained in the
same file as the "what this costs today" exhibit rather than deleted.
