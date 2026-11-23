"""
Fock Variance Ladder — numerical engine (revised, v2.0)
=======================================================
M. L. McKnight, ML Innovations Research Lab (ML Innovations LLC), Pheba, MS
ml.innovation.research.lab@gmail.com

Conventions (used everywhere in the package)
--------------------------------------------
* hbar is kept explicit in the documents; the code works in oscillator units.
* x0 = sqrt(hbar/(m*omega)), p0 = sqrt(hbar*m*omega);  xi = x/x0, pi = p/p0.
* xi = (a + a^dag)/sqrt(2),  pi = (a - a^dag)/(i*sqrt(2)),  [xi, pi] = i.
* Vacuum: Var(xi) = Var(pi) = 1/2.  Heuristic bound: dxi*dpi >= 1/2.
* Wigner function in (xi, pi): W(xi,pi) = (1/pi) Tr[rho D(alpha) P D(alpha)^dag],
  alpha = (xi + i pi)/sqrt(2), P = (-1)^N.  Normalised: integral W dxi dpi = 1.
  (Equivalently W(alpha) = (2/pi) Tr[...] per unit d^2 alpha.)
* Squeeze operator S(r) = exp[r(a^2 - a^dag^2)/2]: Var(xi) = e^{-2r}/2, Var(pi) = e^{2r}/2.

AI tools assisted with code and drafting; the author reviewed and is responsible for all content.
"""
import numpy as np
from scipy.special import gammaln, eval_genlaguerre
from scipy.linalg import expm


class Oscillator:
    """Truncated Fock-space harmonic oscillator, built from ladder operators only."""

    def __init__(self, N):
        self.N = N
        self.a = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
        self.ad = self.a.T.copy()
        self.n_op = np.diag(np.arange(N, dtype=float))
        self.xi = (self.a + self.ad) / np.sqrt(2)
        self.pi = (self.a - self.ad) / (1j * np.sqrt(2))

    # ---------- states (density matrices) ----------
    def ket_to_rho(self, psi):
        psi = np.asarray(psi, dtype=complex)
        return np.outer(psi, psi.conj())

    def fock_ket(self, n):
        v = np.zeros(self.N, complex); v[n] = 1; return v

    def fock(self, n):
        return self.ket_to_rho(self.fock_ket(n))

    def coherent_ket(self, alpha):
        n = np.arange(self.N)
        logc = -abs(alpha) ** 2 / 2 - 0.5 * gammaln(n + 1)
        with np.errstate(divide="ignore"):
            c = np.exp(logc) * np.power(complex(alpha), n)
        return c

    def squeezed_ket(self, r):
        """Analytic S(r)|0>: c_{2m} = (-tanh r)^m sqrt((2m)!)/(2^m m!) / sqrt(cosh r)."""
        c = np.zeros(self.N, complex)
        m = np.arange(0, (self.N + 1) // 2)
        logmag = 0.5 * gammaln(2 * m + 1) - m * np.log(2) - gammaln(m + 1) - 0.5 * np.log(np.cosh(r))
        t = np.tanh(r)
        if t == 0:
            vals = np.where(m == 0, 1.0, 0.0)
        else:
            vals = np.exp(logmag + m * np.log(t)) * (-1.0) ** m
        c[2 * m[2 * m < self.N]] = vals[2 * m < self.N]
        return c

    def squeezed_op(self, r):
        return expm(r * (self.a @ self.a - self.ad @ self.ad) / 2)

    def displacement(self, alpha):
        return expm(alpha * self.ad - np.conj(alpha) * self.a)

    def thermal(self, nbar):
        n = np.arange(self.N)
        p = np.exp(n * np.log(nbar) - (n + 1) * np.log1p(nbar)) if nbar > 0 else (n == 0).astype(float)
        return np.diag(p).astype(complex)  # NOT renormalised: missing tail weight is reported

    # ---------- observables ----------
    @staticmethod
    def ev(op, rho):
        return np.real(np.trace(op @ rho))

    def var(self, op, rho):
        tr = np.real(np.trace(rho))
        m = self.ev(op, rho) / tr
        return self.ev(op @ op, rho) / tr - m ** 2

    def var_xi(self, rho): return self.var(self.xi, rho)
    def var_pi(self, rho): return self.var(self.pi, rho)
    def mean_n(self, rho): return self.ev(self.n_op, rho) / np.real(np.trace(rho))
    def var_n(self, rho): return self.var(self.n_op, rho)

    # ---------- dynamics ----------
    def lindblad_rk4(self, rho, gamma, nth, dt, steps, record_every=1):
        a, ad = self.a, self.ad
        ada, aad = ad @ a, a @ ad
        def L(r):
            return (gamma * (nth + 1) * (a @ r @ ad - 0.5 * (ada @ r + r @ ada))
                    + gamma * nth * (ad @ r @ a - 0.5 * (aad @ r + r @ aad)))
        out = [rho.copy()]; r = rho.copy()
        for k in range(steps):
            k1 = L(r); k2 = L(r + dt / 2 * k1); k3 = L(r + dt / 2 * k2); k4 = L(r + dt * k3)
            r = r + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            if (k + 1) % record_every == 0: out.append(r.copy())
        return out


# ---------- Wigner functions ----------
def wigner_laguerre(rho, xs, ps):
    """Exact Fock-basis Wigner function (no displacement-operator truncation).
    W(xi,pi) = sum_{m,n} rho_{mn} W_{|m><n|}(xi,pi), normalised to 1 in (xi,pi)."""
    X, P = np.meshgrid(xs, ps, indexing="ij")
    A2 = 2 * (X ** 2 + P ** 2)                      # = 4|alpha|^2
    z = np.sqrt(2) * (X + 1j * P)                   # = 2 alpha
    N = rho.shape[0]
    W = np.zeros_like(X, dtype=complex)
    keep = np.where(np.abs(rho) > 1e-14)
    pairs = set(zip(*keep))
    for (m, n) in pairs:
        if m >= n:
            k = m - n
            coef = (-1) ** n * np.exp(0.5 * (gammaln(n + 1) - gammaln(m + 1)))
            term = coef * np.conj(z) ** k * eval_genlaguerre(n, k, A2) * np.exp(-A2 / 2) / np.pi
            W += rho[m, n] * term
            if m != n:
                W += rho[n, m] * np.conj(term)
    return np.real(W)


def wigner_parity(osc, rho, xs, ps, pad=0):
    """Displaced-parity Wigner (the experimental method), W = (1/pi) Tr[rho D P D^dag].
    `pad` embeds rho in a larger Fock space so D(alpha) is not truncated."""
    N = rho.shape[0] + pad
    big = Oscillator(N)
    R = np.zeros((N, N), complex); R[:rho.shape[0], :rho.shape[0]] = rho
    Par = np.diag((-1.0) ** np.arange(N))
    W = np.zeros((len(xs), len(ps)))
    for i, x in enumerate(xs):
        for j, p in enumerate(ps):
            D = big.displacement((x + 1j * p) / np.sqrt(2))
            W[i, j] = np.real(np.trace(R @ D @ Par @ D.conj().T)) / np.pi
    return W


def converged_N(fn, Ns=(30, 60, 100, 150, 200, 300, 400), rtol=1e-9):
    """Smallest N in Ns whose value agrees with the next-larger N to rtol. Returns (N, value, history)."""
    hist = [(N, fn(N)) for N in Ns]
    for (N1, v1), (N2, v2) in zip(hist, hist[1:]):
        if np.all(np.abs(np.asarray(v1) - np.asarray(v2)) <= rtol * np.maximum(1, np.abs(np.asarray(v2)))):
            return N1, v1, hist
    return None, hist[-1][1], hist
