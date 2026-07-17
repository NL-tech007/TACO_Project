"""第9课：FastAPI 请求数据模型。
本文件定义 /analyze 接口接收的 JSON 格式。
"""
from pydantic import BaseModel, Field
 
class AnalyzeRequest(BaseModel):
    """/analyze 接口的请求体格式。
    前端或其他程序必须发送：
    {
        "statement": "一条 Trump 相关言论"
    }
    """
    statement: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="需要分析的 Trump 相关言论",
    )