# Research context and historical embedding

**Repository:** `alexcour/hol01-monodromy-p7`  
**Public claim boundary:** exact finite certificate at (p=7).

## Historical line

The objects used here sit inside a long and well-developed mathematical history:

1. **Pythagorean triples and tree generation** — Berggren (1934), Barning (1963), Hall (1970).
2. **Modular interpretation** — Alperin (2005) relates the Pythagorean tree to the modular group and
   the congruence subgroup (Gamma(2)).
3. **Dynamical formulation** — Romik (2008) develops a dynamical system whose symbolic coding
   follows the Barning tree.
4. **Thin-orbit and congruence viewpoints** — Kontorovich–Oh and related work place Pythagorean
   triples in a broader group-orbit setting.
5. **Graph coverings and monodromy** — permutation/voltage descriptions of graph coverings are
   classical, with Gross–Tucker as a standard reference.
6. **Reduction modulo odd prime powers** — Biddle (2026) studies primitive Pythagorean triples
   modulo powers of odd primes and formalises substantial parts in Lean.

The repository should therefore not be read as introducing the Barning–Berggren tree, modular
parametrisation, graph monodromy, Heisenberg groups, or congruence filtrations.

## What this repository does

It packages one **bounded finite object** in exact, independently checkable form:

[
Gamma_{49}	oGamma_7
]

with the root (r=(3,4,5)^T), its 49-point fibre, the order-686 monodromy permutation group, and two
explicit short positive loops whose generated subgroup has order (7^3) and is identified
algebraically with (UT_3(mathbf F_7)).

The scientific value of the repository is therefore primarily:

- exact finite certification;
- explicit short witnesses;
- independent permutation cross-checking;
- reproducible regression evidence at additional primes;
- an explicit claim boundary separating finite fact from general theory.

## Later internal clarification: HOL-01U

After the public v1.1.1 boundary was frozen, the broader all-primes/all-levels pattern was revisited
internally. A 2x2/Schreier derivation explains the uniform structure using classical congruence-group
machinery. That internal branch is named **HOL-01U**.

HOL-01U is **not** a new public theorem claim of this repository and is not used to enlarge v1.1.1.
It is treated as a classical/unclaimed explanatory appendix in the wider research program.

This distinction is deliberate:

- **HOL-01 public:** finite exact (p=7) certificate;
- **HOL-01U internal:** classical structural explanation of the broader pattern;
- **no inference of novelty** from either the existence of the certificate or the later derivation.

## Why retain a finite certificate if the broad mechanism is classical?

A finite certificate can still be useful when the surrounding mechanism is known. It provides a
stable test object, exact witnesses, regression fixtures, and a concrete record of how a broad claim
was narrowed before publication.

That narrowing is part of the scientific provenance of the project.
