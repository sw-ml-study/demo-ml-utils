# MLX Training TODO and Current Blockers

The spelling of this filename follows the requested handoff name. The canonical
training design remains in [training-plan.md](training-plan.md).

> Update (2026-08-11): direct Python tooling has been removed. The local
> artifacts below document an earlier experiment, not current prerequisites.
> Qwen execution is gated on
> [rust-native-model-training.md](rust-native-model-training.md).

The two-stage Agentrail Qwen training saga is intentionally deferred while the
progressive built-in-help mechanics are developed.

## Historical prerequisite status (2026-08-10)

- `.venv-mlx` contains Python 3.12.13, MLX 0.32.0, and MLX-LM 0.31.3.
- `models/Qwen2.5-Coder-1.5B-Instruct-4bit` is present (about 839 MiB).
- `models/Qwen2.5-Coder-7B-Instruct-4bit` is present (about 4.0 GiB).
- Both public checkpoints downloaded anonymously; no HF token was required.
- An unsandboxed device probe reports `Device(gpu, 0)`.
- The earlier preflight found the ignored local environment and models. The
  current preflight reports `rust_causal_lm=missing`.

These local artifacts are intentionally ignored and are not redistributed.

## Remaining acceptance work

- The cached Ollama `qwen2.5-coder:7b` artifact is GGUF inference data and
  cannot be used directly as an MLX-LM training checkpoint.
- The 12,288 MiB limit has not yet been measured during either student's
  training; checkpoint-size estimates are not acceptance evidence.
- GLM-5.x distillation additionally lacks a configured endpoint, credentials,
  reviewed provider/generated-data terms, and explicit token/cost budget.

## Resume conditions

1. Run `just agentrail-mlx-preflight` outside GPU-restricted sandboxes and
   confirm `overall=ready`.
2. Continue the active Agentrail step `small-model-pipeline`.
3. Prove the 1.5B adapter round-trip, held-out improvement, and measured memory
   before starting 7B training.
4. Keep all downloads, training, credentials, and teacher calls outside
   `just check`.

No upstream sw-MLPL change is currently required to continue the unblocked
dataset, routing, validation, and report work.
