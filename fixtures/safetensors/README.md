# Safetensors header fixtures

The fixture layout follows the authoritative
[Safetensors format specification](https://github.com/huggingface/safetensors/blob/main/README.md#format):
an eight-byte unsigned little-endian header length, that many bytes of UTF-8
JSON, then tensor data. Hugging Face also documents metadata-only access using
[bounded HTTP range requests](https://github.com/huggingface/safetensors/blob/main/docs/source/metadata_parsing.mdx).

| Fixture | Purpose |
|---|---|
| `valid-small.safetensors` | One four-byte U8 tensor |
| `valid-empty.safetensors` | Valid empty JSON object and no data |
| `boundary-header.safetensors` | Exactly 4096 header bytes using permitted space padding |
| `empty.safetensors` | No length prefix |
| `truncated-prefix.safetensors` | Only four prefix bytes |
| `truncated-header.safetensors` | Declares 16 header bytes but supplies two |
| `malformed-json.safetensors` | Complete declared header containing invalid JSON |
| `oversized-header.safetensors` | Declares 4097 bytes against the demo’s 4096-byte budget |
| `overflow-length.safetensors` | Encodes u64 maximum, outside MLPL’s exact integer domain |

The 4096-byte demo budget is intentionally much smaller than the reference
implementation’s broader defensive limits. It is enough for deterministic
teaching fixtures and ensures the decoder rejects before an inexact f64
multiplication or allocation can occur.

These tests call `file_size`, read the eight-byte prefix, validate the declared
length against file size and the 4096-byte budget, then read only that header
range. Their memory complexity is O(max header bytes), independent of tensor
data and total file size.
