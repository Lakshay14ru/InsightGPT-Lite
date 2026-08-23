# 📊 InsightGPT Lite

## An AI-Powered Data Analytics and Retrieval-Augmented Query Platform

InsightGPT Lite is an AI-powered data analytics platform that allows users to upload datasets, perform data cleaning and preprocessing, generate interactive visualizations, perform statistical and exploratory data analysis, assess data quality, generate automatic insights, and ask natural language questions about their datasets using Generative AI and Retrieval-Augmented Generation (RAG).

The platform combines **Data Analytics, Statistical Analysis, Exploratory Data Analysis, Data Quality Assessment, Semantic Search, Embeddings, ChromaDB, Retrieval-Augmented Generation, and Google Gemini AI** to provide intelligent and data-driven insights from structured datasets.

The project was developed as an **internship project** and was completed through multiple development phases, starting from the initial Streamlit dashboard and gradually adding advanced analytics, AI features, RAG-based retrieval, statistical question answering, automatic insights, dataset health analysis, and professional PDF reporting.

---

# 🚀 Features

## 📂 Dataset Management

- ✅ CSV Dataset Upload
- ✅ Dataset Preview
- ✅ Dataset Information Panel
- ✅ Row and Column Count
- ✅ Column Data Type Detection
- ✅ Numerical Column Detection
- ✅ Categorical Column Detection
- ✅ Missing Value Detection
- ✅ Missing Value Percentage Analysis
- ✅ Duplicate Record Detection
- ✅ Duplicate Record Removal
- ✅ Missing Value Handling
- ✅ Dataset Filtering
- ✅ Processed Dataset Download

---

## 📊 Data Analytics

- ✅ Dataset Summary
- ✅ Dataset Health Score
- ✅ Data Quality Analysis
- ✅ Missing Value Analysis
- ✅ Duplicate Record Analysis
- ✅ Numerical Column Analysis
- ✅ Categorical Column Analysis
- ✅ Automated Exploratory Data Analysis
- ✅ Unique Value Analysis
- ✅ Data Type Analysis
- ✅ Statistical Summary
- ✅ Column-Level Statistical Insights
- ✅ Outlier Detection
- ✅ IQR-Based Outlier Analysis
- ✅ Correlation Matrix
- ✅ Strong Correlation Detection
- ✅ Analytical Findings Generation

---

## 📈 Data Visualization

- ✅ Interactive Histograms
- ✅ Scatter Plot Visualizations
- ✅ Box Plot Visualizations
- ✅ Bar Charts
- ✅ Pie Charts
- ✅ Line Charts
- ✅ Correlation Heatmaps
- ✅ Distribution Analysis
- ✅ Interactive Plotly Visualizations

---

## 💡 Automatic Dataset Insights

- ✅ Automatic Dataset Overview
- ✅ Automatic Data Quality Insights
- ✅ Missing Data Analysis
- ✅ Duplicate Analysis
- ✅ Automatic Outlier Analysis
- ✅ Correlation Analysis
- ✅ Key Analytical Findings
- ✅ Dataset Health Assessment
- ✅ Health Score Calculation
- ✅ Health Score Breakdown
- ✅ Data Quality Recommendations
- ✅ Recommended Actions

The automatic insight system analyzes the uploaded dataset and generates structured analytical findings without requiring the user to manually perform every statistical operation.

---

## 🤖 Artificial Intelligence

- ✅ Google Gemini AI Integration
- ✅ AI Dataset Summary
- ✅ AI Cleaning Recommendations
- ✅ AI Executive Summary
- ✅ Natural Language Dataset Question Answering
- ✅ Context-Aware AI Responses
- ✅ Intelligent Question Routing
- ✅ Statistical Question Detection
- ✅ Dataset Context Generation
- ✅ AI-Based Analytical Interpretation

The AI system is designed to answer questions using the **current uploaded dataset** and prioritize calculated statistical results whenever they are available.

---

## 🧠 Intelligent Statistical Analysis

The project includes a dedicated statistical question-answering system that detects analytical questions and performs calculations directly on the dataset before sending the relevant results to Gemini.

### Supported Statistical Analysis

- ✅ Group-Wise Analysis
- ✅ Group-Wise Average Calculation
- ✅ Highest Group Average
- ✅ Lowest Group Average
- ✅ Survival Rate Analysis
- ✅ Average / Mean Analysis
- ✅ Minimum Analysis
- ✅ Maximum Analysis
- ✅ Count Analysis
- ✅ Missing Value Percentage
- ✅ Correlation Analysis
- ✅ Numerical Summary

### Example Questions

```text
Which gender has the highest average final grade?

What is the average age?

Which group has the highest survival rate?

What is the maximum age?

What is the average study time?

Which gender has the lowest average grade?

🧠 Retrieval-Augmented Generation (RAG)
✅ Dataset Chunking
✅ Embedding Generation
✅ ChromaDB Vector Database Integration
✅ Semantic Search and Retrieval
✅ Retrieved Context Display
✅ Retrieval-Augmented Question Answering

The RAG pipeline converts relevant dataset information into searchable embeddings and retrieves the most relevant context for natural language questions.

🧹 Data Cleaning

The Data Cleaning section allows users to process and prepare the uploaded dataset directly through the Streamlit interface.

Cleaning Features
✅ Duplicate Removal
✅ Missing Value Handling
✅ Processed Dataset Preview
✅ Dataset Filtering
✅ Processed Dataset Download
✅ Recalculation After Dataset Changes

The application ensures that analysis can be performed on the processed dataset after cleaning operations are completed.

🔍 Exploratory Data Analysis

The application performs automated exploratory data analysis on numerical and categorical columns.

EDA Features
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

📄 Reporting
✅ Professional PDF Report Generation
✅ Dataset Summary Reports
✅ Data Quality Reports
✅ Dataset Health Reports
✅ Automatic Insights in Reports
✅ AI Executive Summary in Reports
✅ Report Download Feature

The reporting system generates a professional PDF report containing important dataset information, analytical findings, data quality information, visualizations, and AI-generated summaries.

🎨 User Interface
✅ Streamlit Interactive Dashboard
✅ Professional Sidebar
✅ Tab-Based Navigation
✅ Wide Screen Responsive Layout
✅ Dashboard Section
✅ Data Cleaning Section
✅ Exploratory Data Analysis Section
✅ Visualization Section
✅ AI Insights Section
✅ Statistical Analysis Section
✅ Professional Report Generation Interface

InsightGPT_Lite/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── visualization.py
│   ├── filtering.py
│   ├── ai_engine.py
│   ├── ai_context.py
│   ├── ai_analytics.py
│   ├── ai_cleaning.py
│   ├── analytics.py
│   ├── advanced_analytics.py
│   ├── automatic_insights.py
│   ├── data_quality.py
│   ├── question_classifier.py
│   ├── statistical_question.py
│   ├── statistical_analysis.py
│   ├── rag_pipeline.py
│   ├── embedding_model.py
│   ├── chroma_db.py
│   └── report_generator.py
│
└── reports/
    └── InsightGPT_Report.pdf

🛠 Technology Stack
Programming Language
Python
Frontend Framework
Streamlit
Data Processing
Pandas
NumPy
Data Visualization
Plotly
Matplotlib
Exploratory Data Analysis
Pandas
NumPy
Scikit-learn
Statistical Analysis
Artificial Intelligence
Google Gemini API
Generative AI
Embedding Models
Sentence Transformers
Vector Database
ChromaDB
Retrieval-Augmented Generation
RAG Pipeline
Semantic Search
Vector Embeddings
Context Retrieval
Version Control
Git
GitHub
⚙️ Installation
Clone Repository
git clone https://github.com/Lakshay14ru/InsightGPT-Lite.git
Move into Project Directory
cd InsightGPT_Lite
Create Virtual Environment
python -m venv venv
Activate Virtual Environment
Windows
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Configure Gemini API

Create a .env file in the project directory and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

Never upload your .env file or API keys to GitHub.

Run Application
streamlit run app.py

The application will open in your browser at:

http://localhost:8501
📈 Project Workflow
CSV Dataset
      ↓
Dataset Upload
      ↓
Dataset Preview
      ↓
Data Cleaning
      ↓
Missing Value Handling
      ↓
Duplicate Removal
      ↓
Dataset Filtering
      ↓
Data Quality Analysis
      ↓
Exploratory Data Analysis
      ↓
Statistical Analysis
      ↓
Visualizations
      ↓
Automatic Dataset Insights
      ↓
Question Classification
      ↓
Statistical Question Analysis
      ↓
Dataset Chunking
      ↓
Embedding Generation
      ↓
ChromaDB Vector Database
      ↓
Semantic Retrieval
      ↓
Relevant Dataset Context
      ↓
Gemini AI
      ↓
Context-Aware Responses
      ↓
PDF Report Generation
      ↓
Report Download
🔎 Natural Language Question Answering

InsightGPT Lite allows users to ask natural language questions about their uploaded dataset.

Example Questions
Which gender has the highest average final grade?

What is the average age?

What is the percentage of missing values?

Which columns have strong correlations?

Which columns contain outliers?

What is the maximum age?

What is the average study time?

The system identifies the type of question and performs the required statistical calculation using the uploaded dataset.

For example:

Question:
Which gender has the highest average final grade?

Result:
Female students have the highest average final grade.

Another example:

Question:
What is the average age?

Result:
The average age in the dataset is approximately 16.74 years.
📊 Statistical Analysis Example

The system can calculate group-wise statistics directly from the dataset.

For example, for student performance data:

Female Average G3 = 12.253
Male Average G3   = 11.406

The system identifies:

Female students have the highest average final grade.

The system can also calculate:

Average Age = 16.744

and detect correlations such as:

G2 and G3 = 0.919
G1 and G2 = 0.865
G1 and G3 = 0.826
📄 PDF Reporting

InsightGPT Lite includes a professional PDF reporting system.

The generated report can contain:

Dataset Overview
Dataset Dimensions
Data Types
Missing Value Analysis
Duplicate Analysis
Dataset Health Score
Statistical Summary
Numerical Analysis
Categorical Analysis
Outlier Analysis
Correlation Analysis
Automatic Insights
Key Findings
Recommended Actions
AI Executive Summary
Data Cleaning Information
Analytical Results

The report can be generated and downloaded directly from the Streamlit application.

📸 Project Screenshots

Screenshots can be maintained inside the screenshots/ folder.

Recommended screenshots include:

Dashboard
Dataset Upload
Dataset Information
Data Cleaning
Dataset Filtering
Exploratory Data Analysis
Data Visualizations
Automatic Dataset Insights
AI Insights
Statistical Question Answering
Retrieved RAG Context
PDF Report
Generated Analytical Findings
🎯 Project Objectives
Simplify data analytics for non-technical users.
Provide AI-driven insights from structured datasets.
Automate exploratory data analysis.
Provide data quality assessment.
Detect missing values, duplicates, outliers, and correlations.
Implement statistical question answering.
Implement Retrieval-Augmented Generation for contextual question answering.
Integrate Google Gemini AI with dataset analysis.
Generate automatic analytical insights.
Generate professional PDF reports.
Demonstrate practical integration of Data Science, Generative AI, RAG, and Streamlit.
🔮 Future Scope

Although the current project is completed, the following features could be added in future versions:

Multi-file Dataset Upload
Excel File Support
PDF Dataset Support
Automated Advanced EDA Reports
Predictive Analytics
Machine Learning Model Integration
Automated Machine Learning
Time-Series Forecasting
User Authentication
Cloud Database Integration
Cloud Deployment
Dashboard Export Features
Advanced RAG Pipelines
Multiple LLM Support
Conversation Memory
Role-Based Access Control
🏆 Development Phases

The project was developed through multiple phases.

Phase 1 – Project Setup
✅ Project initialization
✅ Streamlit application setup
✅ Virtual environment setup
✅ Project folder structure
✅ Git and GitHub repository setup
✅ Initial requirements configuration
Phase 2 – Core Analytics Dashboard
✅ CSV dataset upload
✅ Dataset preview
✅ Dataset information
✅ Data type detection
✅ Missing value detection
✅ Duplicate detection
✅ Basic dataset analytics
✅ Dashboard metrics
Phase 3 – Data Cleaning and Visualization
✅ Data cleaning functionality
✅ Missing value handling
✅ Duplicate removal
✅ Dataset filtering
✅ Processed dataset preview
✅ Processed dataset download
✅ Histograms
✅ Scatter plots
✅ Additional visualizations
Phase 4 – AI and RAG Integration
✅ Gemini AI integration
✅ Dataset context generation
✅ Dataset chunking
✅ Embedding generation
✅ Sentence Transformer integration
✅ ChromaDB integration
✅ Semantic retrieval
✅ RAG-based question answering
Phase 5 – Advanced Analytics and Insights
✅ Automated EDA
✅ Statistical analysis
✅ Numerical analysis
✅ Categorical analysis
✅ Outlier detection
✅ Correlation analysis
✅ Data quality analysis
✅ Dataset health score
✅ Automatic dataset insights
✅ Recommended actions
Phase 6 – Intelligent Question Answering
✅ Question classification
✅ Statistical question detection
✅ Group-wise analysis
✅ Group-wise average calculations
✅ Minimum and maximum analysis
✅ Missing value percentage analysis
✅ Correlation-based questions
✅ Dataset-specific analytical answers
✅ Context-aware AI responses
Phase 7 – Finalization and Professional Reporting
✅ Final UI improvements
✅ Final analytics validation
✅ Final AI question-answering validation
✅ Statistical question validation
✅ Automatic insights validation
✅ Dataset health validation
✅ Professional PDF report generation
✅ PDF report validation
✅ Final README documentation
✅ Final project testing
✅ Final GitHub repository preparation
✅ Final project completion
🧪 Final Testing

The application was tested using real dataset analysis and natural language questions.

Tested Question 1
Which gender has the highest average final grade?
Result
Female students have the highest average final grade.
Tested Question 2
What is the average age?
Result
The average age in the dataset is approximately 16.74 years.
Additional Analysis

The system successfully generated:

Average values
Minimum values
Maximum values
Group-wise averages
Missing value percentages
Correlation results
Outlier detection
Automatic key findings
Dataset interpretations
AI-generated analytical responses
📌 Project Status
✅ Completed

All planned development phases have been completed successfully.

Phase 1  → ✅ Completed
Phase 2  → ✅ Completed
Phase 3  → ✅ Completed
Phase 4  → ✅ Completed
Phase 5  → ✅ Completed
Phase 6  → ✅ Completed
Phase 7  → ✅ Completed
🎉 Final Status

InsightGPT Lite – Project Completed Successfully

The project is finalized with:

✅ Data Analytics
✅ Data Cleaning
✅ Exploratory Data Analysis
✅ Statistical Analysis
✅ Data Quality Assessment
✅ Automatic Insights
✅ AI Integration
✅ RAG Pipeline
✅ ChromaDB Integration
✅ Natural Language Question Answering
✅ Professional PDF Reporting
✅ Final Testing
✅ Complete Documentation
👨‍💻 Developer

Lakshay Kundariya

BCA (Data Science)
Apex University, Jaipur

Internship Project – InsightGPT Lite

⭐ Acknowledgement

This project was developed as an internship project to gain practical experience in:

Data Science
Data Analytics
Machine Learning
Generative AI
Retrieval-Augmented Generation
Vector Databases
Natural Language Processing
Streamlit Application Development
Statistical Data Analysis
Git and GitHub
📜 License

This project is developed for educational and internship purposes.