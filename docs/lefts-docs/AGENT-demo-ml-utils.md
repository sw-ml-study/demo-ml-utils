# Agent Brief: `sw-ml-study/demo-ml-utils`

## Mission

Create a LEFTS-inspired composable-experiments research slice using pure sw-MLPL first.

This is a language/library expressiveness experiment, not a port of the LEFTS implementation and not an excuse to add native code.

Preserve the repository's existing rule: substantive algorithms remain in MLPL wherever the language can express them.

## Non-goals

Do not:

- modify `sw-mlpl`;
- modify `demo-extensions`;
- create a new repository;
- add Rust;
- add new language keywords/builtins;
- imitate Python APIs for their own sake;
- hide gaps behind shell/Python helpers;
- claim a LEFTS concept requires a new primitive until an explicit MLPL formulation has been attempted.

## Step 0 — inspect before editing

Read at least:

- `README.md`
- `docs/plan.md`
- `docs/sagas.md`
- `docs/development.md`
- `docs/upstream-contract.md`
- `catalog/README.md`
- `AGENTS.md`

Follow the repo's existing AgentRail/TDD/catalog conventions.

## Step 1 — add a research/architecture document

Add a focused document such as:

`docs/composable-experiments-plan.md`

It should:

- credit LEFTS as inspiration;
- explain that the target is the algebra/closure idea, not API compatibility;
- define the implementation-layer rule: pure MLPL first;
- describe split/lift/ensemble/feed/tune conceptually;
- describe the blocker classification scheme;
- state that named combinators are optional if ordinary MLPL composition is already clearer;
- define the incremental acceptance sequence.

Do not rewrite the repository's main plan wholesale. Link the new plan from the appropriate existing planning/catalog docs.

## Step 2 — capability probes

Before building abstractions, add minimal executable probes for the capabilities the design needs.

Probe, using current legal sw-MLPL syntax:

- function references as values;
- passing user functions to higher-order operations;
- returning function-like/computation values if possible;
- storing the needed model state in records/arrays;
- arrays or collections of model/computation descriptions;
- `each`/higher-order application over those descriptions;
- composition of user functions;
- records carrying data plus behavior references, if supported;
- deterministic inspectability/printing of intermediate structures.

Do not assume object-oriented `Model` objects are necessary. Prefer data + functions if that is more natural in MLPL.

Each failed probe must produce a minimized blocker record rather than an immediate upstream request.

## Step 3 — tiny deterministic learner

Implement the smallest useful teaching learner needed to exercise composition.

Prefer something like:

- scalar/one-feature linear fit;
- mean predictor;
- threshold classifier;
- another tiny deterministic learner already easy in current MLPL.

The math must be intentionally boring.

Represent the learner/model in the simplest MLPL-native form that allows the subsequent experiments.

## Step 4 — explicit baseline demo

Create a runnable demo that does the workflow explicitly, without a new abstraction layer:

1. deterministic input dataset;
2. split/group into contexts;
3. construct/train one learner per context;
4. obtain predictions from all learners;
5. aggregate the predictions;
6. assert exact/golden results;
7. expose useful intermediate values.

This baseline is required. It lets later library helpers prove that they improve readability rather than just add vocabulary.

## Step 5 — implement concepts incrementally

Use separate small modules/files or the repository's established equivalent.

### A. split

Express a transformation selecting/partitioning training or evaluation data.

Acceptance:

- deterministic;
- visible partition contents/counts;
- malformed/empty cases covered;
- no unnecessary new abstraction.

### B. lift

Attempt first as ordinary MLPL:

`contexts |> each(make_or_transform_computation)`

or the closest current syntax.

Only add a named `lift` library function if it materially improves clarity or captures behavior beyond plain `each`.

Acceptance:

- several context-specific computations/models;
- their construction is inspectable;
- results equal the explicit baseline.

### C. ensemble

Map predictions and reduce them with a visible aggregation rule such as mean or vote.

Acceptance:

- aggregation policy is a supplied function/value where current MLPL permits;
- exact comparison to hand-computed expected output;
- edge cases documented.

### D. feed

Compose output from one fitted/computation stage into another.

This is a high-value expressiveness probe.

Acceptance:

- two distinguishable stages;
- intermediate output is inspectable;
- composed result matches explicit staged execution;
- if direct composability fails, minimize the failure before requesting anything upstream.

### E. tune

Use one computation/search/evaluation to produce configuration consumed by another.

Keep it tiny; e.g. select among a few thresholds or scalar hyperparameters.

Acceptance:

- candidate settings visible;
- scoring/selection visible;
- selected setting feeds the downstream learner;
- deterministic held-out evaluation.

## Step 6 — end-to-end composed demo

Add one demo combining at least three concepts, ideally split + lift + ensemble, then a second using feed or tune if concise.

A good candidate is rolling/grouped regression or threshold classification.

The headline should be the program structure, not predictive quality.

## Step 7 — library surface

Only after explicit implementations exist, factor repeated behavior into reusable `.mlpl`.

Tentative namespace/library name: `experiment`.

Possible public concepts:

- `experiment.split`
- `experiment.lift`
- `experiment.ensemble`
- `experiment.feed`
- `experiment.tune`

Treat these names as provisional. If an operation is more naturally expressed by existing `each`, `over`, `atop`, records, or pipelines, prefer the existing language and document that result.

## Step 8 — blocker report

Add/update a document such as:

`docs/composable-experiments-capabilities.md`

For every encountered gap classify it as:

- DEMO_BUG
- LIBRARY_GAP
- LANGUAGE_EXPRESSIVENESS_GAP
- NATIVE_CAPABILITY_GAP
- PERFORMANCE_ONLY
- ERGONOMICS_ONLY

For any candidate upstream/native gap include:

- minimized `.mlpl`;
- command used;
- exact result/error;
- expected semantics;
- why existing constructs are insufficient;
- workaround attempted;
- generality assessment;
- recommended owning repo.

Do not implement cross-repo fixes from this agent.

## Step 9 — catalog and tests

Integrate with the repo's normal demo catalog, tests, `just` recipes, documentation checks, and acceptance reports.

Default tests must remain tiny, deterministic, local, and redistributable.

## Deliverables

Expected minimum:

- `docs/composable-experiments-plan.md`
- `docs/composable-experiments-capabilities.md`
- pure `.mlpl` source for the tiny learner/computation representation
- explicit baseline demo
- split demo
- lift/equivalent demo
- ensemble demo
- feed demo or minimized blocker
- tune demo or minimized blocker
- one composed end-to-end demo
- tests/catalog/just integration
- links from existing planning/readme material as appropriate

## Stop conditions

Stop and report rather than crossing repo boundaries when:

- callable values cannot be represented as required;
- closures/function-returning-functions are insufficient;
- records/arrays cannot carry the required data/function references;
- higher-order invocation cannot handle the required user functions;
- a generic native service is actually necessary.

A blocked experiment with a precise reproducer is a successful outcome.

## Final report

Conclude with:

1. Which LEFTS ideas mapped directly to existing MLPL idioms.
2. Which named library helpers were worth keeping.
3. Which helpers were unnecessary.
4. Any language expressiveness gaps.
5. Any native capability gaps.
6. Exact proposed follow-up tasks, separated by owning repo.
