# Selective Bounded GGUF Integer Decode

The normative layout and type identifiers come from the official
[ggml GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md).
This deliberately small decoder supports only GGML I8 (type 24) and I16 (type
25), using generated golden bytes whose signed boundary values are asserted by
the default test gate.

`u:read_gguf_tensor` first builds the fully validated bounded catalog, resolves
the requested tensor name exactly from its retained byte table, and checks its
known extent against the caller's payload-read budget. Only then does it derive
the absolute offset from the aligned tensor-data start and issue one exact
`read_bytes` call for the selected range. Unsupported F32 descriptors fail
closed before payload I/O; Q8_0 uses its separate budgeted block decoder.

Native code supplies sandboxed `file_size` and bounded `read_bytes`. MLPL owns
catalog validation, exact name resolution, dtype policy, budget enforcement,
offset arithmetic, little-endian assembly, and signed conversion. No external
GGUF parser or numeric decoder participates in the demo.

For catalog size K, tensor count T, maximum padded name width S, and selected
payload size B, the additional selection and decode work is O(TS + B), with
O(B) retained payload/output memory beyond the catalog. The teaching fixture
caps catalog reads at 4096 bytes, metadata at 8 entries, tensors at 4, rank at
4, parameters at one million, and the selected payload at exactly 8 bytes.

Run `just gguf-slice` for a narrated decode of four I16 boundary-spanning
values. Current limitations are intentional: only exact-name I8/I16 selection,
whole selected-region output, little-endian GGUF v3, and already-cataloged
extents are supported. Floating types, quantized blocks, slicing within a
tensor, and chunked statistics remain later steps.
