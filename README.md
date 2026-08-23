<div align="center">

# 📊 InsightGPT Lite

### AI-Powered Data Analytics & Retrieval-Augmented Query Platform

Upload a dataset. Clean it. Visualize it. Ask it questions in plain English.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-00A67E)](https://www.trychroma.com/)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#-license)

</div>

---

## 📖 Overview

**InsightGPT Lite** is an AI-powered data analytics platform that lets users upload a dataset and instantly get cleaning, exploratory analysis, visualizations, data-quality scoring, and natural-language Q&A — powered by **Google Gemini** and a **Retrieval-Augmented Generation (RAG)** pipeline built on **ChromaDB**.

Instead of manually writing pandas queries or SQL, users can simply ask:

> *"Which gender has the highest average final grade?"*
> *"What are the strongest correlations in this dataset?"*
> *"Give me an executive summary of this dataset."*

The app detects whether a question needs a direct statistical calculation or a semantic/contextual answer, computes it against the live dataset, retrieves supporting context via RAG, and returns a grounded, context-aware response — with the option to export everything as a professional PDF report.

This project was built as an **internship project** and was developed incrementally across 7 structured development phases (see [Development Phases](#-development-phases)).

---

## ✨ Key Highlights

| | |
|---|---|
| 🧹 **Data Cleaning** | Missing value handling, duplicate detection & removal, dataset filtering |
| 📊 **Automated EDA** | Statistical summaries, outlier detection (IQR), correlation analysis |
| 📈 **Visualizations** | Histograms, scatter, box, bar, pie & line charts, correlation heatmaps |
| 💚 **Health Scoring** | 0–100 dataset health score with a full quality breakdown |
| 🤖 **Gemini AI** | Natural-language Q&A, cleaning recommendations, executive summaries |
| 🧠 **RAG Pipeline** | Chunking → Embeddings → ChromaDB → Semantic retrieval → Gemini |
| 🔢 **Stat Engine** | Group-wise averages, min/max, correlation & missing-value queries answered with real calculations, not guesses |
| 📄 **PDF Reports** | One-click, professional report with insights, charts & AI summary |

---

## 🧭 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Example Questions](#-example-questions--sample-output)
- [PDF Report](#-pdf-report)
- [Screenshots](#-screenshots)
- [Development Phases](#-development-phases)
- [Future Scope](#-future-scope)
- [Security](#-security--api-key-safety)
- [Developer](#-developer)
- [License](#-license)

---

## 🚀 Features

<details open>
<summary><strong>📂 Dataset Management</strong></summary>

- CSV upload with instant preview
- Dataset info panel (rows, columns, dtypes)
- Numerical / categorical column detection
- Missing value detection & percentage breakdown
- Duplicate detection & removal
- Filtering and processed-dataset download

</details>

<details>
<summary><strong>📊 Analytics & Exploratory Data Analysis</strong></summary>

- Dataset summary & statistical profiling (mean, median, std, min/max)
- Column-level numerical & categorical insights
- IQR-based outlier detection
- Correlation matrix + strong correlation detection
- Automatically generated analytical findings

</details>

<details>
<summary><strong>📈 Visualizations</strong></summary>

- Interactive Plotly charts: Histogram, Scatter, Box, Bar, Pie, Line
- Correlation heatmaps
- Distribution analysis

</details>

<details>
<summary><strong>💡 Automatic Dataset Insights & Health Score</strong></summary>

- Auto-generated data-quality insights (missing data, duplicates, outliers)
- Dataset Health Score with classification:

  | Score | Status |
  |---|---|
  | 90–100 | 🟢 Excellent |
  | 75–89 | 🟢 Good |
  | 50–74 | 🟡 Needs Cleaning |
  | < 50 | 🔴 Poor |

- Actionable, prioritized recommendations

</details>

<details>
<summary><strong>🤖 AI & Retrieval-Augmented Generation</strong></summary>

- Google Gemini integration for natural-language Q&A
- Intelligent question routing — statistical vs. semantic
- Dataset chunking → Sentence-Transformer embeddings → ChromaDB
- Semantic search with retrieved-context transparency
- AI-generated executive summaries & cleaning recommendations

</details>

<details>
<summary><strong>📄 Professional PDF Reporting</strong></summary>

- Dataset overview, quality analysis & health score
- Statistical summary, outliers & correlations
- Automatic insights + AI executive summary
- One-click generation and download

</details>

---

## ⚙️ How It Works

```text
 CSV Upload
     │
     ▼
 Data Cleaning  ──▶  Missing Values · Duplicates · Filtering
     │
     ▼
 Data Quality Analysis  ──▶  Health Score
     │
     ▼
 Exploratory Data Analysis  ──▶  Statistics · Outliers · Correlations
     │
     ▼
 Automatic Insights  ──▶  Visualizations
     │
     ▼
 User Question
     │
     ▼
 Question Classifier ──┬──▶ Statistical Question ──▶ Direct Calculation
                        │                                   │
                        └──▶ Semantic Question ──▶ RAG Retrieval (ChromaDB)
                                                             │
                                                             ▼
                                                        Gemini AI
                                                             │
                                                             ▼
                                            Context-Aware Response / Executive Summary
                                                             │
                                                             ▼
                                                      PDF Report Export
```

The system **prioritizes direct statistical calculations** whenever a question requires an exact numerical answer, and falls back to RAG-based semantic retrieval for open-ended or interpretive questions — reducing hallucination and keeping answers grounded in the actual uploaded data.

---

## 🛠 Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python |
| **App Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib |
| **Machine Learning** | Scikit-learn |
| **Generative AI** | Google Gemini API |
| **Embeddings** | Sentence Transformers |
| **Vector Database** | ChromaDB |
| **RAG** | Custom chunking + semantic retrieval pipeline |
| **Reporting** | ReportLab (PDF generation) |
| **Version Control** | Git, GitHub |

---

## 📂 Project Structure

```text
InsightGPT_Lite/
│
├── app.py                     # Streamlit entry point
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   ├── preprocessing.py       # Cleaning & preprocessing
│   ├── visualization.py       # Chart generation
│   ├── filtering.py           # Dataset filtering
│   │
│   ├── ai_engine.py           # Gemini API integration
│   ├── ai_context.py          # Dataset context builder
│   ├── ai_analytics.py        # AI-driven analytical interpretation
│   ├── ai_cleaning.py         # AI cleaning recommendations
│   │
│   ├── analytics.py           # Core analytics
│   ├── advanced_analytics.py  # Outliers, correlations
│   ├── automatic_insights.py  # Auto-generated findings
│   ├── data_quality.py        # Quality scoring
│   │
│   ├── question_classifier.py # Statistical vs semantic routing
│   ├── statistical_question.py
│   ├── statistical_analysis.py
│   │
│   ├── rag_pipeline.py        # RAG orchestration
│   ├── embedding_model.py     # Sentence-Transformer embeddings
│   ├── chroma_db.py           # ChromaDB integration
│   │
│   └── report_generator.py    # PDF report generation
│
└── reports/
    └── InsightGPT_Report.pdf
```

---

## 🏁 Getting Started

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://ai.google.dev/)

### 1. Clone the repository
```bash
git clone https://github.com/Lakshay14ru/InsightGPT-Lite.git
cd InsightGPT-Lite
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```
> ⚠️ Never commit your `.env` file or real API key to GitHub.

### 5. Run the app
```bash
streamlit run app.py
```
The app will open automatically at **http://localhost:8501**

---

## 💬 Example Questions & Sample Output

**Statistical**
```text
Which gender has the highest average final grade?
What is the average age?
What is the percentage of missing values?
What is the maximum age?
```

**Analytical**
```text
What are the strongest correlations?
Which columns contain outliers?
What is the overall dataset health?
```

**AI-Generated**
```text
Give me an executive summary.
What recommendations would you give for cleaning this dataset?
```

### Sample Output — Student Performance Dataset

| Query | Result |
|---|---|
| Highest average final grade by gender | **Female** students → avg. G3 = `12.25` vs Male → `11.41` |
| Average age | `16.74` years |
| Missing values | `0%` |
| Strongest correlations | G2 ↔ G3 = `0.919`, G1 ↔ G2 = `0.865`, G1 ↔ G3 = `0.826` |

---

## 📄 PDF Report

Every analysis session can be exported as a polished PDF containing:

- Dataset overview & dimensions
- Data quality & health score breakdown
- Statistical summary (numerical + categorical)
- Outlier & correlation analysis
- Automatic insights and recommended actions
- AI-generated executive summary

---

## 📸 Screenshots

> Add screenshots to a `screenshots/` folder and reference them below.

| Dashboard | Data Cleaning | AI Insights |
|---|---|---|
| `screenshots/dashboard.png` | `screenshots/cleaning.png` | `screenshots/ai_insights.png` |

| Visualizations | RAG Retrieved Context | PDF Report |
|---|---|---|
| `screenshots/visualizations.png` | `screenshots/rag_context.png` | `screenshots/pdf_report.png` |

---

## 🏆 Development Phases

| Phase | Focus | Status |
|---|---|---|
| **1** | Project setup, Streamlit scaffold, Git/GitHub init | ✅ Completed |
| **2** | Core dashboard — upload, preview, dataset info | ✅ Completed |
| **3** | Data cleaning + core visualizations | ✅ Completed |
| **4** | Gemini AI + RAG pipeline (chunking, embeddings, ChromaDB) | ✅ Completed |
| **5** | Advanced analytics — outliers, correlations, health score | ✅ Completed |
| **6** | Intelligent statistical question answering | ✅ Completed |
| **7** | Final integration, PDF reporting, testing & docs | ✅ Completed |

**Project Status: ✅ Completed** — all 7 phases delivered and tested end-to-end.

---

## 🔮 Future Scope

- Multi-file & Excel/JSON dataset support
- Predictive analytics & ML model integration
- Time-series forecasting
- Advanced statistical testing
- User authentication & role-based access
- Cloud database integration & deployment
- Multi-model AI support with conversation memory

---

## 🔐 Security & API Key Safety

- API keys are stored locally via a `.env` file and are **never** committed to version control.
- Recommended `.gitignore` entries:
  ```gitignore
  .env
  venv/
  __pycache__/
  *.pyc
  ```
- Never expose real API keys in source code, screenshots, or documentation.

---

## 👨‍💻 Developer

**Lakshay Kundariya**
BCA (Data Science) — Apex University, Jaipur
*Internship Project — InsightGPT Lite*

[![GitHub](https://img.shields.io/badge/GitHub-Lakshay14ru-181717?logo=github&logoColor=white)](https://github.com/Lakshay14ru)

---

## 📜 License

This project is developed for **educational and internship purposes**. Feel free to fork, explore, and build on it — attribution appreciated.

<div align="center">

⭐ If you found this project useful, consider giving it a star on GitHub!

</div>