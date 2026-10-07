from __future__ import annotations

from dataclasses import dataclass, asdict
import math

from .sets import Interval


@dataclass(frozen=True)
class IntersectionDiagnostic:
    """Explain a reachable-set/unsafe-set intersection without claiming a trace."""

    dimension: int
    overlap_widths: tuple[float, ...]
    overlap_volume: float
    reachable_volume: float
    unsafe_volume: float
    reachable_overlap_fraction: float | None
    unsafe_overlap_fraction: float | None
    candidate_center: tuple[float, ...]
    point_intersection: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _safe_fraction(numerator: float, denominator: float) -> float | None:
    if denominator <= 0.0 or not math.isfinite(denominator):
        return None
    return numerator / denominator


def diagnose_intersection(
    reachable: Interval,
    unsafe: Interval,
) -> IntersectionDiagnostic | None:
    """Quantify an over-approximation intersection.

    The candidate center is only a point inside the geometric overlap. It is
    not a concrete trajectory witness because the reachable set itself may be
    an over-approximation.
    """
    overlap = reachable.intersection(unsafe)
    if overlap is None:
        return None

    overlap_volume = overlap.volume()
    reachable_volume = reachable.volume()
    unsafe_volume = unsafe.volume()
    widths = tuple(float(value) for value in overlap.width())

    return IntersectionDiagnostic(
        dimension=overlap.dim,
        overlap_widths=widths,
        overlap_volume=overlap_volume,
        reachable_volume=reachable_volume,
        unsafe_volume=unsafe_volume,
        reachable_overlap_fraction=_safe_fraction(overlap_volume, reachable_volume),
        unsafe_overlap_fraction=_safe_fraction(overlap_volume, unsafe_volume),
        candidate_center=tuple(float(value) for value in overlap.center),
        point_intersection=any(width == 0.0 for width in widths),
    )
