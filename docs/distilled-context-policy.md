# Distilled Context Policy

`just distilled-policy` extracts four offline examples from source histories.
The feature is cumulative arm-1 reward minus arm-0 reward; the label is the
source learner’s next action. Manual batch gradient descent trains a two-value
logistic policy for 40 steps and visibly reduces binary cross-entropy.

The published `sw-ml-study.distilled-context-policy` artifact is versioned,
fingerprinted, and frozen. Negative probe features select arm 0 and positive
features select arm 1. Held-out task 501 is named for separation, but contributes
zero records to training.

This offline update phase is explicitly not ICRL. The ICRL claim is reserved for
the next step, where this unchanged artifact consumes growing reward history on
a held-out task.
