"""
第6课：Dify Code 节点代码。
用途：
清理 LLM 节点输出，提取 JSON，并保证最终输出包含稳定的
hardness、domain、reasoning 三个字段。
说明：
Dify Code 节点中只需要复制 import json、import re 和 main 函数部分。
文件底部的本地测试区只用于在本地课堂演示。
"""
import json
import re
 
def main(llm_output: str) -> dict:
    """清理 LLM 输出，并返回稳定的分类结果字典。"""
    valid_domains = {"tariff", "tech", "energy", "fx", "other"}
    # 如果输入不是字符串，先转成字符串，避免后面处理时报错。
    text = str(llm_output)
    # 去掉常见的 markdown 代码块标记，例如 ```json 和 ```。
    text = text.replace("```json", "")
    text = text.replace("```JSON", "")
    text = text.replace("```", "")
    text = text.strip()
    # 从文本中提取第一个 JSON 对象。
    # 有些模型会在 JSON 前后加解释文字，所以这里寻找最外层的大括号。
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        json_text = match.group(0)
    else:
        json_text = text
    try:
        data = json.loads(json_text)
    except Exception:
        # 如果 JSON 解析失败，返回安全默认值，保证工作流不会直接中断。
        return {
            "hardness": 5,
            "domain": "other",
            "reasoning": "解析失败，使用默认值。",
        }
    # 处理 hardness：缺失或无法转换时默认 5，并限制在 1-10。
    try:
        hardness = int(data.get("hardness", 5))
    except Exception:
        hardness = 5
    if hardness < 1:
        hardness = 1
    if hardness > 10:
        hardness = 10
    # 处理 domain：只能是指定的 5 类，否则改成 other。
    domain = str(data.get("domain", "other")).strip().lower()
    if domain not in valid_domains:
        domain = "other"
    # 处理 reasoning：缺失或空字符串时使用默认理由。
    reasoning = str(data.get("reasoning", "")).strip()
    if not reasoning:
        reasoning = "模型未提供明确理由"
    return {
        "hardness": hardness,
        "domain": domain,
        "reasoning": reasoning,
    }
 
if __name__ == "__main__":
    # 本地测试区：Dify Code 节点中不需要复制这一段。
    sample_output = """```json
{"hardness": 9, "domain": "tech", "reasoning": "立即限制芯片出口。"}
```"""
    print(main(sample_output))