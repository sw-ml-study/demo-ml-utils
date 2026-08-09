# Development workflow

## Validation

Use the thin `justfile` entry points:

```sh
just audit
just tests
just check
```

`just check` is the required pre-commit gate. It validates shell syntax,
licensing, local Markdown links, fixture policy, source permissions, catalog
schema, focused failure cases, and Git whitespace. Recipes delegate to scripts
so direct `./scripts/check` remains available in minimal environments.

Tiny deterministic fixtures belong under `fixtures/` and may be committed.
They must be regular files no larger than 1 MiB. Downloaded or generated model
artifacts belong under ignored `models/` or `artifacts/` directories and are
never part of the default gate.

## Selecting sw-MLPL

The repository never installs or replaces an sw-MLPL executable. Scripts that
need the interpreter call `scripts/select-mlpl`, which selects in this order:

1. the absolute executable path in `MLPL`;
2. `../sw-mlpl/target/release/mlpl-repl` when executable;
3. otherwise, a clear failure with setup instructions.

Examples:

```sh
MLPL=/absolute/path/to/mlpl-repl just mlpl-path
just mlpl-path
```

Capability probes record the selected binary’s version and observed behavior.
They do not install dependencies or assume that a stable binary has features
from the adjacent development checkout.

Run the executable capability contract with `just capabilities`. It verifies
whole-file and bounded range reads, `file_size`, EOF behavior, duplicate JSON
rejection, and all three decode budgets. The routine `just check` gate also runs
it, so the configured interpreter is a required development prerequisite.

Safetensors fixtures are generated without Python or downloaded model data:

```sh
just generate-fixtures
just safetensors-headers
just safetensors-catalog
```

Fixture regeneration also covers deterministic shell-built checkpoint ZIPs.
They contain hand-authored pickle bytes; generation never imports Python,
PyTorch, or a pickle implementation.

The routine gate checks that committed fixture bytes exactly match fresh
generation before running the MLPL decoder tests.

## Demonstrations versus validation

User-facing recipes such as `just safetensors-statistics`, `just gguf-catalog`,
and `just gguf-statistics` first run internal golden/adversarial assertions quietly,
then display an actual narrated scenario. Each output identifies the native
boundary and MLPL-owned algorithm, active budgets, representative result, and
how to interpret it. `tests/test-demo-output` executes every fast demo and
checks this presentation contract; `just check` keeps their narrative hidden.

`just transport` validates and then narrates the ordered visualization JSONL
handoff. The optional `viewer/transport-viewer.html` can inspect pasted
envelopes without a build or network dependency; it is presentation only and
does not replace the MLPL schema and budget checks.

`just sparse-acceptance` follows the same narrative contract but remains
opt-in because it creates a temporary 1 MiB sparse artifact, performs a longer
scalar reduction, and queries platform peak-RSS metrics.
`just gguf-sparse-acceptance` applies the same opt-in measurement to a generated
GGUF I8 tensor with explicit iteration, sample, and report budgets.

`just checkpoint-oracle` is also opt-in. It creates a temporary Safetensors
artifact through MLPL, then uses only Python's standard library to compare the
source ZIP storage member, destination header/payload, and decoded I16 values.
It never imports or executes pickle or PyTorch.
