# Fine-Tuning, ICL, and ICRL Demo Plan

## Goal

Add a progression of small, deterministic demos that makes three different
forms of adaptation visible:

| Mode | What changes during the demonstrated adaptation? | Required evidence |
|---|---|---|
| Fine-tuning | Model parameters | Before/after parameters, loss trajectory, held-out metrics, update count |
| In-context learning (ICL) | Context only; parameters remain fixed | Demonstrations/query, fixed-parameter fingerprint, prediction changes, order/distractor controls |
| In-context reinforcement learning (ICRL) | Action/observation/reward history only; deployment parameters remain fixed | Per-round history, rewards/regret, fixed-parameter fingerprint, held-out-task adaptation curve |

Here, **ICRL means in-context reinforcement learning**: adaptation at
inference time from interaction history without deployment-time parameter
updates. It does not mean RL fine-tuning, RLHF, or updating weights after each
reward. This follows the usage in
[Algorithm Distillation](https://openreview.net/pdf?id=hy0a5MMPUv). The later
LLM-oriented variant also records previous responses and scalar rewards in the
next prompt, but remains an external interoperability demo.

The proof standard is the same as the existing artifact demos: each recipe
must narrate its scenario, implementation boundary, budgets, actual outputs,
and interpretation. A recipe that only prints `PASS` is validation, not a
demo.

## Scope and non-goals

The default gate will use tiny numeric tasks and generated fixtures. It will
not download a foundation model, require a GPU, call a hosted API, or imply
that a hand-written learner is a production LLM. Real tokenizer/model
execution belongs behind an opt-in external adapter with a pinned model,
revision, dependency lock, seed policy, and output capture.

The first native demonstrations should favor interpretability over scale:

- manual bounded gradients instead of an autodiff framework;
- fixed datasets instead of unavailable runtime randomness;
- explicit vector/matrix loops instead of requiring a new tensor runtime;
- JSON evidence first, with learned-weight Safetensors artifacts only after
  floating-point byte encoding and multi-tensor writing are supported;
- external Python/PyTorch or another named framework only as an oracle or
  opt-in large-model implementation, never hidden behind an MLPL claim.

## Shared evaluation contract

All three tracks should use one versioned adaptation-run record with:

- task and dataset identifiers plus train/context/evaluation split hashes;
- method, seed or deterministic schedule, and implementation layer;
- parameter counts: total, trainable, and changed during deployment;
- configured ceilings for examples, features, classes/actions, steps/rounds,
  context records, arithmetic iterations, output elements, and bytes;
- before/after or per-round predictions, loss/reward, accuracy, and regret;
- parameter fingerprint before and after deployment-time adaptation;
- explicit leakage, baseline, determinism, and held-out-task checks;
- timing as descriptive evidence only, unless a separately specified
  performance methodology makes it comparable.

The report should round-trip through budgeted tagged JSON and feed a small
renderer-neutral learning-curve IR. Demos should show representative records
and explain why the curve changed.

## Track A — fine-tuning

### A1. Full-parameter teaching baseline

Train a two-feature linear regressor or binary logistic classifier on a fixed
tiny dataset using manually derived batch-gradient updates. Show:

- initial and final weights;
- loss at selected steps rather than an opaque final score;
- training and held-out predictions;
- gradient norm, learning rate, step count, and early-stop reason;
- a no-training baseline and an intentionally excessive-learning-rate failure.

The initial implementation may use squared loss so it needs only arithmetic
already observed in MLPL. Logistic loss follows only after stable `exp`/`log`
behavior is pinned by a capability probe.

### A2. Parameter-efficient adaptation

Freeze a small base matrix and train a rank-one or rank-two update
`delta = B * A`. Display base, adapter, merged weights, trainable-versus-total
parameter counts, update rank, loss curve, and parity between merged and
unmerged inference. This is a teaching-sized LoRA mechanism, motivated by the
original [LoRA paper](https://arxiv.org/abs/2106.09685), not a claim of
large-model fine-tuning.

### A3. Artifact and oracle acceptance

Write the run report atomically and self-validate it. Once floating-point
Safetensors writing exists, store base and adapter tensors separately and
verify merged predictions after read-back. An opt-in external oracle should
recompute the same fixed update trace and compare tolerances.

## Track B — in-context learning

### B1. Frozen associative-attention learner

Implement a tiny fixed-parameter predictor over vector demonstrations. Each
context record contains a feature key and label/value; the query attends to or
selects similar keys and aggregates their labels. No parameter changes occur.
This is a transparent mechanism demo of supervised adaptation from examples in
context, not a pretrained language model.

The demo compares zero-, one-, and few-shot contexts on held-out queries and
prints attention/similarity evidence, prediction, confidence or margin, and an
unchanged parameter fingerprint. Controls include shuffled order, irrelevant
demonstrations, conflicting labels, context truncation, and a leaked-label
fixture that must be rejected.

ICL terminology and the no-gradient distinction are consistent with
[Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165),
while the demo intentionally uses a much smaller inspectable model.

### B2. Optional real-model adapter

Add an opt-in adapter only after the native protocol is stable. It should run
the same zero/one/few-shot records against a pinned local model or explicitly
configured provider, record token counts and raw responses, normalize answers
without silently repairing them, and score with the MLPL-owned evaluator.
Network access, credentials, downloaded weights, and nondeterministic sampling
must remain outside `just check`.

## Track C — in-context reinforcement learning

### C1. Environment and non-ICRL baselines

Start with deterministic two-armed Bernoulli reward tapes and held-out bandit
tasks. Implement random/fixed, greedy, and UCB-style policies as clearly named
baselines. These policies establish reward and regret calculations; they must
not be labeled ICRL because their adaptation rule is directly programmed.

### C2. Miniature algorithm distillation

Generate bounded learning histories from a source bandit learner across
training tasks. Train a tiny sequence/history-conditioned policy to predict
the source learner's actions from prior action/reward context. At deployment,
freeze the learned parameters and evaluate unseen reward tapes while the
history grows.

The demonstration must show both phases:

1. training changes the distilled policy parameters across task histories;
2. held-out deployment improves reward or reduces regret using context only,
   while the parameter fingerprint remains unchanged.

Compare with the fixed and UCB baselines, an empty-history ablation, shuffled
rewards, truncated context, and an unseen task. Report exploration failures as
results rather than hiding unfavorable seeds. This is a small pedagogical
analogue of algorithm-distillation ICRL, whose defining property is
improvement entirely in context without parameter updates.

### C3. Optional LLM reward-context loop

After the bandit acceptance gate, an external adapter may demonstrate repeated
LLM attempts where the next context contains prior responses and scalar
rewards. Use a deterministic, locally scoreable task first (for example exact
arithmetic or constrained classification), cap rounds/tokens/cost, preserve
every attempt, and distinguish provider/model inference from MLPL-owned
orchestration and scoring. This is opt-in and cannot substitute for the
deterministic native acceptance path.

## Required foundations and blockers

### Runnable with the current boundary

- deterministic datasets and reward tapes;
- scalar/vector arithmetic, reductions, bounded loops, and manual gradients;
- report construction, budgeted JSON, atomic writes, and learning-curve IR;
- tiny matrix operations implemented as small MLPL library functions.

### Capabilities to probe before claiming them

- stable `exp`/`log` and overflow policy for softmax/logistic loss;
- deterministic pseudo-random generation or an explicit seeded native
  primitive if stochastic fixtures become necessary;
- efficient matrix multiplication/transpose and typed f32 arrays for demos
  larger than teaching scale;
- floating-point Safetensors encoding and multi-tensor writing;
- hashing/fingerprinting, or a canonical JSON/byte comparison substitute;
- tokenizer and causal-model inference interfaces for real-model ICL/ICRL.

Absence of these capabilities does not block the first squared-loss,
associative-attention, or fixed-reward-tape demos. It does block honest claims
of native large-language-model fine-tuning or inference.

## Recommended Agentrail sequence

Finish the active restricted-checkpoint saga before initializing these future
sagas.

### Saga 7 — `bounded-fine-tuning`

1. `adaptation-contract` — terminology, versioned run schema, deterministic
   datasets, split/leakage validation, and numeric capability probes.
2. `linear-fine-tune` — bounded manual-gradient baseline with visible loss and
   held-out predictions.
3. `low-rank-adapter` — frozen base plus rank-one/two adapter, merge parity,
   and trainable-parameter comparison.
4. `adaptation-curve-ir` — renderer-neutral loss/prediction/update evidence.
5. `fine-tuning-acceptance` — adversarial budgets, determinism, atomic report,
   and optional independent oracle.

### Saga 8 — `in-context-learning`

1. `context-record-contract` — context/query schema, budgets, split checks,
   parameter fingerprint, and zero-shot baseline.
2. `associative-icl` — fixed-parameter vector attention/nearest-example
   prediction with one/few-shot output evidence.
3. `icl-controls` — order, distractor, contradiction, truncation, and leakage
   cases.
4. `icl-comparison-ir` — context composition, attention, prediction, and
   accuracy visualization.
5. `icl-acceptance` — deterministic native report plus opt-in pinned external
   model adapter.

### Saga 9 — `in-context-reinforcement-learning`

1. `bandit-history-contract` — deterministic environments, reward tapes,
   history schema, reward/regret metrics, and named non-ICRL baselines.
2. `history-generator` — bounded source-learner histories across training
   tasks.
3. `distilled-context-policy` — train the tiny history-conditioned policy and
   freeze a versioned parameter artifact.
4. `held-out-icrl-rollout` — demonstrate reward adaptation from growing
   context with unchanged deployment parameters and ablations.
5. `icrl-acceptance` — held-out/adversarial evidence, curve IR, optional LLM
   reward-context adapter, and final limitations report.

## Acceptance decision

The first increment should be Saga 7 step 1, not a large-model integration.
It creates the shared evidence contract and probes the numeric operations that
all three tracks need. The first user-facing demo should then be the linear
fine-tuning baseline because it makes the crucial parameter-update distinction
visually obvious and supplies comparison machinery reused by ICL and ICRL.
