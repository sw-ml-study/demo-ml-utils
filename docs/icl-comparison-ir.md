# ICL Comparison IR

`just icl-comparison-ir` emits `sw-ml-study.icl-comparison-ir` version 1 for
zero-, one-, and few-shot inference. Each stable variant exposes context IDs,
similarity and contribution matrices, predictions and targets, MSE,
exact-within-tolerance matches and accuracy, and bounded association work.

The shared deployment section proves identical before/after fingerprints and
zero updates. Provenance identifies the fixture, task, mechanism, and analyzer.
Headless validation checks root and variant schemas, stable IDs, matrix and
prediction alignment, finite magnitudes, metric consistency, query/work/evidence
budgets, tagged-JSON round-trip, and byte-identical deterministic rebuilds.

The fixed example progresses from MSE `152/3` and accuracy 0, through MSE 24
and accuracy `1/3`, to MSE 0 and accuracy 1. Accuracy here means regression
predictions within the explicit `1e-9` absolute tolerance; it is not a
classification metric or a general benchmark.

The IR is renderer-neutral evidence transport. It does not prescribe a chart,
represent transformer attention, or claim production evaluation quality.
