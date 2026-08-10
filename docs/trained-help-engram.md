# CPU-Trained Help Router with Engram

`just trained-help-engram` supplies the training stage that the protocol-only
`just help-escalation` demo intentionally lacks. It trains a small classifier
on CPU, with sw-MLPL's Engram conditional n-gram memory, and then evaluates
held-out phrase variants.

## What “trained” means here

This is not a synonym for a hand-written decision tree. The demo initializes a
fresh `engram(...)`, measures its held-out loss, and runs 160 Adam updates over
a bounded labeled tensor. The test requires that held-out loss decreases, all
six held-out examples receive the expected class, and `engram_stats` reports
nonzero memory rows. Learned results remain inert proposals with automatic send
and execution disabled.

The model is a tiny route classifier, not a generative help chatbot. Its six
classes correspond to `Answer`, `NeedDocs`, `NeedProgramContext`,
`NeedRepository`, `NeedReasoning`, and `OutsideDomain`.

## Data and generalization exercise

MLPL constructs six synthetic three-token training phrases and their one-hot
route labels. A token is a fixed-vocabulary feature, not a byte-pair tokenizer
or embedding-model result. Each held-out phrase changes its first token but
retains the decisive final bigram. This makes the demonstration narrow and
inspectable: Engram retrieves a learned route correction from local phrase
context instead of seeing an identical full input.

The synthetic corpus proves the mechanism, not production accuracy. A later
slice should generate licensed examples from the versioned help catalog,
reserve templates and command families before training, and report confusion,
calibration, collision, and adversarial results.

## Where Engram fits

`engram(hidden, ngrams, heads, slots, head_dim, seed)` owns a trainable hashed
n-gram table, value projection, and gate. `apply_engram` retrieves corrections
conditioned on token context. Adam writes the addressed rows; `engram_stats`
shows addressing, collisions, nonzero rows, row norms, and gate activity.

Engram is useful for frequent, local, versioned phrases such as command and
error patterns. It is not the documentation truth source, a permission system,
or a substitute for broader reasoning.

## Composition with the escalation protocol

The trained classifier proposes a class. The deterministic contract in
`src/help/escalation.mlpl` remains authoritative: retrieval and interpreter
evidence decide whether an answer is grounded; capability checks decide whether
program or repository context is needed; consent decides whether source or
transcript enters an inert bundle; and no learned score can send data or run a
command.
