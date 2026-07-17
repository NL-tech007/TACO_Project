# 用途：第8课 Dify Workflow 3 中 Code 节点要粘贴的 Python 代码。
# 说明：这个文件主要是为了方便老师和学生复制到 Dify Code 节点。
# 注意：不要在这里填写 Dify API Key，也不要写调用 Dify API 的代码。
import json
import re
 
def main(llm_output: str) -> dict:
    """
    清洗市场影响预测 LLM 输出，保证最终结果稳定。
    输入：
        llm_output: LLM 节点的原始输出文本
    输出：
        direction_uso: up / down / sideways
        direction_gld: up / down / sideways
        direction_spy: up / down / sideways
        key_assets: 重点关注资产列表
        magnitude: low / mid / high
        reasoning: 简短解释
    """
    valid_directions = {"up", "down", "sideways"}
    valid_magnitude = {"low", "mid", "high"}
    default_result = {
        "direction_uso": "sideways",
        "direction_gld": "sideways",
        "direction_spy": "sideways",
        "key_assets": [],
        "magnitude": "low",
        "reasoning": "LLM 输出解析失败或格式不完整，使用默认震荡判断。",
    }
    try:
        text = str(llm_output).strip()
        # 去掉 markdown 代码块
        text = re.sub(r"```json|```", "", text).strip()
        # 如果有多余文字，尝试提取 JSON 对象
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
        data = json.loads(text)
        # 方向字段校验
        for field in ["direction_uso", "direction_gld", "direction_spy"]:
            value = str(data.get(field, "sideways")).lower().strip()
            # 常见同义词修正
            mapping = {
                "bullish": "up",
                "rising": "up",
                "increase": "up",
                "higher": "up",
                "bearish": "down",
                "falling": "down",
                "decrease": "down",
                "lower": "down",
                "flat": "sideways",
                "neutral": "sideways",
                "stable": "sideways",
            }
            value = mapping.get(value, value)
            if value not in valid_directions:
                value = "sideways"
            data[field] = value
        # magnitude 校验
        magnitude = str(data.get("magnitude", "low")).lower().strip()
        if magnitude == "medium":
            magnitude = "mid"
        if magnitude not in valid_magnitude:
            magnitude = "low"
        data["magnitude"] = magnitude
        # key_assets 校验
        key_assets = data.get("key_assets", [])
        if not isinstance(key_assets, list):
            key_assets = [str(key_assets)]
        # 只保留常见资产名称
        valid_assets = {"USO", "GLD", "SPY", "QQQ"}
        cleaned_assets = []
        for asset in key_assets:
            asset = str(asset).upper().strip()
            if asset in valid_assets:
                cleaned_assets.append(asset)
        data["key_assets"] = cleaned_assets
        # reasoning 兜底
        reasoning = data.get("reasoning", "")
        if not reasoning:
            reasoning = "模型未提供明确理由。"
        data["reasoning"] = reasoning
        return {
            "direction_uso": data["direction_uso"],
            "direction_gld": data["direction_gld"],
            "direction_spy": data["direction_spy"],
            "key_assets": data["key_assets"],
            "magnitude": data["magnitude"],
            "reasoning": data["reasoning"],
        }
    except Exception:
        return default_result