"""Data-generating processes for the Monte Carlo study.

Panel:   X_t = B f_t + u_t (+ g_t c for the weak "case A" factor)
         f_t and u_t are stationary AR(1) processes with unit variance.
Target:  y_{t+h} = mu + rho_y * y_t + f_t'gamma + u_t'theta (+ g_t delta) + s_t * eps_{t+h}
         eps is standardised Student-t; the scale s_t can depend on a factor or on one
         specific indicator, so that the lower quantiles react more than the median.

Worlds (what the target loads on):
  dense   common factors only (theta = 0)
  sparse  a few idiosyncratic components only (gamma = 0)
  mixed   both (the case the factor-augmented model is built for; "case B")
  caseA   a weak factor that loads on a small block of indicators and is missed by PCA
Factor strength: loadings are scaled by p^((alpha-1)/2); alpha = 1 strong, alpha < 1 weak.
Persistence: rho_f, rho_u (AR(1) coefficients of factors and idiosyncratic parts) and rho_y
(own persistence of the target). Year-on-year Chinese series are highly persistent, so
values around 0.9 are closer to the application than the defaults of Wang's simulations.
"""
import numpy as np
import pandas as pd


def _ar1(rng, t, k, rho, burn=100):
    e = rng.standard_normal((t + burn, k)) * np.sqrt(1.0 - rho ** 2)
    out = np.zeros_like(e)
    for s in range(1, t + burn):
        out[s] = rho * out[s - 1] + e[s]
    return out[burn:]


def simulate(world="mixed", t=260, p=100, r=3, h=1, alpha=1.0, n_sparse=5,
             signal=0.6, tail="specific", tail_strength=0.4, df=3.0,
             rho_f=0.5, rho_u=0.3, rho_y=0.0, block=10, start="2005-01", seed=None):
    """Simulate one data set. Returns (y, X, truth).

    tail: "none" (pure location shift), "factor" (scale driven by the first factor) or
          "specific" (scale driven by one idiosyncratic component that has no mean effect,
          so it matters for the tails only).
    """
    rng = np.random.default_rng(seed)
    f = _ar1(rng, t, r, rho_f)
    u = _ar1(rng, t, p, rho_u)
    load = rng.standard_normal((p, r)) * p ** ((alpha - 1.0) / 2.0)
    x = f @ load.T + u

    gamma = np.zeros(r)
    theta = np.zeros(p)
    g = np.zeros(t)
    if world in ("dense", "mixed"):
        gamma = signal * np.array([1.0, 0.6, 0.3][:r] + [0.0] * max(0, r - 3))
    if world in ("sparse", "mixed"):
        theta[rng.choice(p, n_sparse, replace=False)] = signal * 0.8
    if world == "caseA":
        g = _ar1(rng, t, 1, rho_f)[:, 0]
        blk = rng.choice(p, block, replace=False)
        x[:, blk] += g[:, None]
    if world not in ("dense", "sparse", "mixed", "caseA"):
        raise ValueError("unknown world %r" % world)

    loc = f @ gamma + u @ theta + (signal * 1.5 * g if world == "caseA" else 0.0)
    if tail == "none":
        drv, tail_var = np.zeros(t), None
    elif tail == "factor":
        drv, tail_var = -f[:, 0], None
    elif tail == "specific":
        cand = np.flatnonzero(theta == 0)
        j = int(rng.choice(cand))
        drv, tail_var = -u[:, j], j
    else:
        raise ValueError("unknown tail %r" % tail)
    scale = np.exp(tail_strength * drv - 0.5 * tail_strength ** 2)
    eps = rng.standard_t(df, size=t) / np.sqrt(df / (df - 2.0))

    y = np.full(t, np.nan)
    shock = loc[:-h] + scale[:-h] * eps[h:]          # predictable part + noise, for y_h .. y_{T-1}
    if rho_y == 0.0:
        y[h:] = 2.0 + shock
    else:
        level = 2.0 / (1.0 - rho_y)                   # unconditional mean of the AR part
        for s_ in range(h, t):
            prev = y[s_ - h] if np.isfinite(y[s_ - h]) else level
            y[s_] = 2.0 + rho_y * prev + shock[s_ - h]

    idx = pd.period_range(start=start, periods=t, freq="M").to_timestamp()
    names = ["x%03d" % (j + 1) for j in range(p)]
    truth = {"gamma": gamma, "theta": theta, "relevant": [names[j] for j in np.flatnonzero(theta)],
             "tail_indicator": None if tail_var is None else names[tail_var],
             "world": world, "alpha": alpha, "h": h,
             "rho_f": rho_f, "rho_u": rho_u, "rho_y": rho_y}
    return pd.Series(y, index=idx, name="y"), pd.DataFrame(x, index=idx, columns=names), truth
