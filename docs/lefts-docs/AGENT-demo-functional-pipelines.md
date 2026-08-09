# Agent Brief: `sw-ml-study/demo-functional-pipelines`

## Status

No implementation work is required for the first LEFTS-inspired milestone.

This repository is a peer/reference, not the owner of the ML experiment.

## Mission if activated later

After `demo-ml-utils` completes the first composable-experiments slice, review its results for *domain-neutral functional-pipeline idioms* worth demonstrating separately.

Examples might include:

- context-dependent mapping;
- composition of user-function references;
- map-then-reduce patterns;
- reusable branching/feeding pipelines;
- function-valued configuration.

## Rules

Do not:

- copy the LEFTS-inspired ML demo;
- add model/fit/predict abstractions here;
- duplicate `experiment.*` helpers;
- request upstream changes independently if `demo-ml-utils` already has the same blocker.

Do:

- extract at most a small general example whose value is obvious without ML;
- cross-reference the ML consumer where useful;
- reuse the existing upstream-contract mechanism;
- keep examples deterministic and self-checking.

## Activation criterion

Change this repo only if at least one abstraction discovered in `demo-ml-utils` is both:

1. clearly useful outside machine learning; and
2. best explained as a functional-pipeline concept rather than an ML experiment concept.

Otherwise leave this repository unchanged.
