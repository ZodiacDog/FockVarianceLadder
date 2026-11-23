# Fock Variance Ladder — code (v2.0)

Author: M. L. McKnight, ML Innovations Research Lab (ML Innovations LLC), Pheba, MS.
Contact: ml.innovation.research.lab@gmail.com
AI tools assisted with code and drafting. The author reviewed all text, code and results and takes full responsibility for the content.

The code in this directory is licensed under the MIT License (`LICENSE` at the repository root). The paper, figures, and other text are licensed separately under CC BY 4.0 (`LICENSE-CC-BY-4.0`).

| File | Purpose |
|---|---|
| `fvl_core.py` | Oscillator in a truncated Fock basis; analytic coherent/squeezed kets; thermal states (not renormalised); exact Laguerre Wigner function; displaced-parity Wigner (padded basis); `converged_N`; RK4 Lindblad integrator |
| `fvl_verify.py` | Runs Experiments A–I and writes `../results/results.json`. Pass/fail is computed against tolerances (exact 1e-12, convergence 1e-9 relative, analytic 1e-8, Lindblad-vs-analytic 1e-6). |
| `check_results.py` | Asserts the computed summary verdicts, including the expected FAIL of the withdrawn δπ = δξ + 1 claim and the null result at r*. |
| `regen_figures.py` | Writes `../figures/fig1…fig9*.png` from the same engine |
| `docbuild_common.py` | Shared python-docx helpers and author/contact constants |
| `build_paper.py`, `build_supplement.py`, `build_protocol.py` | Build the three `.docx` files in `../docs/`; every number is read from `results.json` |
| `run_all.sh` | Runs verification, figures, and document builds, then converts to PDF with LibreOffice if present. The protocol rebuild is skipped unless the v1.0 source docx is available locally (it is not part of this repository). |

Conventions: ξ = (a+a†)/√2, π = (a−a†)/(i√2), [ξ,π] = i, vacuum variance ½, x₀ = √(ħ/mω).
W(ξ,π) = (1/π)Tr[ρ D(α) Π D†(α)], α = (ξ+iπ)/√2, ∫W dξ dπ = 1.

Requirements: Python 3.10+, numpy, scipy, sympy, matplotlib. python-docx is needed only to rebuild the Word documents. No random elements.
