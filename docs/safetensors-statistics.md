# Bounded Safetensors Statistics

`demos/safetensors/statistics.mlpl` computes count, minimum, maximum, sum,
mean, and population variance for a selected supported integer tensor. It
validates a positive exact chunk budget and a six-field output budget before
filesystem access, validates the complete artifact catalog, then performs
aligned bounded range reads without materializing the complete tensor.

MLPL owns dtype decoding, iterative Welford updates, parallel-state merging,
chunk iteration, and result construction. The within-chunk folds are loops,
so their execution stack is constant rather than proportional to chunk size.
Native code supplies only generic
sandboxed file metadata, bounded byte reads, JSON decoding, and record access.
The fixture suite proves fixed-chunk results match a single-slice golden result
and that independently accumulated partitions merge to the same statistics.

For H header bytes, T tensors, B payload bytes, and C configured chunk bytes,
time is O(H + T log T + B), while retained memory is O(H + T + C). Each read is
at most `floor(C / dtype_width) * dtype_width`; decoded chunk values temporarily
add O(C / dtype_width) f64 cells. The six-field output is constant size. This
logical bound is backed by the opt-in `just sparse-acceptance` high-water test.

## Sparse-artifact acceptance

The opt-in recipe creates a temporary 1 MiB sparse zero-filled U8 tensor,
analyzes it in 256-byte chunks, checks deterministic all-zero statistics, and
deletes it on exit. No large artifact is committed or downloaded. The artifact
is 4096 times the configured chunk budget. Materializing its bytes as ordinary
f64 MLPL cells would add roughly 8 MiB before array overhead to the measured
runtime baseline, putting the process above the 16 MiB peak-RSS ceiling.

On macOS the harness parses bytes from `/usr/bin/time -l`; on Linux it converts
KiB from `/usr/bin/time -v`. Unsupported operating systems exit 77 with an
explicit skip. A supported platform fails if timing metrics are unavailable,
the result is wrong, or peak RSS exceeds 16 MiB. Run it outside a restricted
sandbox when the platform timing tool cannot query process metrics.

Observed on 2026-08-08 with `mlpl-repl 0.20.0` commit `22f69d47` on macOS:
10,158,080 bytes maximum RSS for the 1,048,576-byte artifact and 256-byte
chunks, below the 16,777,216-byte ceiling. This is acceptance evidence for
that binary and platform, not a universal runtime guarantee; the recipe
remeasures rather than trusting the recorded number.

The initial dtype set remains U8, I8, U16, and I16. Variance is population
variance (`m2 / count`); an empty tensor returns six zeros. Floating-point,
wider integer, sub-byte, NaN/Infinity, and sample-variance policies remain
unsupported and fail closed through the selective decoder.
