from cpsverify.uncertainty import BoundedCyberEffect, BoundedFault, combine_effects, inflate_disturbance
from cpsverify.sets import Interval


def test_combined_effect_minkowski_bounds():
    a = BoundedCyberEffect("a", [-1, -2], [1, 2])
    b = BoundedCyberEffect("b", [-0.5, -0.25], [0.5, 0.25])
    c = combine_effects(a, b)
    assert c.lower[0] <= -1.5 and c.upper[1] >= 2.25


def test_fault_inflates_disturbance():
    base = Interval([-0.1], [0.1])
    f = BoundedFault("sensor", [-0.2], [0.3]).as_interval()
    total = inflate_disturbance(base, f)
    assert total.lower[0] <= -0.3 and total.upper[0] >= 0.4
