import numpy as np
from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.properties import SafetyProperty
from .common import DomainCase


def railway_case(attack_scale=1.0):
    # x=[separation_m, relative_speed_mps]; positive relative speed closes the gap.
    dt = 1.0
    A = np.array([[1.0, -dt], [0.0, 0.94]])
    B = np.array([[0.0], [-0.45]])
    c = np.array([0.0, 0.0])
    # Conservative braking authority abstraction.
    u = Interval([0.35], [0.65])
    w = Interval([-0.35, -0.05], [0.35, 0.05]).scale(attack_scale)
    sys = DiscreteLinearSystem(A, B, c, u, w, ("separation_m", "relative_speed_mps"), dt=dt, name="railway")
    x0 = Interval([180.0, 8.0], [200.0, 10.0])
    unsafe = Interval([-1000.0, -100.0], [50.0, 100.0])
    prop = SafetyProperty("minimum_separation_50m", unsafe, "Unsafe when modeled train separation is 50 m or less")
    return DomainCase("railway", sys, x0, [prop], 18,
                      {"separation_m": "m", "relative_speed_mps": "m/s"},
                      "Abstract separation model only; no railway signaling protocol or deployment claim.")
