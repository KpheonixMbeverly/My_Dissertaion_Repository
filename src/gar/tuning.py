"""Time-series cross-validation of the l1 penalty.

Validation blocks sit at the end of the estimation sample and move backwards. Each
block is fitted on observations that end `gap` periods before the block starts, so
overlapping year-on-year targets cannot leak information from the validation block.
"""
import numpy as np

from .qr import check_loss, fit_qr, lambda_max


def lambda_grid(lam_max, n_lambda=10, min_ratio=0.01):
    """Log-spaced grid from lam_max (all theta = 0) down to min_ratio * lam_max."""
    if lam_max <= 0:
        return np.array([0.0])
    return lam_max * np.logspace(0.0, np.log10(min_ratio), n_lambda)


def ts_folds(n, n_folds=3, gap=12, min_train=48):
    """Index pairs (train, valid) for blocked, forward-looking validation.

    The last n - min_train - gap observations are split into n_folds contiguous
    validation blocks; each block's training set ends `gap` observations earlier.
    """
    usable = n - min_train - gap
    if usable < n_folds:
        raise ValueError("sample too short for %d folds (n=%d)" % (n_folds, n))
    size = usable // n_folds
    folds = []
    for k in range(n_folds):
        start = n - (n_folds - k) * size
        stop = start + size
        train_end = start - gap
        folds.append((np.arange(0, train_end), np.arange(start, stop)))
    return folds


def cv_lambda(y, x_free, z_pen, tau, n_lambda=10, min_ratio=0.01, n_folds=3,
              gap=12, min_train=48):
    """Choose the penalty by time-series CV; returns (lam, lam_max, cv_losses).

    Ties go to the larger penalty (the sparser model).
    """
    y = np.asarray(y, dtype=float)
    x_free = np.asarray(x_free, dtype=float)
    z_pen = np.asarray(z_pen, dtype=float)
    lam_max = lambda_max(y, x_free, z_pen, tau)
    grid = lambda_grid(lam_max, n_lambda, min_ratio)
    folds = ts_folds(len(y), n_folds, gap, min_train)
    losses = np.zeros(len(grid))
    for tr, va in folds:
        for j, lam in enumerate(grid):
            b, th = fit_qr(y[tr], x_free[tr], tau, z_pen[tr], lam)
            pred = x_free[va] @ b + z_pen[va] @ th
            losses[j] += check_loss(y[va] - pred, tau).mean()
    losses /= len(folds)
    best = int(np.flatnonzero(losses <= losses.min() + 1e-12)[0])
    return float(grid[best]), lam_max, losses
