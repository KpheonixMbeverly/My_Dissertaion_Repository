"""AR(p)-GARCH(1,1) benchmark (Brownlees and Souza, 2021), estimated on the target's own
history only. Two steps: OLS for the AR mean, Gaussian quasi-ML for the GARCH variance.
h-step quantiles come from filtered historical simulation (bootstrapping the
standardised residuals), so no distributional shape is imposed.
"""
import numpy as np
from scipy.optimize import minimize


def _garch_filter(e, omega, alpha, beta):
    n = len(e)
    s2 = np.empty(n)
    s2[0] = e.var()
    for t in range(1, n):
        s2[t] = omega + alpha * e[t - 1] ** 2 + beta * s2[t - 1]
    return s2


def _unpack(par, var_e):
    par = np.clip(par, -30.0, 30.0)
    omega = var_e * np.exp(par[0])
    persist = 1.0 / (1.0 + np.exp(-par[1]))          # alpha + beta in (0, 1)
    share = 1.0 / (1.0 + np.exp(-par[2]))            # alpha / (alpha + beta)
    return omega, persist * share, persist * (1.0 - share)


def fit_ar_garch(y, p=2):
    """Returns a dict with AR coefficients, GARCH parameters, residuals and variances."""
    y = np.asarray(y, dtype=float)
    yy = y[p:]
    xx = np.column_stack([np.ones(len(yy))] + [y[p - j:len(y) - j] for j in range(1, p + 1)])
    phi = np.linalg.lstsq(xx, yy, rcond=None)[0]
    e = yy - xx @ phi
    var_e = e.var()

    def nll(par):
        omega, alpha, beta = _unpack(par, var_e)
        s2 = _garch_filter(e, omega, alpha, beta)
        return 0.5 * np.sum(np.log(s2) + e ** 2 / s2)

    start = np.array([np.log(0.05), 2.2, -1.4])   # persistence ~0.9, alpha ~0.18
    opt = minimize(nll, start, method="Nelder-Mead",
                   options={"maxiter": 2000, "xatol": 1e-6, "fatol": 1e-8})
    omega, alpha, beta = _unpack(opt.x, var_e)
    s2 = _garch_filter(e, omega, alpha, beta)
    return {"phi": phi, "p": p, "omega": omega, "alpha": alpha, "beta": beta,
            "resid": e, "sigma2": s2, "z": e / np.sqrt(s2), "y_tail": y[-p:]}


def forecast_quantiles(fit, h, taus, n_sim=2000, seed=0):
    """Quantiles of y_{T+h} by simulating the fitted AR-GARCH forward."""
    rng = np.random.default_rng(seed)
    phi, p = fit["phi"], fit["p"]
    z = fit["z"]
    hist = np.tile(fit["y_tail"], (n_sim, 1))          # last p observations
    e_last = np.full(n_sim, fit["resid"][-1])
    s2_last = np.full(n_sim, fit["sigma2"][-1])
    for _ in range(h):
        s2 = fit["omega"] + fit["alpha"] * e_last ** 2 + fit["beta"] * s2_last
        e = np.sqrt(s2) * rng.choice(z, size=n_sim, replace=True)
        mean = phi[0] + hist[:, ::-1][:, :p] @ phi[1:]
        y_new = mean + e
        hist = np.column_stack([hist[:, 1:], y_new]) if p > 1 else y_new[:, None]
        e_last, s2_last = e, s2
    draws = hist[:, -1]
    return {tau: float(np.quantile(draws, tau)) for tau in taus}
