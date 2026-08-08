# Bounded GGUF v3 Catalog Foundation

The normative contract is the official
[ggml GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md).
It defines the `GGUF` byte magic, v3 header, little-endian default, u64 counts
and strings, typed metadata, tensor descriptors, and aligned tensor-data
region. The demo implements a deliberately conservative subset rather than
claiming full GGUF compatibility.

`demos/gguf/catalog.mlpl` accepts little-endian v3, requires
`general.architecture`, supports optional `general.alignment` u32 (default 32),
and catalogs zero or one F32 tensor. It rejects all other metadata keys/value
types and tensor types in this first slice. Names, strings, counts, rank,
parameter products, cursor movement, padding, offsets, and file bounds are
checked under caller budgets. Tensor payload bytes are never requested; only
the final F32 range is proven to fit the file.

Native code supplies generic sandboxed `file_size` and exact bounded
`read_bytes`. MLPL owns little-endian decoding, cursor movement, format/type
policy, metadata parsing, alignment, shape arithmetic, descriptor validation,
and catalog construction. No external GGUF parser is used.

For M metadata items, T tensors, R total dimensions, S total catalog string
bytes, and K catalog bytes, logical time is O(M + T + R + S + K) and retained
memory is O(R + S + largest field read). Current teaching budgets cap catalog
reads at 4096 bytes, metadata at 8, tensors at 4 (while the subset additionally
allows at most one), strings at 256 bytes, rank at 4, and parameters at one
million. Because byte values are f64-backed, u64 fields outside configured
exact bounds fail closed.

Big-endian v3, arbitrary metadata, arrays, floating metadata, multiple tensor
names, non-F32 types, overlapping tensor extents, payload decoding, and
quantization blocks remain later work. The next catalog-coverage step should
retain unsupported tensor type IDs visibly where bounds can be validated,
rather than describing them as decoded.
