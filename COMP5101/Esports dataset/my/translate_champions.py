# translate_champions.py

import pandas as pd
# 从 champion_map.py 文件中导入字典
from champion_map import CHAMPION_TRANSLATION_MAP

def translate_champions(file_path, translation_map):
    """
    加载CSV文件，将'champion'列的英文英雄名转换为中文，
    并在新的'champion_cn'列中显示结果。
    
    Args:
        file_path (str): CSV文件路径。
        translation_map (dict): 英文到中文英雄名的映射字典。

    Returns:
        pd.DataFrame: 包含中文英雄名的新DataFrame。
    """
    print(f"📄 正在加载文件: {file_path}")
    try:
        # 加载CSV文件
        df = pd.read_csv(file_path)

        # 检查'champion'列是否存在
        if 'champion' not in df.columns:
            print("🚨 错误: CSV文件中未找到 'champion' 列。请检查列名是否正确。")
            return None

        # 使用映射字典将'champion'列的值进行替换
        # .map() 方法：对'champion'列的每个值，查找字典中的对应中文名。
        # .fillna(df['champion'])：如果字典中没有找到（即返回NaN），则保留原英文名。
        df['champion_cn'] = df['champion'].map(translation_map).fillna(df['champion'])

        print("✅ 英雄名转换完成。")
        print("以下是前10行数据中英文名的对比:")
        print("---" * 15)
        print(df[['champion', 'champion_cn', 'player', 'kills', 'deaths', 'assists']].head(10))
        print("---" * 15)
        
        return df

    except FileNotFoundError:
        print(f"❌ 错误: 文件未找到 - {file_path}。请确保文件在正确的目录下。")
        return None
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        return None

# --- 配置和执行 ---
input_file = "MyColab/COMP5101/Esports dataset/my/2021_worlds_kda_final.csv"
output_file = "2021_worlds_kda_final_cn.csv"

df_translated = translate_champions(input_file, CHAMPION_TRANSLATION_MAP)

# 保存新的文件
if df_translated is not None:
    print(f"\n💾 正在保存新文件至: {output_file}")
    # 使用 encoding='utf-8-sig' 确保中文在 Excel 中显示正常
    df_translated.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"🎉 文件已成功保存！")