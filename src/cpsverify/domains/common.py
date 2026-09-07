from dataclasses import dataclass
from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.properties import SafetyProperty


@dataclass
class DomainCase:
    name: str
    system: DiscreteLinearSystem
    initial_set: Interval
    properties: list[SafetyProperty]
    default_steps: int
    units: dict[str, str]
    notes: str = ""
