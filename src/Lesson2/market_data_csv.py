# ==============================
# TACO 第2次课 示例4
# 使用 yfinance 下载四个资产的历史价格
# 文件名：get_market.py
# ==============================
 
import yfinance as yf
import pandas as pd
from pathlib import Path
 
# 找到项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]
 
# data 文件夹路径
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
 
# 四个资产代码
tickers = ["USO", "GLD", "SPY", "QQQ"]
 
# 用字典保存每个资产的收盘价
data = {}
 
for t in tickers:
    print(f"正在下载 {t} 的历史价格...")
 
    try:
        obj = yf.Ticker(t)
 
        # 从 2018-01-01 开始下载
        # 只保留 Close 收盘价
        close_price = obj.history(start="2018-01-01")["Close"]
 
        if len(close_price) == 0:
            print(f"{t} 没有获取到数据。")
        else:
            data[t] = close_price
            print(f"{t} 下载成功，共 {len(close_price)} 个交易日。")
 
    except Exception as e:
        print(f"{t} 下载失败。")
        print("错误原因：", e)
 
# 把四个资产合并成 DataFrame
df_market = pd.DataFrame(data)
# 判断
if len(df_market) == 0:
    print("\n没有成功下载任何市场数据")
    print("可以改用已提供的 market_data_2018_2025.csv.")
else:
    print("\n市场数据下载成功，预览：")
    print(df_market.head())
    print("\n数据形状：")
    print(df_market.shape)
    output_path = DATA_DIR / "market_data.csv"
    df_market.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("\n市场数据已保存到: ")
    print(output_path)
