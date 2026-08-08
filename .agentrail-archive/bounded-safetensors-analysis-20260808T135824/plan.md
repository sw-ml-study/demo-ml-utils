# Bounded Safetensors Analysis

Build bounded tensor-payload analysis on the completed range-I/O and metadata-catalog foundation. MLPL owns dtype decoding, reductions, and summary construction; native builtins remain generic bounded I/O and JSON services. Default tests use tiny generated fixtures, while large sparse acceptance remains opt-in and measured.

1. `selective-slice-dtype-decode` — Add selective tensor-region reads and golden decoding for an intentionally small byte-aligned dtype set. Validate alignment, range, exactness, and read budgets; update catalog and attribution docs.
2. `mergeable-chunk-statistics` — Compute count, min, max, sum, mean, and variance from fixed-size chunks with mergeable state and deterministic parity tests.
3. `sparse-large-artifact-acceptance` — Generate an opt-in sparse Safetensors artifact larger than the configured memory budget and record measured peak memory while preserving the chunk bound.
4. `visualization-summary-ir` — Emit a versioned, budgeted JSON summary IR and validate it headlessly without adding a renderer dependency.
5. `bounded-analysis-report` — Run the full suite, reconcile complexity and limitations, decide the GGUF saga gate, close the saga, and stop.

Acceptance: selected supported tensors decode and reduce without reading the complete artifact or exceeding documented chunk memory; malformed and unsupported inputs fail closed; implementation-layer claims remain explicit.