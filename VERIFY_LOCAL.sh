#!/usr/bin/env sh
set -eu
python3 hol01_certificate.py --check RESULTS.json
python3 independent_p7_permutation_check.py
python3 finite_prime_regression_check.py --check FINITE_REGRESSION_RESULTS.json
