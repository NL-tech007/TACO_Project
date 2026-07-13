# ==============================

# RSS 新闻抓取：BBC Business 版本

# ==============================

# 导入 feedparser，用来解析 RSS 新闻

import feedparser

# BBC Business RSS 地址

# 这个地址用于获取 BBC 商业新闻

url = "http://feeds.bbci.co.uk/news/business/rss.xml"

# 解析 RSS

feed = feedparser.parse(url)

# 判断是否成功获取新闻

if len(feed.entries) == 0:

    print("没有抓取到新闻，请检查网络或 RSS 地址。")

else:

    print("成功抓取新闻！")

    print("=" * 50)

    # 输出前 10 条新闻

    for entry in feed.entries[:10]:

        print("标题：", entry.title)

        # 有些 RSS 用 published，有些用 updated

        if hasattr(entry, "published"):

            print("时间：", entry.published)

        elif hasattr(entry, "updated"):

            print("时间：", entry.updated)

        else:

            print("时间：暂无时间")

        print("-" * 50)