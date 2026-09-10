# demo-ml-utils

Practical machine-learning artifact utilities written in sw-MLPL. The project
demonstrates bounded inspection, validation, visualization, conversion, and
quantization for Safetensors, GGUF, and restricted tensor-only checkpoints.

Substantive algorithms stay in MLPL wherever the language can express them.
Native or external tools are limited to generic services such as I/O,
rendering, interoperability, performance measurement, and independent
validation. Each demo documents that boundary explicitly.

## What is runnable

Each area below has runnable demos with narrated output. The
[documentation index](docs/README.md) describes each one; the
[demo catalog](catalog/README.md) is the machine-readable inventory.

| Area | What it covers | Status |
|---|---|---|
| [Safetensors](docs/README.md#safetensors) | Bounded header inspection, metadata cataloging, selective decoding, chunked statistics | Accepted |
| [GGUF](docs/README.md#gguf) | v3 catalog, selective tensor decoding, Q8_0 block decoding with ggml parity | Accepted |
| [Visualization](docs/README.md#visualization) | Renderer-neutral scene/tile IR, tensor-city layout, detail and error tiles | Accepted |
| [Quantization and conversion](docs/README.md#quantization-and-conversion) | Numeric goldens, symmetric INT8 and Q8_0, teaching Q4, Safetensors-to-GGUF | Accepted |
| [Restricted checkpoints](docs/README.md#restricted-checkpoints) | Passive pickle risk inventory, allow-listed primitive parsing, tensor-only extraction | Constrained slice |
| [Adaptation](docs/README.md#adaptation) | Fine-tuning, low-rank adapters, in-context learning, in-context RL | Accepted |
| [Experiments](docs/README.md#experiments) | Split, Lift, Ensemble, Feed, and Tune as inspectable MLPL | Accepted |
| [Convolution from equations](docs/README.md#convolution-from-equations) | A paper's convolution equation carried down to executable MLPL in six rungs, checked against `conv2d`, ending in a kernel learned by gradient descent | Runnable |
| [Model training](docs/README.md#model-training-gated-opt-in) | Agentrail coding-model fine-tuning and distillation | Gated, opt-in |

## Running the project

The repository uses a thin `justfile`:

```sh
just                    # list available recipes
just check              # run the complete local pre-commit gate
just array-capabilities # report which array capabilities the binary ships
just checkpoint-tensor-metadata
```

Recipes print the scenario, implementation boundary, budgets, observable
results, and interpretation — not only a pass/fail marker.

## Where to read more

- [Documentation index](docs/README.md) — every demo, contract, and plan
- [Demo catalog](catalog/README.md) — formats, layers, memory contracts, status
- [Development guide](docs/development.md) — fixtures, binary selection, validation
- [Saga queue](docs/sagas.md) — what is done, active, and planned

## Copyright and license

Copyright (c) 2026 Michael A Wright. See [COPYRIGHT](COPYRIGHT).

This project is available under the [MIT License](LICENSE).
