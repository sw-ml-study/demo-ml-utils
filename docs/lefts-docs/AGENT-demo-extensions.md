# Agent Brief: `sw-ml-study/demo-extensions`

## Activation condition

Do not start this work merely because the LEFTS-inspired demo exists.

This brief becomes active only when `demo-ml-utils` supplies a minimized `NATIVE_CAPABILITY_GAP` that cannot reasonably be solved in pure MLPL or by an existing sw-MLPL capability.

`demo-extensions` is the incubator/research playground. A successful capability may later graduate into its own per-extension repository.

## Mission

Prototype the *smallest generic native capability* needed by the composable-experiments demo while preserving MLPL ownership of experiment semantics.

The extension must provide capability, not reimplement the ML DSL.

## Forbidden scope

Do not implement Rust-native versions of these merely by name:

- lift
- split
- feed
- ensemble
- tune

unless the blocker demonstrates that one of those names actually denotes an irreducibly native generic capability. That is unlikely.

Do not create a monolithic `lefts` extension.

Do not move ordinary orchestration, mapping, reduction, composition, or experiment definitions into Rust.

## Likely valid extension candidates

Examples include:

- generic parallel map/execution;
- external native numerical library bridge;
- mmap/range-backed numeric storage;
- zero/low-copy dense array service;
- GPU/device execution;
- generic cache/persistent native object;
- native callback/event-loop capability;
- optimized kernel where semantic reference remains in MLPL.

Choose only the capability identified by the upstream blocker report.

## Required inputs from `demo-ml-utils`

Before coding, require:

- minimized `.mlpl` reproducer;
- exact missing capability;
- expected semantics;
- reason pure MLPL is insufficient;
- reason this is native rather than a language expressiveness issue;
- at least one non-ML use case if the capability claims to be generic;
- acceptance criteria.

If those are absent, stop and request refinement in `demo-ml-utils`; do not invent the need.

## Architecture

Follow the existing extension architecture and contracts in this repository.

Prefer:

- private native namespace;
- public MLPL facade;
- one versioned ABI path;
- safe SDK/macros;
- host-owned/copy-safe values at boundaries;
- existing array/handle mechanisms when applicable;
- identical semantic surface regardless of static/dynamic provider once upstream supports it.

The public MLPL-facing name should describe the capability, not its implementation mechanism. Avoid public names like `native_*` unless the distinction is semantically necessary.

## Implementation sequence

1. Add a research note/saga naming the exact blocker.
2. Write Rust tests against the extension SDK/loader first.
3. Implement the smallest capability.
4. Add a tiny MLPL facade if the current integration surface permits it.
5. Add an isolated acceptance demo independent of ML.
6. Add an ML-oriented acceptance example only after the generic proof passes.
7. Document ownership, lifetime, errors, resource limits, determinism, and unsupported cases.
8. Run the repo's complete `just check`.

## Graduation rule

Recommend promotion into a standalone extension repo only when:

- the capability has a stable public contract;
- it is useful outside the one LEFTS-inspired demo;
- its lifecycle/versioning deserves independence;
- `demo-extensions` has proven ABI, safety, packaging, and acceptance;
- at least one real consumer is ready to depend on it.

Otherwise keep it as an incubated experiment.

## Deliverable back to `demo-ml-utils`

Return:

- the public capability contract;
- exact invocation syntax supported today;
- version/feature assumptions;
- deterministic test fixture/example;
- performance/resource notes;
- limitations;
- whether a pure-MLPL semantic reference implementation remains available.

The consumer repo should then decide whether using the extension improves the demo.
