"""Part 5: portfolio diversification across cities.

Plan: docs/analysis_plan_hp_part5_portfolio_20261127.md
Locked 2026-11-26 18:35:34 UTC, SHA-256 prefix 0fcd2687.

Usage: python scripts/hp_run_portfolio.py ZIP MODE B OUTDIR [--nport N] [--smoke]
Run points (B=0), boot_city (999), boot_time (999), bench_qr (199), boot_qr (499).
Smoke runs use B=5 and 200 random portfolios by default. Set
HP_PORTFOLIO_WORKERS to select the number of QR worker processes.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor
from contextlib import contextmanager, nullcontext
import hashlib
import json
import logging
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True

import numpy as np
import pandas as pd
import scipy

import hp_lib as hp
import portfolio_lib as p


PLAN = "analysis_plan_hp_part5_portfolio_20261127.md"
PLAN_SHA = "0fcd2687347df5e67835ec286301329637455157ec0bc49abb30a9de79910ad3"
SEED = 20261127
# Retain the unshifted seed wherever section 3, 4, or 5 specifies it.
MODE_SEED_OFFSETS = {"points": 0, "boot_city": 0, "boot_time": 1, "bench_qr": 0, "boot_qr": 0}
FULL_B = {"points": 0, "boot_city": 999, "boot_time": 999, "bench_qr": 199, "boot_qr": 499}
FULL_NPORT = 10_000
NPORT_QR = NPORT_BOOT = 2_000
NPORT_QR_BOOT = 300
N_NORMAL = 999
BLOCK = 6
CHECKPOINT = 25
LOW_MID = (0.25, 0.5)
WINDOW = {name: f"{start}–{end}" for name, (start, end, _) in p.WINDOWS.items()}
WINDOW["D_U"] = WINDOW["D"] + " / " + WINDOW["U"]
WINDOW["D_late_U"] = WINDOW["D_late"] + " / " + WINDOW["U"]
WINDOW["pre_D"] = WINDOW["pre"] + " / " + WINDOW["D"]
LOG = logging.getLogger("portfolio")


@contextmanager
def timed(timings, task):
    start = time.perf_counter()
    try:
        yield
    finally:
        timings[task] = time.perf_counter() - start
        LOG.info("%s %.3f seconds", task, timings[task])


@contextmanager
def atomic_path(path):
    temporary = path.with_name(f"{path.name}.{os.getpid()}.partial")
    try:
        yield temporary
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_json(path, obj):
    with atomic_path(path) as temporary:
        temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, data):
    compression = {"method": "gzip", "mtime": 0} if path.suffix == ".gz" else None
    with atomic_path(path) as temporary:
        if compression:
            # Using a file object keeps the temporary filename out of the gzip header.
            with temporary.open("wb") as stream:
                data.to_csv(stream, index=False, compression=compression)
        else:
            data.to_csv(temporary, index=False, encoding="utf-8")


def load_or_create_random(path, generator):
    if not path.exists():
        values = generator()
        with atomic_path(path) as temporary, temporary.open("wb") as stream:
            np.savez(stream, **values)
    with np.load(path, allow_pickle=False) as saved:
        return {name: saved[name] for name in saved.files}


def source_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def base_portfolios(panel, out, count, create):
    tmp = out / "tmp"
    names = [f"n{n}" for n in p.RANDOM_SIZES] + ["same", "cross"]
    paths = {name: tmp / f"portfolios_{name}.npy" for name in names}
    marker = tmp / "portfolios_ready.json"
    if create and not marker.exists():
        rng = np.random.default_rng(SEED + MODE_SEED_OFFSETS["points"])
        portfolios = {f"n{n}": p.sample_portfolios(rng, count, n) for n in p.RANDOM_SIZES}
        portfolios["same"], portfolios["cross"] = p.sample_regions(rng, count, panel.regions)
        for name, members in portfolios.items():
            with atomic_path(paths[name]) as temporary, temporary.open("wb") as stream:
                np.save(stream, members, allow_pickle=False)
            codes = pd.DataFrame(panel.cities[members], columns=[
                f"city_{i + 1}" for i in range(members.shape[1])
            ])
            write_csv(out / f"portfolios_{name}.csv", codes)
        write_json(marker, {"count": count, "seed": SEED})
    if not marker.exists():
        raise FileNotFoundError("Run points before the bootstrap and benchmark modes")
    portfolios = {name: np.load(path, allow_pickle=False) for name, path in paths.items()}
    portfolios["n1"] = np.arange(len(panel.cities))[:, None]
    portfolios["n70"] = np.arange(len(panel.cities))[None, :]
    return portfolios


def save_draws(out, name, count, batch):
    path = out / f"{name}_draws.csv.gz"
    rows = []
    if path.exists():
        previous = pd.read_csv(path, float_precision="round_trip")
        if len(previous) > count or list(previous["draw"]) != list(range(1, len(previous) + 1)):
            raise ValueError(f"Invalid checkpoint in {path}")
        rows = previous.to_dict("records")
        LOG.info("resuming %s at %d/%d", name, len(rows), count)
    for start in range(len(rows), count, CHECKPOINT):
        stop = min(start + CHECKPOINT, count)
        rows.extend({"draw": i + 1, **result} for i, result in enumerate(batch(start, stop), start))
        write_csv(path, pd.DataFrame(rows))
        LOG.info("%s %d/%d draws saved", name, stop, count)
    return pd.DataFrame(rows)


def statistic(name, point, n, window):
    return {"stat": name, "point": point, "n": n, "window": WINDOW[window]}


def summarize(points, draws=None):
    rows = []
    for point in points:
        row = dict(point)
        row.update(se=np.nan, lo=np.nan, hi=np.nan, mde=np.nan, p_two=np.nan, B_eff=0)
        if draws is not None:
            x = draws[point["stat"]].dropna().to_numpy()
            row["B_eff"] = len(x)
            if len(x):
                row["lo"], row["hi"] = np.percentile(x, [2.5, 97.5])
                row["p_two"] = min(1.0, 2 * min(np.mean(x <= 0), np.mean(x >= 0)))
            if len(x) > 1:
                row["se"] = x.std(ddof=1)
                row["mde"] = 2.5 * row["se"]
        rows.append(row)
    return pd.DataFrame(rows, columns=["stat", "point", "se", "lo", "hi", "mde", "p_two",
                                       "B_eff", "n", "window"])


def qr_chunk(task):
    data, taus, split, use_lag = task
    return p.fit_qr(data, taus, split, use_lag)


def qr_fit(pool, data, taus=p.TAUS, split=True, use_lag=True):
    if pool is None:
        return p.fit_qr(data, taus, split, use_lag)
    tasks = [
        (tuple(arr[i:i + 40] for arr in data), taus, split, use_lag)
        for i in range(0, len(data[0]), 40)
    ]
    return np.concatenate(list(pool.map(qr_chunk, tasks)), axis=0)


def nweights(portfolios, n, limit=None):
    return p.portfolio_weights(portfolios[f"n{n}"][:limit])


def loss_curves(window, portfolios, limit=None, rebalance=False):
    return {
        n: window.statistics(
            nweights(portfolios, n, limit if n in p.RANDOM_SIZES else None),
            rebalance=rebalance,
        )
        for n in p.SIZES
    }


def regional_returns(window, panel, portfolios, limit=None, rebalance=False):
    same, cross = portfolios["same"][:limit], portfolios["cross"][:limit]
    labeled_same = panel.regions[same[:, 0]]
    groups = {"same": same, "cross": cross}
    groups.update({region: same[labeled_same == region] for region in p.REGION_COUNTS})
    return {
        name: {**window.statistics(p.portfolio_weights(group), rebalance=rebalance),
               "count": len(group)}
        for name, group in groups.items() if len(group)
    }


def window_difference(down, up):
    return {
        "rho_bad_D": down["rho_bad"], "rho_bad_U": up["rho_bad"],
        "rho_sd_D": down["rho_sd"], "rho_sd_U": up["rho_sd"],
        "HP6_bad": down["rho_bad"] - up["rho_bad"],
        "HP6_sd": down["rho_sd"] - up["rho_sd"],
    }


def normal_r1(monthly, weights, out, count, timings):
    with timed(timings, "normal_inputs"):
        def simulate():
            rng = np.random.default_rng(SEED)
            normals = rng.multivariate_normal(
                monthly.mean(axis=0), np.cov(monthly, rowvar=False),
                size=(count, len(monthly)), check_valid="raise",
            )
            return {"returns": normals}

        normal = load_or_create_random(out / "tmp" / "r1_normal_inputs.npz", simulate)["returns"]

    def batch(start, stop):
        for sample in normal[start:stop]:
            values = p.ReturnWindow(sample, simulated=True).statistics(weights, include_loss=False)
            yield {k: values[k] for k in ("rho_bad", "rho_sd", "R1_raw")}

    with timed(timings, "normal_draws"):
        return float(save_draws(out, "r1_normal", count, batch)["R1_raw"].mean())


def hp4_hp5_points(panel, portfolios):
    down = panel.windows["D"]
    cumulative = down.cumsum(axis=0)
    low_dates = panel.dates_down[cumulative.argmin(axis=0)]
    r6 = panel.windows["R6"].sum(axis=0)[panel.strength_positions]
    rho_strength = p.rho(panel.strength_scores, r6, rank=True)
    past_low = low_dates[panel.strength_positions] != panel.dates_down[-1]
    ordered = np.argsort(panel.strength_scores, kind="stable")
    thirds = dict(zip(("weak", "middle", "strong"), [
        {"count": len(idx), "bottomed": int(past_low[idx].sum()), "share": float(past_low[idx].mean())}
        for idx in np.split(ordered, 3)
    ]))

    beta = p.ols_beta(panel.windows["pre"], panel.f_pre)
    log_change = down.sum(axis=0)
    beta_order = np.argsort(beta, kind="stable")
    deep = np.argsort(log_change, kind="stable")[:17]
    high_beta = np.argsort(-beta, kind="stable")[:17]
    overlap = len(np.intersect1d(deep, high_beta))
    low_beta = beta_order[:10]
    loss = p.terminal_loss(down)
    rule_loss = float(loss[low_beta].mean())
    random_loss = loss[portfolios["n10"]].mean(axis=1)
    rule_percentile = 100 * float((random_loss <= rule_loss).mean())
    return {
        "HP4_rho": rho_strength, "HP5_rho": p.h5_correlation(beta, log_change),
        "HP4_terciles": thirds, "HP5_overlap": overlap, "HP5_overlap_expected": 17 ** 2 / 70,
        "HP5_rule_loss": rule_loss, "HP5_rule_percentile": rule_percentile,
        "HP5_rule_cities": panel.cities[low_beta].tolist(),
        "by_city": [
            {"citycode": int(code), "city": panel.names.get(code), "beta_pre": float(slope),
             "D_log_change": float(change), "bottom_month": month,
             "bottomed": bool(month != panel.dates_down[-1])}
            for code, slope, change, month in zip(panel.cities, beta, log_change, low_dates)
        ],
        "HP4_by_city": [
            {"citycode": int(code), "S": float(score), "R6_log_change": float(change)}
            for code, score, change in zip(panel.cities[panel.strength_positions], panel.strength_scores, r6)
        ],
    }


def qr_points(panel, portfolios, pool):
    curves = {}
    comparisons = {}
    qr_data = {}
    for n in p.SIZES[:-1]:
        weights = nweights(portfolios, n, NPORT_QR)
        data = p.qr_data(panel.y, panel.lag, weights, n)
        qr_data[n] = data
        widths = p.qr_widths(qr_fit(pool, data))
        if n == 1:
            city_widths = widths
        curves[n] = p.qr_curve(widths, city_widths, weights)
        if n == 10:
            matched = {key: values[:NPORT_QR_BOOT] for key, values in widths.items()}
            comparisons["matched_300"] = p.qr_curve(
                matched, city_widths, nweights(portfolios, 10, NPORT_QR_BOOT),
            )
        LOG.info("full-window QR points for n=%d saved in memory (%d portfolios)", n, weights.shape[0])

    for n, data in qr_data.items():
        down_data = tuple(array[:, -len(panel.windows["D"]):] for array in data)
        fits = qr_fit(pool, down_data, LOW_MID, split=False)
        design = np.stack([p.qr_design(f, lag, split=False) for f, lag in zip(*down_data[1:])])
        curves[n].update({
            "D_b_q25": float(fits[:, 0, 1].mean()),
            "D_b_q50": float(fits[:, 1, 1].mean()),
            "D_fitted_width": float(np.einsum("ntk,nk->nt", design, fits[:, 1] - fits[:, 0]).mean()),
        })
    no_lag_city = p.qr_widths(qr_fit(pool, qr_data[1], use_lag=False))
    no_lag_ten = p.qr_widths(qr_fit(pool, qr_data[10], use_lag=False))
    comparisons["no_lag"] = p.qr_curve(no_lag_ten, no_lag_city, nweights(portfolios, 10, NPORT_QR))
    comparisons["regional_R_w"] = {}
    for key in ("same", "cross"):
        weights = p.portfolio_weights(portfolios[key][:NPORT_QR])
        fits = qr_fit(pool, p.qr_data(panel.y, panel.lag, weights, 5), LOW_MID)
        comparisons["regional_R_w"][key] = p.retention(p.mean_width(fits), city_widths["w0"], weights)
    return curves, comparisons


def inference_points(main, qr, regional, city, h6, centered_r1, qr_compare):
    boot_city = [statistic(f"delta_cross_n{n}", main[n]["delta_cross"], n, "D") for n in p.SIZES]
    boot_city += [
        statistic("HP3_cvar_difference", regional["cross"]["CVaR"] - regional["same"]["CVaR"], 5, "D"),
        statistic("HP4_rho", city["HP4_rho"], 69, "R6"),
        statistic("HP5_rho", city["HP5_rho"], 70, "pre_D"),
    ]
    boot_time = [statistic(f"delta_time_n{n}", main[n]["delta_time"], n, "D") for n in p.SIZES]
    boot_time += [
        statistic("R1_centered", centered_r1, 10, "D"),
        statistic("R1_mirror", main[10]["R1_mirror"], 10, "D"),
        statistic("HP4_rho_twoway", city["HP4_rho"], 69, "R6"),
        statistic("HP5_rho_twoway", city["HP5_rho"], 70, "pre_D"),
    ]
    boot_time += [statistic(name, value, 10, "D_U") for name, value in h6.items()]
    boot_qr = [statistic("HP2_omega_bar", qr[1]["omega"], 1, "QR")]
    boot_qr += [statistic(f"HP2_{key}", qr[10][key], 10, "QR")
                for key in ("R_w", "R_omega", "theta", "theta_upper")]
    return {
        "boot_city": boot_city, "boot_time": boot_time, "boot_qr": boot_qr,
        "bench_qr": [statistic("HP2_R_w_independent", qr_compare["matched_300"]["R_w"], 10, "QR")],
    }


def run_points(panel, portfolios, out, pool, timings, normal_count, metadata):
    with timed(timings, "holding_points"):
        down, up, late = (p.ReturnWindow(panel.windows[name]) for name in ("D", "U", "D_late"))
        main = loss_curves(down, portfolios)
        portfolio_means = {n: main[n]["loss_mean"] - main[1]["loss_mean"] for n in p.SIZES}
        LOG.info("mean cumulative loss differences vs all 70 single cities (pp): %s", portfolio_means)
        fixed = loss_curves(down, portfolios, NPORT_BOOT)
        alternate = loss_curves(late, portfolios)
        rebalanced = loss_curves(down, portfolios, rebalance=True)
        region = regional_returns(down, panel, portfolios)
        region_fixed = regional_returns(down, panel, portfolios, NPORT_BOOT)
        region_late = regional_returns(late, panel, portfolios)
        region_rebalanced = regional_returns(down, panel, portfolios, rebalance=True)
        h6, h6_fixed, h6_late, h6_rebalanced = [
            window_difference(down_stats, up.statistics(nweights(portfolios, 10, limit), rebalance))
            for down_stats, limit, rebalance in (
                (main[10], None, False), (fixed[10], NPORT_BOOT, False),
                (alternate[10], None, False), (rebalanced[10], None, True),
            )
        ]
        city = hp4_hp5_points(panel, portfolios)
    normal_mean = normal_r1(down.monthly.T, nweights(portfolios, 10), out, normal_count, timings)
    centered = main[10]["R1_raw"] - normal_mean
    with timed(timings, "qr_points"):
        qr, qr_compare = qr_points(panel, portfolios, pool)
    inference = inference_points(main, qr, region, city, h6, centered, qr_compare)

    points = {
        "metadata": metadata, "data_checks": {**panel.checks, "mean_L_difference": portfolio_means},
        "main": main, "fixed_prefix": fixed, "QR": qr, "QR_comparisons": qr_compare,
        "R1": {"normal_mean": normal_mean, "centered": centered, "fixed_centered": fixed[10]["R1_raw"] - normal_mean},
        "regional": region, "regional_fixed": region_fixed,
        "city": city, "HP6": h6, "HP6_fixed": h6_fixed, "inference": inference,
        "robustness": {
            "D_late": {"holding": alternate, "regional": region_late, "HP6": h6_late},
            "rebalanced": {"holding": rebalanced, "regional": region_rebalanced, "HP6": h6_rebalanced},
        },
    }
    write_json(out / "points.json", points)
    write_csv(out / "curves.csv", pd.DataFrame([
        {"n": n, **main[n], **qr.get(n, {})} for n in p.SIZES
    ]))
    point_rows = {}
    for mode in inference.values():
        point_rows.update({entry["stat"]: entry for entry in mode})
    for label, curves, window in (
        ("D", main, "D"), ("D_prefix", fixed, "D"),
        ("D_late", alternate, "D_late"), ("rebalanced", rebalanced, "D"), ("QR", qr, "QR"),
    ):
        for n, values in curves.items():
            for name, value in values.items():
                period = "D" if name.startswith("D_") else window
                tag = f"{label}.{name}_n{n}"
                point_rows[tag] = statistic(tag, value, n, period)
    for label, values, n, window in (
        ("QR_prefix300", qr_compare["matched_300"], 10, "QR"),
        ("QR_nolag", qr_compare["no_lag"], 10, "QR"),
        ("HP3_R_w", qr_compare["regional_R_w"], 5, "QR"),
        ("R1", points["R1"], 10, "D"),
        ("HP6_prefix", h6_fixed, 10, "D_U"),
        ("HP6_late", h6_late, 10, "D_late_U"),
        ("HP6_rebalanced", h6_rebalanced, 10, "D_U"),
    ):
        for name, value in values.items():
            tag = f"{label}.{name}"
            point_rows[tag] = statistic(tag, value, n, window)
    for label, groups, window in (
        ("regional", region, "D"), ("regional_prefix", region_fixed, "D"),
        ("regional_late", region_late, "D_late"), ("regional_rebalanced", region_rebalanced, "D"),
    ):
        for group, values in groups.items():
            for name in ("CVaR", "ES", "count"):
                tag = f"{label}.{group}.{name}"
                point_rows[tag] = statistic(tag, values[name], 5, window)
    for name in ("HP5_overlap", "HP5_overlap_expected", "HP5_rule_loss", "HP5_rule_percentile"):
        point_rows[name] = statistic(name, city[name], 10 if "_rule_" in name else 70, "pre_D")
    for name, group in city["HP4_terciles"].items():
        tag = f"HP4_bottomed_share.{name}"
        point_rows[tag] = statistic(tag, group["share"], group["count"], "D")
    write_csv(out / "points.csv", summarize(point_rows.values()))


def city_inputs(panel, count, nport, rng):
    indices_70 = np.empty((count, 70), dtype=np.uint8)
    indices_69 = np.empty((count, 69), dtype=np.uint8)
    members = {f"n{n}": np.empty((count, nport, n), dtype=np.uint8) for n in p.RANDOM_SIZES}
    members["same"] = np.empty((count, nport, 5), dtype=np.uint8)
    members["cross"] = np.empty_like(members["same"])
    for i in range(count):
        indices_70[i] = rng.integers(0, 70, size=70)
        indices_69[i] = rng.integers(0, 69, size=69)
        for n in p.RANDOM_SIZES:
            members[f"n{n}"][i] = p.sample_portfolios(rng, nport, n)
        same, cross = p.sample_regions(rng, nport, panel.regions[indices_70[i]])
        members["same"][i], members["cross"][i] = same, cross
        if (i + 1) % 100 == 0:
            LOG.info("city bootstrap random inputs generated for %d/%d draws", i + 1, count)
    return {"indices_70": indices_70, "indices_69": indices_69, **members}


def boot_city(panel, out, count, nport, rng, timings):
    with timed(timings, "random_inputs"):
        draws = load_or_create_random(
            out / "tmp" / "boot_city_inputs.npz",
            lambda: city_inputs(panel, count, min(nport, NPORT_BOOT), rng),
        )
    loss = p.terminal_loss(panel.windows["D"])
    down_sum = panel.windows["D"].sum(axis=0)
    r6 = panel.windows["R6"].sum(axis=0)[panel.strength_positions]

    def batch(start, stop):
        for i in range(start, stop):
            idx = draws["indices_70"][i]
            sampled_loss = loss[idx]
            city_tail = p.cvar(sampled_loss)
            result = {"delta_cross_n1": 0.0}
            for n in p.RANDOM_SIZES:
                result[f"delta_cross_n{n}"] = city_tail - p.cvar(
                    sampled_loss[draws[f"n{n}"][i]].mean(axis=1),
                )
            result["delta_cross_n70"] = city_tail - float(sampled_loss.mean())
            result["HP3_cvar_difference"] = (
                p.cvar(sampled_loss[draws["cross"][i]].mean(axis=1)) -
                p.cvar(sampled_loss[draws["same"][i]].mean(axis=1))
            )
            result["HP4_rho"] = p.h4_correlation(panel, draws["indices_69"][i], r6)
            beta = p.ols_beta(panel.windows["pre"][:, idx], panel.f_pre[:, idx])
            result["HP5_rho"] = p.h5_correlation(beta, down_sum[idx])
            yield result

    with timed(timings, "calculate_draws"):
        return save_draws(out, "boot_city", count, batch)


def block_inputs(panel, count, rng, names):
    return {
        name: np.array([hp.cbb_index(len(panel.windows[name]), BLOCK, rng) for _ in range(count)])
        for name in names
    }


def boot_time(panel, portfolios, out, count, rng, timings, normal_mean):
    weights = {n: nweights(portfolios, n, NPORT_BOOT) for n in p.SIZES}
    with timed(timings, "random_inputs"):
        indices = load_or_create_random(
            out / "tmp" / "boot_time_inputs.npz",
            lambda: block_inputs(panel, count, rng, ("D", "U", "pre", "R6")),
        )
        with np.load(out / "tmp" / "boot_city_inputs.npz", allow_pickle=False) as city_cache:
            city_70, city_69 = city_cache["indices_70"], city_cache["indices_69"]

    def batch(start, stop):
        for i in range(start, stop):
            y_down = panel.windows["D"][indices["D"][i]]
            y_up = panel.windows["U"][indices["U"][i]]
            down = p.ReturnWindow(y_down)
            down_results = {
                n: down.statistics(weights[n], include_loss=False)
                for n in p.SIZES
            }
            up = p.ReturnWindow(y_up).statistics(weights[10], include_loss=False)
            h6 = window_difference(down_results[10], up)

            # One length-six block is a rotation. Chronological summation preserves numerical ties.
            r6_rows = np.sort(indices["R6"][i])
            r6 = panel.windows["R6"][r6_rows].sum(axis=0)[panel.strength_positions]
            h4 = p.h4_correlation(panel, city_69[i], r6)
            pre_rows = indices["pre"][i]
            idx = city_70[i]
            beta = p.ols_beta(panel.windows["pre"][np.ix_(pre_rows, idx)], panel.f_pre[np.ix_(pre_rows, idx)])
            h5 = p.h5_correlation(beta, y_down[:, idx].sum(axis=0))
            yield {
                **{f"delta_time_n{n}": values["delta_time"] for n, values in down_results.items()},
                "R1_centered": down_results[10]["R1_raw"] - normal_mean,
                "R1_mirror": down_results[10]["R1_mirror"],
                "HP4_rho_twoway": h4, "HP5_rho_twoway": h5, **h6,
            }

    with timed(timings, "calculate_draws"):
        return save_draws(out, "boot_time", count, batch)


_qr_context = None


def qr_worker_init(context):
    global _qr_context
    _qr_context = context


def qr_boot_draw(rows):
    y, lag, one, ten = _qr_context
    ys, lags = y[rows], lag[rows]
    city = p.qr_widths(p.fit_qr(p.qr_data(ys, lags, one, 1)))
    ports = p.qr_widths(p.fit_qr(p.qr_data(ys, lags, ten, 10)))
    values = p.qr_curve(ports, city, ten)
    return {
        "HP2_omega_bar": float(city["omega"].mean()),
        **{f"HP2_{k}": values[k] for k in ("R_w", "R_omega", "theta", "theta_upper")},
    }


def qr_bench_draw(shifts):
    fitted, residual, one, ten, original_city, original_port = _qr_context
    offsets = (np.arange(residual.shape[1])[None, :] + shifts[:, None]) % residual.shape[1]
    y = fitted + np.take_along_axis(residual, offsets, axis=1)
    wc = p.mean_width(p.fit_qr((one @ y, *original_city[1:]), LOW_MID))
    wp = p.mean_width(p.fit_qr((ten @ y, *original_port[1:]), LOW_MID))
    return {"HP2_R_w_independent": p.retention(wp, wc, ten)}


def bootstrap_qr(panel, portfolios, out, mode, count, rng, workers, timings):
    one, ten = nweights(portfolios, 1), nweights(portfolios, 10, NPORT_QR_BOOT)
    is_benchmark = mode == "bench_qr"
    with timed(timings, "random_inputs"):
        def inputs():
            if is_benchmark:
                return {"shifts": rng.integers(0, len(panel.y), size=(count, len(panel.cities)))}
            return block_inputs(panel, count, rng, ("QR",))

        random = load_or_create_random(out / "tmp" / f"{mode}_inputs.npz", inputs)
    if is_benchmark:
        with timed(timings, "benchmark_median_fits"):
            original_city = p.qr_data(panel.y, panel.lag, one, 1)
            original_port = p.qr_data(panel.y, panel.lag, ten, 10)
            beta = p.fit_qr(original_city, (0.5,))[:, 0]
            fitted = np.stack([
                p.qr_design(factor, lag) @ coeff
                for factor, lag, coeff in zip(*original_city[1:], beta)
            ])
            residual = original_city[0] - fitted
            context = fitted, residual, one, ten, original_city, original_port
        task, rows = qr_bench_draw, random["shifts"]
    else:
        context = panel.y, panel.lag, one, ten
        task, rows = qr_boot_draw, random["QR"]

    # Only the parent saves checkpoints, and the map preserves input order.
    qr_worker_init(context)
    executor = ProcessPoolExecutor(workers, initializer=qr_worker_init, initargs=(context,)) if workers > 1 else nullcontext()
    with timed(timings, "calculate_draws"):
        with executor as pool:
            def batch(start, stop):
                mapper = pool.map if pool is not None else map
                return mapper(task, rows[start:stop])

            return save_draws(out, mode, count, batch)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("zip", type=Path)
    parser.add_argument("mode", choices=FULL_B)
    parser.add_argument("B", type=int)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--nport", type=int)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    required = 5 if args.smoke else FULL_B[args.mode]
    if args.B != required:
        parser.error(f"{args.mode} requires B={required} for this run")
    nport = args.nport if args.nport is not None else (200 if args.smoke else FULL_NPORT)
    if nport <= 0 or (not args.smoke and nport != FULL_NPORT):
        parser.error(f"Full execution requires nport={FULL_NPORT}")
    return args, nport


def run(args, nport, repo, timings):
    out = args.outdir.resolve()
    tmp = out / "tmp"
    mode = args.mode
    workers = int(os.environ.get("HP_PORTFOLIO_WORKERS", "1"))
    if workers < 1:
        raise ValueError("HP_PORTFOLIO_WORKERS must be positive")
    city_file = repo / "results" / "hp_hetero" / "sec_cities.csv"
    metadata = {
        "plan_sha256": PLAN_SHA,
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                     "scipy": scipy.__version__, "pandas": pd.__version__},
        "smoke": args.smoke, "nport": nport, "seed": SEED, "mode_seed_offsets": MODE_SEED_OFFSETS,
        "zip_sha256": source_hash(args.zip),
        "strength_csv_sha256": source_hash(city_file),
        "source_sha256": {
            file.name: source_hash(file)
            for file in (Path(__file__), Path(p.__file__), Path(hp.__file__), repo / "scripts" / "hp_run_hetero.py")
        },
    }
    LOG.info("mode=%s smoke=%s B=%d nport=%d QR workers=%d", mode, args.smoke, args.B, nport, workers)
    LOG.info("metadata %s", json.dumps(metadata))
    manifest = tmp / "manifest.json"
    if manifest.exists():
        if json.loads(manifest.read_text(encoding="utf-8")) != metadata:
            raise ValueError(f"Incompatible existing random inputs or checkpoint metadata: {manifest}")
    else:
        write_json(manifest, metadata)
    with timed(timings, "input_checks"):
        panel = p.load_price_panel(args.zip, city_file)
        LOG.info("data checks passed %s", json.dumps(panel.checks))
    with timed(timings, "base_portfolios"):
        portfolios = base_portfolios(panel, out, nport, create=mode == "points")
    if mode == "points":
        pool = ProcessPoolExecutor(workers) if workers > 1 else nullcontext()
        with pool as executor:
            run_points(panel, portfolios, out, executor, timings, 5 if args.smoke else N_NORMAL, metadata)
        return

    point_file = json.loads((out / "points.json").read_text(encoding="utf-8"))
    rng = np.random.default_rng(SEED + MODE_SEED_OFFSETS[mode])
    if mode == "boot_city":
        draws = boot_city(panel, out, args.B, nport, rng, timings)
    elif mode == "boot_time":
        draws = boot_time(panel, portfolios, out, args.B, rng, timings, point_file["R1"]["normal_mean"])
    else:
        draws = bootstrap_qr(panel, portfolios, out, mode, args.B, rng, workers, timings)
    write_csv(out / f"{mode}.csv", summarize(point_file["inference"][mode], draws))


def main():
    args, nport = arguments()
    repo = Path(__file__).resolve().parents[1]
    plan = repo / "docs" / PLAN
    plan_digest = hashlib.sha256(plan.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    if plan_digest != PLAN_SHA:
        raise SystemExit(f"Lock hash mismatch: expected {PLAN_SHA}, got {plan_digest}")

    out = args.outdir.resolve()
    (out / "tmp").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(out / f"{args.mode}.log", encoding="utf-8")],
    )
    LOG.info("verified plan SHA-256 %s", plan_digest)
    timings = {}
    try:
        with timed(timings, "wall"):
            run(args, nport, repo, timings)
        write_json(out / "tmp" / f"{args.mode}_timings.json", timings)
    except Exception:
        LOG.exception("Run stopped")
        raise


if __name__ == "__main__":
    main()
