# Observed sw-MLPL Binary-Format Capabilities

Observation date: 2026-08-08. Probe: `just capabilities` using the adjacent
release executable selected by `scripts/select-mlpl`.

Observed binary:

```text
mlpl-repl 0.20.0
Commit: 5ef1ef72
Timestamp: 2026-08-08T10:19:01-0700
```

These are executable observations, not promises about every sw-MLPL binary.
The routine validation gate reruns the probe against the configured binary.

| Capability | Observed contract | Evidence and consequence |
|---|---|---|
| Byte reads | `read_bytes(path)` returns `Result` containing a rank-1 ordinary array | Exact `[0,1,127,255]` round trip; missing path is `Err` |
| Byte writes | `write_bytes` accepts integer cells `0..255` and returns `Result` | 256 and 1.5 return `Err` without replacing valid contents |
| Read memory | Whole-file materialization | No offset, length, seek, handle, or chunk argument exists |
| Byte representation | Ordinary f64-backed array | `type_of(read_bytes(...)? )` is `array`; there is no first-class byte-array kind or reinterpretation view |
| Bit operations | `band`, `bor`, `bxor`, `bnot`, `shl`, `shr`, `bits`, and `from_bits` work on unsigned exact integers below 2^53 | 8-bit pack/view golden cases pass; an operand at 2^53 fails loudly |
| Integer precision | Consecutive mathematical integers cease to be distinguishable after 2^53 | Literals 9007199254740992 and 9007199254740993 compare equal after f64 representation |
| JSON budgets | `parse_json` returns `Result` and accepts `max_bytes`/`max_depth` | Valid bounded header parses; byte/depth excess and malformed JSON return `Err` |

## Safetensors consequences

The 8-byte Safetensors header length is an unsigned 64-bit field, but current
MLPL values cannot exactly represent every u64. The demo must enforce a small
header budget before using the decoded length and reject lengths above both the
configured budget and MLPL’s exact integer domain. It must not imply arbitrary
u64 support.

Small fixtures can be inspected with `read_bytes`, bit operations, byte-to-text
decoding, and budgeted JSON today. Such an implementation has O(file size)
memory and must be cataloged as `whole-file`.

## Explicitly absent

- bounded byte-range reads, seekable handles, or consumable file chunks;
- first-class `u8`/typed arrays and zero-copy reinterpretation;
- a binary stream fold whose memory is independent of file size.

Browser/server metric streaming is unrelated to binary file consumption and
does not satisfy these gaps. Large-file Safetensors statistics and every
`chunk-bounded` catalog entry remain gated until a separately authorized
upstream capability is available and conformance-tested here.
