# Automatic Formal Verification of Cyber-Physical Systems

**Reachability analysis for bounded uncertainty, abstract cyber effects, faults, and safety properties.**

This repository is a PhD-oriented research framework for asking a stronger question than ordinary simulation:

> Given a mathematical CPS model, an uncertain initial set, bounded inputs/disturbances, a finite horizon, and an unsafe state set, can we prove that the entire reachable over-approximation remains outside the unsafe region?

The v0.1 core focuses on **discrete-time affine systems**, because its verification semantics can be stated precisely and tested rigorously. It provides outward-rounded interval propagation, zonotope propagation with conservative reduction, hybrid-mode orchestration, unsafe-set checking, candidate witness regions, bounded cyber/fault effects, verification-margin experiments, and four reduced-order CPS domains.

## Verification semantics

For

\[
x_{k+1}=A x_k+B u_k+c+w_k,
\]

with

\[
x_0\in X_0,\quad u_k\in U_k,\quad w_k\in W_k,
\]

the verifier computes an over-approximation \(\mathcal R_k\) of every state reachable at each step.

For unsafe region \(X_{unsafe}\), a property is returned as:

- **`VERIFIED_SAFE`** — every computed reachable over-approximation is disjoint from the unsafe set over the requested horizon.
- **`POTENTIALLY_UNSAFE`** — at least one over-approximation intersects the unsafe set. This is conservative: the intersection may be caused by set over-approximation and is **not automatically a concrete unsafe trajectory**.
- **`UNKNOWN`** — the computation was incomplete or lost its over-approximation guarantee.

A verification result is conditional on the **model, represented coefficients, bounds, property, horizon, and algorithm**. It is not a certification of a real deployment.

## Why cybersecurity belongs in reachability

Cybersecurity effects are represented only as bounded mathematical uncertainty in the simulated model, for example:

\[
y_k=Cx_k+a_k,\qquad a_k\in A,
\]

or an abstract bounded control/process effect:

\[
x_{k+1}=Ax_k+Bu_k+c+w_k+d_k,\qquad d_k\in D.
\]

The research question becomes:

> Is the unsafe set unreachable for **all admissible disturbances or cyber-effect signals inside the stated bounds**?

This project does not contain operational exploit procedures, protocol abuse, credentials, or live-system targeting.

## Included domains

| Domain | State abstraction | Example property |
|---|---|---|
| Battery | SOC, temperature | temperature remains below unsafe region |
| Water | two tank levels | avoid high-high overflow region |
| Robot | 2-D position and velocity | avoid obstacle rectangle |
| Railway | train separation, relative speed | preserve modeled minimum separation |

All four are **synthetic reduced-order models**. They are not calibrated replicas of real infrastructure.

## Methods

### Outward-rounded intervals

For a box \(X=[\underline x,\overline x]\), affine maps use the positive/negative matrix decomposition and expand computed bounds using `numpy.nextafter`.

This deliberately avoids accidental inward rounding at the final floating-point operation. The guarantee is relative to the represented floating-point model; this is not a replacement for arbitrary-precision validated numerics.

### Zonotopes

A zonotope is represented as

\[
Z=\{c+G\xi:\|\xi\|_\infty\le1\}.
\]

Affine maps and Minkowski sums preserve the representation. Generator reduction conservatively boxes discarded generators. Safety checks use the interval hull, so `VERIFIED_SAFE` remains conservative even if the hull loses precision.

### Hybrid reachability

The repository includes a branching interval engine for box guards/invariants and affine resets. It preserves both staying and enabled-transition branches. If the configured branch cap is exceeded, the flowpipe is explicitly marked incomplete and safety status becomes `UNKNOWN`.

## Quick start

```bash
python -m pip install -e ".[dev]"
pytest -q
python scripts/verify.py --domain battery --method interval
python scripts/run_benchmarks.py
```

Or after installation:

```bash
cpsverify battery --method zonotope --json
```

Example status output:

```text
Domain: battery
Method: interval
Property: temperature_below_60C
STATUS: VERIFIED_SAFE
```

The numeric result is a property of the included synthetic model and specified bounds—not a statement about a physical battery.

## Research experiments

The repository supports:

1. interval vs zonotope reachable-set conservatism;
2. reachability vs Monte-Carlo sampling;
3. verification under increasing bounded disturbance/cyber-effect magnitude;
4. safe-margin bisection;
5. hybrid mode/guard branching;
6. candidate witness-region extraction;
7. scaling with state dimension and horizon;
8. future digital-twin-informed bound tightening.

A particularly important comparison is **verification vs sampling**. Thousands of sampled trajectories remaining safe do not prove safety, while a sound reachable-set over-approximation can prove a finite-horizon property under the stated assumptions.

## Repository structure

```text
src/cpsverify/
  sets/             interval and zonotope representations
  models/           affine and hybrid CPS models
  reachability/     interval, zonotope, and hybrid propagation
  properties/       unsafe-set checking and verification status
  uncertainty/      bounded cyber/fault/parameter effects
  counterexample/   witness-region and sampling helpers
  domains/          battery, water, robot, railway abstractions
  benchmarks/       sampling and verified-margin experiments
  visualization/    optional flowpipe plots
  io/               configuration helpers
```

See `docs/` for the formal-semantics boundary, threat model, benchmark protocol, domain assumptions, research questions, limitations, and roadmap.

## Scientific integrity boundary

This project intentionally distinguishes:

- **formal over-approximation** from simulation;
- **potential unsafe intersection** from a concrete counterexample;
- **synthetic reduced-order models** from measurements;
- **bounded abstract cyber effects** from real attack procedures;
- **finite-horizon verification** from real-world certification.

## Relationship to the PhD program

This repository adds a proof-oriented pillar to the broader trustworthy-CPS research program:

```text
trustworthy-digital-twin-cps-benchmark
        ├── cross-domain detection / diagnosis / recovery
        ├── federated-trustworthy-digital-twin-cps
        │       └── distributed trustworthy intelligence
        └── automatic-formal-verification-cps
                └── finite-horizon reachable-set safety guarantees
```

A central future research question is whether a trustworthy digital twin can **tighten uncertainty sets online while preserving sound verification assumptions**, reducing reachable-set conservatism without turning a proof into a heuristic.

## References and related tools

The implementation is independent, but the research direction is informed by mature reachability ecosystems including **CORA**, **JuliaReach / ReachabilityAnalysis.jl**, and neural/learning-enabled CPS verification work such as **NNV**. See `docs/REFERENCES.md`.

## License

MIT. See `LICENSE`.
