import numpy as np
from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.properties import SafetyProperty
from .common import DomainCase


def robot_case(attack_scale=1.0):
    # x=[px, py, vx, vy], u=[ax, ay]; simple sampled double integrator.
    dt = 0.2
    A = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)
    B = np.array([[0.5*dt*dt, 0], [0, 0.5*dt*dt], [dt, 0], [0, dt]], dtype=float)
    c = np.zeros(4)
    # Controller abstraction constrained to progress along +x with small y correction.
    u = Interval([0.10, -0.04], [0.24, 0.04])
    w = Interval([-0.004, -0.004, -0.015, -0.015], [0.004, 0.004, 0.015, 0.015]).scale(attack_scale)
    sys = DiscreteLinearSystem(A, B, c, u, w, ("x_m", "y_m", "vx_mps", "vy_mps"), dt=dt, name="robot")
    x0 = Interval([0.0, 1.40, 0.6, -0.02], [0.1, 1.60, 0.8, 0.02])
    # Obstacle rectangle extruded over velocity dimensions.
    unsafe = Interval([4.0, -0.50, -10, -10], [5.0, 0.50, 10, 10])
    prop = SafetyProperty("avoid_obstacle", unsafe, "Obstacle occupies x=[4,5], y=[-0.5,0.5]")
    return DomainCase("robot", sys, x0, [prop], 30,
                      {"x_m": "m", "y_m": "m", "vx_mps": "m/s", "vy_mps": "m/s"},
                      "Reduced-order sampled kinematics; not a controller for a real robot.")
