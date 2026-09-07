from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval, Zonotope
from .flowpipe import Flowpipe, ReachSet


def reach_zonotope(system: DiscreteLinearSystem, initial: Interval | Zonotope,
                    steps: int, input_sets=None, disturbance_sets=None,
                    max_generators=50) -> Flowpipe:
    state = Zonotope.from_interval(initial) if isinstance(initial, Interval) else initial
    fp = Flowpipe(
        method="zonotope propagation with conservative generator reduction",
        sound_overapproximation=True,
        assumptions=[
            "discrete-time affine dynamics",
            "interval hull is used for property checking",
            "generator reduction boxes discarded generators conservatively",
        ],
    )
    fp.append(ReachSet(0, 0.0, state))
    for k in range(steps):
        u = input_sets[k] if input_sets is not None else None
        w = disturbance_sets[k] if disturbance_sets is not None else None
        state = system.step_zonotope(state, u, w, max_generators=max_generators)
        fp.append(ReachSet(k + 1, (k + 1) * system.dt, state))
    return fp
