"""Quantile factor analysis (Chen, Dolado & Gonzalo 2021, Econometrica) for the 70-city panel.
Plan: docs/analysis_plan_hp_part3_qfm_20261124.md (locked 2026-11-24 14:27 UTC).

One-factor model with city intercepts:  Q_tau(y_it | f_t) = a_i + b_i f_t.
Alternating exact minimisation:
  city step  (a_i, b_i | f): convex in b after profiling a out (a = ceil(tau*T)-th order statistic of y - b f);
                              golden-section search on b inside [min, max] of pairwise slopes (the optimum is a pairwise slope).
  month step (f_t | a, b):    one-parameter convex piecewise-linear problem; exact by enumerating its kinks.
"""
import numpy as np
import hp_lib as L

GR = (np.sqrt(5) - 1) / 2


def rho(u, tau):
    return u * (tau - (u < 0))


def v0(Y, tau):
    """Sum over cities of min_q sum_t rho(y_it - q): exact (q = an order statistic)."""
    T = Y.shape[0]
    k = int(np.ceil(tau * T)) - 1
    q = np.partition(Y, k, axis=0)[k]
    return float(rho(Y - q, tau).sum())


def _profile(Y, f, b, tau, k):
    R = Y - f[:, None] * b[None, :]
    a = np.partition(R, k, axis=0)[k]
    return a, rho(R - a, tau).sum(0)


def city_step(Y, f, tau, iters=80):
    T, N = Y.shape
    k = int(np.ceil(tau * T)) - 1
    s, t = np.triu_indices(T, 1)
    df = f[t] - f[s]
    ok = np.abs(df) > 1e-12
    sl = (Y[t[ok]] - Y[s[ok]]) / df[ok][:, None]
    lo, hi = sl.min(0), sl.max(0)
    x1 = hi - GR * (hi - lo); x2 = lo + GR * (hi - lo)
    _, g1 = _profile(Y, f, x1, tau, k); _, g2 = _profile(Y, f, x2, tau, k)
    for _ in range(iters):
        left = g1 <= g2
        hi = np.where(left, x2, hi); lo = np.where(left, lo, x1)
        x1 = hi - GR * (hi - lo); x2 = lo + GR * (hi - lo)
        _, g1 = _profile(Y, f, x1, tau, k); _, g2 = _profile(Y, f, x2, tau, k)
    b = np.where(g1 <= g2, x1, x2)
    a, g = _profile(Y, f, b, tau, k)
    return a, b, g


def month_step(Y, a, b, tau):
    C = Y - a[None, :]
    nz = np.abs(b) > 1e-12
    cand = C[:, nz] / b[nz][None, :]                       # (T, M)
    R = C[:, None, :] - b[None, None, :] * cand[:, :, None]  # (T, M, N)
    Lm = rho(R, tau).sum(2)
    j = Lm.argmin(1)
    r = np.arange(len(C))
    return cand[r, j], Lm[r, j]


def _std(f):
    f = f - f.mean()
    s = np.sqrt((f ** 2).mean())
    return f / s if s > 0 else f


def qfa1(Y, tau, starts, tol=1e-10, maxit=500):
    """Returns dict(a, b, f, obj, iters, start) for the start with the lowest objective."""
    best = None
    for si, f0 in enumerate(starts):
        f = _std(np.asarray(f0, float))
        prev = np.inf
        it = 0
        for it in range(1, maxit + 1):
            a, b, _ = city_step(Y, f, tau)
            f, lm = month_step(Y, a, b, tau)
            obj = lm.sum()
            if np.isfinite(prev) and prev - obj <= tol * abs(prev):
                break
            prev = obj
        a, b, lc = city_step(Y, f, tau)
        obj = float(lc.sum())
        if best is None or obj < best['obj'] - 1e-12:
            m = f.mean(); s = np.sqrt(((f - m) ** 2).mean())
            fn = (f - m) / s; bn = b * s; an = a + b * m
            if bn.mean() < 0:
                fn, bn = -fn, -bn
            best = dict(a=an, b=bn, f=fn, obj=obj, iters=it, start=si)
    return best


def pc1_start(Y):
    Z = Y - Y.mean(0)
    u, s, vt = np.linalg.svd(Z, full_matrices=False)
    return u[:, 0] * s[0]


def qfa_k(Y, tau, k, tol=1e-8, maxit=200, F0=None):
    """k-factor QFA via HiGHS LP (point estimates only). City intercept included."""
    T, N = Y.shape
    if F0 is None:
        Z = Y - Y.mean(0)
        u, s, vt = np.linalg.svd(Z, full_matrices=False)
        F = u[:, :k] * np.sqrt(T)
    else:
        F = np.asarray(F0, float)
    prev = np.inf
    for it in range(maxit):
        AB = np.array([L.qreg(Y[:, i], np.column_stack([np.ones(T), F]), tau) for i in range(N)])  # (N, k+1)
        a, B = AB[:, 0], AB[:, 1:]
        F = np.array([L.qreg(Y[t] - a, B, tau) for t in range(T)])
        obj = rho(Y - a[None, :] - F @ B.T, tau).sum()
        if np.isfinite(prev) and prev - obj <= tol * abs(prev):
            break
        prev = obj
    AB = np.array([L.qreg(Y[:, i], np.column_stack([np.ones(T), F]), tau) for i in range(N)])
    a, B = AB[:, 0], AB[:, 1:]
    obj = float(rho(Y - a[None, :] - F @ B.T, tau).sum())
    return dict(a=a, B=B, F=F, obj=obj, iters=it + 1)
