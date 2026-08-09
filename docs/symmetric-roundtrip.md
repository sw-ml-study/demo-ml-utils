# Symmetric INT8 and Q8_0 Round Trips

`just symmetric-roundtrip` quantizes the 32-value ramp -16..15 with one
max-absolute scale. Bare INT8 rounds to nearest with halves away from zero,
saturates to -127..127, packs negative quants as unsigned bytes, and decodes
the payload back to scaled values. The Q8_0 path encodes the scale as
little-endian IEEE binary16 followed by 32 signed quant bytes, then hands the
34-byte block to the existing GGUF Q8_0 decoder.

The committed golden payload begins with scale bytes `[8,48]` and fixes all 32
quant bytes. Separate `[0,56]` and `[0,60]` goldens cover binary16 encodings of
0.5 and 1. Zero blocks encode as 34 zero bytes. The demo prints scale, boundary
quants, byte counts, RMSE, maximum error, and cosine, and explains that binary16
scale rounding is part of the Q8_0 reconstruction error.

MLPL owns scale selection, rounding, saturation, signed-byte packing,
binary16 encoding, block construction, decoding, and metrics. There is no
native or external quantizer and no filesystem access. This is payload-format
compatibility with the repository's GGUF decoder; it does not claim bit parity
with every external quantizer's scale-selection or rounding policy.

Inputs must be finite, rank-one, nonempty, within the magnitude budget, and a
multiple of 32 for Q8_0. Value, iteration, output-value, block, payload-byte,
and binary16-normalization budgets fail closed, as do partial blocks, invalid
bytes/scales, and binary16 overflow or non-finite input.

For N values and B blocks, arithmetic work is O(N+B). Repeated MLPL `concat`
causes O(N²) copying inside payload construction; the demo is capped at two
blocks/64 values and 128 output bytes. Source, quant, byte, reconstructed,
metric, and per-block temporary arrays can coexist under those explicit caps.
