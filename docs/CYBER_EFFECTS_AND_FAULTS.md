# Cyber effects and faults as bounded uncertainty

The verification engine intentionally represents cyber effects and physical faults in the same mathematical language: sets of admissible perturbations.

This permits questions such as:

> Is the property safe for every disturbance in `W_fault ⊕ W_cyber`?

The abstraction is useful for resilience analysis but does not by itself distinguish attack from fault. Attribution belongs to the trustworthy-digital-twin/diagnosis repositories; this project focuses on **safety under bounded possibilities**.

The magnitude and units of each effect must be justified by a model, experiment, standard, or clearly labeled synthetic assumption before a publication-level claim is made.
