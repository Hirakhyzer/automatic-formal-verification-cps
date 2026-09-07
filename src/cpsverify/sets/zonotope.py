from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .interval import Interval
from .rounding import down, up


@dataclass(frozen=True)
class Zonotope:
    center: np.ndarray
    generators: np.ndarray

    def __init__(self, center, generators=None):
        c = np.asarray(center, dtype=float).reshape(-1)
        if generators is None:
            G = np.zeros((c.size, 0), dtype=float)
        else:
            G = np.asarray(generators, dtype=float)
            if G.ndim == 1:
                G = G.reshape(c.size, -1)
            if G.ndim != 2 or G.shape[0] != c.size:
                raise ValueError("generator matrix must have shape (dim, n_generators)")
        object.__setattr__(self, "center", c)
        object.__setattr__(self, "generators", G)

    @property
    def dim(self):
        return int(self.center.size)

    @property
    def order(self):
        return self.generators.shape[1] / max(1, self.dim)

    @classmethod
    def from_interval(cls, box: Interval) -> "Zonotope":
        return cls(box.center, np.diag(box.radius))

    def interval_hull(self) -> Interval:
        radius = np.sum(np.abs(self.generators), axis=1) if self.generators.size else np.zeros(self.dim)
        return Interval(down(self.center - radius), up(self.center + radius))

    def affine_map(self, matrix, bias=None) -> "Zonotope":
        M = np.asarray(matrix, dtype=float)
        if M.ndim != 2 or M.shape[1] != self.dim:
            raise ValueError("matrix shape incompatible with zonotope")
        c = M @ self.center
        if bias is not None:
            c = c + np.asarray(bias, dtype=float).reshape(-1)
        G = M @ self.generators if self.generators.size else np.zeros((M.shape[0], 0))
        return Zonotope(c, G)

    def minkowski_sum(self, other: "Zonotope") -> "Zonotope":
        if self.dim != other.dim:
            raise ValueError("dimension mismatch")
        G = np.concatenate([self.generators, other.generators], axis=1)
        return Zonotope(self.center + other.center, G)

    def reduce(self, max_generators: int) -> "Zonotope":
        """Conservative Girard-style simplification by boxing dropped generators."""
        if max_generators < self.dim:
            raise ValueError("max_generators must be at least the state dimension")
        if self.generators.shape[1] <= max_generators:
            return self
        scores = np.linalg.norm(self.generators, ord=1, axis=0)
        keep_count = max_generators - self.dim
        if keep_count > 0:
            keep_idx = np.argsort(scores)[-keep_count:]
        else:
            keep_idx = np.array([], dtype=int)
        mask = np.ones(self.generators.shape[1], dtype=bool)
        mask[keep_idx] = False
        dropped = self.generators[:, mask]
        kept = self.generators[:, keep_idx]
        box_r = np.sum(np.abs(dropped), axis=1)
        G = np.concatenate([kept, np.diag(box_r)], axis=1)
        return Zonotope(self.center, G)

    def to_dict(self):
        return {"center": self.center.tolist(), "generators": self.generators.tolist()}
