# Is One Index Enough? 中国工业增长下行风险的因子与个别指标

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
docs/               研究设计与分析协议
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
- [x] 蒙特卡洛脚本
- [ ] 数据整理脚本 → `data/processed/panel_monthly.csv`
- [ ] 描述统计与分析协议
- [ ] 真实数据样本外预测（2×2 设计 + AR-GARCH）
- [ ] 按真实数据校准的第二轮蒙特卡洛
