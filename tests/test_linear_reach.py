import numpy as np
from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.reachability import reach_interval, reach_zonotope


def test_scalar_linear_closed_form_enclosed():
    sys = DiscreteLinearSystem([[0.9]], c=[0.1], disturbance_set=Interval([-0.01], [0.01]))
    fp = reach_interval(sys, Interval([1.0], [1.1]), 5)
    # deterministic center trajectory with zero disturbance must be enclosed
    x = 1.05
    for k, item in enumerate(fp.sets):
        assert item.set.contains([x])
        x = 0.9*x + 0.1


def test_zonotope_and_interval_hulls_overlap():
    sys = DiscreteLinearSystem([[1.0, 0.1], [0, 0.95]], disturbance_set=Interval([-0.01, -0.01],[0.01,0.01]))
    x0 = Interval([-0.2, 1.0], [0.2, 1.2])
    fi = reach_interval(sys, x0, 4)
    fz = reach_zonotope(sys, x0, 4)
    assert len(fi) == len(fz) == 5
    assert fi.sets[-1].set.intersects(fz.sets[-1].set.interval_hull())
