"""Build the revised paper: Fock Variance Ladder (pedagogical note), v2.0."""
from docbuild_common import *

A = R["A_unit_step"]; Aph = R["A_physical"]; B = R["B_quadrature_map"]; C = R["C_thermal_number_spread"]
D = R["D_squeezed_decoherence"]; E = R["E_anharmonic_control"]; Fm = R["F_identity_family"]; FM = Fm["fock_mappings"]
G = R["G_wigner"]; Hn = R["H_nonharmonic"]
Cn = {c["nbar"]: c for c in C}
sq = {s["r"]: s for s in B["squeezed"]}

TITLE = "The Fock Variance Ladder"
SUB = "Unit Variance Steps of the Quantum Harmonic Oscillator and the ML Identity Family — a pedagogical note"
d = new_doc(f"{TITLE}: {SUB}", "Pedagogical note on harmonic-oscillator eigenstate variances (arXiv physics.ed-ph)",
            "harmonic oscillator; Fock states; quadrature variance; consecutive squares; gnomon; triangular numbers; Wigner function",
            "ML Innovations Research Lab — The Fock Variance Ladder (v2.0)", "Fock Variance Ladder v2.0")
title_block(d, "PEDAGOGICAL NOTE  ·  suggested arXiv category: physics.ed-ph (cross-list quant-ph)",
            ["The Fock Variance Ladder"], SUB,
            "Version 2.0 — November 2026 (revises the February 2026 draft titled “Shadow of the Unknown”)")

H(d, "Abstract", 1)
P(d, ("In the energy eigenstates |n⟩ of the quantum harmonic oscillator, the dimensionless position and momentum variances are "
      "⟨ξ²⟩ₙ = ⟨π²⟩ₙ = n + ½. Successive eigenstates therefore form a ladder of equally spaced rungs, with spacing exactly 1 "
      "in oscillator units (ħ/mω in physical units). We call this the Fock variance ladder and use it as a compact teaching example. "
      "We show that the elementary identity a + a² + b = b² with b = a + 1 (the “ML Identity”, rediscovered by the author in 1999) "
      "belongs to a classical family of consecutive-integer identities: the gnomon (n+1)² = n² + (2n+1), the difference-of-squares "
      "form b² − a² = a + b, the product form ab = a² + a, completing the square n(n+1) = (n+½)² − ¼ and the triangular-number forms. "
      "We prove each one and show where it appears on the ladder. "
      "For example, n(n+1) is the excess of the uncertainty product ⟨ξ²⟩⟨π²⟩ over the Heisenberg value ¼, and, for thermal states, "
      "it is the photon-number variance n̄(n̄+1). Every number in the note comes from a deposited, convergence-checked computation. "
      "We report our negative control (a quartic oscillator, whose rungs become unequal) and a null result (a squeezed vacuum singled out "
      "algebraically decoheres exactly like its neighbours). An earlier draft claimed a conjugate-variable constraint δπ = δξ + 1; "
      "we withdraw that claim here and explain why it fails."), align="justify")

H(d, "1. Introduction", 1)
P(d, ("The Heisenberg–Kennard–Robertson relation Δx·Δp ≥ ħ/2 [1–3] sets a floor under conjugate uncertainties. For the harmonic oscillator "
      "the energy eigenstates sit at definite heights above that floor, and their variances grow in equal steps. This is textbook material "
      "[4–7], but it is rarely drawn as a ladder. Drawing it that way shows how a family of elementary integer identities maps onto "
      "oscillator algebra. This note collects those observations, proves them and checks them numerically. Its aim is teaching, not new physics."), align="justify")
P(d, ("A note on names. An earlier draft of this work was titled “Shadow of the Unknown”, and its companion documents used the phrase "
      "“shadow tomography”. That phrase already names an established, unrelated quantum-information task (Aaronson [8]) and the "
      "classical-shadows method of Huang, Kueng and Preskill [9]. We have therefore renamed the work. The earlier draft's "
      "“shadow line” δπ = δξ + 1 is withdrawn (Sec. 5), and its “corridor” is reinterpreted as the thermal photon-number spread (Sec. 6)."), align="justify")

H(d, "2. Conventions and units", 1)
P(d, "We keep ħ explicit. The oscillator Hamiltonian and its natural scales are")
EQ(d, "H = p²/2m + mω²x²/2,    x₀ = √(ħ/mω),    p₀ = √(ħmω) = ħ/x₀", 1)
P(d, "Dimensionless quadratures and ladder operators are defined by")
EQ(d, "ξ = x/x₀ = (a + a†)/√2,    π = p/p₀ = (a − a†)/(i√2),    [ξ, π] = i,    [a, a†] = 1", 2)
P(d, ("so that H = ħω(ξ² + π²)/2 = ħω(a†a + ½), and the uncertainty relation reads δξ·δπ ≥ ½, where δξ ≡ √Var(ξ). "
      "Wigner functions are normalised in the (ξ, π) plane: W(ξ, π) = (1/π) Tr[ρ D(α) Π D†(α)], with α = (ξ + iπ)/√2 and Π = (−1)^{a†a}. "
      "Equivalently, W(α) = (2/π) Tr[…] per unit d²α [10–12]. The squeeze operator is S(r) = exp[r(a² − a†²)/2], giving "
      "Var ξ = e^{−2r}/2 and Var π = e^{2r}/2."), align="justify")
P(d, ("The size of the step depends on convention. With ξ = (a+a†)/√2 the vacuum variance is ½ and the step is 1. With X = (a+a†)/2 they are "
      "¼ and ½; with X = a + a† they are 1 and 2. What is invariant is that the step equals twice the vacuum variance. In physical units "
      "the step is x₀² = ħ/mω."), align="justify")

H(d, "3. The Fock variance ladder", 1)
P(d, "Using ξ² = (a² + a†² + 2a†a + 1)/2 and ⟨n|a²|n⟩ = ⟨n|a†²|n⟩ = 0:")
EQ(d, "⟨ξ²⟩ₙ = ⟨π²⟩ₙ = n + ½ = Eₙ/ħω,    ⟨ξ⟩ₙ = ⟨π⟩ₙ = 0", 3)
EQ(d, "⟨ξ²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = 1    (physical units: Var(x)ₙ₊₁ − Var(x)ₙ = ħ/mω)", 4)
P(d, ("The rungs sit at ½, 3/2, 5/2, …. The ½ (the zero-point offset) comes from the commutator [a, a†] = 1. The unit spacing comes "
      "from the integer spectrum of a†a. Both are dimensionless; the quantum of action ħ enters only through x₀. "
      f"Numerically, the ten steps from n = 0 to 10 equal 1 to within {e(A['max_dev'])} (tolerance {e(A['tol'],0)}). "
      f"For a ²⁵Mg⁺ ion at ω/2π = 2 MHz, x₀ = {Aph['x0_m']*1e9:.1f} nm, so each rung adds {Aph['step_m2']:.3e} m² to Var(x) "
      f"(zero-point r.m.s. extent x₀/√2 = {Aph['zero_point_rms_m']*1e9:.1f} nm)."), align="justify")
P(d, ("Equal rungs are special to the quadratic potential (Fig. 1c). In the infinite square well, Var(x)ₙ = L²[1/12 − 1/(2n²π²)] "
      "(checked by quadrature), and the steps shrink. For hydrogen, the second moment is "
      "⟨r²⟩ₙₗ = (n²a₀²/2)[5n² + 1 − 3l(l+1)] [13]. This corrects a divisor of 4 in the earlier draft and was checked numerically for n ≤ 5, l ≤ 2. "
      "For s states, Var(x) = ⟨r²⟩/3, so the steps grow roughly as n³. Adding a quartic term λξ⁴ makes the rungs unequal at once: for "
      f"λ = 0.1 the position steps fall from {f(E['0.1']['x_steps'][0],3)} to {f(E['0.1']['x_steps'][-1],3)}, while the momentum steps rise from "
      f"{f(E['0.1']['p_steps'][0],3)} to {f(E['0.1']['p_steps'][-1],3)} (Sec. 8)."), align="justify")
FIGURE(d, "fig1_variance_ladder.png", "Figure 1. (a) Oscillator levels Eₙ/ħω = n + ½ with |ψₙ(ξ)|². (b) The Fock variance ladder: "
       "⟨ξ²⟩ₙ = ⟨π²⟩ₙ = n + ½, so adjacent rungs differ by exactly 1. (c) Variance steps normalised to the first step for the harmonic "
       "oscillator, a quartic (Duffing) oscillator (λ = 0.1), the infinite square well and hydrogen s states. Only the harmonic case is flat. "
       "All data from fvl_verify.py.")

H(d, "4. The ML Identity family", 1)
P(d, ("The author noticed the identity below in 1999, as a high-school student [14]. It is a special case of results known since antiquity: "
      "the Pythagorean gnomon and the sums of odd numbers (Nicomachus [15]), and Fibonacci's systematic treatment of consecutive squares in "
      "the Liber Quadratorum (1225) [16]. We keep the name “ML Identity” for the author's form (F1) and credit the classical sources for "
      "the family."), align="justify")
P(d, ("The earlier draft also claimed F1 is the unique degree-2 identity linking a and b = a + 1. That claim is withdrawn. "
      "By the factor theorem, a polynomial P(a, b) vanishes on the whole line b = a + 1 exactly when (b − a − 1) divides it. "
      "So every identity of degree at most 2 on that line has the form (b − a − 1)(c₀ + c₁a + c₂b) = 0, a three-parameter family. "
      "F1 is the member with c₀ = 0 and c₁ = c₂ = −1, since a + a² + b − b² = −(b − a − 1)(a + b). F3 is the member with c₁ = 1."), align="justify")
H(d, "4.1 Statements and proofs (b = a + 1 throughout; Tₖ = k(k+1)/2)", 2)
forms = [
 ("F1", "a + a² + b = b²", "b² = a² + 2a + 1 = a² + a + (a + 1) = a² + a + b."),
 ("F2", "b² − a² = a + b", "b² − a² = (b − a)(b + a) = 1·(a + b). F2 is F1 rearranged: the gap between consecutive squares equals their sum."),
 ("F3", "ab = a² + a", "ab = a(a + 1) = a² + a."),
 ("F4", "(b − a)² = 1", "Immediate from b − a = 1."),
 ("F5", "a² + b² = 2ab + 1", "a² + b² − 2ab = (b − a)² = 1, by F4."),
 ("F6", "(n+1)² = n² + (2n + 1)  [gnomon]", "Expand (n+1)². Adding the L-shaped border of n + (n+1) unit squares turns an n×n square into an (n+1)×(n+1) square; "
        "summing over n gives 1 + 3 + 5 + … + (2n+1) = (n+1)²."),
 ("F7", "n(n+1) = (n + ½)² − ¼", "(n + ½)² = n² + n + ¼. Geometrically, move a ½-wide strip of the n×(n+1) rectangle to complete a square with one ¼ corner missing."),
 ("F8", "Tₙ + Tₙ₊₁ = (n+1)²", "[n(n+1) + (n+1)(n+2)]/2 = (n+1)(2n+2)/2 = (n+1)²."),
 ("F9", "8Tₙ + 1 = (2n+1)² = (a + b)²", "4n(n+1) + 1 = 4n² + 4n + 1 = (2n+1)², and 2n + 1 = a + b."),
 ("F10", "Tₙ₊₁ − Tₙ = n + 1 = b", "(n+1)(n+2)/2 − n(n+1)/2 = (n+1)(2)/2."),
]
TABLE(d, [["Form", "Statement", "Proof"]] + [[a_, b_, c_] for a_, b_, c_ in forms], widths=[0.5, 2.0, 4.0])
P(d, ("General factorisation. Without imposing b = a + 1, F1 reads a + a² + b − b² = (a + b)(a − b + 1) = 0. Its solution set is "
      f"b ∈ {{{', '.join(Fm['F1 solution set'])}}}: the ML Identity branch b = a + 1, plus a second branch b = −a that the original "
      "statement does not mention (Fig. 2d). "
      "All ten forms were also checked symbolically: after substituting b = a + 1 each reduces to 0 (fvl_verify.py, sympy)."), align="justify")
H(d, "4.2 Where each form appears on the ladder", 2)
mp = [
 ("F1/F2 on rungs", "Set a = ⟨ξ²⟩ₙ and b = ⟨ξ²⟩ₘ. Over all pairs n, m ≤ 11, (a+b)(a−b+1) vanishes only for m = n + 1, because the branch b = −a is "
  "impossible for positive variances. The identity holds exactly for adjacent rungs and nowhere else.", "zero set = {(n, n+1)}"),
 ("F6 gnomon", "2⟨ξ²⟩ₙ = 2n + 1 is the n-th odd number, so the cumulative ladder height is Σₖ₌₀ⁿ ⟨ξ²⟩ₖ = (n+1)²/2.", "checked n ≤ 9"),
 ("F7 / F3", "⟨ξ²⟩ₙ⟨π²⟩ₙ − ¼ = (n+½)² − ¼ = n(n+1). This is how far |n⟩ sits above the Heisenberg floor. Also ⟨n|a†a·aa†|n⟩ = n(n+1). "
  "The same algebra gives Langer's replacement l(l+1) → (l+½)² in the WKB treatment of angular momentum [17].", "checked n ≤ 9"),
 ("F7 thermal", "For a thermal state, Var(n) = n̄(n̄+1) = (n̄+½)² − ¼ = ⟨ξ²⟩⟨π²⟩ − ¼ (Sec. 6).", "checked n̄ = 0.01–10"),
 ("F8/F10 triangular", "Var(ξ²) in |n⟩ equals (n² + n + 1)/2 = Tₙ + ½. The total excitation Σₖ₌₀ⁿ k of the first n+1 rungs equals Tₙ.", "checked n ≤ 9"),
]
TABLE(d, [["Form", "Ladder reading", "Numerical check"]] + [list(x) for x in mp], widths=[1.1, 4.4, 1.0])
P(d, f"Largest residual over all ladder checks: {e(FM['max_abs_residual'])} (fvl_verify.py, section F).", size=10, italic=True)
FIGURE(d, "fig2_identity_family.png", "Figure 2. Geometry of the identity family. (a) Gnomon: (n+1)² = n² + n + (n+1). (b) Two consecutive "
       "triangular numbers tile a square, Tₙ + Tₙ₊₁ = (n+1)². (c) Completing the square: n(n+1) = (n+½)² − ¼. (d) The zero set of "
       "a + a² + b − b² = (a+b)(a−b+1): the lines b = a + 1 and b = −a. Adjacent Fock rungs (⟨ξ²⟩ₙ, ⟨ξ²⟩ₙ₊₁) lie on the first.")

H(d, "5. What the +1 is, and what it is not", 1)
P(d, ("The +1 of the ladder is a step between two different states: ⟨ξ²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = 1. It is not an offset between the two "
      "quadratures of one state. The earlier draft proposed the conjugate constraint δπ = δξ + 1 (“shadow line”) and asserted that it "
      "holds exactly for eigenstates. That contradicts Eq. (3): every Fock state has δξ = δπ. "
      f"Our computation gives δπ − δξ = {f(B['withdrawn_shadow_line']['max_abs_dpi_minus_dxi_fock'],1)} for n = 0–6, so the claimed residual "
      "is −1, not 0. The claim is withdrawn."), align="justify")
P(d, ("The cross-state relation ⟨π²⟩ₙ₊₁ = ⟨ξ²⟩ₙ + 1 does hold, but only because the step is 1 and ⟨ξ²⟩ = ⟨π²⟩ in every eigenstate. It "
      "places no constraint on any single state. Figure 3 shows where actual states lie in the (δξ, δπ) plane. Fock and thermal states lie on "
      "the diagonal δπ = δξ; coherent states all sit at (1/√2, 1/√2); squeezed vacua lie on the Heisenberg hyperbola δξ·δπ = ½. "
      "These are the standard loci [5, 6]. No state family clusters along δπ = δξ + 1."), align="justify")
FIGURE(d, "fig4_quadrature_map.png", "Figure 3. Left: quadrature-variance map of Fock, thermal, coherent, squeezed and displaced-squeezed states "
       "(converged Fock cutoffs). Right: δξ·δπ of squeezed vacuum versus r. With converged N it stays at ½; with a fixed N = 30 (the v1.0 "
       f"setting) it drifts to {f(sq[1.2]['N30_product'],3)} at r = 1.2 and {f(sq[1.5]['N30_product'],3)} at r = 1.5, a pure truncation artefact.")

H(d, "6. Thermal states: the rung occupation and its spread", 1)
P(d, ("A thermal state is ρ = Σ P(n)|n⟩⟨n| with P(n) = n̄ⁿ/(1+n̄)ⁿ⁺¹ and n̄ = 1/(e^{ħω/k_BT} − 1) [18]. "
      "Its quadrature variances are fixed numbers, ⟨ξ²⟩ = ⟨π²⟩ = n̄ + ½, so in the (δξ, δπ) plane it is a single point on the "
      "diagonal, not a band. What spreads is the rung the system occupies. Because the rung value rₙ = n + ½ has unit spacing, "
      "its variance over the Bose–Einstein mixture equals the photon-number variance. This corrects Eq. (23) of the earlier draft, "
      "which carried a spurious factor of 4:"), align="justify")
EQ(d, "Var_P(rₙ) = Var_P(n + ½) = ⟨n²⟩ − ⟨n⟩² = n̄(n̄ + 1),    σₙ = √(n̄(n̄+1))", 5)
P(d, ("Combining with F7 gives a compact statement, σₙ² = ⟨ξ²⟩⟨π²⟩ − ¼. For a thermal state, the photon-number variance equals the "
      "squared uncertainty product minus its Heisenberg minimum. As T → 0, σₙ → 0; for k_BT ≫ ħω, σₙ ≈ k_BT/ħω. "
      "Table 1 lists computed values. Each Fock cutoff N was increased until the result agreed with the next larger N to 10⁻⁹. "
      f"With the fixed N = 30 used in v1.0, the error at n̄ = 10 is {100*Cn[10.0]['rel_err_at_N30']:.1f}%."), align="justify")
rows = [["n̄", "N (converged)", "σₙ computed", "√(n̄(n̄+1))", "rel. error", "rel. error at N = 30"]]
for nb in [0.1, 0.5, 1.0, 3.0, 5.0, 10.0]:
    c = Cn[nb]; rows.append([nb, c["N_converged"], f(c["sigma_n"], 6), f(c["sigma_pred"], 6), e(c["rel_err"]), e(c["rel_err_at_N30"])])
TABLE(d, rows); P(d, "Table 1. Thermal photon-number spread (fvl_verify.py, section C).", size=9, italic=True)
FIGURE(d, "fig5_thermal.png", "Figure 4. (a) σₙ versus n̄ (converged N, circles; N = 30, crosses). (b) Rung occupation P(n) with n̄ ± σₙ bars. "
       "(c) σₙ² against ⟨ξ²⟩⟨π²⟩ − ¼ on the identity line, the thermal instance of F7.")

H(d, "7. A squeezed vacuum singled out by algebra: a null result", 1)
P(d, ("Intersecting the withdrawn line δπ = δξ + 1 with the hyperbola δξ·δπ = ½ gives 2δξ² + 2δξ − 1 = 0, so δξ* = (√3 − 1)/2 and "
      "δπ* = (√3 + 1)/2. It remains a pleasant exercise. Physically, the point is just the squeezed vacuum S(r*)|0⟩ with "
      f"e^{{−r*}}/√2 = δξ*, i.e. r* = ln[(√6 + √2)/2] = ln(2 cos 15°) = {f(D['r_star'])}. Every point on the hyperbola is a squeezed vacuum "
      "with some r, and none is preferred. The earlier draft predicted enhanced stability at r*. We tested that prediction under thermal "
      f"amplitude damping (γ = {D['gamma']}, n̄_th = {D['nth']}). For this Gaussian channel the variances are known exactly [6]:"), align="justify")
EQ(d, "Var ξ(t) = ½e^{−2r} e^{−γt} + (n̄_th + ½)(1 − e^{−γt}),    Var π(t) = ½e^{2r} e^{−γt} + (n̄_th + ½)(1 − e^{−γt})", 6)
P(d, ("A fourth-order Runge–Kutta integration of the Lindblad equation agrees with Eq. (6) to "
      f"{e(max(c['max_abs_err_rk4_vs_analytic'] for c in D['rk4_check']))}. The time for δξ·δπ to reach 0.55 decreases monotonically with r, "
      f"from {f(D['rows'][0]['departure_time'],1)} (r = 0) to {f(D['rows'][-1]['departure_time'],2)} (r = 1.2), in units of 1/ω. "
      f"At r* it is {f(D['t_dep_rstar'],2)}, against {f(D['t_dep_linear_interp_neighbours'],2)} from linear interpolation between neighbours. "
      "There is no anomaly: the null result is what standard theory predicts (Fig. 5)."), align="justify")
FIGURE(d, "fig6_decoherence.png", "Figure 5. Left: uncertainty product under thermal amplitude damping for several r, including r*. Right: time to "
       "δξ·δπ = 0.55 versus the initial δξ. The curve is smooth and monotonic through r* (star).")

H(d, "8. Controls and numerical method", 1)
P(d, ("Negative control. For H = ħω(π² + ξ²)/2 + λξ⁴, the position-variance steps between the first seven eigenstates are "
      + "; ".join(f"λ = {k}: {f(v['x_steps'][0],3)} → {f(v['x_steps'][-1],3)}" for k, v in E.items() if k != "0.0")
      + f". The values are unchanged between Fock bases of 40 and 120 states (largest change {e(max(v['basis_change_40_to_120'] for v in E.values()))}). "
      "The unit step therefore depends on the harmonic potential, as expected."), align="justify")
P(d, ("Numerics. All states are built from ladder operators in a truncated Fock basis. Analytic expansions are used for coherent and "
      "squeezed states, so they do not depend on a truncated matrix exponential. Each quoted value comes from the smallest cutoff N "
      "that agrees with the next larger one to a relative 10⁻⁹. Wigner functions are evaluated exactly in the Fock basis with Laguerre "
      f"polynomials. They integrate to 1, give W(0,0) = (−1)ⁿ/π for |n⟩ ({f(G['fock1']['W00'],5)} for n = 1) and agree with displaced-parity "
      f"evaluation to {e(G['parity_vs_laguerre_max_diff_pad60'])}. "
      "The v1.0 code evaluated the displaced-parity expression inside a 25-state basis. That produced spurious outer rings for |3⟩ "
      f"(W = {f(G['fock3_corner_4_4']['parity_N25_unpadded'],3)} at ξ = π = 4, against {e(G['fock3_corner_4_4']['laguerre_exact'])} exactly). "
      "It also used a 2/π prefactor in (ξ, π) units and the operator order D†ΠD. Together these doubled the amplitude and mirrored "
      f"displaced states (a coherent state with ⟨ξ⟩ = +2.83 peaked at ξ = −2.83). The Supplement (Figs. S1, S8 and S9) documents all fixes."), align="justify")
FIGURE(d, "fig8_wigner.png", "Figure 6. Wigner functions in (ξ, π), normalised to unit integral, colour scale ±1/π: vacuum, |1⟩, |3⟩, coherent "
       "α = 2, squeezed vacuum r = 0.8 and thermal n̄ = 2. Insets give W(0,0) and the quadrature variances from ρ.")

H(d, "9. Experimental outlook", 1)
P(d, ("The ladder can be measured directly in a trapped-ion oscillator. Prepare |n⟩ by sideband pulses [19, 20], reconstruct W by "
      "displaced-parity tomography [21, 22] and extract the marginal variances. The companion protocol [23] describes such an experiment "
      "as a calibration and teaching exercise. Its outcomes are fixed by standard quantum mechanics, and it is not proposed as a test of "
      "new physics."), align="justify")

H(d, "10. Conclusion", 1)
P(d, ("Harmonic-oscillator eigenstates form a variance ladder with rungs n + ½ and spacing exactly 1 in oscillator units. Read on this "
      "ladder, the consecutive-integer identities (the ML Identity a + a² + b = b², the gnomon, the difference and product forms, completing "
      "the square and the triangular forms) become small facts of oscillator algebra. For example, n(n+1) measures how far |n⟩ sits above the "
      "Heisenberg floor, and it is the thermal photon-number variance. These connections are elementary, and they are presented here as "
      "teaching material. The earlier draft's conjugate “shadow” constraint and its fixed-point prediction do not survive scrutiny. "
      "We withdraw them and report the null result."), align="justify")

H(d, "Acknowledgments", 1)
P(d, ("The author thanks Mrs. Allen of Raymond High School, Raymond, Mississippi, whose mathematics class was the setting for his 1999 "
      "exploration of consecutive squares. " + AI_ACK), align="justify")
H(d, "Data and code availability", 2)
P(d, ("The deposited package contains fvl_core.py (engine), fvl_verify.py (writes results/results.json with computed pass/fail and "
      "tolerances), regen_figures.py (all figures) and the document builders. Every number in this note is read from results.json."), align="justify")

H(d, "References", 1)
refs = [
 "W. Heisenberg, Z. Phys. 43, 172 (1927).",
 "E. H. Kennard, Z. Phys. 44, 326 (1927).",
 "H. P. Robertson, Phys. Rev. 34, 163 (1929); E. Schrödinger, Sitzungsber. Preuss. Akad. Wiss., Phys.-Math. Kl. 14, 296 (1930).",
 "D. J. Griffiths and D. F. Schroeter, Introduction to Quantum Mechanics, 3rd ed. (Cambridge University Press, 2018), Sec. 2.3.",
 "C. C. Gerry and P. L. Knight, Introductory Quantum Optics (Cambridge University Press, 2005), Chs. 2–3, 7.",
 "D. F. Walls and G. J. Milburn, Quantum Optics, 2nd ed. (Springer, 2008).",
 "J. J. Sakurai and J. Napolitano, Modern Quantum Mechanics, 3rd ed. (Cambridge University Press, 2020), Sec. 2.3.",
 "S. Aaronson, “Shadow tomography of quantum states,” in Proc. 50th ACM STOC (2018), pp. 325–338; arXiv:1711.01053.",
 "H.-Y. Huang, R. Kueng and J. Preskill, Nat. Phys. 16, 1050 (2020).",
 "M. Hillery, R. F. O'Connell, M. O. Scully and E. P. Wigner, Phys. Rep. 106, 121 (1984).",
 "A. Royer, Phys. Rev. A 15, 449 (1977).",
 "W. P. Schleich, Quantum Optics in Phase Space (Wiley-VCH, 2001).",
 "H. A. Bethe and E. E. Salpeter, Quantum Mechanics of One- and Two-Electron Atoms (Springer, 1957), Sec. 3.",
 "M. L. McKnight, the ML Identity (unpublished note, Raymond High School, Raymond, Mississippi, 1999).",
 "Nicomachus of Gerasa, Introduction to Arithmetic (c. 100 CE), transl. M. L. D'Ooge (Macmillan, 1926).",
 "Leonardo Pisano (Fibonacci), The Book of Squares (Liber Quadratorum, 1225), transl. L. E. Sigler (Academic Press, 1987).",
 "R. E. Langer, Phys. Rev. 51, 669 (1937).",
 "F. Mandl, Statistical Physics, 2nd ed. (Wiley, 1988).",
 "D. M. Meekhof, C. Monroe, B. E. King, W. M. Itano and D. J. Wineland, Phys. Rev. Lett. 76, 1796 (1996).",
 "D. Leibfried, R. Blatt, C. Monroe and D. Wineland, Rev. Mod. Phys. 75, 281 (2003).",
 "D. Leibfried et al., Phys. Rev. Lett. 77, 4281 (1996).",
 "L. G. Lutterbach and L. Davidovich, Phys. Rev. Lett. 78, 2547 (1997).",
 "M. L. McKnight, “Fock Variance Ladder: Experimental Protocol, v2.0” and “Fock Variance Ladder: Computational Verification, v2.0,” ML Innovations Research Lab (2026).",
]
for i, r_ in enumerate(refs, 1): P(d, r_, bold_lead=f"[{i}] ", size=9.5)
P(d, "")
P(d, "──────────────────────────────", align="center", size=10)
P(d, f"{AUTHOR} · {ORG} · {PLACE} · {EMAIL}", align="center", size=9)
out = os.path.join(ROOT, "docs", "Fock_Variance_Ladder_Paper_v2.docx"); d.save(out); print("saved", out)
