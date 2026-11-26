"""Addendum A (part 4, locked 2026-11-25 10:07:30 UTC, SHA-256 06df109e...0a7d90): downturn windows by turning points.

usage: python hp_run_dating.py ZIP OUTDIR
Outputs OUTDIR/dating_tests.csv (point, se, 95% interval, MDE for block 6 and block 3),
        OUTDIR/dating_desc.json (windows, durations, cumulative declines),
        OUTDIR/dating_aligned_breadth.csv (share of cities falling by months since peak).
"""
import sys, os, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hp_lib as L

ZIP, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
d, cities = L.load_panel(ZIP)
B, SEED = 999, 20261124


def turning_points(w):
    I = w.mean(axis=1).cumsum()
    p1 = I.loc['2013-01':'2014-12'].idxmax(); t1 = I.loc[p1:'2016-12'].idxmin()
    p2 = I.loc['2019-01':'2022-12'].idxmax(); t2 = I.loc[p2:'2026-10'].idxmin()
    nxt = lambda m: str(pd.Period(m, 'M') + 1)
    return I, (nxt(p1), t1), (nxt(p2), t2), (p1, p2)


Isec, D1s, D2s, pk_sec = turning_points(d['sec'])
Inew, D1n, D2n, pk_new = turning_points(d['new'])
assert D1s == ('2014-05', '2015-03') and D2s == ('2021-08', '2026-10'), (D1s, D2s)   # as stated in the addendum
D2s11 = (D2s[0], str(pd.Period(D2s[0], 'M') + 10))
WIN = {'D1L': ('2014-01', '2015-12'), 'D2L': ('2022-01', '2025-12'),
       'D1s': D1s, 'D2s': D2s, 'D2s11': D2s11, 'D1n': D1n, 'D2n': D2n}
ARR = {k: {m: d[m].loc[a:b].values for m in ('sec', 'new')} for k, (a, b) in WIN.items()}


def wstats(Y):
    g1, g2 = L.gaps(Y)
    return dict(breadth=L.breadth(Y), share05=L.share_le(Y, -0.5), gap5010=g1, gap9050=g2)


def tests(S):
    o = {}
    for m in ('sec', 'new'):
        for k in ('breadth', 'share05'):
            o[f'{m}.H1L_{k}_D2L-D1L'] = S['D2L'][m][k] - S['D1L'][m][k]
            o[f'{m}.H1s_{k}_D2s-D1s'] = S['D2s'][m][k] - S['D1s'][m][k]
            o[f'{m}.H1s11_{k}_D2s11-D1s'] = S['D2s11'][m][k] - S['D1s'][m][k]
            for w in WIN:
                o[f'{m}.level.{w}.{k}'] = S[w][m][k]
    for k in ('breadth', 'share05'):
        o[f'new.H1own_{k}_D2n-D1n'] = S['D2n']['new'][k] - S['D1n']['new'][k]
    for g in ('gap5010', 'gap9050'):
        dd = {w: float(np.mean(S[w]['new'][g] - S[w]['sec'][g])) for w in ('D1L', 'D2L', 'D1s', 'D2s')}
        o[f'B2L_{g}_change_D2L-D1L'] = dd['D2L'] - dd['D1L']
        o[f'B2s_{g}_change_D2s-D1s'] = dd['D2s'] - dd['D1s']
        o[f'B2s_{g}_new-sec_D2s'] = dd['D2s']
    return o


rows = []
for block in (6, 3):
    rng = np.random.default_rng(SEED)
    point = tests({w: {m: wstats(ARR[w][m]) for m in ARR[w]} for w in ARR})
    draws = []
    for b in range(B):
        Sb = {}
        for w in ARR:
            idx = L.cbb_index(ARR[w]['sec'].shape[0], block, rng)
            Sb[w] = {m: wstats(ARR[w][m][idx]) for m in ARR[w]}
        draws.append(tests(Sb))
    for k, v in point.items():
        a = np.array([x[k] for x in draws])
        rows.append(dict(block=block, stat=k, point=v, se=a.std(ddof=1), lo=np.percentile(a, 2.5),
                         hi=np.percentile(a, 97.5), mde=2.5 * a.std(ddof=1)))
    print('block', block, 'done', flush=True)
pd.DataFrame(rows).to_csv(os.path.join(OUT, 'dating_tests.csv'), index=False)

desc = {'windows': WIN, 'peaks_sec': pk_sec, 'peaks_new': pk_new}
for name, I, (p1, p2), (D1, D2) in (('sec', Isec, pk_sec, (D1s, D2s)), ('new', Inew, pk_new, (D1n, D2n))):
    for lab, pk, (a, b) in (('ep1', p1, D1), ('ep2', p2, D2)):
        n = len(pd.period_range(a, b, freq='M'))
        cum = float(I.loc[b] - I.loc[pk])
        desc[f'{name}.{lab}'] = dict(start=a, end=b, months=n, cum_decline_logpts=cum, per_month=cum / n,
                                     ongoing=(b == '2026-10'))
json.dump(desc, open(os.path.join(OUT, 'dating_desc.json'), 'w'), ensure_ascii=False, indent=1, default=str)

al = []
for lab, (a, b) in (('ep1', D1s), ('ep2', D2s)):
    w = d['sec'].loc[a:b]
    for k, (m, r) in enumerate(w.iterrows(), start=1):
        al.append(dict(episode=lab, months_since_peak=k, month=m, share_falling=float((r < 0).mean()),
                       mean_mom=float(r.mean())))
pd.DataFrame(al).to_csv(os.path.join(OUT, 'dating_aligned_breadth.csv'), index=False)
print('saved', OUT)
