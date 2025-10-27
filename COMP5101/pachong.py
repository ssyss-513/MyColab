import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- 1. 爬虫身份设置（User-Agent） ---
# 必须使用自定义的、不在黑名单中的 User-Agent，以示礼貌和合规
HEADERS = {
    'User-Agent': 'LoLWorlds2021AnalysisBot/1.0 (Contact: user_provided_email@example.com)',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8' # 尽量获取中文内容，方便后续处理
}

# --- 2. 目标 URL 列表 (待填写) ---
# **重要提醒：你需要手动填写所有小组赛比赛详情页的 URL 列表。**
# 每一个 URL 都必须是形如：https://liquipedia.net/leagueoflegends/World_Championship/2021/Group_Stage/Match_Details/...
MATCH_URLS = [
    # 比赛 1 URL：请填写
    'https://liquipedia.net/leagueoflegends/World_Championship/2021/Group_Stage/Match_Details/...',
    # 比赛 2 URL：请填写
    # '...', 
    # ... 请继续添加所有比赛的 URL
]

# 最终存储结果的列表
all_match_data = []

# --- 3. 核心爬取逻辑 ---
def crawl_match_details(url):
    print(f"尝试抓取 URL: {url}...")
    
    try:
        # 发送请求
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # 检查响应状态
        if response.status_code != 200:
            print(f"错误：请求失败，状态码 {response.status_code}")
            return None

        # 使用 pandas 尝试直接读取页面中的表格
        # Liquipedia 的 Ban/Pick 通常在页面上的一个 HTML 表格中
        df_list = pd.read_html(response.text)
        
        # **手动识别正确的 Ban/Pick 表格**
        # 在 Liquipedia 页面上，Ban/Pick 数据通常位于一个独特的表格中。
        # 你需要根据实际页面结构来确定哪个 DataFrame (例如 df_list[0] 或 df_list[1]) 是 Ban/Pick 数据。
        
        # 以下是基于常见 Liquipedia 结构的一个推测性提取，可能需要根据实际 HTML 进行调整：
        
        ban_pick_data = None
        match_result = {} # 用于存储胜负关系
        
        # 使用 Beautiful Soup 提取胜负关系（通常在页面顶部）
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # **此处你需要检查页面上表示胜负结果的 HTML 元素和其类名/ID，并替换下面留空的部分。**
        winning_team_element = soup.find('div', class_='team-template-win') 
        losing_team_element = soup.find('div', class_='team-template-loss')
        
        if winning_team_element and losing_team_element:
            # 胜负队名通常在团队模板的子元素中
            winner_name = winning_team_element.find('span', class_='team-template-text').text.strip()
            loser_name = losing_team_element.find('span', class_='team-template-text').text.strip()
            match_result['Winner'] = winner_name
            match_result['Loser'] = loser_name
            
        # 假设 Ban/Pick 表格是页面上的第一个复杂表格（这需要验证）
        if df_list:
            ban_pick_df = df_list[0] 
            # 提取 Ban/Pick 数据到字典中
            ban_pick_data = ban_pick_df.to_dict(orient='records') 
        
        # 整合数据
        if match_result and ban_pick_data:
            match_data = {
                'URL': url,
                'Result': f"{match_result.get('Winner')} 胜 {match_result.get('Loser')} 负",
                'BanPick_Data': ban_pick_data
            }
            all_match_data.append(match_data)
            print(f"成功抓取比赛数据：{match_result.get('Winner')} vs {match_result.get('Loser')}")
        else:
            print("未能提取完整的比赛结果或 Ban/Pick 数据。请检查 HTML 结构定位。")


    except Exception as e:
        print(f"抓取 {url} 时发生错误: {e}")
    
    # --- 4. 遵守低速原则 ---
    # 每次请求后至少暂停 5 秒，以降低服务器压力，防止被封锁。
    time.sleep(5)
    print("暂停 5 秒...")


# --- 5. 执行抓取 ---
if not MATCH_URLS:
    print("\n请先在 MATCH_URLS 列表中填写 2021 年全球总决赛小组赛所有比赛的详情页 URL。")
else:
    print("\n--- 开始低速爬取数据 ---")
    for url in MATCH_URLS:
        crawl_match_details(url)
    
    # 将结果保存为 CSV
    final_df = pd.DataFrame(all_match_data)
    # final_df.to_csv('worlds_2021_banpick_data.csv', index=False, encoding='utf-8-sig')
    print("\n--- 爬取完成 ---")
    print(f"总共成功抓取 {len(all_match_data)} 场比赛数据。结果存储在 all_match_data 列表中。")


# === 待你自己填写的部分 ===
# 1. 爬虫身份：请将 `user_provided_email@example.com` 替换为你自己的邮箱，以创建一个更礼貌的 User-Agent。
# 2. 目标 URL 列表：请在 `MATCH_URLS` 列表中填写所有 2021 年全球总决赛小组赛比赛的详情页链接。
# 3. HTML 结构：如果你发现 Ban/Pick 数据提取不正确，你需要使用浏览器的“检查元素”功能，确定 Liquipedia 上 Ban/Pick 表格和胜负队伍名称所在的具体 HTML 标签、ID 或 Class Name，并相应调整 `BeautifulSoup` 的查找逻辑。