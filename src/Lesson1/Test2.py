# ==============================
# TACO 第1次课 示例2B
# 读取本地 CSV 市场数据
# 文件名：test_data_csv.py
# ==============================
 
import pandas as pd
from pathlib import Path
 
# 当前文件在 src/lesson1 中
# parents[2] 回到 TACO_Project 根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]
 
DATA_FILE = PROJECT_ROOT / "data" / "market_data_2018_2025.csv"
 
if not DATA_FILE.exists():
    print("没有找到本地市场数据文件：")
    print(DATA_FILE)
else:
    df = pd.read_csv(DATA_FILE)
 
    print("成功读取本地市场数据！")
    print("数据预览：")
    print(df.head())
 
    print("\n数据列名：")
    print(df.columns)