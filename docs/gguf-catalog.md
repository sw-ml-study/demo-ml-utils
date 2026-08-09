# Bounded GGUF v3 Catalog Foundation

The normative contract is the official
[ggml GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md).
It defines the `GGUF` byte magic, v3 header, little-endian default, u64 counts
and strings, typed metadata, tensor descriptors, and aligned tensor-data
region. The demo implements a deliberately conservative subset rather than
claiming full GGUF compatibility.

`demos/gguf/catalog.mlpl` accepts little-endian v3, requires
`general.architecture`, supports optional `general.alignment` u32 (default 32),
and consumes arbitrary unique metadata keys whose scalar tags are U8/I8,
U16/I16, U32/I32, BOOL, STRING, or budgeted U64. Architecture and alignment
values are retained; other values contribute to a deterministic type
histogram in this catalog-oriented slice.

Multiple unique tensor descriptors are retained as name-byte tables and rows
of `[relative_offset, parameters, ggml_type_id, known_bytes]`. Active type IDs
from the pinned specification remain catalog-visible. `known_bytes` is `-1`
when this project has not established the type's block-size rule, explicitly
meaning “cataloged, extent unknown.” Simple F32/F16/BF16, signed integer, and
complete Q8_0 block extents are computed, sorted by offset for layout validation, and rejected if they
overlap or exceed the data buffer. Tensor payload bytes are never requested.

Native code supplies generic sandboxed `file_size` and exact bounded
`read_bytes`. MLPL owns little-endian decoding, cursor movement, format/type
policy, metadata parsing, alignment, shape arithmetic, descriptor validation,
and catalog construction. No external GGUF parser is used.

For M metadata items, T tensors, R total dimensions, S maximum string width,
and K catalog bytes, parsing is O(K + R), exact padded-name duplicate checks
are O(M²S + T²S), and tensor ordering is O(T log T). Retained memory is O(MS +
TS + T + R + largest field read). Current teaching budgets cap catalog reads
at 4096 bytes, metadata at 8, tensors at 4, strings at 256 bytes, rank at 4,
and parameters at one million. Because byte values are f64-backed, u64 fields
outside configured exact bounds fail closed.

Big-endian v3, metadata arrays, floating and signed-64 metadata, decoded scalar
metadata values beyond architecture/alignment, and exact extent rules for
other quantized types remain later work. Separate selective decoders read
catalog-validated [I8/I16 payloads](gguf-slice.md) and [Q8_0 blocks](gguf-q8-0.md);
floating and other quantization-block decode remain unsupported.
Exact name tables avoid hash collisions but intentionally trade quadratic
comparison work for simple fail-closed behavior under small count budgets.
