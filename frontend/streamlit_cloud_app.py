"""第11课：Streamlit Cloud 部署版前端。
云端版不调用本地 FastAPI。
它从 Streamlit Cloud 的 st.secrets 读取 Dify Workflow API Key，
然后直接调用三个 Dify Workflow。
运行方式：
streamlit run frontend/streamlit_cloud_app.py
Streamlit Cloud Secrets 示例：
DIFY_BASE_URL = "https://api.dify.ai/v1"
WF1_API_KEY = "第6课 Statement Classifier 的 API Key"
WF2_API_KEY = "第7课 Probability Engine 的 API Key"
WF3_API_KEY = "第8课 Market Impact Prediction 的 API Key"
"""
import re
import matplotlib.pyplot as plt
import requests
import streamlit as st
 
DEFAULT_DIFY_BASE_URL = "https://api.dify.ai/v1"
 
# ==============================
# Secrets 读取工具
# ==============================
def get_secret(key: str, default: str = "") -> str:
    """
    安全读取 Streamlit Secrets。
    直接访问 st.secrets 时，如果本地没有 secrets.toml，
    Streamlit 会抛出 StreamlitSecretNotFoundError。
    所以这里统一 try / except，避免页面直接崩溃。
    """
    try:
        value = st.secrets.get(key, default)
        return str(value).strip()
    except Exception:
        return default
 
def check_secrets() -> list[str]:
    """检查 Streamlit Cloud Secrets 是否配置完整。"""
    required_keys = [
        "WF1_API_KEY",
        "WF2_API_KEY",
        "WF3_API_KEY",
    ]
    missing = []
    for key in required_keys:
        value = get_secret(key)
        if not value:
            missing.append(key)
    return missing
 
def get_dify_api_url() -> str:
    """读取 Dify API 基础地址，并拼出 Workflow API 地址。"""
    base_url = get_secret("DIFY_BASE_URL", DEFAULT_DIFY_BASE_URL)
    if not base_url:
        base_url = DEFAULT_DIFY_BASE_URL
    base_url = base_url.rstrip("/")
    # 兼容用户写 https://api.dify.ai 的情况
    if not base_url.endswith("/v1"):
        base_url = base_url + "/v1"
    return f"{base_url}/workflows/run"
 
# ==============================
# 数据处理工具函数
# ==============================
def safe_probability(value) -> float:
    """把概率安全转换为 0-100 之间的数字。"""
    try:
        prob = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(100.0, prob))
 
def probability_label(prob) -> str:
    """根据 TACO 概率返回中文标签。"""
    try:
        prob_value = float(prob)
    except (TypeError, ValueError):
        return "未知概率"
    if prob_value > 70:
        return "高 TACO 概率"
    if 30 <= prob_value <= 70:
        return "中等不确定"
    return "低 TACO 概率"
 
def normalize_direction(direction) -> str:
    """把市场方向限制为 up / down / neutral。"""
    value = str(direction).lower().strip()
    if value in {"up", "down", "neutral"}:
        return value
    if value in {"sideways", "flat", "mixed"}:
        return "neutral"
    return "neutral"
 
def parse_market_summary(market_prediction: dict) -> dict:
    """
    兼容 Workflow 3 只返回 summary 的情况。
    例如：
    Market Impact Prediction
    USO: neutral
    GLD: up
    SPY: down
    Key assets: SPY, GLD
    Magnitude: low
    Reasoning:
    ...
    """
    parsed = dict(market_prediction)
    summary = str(market_prediction.get("summary", ""))
    if "direction_uso" not in parsed:
        match = re.search(r"USO:\s*(up|down|neutral|sideways)", summary, re.IGNORECASE)
        if match:
            parsed["direction_uso"] = normalize_direction(match.group(1))
        else:
            parsed["direction_uso"] = "neutral"
    if "direction_gld" not in parsed:
        match = re.search(r"GLD:\s*(up|down|neutral|sideways)", summary, re.IGNORECASE)
        if match:
            parsed["direction_gld"] = normalize_direction(match.group(1))
        else:
            parsed["direction_gld"] = "neutral"
    if "direction_spy" not in parsed:
        match = re.search(r"SPY:\s*(up|down|neutral|sideways)", summary, re.IGNORECASE)
        if match:
            parsed["direction_spy"] = normalize_direction(match.group(1))
        else:
            parsed["direction_spy"] = "neutral"
    if "magnitude" not in parsed:
        match = re.search(r"Magnitude:\s*(low|med|medium|high)", summary, re.IGNORECASE)
        if match:
            magnitude = match.group(1).lower()
            if magnitude == "medium":
                magnitude = "med"
            parsed["magnitude"] = magnitude
        else:
            parsed["magnitude"] = "N/A"
    if "reasoning" not in parsed:
        match = re.search(r"Reasoning:\s*([\s\S]*)", summary, re.IGNORECASE)
        if match:
            parsed["reasoning"] = match.group(1).strip()
        else:
            parsed["reasoning"] = "无"
    return parsed
 
def require_fields(data: dict, fields: list[str], label: str) -> None:
    """检查工作流输出是否包含必要字段。"""
    missing = []
    for field in fields:
        if field not in data:
            missing.append(field)
    if missing:
        raise RuntimeError(
            f"{label} 缺少必要字段：{', '.join(missing)}。"
        )
 
# ==============================
# Dify Workflow 调用
# ==============================
def call_workflow(api_key: str, inputs: dict) -> dict:
    """调用一个 Dify Workflow，并返回 outputs。"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": inputs,
        "response_mode": "blocking",
        "user": "taco-streamlit-cloud",
    }
    response = requests.post(
        get_dify_api_url(),
        headers=headers,
        json=payload,
        timeout=90,
    )
    if response.status_code >= 400:
        print("Dify API request failed")
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
 
def run_full_taco_analysis(statement: str) -> dict:
    """串联 Dify 三个 Workflow，返回完整 TACO 分析结果。"""
    wf1_api_key = get_secret("WF1_API_KEY")
    wf2_api_key = get_secret("WF2_API_KEY")
    wf3_api_key = get_secret("WF3_API_KEY")
    classification = call_workflow(
        wf1_api_key,
        {
            "trump_statement": statement,
        },
    )
    require_fields(
        classification,
        ["hardness", "domain", "reasoning"],
        "Workflow 1 输出",
    )
    probability = call_workflow(
        wf2_api_key,
        {
            "hardness": classification["hardness"],
            "domain": classification["domain"],
            "reasoning": classification["reasoning"],
        },
    )
    require_fields(
        probability,
        ["taco_probability", "confidence"],
        "Workflow 2 输出",
    )
    market_prediction = call_workflow(
        wf3_api_key,
        {
            "taco_probability": probability["taco_probability"],
            "confidence": probability["confidence"],
            "domain": classification["domain"],
        },
    )
    return {
        "statement": statement,
        "classification": classification,
        "taco_probability": probability,
        "market_prediction": market_prediction,
    }
 
# ==============================
# 图表
# ==============================
def plot_market_prediction(market_prediction: dict) -> None:
    """把 USO / GLD / SPY 的方向转换成英文柱状图。"""
    assets = ["USO", "GLD", "SPY"]
    fields = [
        "direction_uso",
        "direction_gld",
        "direction_spy",
    ]
    direction_map = {
        "up": 1,
        "neutral": 0,
        "down": -1,
    }
    color_map = {
        "up": "green",
        "neutral": "gray",
        "down": "red",
    }
    directions = []
    for field in fields:
        direction = normalize_direction(market_prediction.get(field, "neutral"))
        directions.append(direction)
    values = []
    for direction in directions:
        values.append(direction_map[direction])
    colors = []
    for direction in directions:
        colors.append(color_map[direction])
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(
        assets,
        values,
        color=colors,
    )
    ax.set_title("Market Impact Prediction")
    ax.set_xlabel("Asset")
    ax.set_ylabel("Direction Score")
    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["down", "neutral", "up"])
    ax.axhline(
        y=0,
        color="black",
        linewidth=0.8,
    )
    for bar, direction in zip(bars, directions):
        y = bar.get_height()
        if y > 0:
            text_y = y + 0.12
        elif y < 0:
            text_y = y - 0.18
        else:
            text_y = y + 0.12
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            text_y,
            direction,
            ha="center",
            va="center",
        )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
 
# ==============================
# 历史记录
# ==============================
def add_to_history(result: dict) -> None:
    """把本次分析结果放入最近 5 次历史记录。"""
    st.session_state["history"].insert(0, result)
    st.session_state["history"] = st.session_state["history"][:5]
 
# ==============================
# 页面初始化
# ==============================
st.set_page_config(
    page_title="TACO雷达",
    layout="wide",
)
if "result" not in st.session_state:
    st.session_state["result"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []
 
st.title("TACO雷达")
st.caption("AI追踪特朗普言论，分析 TACO 概率与市场影响")
 
# ==============================
# Secrets 检查
# ==============================
missing_secrets = check_secrets()
if missing_secrets:
    st.error(
        "缺少 Streamlit Secrets："
        + "、".join(missing_secrets)
    )
    st.info(
        "如果你在本地运行这个云端版文件，需要创建本地 secrets.toml；"
        "如果你部署到 Streamlit Cloud，需要在 App Settings → Secrets 中配置这些变量。"
    )
    with st.expander("Secrets 示例"):
        st.code(
            """
DIFY_BASE_URL = "https://api.dify.ai/v1"
WF1_API_KEY = "第6课 Statement Classifier 的 API Key"
WF2_API_KEY = "第7课 Probability Engine 的 API Key"
WF3_API_KEY = "第8课 Market Impact Prediction 的 API Key"
""".strip(),
            language="toml",
        )
 
# ==============================
# 输入区
# ==============================
statement = st.text_area(
    "输入特朗普言论 Statement",
    placeholder="Paste a Trump statement here...",
    height=130,
)
button_col1, button_col2 = st.columns([1, 1])
with button_col1:
    analyze_clicked = st.button(
        "开始分析 / Analyze",
        type="primary",
    )
with button_col2:
    clear_clicked = st.button("清空结果 / Clear")
 
# ==============================
# 按钮逻辑
# ==============================
if clear_clicked:
    st.session_state["result"] = None
    st.session_state["history"] = []
    st.success("结果已清空。")
if analyze_clicked:
    clean_statement = statement.strip()
    if not clean_statement:
        st.warning("请先输入一条 Trump 相关言论。")
    elif missing_secrets:
        st.error("Secrets 配置不完整，不能调用 Dify。")
        st.info("请先配置 WF1_API_KEY、WF2_API_KEY、WF3_API_KEY。")
    else:
        with st.spinner("AI分析中，请稍候..."):
            try:
                result = run_full_taco_analysis(clean_statement)
                st.session_state["result"] = result
                add_to_history(result)
                st.success("分析完成。")
            except requests.exceptions.Timeout:
                st.error("请求超时。Dify 工作流可能响应较慢，请稍后重试。")
            except requests.exceptions.HTTPError as error:
                status_code = getattr(error.response, "status_code", "未知状态码")
                response_text = ""
                try:
                    response_text = error.response.text
                except Exception:
                    response_text = ""
                st.error("Dify API 请求失败，请检查 Secrets、API Key 或 Dify 工作流是否已发布。")
                st.caption(f"状态码：{status_code}")
                if response_text:
                    with st.expander("查看 Dify 返回的错误信息"):
                        st.code(response_text)
            except RuntimeError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"分析失败：{error}")
 
# ==============================
# 结果展示区
# ==============================
result = st.session_state["result"]
if result:
    st.subheader("核心分析结果")
    classification = result.get("classification", {})
    probability_info = result.get("taco_probability", {})
    market_prediction_raw = result.get("market_prediction", {})
    market_prediction = parse_market_summary(market_prediction_raw)
    hardness = classification.get("hardness", "N/A")
    domain = classification.get("domain", "N/A")
    prob = probability_info.get("taco_probability", 0)
    confidence = probability_info.get("confidence", "N/A")
    magnitude = market_prediction.get("magnitude", "N/A")
    prob_value = safe_probability(prob)
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("强硬度 Hardness", f"{hardness}/10")
        st.caption(f"领域 Domain：{domain}")
    with metric_col2:
        st.metric("TACO概率", f"{prob_value:.0f}%")
        st.progress(prob_value / 100)
        st.caption(probability_label(prob))
    with metric_col3:
        st.metric("置信度 Confidence", confidence)
        st.caption(f"影响强度 Magnitude：{magnitude}")
    st.subheader("市场影响预测")
    market_col1, market_col2, market_col3 = st.columns(3)
    direction_uso = normalize_direction(market_prediction.get("direction_uso", "neutral"))
    direction_gld = normalize_direction(market_prediction.get("direction_gld", "neutral"))
    direction_spy = normalize_direction(market_prediction.get("direction_spy", "neutral"))
    with market_col1:
        st.metric("USO Oil", direction_uso)
    with market_col2:
        st.metric("GLD Gold", direction_gld)
    with market_col3:
        st.metric("SPY S&P 500", direction_spy)
    plot_market_prediction(market_prediction)
    st.subheader("分析理由")
    st.markdown("**言论分类理由**")
    st.write(classification.get("reasoning", "无"))
    st.markdown("**TACO 概率理由**")
    st.write(probability_info.get("reasoning", "无"))
    st.markdown("**市场方向理由**")
    st.write(market_prediction.get("reasoning", "无"))
    key_cases = probability_info.get("key_cases", [])
    if isinstance(key_cases, str):
        key_cases = [key_cases]
    if isinstance(key_cases, list) and key_cases:
        st.subheader("关键历史案例")
        for index, case in enumerate(key_cases, start=1):
            st.write(f"{index}. {case}")
    with st.expander("查看完整 JSON 返回结果"):
        st.json(result)
 
# ==============================
# 历史记录区
# ==============================
if st.session_state["history"]:
    st.subheader("最近 5 次分析记录")
    for index, item in enumerate(st.session_state["history"], start=1):
        classification = item.get("classification", {})
        probability_info = item.get("taco_probability", {})
        statement_text = str(item.get("statement", ""))
        short_statement = statement_text[:80]
        if len(statement_text) > 80:
            short_statement += "..."
        domain = classification.get("domain", "N/A")
        prob = probability_info.get("taco_probability", "N/A")
        st.write(
            f"{index}. [{domain}] TACO概率：{prob}%｜{short_statement}"
        )
 
# ==============================
# 底部说明
# ==============================
st.caption("提示：本项目仅用于事件影响方向性分析，不构成投资建议。")