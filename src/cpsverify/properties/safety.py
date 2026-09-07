from dataclasses import dataclass
from cpsverify.sets import Interval, Zonotope
from cpsverify.status import VerificationStatus


@dataclass
class SafetyProperty:
    name: str
    unsafe_set: Interval
    description: str = ""


@dataclass
class SafetyCheckResult:
    status: VerificationStatus
    property_name: str
    first_intersection_step: int | None = None
    first_intersection_time: float | None = None
    overlap: Interval | None = None
    reason: str = ""


def _hull(s):
    return s.interval_hull() if isinstance(s, Zonotope) else s


def check_safety(flowpipe, prop: SafetyProperty) -> SafetyCheckResult:
    if not flowpipe.sound_overapproximation:
        return SafetyCheckResult(
            VerificationStatus.UNKNOWN, prop.name,
            reason="reachability computation was incomplete or not certified as an over-approximation",
        )
    for item in flowpipe.sets:
        box = _hull(item.set)
        if box.intersects(prop.unsafe_set):
            return SafetyCheckResult(
                VerificationStatus.POTENTIALLY_UNSAFE,
                prop.name,
                item.step,
                item.time,
                box.intersection(prop.unsafe_set),
                "reachable over-approximation intersects the unsafe set; this is not by itself a concrete unsafe trajectory",
            )
    return SafetyCheckResult(
        VerificationStatus.VERIFIED_SAFE,
        prop.name,
        reason="all computed reachable over-approximations are disjoint from the unsafe set over the requested horizon",
    )
