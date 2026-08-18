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
U16/I16, U32/I32, BOOL, STRING, or budgeted U64. It also consumes non-nested
arrays of every GGUF scalar element type. This includes the STRING
`tokenizer.ggml.tokens`, F32 `tokenizer.ggml.scores`, and I32
`tokenizer.ggml.token_type` arrays used by llama.cpp models. Architecture and
alignment values are retained; other values contribute to deterministic type
and array histograms in this catalog-oriented slice.

`metadata_array_rows` aligns one `[element_type, elements, payload_bytes]` row
with every metadata key; scalar keys use `[-1,0,0]`. This lets a consumer
associate tokenizer keys with their bounded array framing and proves the
cursor reaches the tensor directory exactly. The catalog does not retain token
strings or decode F32 scores: it validates their framing and skips numeric
payloads in chunks of at most 65,536 bytes. String framing delegates to the
native `scan_length_prefixed` fold, which retains no token payloads, uses
constant native stack, and returns the exact logical cursor and aggregate byte
counts.

F32, I64, and F64 top-level scalar fields are also consumed at their exact
fixed widths so ordinary llama.cpp metadata cannot desynchronize the tensor
directory. Their values are not decoded or retained by this catalog API.

Multiple unique tensor descriptors are retained as name-byte tables and rows
of `[relative_offset, parameters, ggml_type_id, known_bytes]`. Active type IDs
from the pinned specification remain catalog-visible. `known_bytes` is `-1`
when this project has not established the type's block-size rule, explicitly
meaning “cataloged, extent unknown.” Simple F32/F16/BF16, signed integer, and
complete Q8_0 block extents are computed, sorted by offset for layout validation, and rejected if they
overlap or exceed the data buffer. Tensor payloads are never decoded or read by
the metadata scanner.

Native code supplies generic sandboxed `file_size` and exact bounded
`read_bytes`. MLPL owns little-endian decoding, cursor movement, format/type
policy, metadata parsing, alignment, shape arithmetic, descriptor validation,
and catalog construction. No external GGUF parser is used.

For M metadata items, A total array elements, T tensors, R total dimensions,
S maximum string width, and K catalog bytes, parsing is O(K + A + R), exact
lazy name duplicate checks are O(M²S + T²S), and tensor ordering is O(T log
T). The catalog retains file offsets and lengths rather than padded name-byte
matrices; consumers decode one name with one bounded range read. Retained
memory is O(M + T + R + largest field read). Current teaching budgets cap catalog reads
at 4096 bytes, metadata at 8, tensors at 4, strings at 256 bytes, rank at 4,
and the shared parameter/array-element ceiling at one million. Metadata keys
have a separate 256-byte ceiling. Packed bounded reads avoid f64 expansion for
fixed-width scalar and skipped numeric-array bytes. u64 fields
outside configured exact bounds fail closed.

Big-endian v3, nested arrays, decoded array values, floating and signed-64
scalar metadata, decoded scalar metadata values beyond architecture/alignment, and exact extent rules for
other quantized types remain later work. Separate selective decoders read
catalog-validated [I8/I16 payloads](gguf-slice.md) and [Q8_0 blocks](gguf-q8-0.md);
floating and other quantization-block decode remain unsupported.
Exact name tables avoid hash collisions but intentionally trade quadratic
comparison work for simple fail-closed behavior under small count budgets.
The completed [GGUF acceptance report](gguf-acceptance-report.md) adds
chunk-bounded sampled statistics.

## Real llama.cpp acceptance

`probes/gguf-real-array-probe.mlpl` was run against the locally downloaded,
SHA-256-verified `SmolLM2-135M-Instruct-Q8_0.gguf`. With explicit ceilings of
64 MiB catalog bytes, 256 metadata entries, 2,048 tensors, 4,096 bytes per
string, rank 8, and one billion parameters/array elements, it recovered:

- architecture `llama`;
- 40 metadata entries and 5 arrays;
- 147,209 array elements occupying 1,767,758 framed payload bytes;
- 272 tensor descriptors;
- an aligned tensor-data boundary at byte 1,786,144;
- the first tensor at relative offset zero with shape product 576 and 2,304
  known F32 bytes.

This probe interprets metadata only, subject to the bounded lookahead above,
and takes materially longer than the tiny demo because token-string framing is
validated in MLPL. It is deterministic and
requires the model path to be inside the selected sw-MLPL filesystem sandbox.

The initial constant-frame MLPL decoder reduced latency but still measured
505,102,336 bytes maximum RSS. sw-MLPL commit `b4691193` then shipped the
generic native scanner, and `be724494` shipped packed bounded reads and offset
scanning requested in
[upstream-contract.md](upstream-contract.md#bounded-length-prefixed-stream-traversal).
`just gguf-real-array-acceptance` enforces 30 seconds, 131,072 KiB RSS, and a
16 MiB stack. On 2026-08-17, SmolLM2 Q8_0 completed in one second at 54,592
KiB peak RSS while reaching 272 tensor descriptors after 147,209 tokenizer
array elements.
