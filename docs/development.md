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
```

The routine gate checks that committed fixture bytes exactly match fresh
generation before running the MLPL decoder tests.
