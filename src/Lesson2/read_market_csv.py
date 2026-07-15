# ==============================
# TACO 第2次课 示例5
# 读取本地市场数据 CSV
# 文件名：read_market_csv.py
# ==============================
 
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
 
# 当前文件在 src/lesson2 中
# parents[2] 回到 TACO_Project 根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]
 
DATA_DIR = PROJECT_ROOT / "data"
MARKET_FILE = DATA_DIR / "market_data_2018_2025.csv"
 
REQUIRED_COLUMNS = [
    "date",
    "USO_Close",
    "GLD_Close",
    "SPY_Close",
    "QQQ_Close"
]
 
if not MARKET_FILE.exists():
    print("没有找到市场数据文件：")
    print(MARKET_FILE)
    print("请把 market_data_2018_2025.csv 放到 data 文件夹中。")
 
else:
    df_market = pd.read_csv(MARKET_FILE)
 
    print("成功读取市场数据！")
    print("文件路径：", MARKET_FILE)
    print("=" * 60)
 
    print("数据预览：")
    print(df_market.head())
 
    print("\n数据列名：")
    print(df_market.columns)
 
    # 检查列是否完整
    missing_columns = []
 
    for col in REQUIRED_COLUMNS:
        if col not in df_market.columns:
            missing_columns.append(col)
 
    if len(missing_columns) > 0:
        print("\n缺少以下列，无法继续分析：")
        print(missing_columns)
 
    else:
        # 转换日期格式
        df_market["date"] = pd.to_datetime(df_market["date"]).dt.date
 
        # 计算 USO 每日涨跌幅
        df_market["USO_Change"] = df_market["USO_Close"].pct_change() * 100
 
        print("\nUSO 最近 10 天数据：")
        print(df_market[["date", "USO_Close", "USO_Change"]].tail(10))
 
        # 保存 USO 涨跌幅
        output_path = DATA_DIR / "uso_daily_change.csv"
        df_market[["date", "USO_Close", "USO_Change"]].to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig"
        )
 
        print("\nUSO 涨跌幅结果已保存到：")
        print(output_path)
 
        # 挑战：画出 SPY 折线图
        plt.figure(figsize=(10, 5))
        plt.plot(df_market["date"], df_market["SPY_Close"])
 
        plt.title("SPY Close Price")
        plt.xlabel("Date")
        plt.ylabel("SPY Close Price")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

        # 挑战：画出 USO 折线图
        plt.figure(figsize=(10, 5))
        plt.plot(df_market["date"], df_market["USO_Close"])
 
        plt.title("USO Close Price")
        plt.xlabel("Date")
        plt.ylabel("USO Close Price")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()