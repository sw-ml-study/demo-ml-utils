# Binary-Format Foundation Report

Report date: 2026-08-08. The full repository gate passes against
`mlpl-repl 0.20.0`, commit `6156e869` (built
`2026-08-08T12:29:42-0700`). The `binary-format-foundations` deliverables are
complete, and Saga 2 is unblocked but not started.

## Acceptance evidence

`just check` validates the catalog, copyright/license policy, documentation
links, generated fixtures, MLPL sources, expected-success and expected-failure
tests, and the pre-commit gate. Its executable components report:

```text
PASS capability probe
PASS Safetensors header fixtures
PASS Safetensors header tests
PASS Safetensors catalog
PASS Safetensors catalog demo
```

The committed Safetensors set contains tiny valid, empty, boundary, malformed,
duplicate-name, truncated, oversized, schema-invalid, unsupported-dtype,
overlap, hole, size-mismatch, and out-of-bounds cases. It requires no network
access or model download.

## Runnable demos

| Demo | Result | Substantive implementation | Logical complexity | Actual memory behavior |
|---|---|---|---|---|
| `capability-probe` | Runnable in the default gate | MLPL assertions exercise generic runtime capabilities | O(N) in the tiny probe payload | Whole-file probe reads materialize O(N); this demo makes no large-file claim |
| `safetensors-catalog` | Runnable in the default gate | MLPL decodes and validates the header and builds aggregates; native code supplies generic bounded I/O, JSON decode, and record discovery | O(H + T log T) time for H header bytes and T tensors; O(H + T) logical space | Two range reads materialize 8 bytes and at most 4096 header bytes; parsed header and catalog retain O(H + T); tensor payload is never read |

The catalog's `mlpl-native` label means MLPL owns format-specific validation
and aggregation while native builtins provide generic services. It does not
mean the filesystem or JSON parser is implemented in MLPL. No external tool
performs substantive work in either runnable demo.

## Foundation capability boundary

The live binary provides sandboxed `file_size` and bounded
`read_bytes(path, offset, length)` Results, ordinary f64-backed byte arrays,
budgeted duplicate-safe JSON decoding, and deterministic sorted
`record_keys`. The Safetensors implementation validates the eight-byte header
length before requesting the bounded header, then validates names, metadata,
dtypes, shapes, offsets, coverage, and file bounds in MLPL.

The 4096-byte teaching budget deliberately limits catalogable headers. It
makes header memory independent of total artifact size but is not a claim that
all real model headers fit. Current byte storage has f64 overhead and no typed
array or zero-copy reinterpretation. There is no generic binary stream/fold;
fixed-memory payload analysis must loop over bounded reads. The current
user-function binder cannot accept a string-list parameter, so the catalog's
key walk remains one visible `while` loop. Byte-aligned dtypes are cataloged;
sub-byte or newly introduced dtypes fail closed pending dedicated packing
tests.

## Saga 2 gate decision

`bounded-safetensors-analysis` is **unblocked, not started**. Its prerequisite
range reader, file-size query, decode budgets, duplicate rejection, and
arbitrary-name discovery are shipped and executable. The foundation already
covers exact slices, EOF clamping, zero-length reads, missing and traversing
paths, invalid numeric arguments, hostile header lengths, truncation, and the
caller-enforced allocation budget.

Saga 2 still must deliver:

1. selective tensor-region reads and supported dtype decoding;
2. mergeable statistics using a fixed chunk-size bound;
3. a sparse artifact larger than the test memory budget plus measured peak
   memory;
4. a versioned JSON visualization-summary IR and headless validation.

The recommended first new step is selective slice decoding for a small,
byte-aligned dtype set. It should reuse the existing range conformance evidence
and add golden numeric vectors before statistics are introduced. The
`safetensors-statistics` catalog entry therefore remains `gated`: its runtime
I/O prerequisite is available, but dtype decoding and mergeable statistics are
not implemented.
