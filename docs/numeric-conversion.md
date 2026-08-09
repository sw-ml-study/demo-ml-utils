# Numeric Conversion and Error Goldens

`just numeric-conversion` sends boundary-heavy values through three explicit
policies: signed i8 truncates toward zero and saturates to -128..127, unsigned
u8 truncates toward zero and saturates to 0..255, and f64 is an identity path.
The demo prints all three outputs, then explains absolute errors, RMSE, maximum
error, and cosine similarity against a deterministic target vector.

The f64 path is intentionally modest. The interpreter uses f64-backed numeric
arrays, so this step does not claim that returning a rounded number creates
f32/f16 storage or byte-level compatibility. Narrow floating encoding belongs
in a later byte-layout step with golden evidence.

MLPL owns finite/magnitude checks, rounding, saturation, vector construction,
metrics, zero-vector cosine policy, and tagged report validation. Native code
only supplies generic JSON encoding and decoding. Unsupported conversion kinds,
empty/rank-mismatched/unequal vectors, NaN or over-budget magnitudes, and value,
iteration, output-value, report-field, encoded-byte, decode-byte, depth, or
element budget violations fail closed.

For N values and J encoded bytes, arithmetic work is O(N) and JSON work is
O(J). The current repeated `concat` vector construction copies growing arrays,
so actual conversion copying is O(N²), deliberately capped at eight values in
the teaching demo. Input, three conversion outputs, error/absolute/squared
temporaries, encoded JSON, and its decoded copy may coexist, each under the
declared value, byte, and element bounds. No filesystem or model payload is
read, so the catalog correctly labels this demo `not-applicable` rather than
claiming chunk-bounded I/O.
