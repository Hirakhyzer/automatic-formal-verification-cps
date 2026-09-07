# Benchmark protocol

The v0.1 benchmark evaluates each domain using:

1. outward-rounded interval reachability;
2. zonotope reachability with conservative reduction;
3. 1,000 seeded Monte-Carlo trajectories as a **non-verifying baseline**.

Record:

- verification status;
- horizon/steps;
- runtime;
- first possible unsafe intersection;
- set widths/volumes where meaningful;
- sampling envelope;
- disturbance scale.

For publication-quality experiments, repeat timing measurements, pin software versions, use multiple seeds for sampling, and report hardware. Do not compare one deterministic verification run to one stochastic timing run as if it were a statistically complete study.
