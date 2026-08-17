# Shipped Upstream Capability Contract

Status: fulfilled and conformance-tested against `mlpl-repl 0.20.0`, commit
`6156e869` (2026-08-08). This document records the downstream contract that
originally blocked large-file Safetensors work and distinguishes shipped
behavior from remaining optional hardening. No upstream source is modified by
this repository.

## Bounded filesystem API

```text
read_bytes(path, offset, length) -> ok(byte_array) | err(message)
file_size(path)                  -> ok(byte_count) | err(message)
```

- `path` is resolved inside the configured filesystem sandbox. Missing files,
  traversal outside the sandbox, unavailable filesystem surfaces, and host I/O
  errors return `Err`; they do not terminate an MLPL program.
- `offset` and `length` are scalar, non-negative integers. Wrong kinds,
  negative values, and fractional values are programmer errors and fail
  loudly before I/O.
- A range read seeks to `offset` and materializes at most `length` bytes. It
  does not materialize preceding or following file contents.
- Reads clamp at EOF. Offset at or beyond EOF and zero length both return an
  empty rank-one array inside `Ok`.
- `file_size` obtains the byte count from metadata without reading contents.
- The existing one-argument `read_bytes(path)` whole-file behavior remains
  compatible.

Byte arrays and sizes remain f64-backed MLPL arrays/scalars. Downstream binary
code therefore restricts offsets, lengths, file sizes, and derived arithmetic
to exactly representable integers. Safetensors header lengths are rejected
against a 4096-byte teaching budget before multiplication or allocation.

## Resource and surface policy

The runtime bounds allocation by the caller-provided `length`; it does not add
an independent global maximum range length. This repository treats that as an
explicit caller responsibility:

1. read exactly eight prefix bytes;
2. decode only while proving the value fits `max_header_bytes`;
3. validate `8 + header_length <= file_size`;
4. request at most `max_header_bytes` in the second read.

An implementation-configured global maximum could be defense in depth, but it
is not required for the current demo because no untrusted length reaches the
range builtin without the MLPL budget check.

Filesystem operations are available on native CLI and server-backed surfaces
that install a sandbox root. A surface without filesystem authority returns
`Err`. Browser/server metric streaming is a separate facility and is not used
to justify bounded file-memory claims.

## Companion parsing capabilities

The same live binary completes the safe header-processing contract:

- `parse_json` and `parse_toml` accept `max_depth`, `max_bytes`, and
  `max_elements`;
- `parse_json` rejects duplicate object members before record construction;
- `record_keys(record)` returns a deterministic sorted string-list.

Together these allow MLPL to discover arbitrary tensor names and validate
duplicate-free headers without delegating substantive catalog logic to Rust.

## Downstream acceptance evidence

| Requirement | Executable evidence |
|---|---|
| Exact slice and file size | `probes/capabilities.mlpl` checks a middle slice and four-byte metadata size |
| EOF behavior | Oversized, at-EOF, beyond-EOF, and zero-length reads |
| Filesystem Results | Missing paths and traversal attempts return `Err` |
| Numeric argument errors | `probes/range-domain-error.mlpl` must exit nonzero for a negative offset |
| Allocation bound | `u:read_safetensors_header` requests 8 bytes and then at most 4096 bytes |
| File/header bounds | Truncated prefix/header, oversized u64, and declared-size fixtures fail closed |
| Decode budgets | Capability probe exercises depth, byte, and element boundaries |
| Duplicate names | Duplicate fixture fails during JSON decode |
| Arbitrary names | Catalog test discovers sorted metadata and three tensor keys |

`just check` runs all of this evidence against the configured binary. The
contract is therefore executable rather than inferred from upstream source or
version strings.

## Remaining needs, not regressions

### Bounded length-prefixed stream traversal

Real GGUF tokenizer metadata demonstrates a missing native streaming contract.
MLPL can correctly traverse u64-length-prefixed strings with bounded reads, but
147,209 array elements still create per-iteration interpreter values. The
constant-frame implementation completes under a 16 MiB stack in 5.14 seconds,
yet reaches 505,102,336 bytes maximum RSS on the local SmolLM2 Q8_0 file.

A general primitive—not a GGUF-specific parser—is needed:

```text
scan_length_prefixed(path, offset, count,
                     length_width, max_item_bytes,
                     max_total_bytes, chunk_bytes)
  -> ok({next_offset, item_count, payload_bytes, bytes_read, max_item_seen})
  | err(message)
```

It must use constant native stack and O(chunk_bytes) retained memory, retain no
payloads, return the exact logical offset despite lookahead, enforce sandbox
and arithmetic checks, and provide interpreter/server/compiler parity. A Rust
native extension may provide the same scalar-record contract if this stays out
of core. Until one route exists, the 128 MiB real-file acceptance intentionally
fails; raising stack or memory ceilings is not acceptance.

- First-class typed byte arrays and zero-copy reinterpretation would reduce
  f64 storage overhead but are not required for bounded correctness.
- A general stream/fold abstraction would improve repeated tensor-region
  statistics; bounded reads already permit an explicit fixed-memory loop.
- User-defined function parameters currently reject string-list values, so the
  catalog keeps its `record_keys` walk in one visible `while` loop.
