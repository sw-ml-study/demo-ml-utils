# Bounded Safetensors Analysis Closeout

Report date: 2026-08-08. The full default gate and opt-in sparse acceptance
pass against `mlpl-repl 0.20.0`, commit `22f69d47` (built
`2026-08-08T13:21:48-0700`). The `bounded-safetensors-analysis` deliverables
are complete.

## Acceptance evidence and runnable demos

`just check` validates repository policy, generated fixtures, capability
contracts, expected failures, header and catalog behavior, selective decoding,
mergeable statistics, and deterministic headless summary JSON. No network or
external decoder is used.

| Demo | Default | Substantive MLPL work | Logical complexity | Actual allocation/copy behavior |
|---|---:|---|---|---|
| `capability-probe` | yes | Executable assertions over the configured runtime | O(N) in tiny probe input | Whole probe payloads are materialized; no large-file claim |
| `safetensors-catalog` | yes | Header length, schema, dtype/shape/offset/layout validation and aggregates | O(H + T log T) time, O(H + T) space | Two bounded reads; no tensor payload read; header capped at 4096 bytes |
| `safetensors-slice` | yes | Tensor selection, integer dtype policy, little-endian and signed decoding | O(H + T log T + B) logical time, O(H + T + B) space | Selected B-byte payload is materialized as bytes and decoded f64 cells; repeated `concat` can copy growing chunk arrays |
| `safetensors-statistics` | yes | Aligned chunk loop, Welford updates, parallel-state merge, six-field result | O(H + T log T + B) logical time, O(H + T + C) retained space | Reads at most aligned chunk C; decoded values use f64 cells; per-value `concat` makes current copy work dependent on C, so small fixed chunks are materially faster |
| `safetensors-summary` | yes | Versioned schema, stable IDs, provenance, budget preflight, validation | O(H + T log T + B + J) logical time, O(H + T + C + J) space | Statistics are recomputed through bounded reads; the conservative preflight and exact J-byte JSON coexist during round-trip validation |

H is header bytes, T tensors, B selected tensor bytes, C chunk bytes, and J
encoded summary bytes. Native code supplies generic sandboxed `file_size`,
bounded `read_bytes`, budgeted JSON decode, deterministic record discovery,
and JSON encode. All format-specific decisions, decoding, reductions, and IR
construction above are MLPL. `/usr/bin/time` is only an opt-in measurement
oracle.

## Measured memory acceptance

`just sparse-acceptance` creates an uncommitted temporary 1,048,576-byte sparse
U8 tensor, analyzes it in 256-byte chunks, verifies 1,048,576 zero values and
zero aggregates, and deletes it. On the binary and macOS host above, maximum
RSS was **10,158,080 bytes**, below the **16,777,216-byte** ceiling. The
artifact is 4096 times the chunk budget. Materializing its bytes as f64 cells
would add about 8 MiB before array overhead to the roughly 10 MiB runtime
baseline and cross the ceiling.

The acceptance originally exposed recursive within-chunk stack growth; both
decoding and Welford folds are now iterative. The measurement is platform and
binary evidence, not a universal promise, so the Darwin/Linux harness
remeasures on every opt-in run and exits 77 on unsupported platforms.

## Resource and security boundary

- Files remain inside the runtime sandbox; missing and traversing paths return
  Results, and payload offsets are derived only from a fully validated catalog.
- Header reads are capped at 4096 bytes. JSON has explicit depth, byte, and
  element budgets; duplicate keys fail before record construction.
- Shape products, offsets, lengths, and derived arithmetic must remain exact
  in the f64 integer domain and within caller parameter/read budgets.
- Payload reads are element-aligned and capped by either the selective-read or
  statistics chunk budget before I/O.
- Statistics output is fixed at six fields. Summary IR requires four objects,
  conservatively preflights output bytes before construction/encoding, checks
  exact encoded size, and round-trips under decode budgets.
- Tiny redistributable fixtures are the default. The sparse artifact is local,
  opt-in, temporary, and contains no downloaded model data.

Supported payload decoding is deliberately limited to U8, I8, U16, and I16.
The metadata catalog recognizes other byte-aligned dtypes for layout checking,
but F16/BF16/F32/F64, 32/64-bit integers, sub-byte formats, NaN/Infinity
policy, sample variance, and quantized blocks are not decoded. The v1 summary
describes one selected tensor; it is not a multi-tensor scene, geometry/LOD
schema, or browser renderer.

## GGUF gate decision

The `gguf-inspection` saga is **unblocked, not started** for metadata catalog
work. Bounded file size/range reads, exact byte and bit operations below 2^53,
allocation budgets, iterative folds, deterministic records, generated-fixture
conventions, and measured-memory infrastructure are sufficient to parse a
bounded GGUF envelope and directory. This decision does not claim that GGUF
tensor decoding or quantization is already supported.

The recommended first vertical slice is a tiny generated GGUF v3 fixture and
malformed variants covering magic, version, tensor/metadata counts, alignment,
one conservative scalar metadata subset, and tensor descriptors without
reading tensor payloads. It must pin the authoritative GGUF specification,
reject unsupported metadata/tensor types while retaining catalog visibility
where possible, budget every count/string before allocation, and fail closed
on u64 values outside the exact configured domain. Unquantized selective
decoding and Q8_0 golden blocks belong in later steps.
