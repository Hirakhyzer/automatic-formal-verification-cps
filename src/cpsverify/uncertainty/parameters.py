from cpsverify.sets import Interval


def inflate_disturbance(base: Interval, additive: Interval) -> Interval:
    return base.minkowski_sum(additive)
