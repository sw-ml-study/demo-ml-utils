# MLX Training TODO and Current Blockers

The spelling of this filename follows the requested handoff name. The canonical
training design remains in [training-plan.md](training-plan.md).

The two-stage Agentrail Qwen training saga is intentionally deferred while the
progressive built-in-help mechanics are developed.

## Missing opt-in prerequisites

- A Python environment containing compatible `mlx` and `mlx_lm` packages is
  not currently selected.
- `mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit` is not present locally.
- `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` is not present locally.
- The cached Ollama `qwen2.5-coder:7b` artifact is GGUF inference data and
  cannot be used directly as an MLX-LM training checkpoint.
- The 12,288 MiB limit has not yet been measured during either student's
  training; checkpoint-size estimates are not acceptance evidence.
- GLM-5.x distillation additionally lacks a configured endpoint, credentials,
  reviewed provider/generated-data terms, and explicit token/cost budget.

## Resume conditions

1. Supply `MLX_LM_PYTHON`, `AGENTRAIL_SMALL_MODEL`, and
   `AGENTRAIL_CODING_MODEL` as explicit local paths.
2. Run `just agentrail-mlx-preflight` until every prerequisite reports `ready`.
3. Resume Agentrail step `small-model-pipeline`.
4. Prove the 1.5B adapter round-trip, held-out improvement, and measured memory
   before starting 7B training.
5. Keep all downloads, training, credentials, and teacher calls outside
   `just check`.

No upstream sw-MLPL change is currently required to continue the unblocked
dataset, routing, validation, and report work.
