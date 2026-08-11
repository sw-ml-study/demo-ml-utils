# Restricted Checkpoint Security Acceptance

The restricted checkpoint saga is accepted for its deliberately narrow
teaching schema. `just checkpoint-security-acceptance` runs all four internal
test suites and then narrates one accepted fixture beside ten independently
named rejection classes. The former external cross-format oracle was retired
when this repository removed direct Python tooling.

## Accepted path

The source must be a bounded, stored, unencrypted, single-disk ZIP with safe
unique names, consistent local/central/end records, exactly one `data.pkl`, and
approved raw storage members. `data.pkl` may use only the primitive evaluator's
integer, text, list, dictionary, mark, and bounded memo instructions. Each
tensor uses the exact five-field declarative schema documented in
[tensor metadata recovery](checkpoint-tensor-metadata.md).

The golden checkpoint contains one I16 `[2,2]` tensor. It becomes an 80-byte
Safetensors artifact whose four values are `[1,-2,300,512]`. Atomic output and
independent internal catalog/selective-decode read-back are required before
success. The official
[Safetensors format](https://github.com/huggingface/safetensors) is the output
authority.

## Adversarial evidence

The self-describing acceptance matrix requires all ten cases to reject:

| Boundary | Fixture/evidence | Rejected condition |
|---|---|---|
| Pickle | `dangerous-global.pt` | GLOBAL/name resolution |
| Pickle | `dangerous-persistence.pt` | persistence callback |
| ZIP | `path-traversal.pt` | unsafe member path |
| ZIP | `encrypted.pt` | encryption flag |
| ZIP | `compressed.pt` | unsupported compression |
| ZIP | `duplicate-member.pt` | duplicate member |
| ZIP | `truncated.pt` | incomplete framing |
| Tensor schema | `tensor-bad-dtype.pt` | dtype outside I8/I16 |
| Tensor range | `tensor-bad-length.pt` | shape/width/length mismatch |
| Tensor range | `tensor-missing-storage.pt` | absent storage member |

Focused tests additionally reject REDUCE, constructors, extensions, unknown
opcodes, malformed stacks/marks/memos, duplicate/missing fields, bad shapes,
and every configured artifact/member/opcode/iteration/stack/node/string/tensor/
rank/parameter/storage/header/JSON/output budget. Pre-write failure preserves
an existing destination.

## Independent oracle

The opt-in oracle first asks MLPL to produce its atomic self-validated output.
A standard-library-only Python program then independently:

1. parses stored local ZIP members without importing or executing pickle;
2. parses the Safetensors little-endian length and duplicate-safe JSON header;
3. compares `data/0` with the entire destination payload byte-for-byte;
4. decodes four little-endian signed 16-bit values; and
5. checks the pinned generated-fixture manifest and both file sizes.

Python is explicitly external, requires no third-party package or download,
and is excluded from `just check`. The oracle's expected tensor manifest is a
fixture golden; it does not independently interpret `data.pkl`, because using
a general pickle implementation would violate the no-execution threat model.

## Claims and limitations

This work demonstrates safe extraction only for the repository's constrained
declarative format. It does not make arbitrary pickle or arbitrary PyTorch
checkpoints safe, support torch rebuild/reduce graphs, resolve persistent
storage callbacks, validate cryptographic provenance, stream outputs larger
than memory, or support compression, ZIP64, sharding, floating/quantized
dtypes, sparse tensors, aliases/views/strides, devices, gradients, optimizer
state, or model code.

MLPL owns the security policy and algorithms. Native primitives provide
bounded reads, file size, generic JSON, and atomic writes. The optional Python
oracle owns only its independent byte/parser comparison. Ordinary numeric byte
arrays are used because packed `u8` and arrays across native-extension
boundaries remain future capabilities.

The serialization path is risky because it may encode executable behavior;
the numeric weight bytes are not themselves executable. Unsupported input
fails closed rather than falling back to PyTorch deserialization.
