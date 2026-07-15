"""第8课：使用本地 CSV 对 AI 市场方向预测做简单对账。

当 yfinance 无法联网或下载失败时，可以使用本脚本读取本地行情文件。
本项目不是投资建议，只用于课堂演示事件影响方向性分析。
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
CSV_PATH = DATA_DIR / "market_data_2018_2025.csv"

ASSET_COLUMNS = {
    "USO": "USO_Close",
    "GLD": "GLD_Close",
    "SPY": "SPY_Close",
}


def judge_direction(first_close: float, last_close: float) -> str:
    """根据 5 日涨跌幅判断方向。"""
    if first_close == 0:
        return "sideways"

    change_pct = (last_close - first_close) / first_close * 100

    if change_pct > 1:
        return "up"
    if change_pct < -1:
        return "down"
    return "sideways"


def main() -> None:
    # 课堂演示用的 AI 预测结果，可以替换成 Dify Workflow 3 的输出。
    ai_result = {
        "direction_uso": "up",
        "direction_gld": "sideways",
        "direction_spy": "up",
    }

    if not CSV_PATH.exists():
        print(f"没有找到本地行情文件：{CSV_PATH}")
        print("请确认 data/market_data_2018_2025.csv 是否存在。")
        return

    try:
        import pandas as pd
    except ImportError:
        print("未安装 pandas，无法读取 CSV。")
        print("可以先运行：pip install pandas")
        return

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as exc:
        print(f"读取 CSV 失败：{exc}")
        return

    required_columns = {"date", *ASSET_COLUMNS.values()}
    missing_columns = sorted(required_columns - set(df.columns))

    if missing_columns:
        print("CSV 缺少必要列：")
        for column in missing_columns:
            print(f"  {column}")
        return

    df = df.dropna(subset=list(required_columns)).tail(5)

    if len(df) < 2:
        print("本地 CSV 有效交易日不足，无法判断最近 5 个交易日方向。")
        return

    print("本地 CSV 最近 5 个交易日收盘价：")
    print(df[["date", *ASSET_COLUMNS.values()]].to_string(index=False))

    hits = 0
    total = len(ASSET_COLUMNS)
    actual_result = {}

    for asset, column in ASSET_COLUMNS.items():
        first_close = float(df[column].iloc[0])
        last_close = float(df[column].iloc[-1])
        actual_result[f"direction_{asset.lower()}"] = judge_direction(first_close, last_close)

    print("\nAI 预测方向 vs 本地真实方向：")
    for asset in ASSET_COLUMNS:
        key = f"direction_{asset.lower()}"
        ai_direction = ai_result[key]
        actual_direction = actual_result[key]
        is_hit = ai_direction == actual_direction
        hits += int(is_hit)
        print(f"{asset}: AI={ai_direction}, 真实={actual_direction}, 命中={is_hit}")

    accuracy = hits / total * 100
    print(f"\n命中数量：{hits}/{total}")
    print(f"准确率：{accuracy:.1f}%")
    print("提示：这只是方向对账，不代表投资建议。")


if __name__ == "__main__":
    main()
