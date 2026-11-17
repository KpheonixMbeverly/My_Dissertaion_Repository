# 数据说明

**原始数据不放进 Git 仓库。** CSMAR 数据受学校授权协议约束，不能公开传播；原始文件也较大。

- 原始下载文件目前在：`C:\Users\Lenovo\Desktop\Y4\Claude工作区\claude工作区\data\raw\`（CSMAR、FRED、央行），
  登记表为同一文件夹下的 `数据登记表.csv`。
- 整理脚本完成后，按以下结构在本文件夹下生成（均已在 `.gitignore` 中排除）：
  - `data/raw/`：原始文件的副本或链接
  - `data/interim/`：逐个序列清洗后的结果
  - `data/processed/panel_monthly.csv`：建模用的月度宽表（每行一个月，每列一个指标）
  - `data/processed/series_info.csv`：每个指标的组别、变换方式、发布滞后、起止时间
- 可以提交到仓库的只有：本说明、数据字典和整理脚本本身。

如果以后把仓库推送到 GitHub，请设为 **Private**，并在推送前确认 `git status` 里没有任何数据文件。
