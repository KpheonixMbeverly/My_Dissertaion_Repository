"""Rolling-window pseudo out-of-sample forecasting.

At each origin T0 the window holds the last `window` months up to and including T0.
Each model is estimated on that window only and forecasts y_{T0+h}. The predictor panel
must already respect publication lags: row t may only contain what was released by the
end of month t (this is done when the panel is built, not here).
"""
import time

import numpy as np
import pandas as pd

from .models import WindowData


def rolling_forecast(y, x, models, horizons=(1,), taus=(0.1, 0.25, 0.5), window=120,
                     first_origin=None, last_origin=None, verbose=True):
    """Run every model over every origin.

    Parameters
    ----------
    y : pd.Series of the target, indexed by month
    x : pd.DataFrame of predictors on the same index
    models : list of model objects (see gar.models)

    Returns
    -------
    forecasts : long DataFrame (origin, target_date, h, tau, model, forecast, realized)
    selections : long DataFrame (origin, h, tau, model, variable, coef) for penalised models
    meta : DataFrame of per-origin information (number of factors, number of indicators)
    """
    if not y.index.equals(x.index):
        raise ValueError("y and x must share the same index")
    yv, xv, names, idx = y.values.astype(float), x.values.astype(float), list(x.columns), y.index
    n = len(yv)
    rows, sels, metas = [], [], []
    t_start = time.time()
    for h in horizons:
        lo = window - 1 if first_origin is None else max(first_origin, window - 1)
        hi = n - 1 - h if last_origin is None else min(last_origin, n - 1 - h)
        states = {m.name: {"count": 0} for m in models}
        for k, t0 in enumerate(range(lo, hi + 1)):
            sl = slice(t0 - window + 1, t0 + 1)
            wd = WindowData(yv[sl], xv[sl], names, h)
            realized = yv[t0 + h]
            for m in models:
                st = states[m.name]
                q, info = m.fit_predict(wd, taus, st)
                st["count"] += 1
                for tau in taus:
                    rows.append((idx[t0], idx[t0 + h], h, tau, m.name, q[tau], realized))
                for tau, chosen in info.get("selected", {}).items():
                    for var, coef in chosen.items():
                        sels.append((idx[t0], h, tau, m.name, var, coef))
                if "r" in info:
                    metas.append((idx[t0], h, m.name, info["r"], info["p"]))
            if verbose and (k % 12 == 0):
                print("h=%d origin %s (%d/%d)  %.0fs" % (h, idx[t0], k + 1, hi - lo + 1,
                                                          time.time() - t_start), flush=True)
    fc = pd.DataFrame(rows, columns=["origin", "target_date", "h", "tau", "model",
                                     "forecast", "realized"])
    sel = pd.DataFrame(sels, columns=["origin", "h", "tau", "model", "variable", "coef"])
    meta = pd.DataFrame(metas, columns=["origin", "h", "model", "r", "p"])
    return fc, sel, meta
