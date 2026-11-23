"""
Fock Variance Ladder — regenerate every figure of the revised package.
Reads ../results/results.json (written by fvl_verify.py) and recomputes Wigner grids
and convergence curves deterministically. Output: ../figures/*.png
M. L. McKnight, ML Innovations Research Lab (ML Innovations LLC), Pheba, MS
AI tools assisted with code and drafting; the author reviewed and is responsible for all content.
"""
import json, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fvl_core import Oscillator, wigner_laguerre, wigner_parity

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "..", "results", "results.json")))
FIG = os.path.join(HERE, "..", "figures"); os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.titleweight": "bold", "figure.dpi": 100})
C1, C2, C3, C4, CK = "#E8742A", "#2B6CB0", "#7B3F99", "#2F855A", "#222222"
INVPI = 1 / np.pi

def save(fig, name):
    p = os.path.join(FIG, name); fig.savefig(p, dpi=200, bbox_inches="tight"); plt.close(fig); print("saved", p)

# ---------------- panels reused in several figures ----------------
def panel_steps(ax):
    st = R["A_unit_step"]["steps"]
    ax.bar(range(len(st)), st, color=C1, edgecolor="k")
    ax.axhline(1, ls="--", c="k", lw=1)
    ax.set_ylim(0.9, 1.1); ax.set_xlabel("rung step  n → n+1"); ax.set_ylabel(r"$\Delta\langle\xi^2\rangle$")
    ax.set_title("A. Unit variance step")
    ax.text(0.5, 0.94, f"max |step−1| = {R['A_unit_step']['max_dev']:.1e}  (tol {R['A_unit_step']['tol']:.0e}): {R['A_unit_step']['status']}",
            transform=ax.transAxes, ha="center", fontsize=8)

def panel_qmap(ax, legend=True, big=False):
    B = R["B_quadrature_map"]
    x = np.linspace(0.08, 4.2, 400)
    ax.fill_between(x, 0, 1 / (2 * x), color="red", alpha=0.07, label="forbidden: δξ·δπ < 1/2")
    ax.plot(x, 1 / (2 * x), "k", lw=1.6, label="Heisenberg: δξ·δπ = 1/2")
    ax.plot(x, x, ":", c="gray", lw=1.2, label="δπ = δξ (Fock, thermal, coherent)")
    f = B["fock"]; ax.plot([d["dxi"] for d in f], [d["dpi"] for d in f], "o", c=CK, ms=6, label="Fock |n⟩, n=0–6")
    t = B["thermal"]; ax.plot([d["dxi"] for d in t], [d["dpi"] for d in t], "D", mfc="none", c=C2, ms=7, label="thermal $\\bar n$=0.1–10")
    s = [d for d in B["squeezed"]]
    ax.plot([d["dxi"] for d in s], [d["dpi"] for d in s], "o", c=C1, mec="k", ms=6, label="squeezed vacuum r=0.2–1.5 (converged N)")
    ds = B["displaced_squeezed"]; ax.plot([d["dxi"] for d in ds], [d["dpi"] for d in ds], "^", c=C4, mec="k", ms=6, label="displaced squeezed")
    ax.plot(0.7071, 0.7071, "s", c="gold", mec="k", ms=8, label="coherent |α⟩ (all α)")
    D = R["D_squeezed_decoherence"]
    ax.plot(D["dxi_star"], D["dpi_star"], "*", c="red", mec="k", ms=14, label=f"squeezed vacuum r*={D['r_star']:.4f}")
    ax.set_xlim(0, 4.2 if big else 3.5); ax.set_ylim(0, 4.2 if big else 3.5)
    ax.set_xlabel("δξ = √Var(ξ)"); ax.set_ylabel("δπ = √Var(π)"); ax.set_title("B. Quadrature-variance map")
    if legend: ax.legend(fontsize=7 if not big else 8, loc="lower right", framealpha=0.95)

def panel_thermal(ax):
    Cc = R["C_thermal_number_spread"]
    nb = np.array([d["nbar"] for d in Cc]); xx = np.linspace(0, 10.5, 200)
    ax.plot(xx, np.sqrt(xx * (xx + 1)), "k--", lw=1.2, label=r"$\sqrt{\bar n(\bar n+1)}$ (Bose–Einstein)")
    ax.plot(nb, [d["sigma_n"] for d in Cc], "o", c=C1, mec="k", label="computed, converged N")
    ax.plot(nb, [d["sigma_n_at_N30_renormalised"] for d in Cc], "x", c=C2, ms=7, label="N = 30 (v1.0 setting)")
    ax.set_xlabel(r"$\bar n$"); ax.set_ylabel(r"$\sigma_n$ (photon-number std. dev.)"); ax.legend(fontsize=7)
    ax.set_title("C. Thermal photon-number spread")

def panel_decoh(ax):
    D = R["D_squeezed_decoherence"]; rows = D["rows"]
    ax.plot([d["dxi0"] for d in rows], [d["departure_time"] for d in rows], "o-", c=C2, mec="k", ms=5)
    ax.plot(D["dxi_star"], D["t_dep_rstar"], "*", c="red", mec="k", ms=14, label=f"r* = {D['r_star']:.4f}: t = {D['t_dep_rstar']:.2f}")
    ax.set_yscale("log"); ax.set_xlabel(r"initial $\delta\xi_0 = e^{-r}/\sqrt{2}$"); ax.set_ylabel(r"time to $\delta\xi\delta\pi = 0.55$  ($1/\gamma$ = 200)")
    ax.set_title("D. Squeezed-vacuum decoherence: null"); ax.legend(fontsize=7, loc="lower right")
    ax.text(0.03, 0.92, f"γ={D['gamma']}, $\\bar n$_th={D['nth']}; monotonic: {D['monotonic_decreasing_in_r']}", transform=ax.transAxes, fontsize=7)

def panel_anh(ax):
    E = R["E_anharmonic_control"]; cols = [CK, C2, C1, C3]
    for (lam, d), c in zip(E.items(), cols):
        ax.plot(range(6), d["x_steps"], "o-", c=c, label=f"λ={lam}")
    ax.axhline(1, ls="--", c="gray", lw=1)
    ax.set_xlabel("rung step  n → n+1"); ax.set_ylabel(r"$\Delta\langle\xi^2\rangle$"); ax.legend(fontsize=7)
    ax.set_title(r"E. Control: $H=\hbar\omega(\pi^2+\xi^2)/2+\lambda\xi^4$")

def panel_idpairs(ax):
    rg = np.array(R["F_identity_family"]["fock_mappings"]["rungs_var_xi_n"])[:9]
    M = np.array([[(a + b) * (a - b + 1) for b in rg] for a in rg])
    im = ax.imshow(np.log10(np.abs(M) + 1e-3), origin="lower", cmap="viridis")
    for i in range(len(rg) - 1): ax.plot(i + 1, i, "s", mfc="none", mec="red", ms=9)
    ax.set_xlabel("rung m  (b = ⟨ξ²⟩ₘ)"); ax.set_ylabel("rung n  (a = ⟨ξ²⟩ₙ)")
    ax.set_title("F. (a+b)(a−b+1) on rung pairs")
    plt.colorbar(im, ax=ax, label="log₁₀|value| (zeros: red boxes, m=n+1)")

def wigner_grid(rho, L, npts=201):
    xs = np.linspace(-L, L, npts); return xs, wigner_laguerre(rho, xs, xs)

def panel_wigner(ax, name, rho, L, cb=True):
    xs, W = wigner_grid(rho, L)
    im = ax.pcolormesh(xs, xs, W.T, cmap="RdBu_r", vmin=-INVPI, vmax=INVPI, shading="auto")
    ax.set_aspect("equal"); ax.set_xlabel("ξ"); ax.set_ylabel("π"); ax.set_title(name)
    if cb: plt.colorbar(im, ax=ax, ticks=[-INVPI, 0, INVPI], format=lambda v, p: {-INVPI: "−1/π", 0: "0", INVPI: "1/π"}.get(v, f"{v:.2f}"), shrink=0.85)
    return W

# ---------------- Fig 1: variance ladder ----------------
fig, ax = plt.subplots(1, 3, figsize=(19, 5.4))
x = np.linspace(-4.2, 4.2, 600); ax[0].plot(x, x ** 2 / 2, "k", lw=1.5)
from numpy.polynomial.hermite import hermval
from math import factorial, pi as PI
for n in range(6):
    c = np.zeros(n + 1); c[n] = 1
    psi = hermval(x, c) * np.exp(-x ** 2 / 2) / np.sqrt(2 ** n * factorial(n) * np.sqrt(PI))
    E = n + 0.5; xt = np.sqrt(2 * E)
    ax[0].plot([-xt, xt], [E, E], c=C2, lw=1)
    ax[0].fill_between(x, E, E + 0.8 * psi ** 2, color=C1, alpha=0.6)
    ax[0].text(4.3, E, f"n={n}", va="center", fontsize=8)
ax[0].set_ylim(0, 6.6); ax[0].set_xlim(-4.2, 5.2); ax[0].set_xlabel("ξ = x/x₀"); ax[0].set_ylabel("E/ħω")
ax[0].set_title("(a) Oscillator levels and |ψₙ(ξ)|²")
rows = R["A_unit_step"]["rows"][:7]
for d in rows:
    ax[1].plot([0, 1], [d["var_xi"]] * 2, c=CK, lw=3)
    ax[1].text(1.05, d["var_xi"], f"⟨ξ²⟩ = ⟨π²⟩ = {d['var_xi']:.1f}   (|{d['n']}⟩)", va="center", fontsize=8)
for d0, d1 in zip(rows, rows[1:]):
    ax[1].annotate("", xy=(0.25, d1["var_xi"]), xytext=(0.25, d0["var_xi"]), arrowprops=dict(arrowstyle="->", color=C1, lw=1.6))
    ax[1].text(0.08, (d0["var_xi"] + d1["var_xi"]) / 2, "+1", color=C1, fontweight="bold", va="center")
ax[1].plot([0, 1], [0, 0], c="gray", lw=1, ls=":"); ax[1].set_xlim(-0.1, 2.6); ax[1].set_ylim(-0.2, 7.2); ax[1].axis("off")
ax[1].set_title("(b) Fock variance ladder: rungs n+½, spacing 1")
H = R["H_nonharmonic"]; E = R["E_anharmonic_control"]
sw = np.array([d["var_x_numeric_L2"] for d in H["square_well"]]); swst = np.diff(sw) / np.diff(sw)[0]
hy = np.array([d["var_x"] for d in H["hydrogen_s_state_var_x_over_a0^2_(<r^2>/3)"]]); hyst = np.diff(hy) / np.diff(hy)[0]
an = np.array(E["0.1"]["x_steps"]); an = an / an[0]
ax[2].plot(range(6), np.ones(6), "o-", c=CK, label="harmonic (exact 1)")
ax[2].plot(range(6), an, "s-", c=C3, label="quartic λ=0.1 (Duffing)")
ax[2].plot(range(len(swst)), swst, "^-", c=C2, label="infinite square well")
ax[2].plot(range(len(hyst)), hyst, "D-", c=C1, label="hydrogen s-states, Var(x)=⟨r²⟩/3")
ax[2].set_yscale("log"); ax[2].set_xlabel("step index (n → n+1)"); ax[2].set_ylabel("variance step / first step")
ax[2].legend(fontsize=8); ax[2].set_title("(c) Equal rungs only for the quadratic potential")
save(fig, "fig1_variance_ladder.png")

# ---------------- Fig 2: identity family (geometry) ----------------
fig, ax = plt.subplots(1, 4, figsize=(20, 5)); n = 4
def sq(a_, x0, y0, c, alpha=1): a_.add_patch(Rectangle((x0, y0), 1, 1, fc=c, ec="k", lw=0.8, alpha=alpha))
for i in range(n + 1):
    for j in range(n + 1):
        sq(ax[0], i, j, C2 if (i < n and j < n) else (C1 if i == n else "#F6AD55"))
ax[0].set_title(f"(a) Gnomon: (n+1)² = n² + n + (n+1)\n n={n}: 25 = 16 + 4 + 5")
for i in range(n + 1):
    for j in range(n + 1):
        sq(ax[1], i, j, C1 if j <= i else C2)
ax[1].set_title(f"(b) Tₙ + Tₙ₊₁ = (n+1)²\n T₄ + T₅ = 10 + 15 = 25")
for i in range(n):
    for j in range(n):
        sq(ax[2], i, j, C2)
ax[2].add_patch(Rectangle((n, 0), 0.5, n, fc=C1, ec="k"))
ax[2].add_patch(Rectangle((0, n), n, 0.5, fc=C1, ec="k"))
ax[2].add_patch(Rectangle((n, n), 0.5, 0.5, fc="white", ec="k", ls="--"))
ax[2].text(n + 0.25, n + 0.25, "¼", ha="center", va="center", fontsize=9)
ax[2].add_patch(Rectangle((0, 0), n + 0.5, n + 0.5, fc="none", ec="red", lw=2))
ax[2].set_title("(c) n(n+1) = (n+½)² − ¼\n 16 + 2 + 2 = 20 = 4.5² − ¼")
for a_ in ax[:3]:
    a_.set_xlim(-0.3, n + 1.5); a_.set_ylim(-0.3, n + 1.5); a_.set_aspect("equal"); a_.axis("off")
aa = np.linspace(-3, 8, 100)
ax[3].plot(aa, aa + 1, c=C1, lw=2, label="b = a + 1  (the ML Identity branch)")
ax[3].plot(aa, -aa, c=C2, lw=2, label="b = −a  (second root)")
rg = R["F_identity_family"]["fock_mappings"]["rungs_var_xi_n"][:7]
ax[3].plot(rg[:-1], rg[1:], "o", c=CK, label="adjacent Fock rungs (⟨ξ²⟩ₙ, ⟨ξ²⟩ₙ₊₁)")
ax[3].axhline(0, c="gray", lw=0.6); ax[3].axvline(0, c="gray", lw=0.6)
ax[3].set_xlabel("a"); ax[3].set_ylabel("b"); ax[3].legend(fontsize=7, loc="lower right")
ax[3].set_title("(d) a + a² + b − b² = (a+b)(a−b+1) = 0")
save(fig, "fig2_identity_family.png")

# ---------------- Fig 3: corrected summary ----------------
fig, ax = plt.subplots(3, 3, figsize=(16, 14)); ax = ax.ravel()
fig.suptitle("Fock Variance Ladder: Computational Verification Summary (v2.0)\nML Innovations Research Lab — M. L. McKnight", fontsize=14, fontweight="bold")
panel_steps(ax[0]); panel_qmap(ax[1]); panel_thermal(ax[2]); panel_decoh(ax[3]); panel_anh(ax[4]); panel_idpairs(ax[5])
q = Oscillator(60)
panel_wigner(ax[6], "G. Wigner: vacuum |0⟩", q.fock(0), 3.5)
panel_wigner(ax[7], "H. Wigner: Fock |3⟩", q.fock(3), 4.5)
panel_wigner(ax[8], "I. Wigner: squeezed vacuum r=0.8", q.ket_to_rho(q.squeezed_ket(0.8)), 4.5)
plt.tight_layout(rect=[0, 0, 1, 0.95]); save(fig, "fig3_summary.png")

# ---------------- Fig 4: quadrature map (large) ----------------
fig, ax = plt.subplots(1, 2, figsize=(15, 6.2))
panel_qmap(ax[0], big=True)
s = R["B_quadrature_map"]["squeezed"]
ax[1].plot([d["r"] for d in s], [d["product"] for d in s], "o-", c=C1, mec="k", label="converged N (see table)")
ax[1].plot([d["r"] for d in s], [d["N30_product"] for d in s], "x--", c=C2, ms=8, label="fixed N = 30 (v1.0): invalid for r ≥ 1.0")
ax[1].axhline(0.5, c="k", ls=":"); ax[1].set_xlabel("squeeze parameter r"); ax[1].set_ylabel("δξ·δπ"); ax[1].legend(fontsize=8)
ax[1].set_title("Squeezed vacuum stays minimum-uncertainty; N=30 truncation does not")
save(fig, "fig4_quadrature_map.png")

# ---------------- Fig 5: thermal ----------------
fig, ax = plt.subplots(1, 3, figsize=(17, 5))
panel_thermal(ax[0])
for nb, c in [(0.5, C2), (2.0, C1), (5.0, C3)]:
    k = np.arange(0, 25); P = nb ** k / (1 + nb) ** (k + 1)
    ax[1].plot(k, P, "o-", c=c, ms=4, label=f"$\\bar n$={nb}: σₙ={np.sqrt(nb*(nb+1)):.3f}")
    ax[1].errorbar(nb, P.max() * 1.08, xerr=np.sqrt(nb * (nb + 1)), fmt="|", c=c, capsize=4)
ax[1].set_xlabel("Fock rung n"); ax[1].set_ylabel("P(n) = $\\bar n$ⁿ/(1+$\\bar n$)ⁿ⁺¹"); ax[1].legend(fontsize=8)
ax[1].set_title("Rung occupation of a thermal state (bars: $\\bar n$ ± σₙ)")
Cc = R["C_thermal_number_spread"]
xv = np.array([d["var_xi"] for d in Cc]); sg = np.array([d["sigma_n"] for d in Cc])
ax[2].plot(xv ** 2 - 0.25, sg ** 2, "o", c=C1, mec="k", label="computed")
mn, mx = (xv ** 2 - 0.25).min(), (xv ** 2 - 0.25).max(); ax[2].plot([mn, mx], [mn, mx], "k--", lw=1, label="y = x")
ax[2].set_xscale("log"); ax[2].set_yscale("log")
ax[2].set_xlabel(r"$\langle\xi^2\rangle\langle\pi^2\rangle-\frac{1}{4}$"); ax[2].set_ylabel(r"$\sigma_n^2$"); ax[2].legend(fontsize=8)
ax[2].set_title("$\\bar n$($\\bar n$+1) = ($\\bar n$+½)² − ¼ for thermal states")
save(fig, "fig5_thermal.png")

# ---------------- Fig 6: decoherence ----------------
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
D = R["D_squeezed_decoherence"]; g, nth = D["gamma"], D["nth"]; t = np.linspace(0, 300, 400)
for r, c, lab in [(0, CK, "r = 0 (vacuum)"), (0.4, C2, "r = 0.4"), (D["r_star"], "red", f"r* = {D['r_star']:.4f}"), (1.0, C1, "r = 1.0")]:
    e = np.exp(-g * t); Vx = 0.5 * np.exp(-2 * r) * e + (nth + .5) * (1 - e); Vp = 0.5 * np.exp(2 * r) * e + (nth + .5) * (1 - e)
    ax[0].plot(t, np.sqrt(Vx * Vp), c=c, lw=2 if c == "red" else 1.3, label=lab)
ax[0].axhline(0.55, ls=":", c="gray"); ax[0].axhline(nth + 0.5, ls="--", c="gray", lw=0.8)
ax[0].set_xlabel("time (units of 1/ω; γ = 0.005)"); ax[0].set_ylabel("δξ·δπ"); ax[0].legend(fontsize=8)
ax[0].set_title("Uncertainty product under thermal amplitude damping (analytic; RK4-checked)")
panel_decoh(ax[1]); save(fig, "fig6_decoherence.png")

# ---------------- Fig 7: controls ----------------
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
for (lam, d), c in zip(E.items(), [CK, C2, C1, C3]):
    ax[0].plot(range(6), d["x_steps"], "o-", c=c, label=f"λ={lam}: Δ⟨ξ²⟩")
    ax[0].plot(range(6), d["p_steps"], "s--", c=c, mfc="none", label=f"λ={lam}: Δ⟨π²⟩")
ax[0].axhline(1, c="gray", lw=0.8); ax[0].set_xlabel("step n → n+1"); ax[0].set_ylabel("variance step"); ax[0].legend(fontsize=7, ncol=2)
ax[0].set_title("Quartic (Duffing) control: rungs become unequal")
hyd = H["hydrogen"]; l0 = [d for d in hyd if d["l"] == 0]
ax[1].plot([d["n"] for d in l0], [d["r2_numeric_a0^2"] for d in l0], "o", c=C1, mec="k", ms=8, label="⟨r²⟩ numeric (s states)")
nn = np.arange(1, 6); ax[1].plot(nn, nn ** 2 * (5 * nn ** 2 + 1) / 2, "k-", label="n²(5n²+1−3l(l+1))/2 (correct)")
ax[1].plot(nn, nn ** 2 * (5 * nn ** 2 + 1) / 4, "r--", label="…/4 (v1.0 text)")
ax[1].set_yscale("log"); ax[1].set_xlabel("principal quantum number n"); ax[1].set_ylabel("⟨r²⟩ / a₀²"); ax[1].legend(fontsize=8)
ax[1].set_title("Hydrogen ⟨r²⟩: corrected formula")
save(fig, "fig7_controls.png")

# ---------------- Fig 8: corrected Wigner gallery ----------------
fig, ax = plt.subplots(2, 3, figsize=(15, 9.6)); ax = ax.ravel(); q = Oscillator(80)
for a_, (nm, rho, L) in zip(ax, [("Vacuum |0⟩", q.fock(0), 3.5), ("Fock |1⟩", q.fock(1), 3.5), ("Fock |3⟩", q.fock(3), 4.5),
                                ("Coherent α = 2", q.ket_to_rho(q.coherent_ket(2.0)), 5.0), ("Squeezed vacuum r = 0.8", q.ket_to_rho(q.squeezed_ket(0.8)), 4.5),
                                ("Thermal $\\bar n$ = 2", q.thermal(2.0), 5.0)]):
    W = panel_wigner(a_, nm, rho, L)
    a_.text(0.02, 0.98, f"W(0,0) = {wigner_laguerre(rho,[0.0],[0.0])[0,0]:+.4f}\nVar ξ = {q.var_xi(rho):.4f}\nVar π = {q.var_pi(rho):.4f}",
            transform=a_.transAxes, va="top", fontsize=8, bbox=dict(fc="white", alpha=0.85))
fig.suptitle("Wigner functions in (ξ, π), normalised to 1: W = (1/π)Tr[ρ D(α) Π D†(α)], α = (ξ+iπ)/√2  (exact Fock-basis evaluation)", fontsize=11)
plt.tight_layout(rect=[0, 0, 1, 0.96]); save(fig, "fig8_wigner.png")

# ---------------- Fig 9: convergence + truncation artefact ----------------
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
Ns = [20, 30, 40, 60, 80, 100, 150, 200, 300]
for nb, c in [(1.0, C2), (3.0, C4), (5.0, C1), (10.0, C3)]:
    err = []
    for N in Ns:
        qq = Oscillator(N); rho = qq.thermal(nb); tr = np.real(np.trace(rho))
        s_ = np.sqrt(qq.ev(qq.n_op @ qq.n_op, rho) / tr - (qq.ev(qq.n_op, rho) / tr) ** 2)
        err.append(abs(s_ - np.sqrt(nb * (nb + 1))) / np.sqrt(nb * (nb + 1)) + 1e-17)
    ax[0].semilogy(Ns, err, "o-", c=c, label=f"thermal $\\bar n$={nb}: σₙ")
for r, c in [(0.8, "gray"), (1.2, CK), (1.5, "red")]:
    err = []
    for N in Ns:
        qq = Oscillator(N); rho = qq.ket_to_rho(qq.squeezed_ket(r))
        err.append(abs(np.sqrt(qq.var_xi(rho) * qq.var_pi(rho)) - 0.5) / 0.5 + 1e-17)
    ax[0].semilogy(Ns, err, "s--", c=c, label=f"squeezed r={r}: δξδπ")
ax[0].axhline(1e-9, c="k", ls=":", lw=0.8); ax[0].set_xlabel("Fock cutoff N"); ax[0].set_ylabel("relative error"); ax[0].legend(fontsize=8)
ax[0].set_title("Convergence in Fock cutoff (tolerance 1e-9 dotted)")
o25 = Oscillator(25); r3 = o25.fock(3); cut = np.linspace(0, 4.5, 46)
ax[1].plot(cut * np.sqrt(2), [wigner_laguerre(r3, [c], [c])[0, 0] for c in cut], "k-", lw=2, label="exact (Laguerre)")
ax[1].plot(cut * np.sqrt(2), [wigner_parity(o25, r3, [c], [c], pad=0)[0, 0] for c in cut], "r--", label="displaced parity, D(α) in N=25 (v1.0)")
ax[1].plot(cut * np.sqrt(2), [wigner_parity(o25, r3, [c], [c], pad=60)[0, 0] for c in cut], "o", c=C2, ms=3, label="displaced parity, D(α) in N=85")
ax[1].set_xlabel("distance from origin along ξ = π"); ax[1].set_ylabel("W  (1/π units of ξ,π)"); ax[1].legend(fontsize=8)
ax[1].set_title("Fock |3⟩: the outer 'rings' were a truncation artefact")
save(fig, "fig9_convergence.png")
