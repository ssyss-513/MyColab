import pandas as pd
from champion_map_zh2en import translate_champion, translate_dataframe

# ===========================
# 1️⃣ Load the raw CSV data
# ===========================
df = pd.read_csv("./data/games_player_champion_combined.csv")

# ===========================
# 2️⃣ Convert to long format (one row per player + champion + win)
# ===========================
rows = []
for _, row in df.iterrows():
    for i in range(1, 6):
        # Winning players
        win_col = row.get(f"win{i}")
        if pd.notna(win_col) and "_" in win_col:
            player, champ_cn = win_col.split("_", 1)
            champ_en = translate_champion(champ_cn)  # use mapping function
            rows.append([player, champ_en, 1])  # 1 = win

        # Losing players
        lose_col = row.get(f"lose{i}")
        if pd.notna(lose_col) and "_" in lose_col:
            player, champ_cn = lose_col.split("_", 1)
            champ_en = translate_champion(champ_cn)  # use mapping function
            rows.append([player, champ_en, 0])  # 0 = lose

df_long = pd.DataFrame(rows, columns=["player", "champion", "win"])

# ===========================
# 3️⃣ Compute winrate and pickrate
# ===========================
stats = df_long.groupby(["player", "champion"]).agg(
    games=("win", "count"),
    wins=("win", "sum")
).reset_index()

stats["winrate"] = stats["wins"] / stats["games"]
stats["pickrate"] = stats["games"] / len(df)  # proportion of all matches

# ===========================
# 4️⃣ Round to 4 decimals and export CSV
# ===========================
stats = stats[["player", "champion", "games", "winrate", "pickrate"]]
stats["winrate"] = stats["winrate"].round(4)
stats["pickrate"] = stats["pickrate"].round(4)

stats.to_csv("test.csv", index=False)
print("Top 5 rows:\n", stats.head())
print("Solo stats saved to 'solo_stats_translated.csv'.")
