# Provenance and claim history

This file documents the claim history of HOL-01. It complements \`HOL01_STATUS.md\`, \`CHANGELOG.md\` and \`PRIOR_ART.md\`.

## Public authority

The authoritative public release is v1.1.1. Its scope is the exact finite \(p=7\) certificate plus explicitly labelled finite regression/exploratory checks.

The public release does **not** claim a theorem for every odd prime or every congruence level.

## Claim-history summary

1. A broader uniform formulation was considered internally.
2. Review found that the written public proof did not justify that formulation at release time.
3. v1.1.1 therefore froze the public claim at the finite \(p=7\) certificate and relabelled other computations as finite evidence.
4. A later internal derivation, now called HOL-01U, explains the broad pattern through standard modular/congruence and Schreier-graph structure.
5. That later explanation does not retroactively change the public scope of v1.1.1 and is not used here as a novelty claim.

## Attribution

Classical sources are credited in \`PRIOR_ART.md\` and \`HOL01_NOTE.pdf\`. The exact finite scripts, snapshots, release engineering and witness selection are repository artefacts; this does not imply priority for the underlying mathematics.

AI systems were used in parts of the surrounding research workflow for drafting, checking, red-teaming, code assistance and literature orientation. They are not authors. Public scientific responsibility remains with the named human author. See \`AI_ASSISTANCE.md\` for the explicit disclosure boundary.

## Principle

A later synthesis must not silently overwrite an earlier frozen claim boundary. The source hierarchy is:

1. public release/status file for public claims;
2. exact executable artefact for computational facts;
3. dated corrections/changelog;
4. later internal synthesis.

This repository intentionally preserves the narrowing event rather than rewriting history as if the uniform theory had always been the public claim.
