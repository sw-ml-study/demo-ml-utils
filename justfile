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

# Demonstrate the configured binary's verified capabilities and limitations.
capabilities:
    ./scripts/run-capability-probe

# Regenerate committed tiny Safetensors and GGUF fixtures.
generate-fixtures:
    ./scripts/generate-safetensors-fixtures --write
    ./scripts/generate-gguf-fixtures --write
    ./scripts/generate-checkpoint-fixtures --write
    ./scripts/generate-adaptation-fixtures --write

# Demonstrate the shared fine-tuning, ICL, and ICRL evidence contract.
adaptation-contract:
    ./scripts/run-adaptation-contract

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
