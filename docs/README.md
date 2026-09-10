# Documentation index

Every demo area below is runnable unless marked otherwise. Start from the
[demo catalog](../catalog/README.md) for the machine-readable inventory of
formats, implementation layers, memory contracts, and status.

## Planning and process

- [Delivery plan](plan.md)
- [Saga queue and status](sagas.md)
- [Development guide](development.md) — fixture policy, binary selection, validation
- [Peer repository audit](peer-repository-audit.md)

## Capability contracts

These record what the configured sw-MLPL binary provides, pinned by build
commit rather than version string, and enforced by the default gate.

- [Capability report](capabilities.md) — observed binary-format and array capabilities
- [Shipped upstream contract](upstream-contract.md) — bounded I/O and array expressiveness
- [Array-expressiveness blocker record](sw-mlpl-blocker.md) — the C1-C5 gaps and their state
- [Mathematical notation rules](math-notation.md) — how equations must be displayed

## Demo areas

### Safetensors

- [Bounded header inspection](bounded-analysis-report.md) uses range reads
  and `file_size`, so memory is controlled by the header budget rather than
  total artifact size.
- [Deterministic metadata cataloging](safetensors-catalog.md) discovers
  arbitrary tensor names with duplicate-key rejection and bounded JSON reads.
- [Selective integer decoding](safetensors-slice.md) reads exact tensor
  ranges for the currently supported integer dtypes.
- [Fixed-chunk statistics](safetensors-statistics.md) provides mergeable
  summaries without loading a complete tensor.
- [Summary IR](safetensors-summary-ir.md) produces a versioned, budgeted
  JSON handoff for visualization.

The Safetensors analysis slice includes measured sparse-artifact acceptance.
See the [foundation report](foundation-report.md) for its consolidated
evidence and limitations.

### GGUF

- [GGUF v3 catalog](gguf-catalog.md) supports a safe scalar metadata
  subset, multiple tensor descriptors, and visible active type IDs.
- [Selective tensor decoding](gguf-slice.md) resolves exact names and
  reads bounded I8 or I16 payload ranges.
- [Q8_0 block decoding](gguf-q8-0.md) validates exact 34-byte blocks,
  binary16 scales, and golden parity with ggml's dequantization rule.
- [GGUF acceptance](gguf-acceptance-report.md) covers deterministic
  sampling, mergeable statistics, and measured sparse-artifact memory use.

### Visualization

- [Cross-format scene/tile IR](scene-tile-ir.md) creates stable,
  provenance-carrying JSON objects and links without requiring a renderer.
- [Tensor-city layout](tensor-city.md) maps complete bounded catalogs into
  deterministic artifact districts and renderer-neutral building geometry.
- [Detail tiles](detail-tiles.md) add bounded histograms and sampled
  surface strips for selected tensors.
- [Q8_0 error tiles](quantization-error-tiles.md) expose pointwise errors,
  aggregate quality metrics, and size tradeoffs.
- [Visualization acceptance](visualization-acceptance-report.md) validates
  deterministic bounded JSONL transport and an optional dependency-free
  envelope inspector.

### Quantization and conversion

- [Numeric conversion goldens](numeric-conversion.md) demonstrate explicit
  saturating byte policies and reconstruction metrics.
- [Symmetric INT8 and Q8_0](symmetric-roundtrip.md) provide deterministic
  encode/decode round trips with binary16 scales.
- [Teaching Q4](simple-q4.md) makes its 18-byte nibble layout and accuracy
  tradeoff visible.
- [Safetensors-to-GGUF](safetensors-to-gguf.md) writes one bounded signed
  integer tensor to deterministic GGUF v3 and validates the result by reading
  it back.

The [quantization and conversion acceptance report](quantization-conversion-acceptance.md)
summarizes the supported slice and its opt-in independent oracle.

### Restricted checkpoints

This work treats pickle as untrusted executable serialization and uses a
deliberately constrained, non-PyTorch-deserializing path:

1. [Passive risk inventory](checkpoint-risk-inventory.md) validates the
   ZIP structure and classifies pickle opcodes without executing them.
2. [Restricted primitive machine](checkpoint-primitive-machine.md)
   reconstructs inert dictionary/list graphs while rejecting executable and
   persistence opcodes.
3. [Declarative tensor catalog](checkpoint-tensor-metadata.md) validates
   dtype, shape, and exact raw-storage member ranges without reading storage
   payloads or invoking persistence callbacks.
4. [Safetensors extraction](checkpoint-to-safetensors.md) copies only
   approved ranges into an atomic deterministic artifact and validates every
   tensor through the independent existing reader.
5. [Security acceptance](checkpoint-security-acceptance.md) consolidates
   ten adversarial rejection classes and an opt-in independent cross-format
   oracle.

The constrained restricted-checkpoint slice is complete. It does not claim
general PyTorch/pickle compatibility.

### Convolution from equations

Zhao, Wang, Wang & Liu, *Algorithms* **11**(10):159, 2018, Section 2.1,
Equation (1) carried down to executable MLPL and back up to the native `conv2d`
builtin, which is used only as an independent oracle.

Run the whole ladder with `just cnn-ladder`, or one rung at a time:

- `demos/cnn/01_dot_product.mlpl` — one summation, one reduction
- `demos/cnn/02_convolution_1d.mlpl` — a shifted index becomes a windowed axis
- `demos/cnn/03_convolution_2d.mlpl` — two summations, one reduction over two
  axes; asserts the hand-computed `-6` edge response
- `demos/cnn/04_multichannel_convolution.mlpl` — the paper's triple sum, shown
  in four spellings that are bit-identical to each other and match `conv2d`
- `demos/cnn/05_convolution_layer.mlpl` — bias and activation on top

`just cnn-contract` runs the contract test: the hand-derived golden, agreement
between all four spellings, oracle parity for integer and float inputs, and
named rejections for oversized windows, wrong ranks, and unknown axis names.

Bias and activation are **not** part of Equation (1). Rung 5 adds what a real
layer has and says so rather than implying the paper defines it that way. Only
the definitional equation is implemented here; the paper's Winograd and
Strassen contribution is not.

Supporting material:

- [Demo plan and positioning](plan-cnn-from-equations.md)
- [Array-expressiveness blocker record](sw-mlpl-blocker.md) — the C1-C5 gaps
  this demo forced, four of which have shipped
- [Mathematical notation rules](math-notation.md) — every displayed equation
  carries explicit summation limits, a symbol table, the 1-based-to-0-based
  translation, and names cross-correlation rather than inheriting it silently
- `just array-capabilities` reports which array capabilities the binary ships

### Adaptation

The [shared adaptation contract](adaptation-contract.md) defines distinct proof
requirements for fine-tuning, ICL, and ICRL, validates deterministic
train/context/evaluation splits, and pins the numeric operations the
teaching-scale learners need. The [adaptation demo plan](adaptation-demos-plan.md)
records the sequence and production-scale limitations.

**Fine-tuning**

- [Manual linear fine-tuning](linear-fine-tuning.md) — real bounded parameter
  updates with a visible loss and gradient trajectory
- [Frozen-base low-rank adapter](low-rank-adapter.md) — factor gradients, merge
  parity, and honest trainable/storage parameter accounting
- [Adaptation curve IR](adaptation-curve-ir.md) — both trainers normalized into
  shared curve, update, prediction, baseline, and provenance channels
- [Acceptance report](fine-tuning-acceptance.md)

**In-context learning** (parameters stay frozen)

- [ICL record contract](icl-contract.md) — disjoint context/query records and an
  honest zero-shot baseline
- [Frozen associative ICL](associative-icl.md) — zero/one/few-shot predictions
  with visible similarities and contributions
- [Context controls](icl-controls.md) — order, distractor, contradiction,
  truncation, empty-context, and leakage effects made explicit
- [Comparison IR](icl-comparison-ir.md) and [acceptance report](icl-acceptance.md)

**In-context reinforcement learning**

- [Bandit history contract](bandit-history-contract.md) — deterministic reward
  tapes and regret histories, with greedy/UCB baselines named as *not* ICRL
- [Source history generator](history-generator.md) — held-out-separated offline
  trajectories for distillation
- [Distilled context policy](distilled-context-policy.md) — visible offline
  training frozen into a versioned artifact
- [Held-out rollout](held-out-icrl-rollout.md) and [acceptance report](icrl-acceptance.md)

**Help routing**

- [Progressive help escalation](help-escalation.md) — typed answers or explicit
  escalation, with consent-minimized bundles that never send context or execute
  commands. Runnable without model prerequisites.
- [CPU-trained Engram help router](trained-help-engram.md) — a real six-class
  route proposer trained with Adam. A small classifier, not a generative agent.

### Experiments

LEFTS-inspired composable experiment work: Split, Lift, Ensemble, Feed, and
Tune expressed as ordinary inspectable MLPL.

- [Composable experiment plan](plan-lefts.md)
- [Callable and functor-law capability contract](lefts-capability-contract.md)
- [Split and Lift-inspired grouped learning](split-lift.md)
- [Ensemble and Feed composition](ensemble-feed.md)
- [Leakage-safe Tune](tune.md)
- [Composed rolling experiment](rolling-experiment.md)
- [Acceptance and promotion report](lefts-acceptance.md)
- Standalone web UI: [`demos/experiments/lefts_page_web.mlpl`](../demos/experiments/lefts_page_web.mlpl)

### Model training (gated, opt-in)

Execution is gated until sw-MLPL exposes the required
[Rust-native causal-LM training surface](rust-native-model-training.md). Model
downloads and training stay outside `just check`, so the reports below are
historical evidence rather than runnable recipes.

Plans:

- [Coding-model training plan](training-plan.md)
- [Two-stage Agentrail MLX fine-tuning](agentrail-mlx-finetuning.md)
- [Two-stage GLM-to-Qwen distillation plan](plan-agentrail-distillation.md)
- [MLX prerequisites and remaining status](mlx-traiing-todo.md)

Results and evaluation:

- [Stage 1 Qwen2.5-Coder 1.5B QLoRA](agentrail-small-model.md) — 0/3 to 3/3,
  1.104 GB peak
- [Stage 2 Qwen2.5-Coder 7B QLoRA](agentrail-coding-model.md) — 0/3 to 3/3
  including rejection and mandatory-stop behavior, 4.781 GB peak
- [Frozen workflow corpus](agentrail-workflow-corpus.md) — MIT-provenance
  examples, with installed `agentrail --help` kept strictly outside training
- [Live-help drift evaluation](agentrail-help-drift.md) — reports 19 additional
  commands as out-of-scope rather than learned skills
- [Final training acceptance](agentrail-training-acceptance.md)
- [Expanded adversarial evaluation plan](agentrail-adversarial-evaluation-plan.md)
  and [held-out cases](agentrail-adversarial-cases.md)
