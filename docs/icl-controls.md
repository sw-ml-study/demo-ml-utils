# ICL Context Controls

`just icl-controls` changes context while holding the deployment vector and
queries fixed. Reversing the two canonical examples preserves exact predictions
because the teaching kernel is additive. A zero-vector distractor has zero
similarity and contribution. Truncation produces the prior one-shot result and
empty selection produces the zero-shot baseline.

A third example conflicts with the x1 feature. It changes exact `[5,7,11]`
predictions to `[-11,7,-5]`: the x2-only query remains correct while x1-bearing
queries are damaged. The demo prints these outputs and losses so contradiction
sensitivity is observable rather than hidden behind an acceptance flag.

Record validation rejects duplicate context IDs and context/query ID leakage.
Focused tests also exhaust association-work, context-count, and ID-comparison
budgets. Before/after fingerprints remain exact and deployment updates stay
zero across every accepted control.

These results characterize this additive teaching kernel only. Transformer ICL
can be order-sensitive, distractor-sensitive in different ways, and governed by
token windows rather than these array budgets.
