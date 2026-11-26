"""Part 3: quantile factor models (QF1-QF5). Plan locked 2026-11-24 14:27 UTC,
docs/analysis_plan_hp_part3_qfm_20261124.md (sha256 426782a6...).

usage: python hp_run_qfm.py ZIP MARKET MODE B OUT
  MODE = points | boot
"""
import sys, os, json, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hp_lib as L
import qfm_lib as Q

SEED = 20261124
PER = ('P1', 'P2', 'P3')
TIER1 = (110000, 310000, 440100, 440300)


def rows_of(w, p):
    a, b = L.PERIODS[p]
    x = w.loc[a:b]
    return x[x.notna().all(1)].values


def fit(Y, tau, starts=None):
    starts = starts if starts is not None else [Y.mean(1), Q.pc1_start(Y)]
    r = Q.qfa1(Y, tau, starts)
    r['v0'] = Q.v0(Y, tau)
    r['R1'] = 1 - r['obj'] / r['v0']
    return r


def corr(a, b):
    return float(np.corrcoef(a, b)[0, 1])


def stats_from(F, Ys):
    """F[p][tau] = fit dict; Ys[p] = data matrix. Returns the locked statistics."""
    o = {}
    for p in PER:
        for tau in (0.25, 0.75):
            o[f'R1_{p}_{tau}'] = F[p][tau]['R1']
        o[f'Aq_{p}'] = F[p][0.25]['R1'] - F[p][0.75]['R1']
    o['QF1_Aq_P3'] = o['Aq_P3']
    o['QF2_Aq_P3+Aq_P2'] = o['Aq_P3'] + o['Aq_P2']
    o['QF3_R1_25_P3-P1'] = o['R1_P3_0.25'] - o['R1_P1_0.25']
    o['QF3_R1_25_P3-P2'] = o['R1_P3_0.25'] - o['R1_P2_0.25']
    Y3 = Ys['P3']; m = Y3.mean(1); q25, q75 = np.quantile(Y3, [0.25, 0.75], axis=1); iqr = q75 - q25
    f25, f75 = F['P3'][0.25]['f'], F['P3'][0.75]['f']
    o['QF4_corr_f25_f75'] = corr(f25, f75)
    o['QF4_corr_f25_mean'] = corr(f25, m); o['QF4_corr_f75_mean'] = corr(f75, m)
    o['QF4_corr_f25_iqr'] = corr(f25, iqr); o['QF4_corr_f75_iqr'] = corr(f75, iqr)
    if 0.5 in F['P3']:
        f50 = F['P3'][0.5]['f']
        o['QF4_corr_f25_f50'] = corr(f25, f50); o['QF4_corr_f75_f50'] = corr(f75, f50)
        o['R1_P3_0.5'] = F['P3'][0.5]['R1']
    return o


def main():
    ZIP, MARKET, MODE, B, OUT = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
    d0, cities = L.load_panel(ZIP)
    w = d0[MARKET]
    Ys = {p: rows_of(w, p) for p in PER}
    t0 = time.time()
    if MODE == 'points':
        res = {}
        taus = (0.10, 0.25, 0.50, 0.75, 0.90)
        F = {p: {tau: fit(Ys[p], tau) for tau in taus} for p in PER}
        res['main'] = stats_from(F, Ys)
        res['R1_by_period_tau'] = {p: {str(tau): F[p][tau]['R1'] for tau in taus} for p in PER}
        res['fit_info'] = {p: {str(tau): dict(iters=F[p][tau]['iters'], start=F[p][tau]['start'], obj=F[p][tau]['obj'], v0=F[p][tau]['v0']) for tau in taus} for p in PER}
        # tau 0.10 / 0.90 versions
        res['tau10_90'] = {f'Aq10_{p}': F[p][0.10]['R1'] - F[p][0.90]['R1'] for p in PER}
        res['tau10_90']['QF2_10'] = res['tau10_90']['Aq10_P3'] + res['tau10_90']['Aq10_P2']
        print('main done', round(time.time() - t0), 's', flush=True)
        # random-start diagnostic (added; see deviation log)
        rng = np.random.default_rng(7)
        diag = {}
        for p in PER:
            for tau in (0.25, 0.75):
                objs = [Q.qfa1(Ys[p], tau, [rng.normal(size=len(Ys[p]))])['obj'] for _ in range(20)]
                diag[f'{p}_{tau}'] = dict(main_R1=F[p][tau]['R1'], best_random_R1=1 - min(objs) / F[p][tau]['v0'],
                                         median_random_R1=1 - float(np.median(objs)) / F[p][tau]['v0'])
        res['random_start_check'] = diag
        # robustness: deseason, cum3, excl tier 1
        for name, ww, keep in (('deseason', L.deseason(w), None), ('cum3', L.cum3(w), None),
                               ('excl_tier1', w, [c not in TIER1 for c in cities])):
            Yr = {p: rows_of(ww, p) for p in PER}
            if keep is not None:
                Yr = {p: Yr[p][:, np.array(keep)] for p in PER}
            Fr = {p: {tau: fit(Yr[p], tau) for tau in (0.25, 0.5, 0.75)} for p in PER}
            res[name] = stats_from(Fr, Yr)
        print('robustness done', round(time.time() - t0), 's', flush=True)
        # QF5: second factor (LP, point estimates); start from (k=1 factor, PC1 of k=1 residuals)
        full = w.loc['2011-01':'2026-10'].values
        samples = dict(Ys, full=full)
        qf5 = {}
        for sname, Y in samples.items():
            for tau in taus:
                r1 = fit(Y, tau)
                resid = Y - r1['a'][None, :] - np.outer(r1['f'], r1['b'])
                F0 = np.column_stack([r1['f'], Q._std(Q.pc1_start(resid))])
                r2 = Q.qfa_k(Y, tau, 2, F0=F0)
                qf5[f'{sname}_{tau}'] = dict(R1_k1=r1['R1'], R1_k2=1 - r2['obj'] / r1['v0'],
                                             dR1_2nd=(r1['obj'] - r2['obj']) / r1['v0'], iters_k2=r2['iters'])
            print('qf5', sname, round(time.time() - t0), 's', flush=True)
        res['QF5'] = qf5
        # k=2 version of Aq
        res['k2_Aq'] = {p: qf5[f'{p}_0.25']['R1_k2'] - qf5[f'{p}_0.75']['R1_k2'] for p in PER}
        res['k2_Aq']['QF2_k2'] = res['k2_Aq']['P3'] + res['k2_Aq']['P2']
        # factor series for the report
        months = {p: list(w.loc[L.PERIODS[p][0]:L.PERIODS[p][1]].index) for p in PER}
        pd.DataFrame({'month': months['P3'], **{f'f_{tau}': F['P3'][tau]['f'] for tau in taus},
                      'mean': Ys['P3'].mean(1)}).to_csv(OUT + '_factors_P3.csv', index=False)
        json.dump(res, open(OUT + '_points.json', 'w'), indent=1, default=float)
        print('points done', round(time.time() - t0), 's')
        return

    # bootstrap
    Fp = {p: {tau: fit(Ys[p], tau) for tau in (0.25, 0.75)} for p in PER}
    Fp['P3'][0.5] = fit(Ys['P3'], 0.5)
    point = stats_from(Fp, Ys)
    rng = np.random.default_rng(SEED)   # same draws for both markets
    draws = []
    for b in range(B):
        Fb, Yb = {}, {}
        for p in PER:
            T = len(Ys[p]); idx = L.cbb_index(T, 6, rng)
            Yb[p] = Ys[p][idx]
            taus = (0.25, 0.5, 0.75) if p == 'P3' else (0.25, 0.75)
            Fb[p] = {tau: fit(Yb[p], tau, starts=[Fp[p][tau]['f'][idx], Yb[p].mean(1)]) for tau in taus}
        draws.append(stats_from(Fb, Yb))
        if (b + 1) % 50 == 0:
            print(b + 1, round(time.time() - t0), 's', flush=True)
    dr = pd.DataFrame(draws)
    out = []
    for k, v in point.items():
        x = dr[k].dropna().values; se = float(x.std(ddof=1)); lo, hi = np.percentile(x, [2.5, 97.5])
        out.append(dict(market=MARKET, stat=k, point=v, se=se, lo=lo, hi=hi, mde=2.5 * se,
                        p_two=float(min(1, 2 * min((x <= 0).mean(), (x >= 0).mean()))), B_eff=len(x)))
    pd.DataFrame(out).to_csv(OUT + '_boot.csv', index=False)
    dr.to_csv(OUT + '_boot_draws.csv.gz', index=False)
    print('done', round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
