"""Standardisation, principal-component factors and the eigenvalue-ratio estimator of r.

Normalisation follows Bai and Ng (2002) and the slides of Wang:
    F = sqrt(T) * (first r eigenvectors of Z Z'),   B = Z'F / T,   U = Z - F B'.
"""
import numpy as np


def standardize(x):
    """Column-wise z-scores using the given sample only. Returns (z, mean, sd)."""
    x = np.asarray(x, dtype=float)
    mean = x.mean(axis=0)
    sd = x.std(axis=0)
    sd = np.where(sd > 0, sd, 1.0)
    return (x - mean) / sd, mean, sd


def _eig_desc(z):
    t = z.shape[0]
    vals, vecs = np.linalg.eigh(z @ z.T)
    order = np.argsort(vals)[::-1]
    return vals[order], vecs[:, order], t


def eigenvalue_ratio(z, r_max=8):
    """Ahn and Horenstein (2013): r = argmax_{1<=k<=r_max} lambda_k / lambda_{k+1}."""
    vals, _, _ = _eig_desc(np.asarray(z, dtype=float))
    r_max = int(min(r_max, len(vals) - 1))
    vals = np.maximum(vals, 1e-12)
    ratios = vals[:r_max] / vals[1:r_max + 1]
    return int(np.argmax(ratios) + 1)


def pca_factors(z, r):
    """Return factors F (T x r), loadings B (p x r) and idiosyncratic part U (T x p)."""
    z = np.asarray(z, dtype=float)
    if r <= 0:
        return np.zeros((z.shape[0], 0)), np.zeros((z.shape[1], 0)), z.copy()
    _, vecs, t = _eig_desc(z)
    f = np.sqrt(t) * vecs[:, :r]
    b = z.T @ f / t
    u = z - f @ b.T
    return f, b, u
