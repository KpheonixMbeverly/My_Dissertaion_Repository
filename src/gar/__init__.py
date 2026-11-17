"""Factor-augmented sparse quantile forecasting of downside risk to growth (China).

Modules
-------
qr          quantile regression as a linear programme, with an optional l1 penalty
factors     standardisation, principal components, eigenvalue-ratio choice of r
tuning      time-series cross-validation of the penalty, with a gap between blocks
garch       AR(p)-GARCH(1,1) benchmark with filtered-historical-simulation quantiles
models      the forecasting models (benchmarks, factor-only, sparse-only, factor-augmented)
engine      rolling-window pseudo out-of-sample forecasting loop
evaluation  quantile loss, coverage, Diebold-Mariano tests, summary tables
simulate    data-generating processes for the Monte Carlo study
"""
__version__ = "0.1.0"
