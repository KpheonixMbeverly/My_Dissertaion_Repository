"""Shared functions for the 70-city housing synchronisation tests (analysis plan locked 2026-11-24)."""
import io, zipfile, functools
import numpy as np, pandas as pd
from scipy import sparse
from scipy.optimize import linprog
from scipy.stats import norm, multivariate_normal

PERIODS = {'P1': ('2011-01', '2015-12'), 'P2': ('2016-01', '2021-12'), 'P3': ('2022-01', '2026-10'),
           'D1': ('2014-01', '2015-12'), 'D2': ('2022-01', '2025-12')}
# NBS four regions by province code (first two digits of city code)
REGION = {**{p: 'E' for p in (11, 12, 13, 31, 32, 33, 35, 37, 44, 46)},
          **{p: 'C' for p in (14, 34, 36, 41, 42, 43)},
          **{p: 'W' for p in (15, 45, 50, 51, 52, 53, 54, 61, 62, 63, 64, 65)},
          **{p: 'NE' for p in (21, 22, 23)}}

def load_panel(zip_path):
    """Return dict market -> DataFrame (months x 70 cities) of 100*ln(index/100)."""
    z = zipfile.ZipFile(zip_path)
    df = pd.read_csv(io.BytesIO(z.read('CME_MResidSalesPriceIndices.csv')))
    a = df[(df.Datasign == 'A') & (df.Citycode != 156)]
    out = {}
    for key, col in (('new', 'Newcommerresid'), ('sec', 'Nsecondresid')):
        w = a.pivot_table(index='Monthly', columns='Citycode', values=col).sort_index()
        out[key] = 100 * np.log(w / 100.0)
    cities = sorted(set(out['new'].columns) & set(out['sec'].columns))
    cities = [c for c in cities if out['new'].loc['2011-01':'2026-10', c].notna().all()
              and out['sec'].loc['2011-01':'2026-10', c].notna().all()]
    for k in out:
        out[k] = out[k][cities]
    return out, cities

def deseason(w):
    """Remove city-specific calendar-month effects estimated on year-demeaned data (2011-2026)."""
    x = w.loc['2011-01':'2026-10']
    yr, mon = x.index.str[:4], x.index.str[5:7]
    dm = x - x.groupby(yr).transform('mean')
    sea = dm.groupby(mon).mean()
    adj = w.copy()
    m_all = adj.index.str[5:7]
    adj = adj - sea.loc[m_all].values
    return adj

def cum3(w):
    return w.rolling(3).sum()

def region_weights(cities, exclude_region=False):
    """Row-normalised weight matrix W (N x N): f_i = sum_j W_ij y_j over other cities (optionally other regions)."""
    N = len(cities)
    reg = np.array([REGION[c // 10000] for c in cities])
    W = np.ones((N, N)) - np.eye(N)
    if exclude_region:
        W = W * (reg[:, None] != reg[None, :])
    return W / W.sum(1, keepdims=True)

# ---------- cheap statistics on a T x N array ----------
def breadth(Y):
    return float((Y < 0).mean())

def share_le(Y, c=-0.5):
    return float((Y <= c).mean())

def s_raw(Y):
    m = Y.mean(1, keepdims=True)
    return float(1 - ((Y - m) ** 2).sum() / (Y ** 2).sum())

def s_dm(Y):
    return s_raw(Y - Y.mean(0, keepdims=True))

def pc1(Y):
    sd = Y.std(0)
    keep = sd > 1e-12
    Z = (Y[:, keep] - Y[:, keep].mean(0)) / sd[keep]
    ev = np.linalg.eigvalsh(Z.T @ Z / len(Z))
    return float(ev[-1] / ev.sum())

@functools.lru_cache(maxsize=None)
def gauss_table(q_eff):
    rho = np.linspace(-0.99, 0.995, 400)
    z = norm.ppf(q_eff)
    val = np.array([multivariate_normal(mean=[0, 0], cov=[[1, r], [r, 1]]).cdf([z, z]) for r in rho]) / q_eff
    return rho, val

def _ranks(X, rng):
    J = rng.uniform(-1e-7, 1e-7, size=X.shape)  # random tie-breaking (indices have one decimal)
    return np.argsort(np.argsort(X + J, axis=0), axis=0) + 1  # 1..T

def coex(Y, F, q, rng):
    """Per-city lower/upper co-exceedance probabilities and Gaussian benchmark."""
    T = Y.shape[0]
    k = int(np.floor(q * T))
    ry, rf = _ranks(Y, rng), _ranks(F, rng)
    lowf, lowy = rf <= k, ry <= k
    upf, upy = rf > T - k, ry > T - k
    CL = (lowf & lowy).sum(0) / lowf.sum(0)
    CU = (upf & upy).sum(0) / upf.sum(0)
    zy, zf = norm.ppf(ry / (T + 1)), norm.ppf(rf / (T + 1))
    zy, zf = zy - zy.mean(0), zf - zf.mean(0)
    rho = (zy * zf).sum(0) / np.sqrt((zy ** 2).sum(0) * (zf ** 2).sum(0))
    grid, val = gauss_table(k / T)
    CG = np.interp(rho, grid, val)
    return CL, CU, CG, rho

def gaps(Y):
    q10, q50, q90 = np.quantile(Y, [0.1, 0.5, 0.9], axis=0)
    return q50 - q10, q90 - q50

# ---------- quantile regression ----------
def qreg(y, X, tau):
    n, k = X.shape
    c = np.concatenate([np.zeros(2 * k), tau * np.ones(n), (1 - tau) * np.ones(n)])
    I = sparse.identity(n, format='csr')
    A = sparse.hstack([sparse.csr_matrix(X), sparse.csr_matrix(-X), I, -I], format='csr')
    res = linprog(c, A_eq=A, b_eq=y, bounds=(0, None), method='highs')
    return res.x[:k] - res.x[k:2 * k]

def cbb_index(n, L, rng):
    starts = rng.integers(0, n, size=int(np.ceil(n / L)))
    return np.concatenate([(s + np.arange(L)) % n for s in starts])[:n]
