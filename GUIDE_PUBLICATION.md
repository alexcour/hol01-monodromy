# Publication procedure for HOL-01 v1.1.1

Versions 1.0.0 and 1.1.0 were internal release candidates and were never published. The intended first public release is `v1.1.1`.

## Before release

1. Read `HOL01_STATUS.md` first. It is the authoritative claim boundary.
2. From a fresh extraction, run `sha256sum -c SHA256SUMS.txt`.
3. Run `./VERIFY_LOCAL.sh` and save the output.
4. Confirm that README, note, Zenodo metadata and citation metadata all describe p = 7 as the principal certified result and all other primes as finite regression checks.
5. Confirm there is no universal-prime theorem claim and no all-level tower theorem claim.
6. Run CI on the exact commit to be tagged.
7. Create GitHub release/tag `v1.1.1` from that commit.
8. Archive that release with Zenodo as **Software**.
9. Do not invent ORCID or DOI values. Add them only when real.

## Public description

> Exact, dependency-free finite certificate for monodromy in the reduction of a Barning-Berggren congruence graph modulo 49 to modulo 7 above the root (3,4,5). The certificate verifies a 49-point fibre, monodromy order 686, a translation kernel of order 49, a dihedral linear image of order 14, and two explicit positive loops BABC and BABAA generating an order-343 Heisenberg subgroup. Additional primes are finite regression checks only. No theorem for all odd primes or all congruence levels is claimed.

## Do not claim

- that the computations at p = 3, 5, 7, 11, 13 prove a universal theorem;
- that the p^3 -> p^2 checks prove stability for all n;
- that the fibre is canonically `F_p^2` without explaining the affine torsor and coordinate choices;
- holonomy/curvature, Berry/Wilczek-Zee physics, RH, or Hilbert-Pólya consequences;
- novelty from the absence of a prior-art hit.
