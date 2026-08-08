# Selective Safetensors Tensor Decoder

`demos/safetensors/tensor_slice.mlpl` validates the complete Safetensors
catalog, locates one named tensor, enforces a caller-supplied payload byte
budget, reads exactly that tensor range, and decodes it in MLPL. The initial
supported set is deliberately small: `U8`, `I8`, `U16`, and `I16`.

Native builtins provide sandboxed `file_size`, bounded `read_bytes`, budgeted
JSON parsing, and record discovery. MLPL owns tensor selection, dtype policy,
little-endian integer decoding, signed conversion, alignment and budget checks,
and result construction. No external decoder is used.

For H header bytes, T catalog entries, and B selected payload bytes, the
current implementation takes O(H + T log T + B) time and retains O(H + T + B)
memory. It performs two catalog/header passes before one payload read, so the
header can be materialized twice sequentially. The payload allocation is at
most `max_read_bytes` and independent of total file size, but this is a bounded
slice—not yet a streaming statistics implementation.

Unsupported dtypes, missing or metadata names, malformed catalogs, invalid
budgets, and tensors larger than the read budget fail closed. IEEE floating
point and wider integers await dedicated exact golden conversions; sub-byte
formats remain outside this decoder.
