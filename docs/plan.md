# ML Artifact Utility Demo Delivery Plan

## Mission and proof standard

Demonstrate that sw-MLPL can inspect, analyze, transform, visualize, and
validate real ML artifacts while keeping algorithmic work visible in MLPL.
The repository is a forcing function for general binary/data-processing
capabilities, not a wrapper collection and not another ML-algorithm survey.

Every deliverable identifies one of three implementation layers:

1. **MLPL implementation** — parsing, analysis, or transformation is expressed
   in MLPL.
2. **MLPL plus native capability** — MLPL owns the algorithm while a generic
   runtime boundary provides range I/O, transport, or rendering.
3. **External interoperability** — a named tool is an explicit fallback,
   compatibility implementation, performance baseline, or validation oracle.

No demo may describe layer 2 or 3 work as a native MLPL implementation.

## Current capability boundary

The adjacent sw-MLPL language currently documents:

- sandboxed whole-file and bounded `read_bytes(path, offset, length)`,
  `file_size(path)`, and `write_bytes(path, bytes)`;
- f64-backed byte values and fixed-width numeric bit operations such as
  `band`, `bor`, `bxor`, `bnot`, `shl`, and `shr`;
- JSON parsing/encoding with depth, byte, and element budgets and ordinary
  array reductions;
- browser/server metric streaming, which is not a consumable binary-file
  stream and must not be presented as one.

Executable probes pin these facts against the configured binary. Bounded
Safetensors header inspection and arbitrary tensor discovery are available.
First-class typed arrays, reinterpretation, and streaming folds remain
valuable follow-ups driven by executable need.

## Architecture

```text
artifact -> bounded reader -> format parser -> tensor catalog
                                      |              |
                                      v              v
                              selective decoder  statistics
                                      \              /
                                       visualization IR
                                               |
                                browser 3D / JSON / CLI
```

The browser receives derived summaries and requested level-of-detail tiles,
never the whole artifact. A CLI/server owns sandboxed file access. Parsers and
reducers remain MLPL wherever the language can express them.

## Delivery phases

### Phase 0 — repository and capability contract

- Establish licensing, AgentRail instructions, thin validation conventions,
  fixtures, and a demo/catalog schema.
- Pin how `$MLPL` or an adjacent build is selected without installing it.
- Probe whole-file byte I/O, bit operations, JSON limits, integer exactness,
  and error behavior.
- Record the smallest upstream contract for bounded `read_range`/seek-like
  access, including Result errors, sandbox rules, offsets, overflow, and EOF.

Status: fulfilled by bounded `read_bytes`, `file_size`, the decode-budget trio,
duplicate-key rejection, and deterministic `record_keys`; see
[upstream-contract.md](upstream-contract.md) for conformance evidence.

Acceptance: `just check` runs deterministic repository checks, and every
planned claim is marked executable, gated, or external.

### Phase 1 — Safetensors vertical slice

- Generate tiny valid and malformed fixtures locally; do not require model
  downloads in the default gate.
- Parse the 8-byte little-endian header length and bounded JSON header.
- Validate names, dtypes, shapes, offsets, overlap, ordering assumptions,
  truncation, duplicate metadata, integer overflow, and file bounds.
- Produce a tensor catalog and aggregate parameter/byte counts.
- After bounded range I/O exists, selectively read tensor regions and compute
  mergeable statistics with measured O(chunk-size) memory.

Acceptance: small fixtures work today without false large-file claims; the
later large-file test analyzes a sparse artifact larger than the configured
memory budget while staying below a documented high-water mark.

Current status: bounded arbitrary-name metadata cataloging is runnable. Tensor
payload selection, U8/I8/U16/I16 decoding, fixed-chunk mergeable statistics,
opt-in sparse-artifact high-water acceptance, and a headlessly validated
single-tensor visualization summary IR are runnable. The completed
[bounded-analysis report](bounded-analysis-report.md) records acceptance,
attribution, complexity, limitations, and the exact GGUF gate decision.

### Phase 2 — GGUF inspection and decoding

- Parse magic/version, metadata, tensor descriptors, alignment, offsets, and
  tensor types before touching tensor payloads.
- Add unquantized decoding, then one simple block format (Q8_0), with golden
  blocks checked against a named reference implementation.
- Add sampled/mergeable statistics and quantization-block summaries.

Acceptance: arbitrary unsupported tensor types are cataloged without decode;
supported selected regions decode within the same bounded-memory contract.

Current status: bounded GGUF v3 scalar metadata and multiple-tensor cataloging
are runnable. Active tensor type IDs remain visible without decode; known
simple extents receive overlap/file-bound validation. Exact-name selective I8
and I16 payload reads and signed little-endian decoding are runnable under an
explicit read budget. Exact Q8_0 block extents and selective dequantization are
runnable with binary16-scale golden evidence; other floating and quantized
types remain later work. Deterministic stride sampling and mergeable statistics
are runnable for I8, I16, and Q8_0, with sparse-artifact peak RSS measured in
the [GGUF acceptance report](gguf-acceptance-report.md).

### Phase 3 — hierarchical 3D visualization

- Define a renderer-neutral JSON scene/tile IR with stable IDs, labels,
  positions, scalar attributes, links, and provenance.
- Implement tensor-city overview, layer/tensor drilldown, distribution and
  sampled-surface views, and quantization-block inspection.
- Serve LOD 0 model summaries through LOD 4 selected block/region data.

Acceptance: object and payload budgets are enforced at every LOD; a headless
snapshot validates the IR independently of the browser renderer.

Current status: scene/tile IR version 1 is runnable for one bounded
Safetensors tile and one bounded GGUF tile with stable IDs, provenance, an
explicit comparison link, deterministic golden JSON, and object/link/label/
output/decode budgets. Deterministic tensor-city layout is also runnable over
both complete fixture catalogs with columnar stable IDs, name hierarchy,
districts, positions, extents, heights, scalar attributes, and headless tagged
JSON validation. Selected-tensor distribution and sampled-surface tiles are
also runnable for accepted integer and Q8_0 paths. Quantization comparison
tiles remain the next step.

### Phase 4 — quantization, repacking, and conversion

- Implement F32-to-F16/BF16, symmetric INT8, Q8_0, then simple Q4 in MLPL as
  capabilities permit; do not begin with K/IQ quant families.
- Compare original, quantized, and dequantized tensors using size, RMSE,
  maximum error, cosine similarity, and deterministic samples.
- Write/validate GGUF only after reader and block round trips are trustworthy.
- Provide explicit external llama.cpp/Hugging Face routes as optional oracles
  and fallbacks, never as hidden default behavior.

Acceptance: byte-level golden vectors and round-trip invariants pass, and the
documentation attributes every operation to MLPL/native/external code.

### Phase 5 — restricted checkpoint extraction

- Recognize PyTorch ZIP/pickle structure passively and produce a risk report.
- Interpret only an allow-listed, non-executing stack-machine subset needed to
  recover primitive containers, tensor metadata, and storage references.
- Reject global lookup, arbitrary construction/call/reduce behavior, extension
  codes, persistent references outside the explicit tensor-storage policy, and
  resource-limit violations.
- Extract tensor bytes to Safetensors and compare names, shapes, dtypes, byte
  ranges/hashes, and numeric samples with an explicit trusted oracle.

Acceptance: adversarial fixtures execute nothing, unsupported constructs fail
closed, and successful output contains tensor data plus declarative metadata
only. Documentation says the serialization path is risky—not the weights.

## Cross-cutting gates

- Default tests use generated, redistributable, tiny fixtures.
- Large and external tests are opt-in, with exact prerequisites and checksums.
- Parsers enforce byte, depth, entry-count, shape-rank, allocation, and output
  budgets before allocation or iteration.
- Each demo documents logical complexity, actual current copy/allocation
  behavior, peak-memory methodology, and unsupported cases.
- Format specifications and security claims must cite authoritative sources
  when implementation begins; this research transcript is direction, not a
  normative format specification.
- Upstream capability work belongs in `../sw-mlpl` only under separate user
  authorization. This repository records executable requests and remains a
  consumer.

## Recommended next increment

Continue `model-visualization` from [sagas.md](sagas.md) with Q8_0
quantization-block and before/after error tiles. Keep every user-invoked `just`
demo narrative and self-describing.
