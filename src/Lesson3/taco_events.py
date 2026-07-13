import pandas as pd

import matplotlib.pyplot as plt

from pathlib import Path

 

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "market_data_2018_2025.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "taco_events.png"

 

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

 

    # 为了图表更清楚，这里只看 2019 年以后

    price_df = price_df[price_df.index >= "2019-01-01"]

 

    # 归一化

    df_norm = price_df / price_df.iloc[0] * 100

 

    # TACO 历史事件示例

    # 格式：日期、标签、颜色

    # red 可以表示强硬言论，green 可以表示软化或暂停

    events = [

        ("2019-05-05", "Tariff hike 25%", "red"),

        ("2020-01-15", "Phase One Deal", "green"),

        ("2025-04-02", "Liberation Day", "red"),

        ("2025-04-09", "Tariff Pause 90d", "green")

    ]

 

    fig, ax = plt.subplots(figsize=(14, 5))



    for ticker in df_norm.columns:
        
        ax.plot(

            df_norm.index,

            df_norm[ticker],

            linewidth=1.4,

            label=ticker

        )


    for date, label, color in events:
        event_date = pd.Timestamp(date)

        ax.axvline(
            x = event_date,
            color = color,
            linestyle = "--",
            alpha = 0.75
        )

        ax.text(
            event_date,
            140,
            label,
            rotation = 90,
            fontsize = 8,
            color = color,
            verticalalignment = "top",
        )


ax.axhline(y=100, linestyle="--", linewidth=0.8)

ax.set_title("Normalized Asset Prices with TACO Events Markers")
ax.set_xlabel("Date")
ax.set_ylabel("Indexed to 100")
ax.legend()


plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=150)
plt.show()
print("事件标注图已保存到：", OUTPUT_FILE)






