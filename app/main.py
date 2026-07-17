"""第9课：FastAPI 后端入口。
从项目根目录运行：
python -m uvicorn app.main:app --reload
"""
import time
import requests
from fastapi import FastAPI, HTTPException

from app.dify_client import run_full_taco_analysis
from app.models import AnalyzeRequest
 
app = FastAPI(
    title="TACO雷达 API",
    description="TACO 项目的 FastAPI 后端接口，用于调用 Dify 三个工作流并返回完整分析结果。",
    version="1.0.0",
)
 
@app.get("/health")
def health() -> dict[str, str]:
    """健康检查接口，不依赖 Dify，也不需要 API Key。"""
    return {
        "status": "ok",
        "version": "1.0.0",
    }
 
@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> dict:
    """分析一条 Trump 相关言论，并返回完整 TACO JSON。"""
    start_time = time.time()
    statement = request.statement.strip()
    if not statement:
        raise HTTPException(status_code=400, detail="statement 不能为空。")
    print("收到分析请求")
    try:
        result = run_full_taco_analysis(statement)
        elapsed_ms = int((time.time() - start_time) * 1000)
        print("分析完成")
        print(f"耗时 {elapsed_ms} ms")
        return result
    except requests.Timeout:
        print("AI分析超时")
        raise HTTPException(status_code=504, detail="AI分析超时，请稍后重试。")
    except requests.HTTPError as error:
        print(error)
        raise HTTPException(
            status_code=500,
            detail="Dify API 请求失败，请检查 API Key、Workflow ID 或网络。",
        )
    except RuntimeError as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="分析出错，请稍后再试。")