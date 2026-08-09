# Distribution and Sampled-Surface Tiles

`just detail-tiles` emits schema `sw-ml-study.distribution-surfaces`, version
1, for one selected Safetensors integer tensor and one selected GGUF Q8_0
tensor. Each tile retains its stable parent tensor ID, format, LOD 2, value
range, deterministic histogram edges/counts, and endpoint-inclusive sample
indices/values for a renderer-neutral surface strip.

Bins are left-closed and equal width; the maximum is assigned explicitly to
the last bin. Empty input has range zero, empty samples, and zero counts.
Constant input uses identical edges and bin zero. Surface positions are
`floor(i*(N-1)/(P-1))`, so both endpoints survive when P > 1. MLPL owns
decoding, extrema, bins, mergeable counts, sampling, IDs, schema validation,
and tagged JSON round-trip. Native code supplies only bounded reads and generic
serialization.

The demo caps payload reads at 34 bytes, Q8_0 at one block, decoded values at
32, bins and surface points at four, objects at five, iterations at two,
absolute displayed values at 65536, output at 8192 bytes, JSON depth at 8, and
decoded elements at 512. Catalog/dtype/parameter budgets remain active below
those tile limits. Golden tests cover both formats, histogram partition-merge
parity, sample order, deterministic JSON, and payload/sample/bin/object/
iteration/output failures.

For P decoded values, B bins, S surface points, and J JSON bytes, work is
O(P+B+S+J) and retained memory is O(P+B+S+J). The current selective decoders
materialize the complete selected tensor, but only after the strict payload,
block, parameter, and decoded-value caps succeed. Thus this is bounded, not a
claim of streaming arbitrary tensors; a future iterator could reduce retained
memory to one chunk without changing the tile schema.

Version 1 supports I8/I16-compatible Safetensors selection and GGUF Q8_0 in
the cross-format constructor. Random/adaptive sampling, logarithmic bins,
multidimensional surfaces, NaN policy, arbitrary LOD, quantization error,
transport, and rendering remain later work.
