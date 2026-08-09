# Leakage-Safe Tune

Run `just tune` to see a bounded computation select configuration for a
downstream affine predictor. Two training rows fit slope 2. Validation then
scores offsets `[0, 1, 2]` with MSE `[1, 0, 1]`, selecting offset 1. Only after
selection are held-out inputs `[3, 4]` evaluated, producing `[7, 9]` at MSE 0.

Train, validation, and test IDs are pairwise checked before fitting. Candidate
selection records zero held-out reads and the report records exactly one
held-out evaluation. Equal validation scores retain the lower candidate index
because only a strictly smaller score replaces the incumbent.

This demonstrates LEFTS-inspired Tune as one computation producing
configuration for another. It is a tiny exhaustive teaching search, not a
claim of production hyperparameter optimization. Duplicate/leaking IDs,
empty or excessive candidates, malformed shapes, non-finite values, and work
budget overruns fail closed. No language or native blocker was found.
