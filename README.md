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

This repository is at the planning and capability-probing stage. See
[the delivery plan](docs/plan.md), [the saga queue](docs/sagas.md), and
[the peer repository audit](docs/peer-repository-audit.md).

Large-file support is a target, not a current claim: sw-MLPL currently offers
whole-file byte reads, while bounded range/seek I/O remains an upstream gate.

## Copyright and license

Copyright (c) 2026 Michael A Wright. See [COPYRIGHT](COPYRIGHT).

This project is available under the [MIT License](LICENSE).
