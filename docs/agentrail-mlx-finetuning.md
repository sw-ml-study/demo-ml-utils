# Two-Stage Agentrail Coding-Model Fine-Tuning with MLX

Status: repository-local uv environment and both MLX checkpoints are ready;
Stage 1 training remains opt-in and is not part of `just check`.

## Demonstration story

This demo will use the same bounded task schema at two scales:

1. **Pipeline proof:** Qwen2.5-Coder-1.5B-Instruct-4bit learns a narrow mapping
   from a repository/step state to one exact next Agentrail action. This stage
   makes dataset formatting, MLX QLoRA, adapter persistence, before/after held-
   out scoring, and memory measurement cheap to debug.
2. **Agentrail teacher:** Qwen2.5-Coder-7B-Instruct-4bit learns valid workflow
   transitions, invalid-action rejection, and concise explanations. The larger
   coding model is the actual quality claim; the first stage is only pipeline
   calibration.

Both upstream Qwen checkpoints use the Apache-2.0 license. The selected MLX
checkpoints are `mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit` and
`mlx-community/Qwen2.5-Coder-7B-Instruct-4bit`. The latter corresponds to a
7.61-billion-parameter, 28-layer coding and instruction model. The repository
does not redistribute either checkpoint or a trained adapter.

### Local inventory observed 2026-08-10

| Artifact | Local state | Training decision |
|---|---|---|
| Ollama `qwen2.5-coder:7b` | Present, 4,683,074,048-byte GGUF layer | Same desired model family, but inference-only for this demo; MLX-LM does not train the Ollama/GGUF artifact |
| Ollama `qwen2.5vl:7b` | Present, 5,969,233,408-byte GGUF layer | Vision-language scope is unnecessary and adds memory/complexity |
| Ollama `gemma4:31b-mlx` | Present as Ollama tensor layers | Far outside a conservative 12 GiB fine-tuning target |
| MLX Qwen2.5-Coder 1.5B 4-bit | Present under ignored `models/` (about 839 MiB) | Stage 1 checkpoint |
| MLX Qwen2.5-Coder 7B 4-bit | Present under ignored `models/` (about 4.0 GiB) | Stage 2 checkpoint |
| MLX-LM Python package | `.venv-mlx`: MLX 0.32.0, MLX-LM 0.31.3 | Ready; Metal device probe succeeded |

Two `mlx-community/Ornith` cache directories contain only refs and no model
snapshot. They are incomplete downloads and are not candidates. A cached 1B
MiniCPM FP16 derivative was rejected as the main demonstration target because
the requested task calls for a capable coding model and its cached snapshot
lacks a model card/license file suitable for a self-contained provenance check.

## Boundary: what MLPL does

MLPL will own the durable, inspectable experiment:

- validate the frozen Agentrail workflow contract and train/validation/test IDs;
- reject duplicates, leakage, oversized examples, and malformed actions;
- normalize base/adapted responses and score exact actions separately from
  explanations;
- compare the frozen training interface with a bounded live `agentrail --help`
  manifest;
- emit the versioned before/after, drift, provenance, and memory report.

It also owns training-data generation. Records/arrays, deterministic seeded
randomness, mapping/reduction, tagged JSON, bounded reads, atomic writes,
Results, fingerprints, and split/leakage checks are sufficient to enumerate
workflow states, generate valid/invalid pairs, corrupt and repair trajectories,
produce stable train/validation/test identities, and project canonical records
to MLX-LM chat/completion/text JSONL. See the
[distillation plan](plan-agentrail-distillation.md#sw-mlpl-as-the-training-data-laboratory)
for supervised, teacher-distilled, self-supervised, and unsupervised-analysis
variants.

A thin shell runner owns process effects: locating `agentrail`, capturing
`--version` and `--help`, and invoking a configured Python environment.
MLX-LM owns tokenization, causal-model LoRA/QLoRA training, adapter loading, and
generation. Current sw-MLPL does not provide those foundation-model interfaces,
so describing them as MLPL-native would be inaccurate.

## Drift and data separation

Training uses a committed, versioned Agentrail contract—not the live executable
output. At evaluation time the runner captures the installed binary's bounded
help text. MLPL deterministically compares its command/interface manifest with
the frozen training manifest before model evaluation. A model may explain a
change, but model output is never the authority for deciding whether drift
occurred.

This prevents a changed executable from being silently treated as an ordinary
held-out prompt and prevents live evaluation data from leaking into training.

## Twelve-GiB memory contract

The initial QLoRA settings are deliberately conservative: 4-bit base weights,
batch size 1, short examples, four trainable layers, rank 8, gradient
checkpointing, and bounded iterations. The limit is 12,288 MiB. This is a
measured acceptance limit, not an estimate: a stage fails if observed peak MLX
active/cache memory or process high-water evidence exceeds it. Stage 2 does not
start until Stage 1 measurement and adapter round-trip pass.

MLX-LM documents quantization, batch size, fewer trainable layers, shorter
examples, and gradient checkpointing as its primary memory controls. The
locally cached Ollama `qwen2.5-coder:7b` GGUF is useful for base inference but
is not an MLX-LM training checkpoint; the opt-in demo requires MLX Safetensors.

## Read-only preflight

Run:

```sh
just agentrail-mlx-preflight
```

It checks Agentrail on `PATH`, the stable `next`/`begin`/`complete` help surface,
the Rust-native causal-LM provider, and complete local MLX checkpoints. It never
installs, downloads, loads remote model code, trains, or
changes Agentrail state. Override local paths with `AGENTRAIL_SMALL_MODEL`,
and `AGENTRAIL_CODING_MODEL`.

Current result: `overall=unavailable` and `rust_causal_lm=missing`. See
[the Rust-native boundary](rust-native-model-training.md).

## Sources

- [MLX-LM project and supported fine-tuning](https://github.com/ml-explore/mlx-lm)
- [MLX-LM LoRA/QLoRA and memory controls](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- [Qwen2.5-Coder-7B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)
- [Qwen2.5-Coder-7B-Instruct-4bit for MLX](https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit)
