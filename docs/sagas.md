# AgentRail Saga Queue

Only one saga is active at a time. Later sagas are initialized after the
preceding saga is completed and archived. Steps are independently reviewable;
newly discovered work is inserted with AgentRail commands, never by editing
append-only `.agentrail/` state.

## Saga 1 — `binary-format-foundations`

1. `repository-check-gate` — add thin `just check` delegation, binary selection,
   fixture-generation conventions, and documentation/link/license checks.
2. `capability-probe` — executable probes for current byte I/O, bit operations,
   exact-integer limits, JSON header handling, and Result errors.
3. `safetensors-header-fixtures` — generated valid/truncated/oversized/malformed
   fixtures and a little-endian header-length decoder with golden tests.
4. `safetensors-catalog` — validate header schema, dtype/shape/offset invariants,
   and emit a deterministic tensor catalog for small files.
5. `bounded-range-upstream-contract` — turn measured whole-file limitations
   into a minimal API/security/acceptance contract without editing upstream.
6. `foundation-report` — catalog runnable demos, document complexity and
   limitations, and decide whether Saga 2 is unblocked.

Complete. The bounded arbitrary-name Safetensors catalog, fulfilled upstream
contract, and [foundation report](foundation-report.md) provide the acceptance
evidence and limitations needed for closeout.

## Saga 2 — `bounded-safetensors-analysis`

Status: complete. Bounded range I/O,
`file_size`, budgeted JSON decoding, duplicate-key rejection, and deterministic
record enumeration are shipped and covered by the repository gate.

1. Carry forward the completed range-reader conformance and adversarial
   EOF/overflow evidence.
2. Selective tensor slice reads and initial U8/I8/U16/I16 decoding — runnable
   in the default gate.
3. Mergeable statistics with fixed chunk size — runnable in the default gate.
4. Sparse large-artifact acceptance and measured peak memory — opt-in and
   passing on supported platforms.
5. Versioned, budgeted JSON visualization-summary IR and headless validation —
   runnable without a renderer dependency.

## Saga 3 — `gguf-inspection`

Status: acceptance complete. Bounded GGUF v3 scalar metadata and multiple-tensor cataloging
are runnable over tiny generated fixtures; exact-name selective I8/I16 payload
decoding and one-block Q8_0 golden dequantization are also runnable while
unsupported types remain catalog-visible. See the
[GGUF acceptance report](gguf-acceptance-report.md) for the gate evidence.

1. GGUF header, metadata, tensor directory, and alignment fixtures/parser.
2. Multiple-tensor cataloging, scalar metadata coverage, and catalog-visible
   active tensor type IDs — runnable without payload reads.
3. Unquantized selective I8/I16 tensor decoding — runnable in the default gate.
4. Q8_0 golden block decode and ggml reference parity — runnable in the default gate.
5. Bounded tensor sampling/statistics and measured acceptance report — runnable;
   the visualization gate is open.

## Saga 4 — `model-visualization`

Gate: open. Both Safetensors and GGUF now provide bounded catalogs, selective
decode, mergeable summaries, and measured large-artifact evidence suitable for
a budgeted renderer-neutral handoff.

1. Versioned renderer-neutral scene/tile schema and budget validation —
   runnable with cross-format golden JSON and headless validation.
2. Deterministic cross-format tensor-city layout — runnable from bounded
   catalogs without payload reads.
3. Selected-tensor distribution and sampled-surface tiles — runnable for
   bounded Safetensors integer and GGUF Q8_0 selections.
4. Q8_0 quantization-block and before/after error tiles — runnable with golden
   pointwise and aggregate metrics.
5. Bounded CLI/server JSONL transport and optional dependency-free client —
   runnable with deterministic envelopes; headless MLPL validation is retained
   as the acceptance authority.

Status: acceptance complete. See the
[visualization acceptance report](visualization-acceptance-report.md).

## Saga 5 — `native-quantization-and-conversion`

Gate: open. The Q8_0 reader, reconstruction metrics, error IR, and bounded
transport now provide reusable golden evidence for encoder work.

1. Numeric conversion/error metric golden vectors — runnable with bounded
   saturating i8/u8, f64 identity, and deterministic comparison evidence.
2. Symmetric INT8 and Q8_0 encode/decode round trips — runnable with exact
   bytes, independent existing-decoder acceptance, and reconstruction metrics.
3. Simple Q4 encode/decode round trips — runnable with an explicit teaching
   layout, exact nibble bytes, size ratio, and reconstruction evidence.
4. Safetensors-to-GGUF writer with self-validation — runnable for one bounded
   rank-one I8/I16 tensor with atomic output and catalog/value read-back.
5. Explicit external oracle adapters and reproducible comparison report —
   opt-in Python byte/parser comparison is runnable; llama.cpp availability is
   reported without misapplying it to an ineligible I16 teaching artifact.

Status: acceptance complete. See the
[quantization and conversion acceptance report](quantization-conversion-acceptance.md).

## Saga 6 — `restricted-checkpoint-extraction`

Gate: format and threat-model review is complete and resource budgets can be
enforced before allocation.

1. Passive ZIP/pickle opcode inventory and risk report — runnable for a tiny
   stored `data.pkl` container with dangerous-opcode reporting and zero
   deserialization/execution.
2. Budgeted allow-listed primitive stack-machine parser — runnable for an
   inert protocol-2 dictionary/list graph with memo and no-execution evidence.
3. Tensor metadata/storage-reference recovery — runnable for strict primitive
   five-field descriptors with member/range validation and zero payload reads;
   executable constructs and persistence remain rejected rather than invoked.
4. Tensor-only Safetensors extraction — runnable with deterministic padded
   headers, atomic replacement, independent catalog/decode read-back, and
   exact source/output value parity.
5. Cross-format verification and adversarial security report — complete with
   ten named rejection classes, internal read-back, an opt-in independent
   standard-library oracle, explicit non-goals, and attribution.

Status: constrained slice complete. See the
[checkpoint security acceptance report](checkpoint-security-acceptance.md).

## Saga 7 — `bounded-fine-tuning` (planned)

Build the shared adaptation evidence contract, a manual-gradient linear
fine-tuning demo, a teaching-sized low-rank adapter, a learning-curve IR, and
deterministic/oracle acceptance.

Status: acceptance complete. The shared contract, deterministic split/leakage fixture,
canonical parameter fingerprint, and numeric capability evidence are runnable.
Manual-gradient linear fine-tuning is also runnable with visible parameter,
trajectory, stopping, rejection, and held-out evidence.
Frozen-base low-rank adaptation is runnable with rank-one training, rank-two
shape support, merge parity, and explicit parameter-efficiency caveats.
Both trainers now emit a shared renderer-neutral curve/update/prediction IR
with aligned baselines, stable provenance, budgets, and headless validation.
The final acceptance gate adds reproducibility, hostile data/resource cases,
atomic exact read-back and pre-write destination preservation. See the
[fine-tuning acceptance report](fine-tuning-acceptance.md).

## Saga 8 — `in-context-learning` (planned)

Build a frozen associative-attention learner, context controls and leakage
checks, comparison visualization, and an optional pinned external-model
adapter. Deployment parameters must remain unchanged.

Current status: the versioned bounded context/query record, split/leakage
evidence, frozen deployment fingerprint, and zero-shot baseline are runnable.
Frozen associative inference now demonstrates improving zero/one/few-shot
predictions with visible kernel contributions and no parameter updates.
Context controls now expose order invariance, zero-effect distractors,
contradiction harm, truncation, empty selection, leakage, and budget failures.
The renderer-neutral ICL comparison IR now exposes aligned zero/one/few-shot
context, similarity, prediction, MSE, accuracy, fingerprint, and provenance data.
Status: acceptance complete. The final gate adds reproducibility, hostile data
and resource cases, atomic exact/semantic read-back, destination preservation,
attribution, and explicit limitations. See the
[ICL acceptance report](icl-acceptance.md).

## Saga 9 — `in-context-reinforcement-learning` (planned)

Build deterministic bandit baselines, source learning histories, a miniature
distilled history-conditioned policy, and held-out context-only reward
adaptation with an optional external LLM reward loop. Programmed UCB/greedy
baselines are not labeled ICRL.

Current status: deterministic source/held-out bandit tasks, reward tapes,
history and reward/regret metrics, and named non-ICRL greedy/UCB baselines are
runnable.
Deterministic diverse source UCB histories are now runnable with held-out
exclusion, task provenance, and reward/regret trajectories.
Offline policy distillation is now runnable with loss/parameter evidence,
held-out independence, and a versioned frozen artifact.
Held-out frozen-policy reward adaptation is now runnable with per-round context,
actions, probabilities, rewards/regret, and empty/shuffled/reward ablations.
Status: acceptance complete. Deterministic history IR, hostile data/resource
checks, atomic exact/semantic read-back, attribution, and limitations are
documented in the [ICRL acceptance report](icrl-acceptance.md).

The exact steps, proof standards, blockers, and terminology are defined in the
[adaptation demo plan](adaptation-demos-plan.md).

## Saga 10 — `lefts-inspired-composable-experiments` (planned)

Demonstrate LEFTS-inspired Split, Lift, Ensemble, Feed, and Tune concepts as
ordinary, inspectable MLPL. Begin with capability probes and an explicit tiny
learner; introduce reusable helpers only when they improve on direct array and
higher-order composition.

1. `lefts-capability-contract` — pin the binary and probe the function/value,
   collection, composition, and inspection capabilities needed for a minimal
   fit/predict computation contract; explain functor versus endofunctor and
   test the relevant identity/composition laws without overclaiming `M -> M`.
2. `split-lift-baseline` — build a self-describing grouped learner with visible
   split provenance, global baseline, per-group parameters, predictions, and
   explicit-versus-factored equivalence.
3. `ensemble-feed-composition` — demonstrate member disagreement and reduction,
   then a two-stage fed feature with visible intermediate values and ablation.
4. `tune-without-leakage` — score a bounded candidate set on validation data,
   explain deterministic selection, and evaluate once on held-out data.
5. `composed-rolling-experiment` — combine at least three concepts and emit a
   bounded inspectable computation description alongside explicit parity.
6. `lefts-acceptance` — add adversarial budgets, deterministic acceptance,
   catalog/navigation, attribution, limitations, and the promotion decision.

Gate: start in this repository with pure MLPL. An upstream or extension saga
is created only for a minimized `LANGUAGE_EXPRESSIVENESS_GAP` or
`NATIVE_CAPABILITY_GAP`. See the detailed [LEFTS plan](plan-lefts.md).

Current status: the callable and functor-law capability contract is runnable
on binary `7f6dee4d`. Named references, callable records, partials, returned
descriptions, `each`, `map_ok`, `table`, `atop`, and `over` support the tiny
fit/predict record without an upstream blocker. The explicit Split/Lift
baseline is next; see the [capability report](lefts-capability-contract.md).

The Split/Lift baseline is now runnable with explicit train/evaluation
provenance, leakage rejection, a global MSE 9 baseline, per-group MSE 0,
and exact explicit/factored parity. It retains the concrete grouped-fit name
rather than prematurely adding `experiment.lift`. Ensemble and Feed are next;
see [the demo report](split-lift.md).

Ensemble and Feed composition is now runnable. Ordered member predictions,
disagreement, aggregation, intermediate fed features, ablation metrics, and a
shared predict-record evaluator are visible. No cross-repository blocker was
found. Leakage-safe Tune is next; see [the report](ensemble-feed.md).

Tune is now runnable with three-way identity separation, visible candidate
scores, deterministic lower-index tie behavior, zero test reads during
selection, and exactly one held-out evaluation. The composed rolling
experiment is next; see [the report](tune.md).

The composed rolling experiment is now runnable with four concepts, changed
per-window fitted artifacts, visible fed signals and ensemble members, exact
explicit parity, and an independently round-tripped seven-node/six-edge IR.
Final acceptance is next; see [the report](rolling-experiment.md).

Status: acceptance complete. Repeated component outputs are byte-identical;
adversarial and resource cases, catalog/navigation, attribution, limitations,
and promotion decisions are documented. No `sw-mlpl`, native-extension, generic
Functor, or new-repository work is justified by the bounded slice. See the
[LEFTS acceptance report](lefts-acceptance.md).

## Saga 11 — `agentrail-qwen-mlx-finetune` (active)

Build an opt-in two-stage coding-model QLoRA demonstration under a measured
12 GiB limit. Qwen2.5-Coder-1.5B first proves the shared MLX pipeline on a
narrow exact-action task; Qwen2.5-Coder-7B then learns the Agentrail workflow.
MLPL remains responsible for contracts, validation, drift comparison, scoring,
and evidence, while a thin external adapter owns process execution and MLX-LM
owns tokenizer/causal-model operations.

1. `model-contract-and-preflight` — model inventory, license/provenance,
   dependency, PATH, checkpoint, data-separation, and memory contracts.
2. `small-model-pipeline` — Stage 1 Qwen2.5-Coder-1.5B before/after pipeline.
   Accepted locally: validation loss 5.865 to 0.002, held-out exact actions
   0/3 to 3/3, 1.319M trainable parameters, and 1.104 GB MLX training peak.
3. `agentrail-training-corpus` — frozen 12/3/3 MIT-provenance workflow corpus
   with valid, invalid, recovery, held-out, byte-reproducibility, and explicit
   live-help exclusion evidence.
4. `coding-model-agentrail-qlora` — Stage 2 Qwen2.5-Coder-7B adaptation.
   Accepted locally: validation loss 4.297 to 0.798, held-out exact actions
   0/3 to 3/3, rejection classification 2/3 to 3/3, 2.884M trainable
   parameters, and 4.781 GB MLX training peak.
5. `live-help-drift-evaluation` — deterministic live-interface comparison.
6. `acceptance-and-documentation` — consolidated evidence and CUDA handoff.

Current status: step 1 is runnable with a read-only preflight. This host has an
Ollama Qwen2.5-Coder 7B GGUF for inference, but neither required MLX Qwen
checkpoint nor MLX-LM is installed. See the
[two-stage demo contract](agentrail-mlx-finetuning.md).

The Qwen execution steps are temporarily queued behind two bounded CPU steps.
`progressive-help-escalation-demo` implements the model-independent typed
routing, privacy, and context-bundle mechanics. `trained-help-engram` then
trains an actual six-class route proposer with Engram and Adam, checks held-out
phrase variants, and keeps the learned result subordinate to the deterministic
evidence and consent boundary. Missing MLX prerequisites are recorded in
[mlx-traiing-todo.md](mlx-traiing-todo.md).

## Saga 12 — `agentrail-glm-qwen-distillation` (planned)

Use a configured GLM-5.x teacher to generate validated synthetic Agentrail
examples, then distill two different goals into two local MLX students. Stage 1
trains Qwen2.5-Coder-1.5B for exact one-step action/rejection behavior. Stage 2
trains Qwen2.5-Coder-7B for multi-step planning, recovery, explanation, and
help-drift-aware behavior. GLM-5.x is an external teacher because its roughly
745B-parameter MoE is not a 12 GiB local candidate. See the
[distillation plan](plan-agentrail-distillation.md).

## Cross-saga rules

- Do not modify `../sw-mlpl` inside these sagas.
- Do not download large models in the default validation gate.
- Never hide Python, llama.cpp, Hugging Face, Rust parsing, or rendering behind
  a claim that MLPL performed the substantive operation.
- Close a saga only when its acceptance evidence and known limitations are in
  user-facing documentation and the full repository gate passes.
