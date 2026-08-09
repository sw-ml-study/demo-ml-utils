# Ensemble and Feed Composition

Run `just ensemble-feed` for two related LEFTS-inspired transformations.

The Ensemble example evaluates `2x` and `2x+2` in a declared order. Their
predictions differ by two everywhere and each has MSE 1 against `2x+1`.
Their arithmetic mean exactly recovers `[3, 5, 7]`, making the reason for the
MSE 0 aggregate visible rather than merely reporting success.

The Feed example computes `square(x)` upstream and exposes `[1, 4, 9]` before
passing it to `x + fed_feature`. This produces `[2, 6, 12]`. Removing the feed
edge leaves `[1, 2, 3]`, so the reported ablation error shows that the
intermediate is causally useful in this teaching construction.

Ensemble, Feed, and the Feed ablation are records with the same named
`predict` callable field. One bounded evaluator consumes all three, providing
an executable closure result at the computation-interface level. This is a
combinator result, not a claim that the transformations constitute a formally
defined category or endofunctor.

Empty/misaligned inputs, example overruns, and non-finite or excessive
predictions fail clearly. Aggregation is an ordered arithmetic mean; empty
ensembles are outside this bounded two-member demonstration. No native or
language blocker was found.
