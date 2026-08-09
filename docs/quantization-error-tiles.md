# Q8_0 Quantization Error Tile

`just quantization-error` builds schema `sw-ml-study.q8-error-tile`, version 1,
from the generated 34-byte GGUF Q8_0 block and an explicit 32-value reference.
LOD 3 retains the stable parent ID, binary16 scale, signed quants,
dequantized/reference/error vectors, byte sizes, compression ratio, RMSE,
maximum absolute error, and cosine similarity.

The golden reference is the decoded `-8..7.5` ramp shifted by 0.5. Every error
is therefore -0.5, RMSE and maximum error are 0.5, cosine is
0.9941520467836257, and the 128-byte F32 reference is 3.7647 times the 34-byte
block. Two zero vectors have cosine 1; exactly one zero vector has cosine 0.
Non-finite values fail generic JSON encoding.

MLPL owns catalog validation, Q8_0 decode, signed quants, pointwise and
aggregate metrics, provenance, and tagged JSON validation. Native code only
supplies bounded reads and serialization. Payload, block, parameter,
reference, metric, point, object, iteration, value, output, depth, and element
budgets fail closed. Golden tests include the ggml-compatible block, metric
vectors, zero policy, deterministic JSON, and adversarial budgets.

The tile can now be carried as the final LOD 3 message in the
[bounded visualization transport](visualization-acceptance-report.md), after
the scene, tensor-city, and selected-detail messages.

For N points and J JSON bytes, work and retained memory are O(N+J). Reference,
dequantized, quant, error, encoded, and decoded copies coexist under the strict
32-point/8192-byte teaching caps. Encoding, arbitrary blocks, streamed metric
folds, other quantizers, and a full 3D renderer remain later work.
