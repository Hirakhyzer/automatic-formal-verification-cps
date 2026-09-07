import time
import numpy as np
from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.reachability import reach_interval, reach_zonotope


def synthetic_stable_system(dim: int):
    """Deterministic synthetic benchmark, not a physical plant model."""
    A = np.eye(dim) * 0.94
    for i in range(dim - 1):
        A[i, i + 1] = 0.03
    w = Interval(np.full(dim, -0.01), np.full(dim, 0.01))
    return DiscreteLinearSystem(A, disturbance_set=w, state_names=tuple(f"x{i}" for i in range(dim)), name=f"synthetic_{dim}d")


def scaling_sweep(dimensions=(2, 4, 8, 16, 32), steps=40):
    rows = []
    for dim in dimensions:
        sys = synthetic_stable_system(dim)
        x0 = Interval(np.full(dim, -0.1), np.full(dim, 0.1))
        for method in ("interval", "zonotope"):
            t0 = time.perf_counter()
            if method == "interval":
                fp = reach_interval(sys, x0, steps)
                hull = fp.sets[-1].set
            else:
                fp = reach_zonotope(sys, x0, steps, max_generators=max(50, dim))
                hull = fp.sets[-1].set.interval_hull()
            rows.append({
                "dimension": dim,
                "method": method,
                "steps": steps,
                "elapsed_s": time.perf_counter() - t0,
                "mean_final_width": float(np.mean(hull.width())),
            })
    return rows
