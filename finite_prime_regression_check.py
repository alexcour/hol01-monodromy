#!/usr/bin/env python3
"""
HOL-01 v1.1.1 -- finite-prime regression check (Python standard library only).

This program performs exact finite regression checks for the congruence
covering Gamma_{p^2} -> Gamma_p at p in (3, 5, 7, 11, 13), and writes a
deterministic JSON snapshot. These checks are evidence at the listed moduli,
not a proof of a theorem for every odd prime.

For each p it verifies:
  * |V_p| = (p^2 - 1)/2 and |V_{p^2}| = p^2 |V_p|;
  * the fibre above r = (3,4,5) is r + p * r^perp, and it is also the image
    r + p * dphi_(2,1)(F_p^2) of the differential of the parametrisation
    phi(m, n) = (m^2 - n^2, 2mn, m^2 + n^2) at (2, 1);
  * every Schreier loop g acts on the fibre by an affine map u -> L u + t,
    checked point by point against the matrix action modulo p^2;
  * in the basis (r, e1) of r^perp, L = [[1, b], [0, eps]] with
    eps = det(g) = (-1)^(number of letters B in the loop word);
  * the monodromy group has order 2p^3; its translations form F_p^2; the
    elements with eps = +1 form a non-abelian group of order p^3 and exponent p
    whose centre is the group of translations along r; a point stabiliser has
    order 2p, so the covering is not regular.

At p = 7 it checks the explicit loops of the note. It also performs an
exploratory exact check of one further step Gamma_{p^3} -> Gamma_{p^2} for
p = 3, 5, 7; those three computations are not a theorem for arbitrary n.

No floating-point arithmetic and no third-party package is used.
Exit status is non-zero if any assertion fails.

usage:
    python3 finite_prime_regression_check.py                 # run all checks
    python3 finite_prime_regression_check.py --check FINITE_REGRESSION_RESULTS.json
    python3 finite_prime_regression_check.py --write-json FINITE_REGRESSION_RESULTS.json
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path

# Barning-Berggren matrices (same convention as hol01_certificate.py):
# A = M3, B = M2, C = M1, acting on column vectors; a word is applied left to right.
A = ((1, -2, 2), (2, -1, 2), (2, -2, 3))
B = ((1, 2, 2), (2, 1, 2), (2, 2, 3))
C = ((-1, 2, 2), (-2, 1, 2), (-2, 2, 3))
GEN = {"A": A, "B": B, "C": C}
J = ((1, 0, 0), (0, 1, 0), (0, 0, -1))
I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
R = (3, 4, 5)
E1 = (1, -2, -1)                   # together with R, a basis of r^perp mod every odd p
PRIMES = (3, 5, 7, 11, 13)
TOWER_PRIMES = (3, 5, 7)
VERSION = "1.1.1"


def require(cond: bool, message: str) -> None:
    if not cond:
        raise AssertionError(message)


def mul(X, Y, m=None):
    Z = tuple(tuple(sum(X[i][k] * Y[k][j] for k in range(3)) for j in range(3)) for i in range(3))
    return tuple(tuple(z % m for z in row) for row in Z) if m else Z


def app(M, v, m=None):
    w = tuple(sum(M[i][k] * v[k] for k in range(3)) for i in range(3))
    return tuple(x % m for x in w) if m else w


def inv(M, m=None):
    """Inverse of an element of O(Q): J M^T J."""
    return mul(mul(J, tuple(zip(*M)), m), J, m)


def det3(M):
    (a, b, c), (d, e, f), (g, h, i) = M
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def word_matrix(word: str, m=None):
    W = I3
    for letter in word:
        W = mul(GEN[letter], W, m)
    return W


def phi(m: int, n: int):
    return (m * m - n * n, 2 * m * n, m * m + n * n)


# ---------------------------------------------------------------- parametrisation
def check_parametrisation() -> dict:
    """The Barning-Berggren matrices are the images of three 2x2 matrices."""
    two_by_two = {"A": ((2, -1), (1, 0)), "B": ((2, 1), (1, 0)), "C": ((1, 2), (0, 1))}
    for name, ((p, q), (s, t)) in two_by_two.items():
        for m, n in itertools.product(range(-6, 7), repeat=2):
            require(phi(p * m + q * n, s * m + t * n) == app(GEN[name], phi(m, n)),
                    f"phi(g v) = M phi(v) fails for {name}")
    require(phi(2, 1) == R, "r = phi(2, 1)")
    require(mul(inv(C), A) == ((-1, 0, 0), (0, -1, 0), (0, 0, 1)), "C^-1 A = diag(-1,-1,1)")
    require([det3(A), det3(B), det3(C)] == [1, -1, 1], "determinants")
    return {"A_from": [[2, -1], [1, 0]], "B_from": [[2, 1], [1, 0]], "C_from": [[1, 2], [0, 1]],
            "C_inverse_A": "diag(-1,-1,1)", "root": "phi(2,1)"}


# ---------------------------------------------------------------- orbits and loops
def transversal(p: int, n: int, prec: int):
    """BFS on V_{p^n}; for each vertex v a word and its matrix mod p^prec sending r to v."""
    m, P = p ** n, p ** prec
    r0 = tuple(x % m for x in R)
    T = {r0: (tuple(tuple(x % P for x in row) for row in I3), "")}
    queue = deque([r0])
    while queue:
        v = queue.popleft()
        Tv, wv = T[v]
        for letter, S in GEN.items():
            w = app(S, v, m)
            if w not in T:
                T[w] = (mul(S, Tv, P), wv + letter)
                queue.append(w)
    return T


def schreier_loops(p: int, n: int):
    """Loops at r in Gamma_{p^n}, as matrices mod p^(n+1), with the parity of letters B."""
    T = transversal(p, n, n + 1)
    m, P = p ** n, p ** (n + 1)
    loops = []
    for v, (Tv, wv) in T.items():
        for letter, S in GEN.items():
            Tw, ww = T[app(S, v, m)]
            g = mul(inv(Tw, P), mul(S, Tv, P), P)
            parity = (wv.count("B") + (letter == "B") + ww.count("B")) % 2
            loops.append((g, parity))
    return T, loops


def coords(u, p):
    """Coordinates (s, t) of u in r^perp (mod p) with u = s r + t e1."""
    s = ((u[0] + u[2]) * pow(8, -1, p)) % p
    t = (u[0] - 3 * s) % p
    require(all((s * R[i] + t * E1[i] - u[i]) % p == 0 for i in range(3)), "vector not in r^perp")
    return (s, t)


def affine(g, p: int, n: int = 1):
    """Affine action of a loop g on the fibre r + p^n u of V_{p^(n+1)} -> V_{p^n}."""
    m, P = p ** n, p ** (n + 1)
    delta = tuple(((app(g, R, P)[i] - R[i]) % P) // m for i in range(3))
    cr, ce = coords(app(g, R, p), p), coords(app(g, E1, p), p)
    return ((cr[0], ce[0]), (cr[1], ce[1])), coords(delta, p)


def compose(f, h, p):
    (L1, t1), (L2, t2) = f, h
    L = tuple(tuple(sum(L1[i][k] * L2[k][j] for k in range(2)) % p for j in range(2)) for i in range(2))
    return L, tuple((sum(L1[i][k] * t2[k] for k in range(2)) + t1[i]) % p for i in range(2))


IDENTITY = (((1, 0), (0, 1)), (0, 0))


def closure(gens, p):
    G = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        new = []
        for x in frontier:
            for s in gens:
                y = compose(s, x, p)
                if y not in G:
                    G.add(y)
                    new.append(y)
        frontier = new
    return G


def power(x, k, p):
    y = IDENTITY
    for _ in range(k):
        y = compose(x, y, p)
    return y


def fibre_points(p: int, n: int = 1):
    """Points r + p^n u (mod p^(n+1)) with u in r^perp."""
    P = p ** (n + 1)
    return [tuple((R[i] + p ** n * u[i]) % P for i in range(3))
            for u in itertools.product(range(p), repeat=3)
            if (3 * u[0] + 4 * u[1] - 5 * u[2]) % p == 0]


# ---------------------------------------------------------------- one prime
def check_prime(p: int) -> dict:
    P = p * p
    V_p = transversal(p, 1, 1)
    V_p2 = transversal(p, 2, 2)
    require(len(V_p) == (p * p - 1) // 2, f"|V_p| at p={p}")
    require(len(V_p2) == p * p * len(V_p), f"|V_p^2| at p={p}")

    # fibre: orbit points above r = tangent torsor = image of the differential of phi
    r_mod_p = tuple(x % p for x in R)
    orbit_fibre = {x for x in V_p2 if tuple(y % p for y in x) == r_mod_p}
    tangent_fibre = set(fibre_points(p))
    param_fibre = {tuple(c % P for c in phi(2 + p * w1, 1 + p * w2))
                   for w1, w2 in itertools.product(range(p), repeat=2)}
    require(orbit_fibre == tangent_fibre == param_fibre and len(orbit_fibre) == p * p,
            f"fibre description at p={p}")

    _, loops = schreier_loops(p, 1)
    gens = {}
    for g, parity in loops:
        L, t = affine(g, p)
        # affine model checked point by point
        for u in itertools.product(range(p), repeat=3):
            if (3 * u[0] + 4 * u[1] - 5 * u[2]) % p:
                continue
            x = tuple((R[i] + p * u[i]) % P for i in range(3))
            s, tt = coords(u, p)
            s2 = (L[0][0] * s + L[0][1] * tt + t[0]) % p
            t2 = (L[1][0] * s + L[1][1] * tt + t[1]) % p
            predicted = tuple((R[i] + p * (s2 * R[i] + t2 * E1[i])) % P for i in range(3))
            require(app(g, x, P) == predicted, f"affine model at p={p}")
        require(L[0][0] == 1 and L[1][0] == 0 and L[1][1] in (1, p - 1),
                f"linear part is not [[1,b],[0,eps]] at p={p}")
        require((L[1][1] == 1) == (parity == 0), f"eps != (-1)^#B at p={p}")
        require((L[1][1] == 1) == (det3(g) % P == 1), f"eps != det at p={p}")
        gens[(L, t)] = parity

    G = closure(list(gens), p)
    translations = [x for x in G if x[0] == ((1, 0), (0, 1))]
    positive = [x for x in G if x[0][1][1] == 1]
    linear = {x[0] for x in G}
    stabiliser = [x for x in G if x[1] == (0, 0)]
    centre_positive = [x for x in positive if all(compose(x, y, p) == compose(y, x, p) for y in positive)]
    require(len(G) == 2 * p ** 3, f"|Mon| at p={p}")
    require(len(translations) == p * p, f"translations at p={p}")
    require(len(positive) == p ** 3, f"eps=+1 subgroup at p={p}")
    require(len(linear) == 2 * p, f"linear image at p={p}")
    require(len(stabiliser) == 2 * p, f"point stabiliser at p={p}")
    require(any(compose(x, y, p) != compose(y, x, p) for x in positive for y in positive),
            f"eps=+1 subgroup is abelian at p={p}")
    require(all(power(x, p, p) == IDENTITY for x in positive), f"exponent at p={p}")
    require(sorted(centre_positive) == sorted((((1, 0), (0, 1)), (s, 0)) for s in range(p)),
            f"centre of the eps=+1 subgroup at p={p}")
    conic = {(x[0][1][1], x[1][1]) for x in G}
    require(len(conic) == 2 * p, f"conic monodromy at p={p}")
    return {
        "p": p,
        "V_p": len(V_p),
        "V_p2": len(V_p2),
        "fibre": len(orbit_fibre),
        "fibre_equals_tangent_torsor_and_parametrisation_image": True,
        "schreier_loops": len(loops),
        "monodromy_order": len(G),
        "translations": len(translations),
        "linear_image_order": len(linear),
        "eps_plus_subgroup_order": len(positive),
        "eps_plus_subgroup_centre_order": len(centre_positive),
        "point_stabiliser_order": len(stabiliser),
        "regular_covering": False,
        "eps_equals_det_equals_parity_of_B": True,
        "conic_fibre_monodromy_order": len(conic),
    }


# ---------------------------------------------------------------- p = 7, explicit loops
def check_p7() -> dict:
    p, P = 7, 49
    x, y = affine(word_matrix("BABC", P), p), affine(word_matrix("BABAA", P), p)
    for w in ("BABC", "BABAA", "BABAB"):
        require(app(word_matrix(w, p), R, p) == tuple(v % p for v in R), f"{w} is not a loop mod 7")
    require(x[0][1][1] == 1 and y[0][1][1] == 1, "BABC, BABAA must have eps = +1")
    H = closure([x, y], p)
    require(len(H) == 343, "<BABC, BABAA>")
    odd = []
    for length in range(1, 6):
        odd = ["".join(w) for w in itertools.product("ABC", repeat=length)
               if "".join(w).count("B") % 2 == 1
               and app(word_matrix("".join(w), p), R, p) == tuple(v % p for v in R)]
        if odd:
            break
    require(odd and len(odd[0]) == 5 and "BABAB" in odd, "shortest odd loops")
    z = affine(word_matrix("BABAB", P), p)
    require(z[0][1][1] == p - 1, "BABAB must have eps = -1")
    require(len(closure([x, y, z], p)) == 686, "<BABC, BABAA, BABAB>")
    W1, W2 = word_matrix("BABC", P), word_matrix("BABAA", P)
    commutator = mul(mul(W1, W2, P), mul(inv(W1, P), inv(W2, P), P), P)
    factors = sorted(k for k in range(P)
                     if all(app(commutator, f, P) == tuple(k * c % P for c in f) for f in fibre_points(p)))
    require(factors == [36], "commutator is not the homothety x -> 36 x")
    require((x[0][1][1], x[1][1]) == (y[0][1][1], y[1][1]), "BABC and BABAA differ on the conic")
    return {
        "loops_with_two_B": ["BABC", "BABAA"],
        "subgroup_generated": 343,
        "shortest_odd_B_loops_length": 5,
        "shortest_odd_B_loops": odd,
        "with_BABAB": 686,
        "commutator_acts_as_homothety_factor_mod_49": 36,
        "BABC_BABAA_same_permutation_of_conic_fibre": True,
    }


# ---------------------------------------------------------------- tower
def check_tower(p: int) -> dict:
    _, loops = schreier_loops(p, 2)
    gens = {affine(g, p, 2) for g, _ in loops}
    G = closure(list(gens), p)
    require(len(G) == 2 * p ** 3, f"tower step at p={p}")
    return {"p": p, "step": "Gamma_p3 -> Gamma_p2", "monodromy_order": len(G)}


def canonical_json(data) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--write-json", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    data = {
        "check": "HOL-01 finite-prime regression",
        "version": VERSION,
        "arithmetic": "exact integer/modular arithmetic; Python standard library only",
        "scope": "finite regression checks only; no universal-prime or all-level theorem claim",
        "parametrisation": check_parametrisation(),
        "primes": [check_prime(p) for p in PRIMES],
        "p7_explicit_loops": check_p7(),
        "exploratory_tower_step_checks": [check_tower(p) for p in TOWER_PRIMES],
    }
    for row in data["primes"]:
        print(f"p={row['p']:2d} |V_p|={row['V_p']:3d} fibre={row['fibre']:3d} |Mon|={row['monodromy_order']:5d} "
              f"eps=+1:{row['eps_plus_subgroup_order']:5d} stabiliser={row['point_stabiliser_order']:3d}")
    payload = canonical_json(data)
    if args.write_json:
        args.write_json.write_text(payload, encoding="utf-8")
        print(f"wrote {args.write_json}")
    if args.check:
        require(args.check.read_text(encoding="utf-8") == payload, f"snapshot mismatch: {args.check}")
        print(f"snapshot OK: {args.check}")
    print("FINITE_REGRESSION_RESULTS sha256=" + hashlib.sha256(payload.encode("utf-8")).hexdigest())
    print("HOL-01 finite-prime regression check: ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
