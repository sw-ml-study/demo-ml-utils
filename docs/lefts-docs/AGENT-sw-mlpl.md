# Agent Brief: `sw-ml-study/sw-mlpl`

## Activation condition

Do not change the language/runtime for the LEFTS-inspired demo preemptively.

This brief becomes active only when `demo-ml-utils` supplies a minimized `LANGUAGE_EXPRESSIVENESS_GAP` and shows why a reusable `.mlpl` library cannot solve it cleanly.

## Mission

Evaluate and, only if justified, implement the smallest general-purpose language/runtime capability required by the composable-experiments research.

The solution must serve the language broadly, not encode LEFTS or ML-specific vocabulary into the core.

## First task: classify the request

Before coding, decide whether the reported gap is actually:

- already supported but poorly documented;
- a library problem;
- an ergonomics problem;
- a native/performance problem;
- a true language/runtime expressiveness gap.

Reject or redirect requests that belong elsewhere.

## Reconcile with existing roadmap

Search current implementation and queued sagas before designing anything new.

Pay particular attention to existing work around:

- first-class user-function references/callable machinery;
- `each`, `table`, `over`, `atop`, and related higher-order-function support;
- combinator support;
- nested arrays/enclose;
- records and safe record access;
- module/namespace and qualified-name work;
- extension registry/import surface.

Do not create a second mechanism for something already planned or shipped.

## Strong acceptance standard

A language change should have:

- minimized failing `.mlpl`;
- a non-ML example demonstrating generality;
- clear semantics independent of LEFTS terminology;
- parser/evaluator/compiler parity where applicable;
- interaction with function references, arrays, records, errors, and compilation documented;
- regression tests;
- documentation and examples;
- no special-case recognition of `lift`, `feed`, `ensemble`, `split`, or `tune`.

## Likely legitimate categories

Possible examples, only if actually proven missing:

- user-function references cannot be stored/passed in required value positions;
- closures cannot capture required context;
- functions cannot return callable/computation values;
- generic HOF invocation is artificially restricted;
- records/arrays cannot contain the values necessary to represent a computation;
- module/namespace rules prevent a reusable qualified MLPL library surface;
- compiled and interpreted semantics diverge for the required construct.

## Likely illegitimate language requests

Do not add core syntax/builtins merely for:

- parallel execution;
- GPU acceleration;
- faster matrix kernels;
- external library access;
- caching;
- model-specific fit/predict protocols;
- LEFTS API compatibility;
- shorter spelling when existing composition is already clear.

Those belong in libraries/extensions or documentation.

## Implementation method

1. Reproduce the consumer failure in the current tree.
2. Search for an existing capability or pending saga.
3. Write a design note if semantics are nontrivial.
4. Add failing tests at the narrowest layer.
5. Implement the smallest general capability.
6. Verify REPL/interpreter/compiler parity as applicable.
7. Add a non-ML example.
8. Add/update documentation.
9. Run the project's full required checks.
10. Report the exact consumer syntax now enabled.

## Output contract back to `demo-ml-utils`

Provide:

- first sw-MLPL version/commit containing the capability;
- exact supported syntax;
- behavior and error semantics;
- any limitations;
- migration/workaround for older versions;
- a tiny standalone example;
- tests proving the original blocker is resolved.

Do not implement the consumer demo in this repository.
