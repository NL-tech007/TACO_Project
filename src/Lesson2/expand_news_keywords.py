# ==================================
# TACO 第2次课 作业参考代码1
# 扩展关键词列表抓取新闻（已根据作业要求改进）
# ==================================

import feedparser
import pandas as pd
from pathlib import Path
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

def fetch_trump_news(keywords, output_name, max_results=20):
    """
    根据关键词列表抓取特朗普相关新闻，并保存成 CSV。
    满足要求：每组至少抓取 10 条（默认为 20 条），输出标题、时间、摘要。
    """
    
    # 组合关键词
    query = "Trump " + " ".join(keywords)
    query_encoded = quote_plus(query)
    
    # Google News RSS 链接
    url = f"https://news.google.com/rss/search?q={query_encoded}&hl=en-US&gl=US&ceid=US:en"
    
    rss = feedparser.parse(url)
    
    news_data = []
    
    # 遍历并提取新闻的标题(title)、时间(published)、摘要(summary)、链接(link)
    for entry in rss.entries[:max_results]:
        news_data.append({
            "title": entry.get("title", ""),
            "date": entry.get("published", ""),    # 时间
            "summary": entry.get("summary", ""), # 摘要
            "link": entry.get("link", "")
        })
        
    df = pd.DataFrame(news_data)
    
    # 保存为 CSV 文件
    output_path = DATA_DIR / output_name
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    
    print("搜索关键词：", query)
    print("保存路径：", output_path)
    print("新闻数量：", len(df))
    print(df.head())
    print("-" * 50)

# ==================================
# 执行部分：根据作业要求，至少选择 3 组，这里将 4 组全部实现
# ==================================

# 1. 关税与贸易领域
fetch_trump_news(["tariff", "trade"], "trump_tariff_trade_news.csv")

# 2. 石油与欧佩克领域
fetch_trump_news(["oil", "OPEC"], "trump_oil_opec_news.csv")

# 3. 芯片与半导体领域
fetch_trump_news(["chip", "semiconductor"], "trump_chip_news.csv")

# 4. 美元与美联储领域（新增满足作业图片中的第四组要求）
fetch_trump_news(["dollar", "Fed"], "trump_dollar_fed_news.csv")