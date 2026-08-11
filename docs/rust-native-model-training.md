# Rust-native model training boundary

This repository has no direct dependency on Python tooling. Its runnable
demos, fixture generators, validators, and acceptance checks use MLPL and
small POSIX-shell launchers only. `scripts/check-sources` rejects tracked
`.py` files and executable calls to Python or MLX-LM.

The Agentrail corpus, provenance records, deterministic split checks,
live-help drift demo, CPU Engram router, and adversarial fixtures remain
runnable. The Qwen QLoRA recipes are discoverable capability gates, but exit
with status 77 until sw-MLPL provides the missing Rust surface.

## Required upstream surface

The smallest useful backend-neutral sw-MLPL contract must:

1. Load a supported tokenizer and apply its chat template.
2. Load a quantized causal model from local Safetensors and configuration.
3. Attach LoRA adapters to selected linear layers.
4. Train with bounded batch, sequence, iteration, memory, and seed settings.
5. Save and reload adapter weights plus reproducibility metadata.
6. Generate deterministically with explicit token and memory budgets.
7. Return structured loss, memory, timing, and generation evidence.

An optional MLX provider should implement that contract in Rust with `mlx-rs`.
A later CUDA provider can implement the same contract with a Rust CUDA stack.
Model-family details such as Qwen tensor names, rotary configuration, and chat
templates belong behind the provider boundary.

The extension ABI is suitable for coarse model operations and provider
registration. It should not serialize individual tensors inside the training
hot path. Core sw-MLPL should own budgets, experiment semantics, evidence, and
backend selection; providers should own device tensors, kernels, model loading,
and optimization.

## Acceptance before re-enabling Qwen recipes

- no tracked Python source or executable Python dependency;
- local-only model loading with remote code disabled;
- Qwen2.5-Coder 1.5B and 7B 4-bit checkpoint compatibility;
- deterministic base-versus-adapter generation for fixed seeds;
- bounded LoRA training below the declared 12 GiB ceiling;
- adapter save/reload parity;
- structured failures for unsupported tokenizer/model/config combinations;
- Metal tests upstream and backend-neutral contract tests reusable by CUDA.

Historical Agentrail measurements describe earlier experiments. They remain
evidence, not a currently runnable implementation path.
