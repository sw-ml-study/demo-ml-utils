# Observed sw-MLPL Binary-Format Capabilities

Observation date: 2026-08-08. Probe: `just capabilities` using the adjacent
release executable selected by `scripts/select-mlpl`.

Observed binary:

```text
mlpl-repl 0.20.0
Commit: 22f69d47
Timestamp: 2026-08-08T13:21:48-0700
```

These are executable observations, not promises about every sw-MLPL binary.
The routine validation gate reruns the probe against the configured binary.

| Capability | Observed contract | Evidence and consequence |
|---|---|---|
| Byte reads | `read_bytes(path)` and `read_bytes(path, offset, length)` return `Result` containing a rank-1 ordinary array | Exact whole-file and slice round trips; missing path is `Err`; reads clamp at EOF |
| Byte writes | `write_bytes` accepts integer cells `0..255` and returns `Result` | 256 and 1.5 return `Err` without replacing valid contents |
| File size | `file_size(path)` returns metadata byte count as `Result` | No file contents are materialized |
| Read memory | Bounded range materialization is available | A read allocates O(requested length), independent of total file size |
| Byte representation | Ordinary f64-backed array | `type_of(read_bytes(...)? )` is `array`; there is no first-class byte-array kind or reinterpretation view |
| Bit operations | `band`, `bor`, `bxor`, `bnot`, `shl`, `shr`, `bits`, and `from_bits` work on unsigned exact integers below 2^53 | 8-bit pack/view golden cases pass; an operand at 2^53 fails loudly |
| Integer precision | Consecutive mathematical integers cease to be distinguishable after 2^53 | Literals 9007199254740992 and 9007199254740993 compare equal after f64 representation |
| JSON budgets | `parse_json` returns `Result` and accepts `max_bytes`, `max_depth`, and `max_elements` | Valid boundaries parse; byte/depth/element excess, duplicates, and malformed JSON return `Err` |
| Record discovery | `record_keys(record)` returns a deterministic sorted string-list | Arbitrary tensor names can drive `record_get` validation |

## Safetensors consequences

The 8-byte Safetensors header length is an unsigned 64-bit field, but current
MLPL values cannot exactly represent every u64. The demo must enforce a small
header budget before using the decoded length and reject lengths above both the
configured budget and MLPL’s exact integer domain. It must not imply arbitrary
u64 support.

Safetensors headers can now be inspected with two bounded reads: eight prefix
bytes, then at most the configured header budget, after `file_size` proves the
declared header fits the file. Header memory is O(max header bytes), independent
of tensor-data or total file size.

The first implementation uses a 4096-byte header budget and decodes each byte
only after proving it cannot exceed the remaining budget. This prevents an
inexact multiplication even when a hostile prefix encodes u64 maximum. The
fixture suite covers the exact budget, one byte over it, truncation, malformed
JSON, and the 2^53 precision boundary.

## Explicitly absent

- first-class `u8`/typed arrays and zero-copy reinterpretation;
- a binary stream fold whose memory is independent of file size.

Browser/server metric streaming is unrelated to binary file consumption and
does not satisfy the remaining gaps. Large-file tensor statistics can now be
built from repeated bounded reads. The bounded arbitrary-name Safetensors
catalog is now runnable.
