# ==============================

# TACO 第3次课 进阶示例

# 绘制相关性热力图

# 文件名：correlation_heatmap.py

# ==============================

 

import pandas as pd

import matplotlib.pyplot as plt

from pathlib import Path

 

PROJECT_ROOT = Path(__file__).resolve().parents[2]

 

CASES_FILE = PROJECT_ROOT / "data"/ "taco_cases.csv"

 

OUTPUT_FILE = PROJECT_ROOT / "data" / "correlation_heatmap.png"

 

if not CASES_FILE.exists():

    print("没有找到 taco_cases.csv。")

    print("这部分可以等第4课案例库整理完成后再运行。")

 

else:

    df = pd.read_csv(CASES_FILE)

 

    # 基础列：强硬度 + 三个资产 5 日涨跌幅

    columns = ["hardness", "uso_5d", "gld_5d", "spy_5d"]

 

    # 如果案例库里有 qqq_5d，也把它加入分析

    if "qqq_5d" in df.columns:

        columns.append("qqq_5d")

 

    # 检查缺失列

    missing_columns = []

 

    for col in columns:

        if col not in df.columns:

            missing_columns.append(col)

 

    if len(missing_columns) > 0:

        print("缺少以下列，无法绘制相关性热力图：")

        print(missing_columns)

 

    else:

        # 计算相关矩阵

        corr_df = df[columns].corr()

 

        print("相关矩阵：")

        print(corr_df)

 

        # 创建画布和坐标轴

        fig, ax = plt.subplots(figsize=(7, 6))

 

        # imshow 可以把二维数字表格画成颜色图

        image = ax.imshow(

            corr_df,

            vmin=-1,

            vmax=1

        )

 

        # 设置 x 轴和 y 轴标签

        ax.set_xticks(range(len(corr_df.columns)))

        ax.set_yticks(range(len(corr_df.index)))

 

        ax.set_xticklabels(corr_df.columns, rotation=45, ha="right")

        ax.set_yticklabels(corr_df.index)

 

        # 在每一个格子里写入相关系数

        for i in range(len(corr_df.index)):

            for j in range(len(corr_df.columns)):

                value = corr_df.iloc[i, j]

 

                ax.text(

                    

                    j,

                    i,

                    f"{value:.2f}",

                    ha="center",

                    va="center"

                )

 

        # 添加颜色条

        fig.colorbar(image, ax=ax)

 

        ax.set_title("Correlation Heatmap")

 

        plt.tight_layout()

        plt.savefig(OUTPUT_FILE, dpi=150)

        plt.close(fig)

 

        print("相关性热力图已保存到：")

        print(OUTPUT_FILE)