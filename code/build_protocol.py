"""Build the revised protocol (v2.0) by editing a COPY of ML's original protocol docx.
The original file is opened read-only; the output is written to docs/."""
import copy, glob, math
from docbuild_common import *
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.shared import Inches

SRC = glob.glob(os.path.join(ROOT, "..", "9df80a77*.docx"))[0]
d = Document(SRC)
els = list(d.element.body.iterchildren())
I = R["I_protocol_numbers"]; B = R["B_quadrature_map"]; D = R["D_squeezed_decoherence"]; Hn = R["H_nonharmonic"]; AP = R["A_physical"]; E = R["E_anharmonic_control"]

def par(i): return Paragraph(els[i], d)
def S(i, body, lead=None):
    """Replace text of paragraph i. If it has a bold lead run, keep/replace it and put body in run 2."""
    p = par(i); runs = p.runs
    if len(runs) >= 2:
        if lead is not None: runs[0].text = lead
        runs[1].text = body
        for r in runs[2:]: r.text = ""
    else:
        runs[0].text = (lead or "") + body
def delete(i): els[i].getparent().remove(els[i])
def tbl(i): return Table(els[i], d)
def cell(t, r, c, text):
    ce = t.rows[r].cells[c]; ps = ce.paragraphs
    if ps[0].runs: ps[0].runs[0].text = text; [setattr(x, "text", "") for x in ps[0].runs[1:]]
    else: ps[0].add_run(text)
def setrow(t, r, vals):
    for c, v in enumerate(vals): cell(t, r, c, str(v))
def droprow(t, r): t._tbl.remove(t.rows[r]._tr)
def fig_before(i, fname, caption, width=6.0):
    anchor = par(i)
    cp = anchor.insert_paragraph_before(caption); cp.alignment = 1
    for r in cp.runs: r.italic = True; r.font.size = docx.shared.Pt(9)
    pp = cp.insert_paragraph_before(); pp.alignment = 1
    pp.add_run().add_picture(os.path.join(FIG, fname), width=Inches(width))
import docx

# ---------------- title block ----------------
S(2, "Fock Variance Ladder:"); S(3, "Measuring the Quadrature-Variance"); S(4, "Ladder of a Trapped-Ion Oscillator")
S(5, "A teaching and calibration protocol companion to the Fock Variance Ladder note")
S(8, ORG); S(10, EMAIL)
S(12, "Document Version: 2.0 (supersedes 1.0)"); S(13, "Date: November 23, 2026")

# ---------------- 1. purpose ----------------
S(17, ("This document specifies an experimental protocol for measuring four standard properties of the quantum harmonic oscillator "
       "that the companion note (McKnight, 2026, ref. [6]) organises around the ML Identity family, a + a² + b = b² with b = a + 1 "
       "and its equivalent forms. These forms are elementary algebraic identities for consecutive integers and half-integers, "
       "known classically. The identity is not unique: every degree-2 identity that holds on the line b = a + 1 is a multiple of b − a − 1. "
       "All four measurements are predicted by textbook quantum mechanics. Their value is pedagogical and as an end-to-end calibration "
       "of state preparation and Wigner tomography. They are not tests of new physics."))
S(19, ("For a harmonic oscillator in Fock state |n⟩, ⟨ξ²⟩ₙ = ⟨π²⟩ₙ = n + ½ (ξ = x/x₀, π = p/p₀, x₀ = √(ħ/mω), p₀ = √(ħmω)). "
       "The step between consecutive rungs is exactly 1, independent of n (in physical units, x₀² = ħ/mω). This is the F1 form "
       "with a = ⟨ξ²⟩ₙ and b = ⟨ξ²⟩ₙ₊₁."), "Prediction 1 — Unit Variance Step: ")
S(20, ("Every state lies on or above the Heisenberg curve δξ·δπ = ½. Fock and thermal states lie on the diagonal δπ = δξ; "
       "coherent states sit at (1/√2, 1/√2); squeezed vacua move along δξ·δπ = ½. The v1.0 “shadow line” δπ = δξ + 1 is withdrawn: "
       "it fails for every Fock state, for which δπ − δξ = 0. The +1 is the step between rungs, ⟨π²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = 1, not a "
       "constraint on a single state."), "Prediction 2 — Quadrature-Variance Map: ")
S(21, ("For a thermal state with mean occupation n̄ = 1/(exp(ħω/k_BT) − 1), the standard deviation of the photon (phonon) number is "
       "σₙ = √(n̄(n̄+1)) (Bose–Einstein statistics). Equivalently, σₙ² = ⟨ξ²⟩⟨π²⟩ − ¼ (form F7). σₙ → 0 as T → 0; σₙ ≈ k_BT/ħω at high T."),
  "Prediction 3 — Thermal Photon-Number Spread: ")
S(22, (f"The squeezed vacuum with r* = ln((√6+√2)/2) = {f(D['r_star'],4)} has δξ* = (√3 − 1)/2 ≈ {f(D['dxi_star'],3)} and "
       f"δπ* = (√3 + 1)/2 ≈ {f(D['dpi_star'],3)}, product ½. Standard theory (Gaussian-channel decoherence) predicts no special stability "
       "at r*: departure from minimum uncertainty is monotonic in r. This is run as a null test."), "Prediction 4 — Squeezed-Vacuum Null Test: ")
t = tbl(25)
setrow(t, 1, ["Unit Variance Step", "Δ⟨ξ²⟩ = 1.00 ± 0.05 across n = 0–6", "Δ⟨ξ²⟩ deviates > 5% for any adjacent pair (diagnose apparatus)"])
setrow(t, 2, ["Quadrature-Variance Map", "Fock/thermal on δπ = δξ; squeezed on δξ·δπ = ½ (within errors)", "Points below δξ·δπ = ½ (calibration error)"])
setrow(t, 3, ["Thermal Number Spread", "Measured σₙ matches √(n̄(n̄+1)) within 10%", "Wrong functional form (non-thermal heating or readout error)"])
setrow(t, 4, ["Squeezed-Vacuum Null", "Degradation monotonic in r; no feature at r*", "Reproducible feature at r* (would require new explanation)"])

# ---------------- 2. platform ----------------
S(30, (f"The axial potential of a linear Paul trap is harmonic to better than 1 part in 10⁴ over the relevant range of motional "
       f"amplitudes for low-lying Fock states (n ≤ 10). Anharmonic corrections enter at order (x/d)² where d is the electrode spacing "
       f"(~1 mm). For ²⁵Mg⁺ at ω/2π = 2 MHz, x₀ = √(ħ/mω) = {AP['x0_m']*1e9:.1f} nm and the ground-state rms extent is "
       f"x₀/√2 = {AP['zero_point_rms_m']*1e9:.1f} nm, so x₀/d ~ 10⁻⁵ and anharmonicity is negligible."))
S(31, ("Resolved sideband cooling of ²⁵Mg⁺ has been demonstrated to mean phonon number n̄ = 0.13 ± 0.04 (Ospelkaus et al., 2011), and "
       "near-unit ground-state occupation has been reported in ⁴⁰Ca⁺ (Schmidt-Kaler et al.; citation year and figure to be verified by the author). "
       "This provides the low-temperature anchor required for Prediction 3."))
S(34, ("Anomalous heating in ion traps is well characterised and can be used constructively: after ground-state cooling, waiting a "
       "controlled time raises the mean occupation at the measured heating rate Γₕ. With Γₕ = 5 phonons/s (the target in Sec. 3.1.1), "
       "one phonon is added every 200 ms. Γₕ must be measured in situ (Calibration 4)."))
S(39, ("The quadrature-variance ladder applies specifically to the harmonic oscillator. Superconducting cavities have weak anharmonicity "
       "from the Kerr effect (self-Kerr K/2π ~ 1–10 kHz for 3D cavities, compared to cavity frequency ~6 GHz). For Fock states n ≤ 10, "
       "the Kerr-induced frequency shift n·K is < 100 kHz, or < 0.002% of the cavity frequency. This is within tolerance but must be "
       "characterised and corrected in the analysis. For n > 20, Kerr corrections become significant and harmonicity cannot be assumed."),
  "Critical note on harmonicity: ")

# ---------------- 4. Experiment A ----------------
S(58, ("Starting from |0, ↓⟩, climb the ladder with alternating blue- and red-sideband π pulses (|n, ↓⟩ → |n+1, ↑⟩ on the blue sideband, "
       "then |n+1, ↑⟩ → |n+2, ↓⟩ on the red sideband), as in Meekhof et al. (1996), ref. [13]. Optical repumping is not used between steps "
       "because it would heat the motion. Each pulse length is set by the n-dependent sideband Rabi frequency, Ω_{n,n+1} = Ω₀√(n+1) "
       "(Lamb–Dicke regime): t_π(n) = π/(Ω₀√(n+1)). Ω₀/2π is typically 50–100 kHz, so n = 6 needs six operations of order 100–200 μs in total."))
S(59, ("For each prepared state, measure displaced parity over a grid of phase-space points α = (ξ + iπ)/√2. Apply D(−α) to the state "
       "(equivalently, measure ⟨D(α) Π D†(α)⟩) with a resonant electric-field drive, then read the parity Π = (−1)^{a†a} via blue-sideband "
       "mapping. In the quadrature units of this protocol, W(ξ, π) = (1/π)⟨D(α) Π D†(α)⟩, normalised so that ∫W dξ dπ = 1 "
       "(equivalently W(α) = (2/π)⟨…⟩ per d²α). Scan at least a 21 × 21 grid covering |α| ≤ √(2n+3)."))
S(60, ("From the measured Wigner function W(ξ, π), take the marginals P(ξ) = ∫W dπ and P(π) = ∫W dξ and compute δξ² = ⟨ξ²⟩ − ⟨ξ⟩² and "
       "δπ² = ⟨π²⟩ − ⟨π⟩². For ideal Fock states both equal n + ½. Alternatively, reconstruct ρ by maximum-likelihood estimation and "
       "compute the variances from ρ."))
S(61, ("For each pair (n, n+1), compute Δ⟨ξ²⟩ = ⟨ξ²⟩ₙ₊₁ − ⟨ξ²⟩ₙ. The prediction is 1.000. Repeat the sequence 500–1000 times per "
       "Fock state to reach statistical uncertainty < 0.02 on each variance."))
S(65, ("For Fock states ⟨ξ²⟩ = ⟨π²⟩ by symmetry. Any deviation from the unit step indicates imperfect state preparation, "
       "anharmonicity or heating during measurement, not new physics."), "Note: ")
fig_before(66, "fig1_variance_ladder.png", "Figure 1. The Fock variance ladder: energy levels and Wigner functions, unit steps in ⟨ξ²⟩, "
           "and the contrast with the square well, hydrogen and a quartic oscillator (computed; see the Computational Verification supplement).")

# ---------------- Experiment B ----------------
S(67, "4.2 Experiment B: Quadrature-Variance Map")
S(69, ("Map δξ against δπ across states with different variance distributions. Verify the textbook loci: Fock and thermal states on "
       "the diagonal δπ = δξ, coherent states at (1/√2, 1/√2), squeezed vacua on δξ·δπ = ½. No state may fall below δξ·δπ = ½."))
S(71, "States that break the symmetry between quadratures, with computed values (converged Fock-basis numerics):")
t = tbl(72)
cell(t, 0, 4, "δξ·δπ")
for row, sq in zip([3, 4, 5], I["squeezed_table"]):
    setrow(t, row, [f"Squeezed vacuum S(r)|0⟩, r = {sq['r']}", "Parametric modulation at 2ωz", f(sq["dxi"], 3), f(sq["dpi"], 3), "0.500"])
setrow(t, 1, ["Vacuum |0⟩", "Sideband cool to ground state", "0.707", "0.707", "0.500"])
setrow(t, 2, ["Coherent |α⟩", "Resonant displacement after cooling", "0.707", "0.707", "0.500"])
setrow(t, 6, ["Squeezed coherent D(α)S(r)|0⟩", "Parametric drive + displacement", "e⁻ʳ/√2", "eʳ/√2", "0.500"])
setrow(t, 7, ["Thermal (mean n̄)", "Wait after cooling (controlled heating)", "√(n̄ + ½)", "√(n̄ + ½)", "n̄ + ½"])
S(73, "4.2.3 What the +1 is")
S(74, ("For a pure squeezed vacuum, δξ² = e⁻²ʳ/2 and δπ² = e²ʳ/2, so δξ·δπ = ½ and δπ − δξ = √2 sinh r, which takes any positive value. "
       "No state family clusters on δπ = δξ + 1, and Fock states violate it by exactly 1."), "Squeezed states: ")
S(75, ("The +1 lives between rungs, not within a state: ⟨ξ²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = 1 and ⟨π²⟩ₙ₊₁ − ⟨ξ²⟩ₙ = 1. Any state written as "
       "ρ = Σ P(n)|n⟩⟨n| + coherences has Fock components on this ladder. The analysis has two levels:"), "")
S(76, "The unit step between adjacent Fock states (Experiment A).", "Level 1 (rung level): ")
S(77, ("For a phase-averaged state ρ = Σ P(n)|n⟩⟨n|, ⟨ξ²⟩ = Σ P(n)(n + ½) = n̄ + ½: the state sits at one point on the diagonal, and "
       "σₙ measures how widely P(n) spreads over the rungs (Experiment C)."), "Level 2 (state level): ")
S(79, ("For each state: (1) prepare it; (2) perform Wigner tomography (21 × 21 grid minimum); (3) extract both quadrature variances; "
       "(4) reconstruct ρ in the Fock basis; (5) extract P(n); (6) compute σₙ² = ⟨n²⟩ − ⟨n⟩²; (7) plot δπ against δξ for all states "
       "together with the curve δξ·δπ = ½."))
S(81, ("Points should fall on the textbook loci within errors. Any point significantly below δξ·δπ = ½ indicates a calibration error "
       "in displacement amplitude or parity readout. This experiment is a check of the tomography chain, not a test of new physics."))
fig_before(82, "fig4_quadrature_map.png", "Figure 2. Computed quadrature-variance map (left) and squeezed-vacuum uncertainty product "
           "against r for converged Fock cutoff and for fixed N = 30 (right).")

# ---------------- Experiment C ----------------
S(83, "4.3 Experiment C: Thermal Photon-Number Spread")
S(85, ("Measure the photon-number spread σₙ against effective temperature and compare it with the parameter-free Bose–Einstein "
       "result √(n̄(n̄+1))."))
t = tbl(87)
cell(t, 0, 2, "Predicted σₙ"); cell(t, 0, 3, f"Physical T (ω/2π = 2 MHz; ħω/k_B = {I['hbar_omega_over_kB_K']*1e6:.1f} μK)")
meth = ["Sideband cool, verify residual excitation", None, None, None, None, "Wait or inject thermal noise", "Direct thermal preparation (or wait)"]
for k, rw in enumerate(I["rows"]):
    w = rw["wait_s_from_ground_at_5_per_s"] * 1000
    m = meth[k] or f"Wait ~{w:.0f} ms at Γₕ = 5 phonons/s"
    if k == 1: m = f"Sideband cool, short wait (~{w:.0f} ms)"
    if k in (5, 6): m = f"{m} (~{w:.0f} ms at 5 phonons/s)"
    T_ = rw["T_K"]; Ts = f"{T_*1e6:.1f} μK" if T_ < 1e-3 else f"{T_*1e3:.2f} mK"
    setrow(t, k + 1, [f(rw["nbar"], 2), m, f(rw["sigma_n"], 3), Ts])
S(89, ("For each temperature point: (1) prepare the ground state by sideband cooling; (2) wait the prescribed time; (3) perform "
       "tomography, or for phase-averaged states read P(n) directly; (4) reconstruct ρ; (5) extract P(n) = ⟨n|ρ|n⟩; (6) compute ⟨n⟩, "
       "⟨n²⟩ and σₙ; (7) verify the Bose–Einstein form P(n) = n̄ⁿ/(1+n̄)ⁿ⁺¹; (8) compare σₙ with √(n̄(n̄+1)). Repeat each point 500+ times. "
       "Note: heating from the ground state at a constant rate is only approximately thermal; step (7) checks this."))
S(90, "4.3.4 Key Test: Number Spread at Low Temperature")
S(91, (f"At n̄ = 0.05, σₙ = {f(I['rows'][0]['sigma_n'],3)}: P(1) = {f(I['thermal_P1_at_nbar0.05'],4)} and P(n ≥ 1) = "
       f"{f(I['thermal_Pge1_at_nbar0.05'],4)}, so the distribution is essentially confined to n = 0. At n̄ = 0 the spread vanishes and "
       "the state is the pure ground state. The low-n̄ points are the most sensitive test of readout fidelity."))

# ---------------- Experiment D ----------------
S(92, "4.4 Experiment D: Squeezed-Vacuum Null Test")
S(94, (f"Test whether squeezed vacua near r* = {f(D['r_star'],4)} (δξ* ≈ {f(D['dxi_star'],3)}) degrade differently from neighbouring "
       "squeeze values. Standard theory predicts that they do not."))
# heating-only estimate of the hold time needed: each quadrature variance grows by Γh·t
def t_dep(r, G=5.0, target=0.55):
    V1, V2 = math.exp(-2*r)/2, math.exp(2*r)/2
    dd = (-(V1+V2) + math.sqrt((V1+V2)**2 + 4*(target**2 - V1*V2))) / 2
    return dd / G
tr = [t_dep(x) for x in (0.0, D["r_star"], 1.2)]
S(96, ("This test is exploratory and must be designed to avoid confirmation bias (prepare squeeze values in randomised order; "
       "analyse blind to r). In the Gaussian-channel model the variance relaxes as V(t) = V₀e^{−γt} + (n̄_th + ½)(1 − e^{−γt}), "
       "which has no feature at any particular r. The companion simulation finds departure times strictly monotonic in r."))
S(97, ("(1) Prepare squeezed vacua with r chosen to give δξ from 0.15 to 0.80 (at least 10 values, randomised order). (2) Confirm "
       "δξ·δπ ≈ ½ at t = 0. (3) Hold for a variable time. With heating at Γₕ = 5 phonons/s acting alone (each quadrature variance growing "
       f"by Γₕt), δξ·δπ reaches 0.55 after {tr[0]*1e3:.1f} ms at r = 0, {tr[1]*1e3:.1f} ms at r* and {tr[2]*1e3:.1f} ms at r = 1.2 "
       "(estimate computed in build_protocol.py), so hold times should span about 0.5–50 ms rather than 10–500 μs. (4) Re-measure the "
       "quadrature variances. (5) Plot the degradation rate against initial δξ. (6) Test for any feature near δξ*."))
S(98, ("Degradation is monotonic in r with no feature at δξ* (the expected outcome). A reproducible feature at r* would conflict "
       "with the Gaussian-channel model and would need an independent explanation; it would not by itself confirm any interpretation "
       "of the identity."), "Null hypothesis: ")

# ---------------- Analysis / controls ----------------
t = tbl(108); setrow(t, 4, ["Squeezed-vacuum null test", "200", "2 quadratures × 10 hold times", "4,000"])
h3 = [h for h in Hn["hydrogen"] if h["l"] == 0]
S(113, ("Where available, measure quadrature variances of eigenstates in a weakly anharmonic potential (e.g. a transmon mode or a "
        "Duffing oscillator). The unit step should fail, as the companion computation shows (quartic λ = 0.1: Δ⟨ξ²⟩ falls from "
        f"{f(E['0.1']['x_steps'][0],3)} to {f(E['0.1']['x_steps'][-1],3)} and Δ⟨π²⟩ rises from {f(E['0.1']['p_steps'][0],3)} to "
        f"{f(E['0.1']['p_steps'][-1],3)} over n = 0→6). This is a specificity check of the measurement chain.") if "0.1" in E else None,
  "Control 1 — Anharmonic comparison: ")
S(114, ("For hydrogen the second moment is ⟨r²⟩ = (n²a₀²/2)[5n² + 1 − 3l(l+1)] (Bethe & Salpeter). For s states, Var(x) = ⟨r²⟩/3, "
        f"so the steps grow roughly as n³ (⟨r²⟩/a₀² = {', '.join(f(h['formula_div2'],0) for h in h3[:4])} for n = 1–4, l = 0) instead of "
        "staying constant. This confirms the unit step is specific to the harmonic potential. It may be done computationally."),
  "Control 2 — Hydrogen (non-harmonic) comparison: ")
S(117, ("Measure the Wigner function of |0⟩. It should be a Gaussian at the origin with standard deviation 1/√2 in both quadratures "
        "and peak W(0,0) = 1/π ≈ 0.318 in (ξ, π) units. It must be positive everywhere; negativity indicates measurement error."))
S(118, ("Prepare |1⟩ and measure its Wigner function. In (ξ, π) units W(0,0) = −1/π ≈ −0.318 (equivalently −2/π per d²α). "
        "Since W(0,0) = (1/π)⟨Π⟩ and, for a mixture of |1⟩ (weight F) and |0⟩, ⟨Π⟩ = 1 − 2F, the measured value calibrates "
        "the preparation fidelity: F = (1 − πW(0,0))/2. F > 0.95 is required to proceed. This is routinely demonstrated in "
        "trapped ions and superconducting circuits."))
S(119, ("After ground-state cooling, measure the mean phonon number at delays of 0, 50, 100, 200, 500, 1000 and 2000 ms (the range "
        "used in Experiment C). Fit ⟨n⟩(t) = ⟨n⟩₀ + Γₕt. Γₕ corrects systematic errors in Experiments A–B and sets the thermal points "
        "in Experiment C."))

# ---------------- 7. outcomes ----------------
t = tbl(123)
setrow(t, 1, ["All four as predicted", "Standard harmonic-oscillator QM and the tomography chain are verified", "Use as a teaching dataset and calibration benchmark"])
setrow(t, 2, ["1–3 as predicted, 4 null", "Expected outcome", "Report the null result; r* is a geometric point, not a dynamical one"])
setrow(t, 3, ["1 as predicted, 2 or 3 off", "Tomography or heating not as modelled", "Diagnose displacement calibration, readout and heating spectrum"])
setrow(t, 4, ["1 fails", "Systematic experimental error; oscillator QM not in doubt", "Diagnose apparatus; do not proceed until the unit step is confirmed"])
S(125, ("All four predictions follow from standard quantum mechanics without reference to the ML Identity. Fock-state variances "
        "n + ½ appear in every textbook (e.g. Gerry & Knight). The Bose–Einstein number variance n̄(n̄+1) is standard statistical "
        "mechanics. The decoherence of squeezed states under thermal damping is standard quantum optics."))
S(126, ("What the ML Identity family adds is organisational. The forms F1–F10 (consecutive-squares gap, ab = a² + a, "
        "n(n+1) = (n + ½)² − ¼, gnomons, triangular numbers) are classical and are not unique. They provide compact reading aids for "
        "the ladder: F1 links adjacent rungs, F7 links the uncertainty product to the number spread, and the gnomon form gives the "
        "cumulative height of the ladder. The experiment does not test whether quantum mechanics is correct."))
S(127, ("None of the predictions goes beyond textbook quantum mechanics. The protocol's value is as a clean, end-to-end demonstration "
        "that can be compared against exact computations, and as a calibration of the tomography chain. The squeezed-vacuum test is "
        "kept as an honest null test."))
t = tbl(131)
cell(t, 4, 0, "Phase 3: Experiment B (Quadrature map)"); cell(t, 5, 0, "Phase 4: Experiment C (Number spread)")
cell(t, 5, 2, "Thermal state preparation at 7 temperature points, Fock distribution extraction, number-spread measurement")
cell(t, 6, 0, "Phase 5: Experiment D (Null test)")
S(134, ("Groups with relevant published capability include (non-exhaustive, not contacted): NIST Ion Storage Group (Boulder, CO), "
        "PTB (Braunschweig), ETH Zürich Trapped Ion Quantum Information Group, Innsbruck Quantum Optics and Spectroscopy, Yale "
        "(Schoelkopf–Devoret, cQED) and the University of Chicago Schuster Lab (cQED)."))
S(136, ("This protocol measures standard properties of the harmonic oscillator that the ML Identity family organises. Limitations:"))
S(137, ("Confirming it is a calibration, not a discovery."), "1. The unit variance step (Prediction 1) is standard quantum mechanics. ")
S(138, ("It provides a consistency check of the tomography chain, not a test of any new framework."), "2. The thermal number spread (Prediction 3) follows from Bose–Einstein statistics. ")
S(139, ("The v1.0 “shadow line” δπ = δξ + 1 is withdrawn; Fock states violate it by exactly 1. The experiment maps the textbook loci."), "3. The quadrature-variance map (Prediction 2) has no new content. ")
S(140, ("A null result is expected from standard theory. A positive result would need an independent explanation."), "4. The squeezed-vacuum test (Prediction 4) is a null test. ")
S(141, ("Claims about relevance to quantum gravity, black holes or holographic bounds are outside its scope."), "5. This protocol does not test non-harmonic systems. ")

# ---------------- references ----------------
refs = [
 ("[3] ", "Heisenberg, W. Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik. Zeitschrift für Physik 43, 172–198 (1927)."),
 ("[4] ", "Kennard, E. H. Zur Quantenmechanik einfacher Bewegungstypen. Zeitschrift für Physik 44, 326–352 (1927)."),
 ("[5] ", "Leibfried, D. et al. Experimental determination of the motional quantum state of a trapped atom. Physical Review Letters 77, 4281 (1996)."),
 ("[6] ", "McKnight, M. L. The Fock Variance Ladder: Unit Variance Steps of the Quantum Harmonic Oscillator and the ML Identity Family — a pedagogical note. v2.0, ML Innovations Research Lab (2026)."),
 ("[7] ", "Schmidt-Kaler, F. et al. Ground state cooling, quantum state engineering and study of decoherence of ions in Paul traps. Journal of Modern Optics 47, 2573–2582 (2000)."),
 ("[8] ", "Wolf, F. et al. Motional Fock states for quantum-enhanced amplitude and phase measurements with trapped ions. Nature Communications 10, 2929 (2019)."),
 ("[9] ", "Wineland, D. J. et al. Quantum harmonic oscillator state synthesis and analysis. Proc. Royal Society (1998)."),
 ("[10] ", "Two-Mode Bosonic State Tomography with Single-Shot Joint-Parity Measurement of a Trapped Ion. PRX Quantum 6 (2025). [Author list to be added.]"),
 ("[11] ", "Shalibo, Y. et al. Direct Wigner tomography of a superconducting anharmonic oscillator. Physical Review Letters 110, 100404 (2013)."),
 ("[12] ", "Tiranov, A. et al. Time-of-flight quantum tomography of an atom in an optical tweezer. Nature Physics 19, 569–573 (2023)."),
]
for k, (lead, body) in zip(range(149, 159), refs): S(k, body, lead)
extra = [
 ("[13] ", "Meekhof, D. M., Monroe, C., King, B. E., Itano, W. M. & Wineland, D. J. Generation of nonclassical motional states of a trapped atom. Physical Review Letters 76, 1796 (1996)."),
 ("[14] ", "Leibfried, D., Blatt, R., Monroe, C. & Wineland, D. Quantum dynamics of single trapped ions. Reviews of Modern Physics 75, 281 (2003)."),
 ("[15] ", "Lutterbach, L. G. & Davidovich, L. Method for direct measurement of the Wigner function in cavity QED and ion traps. Physical Review Letters 78, 2547 (1997)."),
 ("[16] ", "Gerry, C. C. & Knight, P. L. Introductory Quantum Optics. Cambridge University Press (2005)."),
 ("[17] ", "McKnight, M. L. Fock Variance Ladder: Computational Verification and Analysis Pipeline. v2.0, ML Innovations Research Lab (2026)."),
]
anchor = par(159)
for lead, body in extra:
    np_ = copy.deepcopy(els[158]); anchor._p.addprevious(np_)
    q = Paragraph(np_, d); q.runs[0].text = lead; q.runs[1].text = body
ack = copy.deepcopy(els[136]); anchor._p.addprevious(ack); Paragraph(ack, d).runs[0].text = AI_ACK
S(162, f"{AUTHOR} | {ORG}"); S(163, f"{EMAIL} | {PLACE}")

for i in (14, 146, 147, 148): delete(i)

# ---------------- header / footer / metadata ----------------
for s in d.sections:
    for p in s.header.paragraphs:
        if p.text.strip():
            p.runs[0].text = "ML INNOVATIONS RESEARCH LAB — EXPERIMENTAL PROTOCOL"; [setattr(r, "text", "") for r in p.runs[1:]]
    for p in s.footer.paragraphs:
        for r in p.runs:
            if "Shadow" in r.text: r.text = r.text.replace("Shadow Tomography Experiment v1.0", "Fock Variance Ladder Protocol v2.0")
cp = d.core_properties
cp.author = AUTHOR; cp.last_modified_by = AUTHOR; cp.title = "Fock Variance Ladder: Experimental Protocol (v2.0)"
cp.subject = "Measuring the quadrature-variance ladder of a trapped-ion oscillator"; cp.keywords = "Fock states; Wigner tomography; trapped ions; physics.ed-ph"
cp.comments = AI_ACK; cp.category = "physics.ed-ph"

# global sanity: email and leftover words in body text
for p in d.paragraphs:
    for r in p.runs:
        if "innovations.research" in r.text: r.text = r.text.replace("ml.innovations.research.lab", "ml.innovation.research.lab")
out = os.path.join(ROOT, "docs", "Fock_Variance_Ladder_Experimental_Protocol_v2.docx"); d.save(out); print("saved", out)
