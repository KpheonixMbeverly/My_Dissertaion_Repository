"""Forecasting models. Each model sees one estimation window and returns quantile forecasts.

Window convention (direct h-step forecasting)
---------------------------------------------
Rows 0..W-1 of the window are months t; the forecast origin is the last row.
Training pairs use predictors at row i and the target at row i + h, for i <= W-1-h,
so nothing after the origin is used. The forecast uses predictors at row W-1.

Every model re-estimates standardisation, factors and tuning inside the window.
`columns` restricts a model to an information set (e.g. real + external indicators only),
which is how forecasts A-D of the 2x2 design are built.
"""
import numpy as np

from . import factors as fac
from . import garch
from .qr import fit_qr
from .qr import lambda_max
from .tuning import cv_lambda


class WindowData(object):
    """y: (W,) target in the window; x: (W, p) predictors; names: column names."""

    def __init__(self, y, x, names, h):
        self.y = np.asarray(y, dtype=float)
        self.x = np.asarray(x, dtype=float)
        self.names = list(names)
        self.h = int(h)


def _pairs(wd):
    """Training rows i with both y_i and y_{i+h} observed, and the origin row."""
    h, w = wd.h, len(wd.y)
    i = np.arange(0, w - h)
    ok = np.isfinite(wd.y[i]) & np.isfinite(wd.y[i + h])
    i = i[ok]
    return i, i + h


def _subset(wd, columns):
    if columns is None:
        names, x = wd.names, wd.x
    else:
        idx = [wd.names.index(c) for c in columns if c in wd.names]
        names, x = [wd.names[j] for j in idx], wd.x[:, idx]
    keep = np.all(np.isfinite(x), axis=0)          # drop series not observed in the whole window
    return [n for n, k in zip(names, keep) if k], x[:, keep]


class HistoricalQuantile(object):
    """Unconditional quantile of the target over the window (the weakest benchmark)."""
    penalised = False

    def __init__(self, name="HIST"):
        self.name = name

    def fit_predict(self, wd, taus, state):
        y = wd.y[np.isfinite(wd.y)]
        return {tau: float(np.quantile(y, tau)) for tau in taus}, {}


class ARGARCH(object):
    """AR(p)-GARCH(1,1) on the target's own history (Brownlees and Souza, 2021)."""
    penalised = False

    def __init__(self, p=2, n_sim=2000, name="AR-GARCH"):
        self.p, self.n_sim, self.name = p, n_sim, name

    def fit_predict(self, wd, taus, state):
        y = wd.y.copy()
        # a contiguous series is needed; interior gaps (e.g. January) carry the last value
        for t in range(1, len(y)):
            if not np.isfinite(y[t]):
                y[t] = y[t - 1]
        y = y[np.isfinite(y)]
        fit = garch.fit_ar_garch(y, self.p)
        return garch.forecast_quantiles(fit, wd.h, taus, self.n_sim), {}


class _QRBase(object):
    """Shared machinery for the quantile-regression models."""
    penalised = False

    def __init__(self, name, columns=None, r="er", r_max=8, own_lag=True,
                 n_lambda=10, min_ratio=0.01, n_folds=3, gap=12, min_train=48,
                 retune_every=12, cv_tau=None):
        self.name = name
        self.cv_tau = cv_tau          # None: tune at each tau; a number: tune once at that tau
        self.columns = columns
        self.r, self.r_max = r, r_max
        self.own_lag = own_lag
        self.cv = dict(n_lambda=n_lambda, min_ratio=min_ratio, n_folds=n_folds,
                       gap=gap, min_train=min_train)
        self.retune_every = retune_every

    def _design(self, wd):
        """Return (free regressors, penalised regressors, penalised names) for all W rows."""
        raise NotImplementedError

    def _n_factors(self, z):
        if self.r == "er":
            return fac.eigenvalue_ratio(z, self.r_max)
        return int(self.r)

    def _free_base(self, wd):
        cols = [np.ones(len(wd.y))]
        if self.own_lag:
            # carry the last observed value over gaps (e.g. no January release), so that an
            # origin in a gap month uses the latest published figure; training pairs with a
            # missing own lag are still dropped in _pairs
            y = wd.y.copy()
            for t in range(1, len(y)):
                if not np.isfinite(y[t]):
                    y[t] = y[t - 1]
            cols.append(y)
        return np.column_stack(cols)

    def fit_predict(self, wd, taus, state):
        x_free, z_pen, pen_names, info = self._design(wd)
        tr, tg = _pairs(wd)
        origin = len(wd.y) - 1
        y_tr = wd.y[tg]
        out, sel = {}, {}
        for tau in taus:
            if z_pen is None or z_pen.shape[1] == 0:
                b, th = fit_qr(y_tr, x_free[tr], tau)
                out[tau] = float(x_free[origin] @ b)
                continue
            tune_tau = tau if self.cv_tau is None else self.cv_tau
            key = ("ratio", tune_tau)
            need = (key not in state) or (state.get("count", 0) % self.retune_every == 0
                                          and state.get(("tuned_at", tune_tau)) != state.get("count", 0))
            if need:
                lam, lam_mx, _ = cv_lambda(y_tr, x_free[tr], z_pen[tr], tune_tau, **self.cv)
                state[key] = lam / lam_mx if lam_mx > 0 else 0.0
                state[("tuned_at", tune_tau)] = state.get("count", 0)
            lam = state[key] * lambda_max(y_tr, x_free[tr], z_pen[tr], tau)
            b, th = fit_qr(y_tr, x_free[tr], tau, z_pen[tr], lam)
            out[tau] = float(x_free[origin] @ b + z_pen[origin] @ th)
            sel[tau] = {pen_names[j]: float(th[j]) for j in np.flatnonzero(np.abs(th) > 1e-8)}
        info["selected"] = sel
        return out, info


class FactorQR(_QRBase):
    """Factor-only quantile regression (dense; theta = 0)."""

    def __init__(self, name="FO-QR", **kw):
        super(FactorQR, self).__init__(name, **kw)

    def _design(self, wd):
        names, x = _subset(wd, self.columns)
        z, _, _ = fac.standardize(x)
        r = self._n_factors(z)
        f, _, _ = fac.pca_factors(z, r)
        return np.column_stack([self._free_base(wd), f]), None, [], {"r": r, "p": len(names)}


class SparseQR(_QRBase):
    """l1-penalised quantile regression on the raw (standardised) indicators, no factors."""
    penalised = True

    def __init__(self, name="SO-QR", **kw):
        super(SparseQR, self).__init__(name, **kw)

    def _design(self, wd):
        names, x = _subset(wd, self.columns)
        z, _, _ = fac.standardize(x)
        return self._free_base(wd), z, names, {"r": 0, "p": len(names)}


class FactorAugmentedQR(_QRBase):
    """Wang's factor-augmented sparse quantile regression: factors unpenalised,
    l1 penalty on the idiosyncratic components only."""
    penalised = True

    def __init__(self, name="FA-QR", **kw):
        super(FactorAugmentedQR, self).__init__(name, **kw)

    def _design(self, wd):
        names, x = _subset(wd, self.columns)
        z, _, _ = fac.standardize(x)
        r = self._n_factors(z)
        f, _, u = fac.pca_factors(z, r)
        return np.column_stack([self._free_base(wd), f]), u, names, {"r": r, "p": len(names)}
