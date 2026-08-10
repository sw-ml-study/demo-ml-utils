# sw-MLPL Web Demo Handoff: Rolling Retrain (LEFTS-Inspired)

## Agent objective

Add a public-browser demo named **Rolling Retrain (LEFTS-inspired)** to the
existing sw-MLPL Web UI. Adapt the standalone source at:

```text
../demo-ml-utils/demos/experiments/lefts_page_web.mlpl
```

The result must remain browser-CPU runnable, self-contained, deterministic,
and explanatory. Do not introduce LEFTS-specific syntax, builtins, runtime
types, native code, or external dependencies.

This brief authorizes work only in the `sw-mlpl` repository. Follow that
repository's current `AGENTS.md`, Agentrail protocol, scoped-testing rules, and
`sw-checklist` ratchet requirements before making or committing changes.

## Placement decision

Use the existing **Experiment Quality** demo group.

Although Ridge is a classical ML algorithm, the demo's primary lesson is
experiment design:

- expanding-window retraining;
- preventing temporal leakage;
- fitting independent contextual models;
- routing each row to the correct model;
- reconstructing one out-of-time prediction series;
- inspecting the workflow and its evidence.

That makes it a closer companion to the existing Pareto Frontier, Robustness
Suite, and Scaffold Dependence demos than to a basic regression-algorithm demo.

Expected dropdown placement:

```text
Experiment Quality
  Pareto Frontier (which model size is worth it?)
  Robustness Suite (one model, five conditions)
  Rolling Retrain (LEFTS-inspired)
  Scaffold Dependence (train with hints, test without)
```

Names are sorted alphabetically within a group by the Web UI.

## Primary registry change

Edit:

```text
components/web-demos/crates/mlpl-web-demos/demos.toml
```

Add one `[[demos]]` record with:

```toml
category = "Experiment Quality"
name = "Rolling Retrain (LEFTS-inspired)"
```

The record needs a substantial `intro`, a substantial `takeaway`, and a
line-oriented `lines` program adapted from the standalone MLPL file.

Do not hand-edit generated Rust demo constants. `build.rs` generates them from
`demos.toml`.

## Intro: the “what will come” bookend

The `intro` should tell the user what will happen before execution:

- the domain is monthly demand forecasting;
- temperature, humidity, and hour-like activity are the three features;
- demand relationships can drift through the year;
- fitting once on the complete year would leak future observations into past
  predictions;
- the demo will train twelve independent Ridge-like models;
- model `m` trains only on rows before month `m` and predicts month `m` only;
- the outputs will expose growing history, fitted weights, routed predictions,
  actual demand, MSE, and an inspectable Lift-to-Leaf workflow.

Keep the framing concrete: the experiment simulates the information available
at each historical deployment decision.

## Key concepts to explain

Explain these in the intro, line comments, progress notes, or takeaway:

- **Leaf** — one ordinary fit/predict learner, here a bounded Ridge-like model
  with bias and weights for temperature, humidity, and activity.
- **Lift** — repeat that learner across twelve month contexts, producing twelve
  independent fitted parameter sets.
- **Train filter** — month `m` sees only rows with `month < m`; training counts
  therefore grow from 1 through 12.
- **Test routing** — the row for month `m` is predicted only by model `m`; the
  other models do not contribute to that cell.
- **Coalesce** — assemble the twelve disjoint monthly outputs into one
  calendar-ordered forecast vector.
- **Inspectability** — expose the workflow shape, training counts, fitted
  parameters, predictions, targets, and metric instead of reporting only PASS.
- **Closure/composition** — the LEFTS inspiration is transforming a
  fit/predict computation into another computation that can be inspected and
  composed again.

Do not claim a formal Functor or Endofunctor protocol. An `M -> M`-shaped
transformation does not itself define a morphism mapping or prove identity and
composition laws.

## Takeaway: the “what we showed” bookend

The `takeaway` should explicitly recap:

1. one Leaf learner became twelve independent monthly fits;
2. expanding history preserved time causality;
3. month routing prevented cross-month prediction mixing;
4. coalescing reconstructed one useful forecast series;
5. early models had less history and less stable coefficients;
6. later models used progressively more past evidence;
7. predictions and targets make MSE explainable;
8. the demonstration proves workflow structure, not production forecast
   quality.

End with the architectural conclusion: useful LEFTS-inspired composition is
expressible as ordinary MLPL without adding LEFTS-specific language features.

## Source adaptation rules

Use the standalone file as the behavioral source, but adapt it to the Web UI's
line-by-line demo runner.

Preserve:

- generated in-memory month, temperature, humidity, activity, and demand data;
- documented `def u:` functions;
- bounded deterministic Ridge-like gradient descent;
- twelve independent fits initialized separately;
- the strict `month < cutoff` training rule;
- matching-month prediction routing;
- training counts `[1, 2, ..., 12]`;
- the `[12, 4]` fitted-weight matrix;
- twelve coalesced predictions and twelve targets;
- finite MSE and explicit invariants;
- the printed `Lift 'monthly_retrain' -> Leaf 'ridge'` tree.

Remove or consolidate most tutorial `print` statements. The Web UI already
shows `intro`, each evaluated line, results, and `takeaway`; copying every print
from the standalone script would create a noisy evaluation history.

Prefer a small number of visible result lines:

- workflow tree;
- `{months, training_rows}`;
- the fitted weight matrix;
- `{predictions, actual_demand, mse}`;
- optionally a prediction-versus-actual chart, but only if the existing line
  renderer clearly handles two aligned series.

Each `def u:` entry in `lines` must be one complete parseable definition and
must begin its body with a documentation string. The Web demo smoke gate
enforces this.

Do not use `include`, fixtures, filesystem access, Python, sklearn, Polars,
network access, or a connected server. An unlisted capability record defaults
to CPU/live, which is correct for this demo.

## Attribution and compatibility boundary

Credit the official project and example:

- [LEFTS project](https://nsmat.github.io/lefts/)
- its landing-page rolling monthly Ridge/Lift example.

Suggested wording:

> Inspired by LEFTS's rolling monthly Ridge Lift example. This demo reproduces
> its experimental structure in ordinary MLPL; it is not a LEFTS Python API
> port.

State the differences:

- tiny generated data instead of a Polars dataframe;
- numeric months instead of date objects;
- deterministic gradient-descent Ridge analogue instead of sklearn Ridge;
- structural equivalence rather than API compatibility.

## Optional group-order improvement

`Experiment Quality` already exists in `demos.toml`, but it is not listed in
the curated section order. Consider editing:

```text
components/web-components/crates/mlpl-web-components-content/src/demo_gating.rs
```

Add `"Experiment Quality"` to `SECTION_ORDER`, preferably after
`"Training & Learning"` and before `"Classical ML"`.

If this is changed, update:

```text
components/web-components/crates/mlpl-web-components-content/tests/demo_order_tests.rs
```

Assert relative placement rather than a brittle full group list or exact demo
count.

This ordering change is useful but not required to land the demo itself. If it
would materially expand the current Agentrail step, insert a separate step.

## Progress notes

The registry supports `[[progress_notes]]` entries in `demos.toml`. Add one at
the twelve-fit line only if measured execution produces a noticeable pause.
The note should explain that twelve models are being fit independently and
that later models iterate over more historical rows.

Do not classify the demo as heavy or add it to `SKIP_DEMOS` without measured
evidence. The standalone version runs quickly on the current interpreter.

## Required tests

Run the scoped Web demo gate from the `sw-mlpl` repository:

```sh
scripts/gate.sh components/web-demos \
  mlpl-web-demos \
  mlpl-web-demos-smoke
```

The gate must establish that:

- `demos.toml` code generation succeeds;
- every line lexes, parses, and evaluates in one shared environment;
- every `def u:` has a leading doc string;
- the demo stays on the public CPU/live path;
- existing registry and metadata tests pass.

Add focused acceptance for the new demo when the existing smoke sweep does not
make these invariants sufficiently diagnostic:

- exactly 12 model identities;
- training counts exactly `1..12`;
- weight shape exactly `[12, 4]`;
- prediction and target lengths exactly 12;
- finite MSE;
- zero current/future-month rows used during fitting;
- deterministic repeated output or deterministic numeric evidence.

If `SECTION_ORDER` changes, also run the scoped gate for the owning Web
components workspace/package, including `mlpl-web-components-content` and its
ordering tests.

Follow the repository's current policy against running an unnecessary
all-components sweep.

## Pages build and deployment boundary

After scoped tests pass, build the committed GitHub Pages artifact:

```sh
scripts/build-pages.sh
```

Review the generated `pages/` changes and commit them according to the
repository's normal process. The live site is:

```text
https://sw-ml-study.github.io/sw-mlpl/
```

Do not run `scripts/deploy-pages.sh` unless the user has explicitly authorized
deployment. That script force-updates the generated `gh-pages` branch.

## Worktree and commit safety

At the time this brief was written, the adjacent `sw-mlpl` worktree already
contained unrelated modified and untracked files. They belong to the user or
other work. Preserve them, do not stage them, and do not fold them into this
change.

Before committing:

- inspect the exact diff and staged paths;
- follow the repository's Agentrail commit/completion ordering;
- satisfy the current `sw-checklist` ratchet or document an allowed exception
  exactly as required by `AGENTS.md`;
- commit the product change before `agentrail complete`;
- commit generated Agentrail completion metadata separately;
- push both commits so the next agent and GitHub can see them.

## Acceptance criteria

The work is complete when:

- `Rolling Retrain (LEFTS-inspired)` appears under `Experiment Quality`;
- it is enabled without a connected server on the public browser build;
- its intro clearly states the domain, problem, upcoming execution, and
  leakage risk;
- its lines fit twelve independent bounded models and expose meaningful
  intermediate/final evidence;
- its takeaway explains what was demonstrated and the limits of the claim;
- LEFTS is credited and Python API compatibility is explicitly disclaimed;
- the scoped Web demo and ordering gates pass;
- the pages build succeeds;
- unrelated worktree changes remain untouched;
- source, generated pages, and Agentrail state are committed and pushed under
  the repository's required process.
