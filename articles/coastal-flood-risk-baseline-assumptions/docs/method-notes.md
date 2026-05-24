# Method Notes

This scaffold models coastal exposure as a threshold problem.

A simplified site-level exposure indicator is:

\[
E_i = \mathbf{1}(H_w + B + S + T + U \geq Z_i + P_i)
\]

where:

- \(H_w\) is modeled baseline water height.
- \(B\) is the baseline correction.
- \(S\) is the sea-level-rise scenario increment.
- \(T\) is tide and surge contribution.
- \(U\) is an uncertainty margin.
- \(Z_i\) is local land elevation.
- \(P_i\) is protective infrastructure height.
- \(E_i\) equals 1 when the site is exposed.

The scaffold compares exposure under two assumptions:

1. Modeled baseline only.
2. Corrected baseline including the local baseline correction term.

These equations are simplified for teaching and reproducibility. Operational coastal flood-risk modeling requires site-specific hydrodynamics, vertical datum alignment, high-resolution elevation data, tide-gauge records, storm-surge modeling, land-subsidence estimates, uncertainty propagation, and public review.
