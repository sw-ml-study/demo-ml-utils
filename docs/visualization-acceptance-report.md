# Visualization Acceptance Report

The `model-visualization` saga is complete. `just transport` validates and
then demonstrates a deterministic four-message JSONL handoff: scene overview
(LOD 0), tensor-city catalog geometry (LOD 1), selected distribution/surface
detail (LOD 2), and Q8_0 reconstruction error (LOD 3). The displayed sequence,
LOD, envelope sizes, and total size make the progressive handoff inspectable
rather than reducing the demo to a pass marker.

Each version-1 `sw-ml-study.visualization-message` envelope contains kind,
sequence, LOD, provenance, logical object count, exact nested-payload byte
count, and nested JSON. Validation rejects unknown or missing fields, unknown
kinds, kind/payload schema mismatches, altered round trips, and violations of
payload, message, total, object, LOD, sequence, provenance, JSON-depth,
JSON-element, message-count, or iteration budgets. The teaching demonstration
allows four messages, 12 logical objects, 512 payload bytes, 1024 bytes per
message, and 4096 bytes total.

MLPL owns the message-kind policy, schema association, sequence/LOD mapping,
provenance and byte accounting, nested-payload validation, deterministic
envelope round trip, ordering, and JSONL construction. Native facilities only
supply generic JSON encode/decode and stdout or file transport. No socket,
server, browser, WASM runtime, or external renderer is required by the default
gate.

`viewer/transport-viewer.html` is an optional dependency-free inspector for
pasted, already-validated JSONL. It safely renders envelope metadata using DOM
text nodes. It is deliberately not an independent validation oracle or a claim
of a complete 3D renderer; the headless MLPL golden and adversarial tests remain
authoritative.

For aggregate nested payload size P and encoded message size J, construction
and validation take O(P+J) time and retain O(P+J) data. The current design may
coexist with nested payload strings, encoded envelopes/JSONL, and decoded
copies, but each is covered by explicit byte and element caps. It does not yet
stream envelope construction, operate a live transport, automate a browser,
or render geometry.

The recommended next saga is `native-quantization-and-conversion`. The shipped
Q8_0 decoder, reconstruction metrics, error tile, and transport contract make
numeric conversion goldens and a symmetric INT8 encoder the smallest useful
next forcing function before writers or more elaborate quantizers.
