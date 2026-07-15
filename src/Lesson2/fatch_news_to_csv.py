# ==============================
# TACO 第2次课 示例3
# 把 RSS 新闻保存成 CSV
# 文件名：fetch_news_to_csv.py
# ==============================
 
import feedparser
import pandas as pd
from pathlib import Path
from urllib.parse import quote_plus
 
# 当前文件在 src/lesson2 中
# parents[2] 可以回到 TACO_Project 根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]
 
# data 文件夹
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
 
 
def fetch_trump_news(keywords, max_results=20):
    """
    根据关键词列表抓取特朗普相关新闻。
    """
 
    query = "Trump " + " ".join(keywords)
    query_encoded = quote_plus(query)
 
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=en-US&gl=US&ceid=US:en"
 
    print("搜索关键词：", query)
    print("RSS 地址：", url)
 
    rss = feedparser.parse(url)
 
    news_data = []
 
    for entry in rss.entries[:max_results]:
        news_data.append({
            "title": entry.get("title", ""),
            "date": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", "")
        })
 
    return news_data
 
 
# 抓取新闻
news_data = fetch_trump_news(["tariff", "trade"], max_results=20)
 
# 转成 DataFrame
df_news = pd.DataFrame(news_data)

# 判断是否成功抓取
if len(df_news) == 0:
    print("没有抓取到新闻，请检查网络或 RSS 地址。")
else:
    print("/n新闻抓取预览：")
    print(df_news.head())
    output_path = DATA_DIR / "raw_news.csv"
    df_news.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("\n原始数据以保存到：")
    print(output_path)
