from dataclasses import dataclass
import numpy as np
from cpsverify.sets import Interval


@dataclass(frozen=True)
class BoundedFault:
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
