from dataclasses import dataclass, asdict
from cpsverify.diagnostics import diagnose_intersection
from cpsverify.domains import get_case
from cpsverify.reachability import reach_interval, reach_zonotope
from cpsverify.properties import check_safety


@dataclass
class VerificationRequest:
    domain: str
    method: str = "interval"
    steps: int | None = None
    attack_scale: float = 1.0
    property_index: int = 0
    max_generators: int = 50


@dataclass
class VerificationReport:
    domain: str
    method: str
    status: str
    property_name: str
    steps: int
    horizon: float
    first_intersection_step: int | None
    first_intersection_time: float | None
    reason: str
    assumptions: list[str]
    overlap: dict | None
    model_notes: str
    intersection_diagnostic: dict | None = None

    def to_dict(self):
        return asdict(self)


def _intersection_diagnostic(flowpipe, prop, step: int | None):
    if step is None:
        return None
    for item in flowpipe.sets:
        if item.step != step:
            continue
        reachable = item.set.interval_hull() if hasattr(item.set, "interval_hull") else item.set
        diagnostic = diagnose_intersection(reachable, prop.unsafe_set)
        return diagnostic.to_dict() if diagnostic is not None else None
    return None


class VerificationEngine:
    def verify(self, request: VerificationRequest) -> VerificationReport:
        case = get_case(request.domain, attack_scale=request.attack_scale)
        steps = request.steps if request.steps is not None else case.default_steps
        if request.method == "interval":
            fp = reach_interval(case.system, case.initial_set, steps)
        elif request.method == "zonotope":
            fp = reach_zonotope(case.system, case.initial_set, steps, max_generators=request.max_generators)
        else:
            raise ValueError("method must be 'interval' or 'zonotope'")
        prop = case.properties[request.property_index]
        result = check_safety(fp, prop)
        diagnostic = _intersection_diagnostic(fp, prop, result.first_intersection_step)
        return VerificationReport(
            case.name,
            request.method,
            result.status.value,
            prop.name,
            steps,
            steps * case.system.dt,
            result.first_intersection_step,
            result.first_intersection_time,
            result.reason,
            fp.assumptions,
            result.overlap.to_dict() if result.overlap is not None else None,
            case.notes,
            diagnostic,
        )
