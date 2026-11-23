#!/usr/bin/env python3
"""Assert the computed summary verdicts in results/results.json.

Pass/fail labels are produced by fvl_verify.py, not hard-coded into the
paper. One expected verdict is FAIL: the withdrawn v1 claim
δπ = δξ + 1 does not hold on Fock states. The squeezed-vacuum check is a
null result (no special feature at r*).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "results", "results.json")

# Expected statuses after a successful run of fvl_verify.py.
# Do not treat "all PASS" as the criterion; the withdrawn line must FAIL.
EXPECTED = {
    "A unit variance step": "PASS",
    "B squeezed states vs analytic (converged N)": "PASS",
    "B withdrawn line dpi=dxi+1 on Fock states": "FAIL",
    "C thermal number spread": "PASS",
    "D squeezed decoherence (r* feature?)": "NULL (no feature at r*)",
    "D RK4 vs analytic": "PASS",
    "E anharmonic: unit step fails for lambda>0": "PASS",
    "F identity family": "PASS",
    "G Wigner normalisation/cross-check": "PASS",
    "H square well formula": "PASS",
    "H hydrogen <r^2> (divisor 2)": "PASS",
}


def main():
    if not os.path.isfile(PATH):
        print(f"missing results file: {PATH}", file=sys.stderr)
        return 1
    with open(PATH) as fh:
        data = json.load(fh)
    summary = data.get("summary")
    if not isinstance(summary, dict):
        print("results.json has no summary object", file=sys.stderr)
        return 1
    failed = 0
    for key, expected in EXPECTED.items():
        got = summary.get(key)
        ok = got == expected
        mark = "ok" if ok else "MISMATCH"
        print(f"{mark:9s}  {key}: {got!r}" + ("" if ok else f"  (expected {expected!r})"))
        if not ok:
            failed += 1
    unexpected = [k for k in summary if k not in EXPECTED]
    if unexpected:
        print("unexpected summary keys:", unexpected)
        failed += 1
    if failed:
        print(f"{failed} check(s) failed", file=sys.stderr)
        return 1
    print("all expected verdicts matched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
