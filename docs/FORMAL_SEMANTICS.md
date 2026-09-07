# Formal semantics and guarantee boundary

## Supported core

The strongest v0.1 guarantee applies to finite-horizon reachability of the represented **discrete-time affine system**

\[
x_{k+1}=A x_k+B u_k+c+w_k
\]

with axis-aligned bounded sets for the initial state, input, and disturbance.

For interval propagation, each affine image is enclosed using the sign decomposition of the fixed matrix. Final floating-point bounds are expanded with `numpy.nextafter` toward negative/positive infinity. Therefore the implementation is deliberately conservative with respect to the represented floating-point coefficients.

## What `VERIFIED_SAFE` means

`VERIFIED_SAFE` means the computed over-approximation is disjoint from the modeled unsafe set at every stored step in the requested finite horizon.

It does **not** mean:

- the real plant exactly matches the model;
- unmodeled attacks or disturbances are covered;
- numerical assumptions have been independently machine-certified;
- a regulator or safety authority has certified the system;
- safety holds beyond the requested horizon.

## Zonotope semantics

For affine dynamics, the zonotope affine map and Minkowski sum are closed-form set operations. Generator reduction over-approximates discarded generators with an axis-aligned box. Safety is checked against the zonotope's interval hull, making a safe result conservative but potentially less precise than direct polyhedral intersection.

## Hybrid semantics

The hybrid engine supports box invariants/guards and affine resets. When a reachable box intersects a guard, both the no-transition and transition branch are retained. This is conservative for nondeterministic switching. A branch cap is a computational safeguard; if exceeded, sound-completeness is no longer asserted and the flowpipe is marked incomplete, causing `UNKNOWN`.

## Continuous-time models

Continuous-time nonlinear verification is a roadmap item. v0.1 deliberately does **not** label ordinary Euler simulation as formal continuous-time reachability.
