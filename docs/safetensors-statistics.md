# Bounded Safetensors Statistics

`demos/safetensors/statistics.mlpl` computes count, minimum, maximum, sum,
mean, and population variance for a selected supported integer tensor. It
validates a positive exact chunk budget and a six-field output budget before
filesystem access, validates the complete artifact catalog, then performs
aligned bounded range reads without materializing the complete tensor.

MLPL owns dtype decoding, Welford updates, parallel-state merging, chunk
iteration, and result construction. Native code supplies only generic
sandboxed file metadata, bounded byte reads, JSON decoding, and record access.
The fixture suite proves fixed-chunk results match a single-slice golden result
and that independently accumulated partitions merge to the same statistics.

For H header bytes, T tensors, B payload bytes, and C configured chunk bytes,
time is O(H + T log T + B), while retained memory is O(H + T + C). Each read is
at most `floor(C / dtype_width) * dtype_width`; decoded chunk values temporarily
add O(C / dtype_width) f64 cells. The six-field output is constant size. This
logical bound is executable but its process high-water mark is measured in the
next opt-in sparse-artifact step.

The initial dtype set remains U8, I8, U16, and I16. Variance is population
variance (`m2 / count`); an empty tensor returns six zeros. Floating-point,
wider integer, sub-byte, NaN/Infinity, and sample-variance policies remain
unsupported and fail closed through the selective decoder.
