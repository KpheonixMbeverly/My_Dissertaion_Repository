"""Monte Carlo study: how often does each comparison give the right verdict at the
sample size of the application?

For every design (world x factor strength) and replication, one data set is simulated,
the full rolling out-of-sample exercise is run, and the loss of each model relative to
the factor-only model is stored, together with the Diebold-Mariano p-value.

    python scripts/01_monte_carlo.py --reps 2 --jobs 2           # small trial run
    python scripts/01_monte_carlo.py --reps 100 --jobs 6         # full study (hours)
    python scripts/01_monte_carlo.py --summarise                 # tables from saved runs
    python scripts/01_monte_carlo.py --rho_f 0.9 --rho_u 0.8 --rho_y 0.5 --reps 3 --jobs 4

Persistence of the simulated series is set with --rho_f (factors), --rho_u (idiosyncratic
components) and --rho_y (target's own persistence). Each setting is stored in its own
folder results/montecarlo/<tag>/ (default tag built from the three values), so runs with
different settings never mix. Results are appended after every replication; an interrupted
run can be restarted and finished replications are skipped.
"""
import argparse
import itertools
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from gar.engine import rolling_forecast  # noqa: E402
from gar.evaluation import summary_table  # noqa: E402
from gar.models import FactorAugmentedQR, FactorQR, HistoricalQuantile, SparseQR  # noqa: E402
from gar.simulate import simulate  # noqa: E402

BASE = os.path.join(ROOT, "results", "montecarlo")
OUT = BASE
FILE = os.path.join(OUT, "replications.csv")
TAUS = (0.1, 0.25, 0.5)


def set_output(tag):
    global OUT, FILE
    OUT = os.path.join(BASE, tag) if tag else BASE
    FILE = os.path.join(OUT, "replications.csv")


def one_rep(world, alpha, tail, rep, t, p, rho=(0.5, 0.3, 0.0)):
    seed = 10000 * ["dense", "sparse", "mixed", "caseA"].index(world) + int(100 * alpha) * 37 + rep
    y, x, truth = simulate(world, t=t, p=p, alpha=alpha, tail=tail, seed=seed,
                           rho_f=rho[0], rho_u=rho[1], rho_y=rho[2])
    models = [HistoricalQuantile(), FactorQR(), SparseQR(), FactorAugmentedQR()]
    fc, sel, _ = rolling_forecast(y, x, models, horizons=(1,), taus=TAUS, window=120,
                                  verbose=False)
    tab = summary_table(fc, benchmark="FO-QR")
    tab["world"], tab["alpha"], tab["tail"], tab["rep"], tab["seed"] = world, alpha, tail, rep, seed
    tab["rho_f"], tab["rho_u"], tab["rho_y"] = rho
    # selection: share of origins at which a true sparse signal is picked by FA-QR
    fa = sel[sel["model"] == "FA-QR"]
    n_or = fc["origin"].nunique()
    hit = []
    for tau in TAUS:
        s = fa[fa["tau"] == tau]
        true_share = s[s["variable"].isin(truth["relevant"])].groupby("origin").size().sum()
        size = s.groupby("origin").size().reindex(fc["origin"].unique(), fill_value=0).mean()
        hit.append({"tau": tau, "avg_selected": size,
                    "true_picked_per_origin": true_share / max(n_or, 1)})
    tab = tab.merge(pd.DataFrame(hit), on="tau", how="left")
    return tab


def done_keys():
    if not os.path.exists(FILE):
        return set()
    d = pd.read_csv(FILE, usecols=["world", "alpha", "tail", "rep"])
    return set(zip(d["world"], d["alpha"], d["tail"], d["rep"]))


def summarise():
    d = pd.read_csv(FILE)
    d = d[d["model"] != "FO-QR"]
    g = d.groupby(["world", "alpha", "tail", "tau", "model"])
    s = pd.DataFrame({
        "reps": g["rep"].nunique(),
        "mean_ratio": g["ratio"].mean(),
        "share_beats_FO": g["ratio"].apply(lambda r: (r < 1).mean()),
        "reject_10pct": g["p_better"].apply(lambda v: (v < 0.10).mean()),
        "coverage": g["coverage"].mean(),
    }).reset_index()
    s.to_csv(os.path.join(OUT, "summary.csv"), index=False)
    pd.set_option("display.width", 160)
    print(s.round(3).to_string(index=False))
    print("\nreject_10pct = share of replications in which the one-sided DM test (10%) says the "
          "model beats FO-QR.\nIn worlds where it truly should (sparse, mixed) this is power; "
          "where it should not (dense) it is size.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", default="dense,sparse,mixed,caseA")
    ap.add_argument("--alphas", default="1.0,0.6", help="factor strengths")
    ap.add_argument("--tail", default="specific", choices=["none", "factor", "specific"])
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--jobs", type=int, default=1, help="parallel processes")
    ap.add_argument("--t", type=int, default=260)
    ap.add_argument("--p", type=int, default=100)
    ap.add_argument("--rho_f", type=float, default=0.5, help="AR(1) of the factors")
    ap.add_argument("--rho_u", type=float, default=0.3, help="AR(1) of the idiosyncratic parts")
    ap.add_argument("--rho_y", type=float, default=0.0, help="own persistence of the target")
    ap.add_argument("--tag", default=None, help="output sub-folder (default: from the rho values)")
    ap.add_argument("--summarise", action="store_true")
    a = ap.parse_args()
    rho = (a.rho_f, a.rho_u, a.rho_y)
    default = (0.5, 0.3, 0.0)
    tag = a.tag if a.tag is not None else (
        "" if rho == default else "rhof%g_rhou%g_rhoy%g" % rho)
    set_output(tag)
    os.makedirs(OUT, exist_ok=True)
    print("output folder:", OUT)
    if a.summarise:
        summarise()
        return

    todo = [(w, float(al), a.tail, r) for w, al, r in itertools.product(
        a.worlds.split(","), a.alphas.split(","), range(a.reps))]
    done = done_keys()
    todo = [k for k in todo if k not in done]
    print("%d replications to run (%d already done)" % (len(todo), len(done)), flush=True)

    def save(tab):
        tab.to_csv(FILE, mode="a", header=not os.path.exists(FILE), index=False)

    t0 = time.time()
    if a.jobs > 1:
        from joblib import Parallel, delayed
        batch = max(a.jobs, 1)
        for i in range(0, len(todo), batch):
            res = Parallel(n_jobs=a.jobs)(delayed(one_rep)(*k, a.t, a.p, rho)
                                          for k in todo[i:i + batch])
            for tab in res:
                save(tab)
            print("finished %d/%d  (%.0f min)" % (min(i + batch, len(todo)), len(todo),
                                                  (time.time() - t0) / 60), flush=True)
    else:
        for i, k in enumerate(todo):
            save(one_rep(*k, a.t, a.p, rho))
            print("finished %d/%d %s  (%.0f min)" % (i + 1, len(todo), k,
                                                     (time.time() - t0) / 60), flush=True)
    summarise()


if __name__ == "__main__":
    main()
