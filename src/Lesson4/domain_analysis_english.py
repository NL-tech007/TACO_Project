# ==============================
# TACO 第4次课 示例5
# 领域分层分析
# 文件名：domain_analysis.py
# ==============================
 
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
 
 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
 
CASES_FILE = PROJECT_ROOT / "data" / "taco_cases.csv"
OUTPUT_FILE = DATA_DIR / "domain_uso_bar_english.png"
SUMMARY_FILE = DATA_DIR / "domain_summary.csv"
 
 
if not CASES_FILE.exists():
    print("Cannot find taco_cases.csv:")
    print(CASES_FILE)
 
else:
    df = pd.read_csv(CASES_FILE, parse_dates=["date"], encoding="utf-8-sig")
 
    # 统一 result 写法
    df["result"] = df["result"].replace({"NOT_TACO": "HOLD"})
 
    # ==============================
    # 把中文领域名转换成英文领域名
    # ==============================
 
    domain_map = {
        "关税/贸易": "Tariff / Trade",
        "关税/科技": "Tariff / Tech",
        "科技/国家安全": "Tech / National Security",
        "关税/能源": "Tariff / Energy",
        "货币政策": "Monetary Policy"
    }
 
    df["domain_en"] = df["domain"].map(domain_map)
 
    # 如果有没匹配到的领域，保留原始文本，避免空值
    df["domain_en"] = df["domain_en"].fillna(df["domain"])
 
    # ==============================
    # 1. 每个领域下 TACO / HOLD 数量
    # ==============================
 
    stats = df.groupby(["domain_en", "result"]).size().unstack(fill_value=0)
 
    print("TACO / HOLD count by domain:")
    print(stats)
 
    # 如果某些列不存在，补 0，避免 KeyError
    if "TACO" not in stats.columns:
        stats["TACO"] = 0
 
    if "HOLD" not in stats.columns:
        stats["HOLD"] = 0
 
    # ==============================
    # 2. 计算 TACO 率
    # ==============================
 
    stats["total"] = stats["TACO"] + stats["HOLD"]
    stats["taco_rate"] = (stats["TACO"] / stats["total"] * 100).round(1)
 
    # ==============================
    # 3. 每个领域平均强硬度
    # ==============================
 
    hardness_avg = df.groupby("domain_en")["hardness"].mean().round(2)
    stats["avg_hardness"] = hardness_avg
 
    # ==============================
    # 4. 每个领域平均市场反应
    # ==============================
 
    market_avg = df.groupby("domain_en")[["uso_5d", "gld_5d", "spy_5d"]].mean().round(2)
 
    summary = stats.join(market_avg)
 
    print("\nDomain analysis summary:")
    print(summary)
 
    # 保存汇总表
    summary.to_csv(SUMMARY_FILE, encoding="utf-8-sig")
 
    print("\nDomain summary saved to:")
    print(SUMMARY_FILE)
 
    # ==============================
    # 5. 画 USO 平均反应柱状图
    # ==============================
 
    uso_by_domain = df.groupby("domain_en")["uso_5d"].mean().sort_values(ascending=False)
 
    fig, ax = plt.subplots(figsize=(10, 5))
 
    uso_by_domain.plot(kind="bar", ax=ax)
 
    # 0 线：高于 0 表示上涨，低于 0 表示下跌
    ax.axhline(y=0, linestyle="--", alpha=0.6)
 
    ax.set_title("Average USO 5-Day Return by Domain")
    ax.set_xlabel("Domain")
    ax.set_ylabel("Average USO 5-Day Return (%)")
 
    # 让英文标签倾斜，避免重叠
    plt.xticks(rotation=30, ha="right")
 
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=150)
    plt.show()
 
    print("\nDomain USO bar chart saved to:")
    print(OUTPUT_FILE)