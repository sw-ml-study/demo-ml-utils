# Coding-Model Training Plan: Agentrail with sw-MLPL and MLX

## Outcome

Build two related, opt-in demonstrations that make sw-MLPL's role in practical
model work visible:

1. **Two-stage fine-tuning:** prove a bounded MLX QLoRA pipeline with a small
   coding model, then fine-tune a stronger coding model to follow the Agentrail
   process.
2. **Two-stage distillation:** use GLM-5.x as an external teacher, first to
   improve exact one-step behavior in the small student and then to improve
   multi-step Agentrail judgment in the larger student.

All local student training targets a measured 12,288 MiB memory ceiling. CUDA
is a later backend using the same canonical data and evidence contracts.
Downloads, credentials, teacher calls, and model training remain outside the
default `just check` gate.

## Models and stages

| Track | Stage | Model | Goal |
|---|---:|---|---|
| Fine-tuning | 1 | Qwen2.5-Coder-1.5B-Instruct-4bit | Prove MLX QLoRA, adapter persistence, scoring, and memory controls on exact next-action prediction |
| Fine-tuning | 2 | Qwen2.5-Coder-7B-Instruct-4bit | Learn valid Agentrail transitions, invalid-action rejection, recovery, and concise explanations |
| Distillation | 1 | GLM-5.x teacher → Qwen2.5-Coder-1.5B student | Distill diverse one-step paraphrases, counterexamples, and reasons while deterministic MLPL rules retain authority |
| Distillation | 2 | GLM-5.x teacher → Qwen2.5-Coder-7B student | Distill multi-step planning, critique/repair, saga/git-drift recovery, and help-drift-aware behavior |

Qwen2.5-Coder is selected because it is coding- and instruction-specialized,
Apache-2.0 licensed, supported by MLX-LM, and available as 4-bit MLX
Safetensors. The locally cached Ollama Qwen2.5-Coder 7B GGUF is useful for
inference but is not the checkpoint format MLX-LM trains.

GLM-5.x is roughly a 745B-parameter Mixture-of-Experts family, so it is not a
12 GiB local teacher. Teacher generation must use an explicitly configured
remote/OpenAI-compatible endpoint or separately provisioned server with pinned
provider/model/version and cost/token budgets.

## Architecture and ownership

### sw-MLPL owns the experiment

MLPL files own:

- canonical Agentrail state, action, transition, help-interface, and report
  schemas;
- deterministic state-space and trajectory generation;
- seeded sampling, corruption, paraphrase-view selection, and split assignment;
- duplicate, leakage, schema, magnitude, record-count, byte, and work budgets;
- teacher-response ingestion and deterministic acceptance/rejection;
- live-help manifest comparison against the frozen training contract;
- base/adapted response normalization and correctness metrics;
- fingerprints, provenance, learning curves, ablations, and atomic reports;
- projection of canonical records into MLX-LM `chat`, `completions`, or `text`
  JSONL.

Existing sw-MLPL capabilities supporting this include records, arrays, user
functions, loops, map/filter/reduce-style operations, deterministic seeded
randomness, numeric arrays/reductions, Results, bounded file reads, file size,
atomic writes, `to_json`, budgeted `parse_json`, deterministic `record_keys`,
duplicate-key rejection, and exact JSON round-trips. Existing demos already
prove deterministic split validation, synthetic history generation, frozen
policy distillation, held-out rollout, adversarial controls, fingerprints, and
renderer-neutral training curves.

### Thin runners own process effects

Shell runners only:

- locate `agentrail` and capture bounded `--version`/`--help` output;
- locate configured local model paths and Python environment;
- call the configured GLM teacher endpoint in opt-in distillation recipes;
- invoke MLX-LM for tokenization, QLoRA training, adapter loading, and
  generation;
- collect process/MLX memory evidence without installing or downloading in a
  validation command.

Current sw-MLPL does not expose a foundation-model tokenizer/causal-model
training API or a general subprocess-capture API. Those boundaries must remain
explicit rather than being presented as MLPL-native work.

## Training-data approaches

### Supervised

1. **Rule-gold SFT:** enumerate a frozen Agentrail transition table and compute
   the unique valid next action.
2. **Valid/invalid classification:** generate forbidden alternatives and label
   the invariant each violates.
3. **Repair supervision:** deterministically corrupt a valid trajectory and
   target the first bad step plus corrected suffix.
4. **Teacher-distilled SFT:** accept GLM candidate explanations and trajectories
   only after MLPL validates their actions and order.
5. **Contrast/curriculum records:** preserve the same target across bounded
   paraphrases, irrelevant fields, and increasing one-step/recovery/drift
   difficulty.

MLX-LM's LoRA path directly supports chat/completion/text SFT. MLPL may generate
preference pairs for analysis, but this plan does not claim DPO unless a
separate compatible trainer is selected and validated.

### Self-supervised

1. **Contract language modeling:** render rules and safe trajectories as raw
   `text` examples for next-token domain adaptation.
2. **Next-step prediction:** use every trajectory prefix as prompt and its next
   record as completion.
3. **Missing-step reconstruction:** remove one step and target the original.
4. **Corruption/order detection:** seeded shuffle, duplicate, truncate, or
   substitute transforms with the clean source as target.
5. **Invariant views:** change field order, whitespace, commentary, or bounded
   distractors while preserving semantics.

These are self-supervised because targets are derived from the source data.
They are not unlabeled proof that a workflow action is correct.

### Unsupervised analysis

MLPL may count or cluster help commands, failure phrases, state shapes, teacher
rejection reasons, or trajectory lengths to find coverage gaps and choose
examples. Such clusters are corpus-analysis evidence only. Deterministic rules
and held-out gold records remain the correctness authority.

### Required ablation

Each student report compares:

1. base model;
2. self-supervised contract/trajectory adaptation;
3. deterministic supervised gold;
4. deterministic gold plus validated GLM distillation.

This shows what came from domain text, explicit labels, the teacher, and model
scale rather than presenting a single opaque adapter.

## Agentrail live-help drift

Training uses a committed, versioned help/command manifest. It never trains on
the live installed output. Evaluation separately:

1. finds `agentrail` on `PATH`;
2. captures bounded `--version` and `--help` text;
3. lets MLPL deterministically derive and compare the live manifest;
4. reports added, missing, or changed commands before model scoring;
5. prevents the model from using a frozen signature as if it were still live.

The model may explain detected drift, but model output is never the drift
authority.

## Memory and reproducibility

Start both students with 4-bit base weights, batch size 1, rank 8, four
trainable layers, bounded short sequences, gradient checkpointing, fixed seeds,
and bounded iterations. Stage 2 starts only after Stage 1 proves:

- adapter save/load and before/after scoring;
- deterministic dataset and split hashes;
- peak process and MLX active/cache memory below 12,288 MiB;
- destination preservation on failure;
- no hidden downloads or remote-code trust.

Memory is measured acceptance evidence, not inferred from checkpoint size.

## Saga 11 — `agentrail-qwen-mlx-finetune` (active)

1. `model-contract-and-preflight` — inventory, licensing, formats,
   dependencies, PATH/help, memory, and read-only preflight.
2. `small-model-pipeline` — Qwen2.5-Coder-1.5B exact-action QLoRA proof.
3. `agentrail-training-corpus` — frozen workflow corpus and held-out cases.
4. `coding-model-agentrail-qlora` — Qwen2.5-Coder-7B adaptation.
5. `live-help-drift-evaluation` — deterministic installed-interface check.
6. `acceptance-and-documentation` — ablations, memory, provenance, CUDA
   handoff, catalog, and final report.

The active Agentrail store represents this saga. See the detailed
[fine-tuning contract](agentrail-mlx-finetuning.md).

## Saga 12 — `agentrail-glm-qwen-distillation` (queued)

Initialize this saga only after Saga 11 is completed and archived:

1. `distillation-contract` — canonical teacher/student schemas, transition
   validator, provider provenance, budgets, and evaluation freeze.
2. `teacher-candidate-generator` — opt-in GLM-5.x adapter, dry run, redaction,
   retry/token/cost caps, and raw-response evidence.
3. `stage-one-distillation` — validated one-step data and 1.5B student.
4. `trajectory-validator` — multi-step decomposition, corruption, critique,
   repair, and rejection IR.
5. `stage-two-distillation` — validated trajectory data and 7B student.
6. `distillation-acceptance` — four-way ablations, security, reproducibility,
   licenses/terms, memory, costs, and final comparison.

See the detailed [distillation plan](plan-agentrail-distillation.md).

## Current status and remaining blocker

The two-stage MLX track is accepted on this host. The ignored `.venv-mlx`
environment, both local MLX Qwen checkpoints, Metal device, 1.5B pipeline,
12/3/3 frozen corpus, 7B adapter, memory evidence, and live-help comparison are
ready. See the [final acceptance report](agentrail-training-acceptance.md).

Only the optional GLM-5.x distillation track remains externally blocked: it
needs a configured endpoint, credentials, reviewed provider/generated-output
terms, and explicit token/cost budgets. CUDA remains a planned backend handoff,
not a blocker for the accepted Apple MLX demonstration. No default gate
downloads, installs, trains, contacts a provider, or requires GPU artifacts.

## Primary references

- [MLX-LM](https://github.com/ml-explore/mlx-lm)
- [MLX-LM LoRA/QLoRA data and memory guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- [Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)
- [MLX Qwen2.5-Coder-7B-Instruct-4bit](https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit)
- [Official GLM-5 repository](https://github.com/zai-org/GLM-5)
- [Official GLM-5 model card](https://huggingface.co/zai-org/GLM-5)
