"""Quick end-to-end check on one simulated data set (a few minutes).

    python scripts/00_smoke_test.py            # default: "mixed" world, h = 1
    python scripts/00_smoke_test.py --world dense --quick

Prints the loss table relative to the factor-only model and which indicators the
factor-augmented model selects, next to the true ones.
"""
import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import pandas as pd  # noqa: E402

from gar.engine import rolling_forecast  # noqa: E402
from gar.evaluation import summary_table  # noqa: E402
from gar.models import ARGARCH, FactorAugmentedQR, FactorQR, HistoricalQuantile, SparseQR  # noqa: E402
from gar.simulate import simulate  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", default="mixed", choices=["dense", "sparse", "mixed", "caseA"])
    ap.add_argument("--alpha", type=float, default=1.0, help="factor strength (1 strong, <1 weak)")
    ap.add_argument("--tail", default="specific", choices=["none", "factor", "specific"])
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--quick", action="store_true", help="smaller panel and fewer origins")
    a = ap.parse_args()

    p, t = (40, 180) if a.quick else (100, 260)
    y, x, truth = simulate(a.world, t=t, p=p, alpha=a.alpha, tail=a.tail, seed=a.seed)
    models = [HistoricalQuantile(), ARGARCH(), FactorQR(), SparseQR(), FactorAugmentedQR()]
    t0 = time.time()
    fc, sel, meta = rolling_forecast(y, x, models, horizons=(1,), taus=(0.1, 0.25, 0.5),
                                     window=120)
    print("\nrun time %.0f s, %d origins" % (time.time() - t0, fc["origin"].nunique()))

    tab = summary_table(fc, benchmark="FO-QR")
    pd.set_option("display.width", 140)
    print(tab.round(3).to_string(index=False))

    print("\ntrue sparse signals:", truth["relevant"], "| tail-only indicator:", truth["tail_indicator"])
    if len(sel):
        fa = sel[sel["model"] == "FA-QR"]
        n_or = fa["origin"].nunique()
        freq = (fa.groupby(["tau", "variable"])["origin"].nunique() / n_or).rename("freq")
        for tau, g in freq.groupby(level=0):
            top = g.droplevel(0).sort_values(ascending=False).head(8)
            print("FA-QR tau=%.2f most selected:" % tau,
                  ", ".join("%s %.0f%%" % (k, 100 * v) for k, v in top.items()))
    print("factors chosen (FO-QR):", meta[meta["model"] == "FO-QR"]["r"].value_counts().to_dict())

    out = os.path.join(ROOT, "results", "smoke")
    os.makedirs(out, exist_ok=True)
    fc.to_csv(os.path.join(out, "forecasts.csv"), index=False)
    tab.to_csv(os.path.join(out, "summary.csv"), index=False)
    print("saved to", out)


if __name__ == "__main__":
    main()
