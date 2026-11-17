# Is One Index Enough? Common Factors, Specific Indicators and Downside Risk to Growth in China

Undergraduate dissertation code (University of Nottingham Ningbo China). The question: when forecasting
downside risk to Chinese industrial growth, do a few common factors use all the information in a large
monthly panel, or do specific indicators add to them? The estimator is the factor-augmented sparse
quantile regression of Yaping Wang (FA-QR: PCA factors unpenalised, l1 penalty on the idiosyncratic
components), compared out of sample with a factor-only model (FO-QR), a sparse-only l1 quantile
regression (SO-QR), the historical quantile and AR-GARCH, in a 2x2 design (real + external indicators
vs. adding Chinese financial indicators; factors only vs. factors + specific indicators).

**Status (2026-11-18).** Model code, rolling pseudo out-of-sample engine, evaluation (pinball loss,
coverage, Diebold-Mariano) and a Monte Carlo study are written and tested (`python -m pytest`).
The Chinese monthly panel is being assembled (CSMAR, PBoC, FRED); no results on real data yet.

## Preliminary Monte Carlo results

> **Preliminary.** 3-5 replications per design on a generic data-generating process; persistence
> values are guesses, not calibrated to Chinese data. These results are meant for discussing the
> design, not for the dissertation. Details (in Chinese): `docs/montecarlo_preliminary.md`.

**Set-up.** T = 260 months, p = 100 indicators, 3 factors, 120-month rolling window (about 140
out-of-sample forecasts), h = 1, tau = 0.10 / 0.25 / 0.50. Inside each window: standardisation, PCA,
number of factors by the eigenvalue ratio (r_max = 8), penalty by blocked time-series cross-validation
with a 12-month gap. Target = own lag (High setting only) + factor part + idiosyncratic part + Student-t(3) noise whose
scale depends on one idiosyncratic component (so it matters for the tails only).
Worlds: *dense* (factors only), *sparse* (5 idiosyncratic components), *mixed* (both), *case A*
(a factor loading on a block of 10 indicators, missed by PCA). Factor loadings scaled by p^((alpha-1)/2),
strong alpha = 1, weak alpha = 0.6. Two persistence settings: *Low* (AR(1) of factors 0.5,
idiosyncratic 0.3, target 0) and *High* (0.9, 0.8, 0.5; closer to year-on-year Chinese series).

**FA-QR relative to FO-QR**: mean pinball-loss ratio (below 1 = FA-QR better), and in brackets the
share of replications in which a one-sided DM test at 10% says FA-QR is better (power where FA-QR
should win, false rejections in the dense worlds).

| World | Factors | Low: τ=0.10 | Low: τ=0.25 | Low: τ=0.50 | High: τ=0.10 | High: τ=0.25 | High: τ=0.50 |
|---|---|---|---|---|---|---|---|
| Dense | strong | 1.01 (0%) | 1.01 (0%) | 1.00 (0%) | 1.04 (0%) | 1.01 (0%) | 1.00 (0%) |
| Dense | weak | 0.99 (20%) | 1.00 (20%) | 1.00 (40%) | 0.97 (33%) | 0.98 (33%) | 0.94 (67%) |
| Sparse | strong | 1.01 (0%) | 0.86 (100%) | 0.76 (100%) | 1.05 (0%) | 0.92 (100%) | 0.90 (67%) |
| Sparse | weak | 0.97 (40%) | 0.79 (100%) | 0.72 (100%) | 1.05 (33%) | 0.93 (100%) | 0.89 (100%) |
| Mixed (case B) | strong | 0.95 (40%) | 0.79 (100%) | 0.70 (100%) | 1.04 (0%) | 0.93 (100%) | 0.85 (100%) |
| Mixed (case B) | weak | 1.00 (20%) | 0.86 (100%) | 0.75 (100%) | 1.04 (33%) | 1.01 (0%) | 0.99 (33%) |
| Case A (weak block factor) | strong | 0.92 (40%) | 0.79 (100%) | 0.78 (100%) | 1.05 (0%) | 0.94 (67%) | 0.94 (100%) |
| Case A (weak block factor) | weak | 1.00 (0%) | 0.96 (40%) | 0.93 (60%) | 1.00 (33%) | 0.97 (67%) | 0.91 (100%) |

**What the trial runs suggest**

1. At tau = 0.25 and 0.50 the comparison has power: when specific indicators carry information and
   factors are strong, FA-QR wins and the DM test detects it; no false rejections with strong factors.
2. At tau = 0.10 there is little power, and under high persistence FA-QR is slightly worse than FO-QR
   in 6 of 8 designs (coverage of FA-QR 11-16% against a nominal 10%). With about 108 estimation pairs
   per window the 10% quantile is estimated too imprecisely.
3. Weak factors are mistaken for specific information: in the dense world with weak factors, the DM
   test favours FA-QR in 20-67% of replications. PCA leaves part of the weak common component in the
   idiosyncratic residuals, and the lasso picks it up.
4. Selection is noisy: of 5 true signals, about 4 (low persistence) or 2-3 (high persistence) are
   selected per window at tau = 0.25 / 0.50, together with many false ones.

**Design questions to discuss**

- Use tau = 0.25 as the main lower-tail quantile and report tau = 0.10 as secondary, with its power?
- Make r + 1 and r + 2 factors (and possibly another estimator of r) a required check before reading an
  FA-QR gain as evidence of specific information?
- Read selection frequencies only descriptively, and attribute gains to indicator groups by dropping groups?
- Next step: a semi-synthetic Monte Carlo on the real Chinese panel (real predictors, simulated target
  with residuals resampled from the real forecasting errors), including indicator groups so that the
  "does financial information help" comparison is also checked.

---

# 中文说明

本科毕业论文代码仓库。研究问题：预测中国工业增长的下行风险时，少数共同因子是否已经概括了大量宏观金融指标中的信息，还是个别指标另有增量。方法沿用 Yaping Wang 的因子增强稀疏分位数回归（FA-QR），在滚动窗口的伪样本外预测中与基准比较，并用蒙特卡洛模拟检验比较的可靠性。

## 目录结构

```
src/gar/            核心代码（可被所有脚本调用）
  qr.py             分位数回归（线性规划求解）及 l1 惩罚、lambda_max
  factors.py        标准化、主成分因子、特征值比率法选因子个数
  tuning.py         时间序列交叉验证（验证段前留隔离带）选惩罚参数
  garch.py          AR-GARCH(1,1) 基准（Brownlees and Souza, 2021）
  models.py         HIST、AR-GARCH、FO-QR（纯因子）、SO-QR（纯稀疏）、FA-QR（因子+稀疏）
  engine.py         滚动窗口伪样本外预测
  evaluation.py     分位数损失、覆盖率、Diebold-Mariano 检验、汇总表
  simulate.py       蒙特卡洛的数据生成：四种世界 × 强弱因子 × 尾部渠道
scripts/
  check_env.py      检查 Python 环境
  00_smoke_test.py  在一套模拟数据上跑通全流程（约 1–3 分钟）
  01_monte_carlo.py 蒙特卡洛研究（可断点续跑、可并行）
tests/              单元测试（含"不偷看未来"的测试）
data/               数据说明（数据本身不进仓库）
results/            运行结果（不进仓库，可由脚本重新生成）
docs/               研究设计、分析协议、蒙特卡洛初步结果
```

## 环境

Anaconda 自带的 base 环境即可（Python 3.9 及以上，需要 numpy、scipy ≥ 1.6、pandas，蒙特卡洛并行需要 joblib）。**不要用为 CSMAR 接口建的 csmar36 环境**，那个版本太旧。

```
cd 仓库所在文件夹
python scripts/check_env.py
python -m pytest -q
```

## 运行

```
python scripts/00_smoke_test.py                       # 默认：mixed 世界，强因子
python scripts/00_smoke_test.py --world caseA --alpha 0.6
python scripts/01_monte_carlo.py --reps 2 --jobs 2    # 试跑
python scripts/01_monte_carlo.py --reps 100 --jobs 4  # 正式（数小时；中断后重跑会跳过已完成的部分）
python scripts/01_monte_carlo.py --summarise          # 汇总已有结果
```

## 主要约定

- **直接 h 步预测**：用第 t 月的指标预测第 t+h 月的目标；估计窗口为截至预测时点的 120 个月，窗口内的标准化、主成分、因子个数和惩罚参数都只用窗口内数据。
- **发布滞后在建面板时处理**：面板第 t 行只能包含第 t 月月底前已发布的信息，模型代码不再另行处理。
- **信息集**：每个模型可用 `columns=[...]` 限定可用指标。2×2 设计中，A/B 用实体与外部指标，C/D 再加入中国金融指标；B/D 为 FA-QR，A/C 为 FO-QR。
- **窗口内缺失的指标自动剔除**：晚起步的序列在数据完整之前不会进入该窗口。
- **目标缺失（1 月）**：训练时跳过目标缺失的样本对，评分时跳过没有实现值的月份；自身滞后项用最近一次公布的值。

## 尚待确定的设计选择（写进分析协议后再跑真实数据）

| 选项 | 当前默认 | 说明 |
|---|---|---|
| 交叉验证分位数 `cv_tau` | 在各自分位数上调参 | 10% 分位数样本薄，可改为在 0.5 上调参后通用 |
| 隔离带 `gap` | 12 个月 | 同比增速前后 12 个月重叠 |
| 重新调参频率 `retune_every` | 每 12 个预测时点 | 其余时点沿用相对惩罚强度 |
| 因子个数 | 特征值比率法，上限 8 | 稳健性：r+1、r+2 |
| DM 检验的长期方差滞后阶 | max(h−1, 1.5·T^(1/3)) | |
| 2021 年基期效应 | 未处理 | 两年平均增速或剔除 2020–2022 |

## 进度

- [x] 模型与评价代码、单元测试、冒烟测试
- [x] 蒙特卡洛脚本；初步结果见 `docs/montecarlo_preliminary.md`
- [ ] 数据整理脚本 → `data/processed/panel_monthly.csv`
- [ ] 描述统计与分析协议
- [ ] 真实数据样本外预测（2×2 设计 + AR-GARCH）
- [ ] 按真实数据校准的第二轮蒙特卡洛
