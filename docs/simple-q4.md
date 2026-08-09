# Simple Q4 Teaching Round Trip

`just simple-q4` encodes 32 values into an explicit 18-byte teaching block:
two little-endian binary16 scale bytes followed by 16 packed bytes. Each byte
holds the even-index quant in its low nibble and the odd-index quant in its
high nibble. Nibble values decode by subtracting 8, so nibble 8 is zero; the
encoder uses the symmetric -7..7 range and leaves -8 unused.

This format is deliberately called `teaching-q4`, not GGUF Q4_0. Its layout is
small, deterministic, and useful for exercising bit-level repacking, but no
external compatibility is implied. The committed ramp golden is
`[146,64,17,34,51,68,84,101,118,135,136,153,170,187,204,220,237,254]`.
An all-zero block is scale `[0,0]` followed by sixteen bytes of 136 (`0x88`).

MLPL owns scale selection, binary16 encoding/decoding, nearest rounding with
halves away from zero, saturation, nibble packing/unpacking, and absolute,
RMSE, maximum, and cosine metrics. No filesystem, native quantizer, or external
oracle participates. The demo explains the 128-to-18-byte (7.11x) size change
alongside the resulting error, so the compression tradeoff is demonstrable.

Rank, finiteness, magnitude, complete-block, byte validity, value, iteration,
output-value, block, payload-byte, and binary16 normalization limits fail
closed. For N values, work is O(N), while repeated MLPL `concat` causes O(N²)
actual copying. The teaching demo caps work at two blocks/64 values and 64
payload bytes; source, packed, reconstructed, scale, and metric temporaries may
coexist within those bounds.
