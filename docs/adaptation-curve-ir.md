# Adaptation Curve IR

`just adaptation-curve-ir` runs full-parameter and low-rank teaching trainers,
then normalizes their evidence into `sw-ml-study.adaptation-curve-ir` version 1.
The artifact is renderer-neutral: a CLI, chart, notebook, static report, or
audit tool can consume it without importing either training implementation.

Each stable run contains the same channels: a strategy and ID, zero-based loss
coordinates with gradient norms, held-out targets/predictions/loss, an explicit
no-training baseline, parameter-update evidence, and source provenance. The
full run carries initial/final/delta parameter vectors. The low-rank run carries
initial/final factors, rank, materialized delta and merged matrix, parameter
counts, and the frozen-base fingerprints.

Headless validation checks the root version and exact structural keys, stable
run IDs, shared task provenance, finite evidence, curve alignment and canonical
coordinates, prediction/baseline alignment, per-curve point limits, encoded
byte limits, and deterministic tagged-JSON round-trip. The demo prints selected
consumer-facing values and explains why they matter instead of treating a PASS
line as the demonstration.

The IR does not render charts, prescribe a UI, train production models, or make
full and low-rank parameters semantically identical. It preserves their
strategy-specific update evidence behind common curve, prediction, baseline,
and provenance channels.

For P curve points and E held-out scalar values, normalization and validation
are O(P + E) logical work beyond the already completed training runs. Both
source reports, the IR, encoded tagged JSON, and decoded validation copy coexist
in memory; curve points, numeric magnitude, output bytes, JSON depth, and JSON
elements are explicitly bounded.
