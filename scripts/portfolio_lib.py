"""Portfolio construction and estimators for the locked Part 5 plan."""

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

import hp_lib as hp
from hp_run_hetero import XNAMES, rho, strength


SIZES = (1, 2, 3, 5, 10, 20, 35, 70)
RANDOM_SIZES = SIZES[1:-1]
REGION_COUNTS = {"E": 28, "C": 16, "W": 18, "NE": 8}
WINDOWS = {
    "D": ("2021-08", "2026-10", 63),
    "U": ("2015-04", "2021-07", 76),
    "D_late": ("2022-01", "2026-10", 58),
    "QR": ("2011-02", "2026-10", 189),
    "pre": ("2011-01", "2021-07", 127),
    "R6": ("2026-05", "2026-10", 6),
}
TAUS = (0.25, 0.5, 0.75)


@dataclass
class PricePanel:
    cities: np.ndarray
    regions: np.ndarray
    dates_down: np.ndarray
    windows: dict
    y: np.ndarray
    lag: np.ndarray
    f_pre: np.ndarray
    strength_positions: np.ndarray
    features: np.ndarray
    strength_scores: np.ndarray
    names: dict
    checks: dict


def load_price_panel(zip_path, city_file):
    data, codes = hp.load_panel(zip_path)
    assert len(codes) == 70, f"Expected 70 cities, got {len(codes)}"
    cities = np.asarray(codes)
    regions = np.array([hp.REGION[c // 10000] for c in codes])
    counts = {r: int((regions == r).sum()) for r in REGION_COUNTS}
    assert counts == REGION_COUNTS, counts

    prices = data["sec"].loc["2011-01":"2026-10"]
    expected = pd.period_range("2011-01", "2026-10", freq="M").astype(str)
    assert list(prices.index) == list(expected), "Calendar months missing or duplicated"
    assert np.isfinite(prices.to_numpy()).all(), "Non-finite price changes"
    lag = prices.shift(1)
    windows = {}
    for name, (start, end, length) in WINDOWS.items():
        rows = prices.loc[start:end].to_numpy()
        assert len(rows) == length, (name, len(rows), length)
        windows[name] = rows

    down_sum = windows["D"].sum(axis=0)
    down_mean = float(windows["D"].mean(axis=1).sum())
    best, worst = int(np.argmax(down_sum)), int(np.argmin(down_sum))
    assert abs(down_mean + 27.2) <= 0.1, down_mean
    assert cities[best] == 510100 and abs(down_sum[best] + 4.8) <= 0.1, (
        cities[best], down_sum[best],
    )
    assert cities[worst] == 130200 and abs(down_sum[worst] + 39.7) <= 0.1, (
        cities[worst], down_sum[worst],
    )

    strength_data = pd.read_csv(city_file).set_index("citycode")
    assert len(strength_data) == 69 and strength_data.index.is_unique
    assert strength_data.index.isin(cities).all(), "Strength table contains an unknown city"
    positions = pd.Index(cities).get_indexer(strength_data.index)
    features = strength_data[XNAMES].to_numpy()
    scores = strength(features, np.arange(len(features)))[0]
    strength_error = float(np.max(np.abs(scores - strength_data["S"].to_numpy())))
    assert strength_error < 1e-8, ("Strength maximum absolute error", strength_error)

    w_city = hp.region_weights(codes, False)
    y = windows["QR"]
    f_check = w_city @ y.T
    factor_error = float(np.max(np.abs(leave_out_factor(y, y.T, 1) - f_check)))
    assert factor_error < 1e-12, ("Leave-one-out factor maximum absolute error", factor_error)

    checks = {
        "cities": len(codes),
        "regions": counts,
        "months": {name: len(rows) for name, rows in windows.items()},
        "mean_D_log_change": down_mean,
        "max_D_citycode": int(cities[best]),
        "max_D_log_change": float(down_sum[best]),
        "min_D_citycode": int(cities[worst]),
        "min_D_log_change": float(down_sum[worst]),
        "strength_cities": len(strength_data),
        "strength_max_error": strength_error,
        "factor_max_error": factor_error,
    }
    return PricePanel(
        cities, regions, prices.loc["2021-08":"2026-10"].index.to_numpy(),
        windows, y, lag.loc["2011-02":"2026-10"].to_numpy(),
        windows["pre"] @ w_city.T, positions, features, scores,
        strength_data["city"].to_dict(), checks,
    )


def sample_portfolios(rng, count, n, n_cities=70):
    rows = np.empty((count, n), dtype=np.uint8)
    for row in rows:
        row[:] = rng.choice(n_cities, n, replace=False)
    return rows


def sample_regions(rng, count, regions):
    groups = [np.flatnonzero(regions == name) for name in REGION_COUNTS]
    # Bootstrap position counts can fall below five in a region.
    eligible = [group for group in groups if len(group) >= 5]
    sizes = np.array([len(group) for group in eligible], dtype=float)
    choices = rng.choice(len(eligible), size=count, p=sizes / sizes.sum())
    same = np.array([rng.choice(eligible[j], 5, replace=False) for j in choices], dtype=np.uint8)

    id_by_region = {name: i for i, name in enumerate(REGION_COUNTS)}
    region_ids = np.array([id_by_region[region] for region in regions])
    if len(set(region_ids)) < 3:
        raise ValueError("Cross-region portfolios require at least three represented regions")
    cross = np.empty((count, 5), dtype=np.uint8)
    for row in cross:
        while True:
            candidate = rng.choice(len(regions), 5, replace=False)
            a, b, c, d, e = region_ids[candidate]
            if len({a, b, c, d, e}) >= 3:
                row[:] = candidate
                break
    return same, cross


def portfolio_weights(members, n_cities=70):
    count, n = members.shape
    return csr_matrix(
        (np.full(count * n, 1.0 / n),
         (np.repeat(np.arange(count), n), members.ravel())),
        shape=(count, n_cities),
    )


def cvar(loss):
    k = math.ceil(len(loss) / 10)
    return float(np.partition(loss, len(loss) - k)[-k:].mean())


def terminal_loss(log_returns):
    return -100 * np.expm1(log_returns.sum(axis=0) / 100)


def buy_hold_city_levels(log_returns):
    return np.column_stack((
        np.ones(log_returns.shape[1]), np.exp(np.cumsum(log_returns.T, axis=1) / 100),
    ))


def tails(monthly):
    k = monthly.shape[1] // 10
    high_start = monthly.shape[1] - k
    partitioned = np.partition(monthly, (k - 1, high_start), axis=1)
    es = partitioned[:, :k].mean(axis=1)
    mean = monthly.mean(axis=1)
    return es, mean - es, monthly.std(axis=1, ddof=1), partitioned[:, high_start:].mean(axis=1) - mean


class ReturnWindow:
    """Simple city returns and buy-and-hold levels for one window."""

    def __init__(self, log_returns, simulated=False):
        if simulated:
            self.monthly = log_returns.T
            gross = 1 + self.monthly / 100
            if np.any(gross <= 0):
                raise ValueError("Simulated city price became nonpositive")
            self.levels = np.column_stack((np.ones(len(gross)), np.cumprod(gross, axis=1)))
        else:
            self.levels = buy_hold_city_levels(log_returns)
            self.monthly = 100 * (self.levels[:, 1:] / self.levels[:, :-1] - 1)
        self.city_tails = tails(self.monthly)
        self.city_cvar = cvar(100 * (1 - self.levels[:, -1]))

    def statistics(self, weights, rebalance=False, include_loss=True):
        if rebalance:
            monthly = weights @ self.monthly
            terminal = np.prod(1 + monthly / 100, axis=1)
        else:
            levels = weights @ self.levels
            monthly = 100 * (levels[:, 1:] / levels[:, :-1] - 1)
            terminal = levels[:, -1]

        es, bad, sd, upper = tails(monthly)
        city_es, city_bad, city_sd, city_upper = self.city_tails
        rho_bad = retention(bad, city_bad, weights)
        rho_sd = retention(sd, city_sd, weights)
        rho_upper = retention(upper, city_upper, weights)
        out = {
            "ES": float(es.mean()),
            "delta_time": float(es.mean() - city_es.mean()),
            "rho_bad": rho_bad,
            "rho_sd": rho_sd,
            "rho_upper": rho_upper,
            "R1_raw": rho_bad - rho_sd,
            "R1_mirror": rho_upper - rho_sd,
        }
        if include_loss:
            loss = 100 * (1 - terminal)
            tail = cvar(loss)
            out.update(
                loss_mean=float(loss.mean()), loss_median=float(np.median(loss)),
                loss_p90=float(np.percentile(loss, 90)), CVaR=tail,
                delta_cross=self.city_cvar - tail,
                delta_cross_relative=(self.city_cvar - tail) / self.city_cvar,
            )
        return out


def retention(portfolio_values, city_values, weights):
    denominator = float((weights @ city_values).mean())
    return float(portfolio_values.mean()) / denominator if denominator != 0 else float("nan")


def leave_out_factor(y, own, n):
    return (y.sum(axis=1)[None, :] - n * own) / (y.shape[1] - n)


def qr_data(y, lag, weights, n):
    own = weights @ y.T
    return own, leave_out_factor(y, own, n), weights @ lag.T


def qr_design(factor, lag, split=True, use_lag=True):
    cols = [np.ones(len(factor))]
    cols.extend((np.maximum(factor, 0), np.maximum(-factor, 0)) if split else (factor,))
    if use_lag:
        cols.append(lag)
    return np.column_stack(cols)


def fit_qr(data, taus=TAUS, split=True, use_lag=True):
    fits = []
    for y, f, lag in zip(*data):
        design = qr_design(f, lag, split, use_lag)
        fits.append([hp.qreg(y, design, tau) for tau in taus])
    return np.asarray(fits)


def qr_widths(fits):
    lower, middle, upper = fits.transpose(1, 0, 2)
    return {
        "lambda_q25": -lower[:, 2],
        "lambda_q50": -middle[:, 2],
        "lambda_q75": -upper[:, 2],
        "w0": middle[:, 0] - lower[:, 0],
        "omega": middle[:, 2] - lower[:, 2],
        "beta_plus_q25": lower[:, 1],
        "beta_plus_q50": middle[:, 1],
        "beta_plus_q75": upper[:, 1],
        "w0_upper": upper[:, 0] - middle[:, 0],
        "omega_upper": upper[:, 1] - middle[:, 1],
    }


def qr_curve(widths, city_widths, weights):
    values = {name: float(value.mean()) for name, value in widths.items()}
    values["delta_omega"] = float(city_widths["omega"].mean()) - values["omega"]
    for suffix in ("", "_upper"):
        r_w = retention(widths["w0" + suffix], city_widths["w0" + suffix], weights)
        r_omega = retention(widths["omega" + suffix], city_widths["omega" + suffix], weights)
        values.update({
            "R_w" + suffix: r_w, "R_omega" + suffix: r_omega, "theta" + suffix: r_omega - r_w,
        })
    return values


def mean_width(fits):
    return fits[:, 1, 0] - fits[:, 0, 0]


def ols_beta(y, f):
    centered_f = f - f.mean(axis=0)
    centered_y = y - y.mean(axis=0)
    return (centered_f * centered_y).sum(axis=0) / (centered_f ** 2).sum(axis=0)


def h4_correlation(panel, indices, r6):
    scores = strength(panel.features, indices)[0]
    return rho(scores, r6[indices], rank=True)


def h5_correlation(beta, down_sum):
    return rho(beta, -down_sum, rank=True)
