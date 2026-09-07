import numpy as np
from cpsverify.sets import Interval


def test_interval_affine_map_encloses_corners():
    box = Interval([-1, 2], [3, 4])
    M = np.array([[2.0, -1.0], [-0.5, 3.0]])
    image = box.affine_map(M, [0.2, -0.1])
    for x0 in (-1, 3):
        for x1 in (2, 4):
            y = M @ np.array([x0, x1]) + np.array([0.2, -0.1])
            assert image.contains(y)


def test_interval_intersection_and_subset():
    a = Interval([0, 0], [2, 2])
    b = Interval([1, -1], [3, 1])
    c = a.intersection(b)
    assert c is not None
    assert c.subset_of(a)
    assert c.subset_of(b)
    assert np.allclose(c.lower, [1, 0])
    assert np.allclose(c.upper, [2, 1])


def test_negative_scale_swaps_bounds():
    a = Interval([1, 2], [3, 4])
    b = a.scale(-2)
    assert b.lower[0] <= -6 and b.upper[0] >= -2
