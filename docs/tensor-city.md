# Deterministic Cross-Format Tensor City

`just tensor-city` catalogs a Safetensors artifact and a GGUF artifact, then
emits schema `sw-ml-study.tensor-city`, version 1. The city is renderer-neutral
columnar data rather than a graphics-engine scene: every tensor row aligns
with padded UTF-8 name and stable-ID tables, format and group codes, name
hierarchy depth, x/y/z positions, width/depth/height extents, parameter counts,
and encoded byte counts.

Stable IDs remain `<artifact-id>:tensor:<tensor-name>`. Exact padded-byte
comparison rejects ID collisions. Safetensors names retain deterministic
`record_keys` order after excluding `__metadata__`; GGUF names retain validated
descriptor order. The two sources form artifact districts: Safetensors uses
group 0 at z=0 and GGUF group 1 at z=4. Within each district x advances by 2,
width and depth are 1, height is `1 + parameters`, and y is half-height so each
building rests on the ground plane.

Name hierarchy is derived by counting dot-separated segments. The current
fixture names contain no dots and therefore have depth 1. A deeper real name
is retained unchanged but fails before construction if its segment count
exceeds the configured hierarchy budget. Artifact district is the current
top-level group; prefix sub-district placement is intentionally deferred until
fixtures exercise meaningful layered names.

MLPL owns both catalog parsers, name enumeration/decoding, stable ID tables,
hierarchy derivation, geometry, collision validation, conservative output
preflight, and schema validation. Native boundaries are bounded `file_size` /
`read_bytes`, deterministic `record_keys`, and generic tagged JSON encoding
and budgeted decoding. Tensor payload bytes are never requested.

The demonstration allows 12 logical objects (seven tensors plus five schema/
provenance objects), seven tiles and iterations, zero links, hierarchy depth
1, coordinates through 40, 64-byte names, 128-byte IDs, 32768 encoded bytes,
JSON depth 8, and 4096 decoded elements. Catalog, object, tile, link,
hierarchy, coordinate, label/ID width, iteration, conservative/actual output,
JSON depth, and element budgets fail closed.

For Hs Safetensors header bytes, Hg GGUF catalog bytes, T tensors, W padded
name/ID width, and J encoded output, construction is O(Hs + Hg + T²W + J): the
quadratic term is exact collision checking under the small tile budget.
Retained memory is O(Hs + Hg + TW + J). Tagged encoding, encoded JSON, and the
round-trip decoded city coexist during validation; the output and element
budgets bound those deliberate copies.

Golden tests pin both formats' ordering, districts, positions, heights,
attributes, hierarchy depths, and a representative stable ID. They also prove
repeat encoding is deterministic and reject malformed IDs and insufficient
object, tile, hierarchy, coordinate, iteration, or output budgets. This is
catalog geometry only. [Distribution and surface detail tiles](detail-tiles.md)
are now a separate bounded LOD stage; arbitrary prefix sub-districts,
quantization comparison, transport, and rendering remain later work.
