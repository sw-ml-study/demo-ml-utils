# Declarative Checkpoint Tensor Metadata

`just checkpoint-tensor-metadata` demonstrates a generated two-member
checkpoint whose primitive `data.pkl` declares one tensor and whose `data/0`
member holds eight raw bytes. The output explains the tensor name, I16 dtype,
`[2,2]` shape, four-element parameter count, storage member, relative and
absolute offsets, exact byte count, opcode count, report size, and explicit
zero-payload-read evidence.

This is a constrained teaching schema, not general PyTorch deserialization.
Each root dictionary entry maps a safe unique tensor name to a dictionary with
exactly five fields: `storage`, `dtype`, `shape`, `offset`, and `length`.
Storage must name one validated non-`data.pkl` ZIP member. Dtypes are currently
I8 or I16, shapes are positive bounded integer lists, and `length` must equal
the shape product times dtype width. The complete range must fit its member.

The preceding [primitive machine](checkpoint-primitive-machine.md) accepts no
persistence opcode. This step therefore uses explicit primitive text for a
storage-member reference rather than pickle's persistence callbacks. GLOBAL,
STACK_GLOBAL, REDUCE, constructors/build, extensions, PERSID/BINPERSID,
unknown operations, missing members, duplicate/missing descriptor fields,
unsupported dtypes, bad shapes, and inconsistent byte ranges all fail closed.
No Python/PyTorch object or storage callback exists to invoke.

MLPL owns local member cataloging after full ZIP directory validation, graph
field lookup, schema validation, shape/dtype arithmetic, range validation,
budgets, report construction, and tagged JSON round-trip. Native code supplies
file size, bounded reads, and generic JSON. The current implementation rereads
the small bounded artifact during validation/cataloging and retains the
accepted pickle graph and reports concurrently, so the catalog remains
`whole-file`.

For artifact size A, pickle size P, graph edges E, and tensors T, logical work
is O(A+P+E*T) with bounded linear member lookups. Repeated numeric-array
concatenation and fixed-width tables add copying overhead. Defaults cap the
artifact at 512 bytes, pickle at 256 bytes, members/tensors/rank at four,
parameters at 64, declared storage at 128 bytes, and output at 32768 bytes.
Storage bytes are not read in this step; extraction and Safetensors writing are
the next stage.
