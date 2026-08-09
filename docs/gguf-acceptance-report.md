# GGUF Bounded Analysis Acceptance Report

## Accepted scope

The GGUF inspection saga now provides little-endian v3 scalar metadata and
multi-tensor cataloging, exact-name selective I8/I16 reads, golden Q8_0 block
dequantization, and sampled mergeable statistics for those three decoded
types. Unsupported active type IDs remain catalog-visible when their extent is
unknown; unsupported decoding fails closed.

`u:gguf_tensor_statistics` validates the complete bounded catalog and resolves
one tensor name exactly. Before payload I/O it derives and checks aligned chunk
size, total iterations, Q8_0 blocks, deterministic stride-sample count,
parameter count, and the fixed nine-field report allowance. Each iteration
decodes at most one configured chunk, folds selected values into a Welford
state, merges that state, and discards the decoded chunk.

Golden tests prove that one-read and one-element-chunk I16 results agree,
independently accumulated partitions merge to the direct result, the complete
Q8_0 ramp has the expected statistics, and stride-eight selection produces
`[-8, -4, 0, 4]` with mean -2 and population variance 20. Sub-block chunks and
insufficient iteration, sample, or output budgets fail before payload work.

## Attribution and bounds

Native code supplies generic sandboxed `file_size` and bounded `read_bytes`.
MLPL owns GGUF validation, exact name lookup, signed and Q8_0 decode,
deterministic sampling, Welford updates, state merging, and report creation.
The format and Q8_0 rules remain pinned to the official
[GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
and [ggml quantization source](https://github.com/ggml-org/ggml/blob/master/src/ggml-quants.c).

For catalog bytes K, tensors T, decoded parameters P, sample count S, and
configured payload chunk C, the pass is O(K + T log T + P) time and O(K + T +
C + S_state) retained memory, where the Welford sample state is constant size.
Decoded MLPL f64 values temporarily add O(C) cells. Q8_0 block decode currently
uses repeated concatenation inside a chunk, so copy work is bounded by the
caller-controlled blocks per chunk rather than total artifact size.

## Measured sparse acceptance

`just gguf-sparse-acceptance` creates and deletes a temporary sparse GGUF with
one 1,048,576-value I8 tensor. It performs 4,096 reads of 256 bytes, validates
all-zero statistics, and enforces a 16,777,216-byte peak-RSS ceiling. It uses
no download and commits no large artifact.

Observed on 2026-08-08 with `mlpl-repl 0.20.0` commit `22f69d47` on macOS:
11,763,712 bytes maximum RSS, below the ceiling. This is evidence for that
binary and platform, not a universal guarantee; the opt-in recipe remeasures
and exits 77 on unsupported platforms. Sandboxed macOS runs may require host
permission for `/usr/bin/time -l` process metrics.

## Limitations and visualization gate

Statistics currently materialize one decoded chunk, use population variance,
and support whole selected I8, I16, or Q8_0 tensors with deterministic global
stride sampling. Floating types, other quantized families, random sampling,
histograms, NaN policy, cross-file aggregation, and a true streaming decode
builtin remain outside the accepted scope.

The visualization saga gate is open: both supported artifact formats now have
bounded catalogs, selective reads, mergeable numeric summaries, explicit
budgets, and measured large-artifact evidence. The next step should define a
renderer-neutral scene/tile IR with provenance and per-level object/payload
budgets; it should consume derived summaries, never raw complete tensors.
