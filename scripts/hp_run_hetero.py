"""Part 2 (heterogeneity): thin-market gate M1-M5 and H5-H9. Analysis plan locked 2026-11-24 13:30 UTC
(docs/analysis_plan_hp_part2_hetero_20261124.md, sha256 d8cc3f73...).

usage: python hp_run_hetero.py ZIP DATA_DIR MARKET MODE B OUT
  MODE = main     two-way bootstrap, block 6, all statistics incl. quantile regression
         block3 / block12   two-way bootstrap without quantile regression
         points   point estimates for main spec and all robustness variants, city table, tercile table
"""
import sys, os, json, time
import numpy as np, pandas as pd
from scipy.stats import rankdata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hp_lib as L

TIER1 = ['北京', '上海', '广州', '深圳']
TIER2 = ['天津', '石家庄', '太原', '呼和浩特', '沈阳', '大连', '长春', '哈尔滨', '南京', '杭州', '宁波', '合肥', '福州', '厦门',
         '南昌', '济南', '青岛', '郑州', '武汉', '长沙', '南宁', '海口', '重庆', '成都', '贵阳', '昆明', '西安', '兰州', '西宁',
         '银川', '乌鲁木齐']
XNAMES = ['x1_reinv_gdp', 'x2_fiscal_self', 'x3_loan_gdp', 'x4_ln_gdppc', 'x5_ln_pop', 'x6_hpr_share']
SEED = 20261124


# ---------------------------------------------------------------- data
def load_all(zip_path, data_dir):
    d0, cities = L.load_panel(zip_path)
    import zipfile, io
    z = zipfile.ZipFile(zip_path)
    raw = pd.read_csv(io.BytesIO(z.read('CME_MResidSalesPriceIndices.csv')))
    names = raw.drop_duplicates('Citycode').set_index('Citycode').Cityname
    short = {c: names[c].replace('市', '') for c in cities}
    panel = pd.read_stata(os.path.join(data_dir, '【stata文件】各城市面板数据合集 2000-2024年 200+指标合集.dta'))
    hpr = pd.read_csv(os.path.join(data_dir, '整理结果', 'hpr_panel_70city_monthly.csv'))
    yb = pd.read_csv(os.path.join(data_dir, '整理结果', 'panel_35city_yearbook.csv'))

    def chars(years):
        s = panel[panel['城市代码'].isin(cities) & panel['年份'].isin(years)].groupby('城市代码').mean(numeric_only=True)
        x = pd.DataFrame(index=s.index)
        x['x1_reinv_gdp'] = s['房地产开发投资完成额万元'] / s['地区生产总值万元']
        x['x2_fiscal_self'] = s['地方财政一般预算内收入万元'] / s['地方财政一般预算内支出万元']
        x['x3_loan_gdp'] = s['年末金融机构各项贷款余额万元'] / s['地区生产总值万元']
        x['x4_ln_gdppc'] = np.log(s['人均地区生产总值元'])
        x['x5_ln_pop'] = np.log(s['常住人口万人'])
        h = hpr[(hpr.month >= '2016-01') & (hpr.month <= '2021-12')].groupby('citycode').hpr_any.mean()
        x['x6_hpr_share'] = h.reindex(x.index)
        return x
    X = chars(range(2016, 2022))
    X16 = chars([2016])
    scities = [c for c in cities if c in X.index and X.loc[c].notna().all()]
    X, X16 = X.loc[scities], X16.loc[scities]
    tier = np.array([1 if short[c] in TIER1 else (2 if short[c] in TIER2 else 3) for c in scities])
    v = yb[yb.year.between(2016, 2021)].groupby('city').area_resid.mean()
    V = np.array([np.log(v[short[c]]) if short[c] in v.index else np.nan for c in scities])
    pos_s = np.array([cities.index(c) for c in scities])  # column of each S-city in the 70-city panel
    return d0, cities, short, scities, X.values, X16.values, tier, V, pos_s


def build_arrays(w, W, months):
    """Full-sample arrays (months x 70); rows are later resampled within a period."""
    Y = w.values
    F = Y @ W.T
    sh = lambda A, k: np.vstack([np.full((k, A.shape[1]), np.nan), A[:-k]])
    roll = lambda A, h: pd.DataFrame(A).rolling(h).sum().values
    return {'Y': Y, 'F': F, 'F1': sh(F, 1), 'F2': sh(F, 2), 'Ylag': sh(Y, 1),
            'Y3': roll(Y, 3), 'F3': roll(F, 3), 'Y6': roll(Y, 6), 'F6': roll(F, 6), 'months': months}


def period_rows(months, p):
    a, b = L.PERIODS[p]
    return np.where((months >= a) & (months <= b))[0]


# ---------------------------------------------------------------- city-level statistics
def slope(y, x):
    xm, ym = x.mean(0), y.mean(0)
    return ((x - xm) * (y - ym)).sum(0) / ((x - xm) ** 2).sum(0), ym, xm


def city_stats(M, pos, rng_j, full=True, qr=True, lagq=False, q=0.25):
    Y, F = M['Y'][pos], M['F'][pos]
    T, N = Y.shape
    beta, ym, fm = slope(Y, F)
    alpha = ym - beta * fm
    out = {'D': Y.sum(0), 'beta': beta, 'A': T * alpha, 'K': beta * F.sum(0)}
    if not full:
        return out
    F1, F2 = M['F1'][pos], M['F2'][pos]
    bD = np.empty(N)
    for i in range(N):
        Xd = np.column_stack([np.ones(T), F[:, i], F1[:, i], F2[:, i]])
        bD[i] = np.linalg.lstsq(Xd, Y[:, i], rcond=None)[0][1:].sum()
    out['betaD'] = bD
    for h in (3, 6):
        out[f'beta{h}'] = slope(M[f'Y{h}'][pos], M[f'F{h}'][pos])[0]
    if qr:
        Yl = M['Ylag'][pos]
        for tau in (0.25, 0.50, 0.75):
            b = np.empty(N)
            for i in range(N):
                cols = [np.ones(T), F[:, i]] + ([Yl[:, i]] if lagq else [])
                b[i] = L.qreg(Y[:, i], np.column_stack(cols), tau)[1]
            out[f'b{int(tau * 100)}'] = b
    CL, CU, CG, _ = L.coex(Y, F, q, rng_j)
    out['CL'], out['E'] = CL, CL - CG
    return out


def fixed_proxies(M, months, rows3):
    """Z: share of exact-zero months 2011-01..2026-10; rho1: AR(1) of P3 OLS residuals (original data)."""
    full = np.where((months >= '2011-01') & (months <= '2026-10'))[0]
    Z = (M['Y'][full] == 0).mean(0)
    Y, F = M['Y'][rows3], M['F'][rows3]
    beta, ym, fm = slope(Y, F)
    e = Y - (ym - beta * fm) - beta * F
    e = e - e.mean(0)
    rho1 = (e[1:] * e[:-1]).sum(0) / (e ** 2).sum(0)
    return Z, rho1


# ---------------------------------------------------------------- cross-sectional statistics
def strength(X, idx):
    Z = X[idx]
    Z = (Z - Z.mean(0)) / Z.std(0)
    ev, evec = np.linalg.eigh(Z.T @ Z / len(Z))
    v = evec[:, -1]
    if v[3] < 0:
        v = -v
    return Z @ v, v, ev[-1] / ev.sum()


def _r(x, rank):
    return rankdata(x) if rank else np.asarray(x, float)


def corr(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a * b).sum() / np.sqrt((a ** 2).sum() * (b ** 2).sum()))


def resid(y, C):
    C = np.column_stack([np.ones(len(y))] + C)
    return y - C @ np.linalg.lstsq(C, y, rcond=None)[0]


def rho(s, v, rank=True):
    return corr(_r(s, rank), _r(v, rank))


def prho(s, v, controls, rank=True):
    """partial correlation of (ranks of) s and v given controls (list of arrays; ranked if rank)."""
    C = [_r(c, rank) for c in controls]
    return corr(resid(_r(s, rank), C), resid(_r(v, rank), C))


def tier_dummies(t):
    return [(t == k).astype(float) for k in (2, 3) if (t == k).any() and not (t == k).all()]


def cross_stats(cs, S, idx, tier, Z, rho1, V, rank=True):
    """cs[p][key] are arrays over S-cities; idx = resampled S-city indices; S = strength on idx."""
    c3 = {k: v[idx] for k, v in cs['P3'].items()}
    t = tier[idx]
    o = {}
    o['H5_rho_S_D'] = rho(S, c3['D'], rank)
    o['H6_rho_S_beta'] = rho(S, c3['beta'], rank)
    o['rho_D_beta'] = rho(c3['D'], c3['beta'], rank)
    o['H7_rho_S_A'] = rho(S, c3['A'], rank)
    o['rho_S_K'] = rho(S, c3['K'], rank)
    D, A, K = c3['D'], c3['A'], c3['K']
    vD = np.var(D)
    o['phi_A'] = float(np.mean((D - D.mean()) * (A - A.mean())) / vD)
    o['phi_K'] = float(np.mean((D - D.mean()) * (K - K.mean())) / vD)
    if 'betaD' in c3:
        o['M1_rho_S_betaD'] = rho(S, c3['betaD'], rank)
        o['M1_R1'] = o['M1_rho_S_betaD'] / o['H6_rho_S_beta']
        o['M2_rho_S_beta3'] = rho(S, c3['beta3'], rank)
        o['M2_R2'] = o['M2_rho_S_beta3'] / o['H6_rho_S_beta']
        o['rho_S_beta6'] = rho(S, c3['beta6'], rank)
        o['M3_prho_S_beta|Z,rho1'] = prho(S, c3['beta'], [Z[idx], rho1[idx]], rank)
        td = tier_dummies(t)
        o['M4_prho_S_beta|tier'] = prho(S, c3['beta'], td, rank) if td else rho(S, c3['beta'], rank)
        for k in (2, 3):
            m = t == k
            o[f'M4_tier{k}_rho_S_beta'] = rho(S[m], c3['beta'][m], rank) if m.sum() > 5 else np.nan
        m = ~np.isnan(V[idx])
        o['M5_prho_S_beta|V_35'] = prho(S[m], c3['beta'][m], [V[idx][m]], rank) if m.sum() > 5 else np.nan
        o['diag_rho_S_betaD-beta'] = rho(S, c3['betaD'] - c3['beta'], rank)
        o['diag_rho_S_rho1'] = rho(S, rho1[idx], rank)
        o['diag_rho_S_Z'] = rho(S, Z[idx], rank)
        o['H9_rho_S_CL'] = rho(S, c3['CL'], rank)
        o['rho_S_E'] = rho(S, c3['E'], rank)
        o['rho_D_CL'] = rho(c3['D'], c3['CL'], rank)
        o['mean_beta'] = float(c3['beta'].mean()); o['mean_betaD'] = float(c3['betaD'].mean())
        o['mean_beta3'] = float(c3['beta3'].mean())
    if 'b25' in c3:
        o['H8a_rho_S_b25'] = rho(S, c3['b25'], rank)
        o['rho_S_b50'] = rho(S, c3['b50'], rank)
        o['rho_S_b75'] = rho(S, c3['b75'], rank)
        o['H8b_rho_S_b25-b75'] = rho(S, c3['b25'] - c3['b75'], rank)
    for p in ('P1', 'P2'):
        if p in cs:
            o[f'rho_S_beta_{p}'] = rho(S, cs[p]['beta'][idx], rank)
            o[f'rho_S_D_{p}'] = rho(S, cs[p]['D'][idx], rank)
    if 'P1' in cs:
        o['rho_S_beta_P3-P2'] = o['H6_rho_S_beta'] - o['rho_S_beta_P2']
        o['rho_S_beta_P3-P1'] = o['H6_rho_S_beta'] - o['rho_S_beta_P1']
    return o


def all_city_stats(M, rows, sel, rng_j, posd=None, qr=True, lagq=False, q=0.25):
    posd = posd or {p: r for p, r in rows.items()}
    cs = {}
    for p in ('P1', 'P2', 'P3'):
        st = city_stats(M, posd[p], rng_j, full=(p == 'P3'), qr=qr, lagq=lagq, q=q)
        cs[p] = {k: v[sel] for k, v in st.items()}
    return cs


# ---------------------------------------------------------------- main
def main():
    ZIP, DATA, MARKET, MODE, B, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), sys.argv[6]
    d0, cities, short, scities, X, X16, tier, V, sel = load_all(ZIP, DATA)
    months = np.array(d0[MARKET].index)
    W = L.region_weights(cities, False)
    M = build_arrays(d0[MARKET], W, months)
    rows = {p: period_rows(months, p) for p in ('P1', 'P2', 'P3')}
    Z70, r170 = fixed_proxies(M, months, rows['P3'])
    Z, rho1 = Z70[sel], r170[sel]
    n = len(scities)
    idx0 = np.arange(n)
    S0, load0, share0 = strength(X, idx0)
    rng_j = np.random.default_rng(SEED + (0 if MARKET == 'sec' else 1))
    t0 = time.time()

    if MODE == 'points':
        res = {'pca_loadings': dict(zip(XNAMES, load0.round(4).tolist())), 'pca_share': float(share0),
               'n_cities': n, 'n_tier': {k: int((tier == k).sum()) for k in (1, 2, 3)},
               'n_V': int((~np.isnan(V)).sum())}
        cs0 = all_city_stats(M, rows, sel, rng_j)
        res['main'] = cross_stats(cs0, S0, idx0, tier, Z, rho1, V)
        # robustness variants (point estimates)
        keep = np.where(tier != 1)[0]
        res['excl_tier1'] = cross_stats(cs0, strength(X, keep)[0], keep, tier, Z, rho1, V)
        res['S_2016'] = cross_stats(cs0, strength(X16, idx0)[0], idx0, tier, Z, rho1, V)
        res['S_no_x6'] = cross_stats(cs0, strength(X[:, :5], idx0)[0], idx0, tier, Z, rho1, V)
        for k, nm in enumerate(XNAMES):
            res[f'single_{nm}'] = cross_stats(cs0, X[:, k], idx0, tier, Z, rho1, V)
        Mreg = build_arrays(d0[MARKET], L.region_weights(cities, True), months)
        res['f_excl_region'] = cross_stats(all_city_stats(Mreg, rows, sel, rng_j), S0, idx0, tier, Z, rho1, V)
        Mds = build_arrays(L.deseason(d0[MARKET]), W, months)
        res['deseason'] = cross_stats(all_city_stats(Mds, rows, sel, rng_j), S0, idx0, tier, Z, rho1, V)
        res['qr_with_lag'] = cross_stats(all_city_stats(M, rows, sel, rng_j, lagq=True), S0, idx0, tier, Z, rho1, V)
        res['pearson'] = cross_stats(cs0, S0, idx0, tier, Z, rho1, V, rank=False)
        res['q10'] = cross_stats(all_city_stats(M, rows, sel, rng_j, q=0.10), S0, idx0, tier, Z, rho1, V)
        # city table
        c3 = cs0['P3']
        tab = pd.DataFrame({'citycode': scities, 'city': [short[c] for c in scities], 'tier': tier, 'S': S0,
                            **{k: X[:, j] for j, k in enumerate(XNAMES)}, 'Z': Z, 'rho1': rho1, 'lnV': V,
                            **{k: v for k, v in c3.items()},
                            'beta_P1': cs0['P1']['beta'], 'beta_P2': cs0['P2']['beta'],
                            'D_P1': cs0['P1']['D'], 'D_P2': cs0['P2']['D']})
        tab.to_csv(OUT + '_cities.csv', index=False, encoding='utf-8-sig')
        # terciles: group means and within-group co-exceedance (factor = leave-one-out mean within group)
        g = pd.qcut(rankdata(S0), 3, labels=['weak', 'mid', 'strong']).astype(str)
        Y3 = M['Y'][rows['P3']][:, sel]
        terc = {}
        for lab in ('weak', 'mid', 'strong'):
            m = g == lab
            Yg = Y3[:, m]
            Wg = np.ones((m.sum(), m.sum())) - np.eye(m.sum()); Wg /= Wg.sum(1, keepdims=True)
            CLg, CUg, CGg, _ = L.coex(Yg, Yg @ Wg.T, 0.25, np.random.default_rng(SEED))
            terc[lab] = {'n': int(m.sum()), 'S_mean': float(S0[m].mean()),
                         **{f'{k}_mean': float(c3[k][m].mean()) for k in ('D', 'beta', 'betaD', 'beta3', 'A', 'K', 'b25', 'b75', 'CL', 'E')},
                         'CL_within_group': float(CLg.mean()), 'E_within_group': float((CLg - CGg).mean()),
                         'tier_counts': {int(k): int((tier[m] == k).sum()) for k in (1, 2, 3)},
                         'cities': [short[c] for c, mm in zip(scities, m) if mm]}
        res['terciles'] = terc
        json.dump(res, open(OUT + '_points.json', 'w'), ensure_ascii=False, indent=1, default=float)
        print('points done', round(time.time() - t0), 's')
        return

    Lb = 6 if MODE == 'main' else int(MODE.replace('block', ''))
    qr = MODE == 'main'
    cs0 = all_city_stats(M, rows, sel, rng_j, qr=qr)
    point = cross_stats(cs0, S0, idx0, tier, Z, rho1, V)
    rng = np.random.default_rng(SEED + Lb)  # same month/city draws for both markets
    draws = []
    for b in range(B):
        posd = {p: rows[p][L.cbb_index(len(rows[p]), Lb, rng)] for p in ('P1', 'P2', 'P3')}
        idx = rng.integers(0, n, size=n)
        cs = all_city_stats(M, rows, sel, rng_j, posd=posd, qr=qr)
        draws.append(cross_stats(cs, strength(X, idx)[0], idx, tier, Z, rho1, V))
        if (b + 1) % 50 == 0:
            print(b + 1, round(time.time() - t0), 's', flush=True)
    dr = pd.DataFrame(draws)
    rowsout = []
    for k, v in point.items():
        x = dr[k].dropna().values
        se = float(x.std(ddof=1))
        lo, hi = np.percentile(x, [2.5, 97.5])
        p_two = float(min(1, 2 * min((x <= 0).mean(), (x >= 0).mean())))
        rowsout.append({'market': MARKET, 'mode': MODE, 'stat': k, 'point': v, 'se': se, 'lo': lo, 'hi': hi,
                        'mde': 2.5 * se, 'p_two': p_two, 'B_eff': len(x)})
    pd.DataFrame(rowsout).to_csv(OUT + f'_{MODE}.csv', index=False)
    dr.to_csv(OUT + f'_{MODE}_draws.csv.gz', index=False)
    print('done', round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
