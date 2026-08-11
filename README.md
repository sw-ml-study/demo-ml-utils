# demo-ml-utils

Practical machine-learning artifact utilities written in sw-MLPL. The project
demonstrates bounded inspection, validation, visualization, conversion, and
quantization for Safetensors, GGUF, and restricted tensor-only checkpoints.

Substantive algorithms stay in MLPL wherever the language can express them.
Native or external tools are limited to generic services such as I/O,
rendering, interoperability, performance measurement, and independent
validation. Each demo documents that boundary explicitly.

## Current capabilities

### Safetensors

- [Bounded header inspection](docs/bounded-analysis-report.md) uses range reads
  and `file_size`, so memory is controlled by the header budget rather than
  total artifact size.
- [Deterministic metadata cataloging](docs/safetensors-catalog.md) discovers
  arbitrary tensor names with duplicate-key rejection and bounded JSON reads.
- [Selective integer decoding](docs/safetensors-slice.md) reads exact tensor
  ranges for the currently supported integer dtypes.
- [Fixed-chunk statistics](docs/safetensors-statistics.md) provides mergeable
  summaries without loading a complete tensor.
- [Summary IR](docs/safetensors-summary-ir.md) produces a versioned, budgeted
  JSON handoff for visualization.

The Safetensors analysis slice includes measured sparse-artifact acceptance.
See the [foundation report](docs/foundation-report.md) for its consolidated
evidence and limitations.

### GGUF

- [GGUF v3 catalog](docs/gguf-catalog.md) supports a safe scalar metadata
  subset, multiple tensor descriptors, and visible active type IDs.
- [Selective tensor decoding](docs/gguf-slice.md) resolves exact names and
  reads bounded I8 or I16 payload ranges.
- [Q8_0 block decoding](docs/gguf-q8-0.md) validates exact 34-byte blocks,
  binary16 scales, and golden parity with ggml's dequantization rule.
- [GGUF acceptance](docs/gguf-acceptance-report.md) covers deterministic
  sampling, mergeable statistics, and measured sparse-artifact memory use.

### Visualization

- [Cross-format scene/tile IR](docs/scene-tile-ir.md) creates stable,
  provenance-carrying JSON objects and links without requiring a renderer.
- [Tensor-city layout](docs/tensor-city.md) maps complete bounded catalogs into
  deterministic artifact districts and renderer-neutral building geometry.
- [Detail tiles](docs/detail-tiles.md) add bounded histograms and sampled
  surface strips for selected tensors.
- [Q8_0 error tiles](docs/quantization-error-tiles.md) expose pointwise errors,
  aggregate quality metrics, and size tradeoffs.
- [Visualization acceptance](docs/visualization-acceptance-report.md) validates
  deterministic bounded JSONL transport and an optional dependency-free
  envelope inspector.

### Quantization and conversion

- [Numeric conversion goldens](docs/numeric-conversion.md) demonstrate explicit
  saturating byte policies and reconstruction metrics.
- [Symmetric INT8 and Q8_0](docs/symmetric-roundtrip.md) provide deterministic
  encode/decode round trips with binary16 scales.
- [Teaching Q4](docs/simple-q4.md) makes its 18-byte nibble layout and accuracy
  tradeoff visible.
- [Safetensors-to-GGUF](docs/safetensors-to-gguf.md) writes one bounded signed
  integer tensor to deterministic GGUF v3 and validates the result by reading
  it back.

The [quantization and conversion acceptance report](docs/quantization-conversion-acceptance.md)
summarizes the supported slice and its opt-in independent oracle.

### Restricted checkpoints

This work treats pickle as untrusted executable serialization and uses a
deliberately constrained, non-PyTorch-deserializing path:

1. [Passive risk inventory](docs/checkpoint-risk-inventory.md) validates the
   ZIP structure and classifies pickle opcodes without executing them.
2. [Restricted primitive machine](docs/checkpoint-primitive-machine.md)
   reconstructs inert dictionary/list graphs while rejecting executable and
   persistence opcodes.
3. [Declarative tensor catalog](docs/checkpoint-tensor-metadata.md) validates
   dtype, shape, and exact raw-storage member ranges without reading storage
   payloads or invoking persistence callbacks.
4. [Safetensors extraction](docs/checkpoint-to-safetensors.md) copies only
   approved ranges into an atomic deterministic artifact and validates every
   tensor through the independent existing reader.
5. [Security acceptance](docs/checkpoint-security-acceptance.md) consolidates
   ten adversarial rejection classes and an opt-in independent cross-format
   oracle.

The constrained restricted-checkpoint slice is complete. It does not claim
general PyTorch/pickle compatibility.

### Adaptation

The [shared adaptation contract](docs/adaptation-contract.md) defines distinct
proof requirements for fine-tuning, ICL, and ICRL; validates deterministic
train/context/evaluation splits; and pins the numeric operations needed by the
first teaching-scale learners. The broader
[adaptation demo plan](docs/adaptation-demos-plan.md) records the sequence and
production-scale limitations.
The [manual linear fine-tuning demo](docs/linear-fine-tuning.md) then performs
real bounded parameter updates, exposes its loss/gradient trajectory, and
compares no-training with fine-tuned held-out predictions.
The [frozen-base low-rank adapter](docs/low-rank-adapter.md) exposes factor
gradients, merge parity, unchanged base evidence, and honest trainable/storage
parameter accounting for rank one and two.
The [adaptation curve IR](docs/adaptation-curve-ir.md) then normalizes both
trainers into shared curve, update, prediction, baseline, and provenance
channels for headless consumers and future renderers.
The [fine-tuning acceptance report](docs/fine-tuning-acceptance.md) closes that
bounded saga with deterministic, adversarial, and atomic-publication evidence
plus explicit limitations.
The [ICL record contract](docs/icl-contract.md) begins frozen-parameter
in-context learning with disjoint context/query records and an honest zero-shot
baseline.
The [frozen associative ICL demo](docs/associative-icl.md) then exposes exact
zero/one/few-shot predictions, similarities, contributions, and unchanged
deployment fingerprints.
The [ICL context controls](docs/icl-controls.md) make order, distractor,
contradiction, truncation, empty-context, and leakage effects explicit.
The [ICL comparison IR](docs/icl-comparison-ir.md) normalizes context,
similarities, predictions, loss, exact-match accuracy, fingerprints, and
provenance for renderer-neutral consumers.
The [ICL acceptance report](docs/icl-acceptance.md) closes the saga with
reproducible, adversarial, frozen-state, and atomic-publication evidence.
The [bandit history contract](docs/bandit-history-contract.md) begins bounded
ICRL work with deterministic reward tapes, regret histories, held-out
separation, and explicitly non-ICRL greedy/UCB baselines.
The [source history generator](docs/history-generator.md) produces diverse,
held-out-separated offline reward/regret trajectories for policy distillation.
The [distilled context policy](docs/distilled-context-policy.md) performs
visible offline training, then freezes a versioned two-parameter artifact.
The [held-out ICRL rollout](docs/held-out-icrl-rollout.md) demonstrates growing
reward-context adaptation, frozen fingerprints, regret, and ablations.
The [ICRL acceptance report](docs/icrl-acceptance.md) closes the adaptation
roadmap with renderer-neutral histories, adversarial checks, and atomic evidence.

The planned adaptation slice is a two-stage Agentrail coding-model fine-tune.
Its corpus and evaluation contracts are present, but execution is gated until
sw-MLPL exposes the required [Rust-native causal-LM training
surface](docs/rust-native-model-training.md). Model downloads and training
remain outside `just check`.

The [progressive help escalation demo](docs/help-escalation.md) is runnable
without those model prerequisites. It shows how grounded browser help returns
typed answers or explicit documentation/program/repository/reasoning escalation
results, while consent-minimized bundles never send context or execute commands.

The companion [CPU-trained Engram help router](docs/trained-help-engram.md)
trains a real six-class route proposer with Adam, verifies held-out predictions
and written phrase-memory rows, and then hands proposals to that deterministic
evidence and consent boundary. It is a small classifier, not a generative agent.

The [Stage 1 Agentrail QLoRA report](docs/agentrail-small-model.md) records an
earlier Qwen2.5-Coder 1.5B experiment (0/3 to 3/3, 1.104 GB peak). It is
historical evidence while the Rust-native implementation is pending.

The [frozen Agentrail workflow corpus](docs/agentrail-workflow-corpus.md) adds
MIT-provenance valid, invalid, and recovery examples for Stage 2 while keeping
installed `agentrail --help` strictly outside training for later drift checks.

The [Qwen2.5-Coder 7B Agentrail QLoRA report](docs/agentrail-coding-model.md)
records the earlier 0/3 to 3/3 result, including rejection and mandatory stop
behavior, at a measured 4.781 GB peak. It is not a current runnable recipe.

The [live-help drift demo](docs/agentrail-help-drift.md) confirms the three
trained commands remain present in Agentrail 0.1.0 and reports 19 additional
commands as evaluation-only, out-of-scope additions rather than learned skills.

The [final Agentrail training acceptance report](docs/agentrail-training-acceptance.md)
consolidates the two Qwen stages, Engram, provenance, rejected trials, memory,
safety boundaries, reproducibility, limitations, and CUDA handoff.

The follow-on [expanded adversarial evaluation plan](docs/agentrail-adversarial-evaluation-plan.md)
starts by enforcing cross-split lexical leakage and scenario-family coverage
thresholds before adding broader held-out cases.

The [adversarial held-out suite](docs/agentrail-adversarial-cases.md) adds 12
evaluation-only invalid-transition, conflict, injection, malformed-output,
dirty-worktree, and long-trajectory cases with explicit non-execution fields.

## Running the project

The repository uses a thin `justfile`:

```sh
just                 # list available recipes
just check           # run the complete local pre-commit gate
just checkpoint-tensor-metadata
```

Individual recipes print the scenario, implementation boundary, budgets,
observable results, and interpretation—not only a pass/fail marker.

See the [development guide](docs/development.md) for fixture policy, binary
selection, and validation details. The [demo catalog](catalog/README.md)
records each demo's format, implementation layer, memory contract, required
capabilities, and status.

## Project documentation

- [Delivery plan](docs/plan.md)
- [Saga queue and status](docs/sagas.md)
- [Capability report](docs/capabilities.md)
- [Shipped upstream contract](docs/upstream-contract.md)
- [Peer repository audit](docs/peer-repository-audit.md)
- [Fine-tuning, ICL, and ICRL plan](docs/adaptation-demos-plan.md)
- [Coding-model training plan: Agentrail with sw-MLPL and MLX](docs/training-plan.md)
- [Progressive built-in help escalation](docs/help-escalation.md)
- [CPU-trained help router with Engram](docs/trained-help-engram.md)
- [Stage 1 Agentrail small-model QLoRA](docs/agentrail-small-model.md)
- [Frozen Agentrail workflow corpus](docs/agentrail-workflow-corpus.md)
- [Qwen2.5-Coder 7B Agentrail QLoRA](docs/agentrail-coding-model.md)
- [Agentrail live-help drift evaluation](docs/agentrail-help-drift.md)
- [Agentrail training final acceptance](docs/agentrail-training-acceptance.md)
- [Agentrail expanded adversarial evaluation plan](docs/agentrail-adversarial-evaluation-plan.md)
- [Agentrail adversarial held-out cases](docs/agentrail-adversarial-cases.md)
- [MLX prerequisite and remaining distillation status](docs/mlx-traiing-todo.md)
- [Two-stage Agentrail coding-model MLX fine-tuning](docs/agentrail-mlx-finetuning.md)
- [Two-stage GLM-to-Qwen Agentrail distillation plan](docs/plan-agentrail-distillation.md)
- [LEFTS-inspired composable experiment plan](docs/plan-lefts.md)
- [LEFTS callable and functor-law capability contract](docs/lefts-capability-contract.md)
- [Split and Lift-inspired grouped learning](docs/split-lift.md)
- [Ensemble and Feed composition](docs/ensemble-feed.md)
- [Leakage-safe Tune](docs/tune.md)
- [Composed rolling experiment](docs/rolling-experiment.md)
- [LEFTS-inspired acceptance and promotion report](docs/lefts-acceptance.md)
- Standalone Web UI file: [`demos/experiments/lefts_page_web.mlpl`](demos/experiments/lefts_page_web.mlpl)

## Copyright and license

Copyright (c) 2026 Michael A Wright. See [COPYRIGHT](COPYRIGHT).

This project is available under the [MIT License](LICENSE).
