# CHANGELOG — Fock Variance Ladder package v2.0 (2026-11-23)

Supersedes the February 2026 v1.0 package ("Shadow of the Unknown" paper, "Shadow Tomography" protocol and
computational-verification supplement, `shadow_tomography_sim.py`). The originals are unchanged; this package
is a set of new files. Every number in the documents is read from `results/results.json`, which `code/fvl_verify.py` writes.
To regenerate everything: `code/run_all.sh` (about 45 s).

## Renaming
- Paper, protocol, supplement, code and figures are renamed to **Fock Variance Ladder**. "Shadow tomography"
  (Aaronson 2018; classical shadows, Huang–Kueng–Preskill 2020) is an established, unrelated term with 169 exact-phrase
  arXiv hits. "Fock variance ladder" had 0 (check in `../name_search_arxiv.txt`).
- "Shadow law", "shadow line", "shadow constraint", "corridor", "fixed point" and "Stopped-State" are replaced or withdrawn (see below).
- Paper title: *The Fock Variance Ladder: Unit Variance Steps of the Quantum Harmonic Oscillator and the ML Identity Family — a pedagogical note*.

## Physics corrections
- **Shadow line δπ = δξ + 1 withdrawn.** It fails for every Fock state, where δπ − δξ = 0 (the code computes FAIL).
  The +1 is the step between rungs: ⟨ξ²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = 1 and ⟨π²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = 1.
- **Corridor reinterpreted** as the thermal photon-number spread σₙ = √(n̄(n̄+1)). A thermal state is a single point on the diagonal.
  New exact link: σₙ² = ⟨ξ²⟩⟨π²⟩ − ¼ (form F7).
- **Eq. 23 factor fixed:** Var_P(n + ½) = Var(n), so the factor is 1, not 4.
- **Fixed point recast** as the squeezed vacuum at r* = ln((√6+√2)/2) = 0.6585 (δξ* = (√3−1)/2). Gaussian-channel
  decoherence has no feature there. Departure times are monotonic in r: a null result, reported as such.
- **Uniqueness claim removed.** Every degree-≤2 identity on b = a + 1 is (b − a − 1)(c₀ + c₁a + c₂b).
  F1's zero set is b ∈ {a+1, −a}, from the factorisation (a+b)(a−b+1) = 0.
- **ħ and normalisation stated:** ξ = (a+a†)/√2, [ξ,π] = i, vacuum variance ½. In physical units the step is x₀² = ħ/mω
  (2.02×10⁻¹⁶ m² for ²⁵Mg⁺ at 2 MHz). Step = 2 × vacuum variance in any convention.
- **Hydrogen:** ⟨r²⟩ = (n²a₀²/2)[5n²+1−3l(l+1)]; the divisor is 2, not 4. It is a second moment, not a variance.
  For s states Var(x) = ⟨r²⟩/3.

## Added: ML Identity family (paper Sec. 4; verified with sympy and on the Fock rungs)
| Form | Statement (b = a + 1) |
|---|---|
| F1 | a + a² + b = b² |
| F2 | b² − a² = a + b (consecutive-squares gap equals their sum) |
| F3 | ab = a² + a |
| F4 | (b − a)² = 1 |
| F5 | a² + b² = 2ab + 1 |
| F6 | b² = a² + (2a + 1) (gnomon; Σ odd numbers = (n+1)²) |
| F7 | ab = (a + ½)² − ¼, i.e. n(n+1) = (n+½)² − ¼ |
| F8 | Tₐ + T_b = b² (adjacent triangular numbers) |
| F9 | 8Tₐ + 1 = (a + b)² |
| F10 | T_b − Tₐ = b |
| — | Factorisation a + a² + b − b² = (a+b)(a−b+1) |

Ladder readings:
- F1 holds on the Fock rungs only for adjacent rungs.
- Σₖ⟨ξ²⟩ₖ = (n+1)²/2.
- ⟨ξ²⟩⟨π²⟩ − ¼ = n(n+1).
- Var(ξ²) in |n⟩ = Tₙ + ½.
- Langer substitution l(l+1) → (l+½)².

Classical sources credited: Nicomachus and Fibonacci's *Liber Quadratorum* (1225).

## Code fixes (v1.0 → v2.0)
- **Pass/fail:** hard-coded "CONFIRMED" labels are replaced by computed pass/fail with stated tolerances.
  - v1.0 printed CONFIRMED for a 31% thermal error at N = 30.
- **Converged Fock cutoff:** the fixed N = 30 is replaced by the smallest N in {30…400} that agrees with the next N to 1e-9 relative.
  - v1.0 squeezed products at r = 1.0/1.2/1.5 were 0.5019/0.532/0.843 instead of 0.5.
  - N = 30 is now marked invalid there.
- **Thermal states** are no longer renormalised, so a missing tail shows up as an error.
- **Wigner function:**
  - Prefactor: 2/π → 1/π in (ξ,π) units. The v1.0 vacuum integrated to 2.
  - Operator order: D†ΠD → DΠD†. v1.0 mirrored displaced states.
  - Exact Laguerre formula, cross-checked with padded displaced parity to 1.7e-16.
  - The |3⟩ outer-ring artefact came from a 25-state D(α); v1.0 gave −0.117 at (4,4), exact ~1e-10.
- **Dynamics:** Euler is replaced by RK4, checked against the analytic Gaussian-channel solution (< 1e-6).
- **Reproducibility:**
  - Added `regen_figures.py`; v1.0 cited a missing `regen_plots.py`.
  - Removed the hard-coded `/home/claude` path.

## New and corrected figures (`figures/`)
- fig1 variance ladder (levels + Wigner, steps vs square well / hydrogen / quartic)
- fig2 identity-family geometry (gnomon, triangular numbers, completing the square, zero set)
- fig3 corrected 9-panel summary
- fig4 quadrature-variance map + N = 30 vs converged
- fig5 thermal number spread
- fig6 squeezed-vacuum decoherence (null)
- fig7 controls (quartic x/p steps; hydrogen /2 vs /4)
- fig8 corrected Wigner gallery (±1/π)
- fig9 convergence + |3⟩ artefact

## Protocol fixes
- **Temperatures at ω/2π = 2 MHz** (ħω/k_B = 96.0 μK):
  - n̄ = 0.05 → 31.5 μK (was ~0.7 mK).
  - n̄ = 10 → 1.01 mK (was ~30 mK).
  - All rows recomputed.
- **Wait times at 5 phonons/s:** 10, 20, 100, 200, 400, 1000, 2000 ms (were 95/190/380/950 ms with no n̄ = 0.1 value).
- **Squeezed table:**
  - δπ(r=1.0) = 1.922 (was 1.924) and δπ(r=1.5) = 3.169 (was 3.167).
  - The last column is now δξ·δπ.
- **Calibration 3:** W₁(0,0) = −1/π in (ξ,π) units (−2/π per d²α); fidelity F = (1 − πW(0,0))/2 (was "−0.637·F").
- **Calibration 2:** vacuum peak 1/π stated.
- **Calibration 4:** delays extended to 0–2000 ms; v1.0's 0–1000 μs would add only ~0.005 phonon.
- **Step 2:** alternating blue/red sideband π pulses (Meekhof 1996) instead of "repumping".
- **Step 3:** D(α)ΠD†(α) with the (ξ,π) normalisation.
- **Zero-point extent:** x₀ = 14.2 nm and rms 10.1 nm (was "~7 nm").
- **Experiment D:** hold times 0.5–50 ms (heating alone takes an estimated 10.0 ms at r = 0, 5.2 ms at r* and 1.9 ms at r = 1.2 to reach δξ·δπ = 0.55; was 10–500 μs).
  Also randomised/blind ordering.
- **Predictions 2–4 and scenarios** rewritten as textbook checks plus a null test.
- **References:**
  - Unused stopped-light refs [3]–[5] (Hau ×2, Heinze) removed and the list renumbered.
  - Added Meekhof 1996, Leibfried RMP 2003, Lutterbach–Davidovich 1997, Gerry & Knight, and the supplement.
  - [10] flagged as missing authors.

## Document housekeeping
- Removed "Classification: UNCLASSIFIED // ML INNOVATIONS PROPRIETARY".
- Metadata author set to M. L. McKnight (was "Un-named"); titles, subjects and keywords set; category physics.ed-ph.
- Affiliation: ML Innovations Research Lab (ML Innovations LLC), Pheba, MS.
  - E-mail corrected to ml.innovation.research.lab@gmail.com.
  - The public repository lists the email and affiliation only; the telephone number is omitted.
- Consistent citations of the companion documents; textbook citations added.
- Acknowledgement added: "AI tools assisted with code and drafting. The author reviewed all text, code and results and takes full responsibility for the content."
- Framed as a pedagogical note suitable for arXiv physics.ed-ph. The honest null result and the controls are kept.

## Unresolved (needs the author)
- Heating "~1 phonon per 190 ms (Schmidt-Kaler et al., 2003)" and "99.9% ground state in ⁴⁰Ca⁺ (2003)" do not match the reference list (2000) and could not be verified.
  - The heating claim was rewritten around the stated 5 phonons/s target.
  - The 99.9% claim is flagged "to be verified" in the text.
- Ref. [10] (PRX Quantum 6, 2025, joint-parity tomography) has no authors in the original; authors still need to be added.
- The list of labs with demonstrated capability is unverified, and those labs were not contacted.
- Name availability was checked on arXiv and the web, but not directly on Google Scholar.
