import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "market_data_2018_2025.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "four_assets_normalized.png"
 
if not DATA_FILE.exists():
    print("没有找到市场数据文件：", DATA_FILE)
 
else:
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df = df.set_index("date")
 
    price_df = df[[
        "USO_Close",
        "GLD_Close",
        "SPY_Close",
        "QQQ_Close"
    ]].copy()

    price_df.columns = ["USO", "GLD", "SPY", "QQQ"]
    price_df = price_df.dropna()

#完整画图流程
df_norm = price_df / price_df.iloc[0] * 100
colors = {"USO": "#E8521E", "GLD": "#F59E0B", 
          "SPY": "#1A56A0", "QQQ": "#6B3FA0"}
fig, ax = plt.subplots(figsize=(12, 5))
for ticker, color in colors.items():
    ax.plot(df_norm.index, df_norm[ticker],
            label=ticker, color=color , linewidth=1.5)
    
ax.axhline(y=100, color="gray", 
           linestyle="--", linewidth=0.8)

ax.set_ylabel("Indexed to 100")
ax.legend()
plt.tight_layout()
plt.savefig("four_assets_normalized.png", dpi=150)

# ==============================
# TACO 第3次课 示例3
# 四资产归一化走势图
# 文件名：four_assets_normalized.py
# ==============================
 
# import pandas as pd
# import matplotlib.pyplot as plt
# from pathlib import Path
 
# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# DATA_FILE = PROJECT_ROOT / "data" / "market_data_2018_2025.csv"
# OUTPUT_FILE = PROJECT_ROOT / "data" / "four_assets_normalized.png"
 
# if not DATA_FILE.exists():
#     print("没有找到市场数据文件：", DATA_FILE)
 
# else:
#     df = pd.read_csv(DATA_FILE, parse_dates=["date"])
#     df = df.set_index("date")
 
#     # 统一列名：把 USO_Close 改成 USO，方便画图
#     price_df = df[[
#         "USO_Close",
#         "GLD_Close",
#         "SPY_Close",
#         "QQQ_Close"
#     ]].copy()
 
#     price_df.columns = ["USO", "GLD", "SPY", "QQQ"]
 
#     # 删除空值，避免第一行有缺失影响归一化
#     price_df = price_df.dropna()
 
#     # 归一化：所有资产从 100 出发
#     df_norm = price_df / price_df.iloc[0] * 100
 
#     fig, ax = plt.subplots(figsize=(12, 5))
 
#     for ticker in df_norm.columns:
#         ax.plot(
#             df_norm.index,
#             df_norm[ticker],
#             linewidth=1.5,
#             label=ticker
#         )
 
#     # 画一条 100 的水平基准线
#     # 高于 100 表示相对第一天上涨，低于 100 表示下跌
#     ax.axhline(
#         y=100,
#         linestyle="--",
#         linewidth=0.8
#     )
 
#     ax.set_title("Normalized Asset Prices 2018-2025")
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Indexed to 100")
#     ax.legend()
 
#     plt.tight_layout()
#     plt.savefig(OUTPUT_FILE, dpi=150)
#     plt.show()
 
#     print("四资产归一化图已保存到：", OUTPUT_FILE)