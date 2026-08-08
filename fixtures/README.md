# Test fixtures

Fixtures are tiny, deterministic, redistributable byte sequences generated
locally. They contain no downloaded model data. Run
`scripts/generate-safetensors-fixtures --write` to regenerate them and
`--check` to compare committed bytes with fresh output.

The repository gate limits each fixture to 1 MiB and rejects symlinks. Large
or downloaded model artifacts belong in ignored `models/` or `artifacts/`.
