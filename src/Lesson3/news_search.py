# =======================================
# TACO 作业 1
# 新闻搜索小助手
# 文件名: homework_news_search.py
# =======================================

import feedparser
import pandas as pd
from urllib.parse import quote_plus
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "homework_news.csv"

# 让用户输入关键词
query = input("请输入新闻关键词，例如 Trump tariff: ")

# URL 里不能直接有空格，所以要编码
query_encoded = quote_plus(query)

# Bing News RSS
url = f"https://www.bing.com/news/search?q={query_encoded}&format=rss"

print("\n实际访问的 RSS 地址: ")
print(url)
print("-" * 50)

rss = feedparser.parse(url)

news_list = []

if len(rss.entries) == 0:
    print("没有抓取到新闻，请尝试换一个关键词，例如 Trump。")

else:
    for entry in rss.entries[:10]:
        title = entry.get("title", "")
        published = entry.get("published", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        
        print("标题: ", title)
        print("时间: ", published)
        print("摘要: ", summary)
        print("链接: ", link)
        print("-" * 50)
        
        news_list.append({
            "title": title,
            "published": published,
            "summary": summary,
            "link": link
        })

df = pd.DataFrame(news_list)
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\n新闻已保存到: ")
print(OUTPUT_FILE)