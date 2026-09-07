# v0.1 baseline findings

These numbers come from the synthetic reduced-order models in this repository and were reproduced locally before publication. They are **not measurements from real CPS**.

## Verification results at default disturbance scale = 1.0

| Domain | Interval | Zonotope | Horizon | First possible unsafe intersection |
|---|---|---|---:|---:|
| Battery | VERIFIED_SAFE | VERIFIED_SAFE | 80 steps | — |
| Water | VERIFIED_SAFE | VERIFIED_SAFE | 50 steps | — |
| Robot | POTENTIALLY_UNSAFE | POTENTIALLY_UNSAFE | 30 steps / 6 s | step 19 at default scale after benchmark redesign |
| Railway | VERIFIED_SAFE | VERIFIED_SAFE | 18 steps | — |

The robot result is intentionally conservative: the nominal disturbance-free case (`attack_scale=0`) is verified safe, but the default uncertainty set produces a reachable-box/zonotope-hull intersection with the obstacle. A 5,000-sample Monte-Carlo search at scale 1 did not find a concrete unsafe trajectory, illustrating that `POTENTIALLY_UNSAFE` can represent over-approximation rather than a real counterexample.

At larger robot uncertainty (`attack_scale=4`), a seeded 20,000-sample search did find a concrete simulated state inside the obstacle region at step 22. Sampling is used only as counterexample search; its failure never proves safety.

## Disturbance/cyber-effect margin sweep

The scalar `attack_scale` uniformly scales each domain's synthetic bounded disturbance set. Bisection reports a **verified-safe lower bound** and the first not-verified upper bracket when one is found.

| Domain | Verified-safe scale lower bound | First not-verified upper bound | Interpretation |
|---|---:|---:|---|
| Battery | >= 8.0 | not bracketed | searched range remained verified |
| Water | 3.8172851 | 3.8172855 | narrow numerical bracket |
| Robot | 0.1214390 | 0.1214395 | nominally safe but sensitive to uncertainty |
| Railway | 3.0003767 | 3.0003772 | finite verified disturbance margin |

These margins are properties of the included mathematical models and chosen horizons only.

## Interval vs zonotope

For the current low-dimensional affine cases, the final zonotope interval hull is very close to the interval result. This means v0.1 does **not** yet demonstrate a large precision advantage from zonotopes. That is itself useful: future benchmarks should add dynamics with stronger sign changes/correlations and higher dimensionality where wrapping effects become measurable.

This repo therefore avoids claiming that zonotopes are already superior on the included four toy domains.

## Timing observation

On the local validation environment, interval and zonotope verification completed in milliseconds for these small models, whereas 1,000-trajectory Monte-Carlo baselines took hundreds of milliseconds to roughly seconds. These single-run timings are illustrative only; publication-quality performance claims require repeated runs and hardware/software provenance.

## Research gaps exposed by v0.1

1. **Spurious intersection refinement** — when an over-approximation hits an unsafe set but sampling does not, automatically refine the state set or time partition.
2. **Continuous-time soundness** — add validated matrix-exponential/remainder enclosures instead of ordinary numerical integration.
3. **Nonlinear reachability** — implement Taylor/interval remainder techniques or interface with established tools.
4. **Correlation-sensitive benchmarks** — construct higher-dimensional systems where zonotopes materially reduce wrapping.
5. **Validated counterexamples** — convert candidate witness regions into proven trajectories or prove the intersection spurious.
6. **Digital-twin bound tightening** — reduce uncertainty online without silently invalidating formal coverage assumptions.
