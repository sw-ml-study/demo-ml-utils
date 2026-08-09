# Bounded GGUF Q8_0 Golden Decode

The format type ID and tensor placement follow the official
[GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md).
The authoritative ggml [`block_q8_0` definition](https://github.com/ggml-org/ggml/blob/master/src/ggml-common.h)
uses 32 values per block with one binary16 scale and 32 signed int8 quants;
ggml's [`dequantize_row_q8_0`](https://github.com/ggml-org/ggml/blob/master/src/ggml-quants.c)
converts each output as `signed_quant * fp16_scale`.

The generated golden block stores scale 0.5 as little-endian binary16 bytes
`00 38`, followed by signed quants `-16..15`. The default test compares MLPL's
32 outputs to the independently stated ggml oracle sequence `range(32) / 2 -
8`, exactly `-8, -7.5, ... 7.5`. It separately asserts scale conversion,
34-byte extent, complete-block shape, non-finite scale rejection, and read,
block, and output budgets.

The catalog establishes `parameters / 32 * 34` only for complete Q8_0 blocks.
Selection resolves the exact retained tensor name and checks dtype, parameter,
block, payload-byte, and expanded-output limits before its one payload range
read. Native code supplies sandboxed `file_size` and `read_bytes`; MLPL owns
all validation, binary16 conversion, signed conversion, and multiplication.
No external parser or decoder runs in the default gate.

For T catalog tensors, padded name width S, B selected blocks, and N = 32B
outputs, work beyond cataloging is O(TS + N). The payload and result require
O(N) memory; the current simple repeated concatenation can copy O(BN) values,
which is acceptable only under the explicit small block/output budgets and is
a documented target for a future streaming reduction.

Run `just gguf-q8-0` for the narrated scale-and-ramp demonstration. Only
finite little-endian Q8_0, complete whole-tensor reads, and materialized output
are supported. Encoding, partial tensor selection, other quantized families,
big-endian data, and chunked statistics remain out of scope.
