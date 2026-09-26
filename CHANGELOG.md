# Changelog

## 1.1.1 — 2026-09-24

**First intended public release. Claim-scope correction before publication.**

The exact p = 7 computations are unchanged. This release corrects the scientific packaging after critical review:

- withdraws the v1.1.0 claim that a proof was supplied for every odd prime;
- removes the statement that the argument extends "verbatim" to every level `Gamma_{p^(n+1)} -> Gamma_{p^n}`;
- treats p = 3, 5, 11, 13 strictly as finite regression checks;
- treats the `p^3 -> p^2` computations at p = 3, 5, 7 strictly as exploratory checks;
- replaces "canonically F_p^2" language by the intrinsic affine-torsor formulation, with coordinates only after choosing an origin/basis;
- adds `HOL01_STATUS.md` as the authoritative claim-status file;
- renames `uniform_structure_check.py` to `finite_prime_regression_check.py` and `UNIFORM_RESULTS.json` to `FINITE_REGRESSION_RESULTS.json`;
- rewrites the note so that its algebraic theorem is the explicit p = 7 Heisenberg subgroup, while the full order-686 group remains an exact finite computer-certified statement;
- preserves the general affine/cocycle formula only as a lemma and research route, not as a completed uniform classification.

Version 1.1.0 was an internal release candidate and was never published.

## 1.1.0 — 2026-09-24 — superseded before publication

Internal release candidate. It added a proposed uniform structural explanation and finite checks at several primes. Its wording overreached the proof actually written, especially for all congruence levels. Superseded by 1.1.1.

## 1.0.0 — internal release candidate — never published

Finite p = 7 certificate and regression checks. Superseded before public release.
