# Threat model

The project studies **bounded abstract cyber effects** on a mathematical CPS model.

Examples include:

- additive sensor-estimation uncertainty that is translated into a bounded state/control effect;
- bounded command perturbation;
- bounded stale-state error due to modeled delay/replay;
- bounded coordinated disturbance across several state dimensions;
- attack-plus-physical-fault uncertainty.

The verifier answers safety questions only for effects inside the declared set. It does not model attacker access paths, authentication bypass, firmware exploitation, real protocol packets, credentials, or live targets.

A cyber effect outside the modeled bound invalidates the corresponding proof claim.
