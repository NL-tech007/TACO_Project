import pandas as pd

from pathlib import Path

# 当前文件在 src/lesson4 中

# parents[2] 回到 TACO_Project 根目录

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 案例库通常放在项目根目录

CASES_FILE = PROJECT_ROOT / "data" / "taco_cases.csv"

if not CASES_FILE.exists():
    print("没有找到 taco_cases.csv")
    print("请确认文件位置")
    print(CASES_FILE)

else:

    df = pd.read_csv(CASES_FILE, parse_dates=["date"])

    df["result"] = df["result"].replace({"NOT_TACO": "HOLD"})

    print("数据预览：")
    print(df.head())

    print("\n数据列名：")
    print(df.columns)

    print("\nresult 分布：")
    print(df["result"].value_counts())

    print("\ndomain 分布：")
    print(df["domain"].value_counts())

    print("\nhardness 统计：")
    print(df["hardness"].describe())
