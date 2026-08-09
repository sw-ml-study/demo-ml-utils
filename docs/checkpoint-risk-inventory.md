# Passive Checkpoint Risk Inventory

`just checkpoint-inventory` reads two deterministic shell-built PyTorch-style
ZIP fixtures and reports pickle opcode risk without importing Python or
PyTorch, invoking a deserializer, resolving a global, constructing an object,
or evaluating a stack instruction. The report schema is
`sw-ml-study.checkpoint-risk`, version 1, and always carries
`execution_performed: 0`.

The container subset is ordinary single-disk ZIP with stored, unencrypted
members, matching local/central/end records, no extras/comments/data
descriptors, safe relative unique names, and a required `data.pkl`. The current
public teaching path accepts exactly that one member; a bounded multi-member
directory pass is retained for later storage work. Traversal, backslashes,
NUL/empty names, duplicates, encryption, compression, truncation, mismatched
directories, and trailing/commented structures fail closed.

The pickle scanner understands the bounded argument framing needed by its
protocol-2 fixtures and classifies known declarative operations separately from
GLOBAL/STACK_GLOBAL, REDUCE, constructor/build, extension, and persistence
families. A benign dictionary/list stream has protocol 2, 12 declarative
opcodes, two memo operations, maximum mark depth one, and no dangerous opcode.
A three-opcode stream naming `GLOBAL os.system` receives risk `high`; it is
only counted and skipped according to its text framing. Unknown opcodes fail
because their argument lengths cannot be skipped safely.

Python's documentation warns never to unpickle untrusted or tampered data, and
documents `pickletools` as safer for untrusted inspection because it does not
execute pickle bytecode ([pickle security warning](https://docs.python.org/3/library/pickle.html),
[pickletools](https://docs.python.org/3/library/pickletools.html)). PyTorch
documents its modern `torch.save` layout as an uncompressed ZIP64 archive with
`data.pkl`, storage members, byte order, and version entries
([PyTorch serialization semantics](https://docs.pytorch.org/docs/stable/notes/serialization.html)).
ZIP field decisions are pinned to PKWARE's maintained
[APPNOTE](https://support.pkware.com/pkzip/appnote). This first slice is
smaller than general ZIP64/PyTorch output by design.

MLPL owns ZIP/pickle framing, little-endian fields, path and feature policy,
opcode/argument classification, counters, risk decisions, and report
round-trip validation. Native code supplies file size, the single bounded
whole-artifact read, and generic JSON. The catalog therefore says
`whole-file`, not `chunk-bounded`.

For artifact bytes A and pickle bytes P, logical work is O(A+P). The current
implementation materializes the bounded artifact, name/pickle slices, report
JSON, and decoded report together; repeated masks and concatenations can add
O(A²) copying. Default fixtures are at most a few hundred bytes, with explicit
512-byte artifact, 128-byte pickle, 64-opcode/iteration, and 4096-byte report
caps. This is a passive risk inventory—not yet a safe pickle evaluator or
tensor extractor.
