# Counterexamples and witness regions

When an over-approximation intersects an unsafe set, the verifier returns the overlap as a **candidate witness region**.

This is not automatically a concrete trajectory. To find an executable candidate, `sample_counterexample_candidate` performs seeded Monte-Carlo search. Finding a sampled unsafe trajectory is evidence of a concrete model violation; failing to find one proves nothing.

A future refinement engine should back-propagate unsafe intersections and solve constrained reachability to construct validated counterexample traces.
