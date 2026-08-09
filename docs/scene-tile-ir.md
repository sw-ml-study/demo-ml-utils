# Cross-Format Scene/Tile IR Version 1

`just scene-tiles` builds a renderer-neutral JSON scene from one bounded
Safetensors analysis and one bounded GGUF analysis. Schema
`sw-ml-study.scene-tiles`, version 1, contains provenance for both source
artifacts, two tensor tiles, and one explicit comparison link. It contains no
geometry and assumes no browser, graphics API, or transport.

Tile IDs use `<artifact-id>:tensor:<tensor-name>`. Each tile carries a label,
format, parameter and encoded-byte counts, and six bounded population
statistics. The comparison link has its own stable ID and validated endpoints;
it exists because the demonstration intentionally compares two signed-integer
tensors, rather than implying that all tensors are related.

MLPL performs artifact validation and bounded statistics, constructs stable
IDs, provenance, tiles, and links, computes conservative output preflight, and
validates exact key sets and values. Generic native `to_json` and budgeted
`parse_json` are encoding boundaries. A literal golden JSON assertion pins
deterministic key ordering and numeric output, followed by a structural
round-trip check. No renderer or external artifact parser participates.

The current teaching contract permits exactly ten retained record objects and
one link, 64-byte labels, 4096 encoded bytes, JSON depth 8, and 128 decoded
elements. Object, link, label, conservative output, actual UTF-8 output, depth,
and decode-element budgets fail closed. Underlying artifact readers retain
their own catalog, parameter, chunk, block, sample, and iteration limits.

For Safetensors header/catalog work Hs, GGUF catalog work Hg, selected decoded
payload work P, and encoded JSON J, time is O(Hs + Hg + P + J). Retained memory
is O(Hs + Hg + bounded payload chunks + J). Construction holds the two source
summaries, scene IR, encoded JSON, and round-trip decoded IR simultaneously;
the 4096-byte output cap bounds this deliberate copy-heavy validation path.

Version 1 is a foundation, not a rendered 3D scene claim. It supports exactly
two named tiles and one comparison link. The separate
[tensor-city schema](tensor-city.md) now provides arbitrary bounded catalog
columns, hierarchy, and geometry; LOD, histograms, surfaces, renderer
transport, and browser interaction remain later steps. Renderers must consume
derived tiles and must not infer permission to load complete tensor payloads.
