import pandas as pd
import numpy as np
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# === 1️⃣ 读取数据 ===
matches = pd.read_csv("./data/2021_worlds_kda_with_result.csv")
solo = pd.read_csv("./data/solo_stats.csv")

# === 2️⃣ 过滤单排数据，只保留玩过至少 2 场该英雄的记录 ===
if 'games' in solo.columns:
    solo = solo[solo['games'] >= 1].copy()

print(f"✅ 保留的单排记录数: {len(solo)}")

# === 3️⃣ 建立 player+champion 到 winrate/pickrate/games 的映射 ===
solo_dict = solo.set_index(["player", "champion"])[["winrate", "pickrate", "games"]].to_dict("index")

def get_stat(player, champ, key):
    try:
        return solo_dict[(player, champ)][key]
    except KeyError:
        return np.nan  # 如果该组合在单排数据中找不到

# === 4️⃣ 为每位选手添加单排特征 ===
matches["solo_winrate"] = matches.apply(lambda x: get_stat(x["player"], x["champion"], "winrate"), axis=1)
matches["solo_pickrate"] = matches.apply(lambda x: get_stat(x["player"], x["champion"], "pickrate"), axis=1)
matches["solo_games"] = matches.apply(lambda x: get_stat(x["player"], x["champion"], "games"), axis=1)

# === 5️⃣ 按 gameid + team 聚合到队伍级别 ===
team_stats = matches.groupby(["gameid", "team", "win_loss"]).agg(
    team_avg_winrate=("solo_winrate", "mean"),
    team_avg_pickrate=("solo_pickrate", "mean"),
    team_avg_games=("solo_games", "mean")
).reset_index()

# === 6️⃣ 将同一场比赛的两支队伍合并到同一行 ===
games = team_stats.merge(team_stats, on="gameid", suffixes=("_A", "_B"))
games = games[games["win_loss_A"] != games["win_loss_B"]]  # 去除重复组合

# === 7️⃣ 确定 A 队是否获胜（label） ===
games["A_win"] = (games["win_loss_A"] == "Win").astype(int)

# === 8️⃣ 计算特征差值 ===
games["winrate_diff"] = games["team_avg_winrate_A"] - games["team_avg_winrate_B"]
games["pickrate_diff"] = games["team_avg_pickrate_A"] - games["team_avg_pickrate_B"]
games["games_diff"] = games["team_avg_games_A"] - games["team_avg_games_B"]  # 新增特征

# === 9️⃣ 建模 ===
X = games[["winrate_diff", "pickrate_diff", "games_diff"]]
y = games["A_win"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = RandomForestClassifier(n_estimators=800, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("✅ Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("✅ F1 Score:", round(f1_score(y_test, y_pred), 3))

# === 10️⃣ 查看特征重要性 ===
importances = pd.Series(model.feature_importances_, index=X.columns)
print("\nFeature Importance:")
print(importances.sort_values(ascending=False))

# estimator = model.estimators_[0]

# # 绘制决策树
# plt.figure(figsize=(20, 10))  # 调整大小
# tree.plot_tree(
#     estimator,
#     feature_names=X.columns,
#     class_names=["Loss", "Win"],
#     filled=True,
#     rounded=True,
#     fontsize=12
# )
# plt.title("Decision Tree - Split Visualization")
# plt.show()