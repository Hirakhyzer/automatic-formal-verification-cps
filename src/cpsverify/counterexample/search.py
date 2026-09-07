import numpy as np


def candidate_witness_region(check_result):
    """Return the overlap region that caused POTENTIALLY_UNSAFE.

    This is a *candidate* region, not a proven executable trajectory.
    """
    return check_result.overlap


def sample_counterexample_candidate(system, initial, unsafe_set, steps, samples=2000, seed=0):
    """Monte-Carlo search for a concrete candidate; failure to find one proves nothing."""
    rng = np.random.default_rng(seed)
    for _ in range(samples):
        x = rng.uniform(initial.lower, initial.upper)
        for k in range(steps + 1):
            if unsafe_set.contains(x):
                return {"step": k, "state": x.tolist()}
            if k == steps:
                break
            if system.input_dim:
                u = rng.uniform(system.input_set.lower, system.input_set.upper)
            else:
                u = np.zeros(0)
            w = rng.uniform(system.disturbance_set.lower, system.disturbance_set.upper)
            x = system.A @ x + system.c + w
            if system.input_dim:
                x = x + system.B @ u
    return None
