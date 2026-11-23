"""Build the revised supplement: Fock Variance Ladder — Computational Verification v2.0."""
from docbuild_common import *

A = R["A_unit_step"]; B = R["B_quadrature_map"]; C = R["C_thermal_number_spread"]; D = R["D_squeezed_decoherence"]
E = R["E_anharmonic_control"]; Fm = R["F_identity_family"]; FM = Fm["fock_mappings"]; G = R["G_wigner"]; Hn = R["H_nonharmonic"]; T = R["tolerances"]

d = new_doc("Fock Variance Ladder: Computational Verification and Analysis Pipeline (v2.0)",
            "Supplementary material to the Fock Variance Ladder pedagogical note",
            "verification; convergence; Wigner function; Fock states; harmonic oscillator",
            "ML Innovations Research Lab — Fock Variance Ladder: Computational Verification (v2.0)", "FVL Computational Verification v2.0")
title_block(d, "SUPPLEMENTARY MATERIAL", ["Fock Variance Ladder", "Computational Verification and Analysis Pipeline"],
            "Mathematical audit, convergence-controlled numerics, controls and a null result",
            f"Version 2.0 — November 2026 (supersedes v1.0, February 2026) · results generated {R['meta']['run_time_local']}")
P(d, ("COMPUTATIONAL VERIFICATION, NOT EXPERIMENTAL CONFIRMATION. These computations use the same Hamiltonian formalism the results "
      "are derived from. Agreement shows that the algebra and the code are correct. It does not test nature."), bold_lead="", size=10, italic=True)

H(d, "1. Summary of results", 1)
P(d, ("Pass/fail labels are computed by fvl_verify.py against the stated tolerances; none is hard-coded. All numbers in this document "
      "are read from results/results.json, written by the same run."), align="justify")
rows = [["Check", "Computed status", "Criterion"]]
crit = {
 "A unit variance step": f"max |Δ⟨ξ²⟩ − 1| < {e(T['exact'],0)} for n = 0–10",
 "B squeezed states vs analytic (converged N)": f"|δξ, δπ − analytic| < {e(T['analytic'],0)} at converged N",
 "B withdrawn line dpi=dxi+1 on Fock states": "v1.0 claim δπ = δξ + 1 on Fock states (expected to FAIL)",
 "C thermal number spread": "|σₙ − √(n̄(n̄+1))|/σ < 1e-8 at converged N",
 "D squeezed decoherence (r* feature?)": "departure time strictly monotonic in r (no feature at r*)",
 "D RK4 vs analytic": f"|RK4 − Gaussian-channel formula| < {e(T['lindblad_vs_analytic'],0)}",
 "E anharmonic: unit step fails for lambda>0": "steps = 1 at λ = 0 only",
 "F identity family": "sympy: all forms ≡ 0 given b = a+1; ladder residuals < 1e-9",
 "G Wigner normalisation/cross-check": "∫W = 1 (±2e-3 grid), W₁(0,0) = −1/π, parity vs Laguerre < 1e-9",
 "H square well formula": "quadrature vs L²(1/12 − 1/2n²π²) < 1e-9",
 "H hydrogen <r^2> (divisor 2)": "numeric ⟨r²⟩ vs n²(5n²+1−3l(l+1))/2, rel. < 1e-6",
}
for k, v in R["summary"].items(): rows.append([k, v, crit.get(k, "")])
TABLE(d, rows, widths=[2.4, 1.5, 2.6])
FIGURE(d, "fig3_summary.png", "Figure S1. Corrected summary. (A) Unit variance step. (B) Quadrature-variance map: Fock and thermal states "
       "on δπ = δξ, squeezed vacua on δξ·δπ = ½, r* marked. (C) Thermal photon-number spread at converged N, with the N = 30 values for "
       "comparison. (D) Squeezed-vacuum decoherence (null). (E) Quartic control. (F) |(a+b)(a−b+1)| on rung pairs: zero only for m = n+1. "
       "(G–I) Exact Wigner functions in (ξ, π) with colour scale ±1/π.")

H(d, "2. Conventions", 1)
P(d, ("x₀ = √(ħ/mω), p₀ = √(ħmω); ξ = x/x₀ = (a+a†)/√2, π = p/p₀ = (a−a†)/(i√2), [ξ, π] = i; vacuum Var ξ = Var π = ½; "
      "δξ·δπ ≥ ½. W(ξ, π) = (1/π)Tr[ρ D(α) Π D†(α)], α = (ξ+iπ)/√2, ∫W dξ dπ = 1. S(r) = exp[r(a² − a†²)/2]. ħ appears explicitly "
      f"in physical-unit statements: the rung spacing is x₀² = ħ/mω (= {R['A_physical']['step_m2']:.3e} m² for ²⁵Mg⁺ at ω/2π = 2 MHz)."), align="justify")
rows = [["Quadrature convention", "Vacuum variance", "Rung step"]]
for k, v in R["A_conventions"].items():
    if isinstance(v, dict): rows.append([k, v["vac_var"], v["step"]])
TABLE(d, rows); P(d, "Invariant: rung step = 2 × vacuum variance.", size=10, italic=True)

H(d, "3. Numerical method and convergence policy", 1)
for lead, txt in [
 ("Operators. ", "a, a†, ξ, π and n are built in a truncated Fock basis of N states. Fock states are basis vectors. Coherent and squeezed "
  "vacua use their analytic Fock expansions, so no truncated matrix exponential is needed. Thermal states use the Bose–Einstein weights, "
  "without renormalisation, so missing tail weight shows up as an error instead of being hidden."),
 ("Convergence. ", f"Each quantity is evaluated at N = 30, 60, 100, 150, 200, 300, 400. The reported N is the smallest whose value agrees "
  f"with the next larger N to a relative {e(T['converge_rtol'],0)}."),
 ("Dynamics. ", "The Lindblad equation with thermal amplitude damping is integrated with fourth-order Runge–Kutta (dt = 0.5) and checked "
  "against the exact Gaussian-channel solution."),
 ("Wigner functions. ", "Exact Fock-basis (Laguerre) evaluation, cross-checked against displaced-parity evaluation in a padded basis."),
]: P(d, txt, bold_lead=lead, align="justify")
FIGURE(d, "fig9_convergence.png", "Figure S9. Left: relative error against Fock cutoff N for thermal σₙ and squeezed-vacuum δξ·δπ (dotted: 10⁻⁹). "
       "Right: Wigner function of |3⟩ along ξ = π. Exact (black), displaced parity with D(α) truncated at N = 25 as in v1.0 (red, spurious "
       "outer oscillations), and displaced parity with a padded basis (blue dots).", width=6.3)

H(d, "4. Experiment A: the unit variance step", 1)
rows = [["n", "⟨ξ²⟩ computed", "⟨π²⟩ computed", "n + ½", "step to n+1"]]
for i, rw in enumerate(A["rows"]):
    rows.append([rw["n"], f(rw["var_xi"], 12), f(rw["var_pi"], 12), rw["pred"], f(A["steps"][i], 15) if i < len(A["steps"]) else "—"])
TABLE(d, rows)
P(d, f"Maximum deviation of a step from 1: {e(A['max_dev'])}. Status: {A['status']}. This is textbook quantum mechanics and serves as a calibration of the engine.", align="justify")
FIGURE(d, "fig1_variance_ladder.png", "Figure S2. The Fock variance ladder and its non-harmonic comparisons (see paper, Fig. 1).")

H(d, "5. Experiment B: quadrature-variance map", 1)
rows = [["state", "δξ", "δπ", "δξ·δπ", "δπ − δξ"]]
for x in B["fock"]: rows.append([f"|{x['n']}⟩", f(x["dxi"]), f(x["dpi"]), f(x["product"]), f(x["dpi_minus_dxi"], 1)])
for x in B["coherent"]: rows.append([f"coherent α={x['alpha']}", f(x["dxi"]), f(x["dpi"]), f(x["product"]), "0.0"])
for x in B["thermal"]: rows.append([f"thermal n̄={x['nbar']} (N={x['N_converged']})", f(x["dxi"]), f(x["dpi"]), f(x["dxi"] * x["dpi"]), f(x["dpi_minus_dxi"], 1)])
for x in B["displaced_squeezed"]: rows.append([f"D(α={x['alpha']})S(r={x['r']})|0⟩", f(x["dxi"]), f(x["dpi"]), f(x["product"]), f(x["dpi"] - x["dxi"])])
TABLE(d, rows)
rows = [["r", "N converged", "δξ", "δπ", "δξ·δπ", "|error| vs analytic", "status", "δξ·δπ at N=30", "N=30 valid?"]]
for x in B["squeezed"]:
    rows.append([f(x["r"], 4), x["N_converged"], f(x["dxi"], 6), f(x["dpi"], 6), f(x["product"], 6), e(x["abs_err"]), x["status"], f(x["N30_product"], 4), "yes" if x["N30_valid"] else "NO"])
TABLE(d, rows, size=8)
P(d, ("Withdrawn v1.0 claim. The relation δπ = δξ + 1 for eigenstates fails: δπ − δξ = "
      f"{f(B['withdrawn_shadow_line']['max_abs_dpi_minus_dxi_fock'],1)} for every Fock state (computed status: {B['withdrawn_shadow_line']['status']}). "
      "The only exact relation of that shape is across states, ⟨π²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = "
      f"{', '.join(f(v,6) for v in B['cross_state_relation'])} for n = 0–5. It is a consequence of the unit step and places no "
      "constraint on any single state. The v1.0 squeezed-state values at r ≥ 1.0 (fixed N = 30) were truncation-limited. "
      "They are replaced by converged values."), align="justify")
FIGURE(d, "fig4_quadrature_map.png", "Figure S3. Quadrature-variance map (left) and δξ·δπ of squeezed vacuum against r for converged N and fixed N = 30 (right).")

H(d, "6. Experiment C: thermal photon-number spread", 1)
rows = [["n̄", "N", "missing tail", "⟨n⟩", "σₙ", "√(n̄(n̄+1))", "rel. err", "rel. err (N=30)", "σₙ² − (⟨ξ²⟩⟨π²⟩ − ¼)"]]
for c in C:
    rows.append([c["nbar"], c["N_converged"], e(abs(c["tail_weight_missing"])), f(c["mean_n"], 6), f(c["sigma_n"], 6), f(c["sigma_pred"], 6),
                 e(c["rel_err"]), e(c["rel_err_at_N30"]), e(c["identity_check_sigma2_eq_varxi_varpi_minus_quarter"])])
TABLE(d, rows, size=7.5)
P(d, ("Interpretation (corrected). σₙ is the standard deviation of the occupied rung (the photon number) in the Bose–Einstein mixture. It is "
      "not a spread of points in the (δξ, δπ) plane: a thermal state is a single point at δξ = δπ = √(n̄+½). The v1.0 Eq. (23) factor of 4 is "
      "removed, since Var_P(n + ½) = Var(n). The last column checks σₙ² = ⟨ξ²⟩⟨π²⟩ − ¼ (form F7)."), align="justify")
FIGURE(d, "fig5_thermal.png", "Figure S4. Thermal photon-number spread, rung occupation and the F7 identity line.")

H(d, "7. Experiment D: squeezed-vacuum decoherence (null result)", 1)
rows = [["r", "δξ₀", "time to δξ·δπ = 0.55 (1/ω)"]]
for x in D["rows"]: rows.append([f(x["r"], 4) + (" (r*)" if abs(x["r"] - D["r_star"]) < 1e-9 else ""), f(x["dxi0"]), f(x["departure_time"], 2)])
TABLE(d, rows)
P(d, (f"γ = {D['gamma']}, n̄_th = {D['nth']}. r* = {D['r_star_closed_form']} = {f(D['r_star'],6)}, δξ* = {f(D['dxi_star'],6)} = (√3−1)/2, "
      f"δπ* = {f(D['dpi_star'],6)} = (√3+1)/2. Departure times are strictly monotonic in r ({D['monotonic_decreasing_in_r']}). At r* the departure "
      f"time is {f(D['t_dep_rstar'],3)}, against {f(D['t_dep_linear_interp_neighbours'],3)} from linear interpolation between neighbours; the "
      "difference reflects the curvature of a smooth curve, not a feature. RK4 against the analytic solution: "
      + ", ".join(f"r={f(c['r'],4)}: {e(c['max_abs_err_rk4_vs_analytic'])}" for c in D["rk4_check"]) + f" ({D['rk4_status']}). "
      "Status: null, as standard theory predicts. (v1.0 used Euler integration at N = 30 and reported 17.0 at r*.)"), align="justify")
FIGURE(d, "fig6_decoherence.png", "Figure S5. Squeezed-vacuum decoherence under thermal amplitude damping; no feature at r*.")

H(d, "8. The ML Identity family: symbolic and ladder checks", 1)
rows = [["Form", "expression − RHS after b = a + 1", "≡ 0?"]]
for k, v in Fm.items():
    if isinstance(v, dict) and "holds_identically" in v: rows.append([k, v["expr_minus_rhs_after_b=a+1"], "yes" if v["holds_identically"] else "NO"])
TABLE(d, rows)
P(d, (f"Factorisation: a + a² + b − b² = {Fm['F1 factorisation']}; solutions b ∈ {{{', '.join(Fm['F1 solution set'])}}}. "
      f"Σₖ₌₀ⁿ(2k+1) = {Fm['sum of first n+1 odd numbers'].replace('k','n').replace('**2','²')}. "
      f"On the Fock rungs a = ⟨ξ²⟩ₙ, b = ⟨ξ²⟩ₘ (n, m ≤ 11), the zero set of (a+b)(a−b+1) is {FM['F1_on_rung_pairs_zero_set']}, "
      f"which contains only adjacent rungs ({FM['F1_zero_only_for_adjacent_rungs']}). Largest residual over the ladder mappings "
      f"(cumulative height (n+1)²/2; ⟨ξ²⟩⟨π²⟩ − ¼ = n(n+1); Var(ξ²)ₙ = Tₙ + ½; ⟨n|a†a·aa†|n⟩ = n(n+1); Σk = Tₙ): {e(FM['max_abs_residual'])}. "
      f"Status: {Fm['status']}."), align="justify")
FIGURE(d, "fig2_identity_family.png", "Figure S6. Geometry of the identity family (gnomon, triangular numbers, completing the square, zero set).")

H(d, "9. Controls: quartic oscillator, square well, hydrogen", 1)
rows = [["λ", "Δ⟨ξ²⟩ steps (n = 0→6)", "Δ⟨π²⟩ steps", "basis change 40→120"]]
for k, v in E.items(): rows.append([k, ", ".join(f(s, 4) for s in v["x_steps"]), ", ".join(f(s, 4) for s in v["p_steps"]), e(v["basis_change_40_to_120"])])
TABLE(d, rows, size=8)
rows = [["n", "l", "⟨r²⟩/a₀² numeric", "n²(5n²+1−3l(l+1))/2", "v1.0 text (/4)"]]
for h in Hn["hydrogen"]: rows.append([h["n"], h["l"], f(h["r2_numeric_a0^2"], 6), f(h["formula_div2"], 1), f(h["formula_div4_v1"], 1)])
TABLE(d, rows, size=8)
rows = [["n", "Var(x)/L² numeric", "1/12 − 1/(2n²π²)"]]
for s in Hn["square_well"]: rows.append([s["n"], f(s["var_x_numeric_L2"], 10), f(s["formula_1/12-1/(2n^2pi^2)"], 10)])
TABLE(d, rows, size=8)
P(d, ("The hydrogen expression is the second moment ⟨r²⟩, not a variance. For s states, Var(x) = ⟨r²⟩/3, and those values are used in "
      "the paper's Fig. 1c. The anharmonic control is reported as computed: the unit step holds only at λ = 0."), align="justify")
FIGURE(d, "fig7_controls.png", "Figure S7. Left: position (solid) and momentum (dashed) variance steps for the quartic oscillator. Right: hydrogen ⟨r²⟩, numeric against the corrected and the v1.0 formula.")

H(d, "10. Wigner functions: normalisation and corrections", 1)
rows = [["state", "∫W", "W(0,0)", "Var ξ from W", "Var ξ from ρ", "Var π from W", "Var π from ρ", "⟨ξ⟩ from W"]]
for k in ["vacuum", "fock1", "fock3", "coherent_alpha2", "squeezed_r0.8", "thermal_nbar2"]:
    g = G[k]; rows.append([k, f(g["integral"], 5), f(g["W00"], 5), f(g["var_xi_from_W"], 4), f(g["var_xi_from_rho"], 4), f(g["var_pi_from_W"], 4), f(g["var_pi_from_rho"], 4), f(g["mean_xi_from_W"], 3)])
TABLE(d, rows, size=8)
L = G["legacy_v1_formula"]
P(d, (f"v1.0 formula (2/π)Tr[D†ΠDρ] in (ξ, π) units: vacuum W(0,0) = {f(L['vacuum_W00'],4)} (should be 1/π = 0.3183), "
      f"|1⟩ W(0,0) = {f(L['fock1_W00'],4)} (should be −1/π). For a coherent state with ⟨ξ⟩ = +2.83 it returns {f(L['coherent_alpha2_at_xi=+2.83'],4)} "
      f"at ξ = +2.83 and {f(L['coherent_alpha2_at_xi=-2.83'],4)} at ξ = −2.83, i.e. a mirror image with doubled amplitude. "
      f"Displaced parity inside the 25-state basis gives W = {f(G['fock3_corner_4_4']['parity_N25_unpadded'],4)} for |3⟩ at ξ = π = 4 "
      f"(exact {e(G['fock3_corner_4_4']['laguerre_exact'])}); this is the source of the v1.0 outer rings. "
      f"Corrected method against padded displaced parity: {e(G['parity_vs_laguerre_max_diff_pad60'])}. Status: {G['status']}."), align="justify")
FIGURE(d, "fig8_wigner.png", "Figure S8. Corrected Wigner gallery in (ξ, π), normalised to 1, colour scale ±1/π.")

H(d, "11. Changes from v1.0", 1)
for lead, txt in [
 ("Renamed: ", "“Shadow Tomography” is now “Fock Variance Ladder”. The term “shadow tomography” belongs to Aaronson (2018) and the classical-shadows literature."),
 ("Withdrawn: ", "the “shadow line” δπ = δξ + 1 (Sec. 5) and the claim that the identity is unique (it belongs to a three-parameter family)."),
 ("Reinterpreted: ", "the “corridor width” is now the thermal photon-number spread. The “fixed point” is presented as a squeezed vacuum at r*, with a null decoherence result."),
 ("Fixed numerics: ", "hard-coded CONFIRMED labels replaced by computed pass/fail; fixed N = 30 replaced by a convergence policy; Wigner prefactor (2/π → 1/π in (ξ, π)), operator order (D†ΠD → DΠD†) and truncation artefact corrected; Euler replaced by RK4 with an analytic check."),
 ("Fixed formulas: ", "hydrogen ⟨r²⟩ divisor (4 → 2) and Eq. (23) factor (4 → 1)."),
 ("Housekeeping: ", "contact e-mail corrected; document metadata author set; AI-assistance acknowledgement added; textbook citations added; regen_figures.py supplied (v1.0 cited regen_plots.py, which was not included)."),
]: BUL(d, txt, lead)

H(d, "12. Status of each result", 1)
TABLE(d, [["Result", "Status", "Needs ML Identity?", "Needs experiment?"],
          ["Unit variance step = 1", "Textbook (ladder operators)", "No", "No (calibration only)"],
          ["Quadrature-variance map", "Textbook loci; v1.0 line withdrawn", "No", "No"],
          ["Thermal photon-number spread", "Textbook (Bose–Einstein)", "No", "No"],
          ["Squeezed decoherence at r*", "Null, as predicted by Gaussian channel", "No", "Optional"],
          ["ML Identity family", "Elementary algebra (classical)", "—", "No"],
          ["Ladder mappings (F1–F10)", "Exact; pedagogical", "—", "No"],
          ["Anharmonic control", "Unit step fails for λ > 0, as expected", "No", "Optional"]], widths=[2.0, 2.4, 1.1, 1.3])
P(d, ("The contribution of the package is pedagogical: it organises textbook facts around the variance ladder and the consecutive-integer "
      "identities. It does not claim new physics."), align="justify")

H(d, "13. Reproducibility", 1)
P(d, ("python fvl_verify.py  →  results/results.json (about 20 s). python regen_figures.py  →  figures/*.png (about 20 s). "
      "python build_paper.py, build_supplement.py and build_protocol.py  →  docs/*.docx. Requires Python 3 with NumPy, SciPy, SymPy, "
      f"Matplotlib and python-docx (run used NumPy {R['meta']['numpy']}). There are no random elements."), align="justify")
P(d, AI_ACK, italic=True, size=10)
H(d, "References", 2)
for i, r_ in enumerate([
 "M. L. McKnight, “The Fock Variance Ladder: Unit Variance Steps of the Quantum Harmonic Oscillator and the ML Identity Family — a pedagogical note,” v2.0, ML Innovations Research Lab (2026).",
 "M. L. McKnight, “Fock Variance Ladder: Experimental Protocol,” v2.0, ML Innovations Research Lab (2026).",
 "C. C. Gerry and P. L. Knight, Introductory Quantum Optics (Cambridge University Press, 2005).",
 "D. F. Walls and G. J. Milburn, Quantum Optics, 2nd ed. (Springer, 2008).",
 "M. Hillery, R. F. O'Connell, M. O. Scully and E. P. Wigner, Phys. Rep. 106, 121 (1984).",
 "A. Royer, Phys. Rev. A 15, 449 (1977).",
 "H. A. Bethe and E. E. Salpeter, Quantum Mechanics of One- and Two-Electron Atoms (Springer, 1957).",
 "F. Mandl, Statistical Physics, 2nd ed. (Wiley, 1988).",
 "S. Aaronson, Proc. 50th ACM STOC (2018), 325–338; H.-Y. Huang, R. Kueng and J. Preskill, Nat. Phys. 16, 1050 (2020)."], 1):
    P(d, r_, bold_lead=f"[{i}] ", size=9.5)
P(d, "— END OF DOCUMENT —", align="center", size=9)
out = os.path.join(ROOT, "docs", "Fock_Variance_Ladder_Computational_Verification_v2.docx"); d.save(out); print("saved", out)
