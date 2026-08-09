# Safetensors Visualization Summary IR

`demos/visualization/safetensors_summary.mlpl` emits a renderer-neutral JSON
summary for one selected tensor. Schema `sw-ml-study.safetensors-summary`,
version 1, contains four objects: the root, provenance, tensor metadata, and
bounded aggregate statistics. Stable tensor IDs use
`<artifact-id>:tensor:<tensor-name>`; provenance names the source path, format,
artifact ID, and MLPL analyzer.

MLPL constructs and validates the schema, stable IDs, provenance, tensor
metadata, and statistics. Native `to_json` and `parse_json` are generic
encoding boundaries. Headless tests validate exact key sets, schema/version,
stable-ID derivation, deterministic encoding, and structural round trip. No
renderer or browser dependency is present.

The object budget must allow exactly the four schema objects. Before IR
construction or JSON encoding, a conservative byte bound accounts for source
and identifier strings, shape dimensions, statistics, and structural
overhead. The actual UTF-8 encoded size is checked again, and round-trip decode
uses depth, byte, and element budgets. This conservative preflight may reject
an output that would narrowly fit; it intentionally fails closed.

For header size H, tensor count T, selected payload bytes B, chunk bytes C, and
encoded summary bytes J, time is O(H + T log T + B + J) and retained memory is
O(H + T + C + J). Only the selected tensor is summarized. The
[cross-format scene/tile IR](scene-tile-ir.md) can now compose this summary
with a bounded GGUF tile; multi-tensor layout, geometry, LOD tiles, and browser
rendering remain future work.
