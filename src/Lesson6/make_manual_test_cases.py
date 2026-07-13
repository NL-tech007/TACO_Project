"""

第6课：生成言论分类器手动测试数据。

本脚本会生成 CSV 和 TXT 两个文件：

1. data/lesson6_manual_test_cases.csv：用于记录标准答案和后续批量测试。

2. data/lesson6_manual_test_cases.txt：方便学生复制到 Dify 网页端手动测试。

"""

from pathlib import Path

import pandas as pd

 

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

CSV_PATH = DATA_DIR / "lesson6_manual_test_cases.csv"

TXT_PATH = DATA_DIR / "lesson6_manual_test_cases.txt"

 

test_cases = [

    {

        "case_id": 1,

        "trump_statement": "Trump will impose a 25% tariff on Chinese goods next week.",

        "expected_hardness": 8,

        "expected_domain": "tariff",

        "note": "具体关税比例和执行时间，强硬度较高。",

    },

    {

        "case_id": 2,

        "trump_statement": "We are looking at all options and may consider tariffs later.",

        "expected_hardness": 2,

        "expected_domain": "tariff",

        "note": "只是可能考虑，没有明确威胁。",

    },

    {

        "case_id": 3,

        "trump_statement": "The administration may restrict technology exports to foreign companies.",

        "expected_hardness": 6,

        "expected_domain": "tech",

        "note": "涉及技术出口限制，但仍是可能性表态。",

    },

    {

        "case_id": 4,

        "trump_statement": "We will ban the company from using American chips immediately.",

        "expected_hardness": 9,

        "expected_domain": "tech",

        "note": "立即禁令，科技限制非常明确。",

    },

    {

        "case_id": 5,

        "trump_statement": "Oil producers should lower prices or face new energy restrictions.",

        "expected_hardness": 7,

        "expected_domain": "energy",

        "note": "针对能源领域提出限制威胁。",

    },

    {

        "case_id": 6,

        "trump_statement": "The dollar is too strong and the Fed should cut rates.",

        "expected_hardness": 4,

        "expected_domain": "fx",

        "note": "涉及美元和利率，但不是直接制裁或禁令。",

    },

    {

        "case_id": 7,

        "trump_statement": "Trade talks are making progress and policy adjustments are possible.",

        "expected_hardness": 2,

        "expected_domain": "tariff",

        "note": "谈判进展和政策调整，偏软化。",

    },

    {

        "case_id": 8,

        "trump_statement": "Future policy will depend on market conditions.",

        "expected_hardness": 2,

        "expected_domain": "other",

        "note": "表态模糊，没有明确政策威胁。",

    },

]

 

print("正在生成第6课手动测试数据...")

DATA_DIR.mkdir(parents=True, exist_ok=True)

test_df = pd.DataFrame(test_cases)

test_df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")

lines = []

for item in test_cases:

    lines.append(f"Test {item['case_id']}")

    lines.append(f"Statement: {item['trump_statement']}")

    lines.append(f"Expected hardness: {item['expected_hardness']}")

    lines.append(f"Expected domain: {item['expected_domain']}")

    lines.append(f"Note: {item['note']}")

    lines.append("---------------------------------------------------------------")

    lines.append("")

TXT_PATH.write_text("\n".join(lines), encoding="utf-8")

print(f"CSV 测试文件已生成：{CSV_PATH}")

print(f"TXT 测试文件已生成：{TXT_PATH}")

print(f"测试案例数量：{len(test_cases)}")