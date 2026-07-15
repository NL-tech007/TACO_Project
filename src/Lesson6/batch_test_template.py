"""
第6课：课后批量测试 Dify 工作流的模板代码。
说明：
这个脚本只作为课后或老师演示使用。
它会从环境变量读取 DIFY_API_KEY 和 DIFY_WORKFLOW_URL。
请不要把 API Key 写进代码，也不要把 API Key 上传到 GitHub。
如果环境变量不存在，脚本会直接退出，不会请求真实 Dify 工作流。
"""
import json
import os
from pathlib import Path
import pandas as pd
import requests
 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
TEST_CASES_PATH = DATA_DIR / "lesson6_manual_test_cases.csv"
OUTPUT_PATH = DATA_DIR / "lesson6_batch_test_result.csv"
 
def extract_workflow_outputs(response_json):
    """从 Dify 返回结果中尽量取出 hardness、domain、reasoning。"""
    data = response_json.get("data", {})
    outputs = data.get("outputs", {})
    hardness = outputs.get("hardness")
    domain = outputs.get("domain")
    reasoning = outputs.get("reasoning")
    return hardness, domain, reasoning
 
def main():
    """读取测试数据，调用 Dify 工作流，并保存批量测试结果。"""
    api_key = os.getenv("DIFY_API_KEY")
    workflow_url = os.getenv("DIFY_WORKFLOW_URL")
    if not api_key or not workflow_url:
        print("请先设置环境变量，不要把 API Key 写进代码。")
        print("需要设置：DIFY_API_KEY 和 DIFY_WORKFLOW_URL")
        return
    if not TEST_CASES_PATH.exists():
        print("没有找到测试数据文件。")
        print(f"请先运行：python src/lesson6/make_manual_test_cases.py")
        print(f"期望路径：{TEST_CASES_PATH}")
        return
    print("正在读取第6课手动测试数据...")
    test_cases = pd.read_csv(TEST_CASES_PATH)
    results = []
    for _, row in test_cases.iterrows():
        statement = row["trump_statement"]
        payload = {
            "inputs": {
                "trump_statement": statement,
            },
            "response_mode": "blocking",
            "user": "lesson6-local-test",
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        print(f"正在测试 case_id={row['case_id']} ...")
        try:
            response = requests.post(
                workflow_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=60,
            )
            response.raise_for_status()
            response_json = response.json()
            hardness, domain, reasoning = extract_workflow_outputs(response_json)
        except Exception as error:
            hardness = None
            domain = None
            reasoning = f"请求或解析失败：{error}"
        try:
            predicted_hardness = int(hardness)
            expected_hardness = int(row["expected_hardness"])
            error_value = abs(predicted_hardness - expected_hardness)
        except Exception:
            predicted_hardness = None
            expected_hardness = int(row["expected_hardness"])
            error_value = None
        results.append(
            {
                "case_id": row["case_id"],
                "trump_statement": statement,
                "expected_hardness": expected_hardness,
                "predicted_hardness": predicted_hardness,
                "error": error_value,
                "expected_domain": row["expected_domain"],
                "predicted_domain": domain,
                "reasoning": reasoning,
            }
        )
    result_df = pd.DataFrame(results)
    valid_errors = result_df["error"].dropna()
    total_count = len(result_df)
    good_count = int((valid_errors <= 2).sum())
    if valid_errors.empty:
        print("\n没有可计算的误差。")
    else:
        print(f"\n平均误差：{valid_errors.mean():.2f}")
        print(f"误差 ≤ 2 的数量：{good_count}")
        print(f"总测试数量：{total_count}")
    result_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\n批量测试结果已保存到：{OUTPUT_PATH}")
 
if __name__ == "__main__":
    main()