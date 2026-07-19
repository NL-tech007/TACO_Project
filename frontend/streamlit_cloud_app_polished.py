"""
Lesson 11: Streamlit Cloud Production Frontend.
This cloud version directly interfaces with three consecutive Dify Workflows via st.secrets.
Usage: streamlit run frontend/streamlit_cloud_app.py
"""

import re
import matplotlib.pyplot as plt
import requests
import streamlit as st

DEFAULT_DIFY_BASE_URL = "https://api.dify.ai/v1"

# ==============================
# SECRETS ENGINE
# ==============================
def get_secret(key: str, default: str = "") -> str:
    """Safely fetch Streamlit Secrets without crashing if file is missing locally."""
    try:
        value = st.secrets.get(key, default)
        return str(value).strip()
    except Exception:
        return default

def check_secrets() -> list[str]:
    """Verify all critical Dify API environment variables are provisioned."""
    required_keys = ["WF1_API_KEY", "WF2_API_KEY", "WF3_API_KEY"]
    return [key for key in required_keys if not get_secret(key)]

def get_dify_api_url() -> str:
    """Format and normalize the Dify Workflow execution endpoint."""
    base_url = get_secret("DIFY_BASE_URL", DEFAULT_DIFY_BASE_URL)
    if not base_url:
        base_url = DEFAULT_DIFY_BASE_URL
    base_url = base_url.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url += "/v1"
    return f"{base_url}/workflows/run"

# ==============================
# DATA TRANSFORMATION PIPELINES
# ==============================
def safe_probability(value) -> float:
    """Clamp probability bounds strictly between 0.0 and 100.0."""
    try:
        prob = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(100.0, prob))

def probability_label(prob) -> str:
    """Generate dynamic assessment badges based on TACO scores."""
    try:
        prob_value = float(prob)
    except (TypeError, ValueError):
        return "UNKNOWN THREAT LEVEL"
    if prob_value > 70:
        return "🚨 HIGH TACO PROBABILITY (Actionable Event)"
    if 30 <= prob_value <= 70:
        return "⚠️ MODERATE TACO UNCERTAINTY (Watch Closely)"
    return "🟢 LOW TACO PROBABILITY (Market Noise)"

def normalize_direction(direction) -> str:
    """Standardize mixed vector naming constraints into strict market metrics."""
    value = str(direction).lower().strip()
    if value in {"up", "down", "neutral"}:
        return value
    if value in {"sideways", "flat", "mixed"}:
        return "neutral"
    return "neutral"

def parse_market_summary(market_prediction: dict) -> dict:
    """Fallback parsing engine handling stringified responses out of Workflow 3."""
    parsed = dict(market_prediction)
    summary = str(market_prediction.get("summary", ""))
    
    for asset in ["uso", "gld", "spy"]:
        key = f"direction_{asset}"
        if key not in parsed:
            match = re.search(rf"{asset.upper()}:\s*(up|down|neutral|sideways)", summary, re.IGNORECASE)
            parsed[key] = normalize_direction(match.group(1)) if match else "neutral"
            
    if "magnitude" not in parsed:
        match = re.search(r"Magnitude:\s*(low|med|medium|high)", summary, re.IGNORECASE)
        if match:
            mag = match.group(1).lower()
            parsed["magnitude"] = "med" if mag == "medium" else mag
        else:
            parsed["magnitude"] = "N/A"
            
    if "reasoning" not in parsed:
        match = re.search(r"Reasoning:\s*([\s\S]*)", summary, re.IGNORECASE)
        parsed["reasoning"] = match.group(1).strip() if match else "No justification provided."
        
    return parsed

def require_fields(data: dict, fields: list[str], label: str) -> None:
    """Validate data schemas structurally before downstream ingestion."""
    missing = [f for f in fields if f not in data]
    if missing:
        raise RuntimeError(f"Schema Validation Error: {label} missing structural attributes: {', '.join(missing)}")

# ==============================
# DIFY CORE INTEGRATION
# ==============================
def call_workflow(api_key: str, inputs: dict) -> dict:
    """Execute synchronous calls against remote Dify nodes."""
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
        print(f"Dify Endpoint Incident Code: {response.status_code} | Payloads: {response.text}")
    response.raise_for_status()
    
    data = response.json()
    try:
        outputs = data["data"]["outputs"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError("Invalid operational signature returned by Dify Core.") from exc
    if not isinstance(outputs, dict):
        raise RuntimeError("Payload structure rejected: Output data must map to an object context.")
    return outputs

def run_full_taco_analysis(statement: str) -> dict:
    """Orchestrate multi-step pipelines analyzing speech vectors."""
    wf1_api_key = get_secret("WF1_API_KEY")
    wf2_api_key = get_secret("WF2_API_KEY")
    wf3_api_key = get_secret("WF3_API_KEY")
    
    classification = call_workflow(wf1_api_key, {"trump_statement": statement})
    require_fields(classification, ["hardness", "domain", "reasoning"], "Workflow 1 (Classifier)")
    
    probability = call_workflow(wf2_api_key, {
        "hardness": classification["hardness"],
        "domain": classification["domain"],
        "reasoning": classification["reasoning"],
    })
    require_fields(probability, ["taco_probability", "confidence"], "Workflow 2 (Probability)")
    
    market_prediction = call_workflow(wf3_api_key, {
        "taco_probability": probability["taco_probability"],
        "confidence": probability["confidence"],
        "domain": classification["domain"],
    })
    
    return {
        "statement": statement,
        "classification": classification,
        "taco_probability": probability,
        "market_prediction": market_prediction,
    }

# ==============================
# DATA VISUALIZATION ENGINE
# ==============================
def plot_market_prediction(market_prediction: dict) -> None:
    """Render analytical alpha asset shifts via dark-themed canvas matrices."""
    assets = ["USO (Oil)", "GLD (Gold)", "SPY (S&P 500)"]
    fields = ["direction_uso", "direction_gld", "direction_spy"]
    
    direction_map = {"up": 1, "neutral": 0, "down": -1}
    color_map = {"up": "#10B981", "neutral": "#64748B", "down": "#EF4444"}
    
    directions = [normalize_direction(market_prediction.get(f, "neutral")) for f in fields]
    values = [direction_map[d] for d in directions]
    colors = [color_map[d] for d in directions]
    
    # Enforce dark theme properties onto matplotlib canvas context
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor('#1E293B')
    ax.set_facecolor('#1E293B')
    
    bars = ax.bar(assets, values, color=colors, width=0.5, edgecolor='#475569', linewidth=1.2)
    
    ax.set_title("Asset Vector Projections", fontsize=12, pad=15, color='#F8FAFC', weight='bold')
    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["DOWN 📉", "NEUTRAL ➡️", "UP 📈"], color='#94A3B8', fontsize=10)
    ax.tick_params(colors='#94A3B8', labelsize=10)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#475569')
    ax.spines['bottom'].set_color('#475569')
    ax.axhline(y=0, color='#475569', linewidth=1.0, linestyle='--')
    
    for bar, direction in zip(bars, directions):
        y = bar.get_height()
        text_y = y + 0.12 if y >= 0 else y - 0.22
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            text_y,
            direction.upper(),
            ha="center",
            va="center",
            color='#F8FAFC',
            weight='bold',
            fontsize=9
        )
        
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def add_to_history(result: dict) -> None:
    """Cache the latest processed transaction states internally."""
    st.session_state["history"].insert(0, result)
    st.session_state["history"] = st.session_state["history"][:5]

# ==============================
# UI FRAMEWORK APP INITIALIZATION
# ==============================
st.set_page_config(
    page_title="TACO Intelligence Terminal",
    layout="wide",
)

# Custom UI Styling Injection
st.markdown("""
    <style>
    /* Main Background adjustments */
    .reportview-container { 
        background: #0E1117; 
    }
    
    /* Technical Typography & Financial Metric Cards */
    div[data-testid="stMetricValue"] { 
        font-family: 'Courier New', monospace; 
        font-weight: bold; 
        color: #F1F5F9; 
    }
    div[data-testid="stMetric"] { 
        background-color: #1E293B; 
        border: 1px solid #334155; 
        border-radius: 8px; 
        padding: 15px; 
    }
    
    /* Interactive Terminal Inputs */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #F8FAFC !important; 
        border: 1px solid #475569 !important; 
    }

    /* ─── NEW NEON IMAGE MATRIX STYLING ─── */
    div[data-testid="stImage"] img {
        border: 2px solid #00f2fe;
        border-radius: 8px;
        box-shadow: 0 0 10px #00f2fe, 
                    0 0 20px rgba(0, 242, 254, 0.3), 
                    inset 0 0 10px rgba(0, 242, 254, 0.2);
        padding: 4px;
        background-color: #0E1117;
        transition: all 0.3s ease-in-out;
    }

    /* Subtle pulse animation when hovering over images/GIFs */
    div[data-testid="stImage"] img:hover {
        border-color: #ff007f;
        box-shadow: 0 0 15px #ff007f, 
                    0 0 30px rgba(255, 0, 127, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state["result"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []

# Title Section

st.image(
    "frontend/assets/trumptalking.jpg",
    use_container_width=True
)

st.markdown("""
<div style="
text-align:center;
margin-top:-230px;
padding-bottom:170px;
text-shadow: 2px 2px 8px black;
">

<h1 style="
color:white;
font-size:54px;
font-weight:800;
">
🦅 TACO RADAR
</h1>

<p style="
color:#E2E8F0;
font-size:22px;
font-weight:500;
">
Algorithmic Speech Tracking & Alpha Market Impact Engine
</p>

</div>
""", unsafe_allow_html=True)


# ==============================
# SECURITY GATEWAY CONFIG
# ==============================
missing_secrets = check_secrets()
if missing_secrets:
    st.error(f"🚨 Terminal Security Alert: Missing Environment Variables [{', '.join(missing_secrets)}]")
    st.info("System Initialization Halted: Please configure credentials under App Settings → Secrets on your Cloud Node host.")
    with st.expander("Secrets Environment Blueprint Template"):
        st.code(
            "DIFY_BASE_URL = \"https://api.dify.ai/v1\"\n"
            "WF1_API_KEY = \"Classifier_Token\"\n"
            "WF2_API_KEY = \"Probability_Token\"\n"
            "WF3_API_KEY = \"Market_Impact_Token\"",
            language="toml"
        )

# ==============================
# TERMINAL INPUT LAYER
# ==============================
st.write("---")
statement = st.text_area(
    "Political Statement Capture Matrix (Raw Text Input)",
    placeholder="Intercepted transmission stream goes here... (e.g., Target commentary concerning custom tariffs, energy policies, or currency positioning)",
    height=140,
)

button_col1, button_col2 = st.columns([1, 1])
with button_col1:
    analyze_clicked = st.button("⚡ EXECUTE QUANT ANALYSIS", type="primary", use_container_width=True)
with button_col2:
    clear_clicked = st.button("🧹 PURGE CACHE", use_container_width=True)

# ==============================
# TRANSACTION LOGIC CONTROLS
# ==============================
if clear_clicked:
    st.session_state["result"] = None
    st.session_state["history"] = []
    st.success("Internal memory pipelines purged successfully.")

if analyze_clicked:
    clean_statement = statement.strip()
    if not clean_statement:
        st.warning("Analysis Aborted: Transmission capture stream cannot be null.")
    elif missing_secrets:
        st.error("Execution Failure: Cannot connect to remote processing arrays without credentials.")
    else:
        with st.spinner("Processing speech matrices via Dify Deep Intelligence Nodes..."):
            try:
                result = run_full_taco_analysis(clean_statement)
                st.session_state["result"] = result
                add_to_history(result)
                st.success("Telemetry compilation complete.")
            except requests.exceptions.Timeout:
                st.error("Network Exception: Remote Dify computational cluster timed out.")
            except requests.exceptions.HTTPError as error:
                status_code = getattr(error.response, "status_code", "N/A")
                resp_text = getattr(error.response, "text", "")
                st.error(f"Gateway Error: Remote validation failure across external network clusters (Code {status_code}).")
                if resp_text:
                    with st.expander("Raw Core Stack Trace Details"):
                        st.code(resp_text)
            except RuntimeError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"General Operational Failure: {error}")

# ==============================
# CORE SYSTEM ANALYTICS DISPLAY
# ==============================
result = st.session_state["result"]
if result:
    st.write("---")
    st.header("📊 Tactical Analysis Diagnostics")
    
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
    
    # Structural Analytical Overview Cards
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Rhetorical Hardness Factor", f"{hardness} / 10")
        st.caption(f"Target Policy Domain: **{domain.upper()}**")
    with metric_col2:
        st.metric("TACO System Probability Score", f"{prob_value:.0f}%")
        st.progress(prob_value / 100)
        st.caption(probability_label(prob))
    with metric_col3:
        st.metric("Model Confidence Rating", str(confidence).upper())
        st.caption(f"Projected Shift Magnitude: **{str(magnitude).upper()}**")
        
    # Asset Positioning Summary Row
    st.markdown("### 📈 Capital Flow Vector Metrics")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Crude Oil (USO)", normalize_direction(market_prediction.get("direction_uso", "neutral")).upper())
    with m_col2:
        st.metric("Gold Bullion (GLD)", normalize_direction(market_prediction.get("direction_gld", "neutral")).upper())
    with m_col3:
        st.metric("S&P 500 Index (SPY)", normalize_direction(market_prediction.get("direction_spy", "neutral")).upper())
        
    # Visual Canvas Deployment Layout
    display_col1, display_col2 = st.columns([4, 3])
    with display_col1:
        plot_market_prediction(market_prediction)
    with display_col2:
        st.markdown("##### 🔍 Precedent Case Contexts")
        key_cases = probability_info.get("key_cases", [])
        if isinstance(key_cases, str):
            key_cases = [key_cases]
        if isinstance(key_cases, list) and key_cases:
            for index, case in enumerate(key_cases, start=1):
                st.markdown(f"`{index}` {case}")
        else:
            st.info("No explicit historic baseline matches recorded for this parameter footprint.")
            
    # Narrative Justification Logs
    st.markdown("### 📜 Diagnostic Rationale Dossier")
    tab1, tab2, tab3 = st.tabs(["1. Rhetoric Classification", "2. Probability Modeling", "3. Capital Impact Dynamics"])
    with tab1:
        st.info(classification.get("reasoning", "No data logs archived."))
    with tab2:
        st.info(probability_info.get("reasoning", "No data logs archived."))
    with tab3:
        st.info(market_prediction.get("reasoning", "No data logs archived."))
        
    with st.expander("Inspect Unstructured Structural Metadata Response Payload (JSON)"):
        st.json(result)

# ==============================
# TRANSACTIONAL ARCHIVE COMPONENT
# ==============================
if st.session_state["history"]:
    st.write("---")
    st.subheader("📚 Terminal Transaction Log Archive (Last 5 Evaluations)")
    for index, item in enumerate(st.session_state["history"], start=1):
        c_block = item.get("classification", {})
        p_block = item.get("taco_probability", {})
        text_stream = str(item.get("statement", ""))
        truncated = text_stream[:90] + "..." if len(text_stream) > 90 else text_stream
        
        st.write(
            f"**[{index}]** Area: `{c_block.get('domain', 'N/A').upper()}` | "
            f"TACO Score: `{p_block.get('taco_probability', 'N/A')}%` | "
            f"Intercept: *\"{truncated}\"*"
        )

# Footer Disclaimer
st.write("---")
st.caption("⚖️ Institutional Warning: Strategic data outputs displayed here serve exclusively as quantitative event vector modeling tools and do not represent formal investment counsel.")