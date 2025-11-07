import pandas as pd

# --- 配置 ---
INPUT_FILE = '24world_teams.csv'  # 输入文件名
OUTPUT_FILE = '24world_teams_processed.csv' # 输出文件名
# --- 配置结束 ---

try:
    # 1. 读取 CSV 文件
    df = pd.read_csv(INPUT_FILE)
    print(f"成功读取文件: {INPUT_FILE}")

    # 2. 定义一个函数来去除队名
    def remove_team_prefix(full_name):
        try:
            # 假设格式为 "TEAM PlayerName"，分割并返回第二部分
            return full_name.split(' ', 1)[1]
        except (AttributeError, IndexError):
            # 如果格式不符或已经是纯名字，返回原值
            return full_name

    # 3. 将这个函数应用到 'player' 列
    df['player'] = df['player'].apply(remove_team_prefix)
    print("已成功移除 'player' 列中的队名。")

    # 4. 保存到新的 CSV 文件
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"处理后的数据已保存到: {OUTPUT_FILE}")

    # 5. 显示处理后的数据预览
    print("\n处理后数据预览:")
    print(df.head())

except FileNotFoundError:
    print(f"错误: 输入文件 '{INPUT_FILE}' 未找到。")
except Exception as e:
    print(f"发生错误: {e}")
