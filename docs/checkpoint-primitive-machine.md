# Restricted Primitive Pickle Machine

`just checkpoint-machine` demonstrates a deliberately small pickle evaluator.
Its generated protocol-2 fixture describes `{"weight": [1, 2]}`. The demo
shows that result, the intermediate typed nodes, list/dictionary edges, memo
entries, opcode count, encoded report size, and four zero-valued execution
capabilities. It is a demonstration of a readable result and its mechanism,
not a test that merely prints `PASS`; the runner executes adversarial tests
first and then prints the narrated demo.

The evaluator first applies the passive container and opcode inventory from
[the risk-inventory slice](checkpoint-risk-inventory.md). Its only dispatched
value operations are empty dictionary/list, `None`/boolean, bounded integer
and Unicode primitives, mark, append/appends, setitem, and bounded memo
put/get. The result is an inert columnar graph: typed nodes and numeric edge
tables. It never imports a module, looks up a global, calls a callable,
constructs a Python object, or resolves persistence.

GLOBAL/STACK_GLOBAL, REDUCE, object/constructor/build, extension, and
persistence opcode families are rejected before evaluation. Unknown opcodes,
missing memo entries, memo redefinition, malformed stack/mark operations,
multiple roots, trailing bytes, and every resource-limit violation also fail
closed. This does not make arbitrary pickle safe. Python explicitly warns
against unpickling untrusted data and documents `pickletools` as the safer
non-executing inspection route ([pickle security warning](https://docs.python.org/3/library/pickle.html),
[pickletools](https://docs.python.org/3/library/pickletools.html)).

MLPL owns opcode dispatch, stack and memo semantics, node/edge construction,
projection, all budgets, rejection policy, and tagged JSON round-trip
validation. Native code supplies `file_size`, bounded reads, and generic JSON.
The public teaching path currently performs two bounded whole-artifact reads:
one for structural validation and one to copy the accepted `data.pkl` bytes.
Consequently the catalog honestly retains `whole-file` memory behavior.

For artifact size A and pickle size P, logical work is O(A+P+E), where E is
the bounded number of emitted edges. Numeric-array concatenation and scans can
make current copying O(P²+E²); the tiny default fixture is capped at 512
artifact bytes, 128 pickle bytes, 64 opcodes/iterations, 16 stack entries,
nodes, list items, and dictionary items, eight memo entries/mark depth, and a
16384-byte report. Tensor/storage persistence is intentionally unsupported
until the next saga step defines a declarative storage-only policy.
