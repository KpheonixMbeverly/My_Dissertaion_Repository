# 结果文件

全部由 `scripts/` 中的脚本生成，运行命令见根目录 README。每个部分有一份结果报告，先读报告再看表：

- 第一部分：[hp_formal/report.md](hp_formal/report.md)
- 第二部分（敏感度与累计跌幅）：[hp_hetero/report_hetero.md](hp_hetero/report_hetero.md)
- 第三部分（分位数因子）：[hp_qfm/report_qfm.md](hp_qfm/report_qfm.md)
- 附录 A（下跌期重划）：[hp_dating/report_dating.md](hp_dating/report_dating.md)

汇总表的列：`point` 是点估计，`se` 是自助标准误，`lo`、`hi` 是 95% 百分位区间，`mde` 是最小可检测效应（2.5 × se），`p_two` 是双侧自助 p 值，`B_eff` 是有效抽样次数。第一部分的 `results_main.csv` 没有 `mde` 和 `B_eff` 两列。

市场前缀：`sec` 为二手房（主样本），`new` 为新建商品住宅（对照）。时期：P1 = 2011-01 至 2015-12，P2 = 2016-01 至 2021-12，P3 = 2022-01 至 2026-10；附录 A 的下跌期为 D1\* = 2014-05 至 2015-03，D2\* = 2021-08 至 2026-10。

## 第一部分：`hp_formal/`

| 文件 | 内容 |
|---|---|
| `results_main.csv` | 各检验量和各期水平。`variant` 为 `main`（6 个月块，B = 999）和 6 种稳健性设定：`block3`、`block12`、`deseason`、`cum3`、`q10`、`region`（B = 499） |
| `qr_sec.json`、`qr_new.json` | H4：逐城分位数回归的点估计和自助抽样（B = 299） |
| `qr_sec.log`、`qr_new.log` | 运行日志 |

`variant = main` 中的主要统计量：

| 假设 | 统计量 |
|---|---|
| H1 广度 | `sec.H1_breadth_D2-D1`（日历年窗口，已撤回，见附录 A） |
| H2a 共同趋势 | `sec.H2a_sraw_P3-P1`、`sec.H2a_sraw_P3-P2` |
| H2b 同步波动 | `sec.H2b_sdm_P3-P1`、`sec.H2b_pc1_P3-P1` |
| H3 同时深跌 | `sec.H3_E_P3`（超出高斯基准）、`sec.H3_A_P3`（下尾减上尾）、`sec.H3_dCL_P3-P2` |
| 各期水平 | `sec.level.{P1,P2,P3,D1,D2}.*`：广度、S_raw、S_dm、PC1、下尾和上尾同时超越、高斯基准等 |
| B1、B2 新房对照 | `B1_*_new-sec_P3`、`B2_*` |

## 第二部分：`hp_hetero/`

| 文件 | 内容 |
|---|---|
| `sec_points.json`、`new_points.json` | 点估计：主结果（`main`）、稳健性变体、按实力三等分的分组 |
| `sec_cities.csv`、`new_cities.csv` | 逐城表：实力指数 S 及六个特征、β、累计跌幅 D、K、A、下尾斜率、同时超越等 |
| `sec_main.csv`、`new_main.csv` | 双向自助（6 个月块 + 城市重抽，B = 999） |
| `sec_block3.csv`、`sec_block12.csv` | 块长 3、12 个月（B = 499） |
| `*_draws.csv.gz`、`*.log` | 全部自助抽样、运行日志 |

主要统计量：`M1_rho_S_betaD` 至 `M5_prho_S_beta|V_35`（薄市场闸门）、`H5_rho_S_D`、`H6_rho_S_beta`、`H7_rho_S_A`、`H8a_rho_S_b25`、`H8b_rho_S_b25-b75`、`H9_rho_S_CL`、`rho_D_beta`。

## 第三部分：`hp_qfm/`

| 文件 | 内容 |
|---|---|
| `sec_points.json`、`new_points.json` | 点估计，含 τ = 0.10/0.90 版本、第二个因子（QF5）和随机初值诊断 |
| `sec_factors_P3.csv`、`new_factors_P3.csv` | 2022–26 年各分位数的因子序列与当月截面均值 |
| `sec_boot.csv`、`new_boot.csv` | 自助法（6 个月块，B = 499） |
| `*_draws.csv.gz`、`*.log` | 全部自助抽样、运行日志 |

## 附录 A：`hp_dating/`

| 文件 | 内容 |
|---|---|
| `report_dating.md` | 附录 A 的结果报告 |
| `dating_tests.csv` | H1\*、B2\* 等检验（块长 6 和 3 个月） |
| `dating_desc.json` | 拐点、窗口，以及各轮的持续月数和累计跌幅 |
| `dating_aligned_breadth.csv` | 两轮下跌按距高点月数对齐的下跌城市比例和平均环比 |
| `sec_p3alt_points.json`、`sec_p3alt_cities.csv` | 第二部分按 2021-08 起的窗口重算的点估计和逐城表 |

## 第五部分：`hp_portfolio/`

| 文件 | 内容 |
|---|---|
| [report_portfolio.md](hp_portfolio/report_portfolio.md) | 累计跌幅、坏月份、H-P2 至 H-P6 和稳健性结果 |
| `points.json`、`points.csv` | 主设定、前缀组合与稳健性点估计。JSON 同时保存验算、逐城描述和版本信息 |
| `curves.csv` | 按持有城市数的一行一组统计量，含累计跌幅、坏月份及分位数回归描述 |
| `portfolios_*.csv` | 每种组合抽取规格的城市代码清单，保留抽取顺序 |
| `boot_city.csv`、`boot_time.csv`、`boot_qr.csv` | 城市自助和时间自助，分别为 B = 999、999、499 |
| `bench_qr.csv` | 独立冲击基准（199 次） |
| `*_draws.csv.gz`、`*.log` | 全部自助抽样、基准模拟和运行日志 |
| [deviations_proposed.md](hp_portfolio/deviations_proposed.md) | 拟议偏离与实现约定 |

`delta_cross_n10` 是最差一成组合累计跌幅的差。 `delta_time_n10` 是坏月份收益差。H-P2 闸门和主统计量是 `HP2_omega_bar` 和 `HP2_theta`。城市、时间和分位数回归的自助表另有 `n`、`window`，分别记录持有城市数（城市相关检验为样本城市数）与估计月份范围。

在仓库根目录用 `python scripts/hp_run_portfolio.py ZIP MODE B results/hp_portfolio` 运行，`ZIP` 为本地 CSMAR 压缩包。依次运行 `points 0`、`boot_city 999`、`boot_time 999`、`bench_qr 199`、`boot_qr 499`。`HP_PORTFOLIO_WORKERS` 可设置分位数回归进程数。随机输入保存在本地忽略的 `tmp/` 目录。以相同代码、数据、软件版本和参数重启中断的自助模式会从最近保存的抽样继续。
