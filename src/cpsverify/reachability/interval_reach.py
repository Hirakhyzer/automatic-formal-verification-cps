from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from .flowpipe import Flowpipe, ReachSet


def reach_interval(system: DiscreteLinearSystem, initial: Interval, steps: int,
                   input_sets=None, disturbance_sets=None) -> Flowpipe:
    if initial.dim != system.state_dim:
        raise ValueError("initial-set dimension mismatch")
    fp = Flowpipe(
        method="outward-rounded interval propagation",
        sound_overapproximation=True,
        assumptions=[
            "discrete-time affine dynamics",
            "all initial states lie in X0",
            "all inputs/disturbances lie in the supplied boxes",
            "model coefficients are the represented floating-point values",
        ],
    )
    state = initial
    fp.append(ReachSet(0, 0.0, state))
    for k in range(steps):
        u = input_sets[k] if input_sets is not None else None
        w = disturbance_sets[k] if disturbance_sets is not None else None
        state = system.step_interval(state, u, w)
        fp.append(ReachSet(k + 1, (k + 1) * system.dt, state))
    return fp
