from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from cpsverify.sets import Interval, Zonotope


@dataclass
class DiscreteLinearSystem:
    """x[k+1] = A x[k] + B u[k] + c + w[k]."""

    A: np.ndarray
    B: np.ndarray
    c: np.ndarray
    input_set: Interval
    disturbance_set: Interval
    state_names: tuple[str, ...]
    dt: float = 1.0
    name: str = "linear_system"

    def __init__(self, A, B=None, c=None, input_set=None, disturbance_set=None,
                 state_names=None, dt=1.0, name="linear_system"):
        A = np.asarray(A, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("A must be square")
        n = A.shape[0]
        if B is None:
            B = np.zeros((n, 0))
        B = np.asarray(B, dtype=float)
        if B.ndim != 2 or B.shape[0] != n:
            raise ValueError("B shape mismatch")
        m = B.shape[1]
        c = np.zeros(n) if c is None else np.asarray(c, dtype=float).reshape(-1)
        if c.size != n:
            raise ValueError("c shape mismatch")
        if input_set is None:
            input_set = Interval.zeros(m)
        if disturbance_set is None:
            disturbance_set = Interval.zeros(n)
        if input_set.dim != m or disturbance_set.dim != n:
            raise ValueError("input/disturbance dimension mismatch")
        if state_names is None:
            state_names = tuple(f"x{i}" for i in range(n))
        if len(state_names) != n:
            raise ValueError("state_names length mismatch")
        self.A, self.B, self.c = A, B, c
        self.input_set, self.disturbance_set = input_set, disturbance_set
        self.state_names = tuple(state_names)
        self.dt, self.name = float(dt), name

    @property
    def state_dim(self):
        return self.A.shape[0]

    @property
    def input_dim(self):
        return self.B.shape[1]

    def step_interval(self, state: Interval, input_set: Interval | None = None,
                      disturbance_set: Interval | None = None) -> Interval:
        u = input_set or self.input_set
        w = disturbance_set or self.disturbance_set
        nxt = state.affine_map(self.A, self.c)
        if self.input_dim:
            nxt = nxt.minkowski_sum(u.affine_map(self.B))
        return nxt.minkowski_sum(w)

    def step_zonotope(self, state: Zonotope, input_set: Interval | None = None,
                      disturbance_set: Interval | None = None, max_generators=50) -> Zonotope:
        u = Zonotope.from_interval(input_set or self.input_set)
        w = Zonotope.from_interval(disturbance_set or self.disturbance_set)
        nxt = state.affine_map(self.A, self.c)
        if self.input_dim:
            nxt = nxt.minkowski_sum(u.affine_map(self.B))
        nxt = nxt.minkowski_sum(w)
        return nxt.reduce(max_generators)

    def with_disturbance(self, disturbance_set: Interval) -> "DiscreteLinearSystem":
        return DiscreteLinearSystem(
            self.A, self.B, self.c, self.input_set, disturbance_set,
            self.state_names, self.dt, self.name
        )
