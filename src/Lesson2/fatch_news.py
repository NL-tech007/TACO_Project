import feedparser
from urllib.parse import quote_plus
 
# Google News RSS：按关键词搜索
query = "Trump tariff"
 
# URL 里不能直接放空格，所以要先编码
# "Trump tariff" 会变成 "Trump+tariff"
query_encoded = quote_plus(query)
 
url = f"https://news.google.com/rss/search?q={query_encoded}&hl=en-US&gl=US&ceid=US:en"
 
print("实际访问的 RSS 地址：")
print(url)
print("-" * 40)
 
rss = feedparser.parse(url)
 
if len(rss.entries) == 0:
    print("没有抓取到新闻，请检查网络或 RSS 地址。")
else:
    for entry in rss.entries[:5]:
        print("标题：", entry.get("title", ""))
        print("时间：", entry.get("published", ""))
        print("摘要：", entry.get("summary", ""))
        print("---")
    