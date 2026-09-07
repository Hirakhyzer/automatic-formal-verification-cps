import numpy as np


def monte_carlo_envelope(system, initial, steps, samples=1000, seed=0):
    """Sampling baseline. It is not a verification algorithm."""
    rng = np.random.default_rng(seed)
    mins = np.full((steps + 1, system.state_dim), np.inf)
    maxs = np.full((steps + 1, system.state_dim), -np.inf)
    for _ in range(samples):
        x = rng.uniform(initial.lower, initial.upper)
        for k in range(steps + 1):
            mins[k] = np.minimum(mins[k], x)
            maxs[k] = np.maximum(maxs[k], x)
            if k == steps:
                break
            u = rng.uniform(system.input_set.lower, system.input_set.upper) if system.input_dim else np.zeros(0)
            w = rng.uniform(system.disturbance_set.lower, system.disturbance_set.upper)
            x = system.A @ x + system.c + w
            if system.input_dim:
                x = x + system.B @ u
    return mins, maxs
