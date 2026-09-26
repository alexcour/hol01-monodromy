# Publication gate — HOL-01 v1.1.1

A red item blocks publication.

## Reproduction

- [ ] Fresh extraction of the release archive succeeds.
- [ ] `sha256sum -c SHA256SUMS.txt` passes.
- [ ] `python3 hol01_certificate.py --check RESULTS.json` exits 0.
- [ ] `python3 independent_p7_permutation_check.py` exits 0.
- [ ] `python3 finite_prime_regression_check.py --check FINITE_REGRESSION_RESULTS.json` exits 0.
- [ ] CI is green on the exact commit to be tagged.

## Scientific boundary

- [ ] `HOL01_STATUS.md` is present and agrees with README and `HOL01_NOTE.pdf`.
- [ ] The principal public theorem/certificate is p = 7.
- [ ] p = 3, 5, 11, 13 are labelled finite regression checks only.
- [ ] p^3 -> p^2 at p = 3, 5, 7 is labelled exploratory exact computation only.
- [ ] There is no claim that `Mon_p ~= F_p^2 semidirect D_{2p}` has been proved for every odd prime.
- [ ] There is no claim that the argument extends to every `p^(n+1) -> p^n` level.
- [ ] The fibre is described intrinsically as an affine torsor; `F_p^2` appears only after coordinate choices.
- [ ] The p = 7 Heisenberg subgroup is supported by the explicit affine formulas/algebraic argument.
- [ ] The order-686 full group is labelled an exact finite computer-certified result unless/until a separate paper proof is supplied.
- [ ] No Berry/Wilczek-Zee, curvature, RH or Hilbert-Pólya claim is presented as established.

## Metadata / release

- [ ] Release tag is `v1.1.1`; v1.0.0 and v1.1.0 remain unpublished internal candidates.
- [ ] `date-released` in `CITATION.cff` and `publication_date` in `.zenodo.json` are the real release date.
- [ ] `.zenodo.json` and `CITATION.cff` agree on title, author, version and license.
- [ ] Zenodo record type is Software.
- [ ] No fake ORCID or DOI is present.

## Final disclosure check

- [ ] Repository contains no private audit material, credentials, email archives, unrelated research, or unpublished claims from other workstreams.
- [ ] Only after all checks: make the staging repository public and create release `v1.1.1`.
