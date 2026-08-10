set shell := ["sh", "-cu"]

# Show the repository's task recipes.
default:
    @just --list

# Validate the demo catalog and repository policy files.
audit:
    ./scripts/validate-catalog catalog/demos.tsv
    ./scripts/check-license
    ./scripts/check-doc-links
    ./scripts/check-fixtures
    ./scripts/check-sources

# Exercise the validation harness, including expected failures.
tests:
    ./tests/test-validation

# Print the configured sw-MLPL executable without installing anything.
mlpl-path:
    ./scripts/select-mlpl

# Check local prerequisites for the opt-in two-stage Agentrail MLX demo.
agentrail-mlx-preflight:
    ./scripts/check-agentrail-mlx-preflight

# Demonstrate grounded browser help and explicit progressive escalation.
help-escalation:
    ./scripts/run-help-escalation

# Train and evaluate a tiny CPU help router with Engram phrase memory.
trained-help-engram:
    ./scripts/run-trained-help-engram

# Demonstrate the configured binary's verified capabilities and limitations.
capabilities:
    ./scripts/run-capability-probe

# Probe callable composition, mapping laws, and the tiny fit/predict contract.
lefts-capabilities:
    ./scripts/run-lefts-capability-contract

# Compare a global baseline with explicit and factored per-group fitting.
split-lift:
    ./scripts/run-split-lift

# Demonstrate visible ensemble disagreement and a fed intermediate feature.
ensemble-feed:
    ./scripts/run-ensemble-feed

# Select a downstream configuration on validation, then evaluate held-out once.
tune:
    ./scripts/run-tune

# Compose Split, grouped fit, Feed, and Ensemble across two windows.
rolling-experiment:
    ./scripts/run-rolling-experiment

# Rerun the complete LEFTS-inspired slice and report promotion decisions.
lefts-acceptance:
    ./scripts/run-lefts-acceptance

# Run the single-file Web UI equivalent of the official LEFTS page example.
lefts-page-example:
    ./scripts/run-lefts-page-example

# Regenerate committed tiny Safetensors and GGUF fixtures.
generate-fixtures:
    ./scripts/generate-safetensors-fixtures --write
    ./scripts/generate-gguf-fixtures --write
    ./scripts/generate-checkpoint-fixtures --write
    ./scripts/generate-adaptation-fixtures --write

# Demonstrate the shared fine-tuning, ICL, and ICRL evidence contract.
adaptation-contract:
    ./scripts/run-adaptation-contract

# Demonstrate bounded manual-gradient linear fine-tuning.
linear-fine-tune:
    ./scripts/run-linear-fine-tune

# Demonstrate a frozen-base rank-one/rank-two adapter mechanism.
low-rank-adapter:
    ./scripts/run-low-rank-adapter

# Normalize full and low-rank training evidence into a renderer-neutral IR.
adaptation-curve-ir:
    ./scripts/run-adaptation-curve-ir

# Run deterministic, adversarial, and atomic fine-tuning acceptance.
fine-tuning-acceptance:
    ./scripts/run-fine-tuning-acceptance

# Demonstrate the bounded frozen-parameter ICL record contract.
icl-contract:
    ./scripts/run-icl-contract

# Demonstrate zero-, one-, and few-shot frozen associative inference.
associative-icl:
    ./scripts/run-associative-icl

# Demonstrate causal order, distractor, contradiction, and truncation controls.
icl-controls:
    ./scripts/run-icl-controls

# Normalize zero-, one-, and few-shot evidence for renderer-neutral consumers.
icl-comparison-ir:
    ./scripts/run-icl-comparison-ir

# Run final deterministic, adversarial, and atomic ICL acceptance.
icl-acceptance:
    ./scripts/run-icl-acceptance

# Demonstrate deterministic bandit histories and explicitly non-ICRL baselines.
bandit-contract:
    ./scripts/run-bandit-contract

# Generate diverse bounded source-learner bandit histories.
history-generator:
    ./scripts/run-history-generator

# Train and freeze the miniature offline history-conditioned policy.
distilled-policy:
    ./scripts/run-distilled-policy

# Demonstrate held-out reward adaptation with the frozen distilled policy.
icrl-rollout:
    ./scripts/run-icrl-rollout

# Run final deterministic, adversarial, renderer-neutral, and atomic ICRL acceptance.
icrl-acceptance:
    ./scripts/run-icrl-acceptance

# Demonstrate bounded Safetensors header inspection and fail-closed cases.
safetensors-headers:
    ./scripts/run-safetensors-header-tests

# Demonstrate a deterministic bounded Safetensors metadata catalog.
safetensors-catalog:
    ./scripts/run-safetensors-catalog

# Demonstrate selective signed-integer tensor decoding.
safetensors-slice:
    ./scripts/run-safetensors-slice

# Demonstrate fixed-chunk mergeable tensor statistics.
safetensors-statistics:
    ./scripts/run-safetensors-statistics

# Demonstrate a renderer-neutral, headlessly validated summary IR.
safetensors-summary:
    ./scripts/run-safetensors-summary

# Demonstrate a headlessly validated cross-format scene/tile JSON handoff.
scene-tiles:
    ./scripts/run-scene-tiles

# Demonstrate deterministic catalog-only tensor-city geometry.
tensor-city:
    ./scripts/run-tensor-city

# Demonstrate bounded histogram and sampled-surface detail tiles.
detail-tiles:
    ./scripts/run-detail-tiles

# Demonstrate Q8_0 block and reconstruction-error metrics.
quantization-error:
    ./scripts/run-quantization-error

# Demonstrate bounded ordered JSONL transport for visualization IR.
transport:
    ./scripts/run-transport

# Demonstrate bounded numeric conversion and reconstruction metrics.
numeric-conversion:
    ./scripts/run-numeric-conversion

# Demonstrate symmetric INT8 and GGUF-compatible Q8_0 round trips.
symmetric-roundtrip:
    ./scripts/run-symmetric-roundtrip

# Demonstrate an explicit teaching Q4 nibble round trip.
simple-q4:
    ./scripts/run-simple-q4

# Demonstrate bounded self-validating Safetensors-to-GGUF writing.
safetensors-to-gguf:
    ./scripts/run-safetensors-to-gguf

# Demonstrate passive no-execution checkpoint risk inventory.
checkpoint-inventory:
    ./scripts/run-checkpoint-inventory

# Demonstrate a no-execution allow-listed primitive pickle stack machine.
checkpoint-machine:
    ./scripts/run-checkpoint-machine

# Demonstrate metadata-only tensor and storage-range recovery.
checkpoint-tensor-metadata:
    ./scripts/run-checkpoint-tensor-metadata

# Demonstrate atomic, self-validating restricted-checkpoint extraction.
checkpoint-to-safetensors:
    ./scripts/run-checkpoint-to-safetensors

# Demonstrate consolidated restricted-checkpoint security acceptance.
checkpoint-security-acceptance:
    ./scripts/run-checkpoint-security-acceptance

# Opt-in: independently compare checkpoint storage with extracted Safetensors.
checkpoint-oracle:
    ./scripts/run-checkpoint-oracle

# Opt-in: compare a generated GGUF with an explicit external Python oracle.
external-oracle:
    ./scripts/run-external-oracle

# Demonstrate bounded GGUF v3 metadata and mixed-type tensor cataloging.
gguf-catalog:
    ./scripts/run-gguf-catalog

# Demonstrate an exact-name, bounded GGUF I8/I16 tensor payload read.
gguf-slice:
    ./scripts/run-gguf-slice

# Demonstrate one bounded GGUF Q8_0 block and its visible scale conversion.
gguf-q8-0:
    ./scripts/run-gguf-q8-0

# Demonstrate sampled, chunk-bounded, mergeable GGUF statistics.
gguf-statistics:
    ./scripts/run-gguf-statistics

# Opt-in: generate a 1 MiB sparse artifact and enforce its peak-RSS bound.
sparse-acceptance:
    ./scripts/run-sparse-safetensors-acceptance

# Opt-in: generate a 1 MiB sparse GGUF and enforce its peak-RSS bound.
gguf-sparse-acceptance:
    ./scripts/run-sparse-gguf-acceptance

# Run the complete local pre-commit gate.
check:
    ./scripts/check
