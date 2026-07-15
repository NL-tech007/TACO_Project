"""第8课：使用 yfinance 对 AI 市场方向预测做简单对账。
本脚本会下载 USO、GLD、SPY 最近 5 个交易日收盘价，
并把真实方向与手动填写的 AI 示例预测进行比较。
本项目不是投资建议，只用于课堂演示事件影响方向性分析。
"""
from pathlib import Path
 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS = ["USO", "GLD", "SPY"]
 
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
    try:
        import yfinance as yf
    except ImportError:
        print("未安装 yfinance，无法下载行情。")
        print("可以先运行：pip install yfinance")
        print("如果无法联网，请改用：python src/lesson8/check_with_local_csv.py")
        return
    hits = 0
    total = len(ASSETS)
    actual_result = {}
    for asset in ASSETS:
        print(f"\n正在下载 {asset} 最近行情...")
        try:
            data = yf.download(asset, period="10d", interval="1d", progress=False, multi_level_index=False)
        except Exception as exc:
            print(f"{asset} 下载失败：{exc}")
            print("请检查网络连接，或改用：python src/lesson8/check_with_local_csv.py")
            return
        if data is None or data.empty or "Close" not in data.columns:
            print(f"{asset} 没有返回有效收盘价数据。")
            print("请稍后重试，或改用：python src/lesson8/check_with_local_csv.py")
            return
        close_prices = data["Close"].dropna().tail(5)
        if len(close_prices) < 2:
            print(f"{asset} 有效交易日不足，无法判断 5 日方向。")
            print("请改用：python src/lesson8/check_with_local_csv.py")
            return
        print(f"{asset} 最近 5 个交易日收盘价：")
        for date, price in close_prices.items():
            print(f"  {date.date()}  {float(price):.2f}")
        actual_direction = judge_direction(float(close_prices.iloc[0]), float(close_prices.iloc[-1]))
        actual_result[f"direction_{asset.lower()}"] = actual_direction
    print("\nAI 预测方向 vs 真实方向：")
    for asset in ASSETS:
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