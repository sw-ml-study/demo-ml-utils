# Self-Validating Safetensors-to-GGUF Writer

`just safetensors-to-gguf` converts one named rank-one Safetensors `I8` or
`I16` tensor into a deterministic little-endian GGUF v3 file. The writer emits
the required `general.architecture`, explicit 32-byte alignment, one tensor
descriptor at relative offset zero, zero catalog padding, and the unchanged
little-endian source payload. `I8` maps to GGUF type 24 and `I16` to type 25.

The narrated I16 example writes 166 bytes: a 160-byte aligned catalog and the
six source payload bytes. After crash-safe atomic replacement, the existing
GGUF catalog and selective decoder reopen the file and must recover one tensor,
two metadata entries, matching type/extent, and values `[-32768,-2,32767]`.
Only then does conversion return success. A test also places a sentinel at the
destination and proves that a pre-write budget failure leaves it unchanged.

MLPL owns source schema/layout validation, tensor selection, dtype policy,
little-endian scalar/string encoding, metadata and tensor directory structure,
alignment/padding, artifact assembly, and all read-back comparisons. Native
primitives supply bounded reads, file size, and atomic byte replacement. No
Python, llama.cpp, Rust format writer, or other hidden converter participates.

This deliberately narrow slice rejects unsigned, floating, quantized,
multidimensional, multi-tensor, missing, or unsupported tensors. Rank-one
restriction avoids claiming a cross-format dimension-order policy not yet
tested. Header/JSON-element/parameter/payload/output/string/rank/tensor/
metadata/iteration budgets fail before replacement.

For source header H, selected payload P, output G, and read-back catalog C,
logical work is O(H+P+G+C). Repeated MLPL `concat` while assembling fields can
copy growing arrays, so actual writer copying is O(G²). Source header/catalog,
payload, assembled output, read-back catalog, and decoded values may coexist;
the demonstration caps them at 4096 header bytes, 64 payload bytes, and 512
output bytes. This is a bounded teaching writer, not a streaming large-model
converter yet.

Independent cross-language evidence now belongs outside this repository. The
MLPL demo itself compares its deterministic file hash plus header, metadata,
tensor descriptor, shape, offset, and decoded values.
