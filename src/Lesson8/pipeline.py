"""第8课：三工作流串联演示脚本。
本脚本演示如何用 Python 串联 Dify Workflow 1、2、3。
它不会包含真实 API Key，所有密钥和 Workflow ID 都从环境变量读取。
代码适合老师课堂演示，不要求学生一定跑通。
"""
import os
from pathlib import Path
from typing import Any
 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
ENV_PATH = PROJECT_ROOT / ".env"
DEFAULT_DIFY_BASE_URL = "https://api.dify.ai/v1"
 
def load_environment() -> None:
    """读取 .env 文件；如果没有安装 python-dotenv，也给出友好提示。"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("未安装 python-dotenv，无法自动读取 .env。")
        print("可以先运行：pip install python-dotenv")
        return
    load_dotenv(ENV_PATH)
 
def get_required_env() -> dict[str, str] | None:
    """检查必要环境变量是否齐全。"""
    required_keys = ["DIFY_API_KEY", "WF1_ID", "WF2_ID", "WF3_ID"]
    values = {key: os.getenv(key, "").strip() for key in required_keys}
    missing = [key for key, value in values.items() if not value]
    if missing:
        print("缺少必要环境变量，已停止运行。")
        print("请复制 .env.example 为 .env，并填写自己的真实信息。")
        print("缺少：")
        for key in missing:
            print(f"  {key}")
        return None
    return values
 
def extract_workflow_output(response_json: dict[str, Any]) -> dict[str, Any]:
    """从 Dify 响应中尽量取出工作流输出。"""
    if "data" in response_json and isinstance(response_json["data"], dict):
        data = response_json["data"]
        if "outputs" in data and isinstance(data["outputs"], dict):
            return data["outputs"]
    if "outputs" in response_json and isinstance(response_json["outputs"], dict):
        return response_json["outputs"]
    return response_json
 
def call_workflow(workflow_id: str, inputs: dict[str, Any]) -> dict[str, Any] | None:
    """调用单个 Dify 工作流。
    说明：不同 Dify 部署方式的 URL 可能略有差异。
    如果课堂环境的接口地址不同，请老师根据 Dify 控制台文档调整 endpoint。
    """
    try:
        import requests
    except ImportError:
        print("未安装 requests，无法调用 Dify API。")
        print("可以先运行：pip install requests")
        return None
    api_key = os.getenv("DIFY_API_KEY", "").strip()
    base_url = os.getenv("DIFY_BASE_URL", DEFAULT_DIFY_BASE_URL).strip().rstrip("/")
    endpoint = f"{base_url}/workflows/{workflow_id}/run"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": inputs,
        "response_mode": "blocking",
        "user": "taco-lesson8-demo",
    }
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
    except Exception as exc:
        print(f"调用 Dify 工作流失败：{exc}")
        print("请检查 API Key、Workflow ID、DIFY_BASE_URL 和网络连接。")
        return None
    try:
        return extract_workflow_output(response.json())
    except Exception as exc:
        print(f"Dify 返回结果不是有效 JSON：{exc}")
        return None
 
def run_full_taco_analysis(statement: str) -> dict[str, Any] | None:
    """串联运行 WF1、WF2、WF3，并返回完整结果。"""
    load_environment()
    env_values = get_required_env()
    if env_values is None:
        return None
    wf1_id = env_values["WF1_ID"]
    wf2_id = env_values["WF2_ID"]
    wf3_id = env_values["WF3_ID"]
    print("开始运行 WF1：Statement Classifier")
    classification = call_workflow(wf1_id, {"trump_statement": statement})
    if classification is None:
        return None
    print("WF1 classification：")
    print(classification)
    wf2_inputs = {
        "hardness": classification.get("hardness"),
        "domain": classification.get("domain"),
        "reasoning": classification.get("reasoning"),
    }
    print("\n开始运行 WF2：TACO Probability Engine")
    taco_probability = call_workflow(wf2_id, wf2_inputs)
    if taco_probability is None:
        return None
    print("WF2 taco_probability：")
    print(taco_probability)
    wf3_inputs = {
        "taco_probability": taco_probability.get("taco_probability"),
        "confidence": taco_probability.get("confidence"),
        "domain": classification.get("domain"),
    }
    print("\n开始运行 WF3：TACO Market Impact Predictor")
    market_prediction = call_workflow(wf3_id, wf3_inputs)
    if market_prediction is None:
        return None
    print("WF3 market_prediction：")
    print(market_prediction)
    result = {
        "statement": statement,
        "classification": classification,
        "taco_probability": taco_probability,
        "market_prediction": market_prediction,
    }
    print("\n完整结果：")
    print(result)
    print("提示：本项目不是投资建议，只做课堂演示和方向性分析。")
    return result
 
if __name__ == "__main__":
    TEST_STATEMENT = "Trump threatens to impose 50% tariffs on China with no exceptions."
    run_full_taco_analysis(TEST_STATEMENT)