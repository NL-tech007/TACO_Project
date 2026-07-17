# TACO Project

TACO Project 是一个基于新闻、市场数据和 AI 工作流的事件分析项目。  

项目围绕 Trump 相关言论、历史案例和市场数据，分析政策威胁是否可能出现软化、推迟或反转，并进一步判断可能的市场影响方向。

> 本项目仅用于课程学习和事件影响方向性分析，不构成投资建议。

---

## Project Goals

本项目目标包括：

- 抓取和清洗财经新闻数据

- 整理 TACO 历史案例

- 可视化市场数据

- 使用 Dify + RAG 检索历史案例

- 构建 AI 工作流判断言论模式

- 预测可能的市场影响方向

- 使用 FastAPI 和 Streamlit 制作可展示网页应用

- 部署到 Streamlit Cloud，形成完整项目作品集

---

## Folder Structure

```text

TACO_Project

│

├── app

│   ├── models.py

│   ├── dify_client.py

│   └── main.py

│

├── data

│   ├── market_data_2018_2025.csv

│   ├── taco_kb.txt

│   └── ...

│

├── docs

│   └── project documents and lesson notes

│

├── frontend

│   ├── streamlit_app.py

│   └── streamlit_cloud_app.py

│

├── src

|—— |—— lesson1

│   ├── lesson2

│   ├── lesson3

│   ├── lesson4

│   ├── lesson5

│   ├── lesson6

│   ├── lesson7

│   ├── lesson8

│   ├── lesson9

│   ├── lesson10

│   ├── lesson11

│   └── lesson12

│

├── taco_cases.csv

├── requirements.txt

├── .gitignore

└── README.md

```

---

## Tech Stack

本项目使用的主要工具包括：

- Python

- pandas

- matplotlib

- feedparser

- FastAPI

- Streamlit

- Dify

- RAG Knowledge Base

- GitHub

- Streamlit Cloud

---

## Lesson Overview

| Lesson | Topic | Main Output |

|---|---|---|

| Lesson 1 |

| Lesson 2 | 

| Lesson 3 | Financial Data Visualization | 市场走势图、事件标注图、相关性热力图 |

| Lesson 4 | TACO Historical Case Analysis | 历史案例分析图表、RAG 案例 CSV |

| Lesson 5 | Dify + RAG Knowledge Base | taco_kb.txt 知识库文件 |

| Lesson 6 | Statement Classifier | hardness / domain / reasoning |

| Lesson 7 | TACO Probability Engine | taco_probability / confidence |

| Lesson 8 | Market Impact Prediction | USO / GLD / SPY 方向判断 |

| Lesson 9 | FastAPI Backend | /health 和 /analyze API |

| Lesson 10 | Streamlit Frontend | 本地网页应用 |

| Lesson 11 | Streamlit Cloud Deployment | 公开 URL |

| Lesson 12 | Demo Day and Portfolio | Demo 视频、项目总结、申请材料 |

---

# Lesson 3 - Financial Data Visualization

本课目标：

- 绘制 SPY 单资产走势图

- 绘制 USO、GLD、SPY、QQQ 四资产归一化走势图

- 使用 `ax.axvline()` 标注 TACO 事件

- 计算相关矩阵和热力图

运行命令：

```powershell

python src\lesson3\lesson3_run_all.py

```

主要输出：

```text

data/spy_trend.png

data/four_assets_normalized.png

data/taco_events.png

data/correlation_heatmap.png

data/correlation_matrix.csv

```

---

# Lesson 4 - TACO Historical Case Analysis

本课目标：

使用项目根目录下的 `taco_cases.csv`，完成案例库检查、统计分析、可视化和 RAG 案例文件生成。

运行顺序：

```powershell

python src\lesson4\load_cases.py

python src\lesson4\check_cases.py

python src\lesson4\boxplot_taco_vs_hold.py

python src\lesson4\scatter_hardness_uso.py

python src\lesson4\domain_analysis.py

python src\lesson4\format_rag.py

```

主要输出：

```text

data/boxplot_taco_vs_hold.png

data/scatter_hardness_uso.png

data/domain_summary.csv

data/domain_uso_bar.png

data/rag_cases.csv

```

说明：

`data/rag_cases.csv` 是第5课 Dify + RAG 知识库搭建的输入文件。

---

# Lesson 5 - Dify + RAG Knowledge Base

本课目标：

把第4课生成的 `rag_cases.csv` 转换成 Dify 可上传的知识库文本文件 `taco_kb.txt`，并在 Dify 中完成 RAG 检索测试。

运行顺序：

```powershell

python src\lesson5\check_rag_cases.py

python src\lesson5\make_kb.py

python src\lesson5\make_test_queries.py

```

主要输出：

```text

data/taco_kb.txt

data/dify_test_queries.txt

docs/dify_upload_steps.md

docs/dify_test_template.md

```

Dify 网页端操作：

1. 打开 Dify

2. 点击 Knowledge

3. Create Knowledge

4. 上传 `data/taco_kb.txt`

5. 选择 High Quality

6. 等待状态变成 Available

7. 使用测试语句检查 Top-3 检索结果

---

# Lesson 6 - Dify Workflow 1: Statement Classifier

本课目标：

在 Dify 中搭建第一个工作流 Statement Classifier。输入 Trump 相关言论，输出：

```text

hardness

domain

reasoning

```

本地准备运行顺序：

```powershell

python src\lesson6\make_manual_test_cases.py

python src\lesson6\validate_code_node.py

```

核心文件：

```text

src/lesson6/classifier_prompt.txt

src/lesson6/code_node.py

data/lesson6_manual_test_cases.txt

docs/dify_workflow1_steps.md

docs/lesson6_prompt_tuning_guide.md

docs/lesson6_manual_test_record.md

```

Dify 工作流结构：

```text

Start

↓

LLM

↓

Code

↓

End

```

---

# Lesson 7 - TACO Probability Engine

本课目标：

搭建 Dify Workflow 2，把第6课输出的 `hardness / domain / reasoning` 接入第5课 TACO 知识库，检索相似历史案例，并输出 TACO 概率和置信度。

本地辅助文件：

```text

src/lesson7/format_query_prompt.txt

src/lesson7/probability_prompt.txt

src/lesson7/validate_probability_code.py

src/lesson7/lesson7_test_inputs.txt

docs/workflow2_probability_engine_steps.md

docs/workflow2_test_log.md

docs/workflow2_homework.md

```

Dify 工作流结构：

```text

Start

↓

LLM 1: Format Retrieval Query

↓

Knowledge Retrieval

↓

LLM 2: Probability Engine

↓

Code

↓

End

```

输出字段：

```text

taco_probability

confidence

reasoning

key_cases

```

---

# Lesson 8 - Market Impact Prediction

本课目标：

搭建 Dify Workflow 3，把第7课输出的 `taco_probability / confidence / domain` 转换成 USO、GLD、SPY 的市场方向判断。

本地辅助文件：

```text

src/lesson8/market_prompt.txt

src/lesson8/validate_market_code.py

src/lesson8/lesson8_test_inputs.txt

src/lesson8/check_with_yfinance.py

src/lesson8/check_with_local_csv.py

src/lesson8/pipeline.py

src/lesson8/lesson8_run_all.py

```

推荐运行：

```powershell

python src\lesson8\lesson8_run_all.py

python src\lesson8\check_with_local_csv.py

python src\lesson8\check_with_yfinance.py

```

输出字段：

```text

direction_uso

direction_gld

direction_spy

key_assets

magnitude

reasoning

```

---

# Lesson 9 - FastAPI Backend

本课目标：

把完整 TACO 分析链路封装成 FastAPI 后端接口。

后端接口：

```text

GET /health

POST /analyze

```

核心文件：

```text

app/models.py

app/dify_client.py

app/main.py

src/lesson9/sample_requests.json

src/lesson9/test_health.py

src/lesson9/test_analyze.py

```

安装依赖：

```powershell

pip install fastapi uvicorn requests python-dotenv

```

启动后端：

```powershell

python -m uvicorn app.main:app --reload

```

测试地址：

```text

http://127.0.0.1:8000/health

http://127.0.0.1:8000/docs

```

---

# Lesson 10 - Streamlit Frontend

本课目标：

把第9课 FastAPI 后端 `/analyze` 接入 Streamlit 前端页面，让用户可以在网页中输入 Trump 相关言论，并查看 TACO 概率和市场影响预测。

前端文件：

```text

frontend/streamlit_app.py

src/lesson10/sample_statements.txt

src/lesson10/test_backend_connection.py

src/lesson10/lesson10_run_all.py

```

终端 1：启动 FastAPI 后端

```powershell

cd D:\TACO\TACO_Project

python -m uvicorn app.main:app --reload

```

终端 2：启动 Streamlit 前端

```powershell

cd D:\TACO\TACO_Project

streamlit run frontend/streamlit_app.py

```

访问地址：

```text

http://localhost:8501

```

---

# Lesson 11 - Deployment with Streamlit Cloud

本课目标：

把 TACO Radar 从本地 Streamlit App 部署到 Streamlit Cloud，获得一个公开 URL。

本地架构：

```text

Streamlit Frontend

↓

FastAPI Backend

↓

Dify Workflows

```

云端部署架构：

```text

Streamlit Cloud

↓

Dify Workflow API

```

云端主文件：

```text

frontend/streamlit_cloud_app.py

```

Streamlit Cloud 配置：

```text

Repository: GitHub 上的 TACO 项目仓库

Branch: main

Main file path: frontend/streamlit_cloud_app.py

```

Secrets：

```text

DIFY_API_KEY

WF1_ID

WF2_ID

WF3_ID

DIFY_BASE_URL

```

安全提醒：

不要把 `.env`、`.streamlit/secrets.toml` 或真实 API Key 上传到 GitHub。

---

# Lesson 12 - Demo Day and Portfolio

本课目标：

完成 TACO Radar 的最终展示材料，包括 Demo 视频、项目讲解稿、Common App 活动描述、项目总结和作品集材料整理。

最终展示材料：

```text

docs/demo_video_script.md

docs/presentation_pitches.md

docs/common_app_activity.txt

docs/final_project_summary.md

docs/demo_video_link.md

docs/project_portfolio_checklist.md

docs/final_project_checklist.md

docs/next_steps.md

docs/lesson12_homework.md

```

Demo 视频建议结构：

```text

0:00-0:30 问题背景

0:30-1:30 系统演示

1:30-2:30 技术讲解

2:30-3:00 收尾总结

```

Common App 活动描述推荐版本：

```text

Built AI system tracking Trump statements; RAG pipeline, 20 cases, 3 Dify workflows; live on Streamlit Cloud.

```

---

## Security Notes

请务必不要上传以下内容到 GitHub：

```text

.env

.streamlit/secrets.toml

API Key

Dify API Key

GitHub Token

任何账号密码

```

`.gitignore` 中至少应包含：

```text

.env

.streamlit/secrets.toml

__pycache__/

*.pyc

venv/

.venv/

*.log

```

---

## How to Update GitHub

每次修改代码后，在项目根目录运行：

```powershell

git status

git add .

git commit -m "Update TACO project"

git push

```

GitHub 页面刷新后即可看到更新。

---

## Disclaimer

This project is for educational event-analysis purposes only and is not financial advice.

