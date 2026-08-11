# Stage 1 Agentrail Small-Model QLoRA

`just agentrail-small-model` is an opt-in GPU demonstration that fine-tunes the
local Qwen2.5-Coder-1.5B-Instruct-4bit checkpoint on one deliberately narrow
task: emit exactly `agentrail next`, `agentrail begin`, or
`agentrail complete` from a repository-step description.

MLPL generates the bounded supervised corpus: 12 training, three validation,
and three held-out prompt/completion records. The splits use distinct stable
IDs and share action semantics without repeating state text. MLX-LM owns chat
templating, tokenization, the quantized causal model, LoRA optimization,
adapter persistence/loading, and generation.

The fixed training contract is batch size 1, 60 Adam iterations, four
trainable transformer layers, rank 8, prompt masking, gradient checkpointing,
maximum sequence length 192, and seed 17. Artifacts and logs live under ignored
`tmp/`; checkpoints and the uv environment remain under ignored `models/` and
`.venv-mlx/`.

## Evidence from the first accepted run

| Measurement | Base / start | Adapted / finish |
|---|---:|---:|
| Validation loss | 5.865 | 0.002 |
| Held-out exact commands | 0 / 3 | 3 / 3 |
| Test loss / perplexity | — | approximately 0.000 / 1.000 |
| Trainable parameters | — | 1.319M of 1,543.714M (0.085%) |
| MLX training peak | — | 1.104 GB |

The saved adapter is 5,281,601 bytes. Evaluation loads it in a fresh model
construction, fingerprints the file, checks exact normalized output, requires
strict improvement over the base model, and rejects training peak memory above
12.288 GB. `automatic_execute` is always zero.

The evaluator must apply Qwen's chat template. A raw-library probe initially
failed even though CLI generation succeeded because raw `generate()` does not
add that template. The checked evaluator now applies the same template used by
the prompt/completion training dataset; this is an explicit regression seam.

This stage proves the local QLoRA pipeline, not general Agentrail competence.
The next saga step builds the larger licensed workflow corpus with command
arguments, invalid-action rejection, explanations, leakage controls, and drift
separation before the 7B coding-model claim.
