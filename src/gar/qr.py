"""Quantile regression solved exactly as a linear programme.

Objective (as in Wang, factor-augmented sparse quantile regression):

    min_{b, theta}  (1/n) * sum_i rho_tau(y_i - x_i'b - z_i'theta) + lam * ||theta||_1

`x` holds the unpenalised regressors (intercept, own lag, factors) and `z` the penalised
ones (idiosyncratic components or raw indicators). With lam = 0 and no `z` this is
ordinary quantile regression (Koenker and Bassett, 1978).
"""
import numpy as np
from scipy import sparse
from scipy.optimize import linprog


def check_loss(resid, tau):
    """Pinball / check loss rho_tau(u) = u * (tau - 1{u < 0}), elementwise."""
    resid = np.asarray(resid, dtype=float)
    return resid * (tau - (resid < 0))


def _feasible(res, a_eq, b_eq, bounds):
    if res is None or getattr(res, "x", None) is None or not np.all(np.isfinite(res.x)):
        return False
    viol = np.max(np.abs(a_eq @ res.x - b_eq))
    lo = np.array([-np.inf if lb is None else lb for lb, _ in bounds])
    return viol <= 1e-6 * (1.0 + np.max(np.abs(b_eq))) and bool(np.all(res.x >= lo - 1e-8))


# Older SciPy (1.7.x) ships an early HiGHS that sometimes reports "optimal for the scaled
# model" without returning a solution. Presolve is the usual trigger, so the cascade turns it
# off, switches algorithm, and finally uses SciPy's legacy interior-point solver if present.
_ATTEMPTS = (
    ("highs", {}),
    ("highs", {"presolve": False}),
    ("highs-ds", {"presolve": False}),
    ("highs-ipm", {"presolve": False}),
    ("interior-point", {"sparse": True, "tol": 1e-9}),
)


def _solve_lp(c, a_eq, b_eq, bounds):
    """Return the LP solution, or None if every attempt fails."""
    for method, opts in _ATTEMPTS:
        try:
            a = a_eq if method != "interior-point" or opts.get("sparse") else a_eq.toarray()
            res = linprog(c, A_eq=a, b_eq=b_eq, bounds=bounds, method=method, options=opts)
        except (ValueError, TypeError):     # method or option not available in this SciPy
            continue
        except Exception:                   # noqa  numerical failure inside the solver
            continue
        if res.status == 0 or _feasible(res, a_eq, b_eq, bounds):
            return res.x
    return None


def _dump_failure(y, x_free, z_pen, tau, lam):
    """Save a failing problem so it can be reproduced: results/lp_failures/*.npz"""
    import os
    import time
    d = os.path.join(os.getcwd(), "results", "lp_failures")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "lp_fail_%d.npz" % int(time.time() * 1000))
    np.savez(path, y=y, x_free=x_free, z_pen=z_pen, tau=tau, lam=lam)
    return path


def fit_qr(y, x_free, tau, z_pen=None, lam=0.0):
    """Fit a (penalised) linear quantile regression.

    Parameters
    ----------
    y : (n,) array
    x_free : (n, k) array of unpenalised regressors (include a column of ones yourself)
    tau : quantile level in (0, 1)
    z_pen : (n, p) array of penalised regressors, or None
    lam : penalty on ||theta||_1 (the loss is averaged over n)

    Returns
    -------
    b : (k,) coefficients on x_free
    theta : (p,) coefficients on z_pen (empty array if z_pen is None)

    The target is divided by its standard deviation before solving. Because the check
    loss is positively homogeneous, this rescales the whole objective (loss and penalty)
    by the same constant, so the solution is unchanged; it only improves conditioning.
    """
    y = np.asarray(y, dtype=float)
    n = y.shape[0]
    x_free = np.asarray(x_free, dtype=float).reshape(n, -1)
    k = x_free.shape[1]
    if z_pen is None:
        z_pen = np.zeros((n, 0))
    z_pen = np.asarray(z_pen, dtype=float).reshape(n, -1)
    p = z_pen.shape[1]
    scale = y.std()
    scale = scale if scale > 0 else 1.0
    ys = y / scale

    # variables: b (k, free) | theta+ (p) | theta- (p) | e+ (n) | e- (n)
    c = np.concatenate([np.zeros(k), np.full(2 * p, lam),
                        np.full(n, tau / n), np.full(n, (1.0 - tau) / n)])
    eye = sparse.identity(n, format="csr")
    blocks = [sparse.csr_matrix(x_free)]
    if p:
        zp = sparse.csr_matrix(z_pen)
        blocks += [zp, -zp]
    blocks += [eye, -eye]
    a_eq = sparse.hstack(blocks, format="csr")
    bounds = [(None, None)] * k + [(0, None)] * (2 * p + 2 * n)
    z = _solve_lp(c, a_eq, ys, bounds)
    if z is None:
        # break a possible degeneracy with a negligible, reproducible perturbation of y
        jitter = 1e-9 * np.random.default_rng(n).standard_normal(n)
        z = _solve_lp(c, a_eq, ys + jitter, bounds)
    if z is None:
        path = _dump_failure(y, x_free, z_pen, tau, lam)
        raise RuntimeError("quantile regression LP failed after all fallbacks; problem saved to %s"
                           % path)
    b = z[:k] * scale
    theta = (z[k:k + p] - z[k + p:k + 2 * p]) * scale
    return b, theta


def lambda_max(y, x_free, z_pen, tau):
    """Smallest penalty at which every theta is zero (from the KKT conditions).

    Fit the unpenalised model on x_free only; theta = 0 is optimal while
    |(1/n) z' psi| <= lam, where psi_i = tau - 1{resid_i < 0}.
    """
    y = np.asarray(y, dtype=float)
    n = y.shape[0]
    b, _ = fit_qr(y, x_free, tau)
    resid = y - np.asarray(x_free, dtype=float).reshape(n, -1) @ b
    z_pen = np.asarray(z_pen, dtype=float).reshape(n, -1)
    if z_pen.shape[1] == 0:
        return 0.0
    tol = 1e-8 * (1.0 + np.abs(y).max())
    on = np.abs(resid) <= tol                      # interpolated points: subgradient not unique
    psi = np.where(on, 0.0, tau - (resid < 0))
    # bound the contribution of interpolated points, so theta = 0 is guaranteed at lam_max
    score = np.abs(z_pen.T @ psi) / n + np.abs(z_pen[on]).sum(axis=0) * max(tau, 1 - tau) / n
    return float(score.max())
