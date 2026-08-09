# LEFTS-Inspired Composable Experiment Demo Plan

## Goal

Demonstrate the central ideas of [LEFTS](https://nsmat.github.io/lefts/) as
ordinary, inspectable sw-MLPL programs. LEFTS treats a model as a pair of
`fit` and `predict` computations and defines five transformations—Split,
Lift, Ensemble, Feed, and Tune—that each produce another model. The important
property to test is closure: transformed computations can be composed again.

This is an inspired teaching implementation, not a port or API-compatibility
claim. Examples must explain the operation, show meaningful intermediate
values, interpret their results, and compare an explicit workflow with any
factored abstraction. A final `PASS` may validate the evidence, but it is not
the demonstration.

## Architectural decision

Start in this repository with zero Rust changes and zero language changes.
Use small deterministic learners so the experiment exposes composition rather
than hiding it behind a sophisticated model.

The ownership order is:

1. application-specific `.mlpl` in `demo-ml-utils`;
2. a reusable `.mlpl` library here, only after repetition proves its value;
3. an existing general sw-MLPL facility;
4. a narrowly scoped native capability incubated in `demo-extensions`;
5. a general language/runtime change in `sw-mlpl`.

No new repository is planned. `demo-functional-pipelines` receives no initial
work. It may later adopt an idiom only if the idiom is useful outside ML.

The public vocabulary is tentatively `experiment.*`. Do not add LEFTS names
to the global language namespace, and do not add `lift`, `feed`, or other
special syntax. A helper earns a name only when it is clearer than existing
array and higher-order operations.

## Questions the demos must answer

- Can MLPL represent a learner or computation as ordinary bounded data?
- Can functions be passed, stored, selected, and composed where the examples
  require it?
- Can a transformation return a value that can participate in the same
  `fit`/`predict` workflow?
- Can arrays or records describe collections and trees of computations?
- Can a user inspect the resulting computation and its intermediate values?
- Does a named helper improve the program over explicit `each`, partition,
  map, and reduction code?

A failed probe is evidence, not permission to redesign the language. Reduce it
to the smallest reproducer and classify it before escalating.

## Functor story

sw-MLPL currently supplies functor-like operations rather than a language-level
`Functor` interface:

- `each(f, array)` maps a callable over array elements while preserving shape;
- `map_ok(f, result)` maps the successful branch while preserving an error;
- `table`, `atop`, and `over` provide related application/composition forms;
- `call` accepts first-class user/builtin references and partials, and function
  references may be passed, returned, or stored in records.

That is enough to investigate LEFTS without adding a typeclass, trait, keyword,
or general closure facility. The demo documentation must distinguish these
terms precisely:

- a **functor** maps objects and the morphisms between them from one category
  to another while preserving identity and composition;
- an **endofunctor** is a functor whose source and target are the same category;
- a function shaped `M -> M` is only an endomorphism at the value/type level.
  That shape alone does not prove a functor, because no mapping of morphisms or
  preservation laws has yet been defined.

LEFTS transformations are therefore initially described as
*endofunctor-like*: they transform a fit/predict computation into another value
intended to support the same interface and further composition. They are not
automatically formal functors. The demo must identify its computation objects,
their composable mappings, and the observable identity/composition laws before
making a stronger claim. If those laws do not make sense for a transformation,
use the plainer term “combinator” or “computation transformation.”

The capability step will therefore probe:

- array identity and composition behavior under `each`;
- success/error preservation under `map_ok`;
- callable records and partials as model descriptions;
- identity wrapping and sequential transformation equivalence for the tiny
  fit/predict contract.

The corresponding demo narrative must show at least one concrete law check and
explain what it establishes—and what it does not establish—in plain language.

No generic `fmap` is proposed until at least two distinct containers need the
same user-facing abstraction and their laws and failure behavior can be stated
without special cases.

## Concept-to-demo map

| LEFTS idea | MLPL hypothesis | Demonstrable evidence |
| --- | --- | --- |
| Split | partition data and preserve train/evaluation provenance | visible row membership, leakage checks, sizes, and held-out metrics |
| Lift | instantiate or evaluate one computation per context with `each` | per-region parameters and predictions versus a global baseline |
| Ensemble | map predictions and reduce them deterministically | member disagreement, aggregate prediction, and error comparison |
| Feed | make one computation's output a feature or target for another | stage-one output, stage-two input, ablation, and final metric |
| Tune | let one computation select configuration for another | candidate scores, selected configuration, held-out result, and no test leakage |

For every concept, first show explicit MLPL. Factor a reusable helper only
when the comparison demonstrates a concrete clarity or reuse benefit.

## Delivery sequence

### 1. Capability probes and computation contract

Pin the active `mlpl-repl` version and probe function references, higher-order
calls, values returned from functions, records and arrays that describe
computations, nested application, and deterministic inspection. Define the
smallest honest model representation supported today. Publish a capability
matrix with runnable evidence and minimized failures.

Acceptance:

- probes run in the default gate and state the exact binary identity;
- supported and unsupported forms are not conflated;
- all collection, recursion, decode, and output work has explicit budgets;
- any failure has a copy-paste reproducer and one blocker classification.

### 2. Explicit grouped baseline, Split, and Lift

Use a tiny deterministic linear or mean learner over named regions. Show the
dataset, split provenance, global baseline, one fitted result per region,
per-region predictions, and combined metric. Then express the same workflow
using the most natural current MLPL composition.

Acceptance:

- the output explains what grouping changes and why the predictions differ;
- explicit and factored paths agree on deterministic results;
- held-out rows never affect fitted parameters;
- the report states whether a named `experiment.lift` helper is worthwhile.

### 3. Ensemble and Feed

Build an ensemble whose members make visibly different errors and report both
member predictions and the deterministic aggregate. Build a two-stage Feed
example where an upstream prediction becomes a downstream feature, and include
an ablation that removes the fed value.

Acceptance:

- aggregation, tie/empty behavior, and ordering are explicit;
- the Feed demo exposes the intermediate boundary and improves or predictably
  changes a held-out result relative to its ablation;
- each transformed computation remains usable by the same evaluation path, or
  the exact closure limitation is recorded.

### 4. Tune without evaluation leakage

Use a bounded candidate set to select a downstream learner configuration on a
validation partition, then evaluate exactly once on held-out data. Keep the
search intentionally small and display every candidate score.

Acceptance:

- train, validation, and test identities are disjoint and visible;
- deterministic tie-breaking and candidate budgets are tested;
- the output explains why the selected candidate won;
- Tune is described as computation producing configuration, not as a claim of
  production hyperparameter optimization.

### 5. Composed rolling experiment and inspectable description

Compose at least three concepts in one rolling or grouped experiment. Emit a
bounded, versioned, renderer-neutral computation description that names nodes,
edges, transforms, inputs, fitted artifacts, and metrics. Compare it with an
equivalent explicit implementation.

Acceptance:

- repeated windows or groups make the composition interesting and visible;
- the computation description is deterministic and independently validated;
- the narrative walks from input through intermediate outputs to the result;
- explicit and composed outputs agree, within documented numeric tolerance.

### 6. Acceptance and promotion decision

Close with adversarial budgets, deterministic reruns, a catalog entry, concise
README navigation, and a capability/blocker report. Record which helpers stay
local, which are genuinely reusable MLPL, and whether any cross-repository work
is justified.

Acceptance:

- `just check` exercises all default demonstrations and golden evidence;
- malformed shapes, empty groups, excess candidates/nodes/rows, non-finite
  values, leakage, and output overruns fail clearly;
- no Rust, Python, or external tool is hidden behind an MLPL implementation
  claim;
- LEFTS is credited as inspiration and differences/non-goals are explicit.

## Blocker and escalation contract

Every blocker must use one of these labels:

- `DEMO_BUG` — fix here.
- `LIBRARY_GAP` — factor ordinary MLPL here after proving reuse.
- `LANGUAGE_EXPRESSIVENESS_GAP` — stop and produce a minimal general
  reproducer for `sw-mlpl`; do not patch the adjacent repo in this saga.
- `NATIVE_CAPABILITY_GAP` — specify a general power such as parallel map,
  native numerical kernels, mmap, or caching for `demo-extensions`; do not
  implement LEFTS semantics in Rust.
- `PERFORMANCE_ONLY` — retain the correct teaching path and report measured
  limits before proposing acceleration.
- `ERGONOMICS_ONLY` — document the awkward form and compare it with existing
  roadmap mechanisms before proposing syntax.

An upstream request must include the active binary commit, minimal source,
expected and actual behavior, why ordinary MLPL/library code cannot solve it,
a non-ML motivating example, and interpreter/compiler parity requirements.

## Scope boundaries

- Tiny deterministic learners are sufficient; production training is not a
  goal.
- Parallelism, GPU execution, caching, native handles, and external ML
  libraries are optional later capabilities, not prerequisites.
- The default gate downloads no datasets or models.
- The work does not promise compatibility with LEFTS's Python API.
- Qualified modules are preferred when supported, but missing namespace sugar
  is not by itself a language blocker.

## Agentrail execution

The `lefts-inspired-composable-experiments` saga implements this plan in six
independently reviewable steps:

1. `lefts-capability-contract`
2. `split-lift-baseline`
3. `ensemble-feed-composition`
4. `tune-without-leakage`
5. `composed-rolling-experiment`
6. `lefts-acceptance`

Cross-repository work is not pre-created as an active saga. It begins only
after a step records a minimized blocker satisfying the escalation contract.

## Research sources

- [LEFTS project site](https://nsmat.github.io/lefts/)
- [Research transcript](lefts-python-inspired-work-research.txt)
- [Cross-repository overview](lefts-docs/OVERVIEW.md)
- [demo-ml-utils agent brief](lefts-docs/AGENT-demo-ml-utils.md)
- Conditional briefs for [sw-mlpl](lefts-docs/AGENT-sw-mlpl.md),
  [demo-extensions](lefts-docs/AGENT-demo-extensions.md), and
  [demo-functional-pipelines](lefts-docs/AGENT-demo-functional-pipelines.md)
