import numpy as np
from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.properties import SafetyProperty
from .common import DomainCase


def water_case(attack_scale=1.0):
    # x=[tank1_m, tank2_m], u=[pump1, pump2] in normalized flow units.
    A = np.array([[0.985, 0.004], [0.006, 0.982]])
    B = np.array([[0.09, 0.0], [0.0, 0.075]])
    c = np.array([-0.025, -0.018])
    u = Interval([0.25, 0.20], [0.45, 0.40])
    w = Interval([-0.012, -0.012], [0.012, 0.012]).scale(attack_scale)
    sys = DiscreteLinearSystem(A, B, c, u, w, ("tank1_m", "tank2_m"), dt=1.0, name="water")
    x0 = Interval([1.4, 1.2], [1.6, 1.4])
    # This box captures high-high overflow region; separate low-level properties can be added.
    unsafe = Interval([3.2, 3.0], [20.0, 20.0])
    prop = SafetyProperty("avoid_overflow_region", unsafe, "Unsafe high-level region")
    return DomainCase("water", sys, x0, [prop], 50, {"tank1_m": "m", "tank2_m": "m"},
                      "Synthetic two-tank abstraction; not a model of a real treatment facility.")
