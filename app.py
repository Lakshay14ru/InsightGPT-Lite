import streamlit as st
import pandas as pd

from utils.report_generator import generate_report
from utils.filtering import filter_dataframe
from utils.preprocessing import remove_duplicates, fill_missing_values
from utils.visualization import create_histogram, create_scatter
from utils.ai_engine import ask_gemini
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
            st.write("### Sample Chunk")
            st.text(chunks[0][:500])

        # ===============================
        # DATASET PREVIEW
        # ===============================

        st.write("### Dataset Preview")
        st.dataframe(df.head())

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
    

    with tab4:
        # ===============================
        # AI INSIGHTS
        # ===============================

        st.write("## 🤖 Ask AI About Your Dataset")
        user_question = st.text_input(
            "Enter your question about the dataset"
    )

        if st.button(
            "Generate AI Insight",
            key="ai_button"):
            if user_question.strip() == "":
                st.warning("Please enter a question.")

            else:
                with st.spinner("Analyzing dataset..."):
                    results = search_chunks(user_question)
                    retrieved_chunks = "\n\n".join(
                    results["documents"][0]
)

                prompt = f"""
You are a data analytics assistant.

Relevant Dataset Context:

{retrieved_chunks}

User Question:

{user_question}

Provide detailed analytical insights using only the retrieved context.
"""

                response = ask_gemini(prompt)

                st.write("### Retrieved Chunks")

                st.text(retrieved_chunks[:1000])

                st.write("### AI Response")

                st.success(response)
st.markdown("---")

st.markdown(
    """
    ### 🚀 InsightGPT Lite
    AI-Powered Data Analytics and Retrieval-Augmented Query Platform

    Developed by Lakshay Kundariya
    Internship Project – BCA Data Science
    """
)