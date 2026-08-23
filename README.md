# 📊 InsightGPT Lite

## An AI-Powered Data Analytics and Retrieval-Augmented Query Platform

InsightGPT Lite is an AI-powered data analytics platform that allows users to upload datasets, perform data cleaning and preprocessing, generate interactive visualizations, perform statistical and exploratory data analysis, assess data quality, generate automatic insights, and ask natural language questions about their datasets using Generative AI and Retrieval-Augmented Generation (RAG).

The platform combines **Data Analytics, Statistical Analysis, Exploratory Data Analysis, Data Quality Assessment, Semantic Search, Embeddings, ChromaDB, Retrieval-Augmented Generation, and Google Gemini AI** to provide intelligent and data-driven insights from structured datasets.

The project was developed as an **internship project** and was completed through multiple development phases, starting from the initial Streamlit dashboard and gradually adding advanced analytics, AI features, RAG-based retrieval, statistical question answering, automatic insights, dataset health analysis, and professional PDF reporting.

---

# 🚀 Features

## 📂 Dataset Management

✅ CSV Dataset Upload
✅ Dataset Preview
✅ Dataset Information Panel
✅ Row and Column Count
✅ Column Data Type Detection
✅ Numerical Column Detection
✅ Categorical Column Detection
✅ Missing Value Detection
✅ Missing Value Percentage Analysis
✅ Duplicate Record Detection
✅ Duplicate Record Removal
✅ Missing Value Handling
✅ Dataset Filtering
✅ Processed Dataset Download

---

## 📊 Data Analytics

✅ Dataset Summary
✅ Dataset Health Score
✅ Data Quality Analysis
✅ Missing Value Analysis
✅ Duplicate Record Analysis
✅ Numerical Column Analysis
✅ Categorical Column Analysis
✅ Automated Exploratory Data Analysis
✅ Unique Value Analysis
✅ Data Type Analysis
✅ Statistical Summary
✅ Column-Level Statistical Insights
✅ Outlier Detection
✅ IQR-Based Outlier Analysis
✅ Correlation Matrix
✅ Strong Correlation Detection
✅ Analytical Findings Generation

---

## 📈 Data Visualization

✅ Interactive Histograms
✅ Scatter Plot Visualizations
✅ Box Plot Visualizations
✅ Bar Charts
✅ Pie Charts
✅ Line Charts
✅ Correlation Heatmaps
✅ Distribution Analysis
✅ Interactive Plotly Visualizations

---

## 💡 Automatic Dataset Insights

✅ Automatic Dataset Overview
✅ Automatic Data Quality Insights
✅ Missing Data Analysis
✅ Duplicate Analysis
✅ Automatic Outlier Analysis
✅ Correlation Analysis
✅ Key Analytical Findings
✅ Dataset Health Assessment
✅ Health Score Calculation
✅ Health Score Breakdown
✅ Data Quality Recommendations
✅ Recommended Actions

The automatic insight system analyzes the uploaded dataset and generates structured analytical findings without requiring the user to manually perform every statistical operation.

---

## 🤖 Artificial Intelligence

✅ Google Gemini AI Integration
✅ AI Dataset Summary
✅ AI Cleaning Recommendations
✅ AI Executive Summary
✅ Natural Language Dataset Question Answering
✅ Context-Aware AI Responses
✅ Intelligent Question Routing
✅ Statistical Question Detection
✅ Dataset Context Generation
✅ AI-Based Analytical Interpretation

The AI system is designed to answer questions using the **current uploaded dataset** and prioritize calculated statistical results whenever they are available.

---

## 🧠 Intelligent Statistical Analysis

The project includes a dedicated statistical question-answering system that detects analytical questions and performs calculations directly on the dataset before sending the relevant results to Gemini.

### Supported Statistical Analysis

✅ Group-Wise Analysis
✅ Group-Wise Average Calculation
✅ Highest Group Average
✅ Lowest Group Average
✅ Survival Rate Analysis
✅ Average / Mean Analysis
✅ Minimum Analysis
✅ Maximum Analysis
✅ Count Analysis
✅ Missing Value Percentage
✅ Correlation Analysis
✅ Numerical Summary

### Example Questions

```text
Which gender has the highest average final grade?
What is the average age?
Which group has the highest survival rate?
What is the maximum age?
What is the average study time?
Which gender has the lowest average grade?
```

---

# 🔎 Retrieval-Augmented Generation (RAG)

InsightGPT Lite implements a Retrieval-Augmented Generation pipeline to provide relevant dataset context to the AI system.

### RAG Pipeline

```text
Uploaded Dataset
      ↓
Dataset Text Conversion
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
Sentence Transformer
      ↓
ChromaDB Vector Database
      ↓
Semantic Search
      ↓
Relevant Context Retrieval
      ↓
Gemini AI
      ↓
Context-Aware Answer
```

### RAG Features

✅ Dataset Chunking
✅ Embedding Generation
✅ Sentence Transformer Embeddings
✅ ChromaDB Vector Database Integration
✅ Semantic Search and Retrieval
✅ Relevant Context Retrieval
✅ Retrieved Context Display
✅ Retrieval-Augmented Question Answering

The application also displays retrieved context so that users can understand which dataset information was used during the retrieval process.

---

# 🧠 Intelligent Question Processing

The AI question-answering system uses multiple layers of processing before generating the final response.

```text
User Question
      ↓
Question Classification
      ↓
Statistical Question Detection
      ↓
Group-Wise Detection
      ↓
Statistical Calculation
      ↓
Dataset Context Generation
      ↓
RAG Retrieval
      ↓
Relevant Context
      ↓
Gemini AI
      ↓
Final Analytical Response
```

This approach allows the system to handle both general dataset questions and calculation-based statistical questions.

The system prioritizes calculated statistical results whenever the question requires a direct numerical answer.

---

# 🩺 Data Quality Analysis

The platform automatically evaluates the quality of the uploaded dataset.

### Data Quality Checks

✅ Missing Values
✅ Missing Value Percentage
✅ Duplicate Records
✅ Duplicate Percentage
✅ Numerical Columns
✅ Categorical Columns
✅ Outlier Detection
✅ Overall Quality Score
✅ Quality Status
✅ Quality Recommendations

The application provides users with a structured overview of potential data-quality problems before performing deeper analysis.

---

# 💚 Dataset Health Score

InsightGPT Lite includes a dedicated dataset health assessment system.

The health assessment considers important dataset-quality factors such as:

- Missing values
- Duplicate records
- Outliers

### Health Assessment

✅ Health Score
✅ Overall Dataset Status
✅ Health Explanation
✅ Missing Data Impact
✅ Duplicate Impact
✅ Outlier Impact
✅ Recommended Actions

### Example Health Classification

```text
90–100   → Excellent Dataset
75–89    → Good Dataset
50–74    → Dataset Needs Cleaning
Below 50 → Poor Dataset
```

The health score provides a quick overview of the overall condition of the uploaded dataset.

---

# 🧹 Data Cleaning

The Cleaning section allows users to process the uploaded dataset directly from the Streamlit interface.

### Cleaning Features

✅ Duplicate Removal
✅ Missing Value Handling
✅ Processed Dataset Preview
✅ Dataset Filtering
✅ Processed Dataset Download
✅ Recalculation After Dataset Changes

The application ensures that analysis can be performed on the processed dataset after cleaning operations are completed.

---

# 📊 Exploratory Data Analysis

The application performs automated exploratory data analysis on numerical and categorical columns.

### EDA Features

✅ Dataset Summary
✅ Numerical Statistics
✅ Categorical Statistics
✅ Mean
✅ Median
✅ Minimum
✅ Maximum
✅ Standard Deviation
✅ Unique Values
✅ Missing Values
✅ Outlier Detection
✅ Correlation Analysis
✅ Distribution Analysis

This provides users with a detailed understanding of their dataset before asking AI-based questions.

---

# 📈 Outlier Detection

The application detects potential outliers in numerical columns using statistical analysis.

Outlier analysis is performed for relevant numerical features and the results are included in the dataset insights and report generation process.

### Outlier Features

✅ Numerical Column Outlier Detection
✅ IQR-Based Analysis
✅ Outlier Count
✅ Column-Level Outlier Information
✅ Outlier Insights
✅ Outlier Impact on Dataset Health

---

# 🔗 Correlation Analysis

The application automatically calculates correlations between numerical columns.

### Correlation Features

✅ Correlation Matrix
✅ Correlation Heatmap
✅ Strong Correlation Detection
✅ Positive Correlation Detection
✅ Negative Correlation Detection
✅ Correlation-Based Insights

Example strong correlations can be identified between variables such as:

- G1 and G2
- G2 and G3
- G1 and G3

The system can also answer natural language questions related to correlations.

---

# 📄 PDF Reporting

InsightGPT Lite includes a professional PDF report generation system.

### PDF Report Features

✅ Dataset Information
✅ Dataset Summary
✅ Data Quality Analysis
✅ Dataset Health Score
✅ Health Assessment
✅ Automatic Dataset Insights
✅ Outlier Analysis
✅ Correlation Information
✅ Recommended Actions
✅ AI Executive Summary
✅ Professional PDF Formatting
✅ Report Download

The final report provides a consolidated summary of the dataset analysis and AI-generated insights.

---

# 🤖 AI Executive Summary

The application can generate an AI-powered executive summary based on the analyzed dataset.

The executive summary can include:

- Dataset overview
- Important statistical findings
- Data-quality observations
- Outlier information
- Correlation observations
- Key analytical insights
- Recommendations

This makes the analytical results easier to understand for users who may not have a strong technical background.

---

# 🎨 User Interface

The application is built using Streamlit and follows a tab-based dashboard structure.

### Main Sections

```text
📊 Dashboard
      ↓
🧹 Cleaning
      ↓
📈 Visualizations
      ↓
🤖 AI Insights
```

### Dashboard

The Dashboard section contains:

✅ Dataset Overview
✅ Dataset Preview
✅ RAG Statistics
✅ Dataset Summary
✅ Data Quality
✅ Dataset Health Score
✅ Automated EDA
✅ Outlier Analysis
✅ Correlation Analysis
✅ Automatic Insights
✅ Dataset Filters

### Cleaning

The Cleaning section contains:

✅ Duplicate Removal
✅ Missing Value Handling
✅ Processed Dataset Preview
✅ Dataset Download
✅ PDF Report Generation

### Visualizations

The Visualization section contains:

✅ Histogram
✅ Scatter Plot
✅ Box Plot
✅ Bar Chart
✅ Pie Chart
✅ Line Chart
✅ Correlation Heatmap
✅ Statistical Summary
✅ Column Insights
✅ Distribution Analysis
✅ Strong Correlations
✅ Key Findings

### AI Insights

The AI Insights section contains:

✅ AI Cleaning Recommendations
✅ AI Dataset Summary
✅ Natural Language Questions
✅ Statistical Question Analysis
✅ RAG Retrieval
✅ Retrieved Context
✅ Gemini AI Analysis
✅ Context-Aware Responses

---

# 📂 Project Structure

```text
InsightGPT_Lite/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   ├── __init__.py
│   │
│   ├── preprocessing.py
│   ├── visualization.py
│   ├── filtering.py
│   │
│   ├── ai_engine.py
│   ├── ai_context.py
│   ├── ai_analytics.py
│   ├── ai_cleaning.py
│   │
│   ├── analytics.py
│   ├── advanced_analytics.py
│   ├── automatic_insights.py
│   ├── data_quality.py
│   │
│   ├── question_classifier.py
│   ├── statistical_question.py
│   ├── statistical_analysis.py
│   │
│   ├── rag_pipeline.py
│   ├── embedding_model.py
│   ├── chroma_db.py
│   │
│   └── report_generator.py
│
└── venv/
```

The `venv/` directory should normally be excluded from GitHub using `.gitignore`.

---

# 🛠 Technology Stack

### Programming Language
- Python

### Frontend / Application Framework
- Streamlit

### Data Processing
- Pandas
- NumPy

### Data Visualization
- Plotly
- Matplotlib

### Machine Learning
- Scikit-learn

### Artificial Intelligence
- Google Gemini API

### Embedding Models
- Sentence Transformers

### Vector Database
- ChromaDB

### Retrieval-Augmented Generation
- RAG Pipeline
- Semantic Search
- Vector Embeddings
- ChromaDB Retrieval

### PDF Reporting
- ReportLab

### Version Control
- Git
- GitHub

---

# ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/Lakshay14ru/InsightGPT-Lite.git
```

### 2. Move Into Project Directory

```bash
cd InsightGPT_Lite
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Gemini API Key

Create a `.env` file in the project root and add your Gemini API key according to the configuration used by the application.

Example:

```text
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key or `.env` file to GitHub.

### 7. Run Application

```bash
streamlit run app.py
```

The application will open in the browser.

---

# 📈 Complete Project Workflow

```text
                         CSV DATASET
                              ↓
                        CSV UPLOAD
                              ↓
                     DATASET PREVIEW
                              ↓
                       DATA CLEANING
                       ↓           ↓
              Duplicate Removal   Missing Values
                       ↓           ↓
                       └─────┬─────┘
                             ↓
                     DATASET FILTERING
                             ↓
                    DATA QUALITY ANALYSIS
                             ↓
                     DATASET HEALTH SCORE
                             ↓
                 EXPLORATORY DATA ANALYSIS
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
          Statistics      Outliers      Correlations
              ↓              ↓              ↓
              └──────────────┼──────────────┘
                             ↓
                    AUTOMATIC INSIGHTS
                             ↓
                      VISUALIZATIONS
                             ↓
                       AI INSIGHTS
                             ↓
                   QUESTION CLASSIFICATION
                             ↓
                  STATISTICAL QUESTION?
                       ↓           ↓
                     YES            NO
                       ↓           ↓
               Statistical       RAG Retrieval
                 Analysis             ↓
                       ↓          Dataset Context
                       └────┬────────┘
                            ↓
                        Gemini AI
                            ↓
                 Context-Aware Response
                            ↓
                   AI Executive Summary
                            ↓
                     PDF REPORT
                            ↓
                    DOWNLOAD REPORT
```

---

# 📸 Project Screenshots

Screenshots can be stored inside the `screenshots/` folder.

Recommended screenshots:

1. Dashboard
2. Dataset Preview
3. Dataset Information
4. Data Quality Analysis
5. Dataset Health Score
6. Automatic Dataset Insights
7. Dataset Filters
8. Data Cleaning
9. Statistical Summary
10. Correlation Analysis
11. Correlation Heatmap
12. Visualizations
13. AI Cleaning Recommendations
14. AI Dataset Summary
15. Ask AI About Your Dataset
16. Statistical Question Answer
17. RAG Retrieval
18. Retrieved Context
19. AI Executive Summary
20. Generated PDF Report

---

# 🧪 Example Dataset Questions

The final application was tested with multiple types of natural language questions.

### Statistical Questions

```text
Which gender has the highest average final grade?
What is the average age?
What is the percentage of missing values?
What is the maximum age?
What is the average study time?
Which gender has the lowest average grade?
```

### Analytical Questions

```text
What are the strongest correlations?
Which columns contain outliers?
What is the overall dataset health?
What are the main problems in this dataset?
Give me a summary of this dataset.
```

### AI-Based Questions

```text
What are the key findings from this dataset?
What recommendations would you give for cleaning this dataset?
Give me an executive summary.
Explain the important patterns in this dataset.
```

---

# 📸 Final Analysis Example

For the Student Performance dataset, the application was able to generate analytical findings such as:

- Female students have the highest average final grade.
- The average age in the dataset is approximately 16.74 years.
- The dataset contains 0% missing values.
- Strong positive correlations are observed between G1, G2, and G3.
- Outliers are detected in multiple numerical columns.

The exact results depend on the dataset uploaded by the user.

---

# 🎯 Project Objectives

The main objectives of InsightGPT Lite are:

- Simplify data analytics for non-technical users.
- Allow users to upload and analyze CSV datasets.
- Provide automated data quality assessment.
- Perform exploratory data analysis automatically.
- Provide interactive data visualizations.
- Detect outliers and strong correlations.
- Generate automatic analytical insights.
- Implement statistical question answering.
- Integrate Generative AI into data analytics.
- Implement Retrieval-Augmented Generation for contextual responses.
- Integrate ChromaDB for semantic retrieval.
- Generate professional PDF analytics reports.
- Demonstrate practical integration of Data Science, AI, RAG, and Generative AI technologies.

---

# 🔐 Security and API Key Safety

The project uses the Gemini API for AI-powered functionality.

API keys should always be stored locally using environment variables.

The `.env` file should not be committed to GitHub.

Recommended `.gitignore` entries:

```text
.env
venv/
__pycache__/
*.pyc
```

Never expose a real API key in:

- Source code
- GitHub repositories
- Screenshots
- README files
- Public documentation

---

# 🔮 Future Scope

The current planned project has been completed. Future versions could include:

- Multi-file Dataset Upload
- Excel File Support
- PDF Data Support
- JSON Dataset Support
- Automated EDA Reports
- Predictive Analytics
- Machine Learning Model Integration
- Time-Series Forecasting
- Advanced Statistical Testing
- User Authentication
- Role-Based Access
- Cloud Database Integration
- Cloud Deployment
- Dashboard Export Features
- Automated Report Scheduling
- Advanced RAG Strategies
- Multi-Model AI Support

These features are considered future enhancements and are not part of the current completed version.

---

# 📚 Development Phases

The project was developed incrementally through multiple development phases.

### Phase 1 – Project Planning and Setup

✅ Project Planning
✅ Initial Project Structure
✅ Python Environment Setup
✅ Streamlit Application Setup
✅ Git and GitHub Repository Setup
✅ Initial Dependencies Configuration

### Phase 2 – Core Analytics Dashboard

✅ CSV Upload
✅ Dataset Preview
✅ Dataset Information
✅ Row and Column Statistics
✅ Missing Value Detection
✅ Duplicate Detection
✅ Basic Data Analysis
✅ Dashboard Metrics

### Phase 3 – Data Cleaning and Visualization

✅ Duplicate Removal
✅ Missing Value Handling
✅ Dataset Filtering
✅ Histogram Visualization
✅ Scatter Plot Visualization
✅ Box Plot Visualization
✅ Bar Chart Visualization
✅ Pie Chart Visualization
✅ Line Chart Visualization
✅ Processed Dataset Download

### Phase 4 – AI and RAG Integration

✅ Gemini AI Integration
✅ AI Dataset Analysis
✅ Dataset Context Generation
✅ Text Chunking
✅ Embedding Generation
✅ Sentence Transformer Integration
✅ ChromaDB Integration
✅ Semantic Retrieval
✅ Retrieved Context Display
✅ RAG-Based Question Answering

### Phase 5 – Advanced Analytics and Automatic Insights

✅ Advanced EDA
✅ Statistical Summaries
✅ Column-Level Numerical Insights
✅ Outlier Detection
✅ Correlation Analysis
✅ Strong Correlation Detection
✅ Automatic Dataset Insights
✅ Data Quality Insights
✅ Dataset Health Score
✅ Recommended Actions
✅ Analytical Findings

### Phase 6 – Intelligent Statistical Question Answering

✅ Question Classification
✅ Statistical Question Detection
✅ Group-Wise Question Detection
✅ Group-Wise Average Analysis
✅ Highest Group Average Detection
✅ Lowest Group Average Detection
✅ Survival Question Detection
✅ Survival Rate Calculation
✅ Average and Mean Analysis
✅ Minimum and Maximum Analysis
✅ Missing Value Percentage Analysis
✅ Statistical Results Integrated with Gemini
✅ Dataset-Aware AI Responses

### Phase 7 – Final Integration, Reporting and Project Completion

✅ Complete Dashboard Integration
✅ Complete Cleaning Workflow
✅ Complete Visualization Workflow
✅ Complete AI Insights Workflow
✅ Advanced Statistical Analysis Integration
✅ RAG Retrieval Integration
✅ Intelligent Question Routing
✅ Dataset Health Assessment
✅ Automatic Analytical Insights
✅ AI Executive Summary
✅ AI Cleaning Recommendations
✅ Professional PDF Report Generation
✅ PDF Report Download
✅ Processed Dataset Download
✅ Final Dataset Question Testing
✅ Final Statistical Question Testing
✅ Final AI Response Testing
✅ Final RAG Retrieval Testing
✅ Final PDF Report Testing
✅ Final Project Verification
✅ README Documentation Completed
✅ GitHub Repository Preparation Completed

---

# 🏆 Final Project Status

## ✅ PROJECT OFFICIALLY COMPLETED

InsightGPT Lite has successfully completed all planned development phases.

The final application provides an integrated platform for:

```text
CSV Upload
     ↓
Data Cleaning
     ↓
Data Quality Analysis
     ↓
Dataset Health Assessment
     ↓
Exploratory Data Analysis
     ↓
Statistical Analysis
     ↓
Interactive Visualization
     ↓
Automatic Insights
     ↓
Statistical Question Answering
     ↓
RAG Retrieval
     ↓
Gemini AI Analysis
     ↓
AI Executive Summary
     ↓
Professional PDF Report
```

The final version has been tested with:

✅ Dataset Upload
✅ Dataset Preview
✅ Data Cleaning
✅ Missing Value Analysis
✅ Duplicate Analysis
✅ Dataset Filtering
✅ Exploratory Data Analysis
✅ Statistical Analysis
✅ Outlier Detection
✅ Correlation Analysis
✅ Automatic Insights
✅ Dataset Health Score
✅ Visualizations
✅ Statistical Questions
✅ Group-Wise Analysis
✅ Natural Language Questions
✅ RAG Retrieval
✅ Gemini AI Responses
✅ AI Executive Summary
✅ PDF Report Generation
✅ PDF Report Download

---

# ⭐ Current Project Status

✅ Phase 1 – Project Setup Completed
✅ Phase 2 – Core Analytics Dashboard Completed
✅ Phase 3 – Data Cleaning and Visualization Completed
✅ Phase 4 – AI and RAG Integration Completed
✅ Phase 5 – Advanced Analytics and Automatic Insights Completed
✅ Phase 6 – Intelligent Statistical Question Answering Completed
✅ Phase 7 – Final Integration, Reporting and Testing Completed

🎉 **Project Development Officially Completed**

**InsightGPT Lite – AI-Powered Data Analytics and RAG Platform**

---

# 👨‍💻 Developer

**Lakshay Kundariya**
BCA (Data Science)
Apex University, Jaipur
Internship Project – InsightGPT Lite

---

# 📚 Skills Demonstrated

Through this project, the following technical skills were applied:

- Python
- Data Science
- Data Analytics
- Exploratory Data Analysis
- Statistical Analysis
- Machine Learning
- Generative AI
- Google Gemini API
- Retrieval-Augmented Generation
- Semantic Search
- Embeddings
- ChromaDB
- Sentence Transformers
- Pandas
- NumPy
- Plotly
- Matplotlib
- Scikit-learn
- Streamlit
- PDF Report Generation
- Git
- GitHub