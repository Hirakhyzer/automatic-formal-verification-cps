from dataclasses import dataclass
import numpy as np
from cpsverify.sets import Interval


@dataclass(frozen=True)
class BoundedCyberEffect:
    """Abstract, simulator-only additive effect on state dynamics."""
    name: str
    lower: np.ndarray
    upper: np.ndarray
    description: str = ""

    def __init__(self, name, lower, upper, description=""):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "lower", np.asarray(lower, dtype=float).reshape(-1))
        object.__setattr__(self, "upper", np.asarray(upper, dtype=float).reshape(-1))
        object.__setattr__(self, "description", description)
        Interval(self.lower, self.upper)

    def as_interval(self):
        return Interval(self.lower, self.upper)


def combine_effects(*effects: BoundedCyberEffect) -> Interval:
    if not effects:
        return Interval.zeros(0)
    total = effects[0].as_interval()
    for effect in effects[1:]:
        total = total.minkowski_sum(effect.as_interval())
    return total
