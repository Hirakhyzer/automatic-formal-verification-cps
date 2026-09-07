from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .rounding import down, up


@dataclass(frozen=True)
class Interval:
    """Axis-aligned interval/box with outward-rounded arithmetic.

    Bounds are represented by IEEE-754 floats. Operations expand their final
    floating-point result by one representable number in each direction.
    This is a conservative implementation relative to the represented model
    coefficients, but it is not a substitute for a proof assistant or a
    validated-numerics library for arbitrary expressions.
    """

    lower: np.ndarray
    upper: np.ndarray

    def __init__(self, lower, upper):
        lo = np.asarray(lower, dtype=float).reshape(-1)
        hi = np.asarray(upper, dtype=float).reshape(-1)
        if lo.shape != hi.shape:
            raise ValueError("lower and upper must have the same shape")
        if np.any(lo > hi):
            raise ValueError("lower must be <= upper componentwise")
        object.__setattr__(self, "lower", lo)
        object.__setattr__(self, "upper", hi)

    @property
    def dim(self) -> int:
        return int(self.lower.size)

    @property
    def center(self):
        return (self.lower + self.upper) / 2.0

    @property
    def radius(self):
        return (self.upper - self.lower) / 2.0

    def width(self):
        return self.upper - self.lower

    def volume(self) -> float:
        return float(np.prod(np.maximum(0.0, self.width())))

    def contains(self, point) -> bool:
        p = np.asarray(point, dtype=float).reshape(-1)
        return p.shape == self.lower.shape and bool(np.all(p >= self.lower) and np.all(p <= self.upper))

    def intersects(self, other: "Interval") -> bool:
        self._check_dim(other)
        return bool(np.all(self.lower <= other.upper) and np.all(other.lower <= self.upper))

    def intersection(self, other: "Interval") -> "Interval | None":
        if not self.intersects(other):
            return None
        return Interval(np.maximum(self.lower, other.lower), np.minimum(self.upper, other.upper))

    def subset_of(self, other: "Interval") -> bool:
        self._check_dim(other)
        return bool(np.all(self.lower >= other.lower) and np.all(self.upper <= other.upper))

    def minkowski_sum(self, other: "Interval") -> "Interval":
        self._check_dim(other)
        return Interval(down(self.lower + other.lower), up(self.upper + other.upper))

    def affine_map(self, matrix, bias=None) -> "Interval":
        M = np.asarray(matrix, dtype=float)
        if M.ndim != 2 or M.shape[1] != self.dim:
            raise ValueError("matrix shape incompatible with interval")
        pos = np.maximum(M, 0.0)
        neg = np.minimum(M, 0.0)
        lo = pos @ self.lower + neg @ self.upper
        hi = pos @ self.upper + neg @ self.lower
        if bias is not None:
            b = np.asarray(bias, dtype=float).reshape(-1)
            lo = lo + b
            hi = hi + b
        return Interval(down(lo), up(hi))

    def scale(self, factor: float) -> "Interval":
        f = float(factor)
        if f >= 0:
            return Interval(down(self.lower * f), up(self.upper * f))
        return Interval(down(self.upper * f), up(self.lower * f))

    def inflate(self, eps) -> "Interval":
        e = np.asarray(eps, dtype=float)
        if e.ndim == 0:
            e = np.full(self.dim, float(e))
        if np.any(e < 0):
            raise ValueError("inflation must be nonnegative")
        return Interval(down(self.lower - e), up(self.upper + e))

    def project(self, indices) -> "Interval":
        idx = np.asarray(indices, dtype=int)
        return Interval(self.lower[idx], self.upper[idx])

    def to_dict(self):
        return {"lower": self.lower.tolist(), "upper": self.upper.tolist()}

    @classmethod
    def zeros(cls, dim: int) -> "Interval":
        z = np.zeros(dim)
        return cls(z, z)

    def _check_dim(self, other: "Interval"):
        if self.dim != other.dim:
            raise ValueError("dimension mismatch")
