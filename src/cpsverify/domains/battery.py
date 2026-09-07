import numpy as np
from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.properties import SafetyProperty
from .common import DomainCase


def battery_case(attack_scale=1.0):
    # Reduced-order discrete model: x=[SOC, temperature_C], u=[charge_power_pu].
    A = np.array([[1.0, 0.0], [0.0, 0.985]])
    B = np.array([[0.0040], [0.28]])
    c = np.array([0.0, 0.36])
    u = Interval([0.35], [0.55])
    # Bounded cyber/fault effect enters dynamics abstractly, not through a real BMS interface.
    w = Interval([-0.0004, -0.04], [0.0004, 0.04]).scale(attack_scale)
    sys = DiscreteLinearSystem(A, B, c, u, w, ("soc", "temperature_c"), dt=1.0, name="battery")
    x0 = Interval([0.50, 24.0], [0.55, 26.0])
    unsafe = Interval([0.0, 60.0], [1.2, 200.0])
    prop = SafetyProperty("temperature_below_60C", unsafe, "Unsafe when battery temperature reaches 60 C or above")
    return DomainCase("battery", sys, x0, [prop], 80, {"soc": "fraction", "temperature_c": "degC"},
                      "Synthetic reduced-order model; not calibrated to a specific cell or pack.")
