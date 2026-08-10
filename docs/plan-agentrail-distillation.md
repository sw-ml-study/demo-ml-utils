# Two-Stage Agentrail Distillation Plan

## Objective

Use a GLM-5.x coding/agentic model as a teacher and two Qwen2.5-Coder students
to demonstrate output/trajectory distillation at increasing scope. The teacher
generates candidate explanations, counterexamples, and repaired trajectories;
deterministic Agentrail rules decide what is accepted. Student training runs
locally through MLX QLoRA.

This is **not** logit distillation: a remote API does not expose the teacher's
full token distribution. It is supervised response and trajectory distillation
with explicit provenance.

## Why the teacher is external

The official GLM-5 family is roughly 745B total parameters with a large active
Mixture-of-Experts footprint. It is not a 12 GiB local-training or inference
candidate. The demo therefore requires an explicitly configured GLM-5.x
OpenAI-compatible endpoint or separately provisioned server. It never silently
falls back to another teacher, sends repository secrets, or runs in `just
check`.

The exact teacher provider, model identifier, endpoint, API/version response,
sampling parameters, prompt hash, response hash, token counts, latency, and
cost fields belong in every generated-record provenance envelope. Credentials
remain outside the repository and reports.

## Stage 1 — distill one-step process control

### Student

`mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit` with a small MLX QLoRA
adapter.

### Goal 1

Given a compact state record, emit exactly one permitted next action and a
short reason:

```text
state: saga=active, step=pending, source_changes=false
answer: {"action":"agentrail begin","reason":"the current step must enter progress before work"}
```

The state space covers no saga, pending, in-progress, source committed,
validation failed, completed, and blocked cases. Invalid-action examples teach
rejection: completing before committing, beginning twice, hand-editing
`.agentrail`, or continuing after a completed step.

### Teacher contribution

GLM-5.x proposes paraphrases, boundary cases, concise reasons, and adversarial
wrong answers. A deterministic validator maps every accepted answer back to the
frozen transition table. Anything outside the allowed action set or inconsistent
with the state is rejected before it enters training data.

### Acceptance

- exact action accuracy on held-out state combinations;
- invalid-transition rejection rate;
- valid JSON/schema rate;
- base-versus-adapted comparison;
- adapter and dataset hashes;
- peak MLX/process memory below 12,288 MiB;
- no overlap among teacher-generation seeds and held-out evaluation IDs.

## Stage 2 — distill Agentrail engineering judgment

### Student

`mlx-community/Qwen2.5-Coder-7B-Instruct-4bit`, using the same MLX pipeline and
conservative memory controls proven by Stage 1.

### Goal 2

Given repository evidence and a bounded multi-step situation, produce a valid
short plan or repair:

- apply `next → begin → work/test → commit → complete → stop`;
- preserve unrelated work and stage named files;
- respond correctly to failed tests or missing prerequisites;
- distinguish blocked work from incomplete work;
- repair saga/git drift without hand-editing append-only metadata;
- notice a deterministic `agentrail --help` manifest mismatch and avoid using
  commands/signatures known only from the frozen training contract;
- explain process choices without inventing command output.

### Teacher contribution

GLM-5.x produces candidate trajectories, critiques, and corrected variants.
The pipeline decomposes them into state/action/reason steps. Deterministic
transition checks validate commands and order; repository-policy checks reject
unsafe/destructive actions; a human-review queue remains available for
judgment-heavy explanations. Teacher disagreement or failure is retained as
evidence rather than silently repaired.

### Acceptance

- exact transition validity and final-state correctness;
- ordered plan edit distance against held-out gold trajectories;
- command hallucination rate;
- recovery accuracy for failed-gate and saga/git-drift cases;
- explanation rubric scored separately from deterministic correctness;
- base, Stage-1 student, and Stage-2 student comparison;
- unchanged frozen live-help evaluation set;
- peak memory below 12,288 MiB.

## Shared MLPL architecture

MLPL files own:

1. frozen transition/action/help contracts;
2. bounded teacher-record ingestion and validation;
3. deduplication and train/validation/test identity separation;
4. deterministic correctness and drift checks;
5. response normalization and metrics;
6. versioned evidence reports and adapter provenance.

Thin external runners own the two effects MLPL cannot currently perform:

- calling the configured GLM-5.x endpoint to generate teacher candidates;
- invoking MLX-LM to tokenize, train QLoRA adapters, and generate responses.

Teacher generation and student training are separate recipes and artifacts.
Regenerating teacher data must never mutate the committed evaluation fixtures.

## sw-MLPL as the training-data laboratory

sw-MLPL already has the useful data-plane capabilities for this work even
though MLX-LM remains the model runtime:

- records, arrays, loops, user functions, mapping, filtering, and reduction for
  enumerating state spaces and transformations;
- deterministic seeded randomness for reproducible sampling, corruption, and
  split assignment;
- `to_json`, budgeted `parse_json`, deterministic `record_keys`, and
  duplicate-key rejection for versioned records;
- bounded reads, file sizes, byte/string handling, and atomic writes for
  dataset/report publication;
- Results and explicit errors for fail-closed schema, budget, leakage, and
  provenance validation;
- numeric arrays, reductions, fingerprints, loss/accuracy/regret calculations,
  and renderer-neutral curve IR for evaluation;
- existing repository examples for deterministic split validation, synthetic
  bandit-history generation, distilled-policy training, held-out ICRL rollout,
  adversarial controls, and exact JSON round-trips.

The planned MLPL generators should first emit a rich canonical record with
`id`, `source`, `state`, `target`, `rationale`, `validity`, `transform`,
`provenance`, and `split`. A final MLPL projection emits MLX-LM's supported
single-line `chat`, `completions`, or `text` JSONL. This keeps training-format
details downstream of the semantic dataset and allows the same records to feed
future CUDA tooling.

### Supervised approaches

| Approach | How sw-MLPL generates it | What it demonstrates |
|---|---|---|
| Rule-gold SFT | Enumerate valid Agentrail states from the frozen transition table; calculate the unique valid action and templated reason | Training without a teacher; exact correctness authority |
| Teacher-distilled SFT | Ingest GLM candidates, validate action/order deterministically, retain accepted rationale with teacher provenance | A strong teacher adds linguistic breadth and harder cases without becoming the authority |
| Counterexample classification | Pair each state with valid and invalid commands; label `accept`/`reject` plus the violated invariant | Safety and invalid-transition recognition |
| Repair supervision | Corrupt one step in a valid trajectory, then calculate the first bad step and corrected suffix | Debugging and recovery rather than rote command recall |
| Contrastive prompt/completion | Emit the same semantic state under paraphrases, reordered irrelevant fields, and bounded distractors with one invariant target | Robustness to presentation rather than memorization |
| Curriculum | Tag one-step, short-trajectory, recovery, and drift examples; materialize bounded mixtures by difficulty | The two students can share schema while learning different goals |

The current MLX-LM LoRA interface directly consumes chat/completion/text SFT
records. Preference pairs can still be generated and evaluated by MLPL, but a
DPO claim requires a separately selected trainer; the plan does not imply that
ordinary `mlx_lm.lora` performs preference optimization.

### Self-supervised and unsupervised approaches

“Unsupervised” must be used carefully. Causal language-model training on raw
text is normally **self-supervised** because the next token supplies the target.
Useful variants are:

| Approach | Generated material | Honest claim |
|---|---|---|
| Contract language modeling | Render canonical Agentrail rules and safe worked trajectories into bounded `text` JSONL | Self-supervised domain adaptation; no explicit action label |
| Missing-step reconstruction | Remove one action/reason from a valid trajectory and ask for the missing record | Self-supervised denoising after MLPL creates the target from the original |
| Next-step prediction | Use every valid trajectory prefix as input and its following step as completion | Self-supervised sequence prediction derived without teacher labels |
| Order/corruption detection | Shuffle, duplicate, truncate, or substitute steps using a fixed seed; preserve the uncorrupted source as target | Self-supervised structural learning and anomaly detection |
| Invariance views | Create equivalent field-order, whitespace, commentary, and irrelevant-evidence views | Consistency training/evaluation; semantics stay fixed |
| Unsupervised discovery | Cluster/count live help commands, failure phrases, or trajectory shapes without target actions | Corpus analysis only; clusters are not ground-truth workflow labels |

Pure unlabeled clustering is useful for finding coverage gaps and selecting
examples, but it cannot establish that an Agentrail action is correct. Every
workflow-correctness claim remains grounded in the frozen deterministic
transition validator and held-out gold records.

### Demonstration comparison

The final report should compare at least four data conditions for each student:

1. base model, no adaptation;
2. self-supervised contract/trajectory text only;
3. deterministic supervised gold only;
4. deterministic gold plus validated GLM distillation.

This ablation makes the value of labels, the value of the teacher, and the
effect of model scale visible instead of presenting one opaque fine-tune.

## Data and security controls

- Synthetic/minimized workflow states only; do not upload arbitrary repository
  contents, user prompts, credentials, git remotes, or source files.
- Fixed maximum prompts, responses, tokens, records, retries, and estimated
  cost before any teacher call.
- Raw teacher responses retained locally with hashes and rejection reasons.
- Prompt-injection strings included as adversarial data but never executed.
- No shell command emitted by teacher or student is automatically run.
- Model and dataset licenses recorded independently; generated-data terms must
  be reviewed for the selected GLM provider before publication.

## Recommended implementation sequence

1. `distillation-contract` — schemas, budgets, provider/model provenance, and
   deterministic transition validator.
2. `teacher-candidate-generator` — opt-in GLM-5.x adapter with dry-run/cost cap.
3. `stage-one-distillation` — accepted one-step corpus and 1.5B student.
4. `trajectory-validator` — multi-step decomposition, validation, and repair IR.
5. `stage-two-distillation` — 7B student and held-out recovery evaluation.
6. `distillation-acceptance` — reproducibility, ablations, memory, security,
   licensing, and comparison report.

## Sources

- [Official GLM-5 model repository](https://github.com/zai-org/GLM-5)
- [Official GLM-5 model card](https://huggingface.co/zai-org/GLM-5)
- [MLX-LM](https://github.com/ml-explore/mlx-lm)
- [MLX-LM LoRA/QLoRA guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
