# Shared Adaptation Contract

`just adaptation-contract` establishes the evidence shared by the planned
fine-tuning, in-context learning (ICL), and in-context reinforcement learning
(ICRL) demos before implementing any learner.

The generated `two-feature-linear` dataset contains four training examples,
two labeled-context examples, and three held-out evaluation examples. Numeric
IDs are unique within each split and disjoint across splits. Validation checks
all 26 cross-split ID pairs, flattened feature shapes, targets, finite values,
magnitudes, schema fields, and explicit example/feature/comparison/JSON/output
budgets. Flattened features are used because the current JSON decoder rejects
nested numeric arrays; consumers reshape only after validation.

The contract makes the central distinction executable:

| Mode | Deployment parameter updates | Adaptation input |
|---|---:|---|
| Fine-tuning | One or more | Training examples and objective |
| ICL | Zero | Labeled demonstrations in context |
| ICRL | Zero | Action/observation/reward history |

ICRL here follows the definition in the detailed
[adaptation plan](adaptation-demos-plan.md): inference-time reward-history
adaptation, not RL fine-tuning. A programmed UCB or greedy bandit remains a
baseline, not an ICRL claim.

Parameter fingerprints are canonical tagged JSON encodings of validated
numeric arrays. They are exact deterministic comparison evidence, not
cryptographic hashes. Later ICL/ICRL runs must carry identical before/after
deployment fingerprints; fine-tuning must record actual updates and different
parameters.

The executable numeric record pins `dot`, `matmul`, stable row-wise `softmax`,
`sigmoid`, `exp`/`log`, and deterministic seeded `random`. This unblocks tiny
manual-gradient and associative-attention implementations. It does not prove
production-scale numerical stability, autodiff behavior, accelerator support,
or real tokenizer/model inference.

Native code supplies the bounded file read, deterministic numeric primitives,
and generic JSON codec. MLPL owns dataset and leakage validation, terminology,
fingerprint policy, budgets, evidence construction, and report round-trip.
Real foundation-model execution remains an opt-in external layer.
