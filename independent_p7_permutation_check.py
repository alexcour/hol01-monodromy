#!/usr/bin/env python3
"""Independent direct-permutation cross-check for the principal p=7 HOL-01 claim.

This implementation deliberately avoids the affine-coordinate group code used in
``hol01_certificate.py``. It enumerates the 49 lifted fibre points directly,
constructs Schreier generators as permutations of those points, and closes the
resulting finite permutation groups with Python tuples only.
"""

from collections import deque

M1 = ((-1, 2, 2), (-2, 1, 2), (-2, 2, 3))
M2 = ((1, 2, 2), (2, 1, 2), (2, 2, 3))
M3 = ((1, -2, 2), (2, -1, 2), (2, -2, 3))
J = ((1, 0, 0), (0, 1, 0), (0, 0, -1))
I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
R = (3, 4, 5)


def mm0(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def mm(A, B, m):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) % m for j in range(3)) for i in range(3))


def mv(A, v, m):
    return tuple(sum(A[i][k] * v[k] for k in range(3)) % m for i in range(3))


def tr(A):
    return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))


def inv_orth0(A):
    return mm0(mm0(J, tr(A)), J)


def inv_orth(A, m):
    return mm(mm(J, tr(A), m), J, m)


def red(A, m):
    return tuple(tuple(x % m for x in row) for row in A)


GENS = (M1, M2, M3, inv_orth0(M1), inv_orth0(M2), inv_orth0(M3))


def orbit(m):
    root = tuple(x % m for x in R)
    gens = tuple(red(g, m) for g in GENS)
    seen = {root}
    queue = deque([root])
    while queue:
        v = queue.popleft()
        for g in gens:
            w = mv(g, v, m)
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return seen


def spanning_tree_lifts(p):
    """Lift one BFS path to every vertex of the mod-p orbit, modulo p^2."""
    m = p * p
    root = tuple(x % p for x in R)
    path_matrix = {root: red(I3, m)}
    queue = deque([root])
    while queue:
        v = queue.popleft()
        for s0 in GENS:
            s = red(s0, m)
            w = mv(s, v, p)
            if w not in path_matrix:
                path_matrix[w] = mm(s, path_matrix[v], m)
                queue.append(w)
    return path_matrix


def perm_comp(f, g):
    """Composition f o g."""
    return tuple(f[g[i]] for i in range(len(f)))


def perm_inv(f):
    out = [0] * len(f)
    for i, j in enumerate(f):
        out[j] = i
    return tuple(out)


def perm_closure(gens):
    gens = list(dict.fromkeys(gens))
    gens = list(dict.fromkeys(gens + [perm_inv(g) for g in gens]))
    identity = tuple(range(len(gens[0])))
    seen = {identity}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = perm_comp(g, x)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def cycle_signature(f):
    seen = set()
    out = []
    for i in range(len(f)):
        if i in seen:
            continue
        j = i
        n = 0
        while j not in seen:
            seen.add(j)
            n += 1
            j = f[j]
        out.append(n)
    return sorted(out)


def main():
    p = 7
    m = 49

    V7 = orbit(7)
    V49 = orbit(49)
    fibre = sorted(v for v in V49 if tuple(x % 7 for x in v) == R)
    index = {v: i for i, v in enumerate(fibre)}

    assert len(V7) == 24
    assert len(V49) == 1176
    assert len(fibre) == 49

    path_matrix = spanning_tree_lifts(p)
    schreier_perms = []
    for v in path_matrix:
        for s0 in GENS:
            s = red(s0, m)
            w = mv(s, v, p)
            loop = mm(mm(inv_orth(path_matrix[w], m), s, m), path_matrix[v], m)
            perm = tuple(index[mv(loop, x, m)] for x in fibre)
            schreier_perms.append(perm)

    schreier_perms = list(dict.fromkeys(schreier_perms))
    monodromy = perm_closure(schreier_perms)
    assert len(schreier_perms) == 27
    assert len(monodromy) == 686

    A, B, C = M3, M2, M1
    W1 = mm0(mm0(mm0(C, B), A), B)          # positive word BABC
    W2 = mm0(mm0(mm0(mm0(A, A), B), A), B)  # positive word BABAA

    x = tuple(index[mv(W1, v, m)] for v in fibre)
    y = tuple(index[mv(W2, v, m)] for v in fibre)
    assert cycle_signature(x) == [7] * 7
    assert cycle_signature(y) == [7] * 7
    assert perm_comp(x, y) != perm_comp(y, x)

    H = perm_closure([x, y])
    assert len(H) == 343

    z = perm_comp(perm_comp(perm_comp(x, y), perm_inv(x)), perm_inv(y))
    assert cycle_signature(z) == [7] * 7
    assert all(perm_comp(z, h) == perm_comp(h, z) for h in H)

    print("independent p=7 permutation check: ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
