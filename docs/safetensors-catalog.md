# Bounded Safetensors Catalog

`demos/safetensors/catalog.mlpl` catalogs arbitrary tensor names from a
Safetensors file without reading tensor data. It uses `file_size`, an eight-byte
range read, and a header-range read capped at 4096 bytes. Total memory is
O(max header bytes), independent of model-file size.

## Implementation attribution

- **Native generic capabilities:** sandboxed `file_size`, bounded
  `read_bytes`, budgeted `parse_json`, deterministic `record_keys`, and basic
  array/record operations.
- **MLPL implementation:** little-endian length decoding, exactness/budget
  checks, schema validation, dtype/shape byte calculation, metadata policy,
  offset bounds, overlap/hole detection, complete-buffer coverage, aggregate
  counts, and deterministic catalog construction.
- **External tools:** none in the routine demo or tests.

The catalog supports byte-aligned `F64`, `F32`, `F16`, `BF16`, signed and
unsigned 8/16/32/64-bit integers, and `BOOL`. Sub-byte and newly introduced
dtypes fail closed until their packing and alignment rules have dedicated
tests.

## Output contract

The result contains sorted `header_keys`, tensor/parameter/byte counts,
metadata presence, data-buffer size, and a name-sorted numeric table whose rows
are `[start, end, parameters, dtype_bytes]`. `__metadata__`, when present, is
included in `header_keys` for transparent discovery but excluded from tensor
counts and rows.

The catalog rejects malformed JSON, duplicate names, missing/extra tensor
fields, non-string metadata values, unsupported dtypes, invalid shapes,
inexact or reversed offsets, shape/range byte mismatches, overlaps, holes, and
out-of-file ranges. Empty tensors and an entirely empty catalog are supported.

## Complexity and current limitation

For T tensors and H header bytes, JSON decode and schema validation are O(H +
T); offset ordering is O(T log T); memory is O(H + T). Tensor payload bytes are
never read.

The tensor-key walk uses one explicit `while` loop. `record_keys` returns a
string-list, but the current user-function argument binder cannot accept a
string-list parameter, so a recursive helper cannot receive the keys. The loop
keeps this constraint visible while preserving native MLPL validation. A
future general string-list parameter fix could replace it with recursion or a
string-list fold without changing the catalog contract.
