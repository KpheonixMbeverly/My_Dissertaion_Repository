"""H4: lower-tail slope tilt in P3 vs the scale-effect (mirror) prediction estimated in P1. Block bootstrap."""
import sys, os, json, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hp_lib as L

ZIP, MARKET, B, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
d0, cities = L.load_panel(ZIP)

def rows(w, p, W, lag=True):
    a, b = L.PERIODS[p]
    x = w.loc[a:b]; xl = w.shift(1).loc[a:b]
    ok = x.notna().all(1) & (xl.notna().all(1) if lag else True)
    Y, Yl = x[ok].values, xl[ok].values
    return Y, Yl, Y @ W.T

def fit(Y, Yl, F, tau, absf=False, lag=True):
    N = Y.shape[1]; out_f = np.empty(N); out_a = np.full(N, np.nan)
    for i in range(N):
        cols = [np.ones(len(Y)), F[:, i]]
        if absf: cols.append(np.abs(F[:, i]))
        if lag: cols.append(Yl[:, i])
        bcoef = L.qreg(Y[:, i], np.column_stack(cols), tau)
        out_f[i] = bcoef[1]
        if absf: out_a[i] = bcoef[2]
    return out_f, out_a

def h4(R, taus=(0.25, 0.75), lag=True):
    lo, hi = taus
    b_lo, c_lo = fit(*R['P1'], lo, absf=True, lag=lag); b_hi, c_hi = fit(*R['P1'], hi, absf=True, lag=lag)
    l3_lo, _ = fit(*R['P3'], lo, lag=lag); l3_hi, _ = fit(*R['P3'], hi, lag=lag)
    l2_lo, _ = fit(*R['P2'], lo, lag=lag); l2_hi, _ = fit(*R['P2'], hi, lag=lag)
    T_obs3 = l3_lo - l3_hi; T_pred3 = (b_lo - c_lo) - (b_hi - c_hi)
    U_obs2 = l2_hi - l2_lo; U_pred2 = (b_hi + c_hi) - (b_lo + c_lo)
    return {'H4_mean_Tobs3-Tpred3': float(np.mean(T_obs3 - T_pred3)), 'H4_median_Tobs3-Tpred3': float(np.median(T_obs3 - T_pred3)),
            'Tobs3_mean': float(T_obs3.mean()), 'Tpred3_mean': float(T_pred3.mean()),
            'boom_mean_Uobs2-Upred2': float(np.mean(U_obs2 - U_pred2)), 'Uobs2_mean': float(U_obs2.mean()), 'Upred2_mean': float(U_pred2.mean()),
            'lam_lo_P3-P2': float(np.mean(l3_lo - l2_lo)), 'lam_hi_P3-P2': float(np.mean(l3_hi - l2_hi)),
            'absf_coef_lo_P1': float(c_lo.mean()), 'absf_coef_hi_P1': float(c_hi.mean()),
            'share_cities_absf_hi>lo': float((c_hi > c_lo).mean())}

W_all = L.region_weights(cities, False); W_reg = L.region_weights(cities, True)
w = d0[MARKET]
results = {}
t0 = time.time()
# point estimates: main and variants
R_main = {p: rows(w, p, W_all) for p in ('P1', 'P2', 'P3')}
results['main'] = h4(R_main)
results['tau10_90'] = h4(R_main, taus=(0.10, 0.90))
results['nolag'] = h4({p: rows(w, p, W_all, lag=False) for p in ('P1', 'P2', 'P3')}, lag=False)
results['deseason'] = h4({p: rows(L.deseason(w), p, W_all) for p in ('P1', 'P2', 'P3')})
results['cum3'] = h4({p: rows(L.cum3(w), p, W_all) for p in ('P1', 'P2', 'P3')})
results['region'] = h4({p: rows(w, p, W_reg) for p in ('P1', 'P2', 'P3')})
print('points done', round(time.time() - t0), 's', flush=True)
# bootstrap for main spec
rng = np.random.default_rng(20261124 + (0 if MARKET == 'sec' else 1))
draws = []
for b in range(B):
    Rb = {}
    for p, (Y, Yl, F) in R_main.items():
        idx = L.cbb_index(len(Y), 6, rng)
        Rb[p] = (Y[idx], Yl[idx], F[idx])
    draws.append(h4(Rb))
    if (b + 1) % 25 == 0:
        print(b + 1, 'draws', round(time.time() - t0), 's', flush=True)
        json.dump({'points': results, 'draws': draws}, open(OUT, 'w'))
json.dump({'points': results, 'draws': draws}, open(OUT, 'w'))
print('done', round(time.time() - t0), 's', flush=True)
