"""Clean the Wind EDB exports downloaded on 2026-11-25 for the 70-city housing dissertation.

Run from anywhere:  python build_wind_housing_20261125.py
Inputs : data/raw/wind/*.csv (original Wind exports, GB18030), data/raw/csmar/csmar_LoanSector_full_20261118.csv,
         ../中国房地产统计年鉴+面板数据/整理结果/hpr_panel_70city_monthly.csv (70-city list and codes)
Outputs: data/clean/wind_房地产_20261125/*.csv (UTF-8 with BOM) and build_log.txt
Every cleaning decision is printed to build_log.txt; README.md in the output folder documents the files.
"""
import re
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1]
RAW = DATA / 'raw' / 'wind'
OUT = DATA / 'clean' / 'wind_房地产_20261125'
HPR = DATA.parent / '中国房地产统计年鉴+面板数据' / '整理结果' / 'hpr_panel_70city_monthly.csv'
OUT.mkdir(parents=True, exist_ok=True)
LOG = []
MUNI = ('北京', '上海', '天津', '重庆')


def log(msg):
    LOG.append(msg)
    print(msg)


def save(df, name, index=False):
    df.to_csv(OUT / name, index=index, encoding='utf-8-sig')
    log(f'  -> {name}  {df.shape}')


def read_wind(fname):
    """Wind export: row 0 = indicator names, last row = '数据来源：Wind'. Returns (names, body indexed by date)."""
    raw = pd.read_csv(RAW / fname, encoding='gb18030', header=None, dtype=str, low_memory=False)
    names = raw.iloc[0, 1:].tolist()
    body = raw.iloc[1:].copy()
    body = body[~body[0].astype(str).str.startswith('数据来源')]
    body.index = pd.to_datetime(body[0])
    body = body.drop(columns=0)
    body.columns = range(len(names))
    body = body.apply(pd.to_numeric, errors='coerce').sort_index()
    return names, body


def norm_city(x):
    """Wind place name -> 70-city short name."""
    x = x.replace('(停止)', '')
    if x == '吉林市':
        return '吉林'
    if x.startswith('大理'):
        return '大理'
    for suf in ('市', '地区', '盟'):
        if x.endswith(suf) and len(x) > 2:
            return x[:-len(suf)]
    return x


# ---------- 70-city list ----------
hp = pd.read_csv(HPR)
c70 = hp.drop_duplicates('citycode')[['citycode', 'city']].reset_index(drop=True)
CODE = dict(zip(c70.city, c70.citycode))
save(c70, 'city70_codes.csv')

# ---------- 1. residential land, transacted planned GFA (annual) ----------
log('\n[1] 成交土地规划建筑面积:住宅类用地（年）')
names, body = read_wind('wind_成交土地规划建面_住宅类用地_年_20261125.csv')
cols = {}
for j, n in enumerate(names):
    m = re.match(r'中国:(.+?):成交土地规划建筑面积:住宅类用地$', n)
    if not m:
        log(f'  skip non-land column: {n}')
        continue
    s = body[j].dropna()
    s.index = s.index.year
    cols.setdefault(m.group(1), []).append((j, s))
series = {}
for c, lst in cols.items():
    if len(lst) == 1:
        series[c] = lst[0][1]
        continue
    # duplicated name: drop any copy identical to another city's series (export/replace error)
    keep = []
    for j, s in lst:
        twin = [o for o, ll in cols.items() if o != c and any(s.equals(t) for _, t in ll)]
        if twin:
            log(f'  {c}: column {j} is an exact copy of {twin[0]} -> dropped')
        else:
            keep.append(s)
    assert len(keep) == 1, c
    series[c] = keep[0]
deal = pd.DataFrame(series).sort_index()
deal.index.name = 'year'
long = deal.stack().rename('gfa_wan_m2').reset_index().rename(columns={'level_1': 'city'})
long['in70'] = long.city.isin(CODE)
long['citycode'] = long.city.map(CODE)
save(long[['city', 'citycode', 'in70', 'year', 'gfa_wan_m2']], 'land_deal_resid_gfa_annual_long.csv')
w70 = deal.reindex(columns=[c for c in c70.city if c in deal.columns])
save(w70, 'land_deal_resid_gfa_annual_70.csv', index=True)
log(f'  70-city missing: {[c for c in c70.city if c not in deal.columns]}')

# ---------- 2. residential land, supplied planned GFA (weekly -> annual) ----------
log('\n[2] 供应土地规划建筑面积:住宅类用地（周，加总为年）')
names, body = read_wind('wind_供应土地规划建面_住宅类用地_周_20261125.csv')
sup = {}
for j, n in enumerate(names):
    m = re.match(r'中国:(.+?):供应土地规划建筑面积:住宅类用地$', n)
    c = m.group(1)
    s = body[j]
    if c in sup:
        log(f'  duplicate column for {c}: identical={sup[c].equals(s)} -> kept one')
        continue
    sup[c] = s
n2, b2 = read_wind('wind_吉林_供应土地规划建面_住宅类用地_周_20261125.csv')
sup['吉林'] = b2[0]
log('  added 吉林 from separate export')
wk = pd.DataFrame(sup).sort_index()
wk.index.name = 'week_end'
wlong = wk.stack().rename('gfa_wan_m2').reset_index().rename(columns={'level_1': 'city'})
wlong['in70'] = wlong.city.isin(CODE)
save(wlong, 'land_supply_resid_gfa_weekly_long.csv')
ann = wk.groupby(wk.index.year).sum(min_count=1)
ann.index.name = 'year'
log('  annual = sum of weeks by week-end year; 2026 is a partial year')
save(ann.reindex(columns=[c for c in c70.city if c in ann.columns]), 'land_supply_resid_gfa_annual_70.csv', index=True)
log(f'  70-city missing: {[c for c in c70.city if c not in ann.columns]}')

# ---------- 3. second-hand transaction area ----------
log('\n[3] 二手房成交面积（分城市，日/月）')
names, body = read_wind('wind_二手房成交面积_分城市_20261125.csv')
inv, rows = [], []
for j, n in enumerate(names):
    m = re.search(r'中国:([^:]+):(?:成交面积:)?(二手房|存量房)(?:成交面积)?(:住宅)?', n)
    city, typ = m.group(1), m.group(2) + (':住宅' if m.group(3) else '')
    s = body[j].dropna()
    d = np.median(np.diff(s.index.values).astype('timedelta64[D]').astype(int)) if len(s) > 1 else 0
    freq = '日' if d <= 3 else ('月' if d <= 45 else '其他')
    inv.append(dict(series=n, city=city, in70=city in CODE, type=typ, stopped=n.startswith('(停止)'), freq=freq,
                    start=s.index.min().date(), end=s.index.max().date(), n_obs=len(s)))
    for t, v in s.items():
        rows.append((n, city, t.date(), v))
inv = pd.DataFrame(inv)
save(inv, 'sec_volume_inventory.csv')
save(pd.DataFrame(rows, columns=['series', 'city', 'date', 'value_raw']), 'sec_volume_all_series_long.csv')
SEL = {  # city: (type, freq, stopped, use)
    '北京': ('二手房:住宅', '月', False, 'P3'), '广州': ('二手房:住宅', '月', False, 'P3+D1'),
    '深圳': ('二手房', '日', False, 'P3+D1'), '杭州': ('二手房', '日', False, 'P3+D1'),
    '成都': ('二手房', '日', False, 'P3+D1'), '厦门': ('二手房', '日', False, 'P3+D1'),
    '青岛': ('二手房', '日', False, 'P3+D1'), '南宁': ('二手房', '日', False, 'P3+D1'),
    '无锡': ('二手房:住宅', '月', False, 'P3+D1'), '扬州': ('二手房', '日', False, 'P3+D1'),
    '南京': ('二手房:住宅', '月', True, 'D1'), '南昌': ('二手房', '日', True, 'D1'),
    '武汉': ('二手房:住宅', '月', True, 'D1'), '郑州': ('二手房:住宅', '月', True, 'D1'),
    '金华': ('二手房', '日', True, 'D1'), '泸州': ('二手房:住宅', '月', True, 'D1'),
    '岳阳': ('二手房:住宅', '月', True, 'D1'),
}
mon = []
for c, (typ, fr, stp, use) in SEL.items():
    r = inv[(inv.city == c) & (inv.type == typ) & (inv.freq == fr) & (inv.stopped == stp)]
    assert len(r) == 1, (c, len(r))
    n = r.series.iloc[0]
    s = body[names.index(n)].dropna()
    if fr == '日':
        g = s.groupby(s.index.to_period('M'))
        m_ = pd.DataFrame({'value': g.sum(), 'n_days': g.size()})
    else:
        m_ = pd.DataFrame({'value': s.values, 'n_days': np.nan}, index=s.index.to_period('M'))
    m_['city'], m_['citycode'], m_['series'], m_['use'] = c, CODE.get(c), n, use
    m_['incomplete_month'] = (m_.n_days < 15) if fr == '日' else False
    mon.append(m_.reset_index(names='month'))
mon = pd.concat(mon)
mon['month'] = mon.month.astype(str)
cur = '2026-11'                       # export date 2026-11-25: current month is incomplete
mon = mon[mon.month < cur]
log(f'  dropped {cur} (current, incomplete month)')
save(mon[['city', 'citycode', 'month', 'value', 'n_days', 'incomplete_month', 'use', 'series']], 'sec_volume_monthly_selected.csv')
log('  excluded: 大连 (daily gap 2019-07..2022-01), 平顶山 (2019-10..2024-10 only), non-70 cities')

# ---------- 4. resident population ----------
log('\n[4] 常住人口（年）')
names, body = read_wind('wind_常住人口_分地区_年_20261125.csv')
body.index = body.index.year
prow, pick = [], {}
for j, n in enumerate(names):
    p = n.replace('(停止)', '').split(':')
    place = p[0] if len(p) == 2 else ':'.join(p[1:-1])
    prov = p[0] if len(p) > 2 else p[0]
    s = body[j].dropna()
    for y, v in s.items():
        prow.append((n, prov, place, y, v))
    c = norm_city(p[0] if len(p) == 2 else p[1])
    if c in CODE and len(p) <= 3 and c not in pick:
        pick[c] = j
save(pd.DataFrame(prow, columns=['series', 'province', 'place', 'year', 'value_raw']), 'population_all_places_long.csv')
pp = []
for c in c70.city:
    j = pick[c]
    s = body[j].dropna()
    unit_fix = s.max() > 1e5          # a few cities are reported in persons, not 10k persons
    s = s / 1e4 if unit_fix else s
    if unit_fix:
        log(f'  {c}: values in persons -> divided by 10,000')
    for y, v in s.items():
        pp.append(dict(city=c, citycode=CODE[c], year=y, pop_wan=v, census_year=y in (2010, 2020),
                       series=names[j]))
pp = pd.DataFrame(pp)
save(pp, 'population_resident_70_long.csv')
miss2010 = [c for c in c70.city if not ((pp.city == c) & (pp.year == 2010)).any()]
log(f'  70 cities lacking 2010: {miss2010}  (use the 2010 census bulletin)')
log('  WARNING: 2011-2019 intercensal estimates are not comparable across cities; use 2010 and 2020 only')

# ---------- 5. Dali characteristics ----------
log('\n[5] 大理：房地产开发投资、一般公共预算收支')
names, body = read_wind('wind_大理_财政与房地产投资_20261125.csv')
col = {n.split(':', 2)[2]: j for j, n in enumerate(names)}
dec = body[body.index.month == 12].copy()
dec.index = dec.index.year
dl = pd.DataFrame({
    're_invest_yi': dec[col['房地产开发投资完成额']] / 1e4,                 # 万元 -> 亿元
    'fiscal_rev_yi': dec[col['一般公共预算收入:累计值']],
    'fiscal_exp_yi': dec[col['一般公共预算支出:累计值']],
    'fiscal_rev_yoy': dec[col['一般公共预算收入:累计同比']],
    'fiscal_exp_yoy': dec[col['一般公共预算支出:累计同比']],
})
dl['fiscal_backcast'] = False
for v, g in (('fiscal_rev_yi', 'fiscal_rev_yoy'), ('fiscal_exp_yi', 'fiscal_exp_yoy')):
    if pd.isna(dl.loc[2016, v]) and pd.notna(dl.loc[2017, v]):
        dl.loc[2016, v] = dl.loc[2017, v] / (1 + dl.loc[2017, g] / 100)
        dl.loc[2016, 'fiscal_backcast'] = True
log('  2016 fiscal levels back-cast from 2017 level and 2017 yoy (approximate)')
dl.index.name = 'year'
save(dl.loc[2005:2025], 'dali_characteristics_annual.csv', index=True)

# ---------- 6. provincial household medium/long-term loans ----------
log('\n[6] 住户中长期贷款（省级，月）')
names, body = read_wind('wind_住户中长期贷款_省级_月_20261125.csv')
pl, seen = [], set()
for j, n in enumerate(names):
    prov = n.split(':')[0]
    if prov in seen:
        log(f'  duplicate province column dropped: {prov}')
        continue
    seen.add(prov)
    for t, v in body[j].dropna().items():
        pl.append((prov, t.strftime('%Y-%m'), v))
save(pd.DataFrame(pl, columns=['province', 'month', 'loans_yi']), 'household_mlt_loans_province_monthly.csv')

# ---------- 7. national household loans (CSMAR, PBoC credit table) ----------
log('\n[7] 全国住户贷款（CSMAR）')
cs = pd.read_csv(DATA / 'raw' / 'csmar' / 'csmar_LoanSector_full_20261118.csv', low_memory=False).set_index('SgnMonth')
nat = cs[['HouseholdLoan', 'HouseholdMidLongTermLoan', 'LongTermConsumptionLoan']].copy()
last = nat.index.max()
if nat.loc[last].equals(nat.iloc[-2]):
    log(f'  {last} identical to previous month (not yet updated) -> dropped')
    nat = nat.drop(index=last)
nat.index.name = 'month'
save(nat, 'national_household_loans_monthly.csv', index=True)

# ---------- 8. foreclosures (judicial auctions), residential ----------
log('\n[8] 法拍房：首次挂拍量、成交面积（住宅用房，月）')
fl = {}
for fname, var in (('wind_法拍房首次挂拍量_住宅用房_月_20261125.csv', 'first_listings'),
                   ('wind_法拍房成交面积_住宅用房_月_20261125.csv', 'deal_area_m2')):
    names, body = read_wind(fname)
    for j, n in enumerate(names):
        p = n.replace('(停止)', '').split(':')
        prov, place = (p[1], p[1]) if p[2] in ('首次挂拍量', '成交面积') else (p[1], p[2])
        for t, v in body[j].items():
            fl.setdefault((prov, place, t.strftime('%Y-%m')), {})[var] = v
fdf = pd.DataFrame([dict(province=k[0], place=k[1], month=k[2], **v) for k, v in fl.items()])
partial = fdf.month.max()
fdf = fdf[fdf.month < partial]
log(f'  dropped {partial} (current, incomplete month); series start 2023-01 in Wind')
fdf['city'] = fdf.place.map(norm_city)
fdf['in70'] = fdf.city.isin(CODE) & (fdf.place.map(lambda x: x.endswith('市') or x in MUNI or x.startswith('大理')))
save(fdf.sort_values(['province', 'place', 'month']), 'foreclosure_resid_monthly_all.csv')
f70 = fdf[fdf.in70].copy()
f70['citycode'] = f70.city.map(CODE)
save(f70[['city', 'citycode', 'month', 'first_listings', 'deal_area_m2']].sort_values(['citycode', 'month']),
     'foreclosure_resid_monthly_70.csv')
log(f'  70-city covered: {f70.city.nunique()}')

(OUT / 'build_log.txt').write_text('\n'.join(LOG), encoding='utf-8')
