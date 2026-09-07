# Domain models

All included domains are intentionally reduced-order and synthetic.

## Battery

State: SOC and temperature. The model demonstrates coupled charge/thermal reachability. It is not fitted to a specific chemistry, cell, module, or pack.

## Water

State: two tank levels. The model demonstrates coupled inventory dynamics and overflow-region checking. It is not a model of a real treatment plant.

## Robot

State: planar position and velocity with bounded acceleration and disturbance. The property checks intersection with a rectangular obstacle. It is not a navigation stack or a real robot controller.

## Railway

State: separation and relative speed. The property checks a reduced-order separation threshold. It does not implement railway signaling protocols, interlocking standards, or operational train-control logic.

The purpose of these adapters is methodological diversity, not fidelity claims.
