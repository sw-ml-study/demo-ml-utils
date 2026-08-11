# Quantization and Conversion Acceptance Report

The `native-quantization-and-conversion` saga's bounded teaching slice is
complete. The default gate now covers explicit i8/u8 conversion policies,
absolute/RMSE/maximum/cosine goldens, symmetric INT8 packing, GGUF-compatible
Q8_0 blocks accepted by the pre-existing decoder, an explicitly non-GGUF
teaching Q4 layout, and a deterministic atomic single-tensor
Safetensors-to-GGUF writer with catalog and decoded-value read-back.

## Reproducible external evidence

The former external oracle was retired when direct Python tooling was removed.
MLPL still writes and self-validates the tiny I16 artifact. An independent
consumer can parse its header,
metadata, tensor descriptor, alignment, and payload and compares a canonical
JSON record. The expected file is 166 bytes with SHA-256
`884f3fcbef283b2848da263b3bfe5da375f3843fad66ec7afc1ea25ee081062f`,
GGUF v3, architecture `demo`, type 25, shape `[3]`, relative offset zero, and
values `[-32768,-2,32767]`. No package installation or download is performed.

The adapter also reports whether `llama-quantize` is available through
`$LLAMA_QUANTIZE` or `PATH`. It does not run it on this artifact: the current
writer emits one signed-integer teaching tensor, not an eligible floating model
for llama.cpp quantization. Availability is useful future setup evidence;
forcing a predictable rejection would not validate numeric compatibility.

## Attribution and bounds

MLPL performs every substantive conversion, quantization, binary16/nibble/byte
packing, GGUF structure decision, decode, metric, and self-validation in the
default workflows. Native primitives provide bounded reads, file size, JSON,
and atomic replacement. Python participates only in the named opt-in oracle
recipe; llama.cpp is capability-detected only. Temporary oracle artifacts are
created under ignored `tmp/` and removed on exit.

Each demo has explicit value, magnitude, iteration, output, block, byte, decode,
metadata, tensor, rank, or normalization caps appropriate to its work. Logical
numeric work is linear in values/blocks and writer work is linear in source,
output, and read-back sizes. Current MLPL array construction repeatedly uses
`concat`, making actual copy work quadratic in bounded vector/output length;
the teaching demos therefore stay at 32–64 values and at most 512 output bytes.

## Accepted limitations and next gate

The accepted slice does not provide f16/f32 storage conversion, arbitrary
multi-tensor/rank dimension mapping, streamed writing, GGUF Q4_0/K/IQ families,
external quantizer bit parity, model-scale conversion, or performance claims.
The Q4 format is intentionally repository-specific. The writer supports only
rank-one I8/I16 preservation. These are explicit limits, not silent fallbacks.

The next recommended saga is `restricted-checkpoint-extraction`: begin with a
passive ZIP/pickle opcode inventory and risk report, then build only a bounded
allow-listed non-executing parser. Native PyTorch/pickle loading must never be
used on untrusted fixtures as a hidden convenience.
