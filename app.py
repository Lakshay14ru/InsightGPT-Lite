import streamlit as st
import pandas as pd
import plotly.express as px

from utils.analytics import dataset_summary, dataset_health_score, advanced_eda, detect_outliers, correlation_matrix, generate_eda_summary
from utils.report_generator import generate_report
from utils.filtering import filter_dataframe
from utils.preprocessing import remove_duplicates, fill_missing_values
from utils.visualization import create_histogram, create_scatter, create_box_plot, create_bar_chart, create_pie_chart, create_line_chart
from utils.ai_engine import ask_gemini
from utils.ai_analytics import generate_ai_dataset_summary
from utils.rag_pipeline import split_text
from utils.embedding_model import create_embeddings
from utils.chroma_db import store_chunks, search_chunks

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="InsightGPT Lite",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightGPT Lite")
st.subheader("AI-Powered Data Analytics and RAG Platform")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Dashboard",
        "🧹 Cleaning",
        "📈 Visualizations",
        "🤖 AI Insights"
    ]
)

# ===============================
# SIDEBAR
# ===============================

st.sidebar.title("InsightGPT Lite")
st.sidebar.info("AI-Powered Data Analytics Platform")
st.sidebar.markdown("""
### Features

✅ CSV Upload

✅ Dataset Preview

✅ Data Cleaning

✅ Dataset Filtering

✅ Interactive Visualizations

✅ PDF Report Generation

✅ AI Insights

✅ ChromaDB Integration

✅ Retrieval-Augmented Generation (RAG)
""")

# ===============================
# FILE UPLOAD
# ===============================

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    # ===============================
    # LOAD DATASET
    # ===============================

    df = pd.read_csv(uploaded_file)
    summary = dataset_summary(df)
    health_score = dataset_health_score(df)
    eda = advanced_eda(df)
    outlier_results = detect_outliers(df)
    correlation = correlation_matrix(df)
    eda_summary = generate_eda_summary(
        df,
        summary,
        health_score,
        outlier_results
    )

    st.success("File uploaded successfully!")

    # ===============================
    # RAG PIPELINE TESTING
    # ===============================

    dataset_text = df.to_string(index=False)

    chunks = split_text(dataset_text)

    embeddings = create_embeddings(chunks[:5])

    store_chunks(chunks)

    with tab1:

        st.success("File uploaded successfully!")

        st.success("Chunks stored in ChromaDB successfully!")

        st.write("## 🧠 RAG Statistics")

        st.write(f"Chunks Created: {len(chunks)}")

        st.write(f"Embedding Shape: {embeddings.shape}")

    if chunks:
        st.write("### 🧠 RAG Processing")
        rag_col1, rag_col2 = st.columns(2)
        with rag_col1:
            st.metric(
                "Text Chunks",
                len(chunks)
                )

        with rag_col2:
            st.metric(
                "Embedding Dimensions",
                embeddings.shape[1]
                )

        with st.expander("🔍 View Sample RAG Chunk"):
            st.code(
                chunks[0][:1000],
                language="text"
                )

        # ===============================
        # DATASET PREVIEW
        # ===============================

        st.write("### Dataset Preview")
        st.dataframe(df.head())
        st.write("## 📈 Smart Dataset Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric(
             "Rows",
             summary["Rows"]
             )

        col2.metric(
            "Columns",
            summary["Columns"]
            )

        col3.metric(
             "Missing Values",
             summary["Missing Values"]
             )
        col4, col5, col6 = st.columns(3)

        col4.metric(
             "Duplicates",
             summary["Duplicate Records"]
             )
        col5.metric(
             "Numerical Columns",
             summary["Numerical Columns"]
             )
        col6.metric(
             "Categorical Columns",
             summary["Categorical Columns"]
             )
        st.metric(
            "Memory Usage (KB)",
            summary["Memory Usage (KB)"]
            )

        
        st.write("## 💚 Dataset Health Score")
        st.progress(health_score / 100)
        st.metric(
            "Health Score",
            f"{health_score}%"
            )
        
        if health_score >= 90:
            st.success("Excellent Dataset ✅")
        elif health_score >= 75:
            st.info("Good Dataset 👍")
        elif health_score >= 50:
            st.warning("Dataset Needs Cleaning ⚠")
        else:
            st.error("Poor Dataset ❌")

        st.write("### 💡 Recommendations")

        if summary["Missing Values"] > 0:
            st.write("✔ Fill missing values.")

            if summary["Duplicate Records"] > 0:
                st.write("✔ Remove duplicate records.")

                if (
                    summary["Missing Values"] == 0
                    and summary["Duplicate Records"] == 0
                    ):
                    st.write("✔ Dataset is clean and ready for analysis.")


        st.write("## 🧠 Automated EDA Summary")
        st.info(eda_summary) 

        st.write("## 🤖 AI Dataset Summary")
        if st.button(
            "✨ Generate AI Dataset Summary",
            key="ai_dataset_summary"
            ):
            with st.spinner(
                "AI is analyzing your dataset..."
                ):
                ai_prompt = generate_ai_dataset_summary(
                    df,
                    summary,
                    eda_summary
                    )
                ai_response = ask_gemini(
                    ai_prompt
                    )
                st.write("### 🧠 AI Analysis")
                st.success(ai_response)

        st.write("## 📈 Advanced EDA")
        st.write("### Unique Values")
        st.dataframe(
            eda["Unique Values"]
            )
        
        st.write("### Missing Percentage")
        st.dataframe(
            eda["Missing Percentage"]
            )

        st.write("### Data Types")
        st.dataframe(
            eda["Data Types"]
            )

        st.write("## 📦 Outlier Analysis")
        if outlier_results:
            outlier_table = []
            for column, result in outlier_results.items():
                outlier_table.append({
                    "Column": column,
                    "Q1": result["Q1"],
                    "Q3": result["Q3"],
                    "IQR": result["IQR"],
                    "Outliers": result["Outliers"],
                    "Outlier %": result["Outlier Percentage"]
                    })

            outlier_df = pd.DataFrame(outlier_table)

            st.dataframe(
                outlier_df,
                use_container_width=True
                )
        else:
            st.info(
                "No numerical columns available "
                "for outlier analysis."
                )

        st.write("## 📊 Correlation Analysis")
        if correlation is not None:
            st.write(
                "The correlation matrix shows the "
                "relationship between numerical variables."
                )
            st.dataframe(
                correlation.round(2),
                use_container_width=True
                )
            st.write("### 🔥 Correlation Heatmap")
            heatmap_fig = px.imshow(
                correlation,
                text_auto=".2f",
                aspect="auto",
                title="Feature Correlation Heatmap"
            )

            st.plotly_chart(
                heatmap_fig,
                use_container_width=True
            )
        else:
            st.info(
                "At least two numerical columns "
                "are required for correlation analysis."
                )


        # ===============================
        # DATASET INFORMATION
        # ===============================

        st.write("### Dataset Information")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        # ===============================
        # DATA TYPES
        # ===============================

        st.write("### Column Data Types")
        st.dataframe(df.dtypes.astype(str))

        # ===============================
        # DATASET FILTERS
        # ===============================

        st.write("### Dataset Filters")

        filter_columns = df.columns.tolist()

        selected_filter_column = st.selectbox(
            "Select Column to Filter",
            filter_columns
        )

        selected_values = st.multiselect(
            "Select Values",
            df[selected_filter_column].dropna().unique()
        )

        if selected_values:

            df = filter_dataframe(
                df,
                selected_filter_column,
                selected_values
            )

            st.success(f"{len(df)} records found.")

            st.dataframe(df.head())
    
    with tab2:
        # ===============================
        # DATA CLEANING
        # ===============================

        st.write("### Data Cleaning")

        if st.button("Remove Duplicates"):
            df = remove_duplicates(df)
            st.success("Duplicates removed!")

        if st.button("Fill Missing Values"):
           df = fill_missing_values(df)
           st.success("Missing values filled!")
    
        csv = df.to_csv(index=False)

        st.download_button(
            label="📥 Download Dataset",
            data=csv,
            file_name="processed_dataset.csv",
            mime="text/csv"
)
        if st.button("📄 Generate PDF Report"):
            report_path = generate_report(df)
            with open(report_path, "rb") as file:
                st.download_button(
                    label="⬇ Download PDF Report",
                    data=file,
                    file_name="InsightGPT_Report.pdf",
                    mime="application/pdf"
        )
    
    with tab3:
        # ===============================
        # VISUALIZATION
        # ===============================

        st.write("### Data Visualization")
        
        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) > 0:
            
            selected_column = st.selectbox(
                "Select column for histogram",
                 numeric_columns
        )
            
            hist_fig = create_histogram(df, selected_column)
            
            st.plotly_chart(hist_fig)

        if len(numeric_columns) >= 2:
            x_col = st.selectbox(
                "X-axis",
                numeric_columns,
                key="x_axis"
        )

            y_col = st.selectbox(
                "Y-axis",
                numeric_columns,
                index=1,
                key="y_axis"
        )
            scatter_fig = create_scatter(df, x_col, y_col)
            
            st.plotly_chart(scatter_fig)

        st.write("## 📦 Box Plot")
        if len(numeric_columns) > 0:
            box_column = st.selectbox(
                "Select column for Box Plot",
                numeric_columns,
                key="box_plot_column"
            )
            box_fig = create_box_plot(
                df,
                box_column
            )
            st.plotly_chart(
                box_fig,
                use_container_width=True
            )

        st.write("## 📊 Bar Chart")
        categorical_columns = df.select_dtypes(
            include=["object", "category"]
            ).columns
        if len(categorical_columns) > 0:
            bar_column = st.selectbox(
                "Select categorical column",
                categorical_columns,
                key="bar_chart_column"
            )

            bar_fig = create_bar_chart(
                df,
                bar_column
            )

            st.plotly_chart(
                bar_fig,
                use_container_width=True
            )

        else:
            st.info(
                "No categorical columns available "
                "for Bar Chart."
            )

        st.write("## 🥧 Pie Chart")
        if len(categorical_columns) > 0:
            pie_column = st.selectbox(
                "Select categorical column",
                categorical_columns,
                key="pie_chart_column"
            )

            pie_fig = create_pie_chart(
                df,
                pie_column
            )

            st.plotly_chart(
                pie_fig,
                use_container_width=True
            )
        else:
            st.info(
                "No categorical columns available "
                "for Pie Chart."
            )

        st.write("## 📈 Line Chart")
        if len(numeric_columns) >= 2:
            line_x = st.selectbox(
                "Select X-axis for Line Chart",
                numeric_columns,
                key="line_x"
            )

            line_y = st.selectbox(
                "Select Y-axis for Line Chart",
                numeric_columns,
                key="line_y"
            )

            line_fig = create_line_chart(
                df,
                line_x,
                line_y
            )

            st.plotly_chart(
                line_fig,
                use_container_width=True
            )
        else:
            st.info(
                "At least two numerical columns "
                "are required for Line Chart."
            )

    with tab4:
        st.write("## 🤖 Ask AI About Your Dataset")
        user_question = st.text_input(
            "Enter your question about the dataset"
        )

        if st.button(
            "Generate AI Insight",
            key="ai_button"
        ):
            if user_question.strip() == "":

                st.warning(
                    "Please enter a question."
                )

            else:
                with st.spinner(
                    "Analyzing dataset..."
                ):

                    results = search_chunks(
                        user_question
                    )

                    retrieved_chunks = "\n\n".join(
                        results["documents"][0]
                )


                
                outlier_results = detect_outliers(df) 
                outlier_context = ""
                for column, result in outlier_results.items():
                    outlier_context += (
                        f"{column}: "
                        f"{result['Outliers']} outliers detected\n"
                    )   

                prompt = f"""
You are an expert data analytics assistant.

You are analyzing the user's uploaded dataset.

USER QUESTION:
{user_question}

RAG RETRIEVED CONTEXT:
{retrieved_chunks}

STATISTICAL OUTLIER ANALYSIS:
{outlier_context}

INSTRUCTIONS:

1. Answer the user's question using the
   statistical analysis and retrieved context
   provided above.

2. For questions about outliers, use the
   STATISTICAL OUTLIER ANALYSIS rather than
   trying to calculate outliers from the raw
   retrieved rows.

3. For questions about the dataset, use the
   available statistical information whenever
   possible.

4. Do not say that the context is insufficient
   if the required answer is available in the
   statistical analysis.

5. Do not invent values or information.

6. Give a clear and concise analytical answer.

7. If useful, mention the relevant column names
   and numerical values.

Provide the final answer in a professional
data-analysis style.
"""

               

                response = ask_gemini(
                    prompt
                )

           

            st.write("### 🔎 RAG Retrieval")

            retrieved_count = len(
                results["documents"][0]
            )

            st.success(
                f"{retrieved_count} relevant context "
                f"chunks retrieved from ChromaDB."
            )

            with st.expander(
                "🔍 View Retrieved Context"
            ):

                for i, chunk in enumerate(
                    results["documents"][0],
                    start=1
                ):

                    st.markdown(
                        f"**Retrieved Context {i}**"
                    )

                    st.code(
                        chunk[:1000],
                        language="text"
                    )

            # ===============================
            # AI RESPONSE
            # ===============================

            st.write("### 🤖 AI Analysis")

            st.caption(
                "🧠 Response generated using "
                "ChromaDB semantic retrieval + Gemini."
            )

            with st.container(border=True):

                st.markdown(
                    response
                )
st.markdown("---")

st.markdown(
    """
    ### 🚀 InsightGPT Lite
    AI-Powered Data Analytics and Retrieval-Augmented Query Platform

    Developed by Lakshay Kundariya
    Internship Project – BCA Data Science
    """
)