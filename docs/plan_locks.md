# 方案锁定记录

每份分析方案在正式估计前写定，计算 SHA-256 并提交，然后才运行。锁定后的改动只追加在方案文末的“偏离记录”里，正文不动。

| 方案 | 文件 | 锁定时间（UTC） | 锁定版本的 SHA-256 |
|---|---|---|---|
| 第一部分：广度、共同成分、同时深跌、新房对照（H1–H4、B1、B2） | `analysis_plan_hp_20261124.md` | 2026-11-24 | 当时未单独记录 |
| 第二部分：城市异质性（薄市场闸门 M、H5–H9） | `analysis_plan_hp_part2_hetero_20261124.md` | 2026-11-24 13:30 | `d8cc3f73203f860838de10c6ceef760803888d96c3f36a7550371722110d8800` |
| 第三部分：分位数因子（QF1–QF5） | `analysis_plan_hp_part3_qfm_20261124.md` | 2026-11-24 14:27 | `426782a6e63475408a1b640d3023ef3c86d5af0d39a7ba213ba9d8b47e6aaa60` |
| 附录 A：下跌期按拐点重划 | `analysis_plan_hp_part4a_dating_20261125.md` | 2026-11-25 10:07:30 | `06df109e79e382e7d9206f26073c9333a252376c07c5d297a7c145909d0a7d90` |
| 第五部分：跨城持有的分散效果（H-P2 至 H-P6） | `analysis_plan_hp_part5_portfolio_20261127.md` | 2026-11-26 18:35:34 | `0fcd2687347df5e67835ec286301329637455157ec0bc49abb30a9de79910ad3` |

第五部分的方案在运行前算出 SHA-256 并记入本表，但方案文件和本表这一行到 2026-11-27 才第一次提交进 Git，晚于运行（见 `results/hp_portfolio/deviations_proposed.md` 第 11 条）。`scripts/hp_run_portfolio.py` 每次运行前都按这一哈希核对方案文件，不一致就停止。

核对方法（在仓库根目录运行）。第二、三部分去掉文末追加的“重录”行后，就是锁定原版：

```bash
sed '/（重录）/d' docs/analysis_plan_hp_part2_hetero_20261124.md | sha256sum
sed '/（重录）/d' docs/analysis_plan_hp_part3_qfm_20261124.md | sha256sum
sha256sum docs/analysis_plan_hp_part4a_dating_20261125.md
sha256sum docs/analysis_plan_hp_part5_portfolio_20261127.md
```

Windows 上如果检出时换行被改成了 CRLF，`sha256sum` 会对不上，可以先把 CRLF 换成 LF 再算，例如：

```bash
python -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read().replace(b'\r\n',b'\n')).hexdigest())" docs/analysis_plan_hp_part5_portfolio_20261127.md
```

待锁定：附录 B（机制，`analysis_plan_hp_part4b_mechanism_20261127.md`）目前是草稿，锁定前要作者确认三件事（主区间用哪种自助法、H-B1 是否保留、H-B3 是否放在附录 B），见该文件第 9 节；附录 C（检验力模拟与阳性对照）还没有写。两者计划在 2026 年 12 月锁定并运行。

## 仓库重建说明（2026-11-26）

2026-11-26 旧仓库清空后，本仓库按 Claude 会话中保存的副本重建：

- `scripts/` 与原仓库提交时的版本一致。只有 `hp_run_main.py`、`hp_run_qr.py` 的模块路径从固定路径改为脚本所在目录，计算部分没有改动。
- `results/` 中的汇总表、自助抽样和日志与原仓库一致。
- 三份结果报告（`results/hp_formal/report.md`、`results/hp_hetero/report_hetero.md`、`results/hp_qfm/report_qfm.md`）的原文没有保存，2026-11-26 根据同目录的结果文件重写。数字取自结果文件，文字与原报告不同。
- 锁定后追加的偏离记录中，有几行原文没有保存。已知内容据研究计划（2026-11-26 版）、代码注释和结果文件重录，都标为“（重录）”。第三部分方案原来可能还有其他偏离行，内容无法找回；锁定原版和全部结果文件都在，需要时可以重跑核对。
