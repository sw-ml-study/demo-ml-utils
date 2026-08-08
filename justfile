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

# Probe the configured sw-MLPL binary's binary-format capabilities.
capabilities:
    ./scripts/run-capability-probe

# Regenerate committed tiny Safetensors fixtures.
generate-fixtures:
    ./scripts/generate-safetensors-fixtures --write

# Run the bounded Safetensors header decoder tests.
safetensors-headers:
    ./scripts/run-safetensors-header-tests

# Run the complete local pre-commit gate.
check:
    ./scripts/check
