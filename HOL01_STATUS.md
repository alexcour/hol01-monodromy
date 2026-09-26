# HOL-01 — authoritative scientific status for release v1.1.1

**Date:** 2026-09-24  
**Purpose:** single source of truth for the public claim boundary.

If another document conflicts with this file, this file governs release v1.1.1.

## PROVED / exact algebraic argument

- For p = 7, the affine actions of the positive loops `BABC` and `BABAA` generate a group isomorphic to `UT_3(F_7)` of order 343.
- Their non-commutation is explained by a nontrivial central commutator in that Heisenberg group.
- For any fixed p and loop W with `Wr = r mod p`, the first-order lift has affine form
  `u -> Wbar u + delta_p(W)` with `delta_p(W) = (Wr-r)/p mod p`, and `delta_p` satisfies the 1-cocycle identity. This formula alone does not classify the image.

## EXACT FINITE COMPUTATION / certified by the release

For the principal case p = 7:

- `|V_7| = 24`, `|V_49| = 1176`;
- every fibre of `V_49 -> V_7` has 49 points;
- the root fibre is the affine torsor `r + 7 T_7`;
- the monodromy permutation group has order 686;
- its translation kernel has order 49;
- its linear image is dihedral of order 14;
- a zero-translation complement of order 14 is found;
- in chosen coordinates the computed affine group is `F_7^2 semidirect D_14`;
- `BABC` and `BABAA` each have cycle signature `7^7` on the fibre and generate the order-343 subgroup.

The same program family performs finite checks at p = 3, 5, 7, 11, 13. Those additional rows are regression evidence, not a proof for all primes.

## EXPLORATORY EXACT CHECKS

- One higher congruence step `Gamma_{p^3} -> Gamma_{p^2}` is checked at p = 3, 5, 7.
- These checks test a possible all-level pattern; they do not establish it.

## CONJECTURE / theorem target

The following is **not** a theorem of release v1.1.1:

`Mon_p ~= F_p^2 semidirect D_{2p}` for every odd prime p.

It remains a theorem target until the image of the congruence stabilizer and the cocycle are proved uniformly.

## OPEN

- A proof valid for every step `Gamma_{p^{n+1}} -> Gamma_{p^n}`.
- A canonical, choice-independent formulation of the full affine coordinates beyond the torsor structure.
- A literature-level proof/reference identifying the relevant stabilizer quotient/core in the exact Barning-Berggren/Schreier formulation.
- HOL-02: any claim involving a canonical discrete connection/2-complex and curvature.

## TERMINOLOGY

The root fibre is intrinsically an affine torsor under the two-dimensional tangent space `T_7`. Writing it as `F_7^2` requires a choice of origin and basis. The distinguished lift `r` supplies a natural origin in the present computation; the vector-space coordinates still depend on a basis choice.

## NON-CLAIMS

No claim is made here of:

- a theorem for all odd primes;
- a theorem for every congruence level;
- a new general notion of monodromy, holonomy or curvature;
- a quantum interpretation;
- a consequence for the Riemann hypothesis.
