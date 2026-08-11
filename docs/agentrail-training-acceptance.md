# Agentrail Training Demonstrations — Final Acceptance

Status: accepted on 2026-08-10 for the bounded demonstrations described here.
This report consolidates the CPU Engram mechanism, two-stage MLX QLoRA,
training-data provenance, rejected trials, live-interface drift, and remaining
limitations. It is not a claim of general autonomous-agent competence.

## Demonstration sequence

| Stage | Mechanism | Accepted evidence |
|---|---|---|
| CPU help router | sw-MLPL `engram(...)` + Adam | held-out loss 0.1667 to 0.1037; 6/6 route classes; 18 memory rows written |
| Pipeline proof | Qwen2.5-Coder 1.5B 4-bit + rank-8 LoRA | validation loss 5.865 to 0.002; exact held-out actions 0/3 to 3/3; 1.104 GB peak |
| Frozen workflow data | MLPL-generated MIT prompt/completion JSONL | 12/3/3 distinct splits; valid, invalid, recovery, and stop cases; byte-reproducible fixtures |
| Coding model | Qwen2.5-Coder 7B 4-bit + rank-8 LoRA | validation loss 4.297 to 0.798; exact actions 0/3 to 3/3; rejection 2/3 to 3/3; 4.781 GB peak |
| Live drift | bounded shell capture + deterministic MLPL comparison | Agentrail 0.1.0 build `2f06132`; all 3 trained commands present; 19 of 22 live commands out of scope |

Both MLX runs used batch size 1, four trainable transformer layers, prompt
masking, gradient checkpointing, fixed seeds, fresh adapter loading, and a
12.288 GB peak-memory ceiling. The 1.5B adapter is 5,281,601 bytes. The accepted
7B adapter is 11,540,338 bytes with SHA-256
`e34378b6483ddf3e425b7e7b75726eba345170f7850e40d10133a85082923372`.
Adapters and checkpoints remain ignored local artifacts and are not
redistributed by this repository.

## What sw-MLPL demonstrates

MLPL owns the inspectable experiment contracts rather than foundation-model
execution. It generates deterministic supervised JSONL, freezes split IDs and
held-out scenarios, writes provenance and interface manifests, checks resource
budgets, regenerates committed fixtures byte-for-byte, and deterministically
classifies live command drift. The CPU Engram example additionally performs
model initialization, differentiation, Adam updates, conditional-memory
statistics, and held-out classification directly in sw-MLPL.

MLX-LM owns Qwen chat templating, tokenization, quantized causal-model loading,
LoRA training, adapter persistence/loading, and generation. Thin Python and
shell adapters expose this boundary. The Qwen chat-template mismatch found
during Stage 1 is retained as a regression lesson: raw generation and CLI
generation are not comparable unless they use the same template.

## Provenance and separation

The workflow corpus is deterministic repository-authored synthetic material
under the repository's MIT license. Its provenance record declares zero
private, teacher-generated, external-conversation, and live-help examples.
Qwen2.5-Coder source checkpoints are Apache-2.0; the repository references but
does not redistribute the MLX conversions or trained adapters.

Installed `agentrail --help` is captured only into ignored evaluation files.
It never becomes a training fixture. The frozen teaching slice contains
`next`, `begin`, and `complete`; the 19 other live commands are explicitly not
learned capabilities. A missing-`complete` adversarial fixture proves breaking
drift detection independently of model output.

## Rejected trials and why strict acceptance mattered

- The first 7B run used six training records at `1e-4`. It reached only 1/3
  exact held-out actions and failed the stop case.
- Expanding deterministic coverage and using `5e-5` for 60 steps reached 2/3,
  but generated `agentrail begin implementation`; that is not an executable
  exact command and was rejected.
- Eighty conservative steps reached 3/3 without relaxing normalization.

Training loss, fluent explanations, and approximate command prefixes were not
accepted as substitutes for held-out exact behavior. The tiny test set still
limits the strength of the conclusion.

## Safety boundary

Every learned result is advisory. Reports state `automatic_execute=0`; the
model cannot run Agentrail, edit files, stage, commit, push, disclose context,
or decide whether interface drift exists. Deterministic state/evidence checks
and human or controller authorization remain required. Unrelated worktree
changes must be preserved.

## Reproduction

Routine, model-free validation:

```sh
just check
just agentrail-mlx-preflight
just agentrail-help-drift
```

Opt-in local Apple-GPU operations, after providing ignored checkpoints and the
uv environment:

```sh
just agentrail-small-model
just agentrail-small-model-eval
just agentrail-coding-model
just agentrail-coding-model-eval
just agentrail-help-drift-with-model
```

The training recipes overwrite ignored adapter/log destinations. Evaluation
recipes require an existing accepted local adapter.

## CUDA handoff

CUDA support should preserve the committed MLPL-generated JSONL, frozen
manifest, split IDs, held-out scorer semantics, provenance, exact-action
normalization, adapter fingerprinting, and 12.288 GB limit. Only the explicit
trainer/generator adapter changes—for example to a reviewed
Transformers/PEFT/bitsandbytes stack. Before comparing backends, pin package,
CUDA, driver, checkpoint revision, quantization, seed, LoRA targets, optimizer,
and peak allocated/reserved GPU measurements. Do not claim numerical parity
from configuration similarity; require the same held-out actions and report
backend-specific memory and adapter hashes.

## Remaining work

The current held-out sets are mechanism-sized. They do not cover all 22 live
commands, complete subcommand option signatures, long trajectories, semantic
near-duplicate leakage, prompt injection, conflicting state evidence, model
calibration, multi-seed variance, CUDA execution, or GLM-5.x distillation.
Those are follow-on experiments, not hidden parts of this acceptance claim.
