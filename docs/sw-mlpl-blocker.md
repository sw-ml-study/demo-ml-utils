# sw-MLPL array-expressiveness blocker record for convolution from equations

## Status

Partially shipped. C5 and C1 are verified fixed; C2, C3, and C4 remain open. Five gaps are
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

This build reported `0.22.0` when observed. That bump was premature and is
being backed down to 0.21.x with identical content, so the version string is
deliberately omitted from the pin above. The commit is the identity.

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

## C2 — trailing-axis rank broadcasting

Probe: `probes/rank-broadcast.mlpl`. Current behavior:
`error: mul: expected [2, 2, 3, 3], got [3, 3]`.

Scalar broadcasting works. Rank broadcasting does not: elementwise operators
require identical shapes. The convolution's shared kernel must therefore be
replicated to full patch shape before multiplication. The working idiom found
during prototyping is an outer product:

```mlpl
tiled = reshape(table(:mul, ones([oh * ow]), flatten(k)), [oh, ow, c, kh, kw])
```

This is unreadable, and it is not free. Measured on this binary, an
`[8, 32, 32]` input with `[16, 8, 3, 3]` filters materializes 1,036,800 f64
cells of replicated kernel — 8.3 MB — purely to satisfy a shape rule, against
64,800 cells of actual patch data. Total runtime was 211.8 ms against 1.2 ms
for native `conv2d` on the same values, a 172x gap of which the replication is
a large part.

Required behavior: NumPy/PyTorch-style trailing-axis broadcasting for
elementwise operators, where a size-1 or absent leading axis expands. The
contract must state how axis labels combine when ranks differ, since a labeled
`[out_y, out_x, channel, kernel_y, kernel_x]` meeting a labeled
`[channel, kernel_y, kernel_x]` should align by trailing position and validate
the shared names. Mismatches must keep the existing structured
`ShapeMismatch { op, expected, actual }` diagnostic that renders both labeled
shapes.

Acceptance must cover rank-1 against rank-2, size-1 axes expanding, an
incompatible trailing axis, and a label collision between aligned axes.

## C3 — multi-axis reduction

Probe: `probes/multi-axis-reduce.mlpl`. Current behavior:
`error: unsupported: reduce: axis must be a scalar, got rank 1`.

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

## C4 — named-axis parity for higher-order reduce

Probe: `probes/named-axis-reduce.mlpl`. Current behavior:
`error: expected an array value, got a string`.

`reduce_add(M, "feat")` accepts a labeled axis. `reduce(:add, M, "feat")` does
not. This is an inconsistency between a shorthand and the general form it is
documented as equivalent to, and it forces the demo to choose between quoted
operators and readable axis names.

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
- No native performance work. The 172x gap against `conv2d` is reported as a
  measured teaching-path limit under `PERFORMANCE_ONLY`, and the demo states it
  rather than hiding it. C2 would close part of the gap as a side effect; that
  is not the reason to ship C2.
- No autograd extension. The demo is forward-only. Whether `windows` is
  differentiable is an upstream design question, not a downstream requirement.

## Downstream acceptance evidence

| Gap | Probe | Expected once shipped |
|---|---|---|
| C1 | `probes/sliding-windows.mlpl` | **Met at `7f2c4e99`**; matches the `rotate`/`compress` reference construction exactly |
| C2 | `probes/rank-broadcast.mlpl` | Exits zero; product equals the `table`-tiled reference |
| C3 | `probes/multi-axis-reduce.mlpl` | Exits zero; equals nested single-axis reduction |
| C4 | `probes/named-axis-reduce.mlpl` | Exits zero; equals the integer-axis form |
| C5 | `probes/compress-label-preservation.mlpl` | **Met at `274c9133`**; labels match `rotate` |

C2, C3, and C4 currently exit nonzero, so an upstream implementation announces
itself by changing the gate. C5 and C1 have flipped.

## Upstream phased delivery

`sw-mlpl` accepted these gaps and scheduled them as follows. This table is the
reconciliation key: when a release lands, the named probes must flip and the
named rungs are rewritten in the same step.

| Phase | Release | Gaps | Probes flipped | Downstream effect | State |
|---|---|---|---|---|---|
| 1 | `476e9bf4` | C5 | `compress-label-preservation` | Labeled-axis trimming stops needing a `relabel` after every `compress` | **shipped** |
| 2 | `476e9bf4` | C1 | `sliding-windows` | `u:conv_windows` (25 lines) collapses to one `windows` call | **shipped** |
| 3 | next | C3, C4 | `multi-axis-reduce`, `named-axis-reduce` | Three nested integer-axis reduces collapse to one named-axis reduction | open |
| 4 | later | C2 | `rank-broadcast` | The `table`-tiled kernel replication disappears | open |

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

### C2 is a readability gate, not a capability gate

Upstream advised staging the demo as reduce-only patch sums until C2 ships,
on the grounds that `kernel * windows(...)` will not broadcast before then.
The broadcast is genuinely unavailable, but the conclusion does not follow:
the weighted multi-channel convolution runs today, using native `windows` plus
the `table`-tiling workaround this record already documents under C2.

Verified on commits `7f2c4e99` and `476e9bf4`: a `[2, 5, 5]` input against
`[3, 2, 2, 2]` filters reproduces `conv2d` with max absolute difference 0,
using `windows` for the patches and tiling for the kernel.

The distinction that matters is scale. C1 removed the 25-line window
construction, which was the scaffolding the demo could not tolerate. What C2
removes is one remaining line:

```mlpl
tiled = reshape(table(:mul, ones([oh * ow]), flatten(k)), [oh, ow, c, kh, kw])
```

One documented, commented line is an acceptable exhibit in a demo whose
subject is the distance between notation and code. Twenty-five lines of
`rotate`/`compress`/`concat`/`transpose_axes` was not. Rung 4 therefore ships
at `476e9bf4` with that line marked as the C2 placeholder, rather than waiting
for Phase 4.

This matters for sequencing. Rung 4, the paper's triple sum, is the demo's
payload; rungs 1-3 exist to reach it. Deferring the kernel multiply to Phase 4
would ship a box-filter demo and postpone the equation the demo is named for.
The staging is therefore by spelling, not by capability: every rung including
rung 4 ships now with the documented workaround, and C2 replaces the tiling
line when it lands. The frozen axis order is what keeps that a one-line change.

Moving averages and patch sums remain worth showing, but as rung 2 and rung 3
material in their own right, not as a substitute for rung 4.

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
