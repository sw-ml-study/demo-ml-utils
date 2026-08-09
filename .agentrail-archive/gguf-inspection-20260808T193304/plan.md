# GGUF Inspection

Build a bounded, fail-closed GGUF v3 inspection path using the shipped range-I/O and measured-memory foundation. MLPL owns format parsing, validation, cataloging, decoding, and reductions; native builtins remain generic filesystem and serialization boundaries. Default fixtures are tiny, generated, and redistributable.

1. `gguf-v3-catalog-foundation` — Pin the authoritative format contract, generate valid and malformed tiny fixtures, and parse a conservative GGUF v3 envelope, scalar metadata subset, alignment, and tensor directory without reading tensor payloads.
2. `gguf-catalog-type-coverage` — Expand bounded metadata and tensor-type catalog coverage while retaining unsupported entries without pretending to decode them.
3. `gguf-unquantized-slices` — Selectively decode a small unquantized dtype set with golden vectors and fixed read budgets.
4. `gguf-q8-0-golden` — Decode Q8_0 golden blocks in MLPL and compare with an explicitly named reference oracle.
5. `gguf-bounded-statistics-report` — Add bounded sampling/statistics, measured acceptance, reconcile the catalog and roadmap, decide the visualization saga gate, close the saga, and stop.

Acceptance: GGUF metadata and tensor directories are inspectable without payload materialization; selected supported payloads decode under bounded reads; unsupported types fail closed or remain catalog-visible as documented; format-specific work is attributed to MLPL.