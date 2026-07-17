"""第9课：Dify 三个 Workflow 的调用封装。
本文件只从项目根目录的 .env 读取配置，不包含任何真实 API Key。
推荐使用三个 Workflow App 各自的 API Key。
"""
import os
from pathlib import Path
from typing import Any
import requests
from dotenv import load_dotenv
 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)
DIFY_BASE_URL = os.getenv("DIFY_BASE_URL", "https://api.dify.ai/v1").rstrip("/")
WF1_API_KEY = os.getenv("WF1_API_KEY", "").strip()
WF2_API_KEY = os.getenv("WF2_API_KEY", "").strip()
WF3_API_KEY = os.getenv("WF3_API_KEY", "").strip()
 
def check_env() -> None:
    """检查 Dify 调用需要的环境变量是否齐全。"""
    missing = []
    if not WF1_API_KEY:
        missing.append("WF1_API_KEY")
    if not WF2_API_KEY:
        missing.append("WF2_API_KEY")
    if not WF3_API_KEY:
        missing.append("WF3_API_KEY")
    if missing:
        raise RuntimeError(
            "缺少环境变量："
            + "、".join(missing)
            + "。请在 .env 中填写三个 Dify Workflow App 的 API Key。"
        )
 
def call_workflow(api_key: str, inputs: dict[str, Any]) -> dict[str, Any]:
    """调用一个 Dify Workflow，并返回 outputs。"""
    check_env()
    url = f"{DIFY_BASE_URL}/workflows/run"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": inputs,
        "response_mode": "blocking",
        "user": "taco-api",
    }
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )
    if response.status_code >= 400:
        print("Dify API 请求失败")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
    response.raise_for_status()
    data = response.json()
    try:
        outputs = data["data"]["outputs"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError("Dify 返回格式不符合预期。") from exc
    if not isinstance(outputs, dict):
        raise RuntimeError("Dify 返回格式不符合预期。")
    return outputs
 
def require_fields(data: dict[str, Any], fields: list[str], label: str) -> None:
    """检查上一个工作流输出是否包含下一个工作流需要的字段。"""
    missing = [field for field in fields if field not in data]
    if missing:
        raise RuntimeError(f"{label} 缺少必要字段：{', '.join(missing)}。")
 
def run_full_taco_analysis(statement: str) -> dict[str, Any]:
    """串联三个 Dify Workflow，返回完整 TACO 分析结果。"""
    # Workflow 1：言论分类器
    classification = call_workflow(
        WF1_API_KEY,
        {
            "trump_statement": statement,
        },
    )
    print("Workflow 1 输出：", classification)
    require_fields(
        classification,
        ["hardness", "domain", "reasoning"],
        "Workflow 1 输出",
    )
    # Workflow 2：TACO 概率引擎
    probability = call_workflow(
        WF2_API_KEY,
        {
            "hardness": classification["hardness"],
            "domain": classification["domain"],
            "reasoning": classification["reasoning"],
        },
    )
    print("Workflow 2 输出：", probability)
    require_fields(
        probability,
        ["taco_probability", "confidence"],
        "Workflow 2 输出",
    )
    # Workflow 3：市场影响预测
    market_prediction = call_workflow(
        WF3_API_KEY,
        {
            "taco_probability": probability["taco_probability"],
            "confidence": probability["confidence"],
            "domain": classification["domain"],
        },
    )
    print("Workflow 3 输出：", market_prediction)
    return {
        "statement": statement,
        "classification": classification,
        "taco_probability": probability,
        "market_prediction": market_prediction,
    }