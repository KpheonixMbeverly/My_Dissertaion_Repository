"""Cheap statistics (H1-H3, B1, B2) with block bootstrap, main spec and robustness variants."""
import sys, os, json, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hp_lib as L

ZIP = sys.argv[1]; OUT = sys.argv[2]
d0, cities = L.load_panel(ZIP)
W_all = L.region_weights(cities, False); W_reg = L.region_weights(cities, True)

VARIANTS = {
    'main':     dict(B=999, block=6,  q=0.25, transform=None,       W='all'),
    'block3':   dict(B=499, block=3,  q=0.25, transform=None,       W='all'),
    'block12':  dict(B=499, block=12, q=0.25, transform=None,       W='all'),
    'deseason': dict(B=499, block=6,  q=0.25, transform='deseason', W='all'),
    'cum3':     dict(B=499, block=6,  q=0.25, transform='cum3',     W='all'),
    'q10':      dict(B=499, block=6,  q=0.10, transform=None,       W='all'),
    'region':   dict(B=499, block=6,  q=0.25, transform=None,       W='region'),
}
if len(sys.argv) > 3:
    VARIANTS = {k: VARIANTS[k] for k in sys.argv[3].split(',')}

def period_arrays(d, p):
    a, b = L.PERIODS[p]
    yn, ys = d['new'].loc[a:b], d['sec'].loc[a:b]
    ok = yn.notna().all(1) & ys.notna().all(1)
    return {'new': yn[ok].values, 'sec': ys[ok].values}

def stats(Y, W, q, rng):
    F = Y @ W.T
    CL, CU, CG, rho = L.coex(Y, F, q, rng)
    g1, g2 = L.gaps(Y)
    return dict(breadth=L.breadth(Y), share05=L.share_le(Y, -0.5), mean=float(Y.mean()),
                s_raw=L.s_raw(Y), s_dm=L.s_dm(Y), pc1=L.pc1(Y),
                CL=float(CL.mean()), CU=float(CU.mean()), CG=float(CG.mean()), rho=float(rho.mean()),
                E=float((CL - CG).mean()), A=float((CL - CU).mean()),
                CL_med=float(np.median(CL)), E_med=float(np.median(CL - CG)),
                gap5010=g1, gap9050=g2)

def summarise(point, draws):
    """point: dict of scalars; draws: list of dicts. Returns DataFrame of point, se, 2.5%, 97.5%."""
    rows = []
    for k, v in point.items():
        arr = np.array([dd[k] for dd in draws])
        rows.append(dict(stat=k, point=v, se=arr.std(ddof=1), lo=np.percentile(arr, 2.5), hi=np.percentile(arr, 97.5),
                         p_two=2 * min((arr <= 0).mean(), (arr >= 0).mean())))
    return pd.DataFrame(rows)

def tests(S):
    """S[period][market] -> stats dict. Returns flat dict of test statistics."""
    out = {}
    for m in ('sec', 'new'):
        g = lambda p, k: S[p][m][k]
        out[f'{m}.H1_breadth_D2-D1'] = g('D2', 'breadth') - g('D1', 'breadth')
        out[f'{m}.H1_share05_D2-D1'] = g('D2', 'share05') - g('D1', 'share05')
        out[f'{m}.H2a_sraw_P3-P1'] = g('P3', 's_raw') - g('P1', 's_raw')
        out[f'{m}.H2a_sraw_P3-P2'] = g('P3', 's_raw') - g('P2', 's_raw')
        out[f'{m}.H2b_sdm_P3-P1'] = g('P3', 's_dm') - g('P1', 's_dm')
        out[f'{m}.H2b_pc1_P3-P1'] = g('P3', 'pc1') - g('P1', 'pc1')
        out[f'{m}.sdm_P3-P2'] = g('P3', 's_dm') - g('P2', 's_dm')
        out[f'{m}.pc1_P3-P2'] = g('P3', 'pc1') - g('P2', 'pc1')
        out[f'{m}.H3_dCL_P3-P2'] = g('P3', 'CL') - g('P2', 'CL')
        out[f'{m}.H3_E_P3'] = g('P3', 'E')
        out[f'{m}.H3_A_P3'] = g('P3', 'A')
        out[f'{m}.E_P3-P2'] = g('P3', 'E') - g('P2', 'E')
        out[f'{m}.CL_P3-P1'] = g('P3', 'CL') - g('P1', 'CL')
        for p in ('P1', 'P2', 'P3', 'D1', 'D2'):
            for k in ('breadth', 'share05', 'mean', 's_raw', 's_dm', 'pc1', 'CL', 'CU', 'CG', 'E', 'A', 'rho'):
                out[f'{m}.level.{p}.{k}'] = g(p, k)
    for k in ('mean', 's_raw', 's_dm', 'pc1', 'CL', 'E'):
        out[f'B1_{k}_new-sec_P3'] = S['P3']['new'][k] - S['P3']['sec'][k]
    for gname in ('gap5010', 'gap9050'):
        dD2 = float((S['D2']['new'][gname] - S['D2']['sec'][gname]).mean())
        dD1 = float((S['D1']['new'][gname] - S['D1']['sec'][gname]).mean())
        dP2 = float((S['P2']['new'][gname] - S['P2']['sec'][gname]).mean())
        out[f'B2_{gname}_new-sec_D2'] = dD2
        out[f'B2_{gname}_change_D2-D1'] = dD2 - dD1
        out[f'B2_{gname}_change_D2-P2'] = dD2 - dP2
        out[f'B2_{gname}_new-sec_D2_median'] = float(np.median(S['D2']['new'][gname] - S['D2']['sec'][gname]))
    return out

all_res = []
for vname, v in VARIANTS.items():
    t0 = time.time()
    d = {k: (L.deseason(x) if v['transform'] == 'deseason' else L.cum3(x) if v['transform'] == 'cum3' else x) for k, x in d0.items()}
    W = W_all if v['W'] == 'all' else W_reg
    arrs = {p: period_arrays(d, p) for p in L.PERIODS}
    rng = np.random.default_rng(20261124)
    S0 = {p: {m: stats(arrs[p][m], W, v['q'], rng) for m in ('sec', 'new')} for p in arrs}
    point = tests(S0)
    draws = []
    for b in range(v['B']):
        Sb = {}
        for p in arrs:
            n = arrs[p]['sec'].shape[0]
            idx = L.cbb_index(n, v['block'], rng)
            Sb[p] = {m: stats(arrs[p][m][idx], W, v['q'], rng) for m in ('sec', 'new')}
        draws.append(tests(Sb))
    df = summarise(point, draws); df.insert(0, 'variant', vname)
    df['n_months'] = None
    all_res.append(df)
    print(vname, 'done in', round(time.time() - t0), 's', flush=True)
res = pd.concat(all_res)
res.to_csv(OUT, index=False)
print('saved', OUT)
