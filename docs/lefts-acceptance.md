# LEFTS-Inspired Demo Acceptance Report

## Outcome

The bounded LEFTS-inspired teaching slice is complete and requires no changes
to `sw-mlpl`, no native extension, and no new repository. Run the consolidated
gate with `just lefts-acceptance`; `just check` also exercises it through the
self-describing-output suite.

This work is inspired by the [LEFTS project](https://nsmat.github.io/lefts/),
particularly its Split, Lift, Ensemble, Feed, and Tune model transformations
and its emphasis on closure under composition. It is not a port and does not
claim compatibility with the LEFTS Python API.

## Demonstrated evidence

| Concept | Visible result | Adversarial evidence |
| --- | --- | --- |
| callable contract | named references, partials, callable records, returned descriptions, container-specific mapping laws | insufficient element budget fails |
| Split | disjoint row provenance before fitting | duplicates, leakage, misalignment, and comparison limits fail |
| Lift-inspired grouped fit | offsets `[2, 8]`; MSE improves from 9 to 0; explicit/factored parity | empty groups, unknown groups, and row limits fail |
| Ensemble | members disagree by 2 and each score MSE 1; ordered mean scores 0 | empty/misaligned evaluation and magnitude limits fail |
| Feed | squared intermediate `[1, 4, 9]`; MSE 0 versus ablation MSE 32.67 | excessive/non-finite predictions fail |
| Tune | candidate MSE `[1, 0, 1]`; lower-index tie rule; one held-out evaluation | leakage, empty/excess candidates, malformed/non-finite data, and limits fail |
| rolling composition | two refits, exact explicit parity, stable seven-node/six-edge IR | node, edge, output, identity, and grouped-work limits fail |

The acceptance runner executes all five component runners twice and requires
byte-identical stdout, in addition to their internal deterministic goldens and
hostile cases.

## Functor conclusion

`each` over arrays and `map_ok` over Results have concrete identity,
composition, and preservation evidence. That makes “functor-like” useful when
describing those particular mappings. An endofunctor is a functor whose source
and destination category are the same; an `M -> M`-shaped computation
transformation alone proves neither a functor nor an endofunctor because it
does not define a morphism mapping or establish the laws.

The LEFTS-inspired transformations remain computation combinators or
endofunctor-like transformations. A first-class generic `Functor` facility is
not justified by this slice.

## Promotion decisions

- Retain callable records as the reusable MLPL computation-interface pattern.
- Retain grouped fitting as a concrete local MLPL helper; do not add a global
  `lift` keyword or generic `experiment.lift` wrapper yet.
- Retain Ensemble, Feed, and Tune as teaching combinators until a second
  substantive consumer reveals the right reusable API.
- Treat the computation-description IR as a candidate for extraction only
  after a convincing non-ML consumer exists.
- Make no `sw-mlpl`, `demo-extensions`, or `demo-functional-pipelines` change.
- Create no `demo-lefts` or workflow repository.

There are no unresolved `LANGUAGE_EXPRESSIVENESS_GAP` or
`NATIVE_CAPABILITY_GAP` blockers. The absence of heterogeneous arrays of
callable records and lexical closures did not block the record-registry and
partial-application design.

## Boundaries

The demos use tiny deterministic scalar learners, sequential in-memory
execution, and generated data. They do not demonstrate production training,
distributed execution, parallel model evaluation, GPU kernels, caching,
external model libraries, or broad hyperparameter optimization. The IR is an
inspectable description, not a scheduler. Every substantive operation is
MLPL; no Python or Rust implementation is hidden behind the result.
