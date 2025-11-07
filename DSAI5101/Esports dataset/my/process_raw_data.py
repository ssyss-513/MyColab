import pandas as pd
import sqlite3

# --- 配置 ---
# 请将 'your_database.db' 替换为您的 SQLite 数据库文件名
DATABASE_FILE = '../your_database.db'
# 请将 'matches' 替换为存储比赛数据的表名
TABLE_NAME = 'matches'
# --- 配置结束 ---

try:
    # 1. 连接到 SQLite 数据库
    conn = sqlite3.connect(DATABASE_FILE)

    # 2. 编写 SQL 查询语句，从指定的表中选择所有数据
    query = f"SELECT * FROM {TABLE_NAME}"

    # 3. 使用 pandas 直接从数据库读取数据到 DataFrame
    #   这样比手动读取更高效，并且 pandas 会自动处理列名
    df_raw = pd.read_sql_query(query, conn)

    # 4. 关闭数据库连接
    conn.close()

    print(f"成功从数据库 '{DATABASE_FILE}' 的 '{TABLE_NAME}' 表中读取数据。")

    # 5. 创建一个空列表，用于存储转换后的每一行数据
    processed_rows = []

    # 6. 遍历原始数据的每一行（即每一场比赛）
    for _, row in df_raw.iterrows():
        game_id = row['gameId']
        
        # 根据 'win' 列确定蓝红方的胜负状态
        blue_win_loss = 'Win' if row['win'] == 1 else 'Loss'
        red_win_loss = 'Loss' if row['win'] == 1 else 'Win'
        
        # 提取队伍名称（假设队名是选手名的前缀，例如 "MDK Myrwn" -> "MDK"）
        # 使用 try-except 避免没有空格的名字报错
        try:
            blue_team_name = row['bluePlayer1Name'].split(' ')[0]
            red_team_name = row['redPlayer1Name'].split(' ')[0]
        except (AttributeError, IndexError):
            blue_team_name = 'BLUE' # 如果无法分割，则使用默认队名
            red_team_name = 'RED'

        # 处理蓝色方5名选手
        for i in range(1, 6):
            player_name = row[f'bluePlayer{i}Name']
            champion_pick = row[f'bluePlayer{i}Pick']
            
            processed_rows.append({
                'gameid': game_id,
                'team': blue_team_name,
                'player': player_name,
                'champion': champion_pick,
                'win_loss': blue_win_loss
            })

        # 处理红色方5名选手
        for i in range(1, 6):
            player_name = row[f'redPlayer{i}Name']
            champion_pick = row[f'redPlayer{i}Pick']
            
            processed_rows.append({
                'gameid': game_id,
                'team': red_team_name,
                'player': player_name,
                'champion': champion_pick,
                'win_loss': red_win_loss
            })

    # 7. 将处理好的行列表转换为 DataFrame
    df_processed = pd.DataFrame(processed_rows)

    # 8. 保存为 16_teams.csv 文件
    output_filename = '16_teams.csv'
    df_processed.to_csv(output_filename, index=False)

    print(f"数据已成功处理并保存到 '{output_filename}' 文件中。")
    print("\n文件内容预览:")
    print(df_processed.head())

except sqlite3.Error as e:
    print(f"数据库错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")
