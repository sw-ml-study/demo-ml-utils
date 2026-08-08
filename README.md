# demo-ml-utils

Practical machine-learning artifact utilities written in sw-MLPL. The project
will demonstrate bounded inspection, validation, visualization, conversion,
and quantization of formats such as Safetensors, GGUF, and restricted
tensor-only checkpoint representations.

The governing principle is to implement algorithms in MLPL whenever the
language can express them. Native or external tools may provide generic I/O,
rendering, interoperability, performance baselines, and validation oracles,
but documentation must identify which layer performs the substantive work.

## Project status

The bounded Safetensors analysis vertical slice is complete: the repository
has executable capability probes, metadata cataloging, selective integer
decoding, fixed-chunk statistics, measured sparse-artifact acceptance, and a
versioned summary IR. GGUF metadata inspection is unblocked but has not
started. See [the bounded-analysis report](docs/bounded-analysis-report.md),
[the foundation report](docs/foundation-report.md),
[the delivery plan](docs/plan.md), [the saga queue](docs/sagas.md), and
[the peer repository audit](docs/peer-repository-audit.md).

Development uses a thin `justfile`; [the development guide](docs/development.md)
documents the validation gate, fixture policy, and non-installing sw-MLPL
binary selection. The [demo catalog](catalog/README.md) records format,
implementation layer, memory contract, required capabilities, and status.
The [capability report](docs/capabilities.md) records executable observations
from the configured interpreter and the resulting Safetensors constraints.
The [bounded Safetensors catalog](docs/safetensors-catalog.md) documents its
validation, attribution, output, and complexity contracts.
The [selective tensor decoder](docs/safetensors-slice.md) documents bounded
integer payload reads, implementation attribution, and current dtype limits.
The [bounded statistics demo](docs/safetensors-statistics.md) adds fixed-chunk
mergeable reductions without reading a complete tensor at once.
Its opt-in sparse-artifact acceptance recipe measures and enforces peak RSS
without downloading or committing a large model.
The [visualization summary IR](docs/safetensors-summary-ir.md) provides a
versioned, budgeted JSON handoff without coupling analysis to a renderer.
The [shipped upstream contract](docs/upstream-contract.md) maps bounded I/O,
decode budgets, and record discovery to executable downstream evidence.

Safetensors header inspection uses bounded range reads and `file_size`, so its
memory depends on the configured header budget rather than total model size.
Arbitrary tensor cataloging is runnable with deterministic `record_keys`,
duplicate-name rejection, and bounded header reads.

## Copyright and license

Copyright (c) 2026 Michael A Wright. See [COPYRIGHT](COPYRIGHT).

This project is available under the [MIT License](LICENSE).
