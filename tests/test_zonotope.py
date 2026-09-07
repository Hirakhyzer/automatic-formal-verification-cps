import numpy as np
from cpsverify.sets import Interval, Zonotope


def test_zonotope_interval_conversion_contains_box():
    box = Interval([-2, 1], [4, 3])
    z = Zonotope.from_interval(box)
    hull = z.interval_hull()
    assert hull.lower[0] <= -2 and hull.upper[0] >= 4
    assert hull.lower[1] <= 1 and hull.upper[1] >= 3


def test_zonotope_affine_hull_contains_corner_images():
    box = Interval([-1, -2], [2, 1])
    z = Zonotope.from_interval(box)
    M = np.array([[1.0, 2.0], [-3.0, 0.5]])
    hull = z.affine_map(M).interval_hull()
    for x0 in (-1, 2):
        for x1 in (-2, 1):
            assert hull.contains(M @ np.array([x0, x1]))


def test_reduction_is_overapproximation():
    z = Zonotope([0, 0], np.array([[1, 0, 0.2, 0.1], [0, 1, 0.3, -0.2]], dtype=float))
    before = z.interval_hull()
    reduced = z.reduce(2)
    after = reduced.interval_hull()
    assert before.subset_of(after)
    assert reduced.generators.shape[1] <= 2
