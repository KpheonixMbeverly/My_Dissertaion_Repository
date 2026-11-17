"""Forecast evaluation: quantile loss, coverage and Diebold-Mariano tests."""
import numpy as np
import pandas as pd
from scipy import stats

from .qr import check_loss


def add_loss(fc):
    """Add pinball loss and the hit indicator 1{y < q}; rows with missing outcomes are dropped."""
    fc = fc[np.isfinite(fc["realized"])].copy()
    fc["loss"] = check_loss(fc["realized"] - fc["forecast"], fc["tau"].values)
    fc["hit"] = (fc["realized"] < fc["forecast"]).astype(float)
    return fc


def dm_test(loss_a, loss_b, h=1, lags=None):
    """Diebold-Mariano test of equal expected loss, with the Harvey-Leybourne-Newbold
    small-sample correction and a Bartlett (Newey-West) long-run variance.

    d = loss_a - loss_b; a positive mean means model b is more accurate.
    Returns (mean d, t statistic, one-sided p-value for H1: b better, two-sided p-value).
    """
    d = np.asarray(loss_a, float) - np.asarray(loss_b, float)
    d = d[np.isfinite(d)]
    t = len(d)
    if lags is None:
        lags = max(h - 1, int(np.floor(1.5 * t ** (1.0 / 3.0))))
    dbar = d.mean()
    dc = d - dbar
    lrv = dc @ dc / t
    for l in range(1, lags + 1):
        w = 1.0 - l / (lags + 1.0)
        lrv += 2.0 * w * (dc[l:] @ dc[:-l]) / t
    if lrv <= 0:
        return dbar, np.nan, np.nan, np.nan
    stat = dbar / np.sqrt(lrv / t)
    hln = np.sqrt((t + 1 - 2 * h + h * (h - 1) / t) / t)
    stat *= hln
    p_one = 1.0 - stats.t.cdf(stat, df=t - 1)
    p_two = 2.0 * (1.0 - stats.t.cdf(abs(stat), df=t - 1))
    return dbar, stat, p_one, p_two


def summary_table(fc, benchmark, lags=None):
    """Mean loss, ratio to the benchmark, DM test against the benchmark, and coverage,
    by horizon, quantile and model. Every model is scored on the same target months."""
    fc = add_loss(fc)
    out = []
    for (h, tau), g in fc.groupby(["h", "tau"]):
        wide = g.pivot_table(index="target_date", columns="model", values="loss")
        wide = wide.dropna()
        hits = g.pivot_table(index="target_date", columns="model", values="hit").loc[wide.index]
        base = wide[benchmark]
        for m in wide.columns:
            dbar, stat, p1, p2 = (np.nan,) * 4
            if m != benchmark:
                dbar, stat, p1, p2 = dm_test(base.values, wide[m].values, h, lags)
            out.append({"h": h, "tau": tau, "model": m, "n": len(wide),
                        "mean_loss": wide[m].mean(), "ratio": wide[m].mean() / base.mean(),
                        "dm_stat": stat, "p_better": p1, "p_two_sided": p2,
                        "coverage": hits[m].mean()})
    return pd.DataFrame(out)
