# COMP5101 Project — Esports Data Analysis

## 📁 项目目录结构

```text
.
├── Esports dataset
│   ├── my        # 数据和代码
│   ├── pic       # 图片或可视化结果
│   └── data      # 原始数据文件
├── player_winrate_over10.csv
├── position_stats_combined.csv
└── README.md
```

---

## 📊 数据集说明

### 1️⃣ 数据文件

- **`player_winrate_over10.csv`**: 玩家胜率数据，包含至少10场比赛的玩家统计。
- **`position_stats_combined.csv`**: 不同位置的综合统计数据。
- **`Esports dataset/my/data`**: 包含英雄胜率、玩家胜率等详细数据文件（如`position_stats.txt`）。
- **`Esports dataset/my/2021_worlds_kda_final.csv`**: 2021年世界赛的KDA数据。

### 2️⃣ 分析脚本

- **`Esports dataset/my/champion_map.py`**: 英雄中英文名称映射。
- **`Esports dataset/my/champion_map_zh2en.py`**: 英雄中文到英文名称的映射。
- **`Esports dataset/my/randomForest_XGB.ipynb`**: 使用随机森林和XGBoost进行预测分析。
- **`Esports dataset/my/choice_16.py`**: 选取进入世界赛正赛的队伍。

### 3️⃣ 可视化结果

- **`Esports dataset/pic`**: 存储分析结果的图片，如胜率分布、Pick/Ban统计等。

---

## 🚀 安装与运行

### 1️⃣ 克隆仓库

```bash
git clone <repository_url>
cd COMP5101
```

### 2️⃣ 安装依赖

确保已安装以下Python库：

```bash
pip install pandas numpy matplotlib scikit-learn xgboost
```

### 3️⃣ 运行分析脚本

运行Jupyter Notebook或Python脚本：

---

## 📈 功能与分析

### 1️⃣ 数据预处理

- 使用[`champion_map_zh2en.py`](Esports%20dataset/my/champion_map_zh2en.py)将英雄名称从中文翻译为英文。
- 数据清洗与格式化，确保一致性。

### 2️⃣ 数据分析

- **玩家胜率分析**: 统计玩家的胜率和总场次。
- **英雄胜率分析**: 计算英雄的胜率、选择率和Ban率。
- **位置统计**: 分析不同位置的玩家和英雄表现。

### 3️⃣ 机器学习

- 使用随机森林和XGBoost模型预测比赛结果。
- 特征重要性分析，评估影响胜率的关键因素。

---

## 📊 示例结果

- **玩家胜率排名**:
  - `Tactical`: 胜率 71.4%（35胜/49场）
  - `Gumayusi`: 胜率 64.9%（61胜/94场）

- **英雄胜率排名**:
  - `残月之肃 (Aphelios)`: 胜率 63.3%（95胜/150场）
  - `圣枪游侠 (Lucian)`: 胜率 63.2%（225胜/356场）

- **机器学习模型性能**:
  - 随机森林准确率: 62.3%
  - XGBoost准确率: 73.8%

---

## 📜 许可证

本项目遵循MIT许可证，详情请参阅[LICENSE](LICENSE)文件。

---
