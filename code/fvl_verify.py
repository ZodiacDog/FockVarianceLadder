"""
Fock Variance Ladder — computational verification suite (revised, v2.0)
Every number quoted in the revised paper, supplement and protocol is written to
../results/results.json by this script. Pass/fail is COMPUTED against stated tolerances;
nothing is hard-coded as "confirmed".
M. L. McKnight, ML Innovations Research Lab (ML Innovations LLC), Pheba, MS
AI tools assisted with code and drafting; the author reviewed and is responsible for all content.
"""
import json, os, sys, time
import numpy as np, sympy as sp
from scipy.integrate import quad
from scipy.special import genlaguerre, factorial
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fvl_core import Oscillator, wigner_laguerre, wigner_parity, converged_N

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(OUT, exist_ok=True)
R = {"meta": {"title": "Fock Variance Ladder computational verification v2.0",
              "author": "M. L. McKnight, ML Innovations Research Lab (ML Innovations LLC)",
              "run_time_local": time.strftime("%Y-%m-%d %H:%M %Z"),
              "numpy": np.__version__}}
TOL = {"exact": 1e-12, "converge_rtol": 1e-9, "analytic": 1e-8, "lindblad_vs_analytic": 1e-6}
R["tolerances"] = TOL
def verdict(ok): return "PASS" if bool(ok) else "FAIL"
F = lambda x: float(np.real(x))

# ---------------- A. Unit variance step ----------------
o = Oscillator(40)
A = []
for n in range(11):
    rho = o.fock(n); A.append({"n": n, "var_xi": F(o.var_xi(rho)), "var_pi": F(o.var_pi(rho)),
                               "pred": n + 0.5})
steps = [A[n + 1]["var_xi"] - A[n]["var_xi"] for n in range(10)]
maxdev = max(abs(s - 1) for s in steps)
R["A_unit_step"] = {"rows": A, "steps": steps, "max_dev": maxdev, "tol": TOL["exact"],
                    "status": verdict(maxdev < TOL["exact"])}
# physical units: 25Mg+ at omega/2pi = 2 MHz
hbar, kB, amu = 1.054571817e-34, 1.380649e-23, 1.66053906660e-27
m_ion, w = 24.98583696 * amu, 2 * np.pi * 2e6
x0 = np.sqrt(hbar / (m_ion * w))
R["A_physical"] = {"x0_m": x0, "step_m2": x0 ** 2, "zero_point_rms_m": x0 / np.sqrt(2)}
# convention dependence of the "1"
R["A_conventions"] = {"xi=(a+a^dag)/sqrt2 (this work)": {"vac_var": 0.5, "step": 1.0},
                      "X=(a+a^dag)/2": {"vac_var": 0.25, "step": 0.5},
                      "X=a+a^dag": {"vac_var": 1.0, "step": 2.0},
                      "invariant": "step / vacuum variance = 2 in every convention"}

# ---------------- B. Quadrature-variance map ----------------
def sq_vals(N, r):
    q = Oscillator(N); rho = q.ket_to_rho(q.squeezed_ket(r))
    return np.array([np.sqrt(q.var_xi(rho)), np.sqrt(q.var_pi(rho))])
B = {"fock": [], "coherent": [], "squeezed": [], "thermal": [], "displaced_squeezed": []}
for n in range(7):
    rho = o.fock(n); dx, dp = np.sqrt(o.var_xi(rho)), np.sqrt(o.var_pi(rho))
    B["fock"].append({"n": n, "dxi": F(dx), "dpi": F(dp), "product": F(dx * dp),
                      "dpi_minus_dxi": F(dp - dx), "residual_vs_withdrawn_line_dpi_eq_dxi_plus_1": F(dp - dx - 1)})
for al in [0.5, 1.0, 2.0, 3.0]:
    q = Oscillator(80); rho = q.ket_to_rho(q.coherent_ket(al))
    dx, dp = np.sqrt(q.var_xi(rho)), np.sqrt(q.var_pi(rho))
    B["coherent"].append({"alpha": al, "dxi": F(dx), "dpi": F(dp), "product": F(dx * dp), "N": 80})
for r in [0.2, 0.4, 0.6, 0.6585, 0.8, 1.0, 1.2, 1.5]:
    Nc, val, hist = converged_N(lambda N: sq_vals(N, r), rtol=TOL["converge_rtol"])
    an = np.array([np.exp(-r) / np.sqrt(2), np.exp(r) / np.sqrt(2)])
    v30 = dict(hist)[30]
    B["squeezed"].append({"r": r, "N_converged": Nc, "dxi": F(val[0]), "dpi": F(val[1]),
                          "product": F(val[0] * val[1]), "dxi_analytic": F(an[0]), "dpi_analytic": F(an[1]),
                          "abs_err": F(np.abs(val - an).max()),
                          "status": verdict(np.abs(val - an).max() < TOL["analytic"]),
                          "N30_product": F(v30[0] * v30[1]),
                          "N30_valid": bool(np.abs(v30 - an).max() < 1e-3)})
for al, r in [(1.0, 0.5), (2.0, 0.8), (1.0, 1.0)]:
    q = Oscillator(150); psi = q.displacement(al) @ q.squeezed_ket(r); rho = q.ket_to_rho(psi)
    dx, dp = np.sqrt(q.var_xi(rho)), np.sqrt(q.var_pi(rho))
    B["displaced_squeezed"].append({"alpha": al, "r": r, "dxi": F(dx), "dpi": F(dp), "product": F(dx * dp), "N": 150})
def th_vals(N, nb):
    q = Oscillator(N); rho = q.thermal(nb)
    return np.array([np.sqrt(q.var_xi(rho) * 0 + q.ev(q.xi @ q.xi, rho)), np.sqrt(q.ev(q.pi @ q.pi, rho))])
for nb in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    Nc, val, hist = converged_N(lambda N: th_vals(N, nb), rtol=TOL["converge_rtol"])
    B["thermal"].append({"nbar": nb, "N_converged": Nc, "dxi": F(val[0]), "dpi": F(val[1]),
                         "dxi_analytic": F(np.sqrt(nb + 0.5)), "dpi_minus_dxi": F(val[1] - val[0])})
fock_res = [abs(f["dpi_minus_dxi"]) for f in B["fock"]]
B["withdrawn_shadow_line"] = {"claim": "dpi = dxi + 1 for eigenstates",
                              "max_abs_dpi_minus_dxi_fock": max(fock_res),
                              "status": verdict(all(abs(f["residual_vs_withdrawn_line_dpi_eq_dxi_plus_1"]) < 1e-6 for f in B["fock"]))}
B["cross_state_relation"] = [F(o.var_pi(o.fock(n + 1)) - o.var_xi(o.fock(n))) for n in range(6)]
R["B_quadrature_map"] = B

# ---------------- C. Thermal photon-number spread ----------------
C = []
for nb in [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]:
    def fn(N, nb=nb):
        q = Oscillator(N); rho = q.thermal(nb)
        return np.array([q.ev(q.n_op, rho), q.ev(q.n_op @ q.n_op, rho), np.real(np.trace(rho)), q.ev(q.xi @ q.xi, rho)])
    Nc, v, hist = converged_N(fn, Ns=(30, 60, 100, 150, 200, 300, 400), rtol=TOL["converge_rtol"])
    mean, m2, tr, x2 = v
    sig = np.sqrt(m2 - mean ** 2); pred = np.sqrt(nb * (nb + 1))
    v30 = dict(hist)[30]; sig30 = np.sqrt(v30[1] / v30[2] - (v30[0] / v30[2]) ** 2)
    C.append({"nbar": nb, "N_converged": Nc, "tail_weight_missing": F(1 - tr), "mean_n": F(mean),
              "sigma_n": F(sig), "sigma_pred": F(pred), "rel_err": F(abs(sig - pred) / pred),
              "var_xi": F(x2), "var_xi_pred": nb + 0.5,
              "identity_check_sigma2_eq_varxi_varpi_minus_quarter": F(sig ** 2 - (x2 * x2 - 0.25)),
              "sigma_n_at_N30_renormalised": F(sig30), "rel_err_at_N30": F(abs(sig30 - pred) / pred),
              "status": verdict(abs(sig - pred) / pred < 1e-8)})
R["C_thermal_number_spread"] = C

# ---------------- D. Squeezed-vacuum decoherence (former "fixed point") ----------------
rstar = float(np.log((np.sqrt(6) + np.sqrt(2)) / 2))
D = {"r_star": rstar, "r_star_closed_form": "ln((sqrt6+sqrt2)/2) = ln(2 cos 15 deg)",
     "dxi_star": float(np.exp(-rstar) / np.sqrt(2)), "dpi_star": float(np.exp(rstar) / np.sqrt(2)),
     "dxi_star_formula": float((np.sqrt(3) - 1) / 2), "dpi_star_formula": float((np.sqrt(3) + 1) / 2),
     "gamma": 0.005, "nth": 0.1, "threshold_product": 0.55}
g, nth = D["gamma"], D["nth"]
def analytic_product(r, t):
    e = np.exp(-g * t); Vx = 0.5 * np.exp(-2 * r) * e + (nth + 0.5) * (1 - e); Vp = 0.5 * np.exp(2 * r) * e + (nth + 0.5) * (1 - e)
    return np.sqrt(Vx * Vp)
from scipy.optimize import brentq
rows = []
for r in [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, rstar, 0.7, 0.8, 0.9, 1.0, 1.2]:
    t_dep = brentq(lambda t: analytic_product(r, t) - 0.55, 1e-9, 5000)
    rows.append({"r": r, "dxi0": F(np.exp(-r) / np.sqrt(2)), "departure_time": F(t_dep)})
rows.sort(key=lambda d: d["r"])
td = [d["departure_time"] for d in rows]
D["rows"] = rows
D["monotonic_decreasing_in_r"] = bool(all(td[i] > td[i + 1] for i in range(len(td) - 1)))
# numerical check of the analytic Gaussian solution with RK4 Lindblad (N converged for r<=1)
chk = []
for r in [0.0, rstar, 1.0]:
    q = Oscillator(100); rho = q.ket_to_rho(q.squeezed_ket(r))
    st = q.lindblad_rk4(rho, g, nth, dt=0.5, steps=200, record_every=20)
    errs = [abs(np.sqrt(q.var_xi(s) * q.var_pi(s)) - analytic_product(r, 10.0 * k)) for k, s in enumerate(st)]
    chk.append({"r": r, "max_abs_err_rk4_vs_analytic": F(max(errs))})
D["rk4_check"] = chk
D["rk4_status"] = verdict(max(c["max_abs_err_rk4_vs_analytic"] for c in chk) < TOL["lindblad_vs_analytic"])
# local smoothness at r*: compare departure time with interpolation of neighbours
i = [d["r"] for d in rows].index(rstar)
interp = np.interp(rstar, [rows[i - 1]["r"], rows[i + 1]["r"]], [rows[i - 1]["departure_time"], rows[i + 1]["departure_time"]])
D["t_dep_rstar"] = rows[i]["departure_time"]; D["t_dep_linear_interp_neighbours"] = float(interp)
D["status"] = "NULL (no feature at r*)" if D["monotonic_decreasing_in_r"] else "FEATURE?"
R["D_squeezed_decoherence"] = D

# ---------------- E. Anharmonic (Duffing) control ----------------
E = {}
for lam in [0.0, 0.01, 0.05, 0.1]:
    res = {}
    for N in (40, 120):
        q = Oscillator(N); X2 = q.xi @ q.xi; P2 = np.real(q.pi @ q.pi)
        H = np.diag(np.arange(N) + 0.5) + lam * X2 @ X2
        wv, V = np.linalg.eigh(H)
        vx = [F(V[:, k] @ X2 @ V[:, k]) for k in range(7)]; vp = [F(V[:, k] @ P2 @ V[:, k]) for k in range(7)]
        res[N] = {"x_steps": list(np.diff(vx)), "p_steps": list(np.diff(vp)), "energies": [F(e) for e in wv[:7]]}
    E[str(lam)] = {"x_steps": res[120]["x_steps"], "p_steps": res[120]["p_steps"],
                   "energy_gaps": list(np.diff(res[120]["energies"])),
                   "basis_change_40_to_120": F(np.max(np.abs(np.array(res[40]["x_steps"]) - np.array(res[120]["x_steps"])))),
                   "unit_step_holds": bool(max(abs(s - 1) for s in res[120]["x_steps"]) < 1e-9)}
R["E_anharmonic_control"] = E

# ---------------- F. ML Identity family ----------------
a, b, n = sp.symbols("a b n")
forms = {
 "F1  a + a^2 + b = b^2": (a + a**2 + b) - b**2,
 "F2  b^2 - a^2 = a + b": (b**2 - a**2) - (a + b),
 "F3  a*b = a^2 + a": a*b - (a**2 + a),
 "F4  (b - a)^2 = 1": (b - a)**2 - 1,
 "F5  a^2 + b^2 = 2ab + 1": a**2 + b**2 - 2*a*b - 1,
 "F6  b^2 = a^2 + (2a + 1)  [gnomon]": b**2 - a**2 - (2*a + 1),
 "F7  a*b = (a + 1/2)^2 - 1/4": a*b - ((a + sp.Rational(1, 2))**2 - sp.Rational(1, 4)),
 "F8  T_a + T_b = b^2, T_k=k(k+1)/2": a*(a+1)/2 + b*(b+1)/2 - b**2,
 "F9  8 T_a + 1 = (a + b)^2": 4*a*(a+1) + 1 - (a + b)**2,
 "F10 T_b - T_a = b": b*(b+1)/2 - a*(a+1)/2 - b,
}
Ff = {}
for k, e in forms.items():
    Ff[k] = {"expr_minus_rhs_after_b=a+1": str(sp.expand(e.subs(b, a + 1))),
             "holds_identically": bool(sp.expand(e.subs(b, a + 1)) == 0)}
Ff["F1 factorisation"] = str(sp.factor((a + a**2 + b) - b**2))
Ff["F1 solution set"] = [str(s) for s in sp.solve((a + a**2 + b) - b**2, b)]
Ff["sum of first n+1 odd numbers"] = str(sp.factor(sp.summation(2*n + 1, (n, 0, sp.Symbol('k')))))
# Fock-ladder mappings, numerically on the operator algebra
q = Oscillator(60); rungs = [F(q.ev(q.xi @ q.xi, q.fock(k))) for k in range(12)]
pairs = [[F((rungs[i] + rungs[j]) * (rungs[i] - rungs[j] + 1)) for j in range(12)] for i in range(12)]
zeros = [(i, j) for i in range(12) for j in range(12) if abs(pairs[i][j]) < 1e-9]
X2 = q.xi @ q.xi; P2 = np.real(q.pi @ q.pi)
mapping = {
 "rungs_var_xi_n": rungs,
 "F1_on_rung_pairs_zero_set": zeros,
 "F1_zero_only_for_adjacent_rungs": all(j == i + 1 for i, j in zeros),
 "sum_rungs_0..n_equals_(n+1)^2/2": [F(sum(rungs[:k + 1]) - (k + 1) ** 2 / 2) for k in range(10)],
 "varxi_varpi_minus_quarter_equals_n(n+1)": [F(q.var_xi(q.fock(k)) * q.var_pi(q.fock(k)) - 0.25 - k * (k + 1)) for k in range(10)],
 "Var(xi^2)_n_equals_T_n_plus_half": [F(q.ev(X2 @ X2, q.fock(k)) - q.ev(X2, q.fock(k)) ** 2 - (k * (k + 1) / 2 + 0.5)) for k in range(10)],
 "<n|a^dag a a a^dag|n>_equals_n(n+1)": [F(q.ev(q.ad @ q.a @ q.a @ q.ad, q.fock(k)) - k * (k + 1)) for k in range(10)],
 "cumulative_excitation_sum_k=0..n_of_(E_k/hw - 1/2)_equals_T_n": [F(sum(range(k + 1)) - k * (k + 1) / 2) for k in range(10)],
}
mapping["max_abs_residual"] = max(max(abs(x) for x in mapping[k]) for k in mapping if isinstance(mapping[k], list) and k not in ("rungs_var_xi_n", "F1_on_rung_pairs_zero_set"))
Ff["fock_mappings"] = mapping
Ff["status"] = verdict(all(v["holds_identically"] for k, v in Ff.items() if isinstance(v, dict) and "holds_identically" in v)
                       and mapping["F1_zero_only_for_adjacent_rungs"] and mapping["max_abs_residual"] < 1e-9)
R["F_identity_family"] = Ff

# ---------------- G. Wigner function checks ----------------
xs = np.linspace(-10, 10, 401); dxg = xs[1] - xs[0]
G = {}
q = Oscillator(60)
tests = {"vacuum": q.fock(0), "fock1": q.fock(1), "fock3": q.fock(3),
         "coherent_alpha2": q.ket_to_rho(q.coherent_ket(2.0)),
         "squeezed_r0.8": q.ket_to_rho(q.squeezed_ket(0.8)), "thermal_nbar2": q.thermal(2.0)}
for k, rho in tests.items():
    W = wigner_laguerre(rho, xs, xs)
    Px = W.sum(1) * dxg; Pp = W.sum(0) * dxg
    mx = (xs * Px).sum() * dxg; mp = (xs * Pp).sum() * dxg
    G[k] = {"integral": F(W.sum() * dxg * dxg), "W00": F(wigner_laguerre(rho, [0.0], [0.0])[0, 0]),
            "min": F(W.min()), "max": F(W.max()), "mean_xi_from_W": F(mx), "mean_xi_from_rho": F(q.ev(q.xi, rho)),
            "var_xi_from_W": F(((xs - mx) ** 2 * Px).sum() * dxg), "var_xi_from_rho": F(q.var_xi(rho)),
            "var_pi_from_W": F(((xs - mp) ** 2 * Pp).sum() * dxg), "var_pi_from_rho": F(q.var_pi(rho))}
G["fock_W00_expected"] = "(-1)^n / pi in (xi,pi) units; (-1)^n * 2/pi per unit d^2 alpha"
# displaced-parity cross-check and truncation artefact
o25 = Oscillator(25); r3 = o25.fock(3); pts = np.array([-4.0, -2.0, 0.0, 1.5, 4.0])
G["parity_vs_laguerre_max_diff_pad60"] = F(np.abs(wigner_parity(o25, r3, pts, pts, pad=60) - wigner_laguerre(r3, pts, pts)).max())
G["fock3_corner_4_4"] = {"laguerre_exact": F(wigner_laguerre(r3, [4.0], [4.0])[0, 0]),
                          "parity_N25_unpadded": F(wigner_parity(o25, r3, [4.0], [4.0], pad=0)[0, 0])}
# legacy formula used in v1.0 code: (2/pi) Tr[D^dag P D rho]  -> factor 2 and mirror image
def legacy(osc, rho, x, p):
    Dm = osc.displacement((x + 1j * p) / np.sqrt(2)); Par = np.diag((-1.0) ** np.arange(osc.N))
    return F((2 / np.pi) * np.trace(Dm.conj().T @ Par @ Dm @ rho))
oc = Oscillator(30); coh = oc.ket_to_rho(oc.coherent_ket(2.0))
G["legacy_v1_formula"] = {"vacuum_W00": legacy(oc, oc.fock(0), 0, 0), "fock1_W00": legacy(oc, oc.fock(1), 0, 0),
                          "coherent_alpha2_at_xi=+2.83": legacy(oc, coh, 2 * np.sqrt(2), 0),
                          "coherent_alpha2_at_xi=-2.83": legacy(oc, coh, -2 * np.sqrt(2), 0)}
ok = all(abs(G[k]["integral"] - 1) < 2e-3 for k in tests) and abs(G["fock1"]["W00"] + 1 / np.pi) < 1e-12 and G["parity_vs_laguerre_max_diff_pad60"] < 1e-9
G["status"] = verdict(ok)
R["G_wigner"] = G

# ---------------- H. Non-harmonic comparisons (square well, hydrogen) ----------------
H = {"square_well": [], "hydrogen": []}
for nn in range(1, 7):  # infinite well on [0, L], L=1
    f = lambda x: 2 * np.sin(nn * np.pi * x) ** 2
    m1 = quad(lambda x: x * f(x), 0, 1)[0]; m2 = quad(lambda x: x * x * f(x), 0, 1)[0]
    H["square_well"].append({"n": nn, "var_x_numeric_L2": m2 - m1 ** 2, "formula_1/12-1/(2n^2pi^2)": 1 / 12 - 1 / (2 * nn ** 2 * np.pi ** 2)})
def r2_numeric(nn, l):
    rho_ = lambda r: 2 * r / nn
    norm = np.sqrt((2 / nn) ** 3 * factorial(nn - l - 1) / (2 * nn * factorial(nn + l)))
    Rf = lambda r: norm * np.exp(-r / nn) * rho_(r) ** l * genlaguerre(nn - l - 1, 2 * l + 1)(rho_(r))
    nrm = quad(lambda r: Rf(r) ** 2 * r ** 2, 0, 400)[0]
    return quad(lambda r: Rf(r) ** 2 * r ** 4, 0, 400)[0] / nrm
for nn in range(1, 6):
    for l in range(0, min(nn, 3)):
        val = r2_numeric(nn, l)
        H["hydrogen"].append({"n": nn, "l": l, "r2_numeric_a0^2": val,
                              "formula_div2": nn ** 2 * (5 * nn ** 2 + 1 - 3 * l * (l + 1)) / 2,
                              "formula_div4_v1": nn ** 2 * (5 * nn ** 2 + 1 - 3 * l * (l + 1)) / 4})
H["square_well_status"] = verdict(max(abs(d["var_x_numeric_L2"] - d["formula_1/12-1/(2n^2pi^2)"]) for d in H["square_well"]) < 1e-9)
H["hydrogen_status_div2"] = verdict(max(abs(d["r2_numeric_a0^2"] - d["formula_div2"]) / d["formula_div2"] for d in H["hydrogen"]) < 1e-6)
H["hydrogen_s_state_var_x_over_a0^2_(<r^2>/3)"] = [{"n": d["n"], "var_x": d["r2_numeric_a0^2"] / 3} for d in H["hydrogen"] if d["l"] == 0]
R["H_nonharmonic"] = H

# ---------------- I. Protocol numbers (trapped-ion, omega/2pi = 2 MHz) ----------------
hw_over_k = hbar * w / kB
I = {"hbar_omega_over_kB_K": hw_over_k, "heating_rate_phonons_per_s": 5.0, "rows": []}
for nb in [0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    I["rows"].append({"nbar": nb, "sigma_n": float(np.sqrt(nb * (nb + 1))), "T_K": float(hw_over_k / np.log1p(1 / nb)),
                      "wait_s_from_ground_at_5_per_s": nb / 5.0})
I["squeezed_table"] = [{"r": r, "dxi": float(np.exp(-r) / np.sqrt(2)), "dpi": float(np.exp(r) / np.sqrt(2))} for r in (0.5, 1.0, 1.5)]
I["thermal_P1_at_nbar0.05"] = float(0.05 / 1.05 ** 2)
I["thermal_Pge1_at_nbar0.05"] = float(0.05 / 1.05)
R["I_protocol_numbers"] = I

# ---------------- summary ----------------
R["summary"] = {
  "A unit variance step": R["A_unit_step"]["status"],
  "B squeezed states vs analytic (converged N)": verdict(all(s["status"] == "PASS" for s in B["squeezed"])),
  "B withdrawn line dpi=dxi+1 on Fock states": B["withdrawn_shadow_line"]["status"],
  "C thermal number spread": verdict(all(c["status"] == "PASS" for c in C)),
  "D squeezed decoherence (r* feature?)": D["status"],
  "D RK4 vs analytic": D["rk4_status"],
  "E anharmonic: unit step fails for lambda>0": verdict(not any(E[k]["unit_step_holds"] for k in E if k != "0.0") and E["0.0"]["unit_step_holds"]),
  "F identity family": Ff["status"],
  "G Wigner normalisation/cross-check": G["status"],
  "H square well formula": H["square_well_status"],
  "H hydrogen <r^2> (divisor 2)": H["hydrogen_status_div2"],
}
with open(os.path.join(OUT, "results.json"), "w") as fh:
    json.dump(R, fh, indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
for k, v in R["summary"].items(): print(f"{k:48s} {v}")
