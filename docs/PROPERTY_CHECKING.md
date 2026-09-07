# Property checking

Safety properties are currently represented as unsafe axis-aligned boxes.

For each reachable set `R_k`, the checker tests whether its conservative box representation intersects the unsafe region.

- no intersections + sound flowpipe → `VERIFIED_SAFE`;
- an intersection → `POTENTIALLY_UNSAFE`;
- incomplete/non-sound flowpipe → `UNKNOWN`.

`POTENTIALLY_UNSAFE` is intentionally not called `VIOLATED`: an over-approximation may intersect the unsafe set even when no concrete trajectory does.

Future work will add half-space/polyhedral properties, temporal properties, and refinement procedures.
