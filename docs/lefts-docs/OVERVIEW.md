# LEFTS-Inspired Composable ML Experiments: Cross-Repository Plan

## Decision

Proceed without creating a new repository.

The first implementation belongs in `sw-ml-study/demo-ml-utils` and must begin as pure `.mlpl`.

`sw-ml-study/demo-extensions` is an incubator for any *specific native capability* that the pure-MLPL implementation proves is missing.

`sw-ml-study/sw-mlpl` changes only when the demo proves a missing capability is sufficiently general and belongs in the language/runtime rather than a library or extension.

`sw-ml-study/demo-functional-pipelines` should not duplicate this work. It may later cross-reference or extract a general pipeline idiom if the ML experiment discovers one.

## Research question

Can sw-MLPL express the useful algebra behind LEFTS—especially split, lift, ensemble, feed, and tune—as ordinary reusable MLPL code, without adding syntax, keywords, builtins, or Rust?

The objective is not to clone LEFTS. The objective is to use LEFTS as a forcing function for sw-MLPL's existing first-class functions, arrays, records, higher-order functions, and composition.

## Architectural rule

Use the least-powerful implementation layer that works:

1. Pure `.mlpl` application code.
2. Reusable `.mlpl` library code.
3. Existing generic runtime/library capability.
4. New generic native extension capability.
5. New language/runtime capability only when broadly justified.

Do not move upward merely for convenience or performance before the pure form has been demonstrated.

## Repository ownership

### `demo-ml-utils` — primary owner, start here

Owns:

- LEFTS-inspired research notes and attribution.
- Pure-MLPL model/computation representation.
- Pure-MLPL implementations or equivalents for:
  - split
  - lift
  - ensemble
  - feed
  - tune
- Runnable teaching-scale demos.
- Capability/blocker matrix.
- Minimized reproductions for anything that cannot be expressed cleanly.
- Documentation explaining which concepts collapse naturally into existing MLPL operations and which justify reusable library functions.

This repo should remain the consumer and forcing function.

### `demo-extensions` — conditional native incubator

Do nothing initially.

Only start work here when `demo-ml-utils` produces a concrete blocker whose solution requires Rust/native capability.

Examples that could justify extension work:

- generic parallel mapping/execution;
- mmap/range-backed array services;
- optimized numerical kernels;
- native external-library interoperability;
- long-lived opaque native state;
- GPU/device capability.

Do not implement `lift`, `feed`, `ensemble`, `split`, or `tune` in Rust merely because LEFTS names them.

If an extension is proven valuable and stable, it may later graduate into its own per-extension repository.

### `sw-mlpl` — conditional upstream owner

Do nothing initially.

A change is justified only if `demo-ml-utils` finds a missing capability that:

- cannot reasonably be expressed as an MLPL library;
- is not merely a performance concern;
- is useful well beyond ML experiments;
- composes with existing language semantics;
- has a minimized executable reproducer and acceptance criteria.

Examples might include inadequate first-class function values, inability to put callable values in records/arrays, missing closure behavior, generic higher-order application gaps, or a general module/namespace limitation.

The existing upstream roadmap already contains higher-order-function and namespace-related work. Reconcile with that work rather than creating parallel mechanisms.

### `demo-functional-pipelines` — coordination only

No implementation change is required for the first milestone.

After the experiment, inspect whether any newly discovered construct is a general functional-pipeline idiom independent of ML. If so:

- add a small cross-reference or companion example there;
- do not copy the whole ML demo;
- keep ML experiment semantics in `demo-ml-utils`.

## First vertical slice

Implement one tiny deterministic problem entirely in `.mlpl`:

1. Define a trivial learner/model with `fit` and `predict` behavior.
2. Partition a small dataset into several contexts/groups.
3. Train/construct one model per group.
4. Predict with each model.
5. Combine the predictions.
6. Print/return inspectable intermediate values.
7. Compare:
   - explicit MLPL;
   - factored reusable MLPL library;
   - only later, any extension-assisted version if required.

Use trivial arithmetic/linear behavior so model mathematics cannot obscure the language-design question.

## Increment order

Implement concepts in this order:

1. `split`
2. `lift`
3. `ensemble`
4. `feed`
5. `tune`

Reason:

- `split` tests data transformation.
- `lift` tests arrays/contexts of computations.
- `ensemble` tests mapping plus reduction.
- `feed` tests composition between learned computations.
- `tune` tests computations configuring computations and is the strongest abstraction test.

## Required blocker classification

Every obstacle must be classified before another repository is changed:

- `DEMO_BUG` — fix locally.
- `LIBRARY_GAP` — solve with reusable `.mlpl`.
- `LANGUAGE_EXPRESSIVENESS_GAP` — candidate for `sw-mlpl`.
- `NATIVE_CAPABILITY_GAP` — candidate for `demo-extensions`.
- `PERFORMANCE_ONLY` — keep pure implementation first; optimize separately.
- `ERGONOMICS_ONLY` — document explicit form before proposing syntax.

For any non-local gap, record:

- smallest failing `.mlpl` example;
- expected behavior;
- actual behavior/error;
- why existing constructs are insufficient;
- at least one rejected workaround;
- proposed lowest-layer remedy;
- whether the remedy is ML-specific or general.

## Naming

Do not create a global language keyword named `lift`.

During research, `lefts-inspired` is fine as a demo/documentation label.

For reusable public MLPL library naming, prefer a neutral namespace such as `experiment` if namespaces/modules are available:

- `experiment.split`
- `experiment.lift`
- `experiment.ensemble`
- `experiment.feed`
- `experiment.tune`

If current module syntax does not support the desired qualified form, use the repository's current legal naming convention and record qualified names as a future presentation goal. Do not block the pure semantic experiment on namespace polish.

## Exit criteria for the research slice

The slice is complete when:

- all five concepts have either a runnable pure-MLPL implementation/equivalent or a minimized classified blocker;
- at least one end-to-end composed demo uses several concepts together;
- tests are deterministic and self-checking;
- the implementation boundary is explicit;
- no Rust was added unless a native capability blocker was first demonstrated;
- no language change was proposed without a general-purpose justification;
- the docs say when native MLPL idioms make a named LEFTS-style combinator unnecessary.

## New-repository rule

Do not create `demo-workflows`, `demo-lefts`, or another repository now.

Consider a new repository only if the work later proves a domain-neutral workflow/computation abstraction with at least two convincing consumers outside ML, or if a proven extension graduates from the `demo-extensions` incubator and deserves independent lifecycle/versioning.
