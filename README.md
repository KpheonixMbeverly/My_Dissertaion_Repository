# 对全国市场最敏感的城市跌得最深吗？

**2021–2026 年中国 70 城二手房下行中的敏感度与累计跌幅**

*Do the most market-sensitive cities fall furthest? Sensitivity and cumulative falls in China's 70-city resale housing downturn, 2021–2026*

本仓库存放宁波诺丁汉大学经济学本科毕业论文（ECON3067，2026/27 学年）的代码、锁定的分析方案和结果。价格和城市数据受数据库许可限制，不在仓库内，见[数据](#数据)。

> **进度（2026-11-26）**：第一至第三部分的正式检验已完成，附录 A（下跌期重划）也已完成。附录 B（机制）和附录 C（检验力与阳性对照）还没锁定，计划 12 月中旬锁定并运行，1 月中旬完成全部分析。

## 研究问题

到 2026 年 10 月，70 个大中城市的二手房价格全部低于 2021 年 7 月的水平。2021 年 8 月以来，86% 的城市-月份在下跌。70 城平均已连续下跌 63 个月，累计约 27 个对数点（约 −24%）；2014–15 年那轮只跌了 11 个月，约 −5%。

所有城市都在跌，值得问的是哪些城市跌得最多。衡量一个城市房价风险的常用指标，是它对全国市场的敏感度，相当于股票的 β。本研究的主问题是：**对全国市场最敏感的城市，是否就是累计跌得最深的城市？** 下面三个子问题都在这一轮下跌内部回答：

- **RQ1 一个全国冲击**：一个全国因子能解释多少城市涨跌？下跌有多持久？
- **RQ2 敏感度与累计跌幅（主线）**：按敏感度和按累计跌幅给城市排序，结果是否一致？敏感度解释不了的那部分跌幅，与哪些下跌前的城市特征有关？
- **RQ3 同时深跌**：在全国最弱的月份，城市一起深跌的频率是否超过普通相关性所隐含的程度？

研究是描述性和结构性的，不做因果识别。主样本是国家统计局的二手住宅价格指数，新建商品住宅指数作对照。

## 模型

全文用同一个因子分解。f₋ᵢ,ₜ 是剔除城市 i 后其余 69 城的月度对数涨跌均值，Fᵢ = Σₜ f₋ᵢ,ₜ 是全国累计变动，T 是月数：

- yᵢₜ = aᵢ + βᵢ f₋ᵢ,ₜ + eᵢₜ
- Dᵢ = Σₜ yᵢₜ = Kᵢ + Aᵢ，其中 Kᵢ = β̂ᵢ Fᵢ，Aᵢ = Dᵢ − β̂ᵢ Fᵢ = T · âᵢ

Kᵢ 是按敏感度折算的累计变动，Aᵢ 是相对市场基准的累计偏离，类似事件研究里的累计超额收益。Aᵢ = T · âᵢ 是恒等式，只用来说明哪些城市偏离了市场基准，不作为独立证据。

## 目前的结果

下表是二手房的结果，括号内为自助法 95% 区间。各数字在 `results/` 中的位置见 [results/README.md](results/README.md)。

| 问题 | 结果 | 结论的写法 |
|---|---|---|
| RQ1 | 2021-08 至 2026-10，86% 的城市-月份在跌；70 城平均连跌 63 个月、约 −27 个对数点；此前两轮各跌 10、11 个月 | 典型事实，只作描述 |
| RQ2 | 实力强的城市更敏感：ρ(S, β) = 0.62 [0.35, 0.74]，并通过了薄市场测量检验。但敏感度与累计跌幅的秩相关只有 ρ(D, β) = 0.13 [−0.42, 0.59]；2022-01 起跌幅最大的 17 城与 β 最高的 17 城只重合 4 个，随机期望约 4.2 | 没有证据表明敏感的城市就是跌得深的城市。区间较宽，不写“已证实不重合” |
| RQ3 | 同时深跌超出高斯基准 +0.03 [−0.05, 0.11]；下尾减上尾 +0.09 [−0.09, 0.20]；分位数因子模型 QF1 +0.034 [−0.041, 0.109] | 没有超出相关性的同时深跌，写成上限（区间上端约 +0.11） |
| 已撤回 | “这一轮比 2014–15 年更普遍”（H1）：按拐点划定下跌期后为 +0.025 [−0.087, 0.127] | 原来的 +0.33 来自日历年窗口错位，见附录 A |



## 研究流程

- **先锁定，后运行**：每份分析方案在正式估计前写定，计算 SHA-256 并提交，然后才运行。锁定后的改动只追加在方案末尾的“偏离记录”里，锁定记录见 [docs/plan_locks.md](docs/plan_locks.md)。多数点估计在锁定前的探索中已经看过，所以称“分析方案锁定”，不称预注册。
- **只研究一轮**：2011 年以来只有三轮下跌，跨轮比较只作描述。下跌期按全国累计指数的拐点划定。
- **否定结论写成上限**：报告区间上端和最小可检测效应（2.5 × 自助标准误），并用阳性对照模拟说明检验力（附录 C）。
- **推断**：时间维度用 6 个月块的循环块自助法（B = 999，分位数因子部分 B = 499）；城市截面用双向自助法，月份按块重抽，城市有放回重抽。

| 方案 | 内容 | 状态 |
|---|---|---|
| 第一部分 | 广度、共同成分、同时深跌（H1–H4），新房对照（B1、B2） | 2026-11-24 锁定，已完成 |
| 第二部分 | 城市异质性：薄市场闸门 M，H5–H9（敏感度、累计跌幅、下尾），ρ(D, β) | 2026-11-24 锁定，已完成 |
| 第三部分 | 分位数因子模型（QF1–QF5） | 2026-11-24 锁定，已完成 |
| 附录 A | 下跌期按拐点重划（2021-08 至 2026-10） | 2026-11-25 锁定，已完成 |
| 附录 B | 机制：下跌前的估值与 β 的关系；下跌前的供给积压、人口增长与累计跌幅的关系（控制 β） | 待写 |
| 附录 C | 阳性对照、本轮内的对称性检验、因子个数、尾部检验按 2021-08 窗口重算 | 待写 |

## 仓库结构

```
.
├── README.md
├── requirements.txt
├── scripts/          分析代码
├── docs/             锁定的分析方案与锁定记录
├── results/          各部分的输出（汇总表、自助抽样、日志）
└── data_pipeline/    Wind 机制数据的清洗脚本
```

| 文件 | 内容 | 输出 |
|---|---|---|
| `scripts/hp_lib.py` | 读取 70 城面板；全国因子、共同成分份额、广度、同时超越概率与高斯基准；分位数回归（scipy 的 HiGHS 求解器）；循环块自助 | — |
| `scripts/hp_run_main.py` | 第一部分 H1–H3、B1、B2，以及 7 种稳健性设定 | `results/hp_formal/results_main.csv` |
| `scripts/hp_run_qr.py` | 逐城分位数回归与尺度效应外推（H4） | `results/hp_formal/qr_*.json` |
| `scripts/hp_run_hetero.py` | 城市实力指数、薄市场闸门、H5–H9、ρ(D, β) | `results/hp_hetero/` |
| `scripts/hp_run_qfm.py`、`scripts/qfm_lib.py` | 分位数因子模型 QF1–QF5 | `results/hp_qfm/` |
| `scripts/hp_run_dating.py` | 拐点划定与附录 A 的检验 | `results/hp_dating/` |
| `scripts/hp_run_hetero_p3alt.py` | 第二部分按 2021-08 起的窗口重算（点估计） | `results/hp_dating/sec_p3alt_*` |
| `data_pipeline/build_wind_housing_20261125.py` | 清洗 Wind 导出的住宅用地、人口、成交、法拍、贷款数据 | 本地数据目录 |

## 复现

需要 Python 3.9 及以上。现有结果是在 Python 3.13、numpy 2.5、scipy 1.18、pandas 3.0 下得到的。

```bash
pip install -r requirements.txt
```

还需要两份本地数据（不在仓库内）：

- `ZIP`：从 CSMAR 导出的 70 城住宅价格指数压缩包，内含 `CME_MResidSalesPriceIndices.csv`。脚本直接读压缩包。
- `PANEL_DIR`：城市特征数据目录，只有第二部分用到。目录里需要有 `【stata文件】各城市面板数据合集 2000-2024年 200+指标合集.dta`、`整理结果/hpr_panel_70city_monthly.csv` 和 `整理结果/panel_35city_yearbook.csv`。

在仓库根目录运行。`sec` 为二手房，`new` 为新房；自助法部分单个命令约需几分钟到十几分钟。

```bash
ZIP="/path/to/CME_MResidSalesPriceIndices_70城住宅价格指数_20261119.zip"
PANEL_DIR="/path/to/中国房地产统计年鉴+面板数据"

# 第一部分
python scripts/hp_run_main.py "$ZIP" results/hp_formal/results_main.csv
python scripts/hp_run_qr.py   "$ZIP" sec 299 results/hp_formal/qr_sec.json
python scripts/hp_run_qr.py   "$ZIP" new 299 results/hp_formal/qr_new.json

# 第二部分：先算点估计和逐城表，再跑自助法（输出文件名为 前缀_模式）
python scripts/hp_run_hetero.py "$ZIP" "$PANEL_DIR" sec points  0   results/hp_hetero/sec
python scripts/hp_run_hetero.py "$ZIP" "$PANEL_DIR" sec main    999 results/hp_hetero/sec
python scripts/hp_run_hetero.py "$ZIP" "$PANEL_DIR" sec block3  499 results/hp_hetero/sec
python scripts/hp_run_hetero.py "$ZIP" "$PANEL_DIR" sec block12 499 results/hp_hetero/sec
python scripts/hp_run_hetero.py "$ZIP" "$PANEL_DIR" new points  0   results/hp_hetero/new
python scripts/hp_run_hetero.py "$ZIP" "$PANEL_DIR" new main    999 results/hp_hetero/new

# 第三部分
python scripts/hp_run_qfm.py "$ZIP" sec points 0   results/hp_qfm/sec
python scripts/hp_run_qfm.py "$ZIP" sec boot   499 results/hp_qfm/sec
python scripts/hp_run_qfm.py "$ZIP" new points 0   results/hp_qfm/new
python scripts/hp_run_qfm.py "$ZIP" new boot   499 results/hp_qfm/new

# 附录 A
python scripts/hp_run_dating.py "$ZIP" results/hp_dating
python scripts/hp_run_hetero_p3alt.py "$ZIP" "$PANEL_DIR" sec results/hp_dating/sec_p3alt
```

随机种子写在脚本里（主要是 20261124 及其派生值）。用同样的脚本和命令重跑，应得到相同的结果；改动脚本中的计算顺序会改变随机数流，自助区间会有小幅差异。

## 数据

数据受 CSMAR 和 Wind 的使用许可限制。仓库只放代码和由代码生成的统计结果，不放原始数据。

| 数据 | 原始机构 | 获取途径 | 用途 |
|---|---|---|---|
| 70 个大中城市住宅销售价格指数（新建商品住宅、二手住宅，月度环比，2011-01 至 2026-10） | 国家统计局 | CSMAR（`CME_MResidSalesPriceIndices`） | 主变量 |
| 地级市经济社会指标（人均 GDP、人口、财政、信贷、房地产投资等，2000–2024） | 各地统计年鉴 | 汇编的地级市面板 | 城市实力指数 |
| 35 城住宅销售面积等 | 《中国房地产统计年鉴》 | 作者整理的面板 | 薄市场闸门 M5 |
| 70 城限购状态（2010-01 至 2026-10） | 各城市政府文件 | 作者整理编码，169 条事件附来源链接 | 实力指数中的限购强度 |
| 住宅用地成交与供应、常住人口、二手房成交面积、法拍房、住户贷款 | 原始来源待逐项确认 | Wind 经济数据库 | 附录 B 的机制变量 |

`data_pipeline/build_wind_housing_20261125.py` 按本地数据目录的结构编写：脚本放在 `data/scripts/` 下运行，读 `data/raw/wind/` 的原始导出，写到 `data/clean/wind_房地产_20261125/`。每一步清洗决定都记在输出目录的 `build_log.txt` 里。

## 说明

- 本仓库是本科论文的工作仓库，未附开源许可。代码和结果供评阅和复核使用。
- 研究计划全文在单独的文档中维护，不在仓库内。
- 2026-11-26 仓库按清空前保存的副本重建。三份结果报告根据结果文件重写，部分偏离记录据研究计划重录（标为“重录”），见 [docs/plan_locks.md](docs/plan_locks.md) 的“仓库重建说明”。

## 文献地图与开题报告

1. [文献地图：对市场最敏感的城市跌得最深吗？](research/literature-map.md)
2. [开题报告（中文版）](research/proposal-zh.md)
3. [Research Proposal（英文版）](research/proposal-en.md)
