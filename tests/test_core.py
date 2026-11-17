"""Unit tests. Run with:  python -m pytest -q"""
import numpy as np
import pandas as pd

from gar import factors as fac
from gar.engine import rolling_forecast
from gar.evaluation import dm_test
from gar.models import FactorAugmentedQR, FactorQR, HistoricalQuantile, SparseQR, ARGARCH
from gar.qr import check_loss, fit_qr, lambda_max
from gar.simulate import simulate
from gar.tuning import ts_folds


def test_check_loss():
    assert np.isclose(check_loss(2.0, 0.1), 0.2)
    assert np.isclose(check_loss(-2.0, 0.1), 1.8)


def test_intercept_only_qr_is_sample_quantile():
    rng = np.random.default_rng(0)
    y = rng.standard_normal(201)
    b, _ = fit_qr(y, np.ones((201, 1)), 0.5)
    assert np.isclose(b[0], np.median(y), atol=1e-8)


def test_qr_recovers_slope():
    rng = np.random.default_rng(1)
    x = rng.standard_normal(2000)
    y = 1.0 + 2.0 * x + rng.standard_normal(2000)
    b, _ = fit_qr(y, np.column_stack([np.ones(2000), x]), 0.5)
    assert abs(b[1] - 2.0) < 0.1


def test_scale_invariance():
    """Rescaling y by c rescales every coefficient by c (same penalty)."""
    rng = np.random.default_rng(7)
    n, p = 100, 15
    z = rng.standard_normal((n, p))
    xf = np.column_stack([np.ones(n), rng.standard_normal(n)])
    y = xf[:, 1] + z[:, 0] + rng.standard_normal(n)
    b1, t1 = fit_qr(y, xf, 0.1, z, 0.02)
    b2, t2 = fit_qr(1000.0 * y, xf, 0.1, z, 0.02)
    assert np.allclose(1000.0 * b1, b2, atol=1e-5) and np.allclose(1000.0 * t1, t2, atol=1e-5)


def test_penalty_at_lambda_max_zeroes_theta():
    rng = np.random.default_rng(2)
    n, p = 120, 30
    z = rng.standard_normal((n, p))
    y = z[:, 0] + rng.standard_normal(n)
    xf = np.ones((n, 1))
    lm = lambda_max(y, xf, z, 0.25)
    _, th = fit_qr(y, xf, 0.25, z, lm * 1.001)
    assert np.allclose(th, 0.0, atol=1e-8)
    _, th = fit_qr(y, xf, 0.25, z, lm * 0.2)
    assert abs(th[0]) > 0


def test_pca_and_eigenvalue_ratio():
    y, x, _ = simulate("dense", t=200, p=80, r=3, alpha=1.0, seed=3)
    z, _, _ = fac.standardize(x.values)
    assert fac.eigenvalue_ratio(z, 8) == 3
    f, b, u = fac.pca_factors(z, 3)
    assert f.shape == (200, 3) and b.shape == (80, 3) and u.shape == (200, 80)
    assert np.allclose(f.T @ f / 200, np.eye(3), atol=1e-8)


def test_ts_folds_respect_gap():
    for tr, va in ts_folds(108, n_folds=3, gap=12, min_train=48):
        assert tr.max() + 12 < va.min()


def test_dm_sign():
    rng = np.random.default_rng(4)
    a = rng.exponential(1.0, 200) + 0.3
    b = rng.exponential(1.0, 200)
    dbar, stat, p_one, _ = dm_test(a, b, h=1)
    assert dbar > 0 and stat > 0 and p_one < 0.05


def test_no_look_ahead():
    """Changing data after the last origin must not change any forecast."""
    y, x, _ = simulate("mixed", t=170, p=30, seed=5)
    models = [HistoricalQuantile(), FactorQR(), ARGARCH(n_sim=200),
              FactorAugmentedQR(n_lambda=4, n_folds=2, min_train=40),
              SparseQR(n_lambda=4, n_folds=2, min_train=40)]
    kw = dict(horizons=(1,), taus=(0.1, 0.5), window=120, last_origin=140, verbose=False)
    fc1, _, _ = rolling_forecast(y, x, models, **kw)
    y2, x2 = y.copy(), x.copy()
    y2.iloc[142:] += 100.0
    x2.iloc[141:] *= -5.0
    fc2, _, _ = rolling_forecast(y2, x2, models, **kw)
    assert np.allclose(fc1["forecast"].values, fc2["forecast"].values)


def test_information_set_and_missing_columns():
    y, x, _ = simulate("mixed", t=150, p=20, seed=6)
    x.iloc[:50, 0] = np.nan                       # a late starter
    m = FactorQR(columns=list(x.columns[:10]))
    fc, _, meta = rolling_forecast(y, x, [m], horizons=(1,), taus=(0.5,), window=120,
                                   last_origin=121, verbose=False)
    assert (meta["p"] == 9).all()                 # 10 chosen columns minus the late starter
    assert fc["forecast"].notna().all()


def test_solver_fallback(monkeypatch):
    """If the first solver attempts fail (as with old SciPy), later attempts take over."""
    import gar.qr as q
    real = q.linprog
    calls = {"n": 0}

    class Fail(object):
        status, x, message = 4, None, "simulated HiGHS failure"

    def flaky(*args, **kw):
        calls["n"] += 1
        if calls["n"] <= 2:
            return Fail()
        return real(*args, **kw)

    rng = np.random.default_rng(8)
    y = rng.standard_normal(101)
    monkeypatch.setattr(q, "linprog", flaky)
    b, _ = q.fit_qr(y, np.ones((101, 1)), 0.5)
    assert calls["n"] >= 3 and np.isclose(b[0], np.median(y), atol=1e-7)
