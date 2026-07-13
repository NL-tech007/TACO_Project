# ==============================

# TACO 第5次课 示例1

# 将 rag_cases.csv 转换为 Dify 知识库文本

# 文件名：make_kb.py

# ==============================

 

import pandas as pd

from pathlib import Path

 

# 当前文件在 src/lesson5 中

# parents[2] 回到 TACO_Project 根目录

PROJECT_ROOT = Path(__file__).resolve().parents[2]

 

DATA_DIR = PROJECT_ROOT / "data"

 

INPUT_FILE = DATA_DIR / "rag_cases.csv"

OUTPUT_FILE = DATA_DIR / "taco_kb.txt"

 

if not INPUT_FILE.exists():

    print("没有找到 rag_cases.csv。")

    print("请先确认第4课已经生成：")

    print(INPUT_FILE)

 

else:

    # 读取第4课生成的 RAG 案例文件

    df = pd.read_csv(INPUT_FILE)

 

    # 检查 rag_text 列是否存在

    if "rag_text" not in df.columns:

        print("rag_cases.csv 中没有找到 rag_text 列。")

        print("请检查第4课 format_rag.py 是否正确运行。")

 

    else:

        # 写入 TXT 文件

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

            for _, row in df.iterrows():

                f.write(str(row["rag_text"]))

                f.write("\n---\n\n")  # 分隔符：告诉 Dify 每条案例单独切片

 

        print("知识库文本文件已生成：")

        print(OUTPUT_FILE)

 

        print("\n共生成知识库条目：", len(df))

        print("\n第一条内容预览：")

        print(df["rag_text"].iloc[0])