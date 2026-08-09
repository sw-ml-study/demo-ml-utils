# Composed Rolling Experiment

Run `just rolling-experiment` to combine Split, grouped fitting (the
Lift-inspired operation), Feed, and Ensemble across two windows. Window one
learns offsets `[2, 8]`; window two refits changed offsets `[3, 9]`. Signals 1
and 2 are fed into the respective predictions, and symmetric ensemble members
make their averaging behavior visible.

The results `[13, 19]` and `[25, 31]` match a separately written explicit
calculation exactly. A versioned renderer-neutral IR records seven stable
nodes, six stable edges, inputs, fitted artifacts, signals, outputs, metrics,
provenance, and budgets. The test serializes and reparses that IR, then invokes
the validator independently.

Node, edge, grouped-work, identity-comparison, and encoded-output budgets fail
closed. The graph is a bounded computation description, not an execution
scheduler or a claim of formal categorical structure. No upstream blocker was
found.
