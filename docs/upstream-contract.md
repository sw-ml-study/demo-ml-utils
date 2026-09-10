# Shipped Upstream Capability Contract

Status: fulfilled and conformance-tested against commit `6156e869`
(2026-08-08, reported as `mlpl-repl 0.20.0`). This document records the
downstream contract that originally blocked large-file Safetensors work and
distinguishes shipped behavior from remaining optional hardening. No upstream
source is modified by this repository.

A second contract, covering array expressiveness rather than binary-format
I/O, is tracked separately in [the blocker record](sw-mlpl-blocker.md) and
enforced by `just array-capabilities`. Its shipped surface is summarized under
"Array expressiveness" below.

Capability claims in this repository pin the **build commit**, never the
version string. Version labels moved independently of content twice during the
convolution work: a fix scheduled as 0.21.1 rode inside 0.21.0, and a build
released as 0.22.0 was withdrawn and rebuilt as 0.21.0 with identical content.
Two binaries reporting the same version can differ in observable semantics, and
one behavior can carry two version strings, so probe exit codes are the
authority.

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

Real GGUF tokenizer metadata demonstrated a missing native streaming contract.
MLPL can correctly traverse u64-length-prefixed strings with bounded reads, but
147,209 array elements still create per-iteration interpreter values. The
constant-frame implementation completes under a 16 MiB stack in 5.14 seconds,
yet reaches 505,102,336 bytes maximum RSS on the local SmolLM2 Q8_0 file.

sw-MLPL commit `b4691193` shipped the general primitive, and `be724494`
followed with packed bounded reads and the offset-collecting variant:

```text
scan_length_prefixed(path, offset, count,
                     length_width, max_item_bytes,
                     max_total_bytes, chunk_bytes)
  -> ok({next_offset, item_count, payload_bytes, bytes_read, max_item_seen})
  | err(message)
```

It uses constant native stack and O(chunk_bytes) retained memory, retains no
payloads, return the exact logical offset despite lookahead, enforce sandbox
and arithmetic checks, and provide interpreter/server/compiler parity. A Rust
native extension may provide the same scalar-record contract if this stays out
of core. This repository consumes the shipped builtin directly and keeps the
128 MiB real-file acceptance as executable regression evidence.

- `read_bytes_packed` now removes f64 expansion from scalar and chunk reads.
  Catalog names are retained as source offsets and lengths and decoded lazily,
  eliminating repeated growth of padded name matrices.
- A general stream/fold abstraction would improve repeated tensor-region
  statistics; bounded reads already permit an explicit fixed-memory loop.
- User-defined function parameters currently reject string-list values, so the
  catalog keeps its `record_keys` walk in one visible `while` loop.
- `tally` also rejects string lists (`expected an array value, got a string`),
  so a string list's length cannot be measured at all. String lists are
  therefore indexable but not measurable: `list_get(parts, i)` works and
  returns a `Result`, so a loop over one must terminate on the `Err` from an
  out-of-range index rather than on a length. Both limitations are
  `ERGONOMICS_ONLY` — downstream code works around them in ordinary MLPL — but
  together they make string lists visibly second-class next to numeric arrays.

## Array expressiveness

Observed on build `60dd94af` and enforced by `catalog/probes.tsv` through
`scripts/check-capability-probes`, which runs in the default gate. A capability
change in either direction fails the gate and forces reconciliation, rather
than silently invalidating this document.

| Capability | Contract | State |
|---|---|---|
| `windows(x, sizes)` | Sliding-window rearrangement emitting `[out_y, out_x, C, kh, kw]`; a `[channel, kernel_y, kernel_x]` kernel aligns by trailing position with no `transpose_axes`, pinned upstream by a test | shipped |
| `compress` label propagation | Axis labels survive filtering as they survive `rotate` | shipped |
| `reduce(:op, a, axes)` | Reduction over a vector of integer axes in one call | shipped |
| `reduce(:op, a, "name")` | Reduction over a single labeled axis | shipped |
| `reduce(:op, a, [names])` | Reduction over a vector of axis *names* | open, `LIBRARY_GAP` |
| Trailing-axis rank broadcasting | A rank-3 kernel broadcasts against rank-5 patches by trailing position | shipped |
| `svg(text, "equation")` | Renders a line of Unicode math to self-contained SVG with no LaTeX toolchain, MathJax, or network | shipped |

The one open item does not block work here: the axis-name vector is expressible
in ordinary MLPL by resolving labels against `labels(x)` and passing the
resulting integer vector.

With broadcasting shipped, the convolution equation is now writable as one
line, verified exact against the `conv2d` oracle by
`probes/rank-broadcast.mlpl`:

```mlpl
y = reduce(:add, windows(x, [kh, kw]) * w, [2, 3, 4])
```

The im2col spelling remains the faster of the two and needs no broadcasting at
all:

```mlpl
cols = reshape(windows(x, [kh, kw]), [oy * ox, c * kh * kw]);
y    = matmul(cols, flatten(kernel))
```

Measured on build `f4485823`, `[8, 32, 32]` input against `[16, 8, 3, 3]`
filters: that form runs in 1.198 ms against native `conv2d` at 1.230 ms and
agrees exactly, while a broadcast-workaround formulation of the same result
takes 211.3 ms, replicates 1,036,800 cells, and agrees only to 1.42e-13.
Array-expressed convolution is at parity with the native builtin; earlier
drafts of this repository's documentation reported a 172x deficit, which
described one workaround rather than the language, and has been withdrawn.
