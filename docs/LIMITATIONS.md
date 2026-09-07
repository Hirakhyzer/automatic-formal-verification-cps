# Limitations

v0.1 deliberately has strong boundaries:

- core formal claims target discrete-time affine models;
- nonlinear continuous-time reachability is not yet implemented;
- outward rounding uses IEEE-754 `nextafter`, not a full arbitrary-precision validated-numerics stack;
- model coefficients themselves may be uncertain in reality unless explicitly bounded;
- unsafe properties are axis-aligned boxes;
- zonotope safety checking uses interval hulls and may be conservative;
- hybrid branching can grow exponentially;
- cyber effects are abstract bounded perturbations, not protocol-level models;
- candidate witness regions are not necessarily executable trajectories;
- all domain parameters are synthetic/illustrative;
- no result constitutes certification of a real battery, plant, robot, grid, railway, or controller.
