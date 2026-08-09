# Restricted Checkpoint to Safetensors

`just checkpoint-to-safetensors` extracts only catalog-approved raw tensor
ranges from the constrained checkpoint schema, constructs deterministic
Safetensors bytes, replaces the destination atomically, and then validates the
artifact with the repository's independent Safetensors catalog and selective
decoder.

The generated demonstration converts one I16 tensor with shape `[2,2]`. Its
eight source bytes decode to `[1,-2,300,512]`. The output consists of an
eight-byte little-endian header length, a 64-byte JSON header padded with ASCII
spaces to an eight-byte boundary, and the unchanged eight-byte payload: 80
bytes total. This follows the official
[Safetensors format description](https://github.com/huggingface/safetensors),
including data-buffer-relative half-open offsets and complete buffer coverage.

MLPL owns checkpoint validation, tensor/range policy, bounded payload reads,
escaped dynamic-name/header composition through generic JSON, header padding,
little-endian length encoding, payload assembly, budgets, and all self-
validation comparisons. Native code supplies bounded reads, file size,
generic JSON encoding/decoding, and `write_atomic`. Ordinary numeric byte
arrays remain the boundary; packed `u8` arrays are not claimed.

Self-validation recatalogs the written output, checks tensor/parameter/payload
counts, selectively decodes every tensor, rereads each approved source range,
and requires exact value parity. The demo therefore reports 16 source storage
bytes read: eight during extraction and eight during parity validation. Atomic
replacement prevents a torn destination; focused tests also prove that a
failure discovered before writing preserves an existing destination.

GLOBAL/STACK_GLOBAL, REDUCE, object construction/build, extensions,
persistence, unsupported dtype/schema, missing storage, invalid ranges, and
resource excess still fail before output. This path never imports Python or
PyTorch and never asks pickle to resolve an object.

For artifact bytes A, pickle bytes P, selected payload bytes S, and output
tensors T, logical work is O(A+P+S+T), plus the existing graph/member lookup
costs. Current concatenation materializes the complete budgeted output and can
copy repeatedly, so this is not yet a streaming large-checkpoint converter.
Defaults cap both files at 512 bytes, selected storage at 128 bytes, tensors
and rank at four, parameters at 64, and Safetensors header at 256 bytes.
