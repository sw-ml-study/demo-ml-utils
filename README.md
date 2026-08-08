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

The binary-format foundation is complete: the repository has executable
capability probes, bounded Safetensors header inspection, and a deterministic
arbitrary-name metadata catalog. Bounded tensor-payload analysis is unblocked
but has not started. See [the foundation report](docs/foundation-report.md),
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
The [shipped upstream contract](docs/upstream-contract.md) maps bounded I/O,
decode budgets, and record discovery to executable downstream evidence.

Safetensors header inspection uses bounded range reads and `file_size`, so its
memory depends on the configured header budget rather than total model size.
Arbitrary tensor cataloging is runnable with deterministic `record_keys`,
duplicate-name rejection, and bounded header reads.

## Copyright and license

Copyright (c) 2026 Michael A Wright. See [COPYRIGHT](COPYRIGHT).

This project is available under the [MIT License](LICENSE).
