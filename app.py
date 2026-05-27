import streamlit as st
import pandas as pd

from utils.preprocessing import remove_duplicates, fill_missing_values
from utils.visualization import create_histogram, create_scatter

st.set_page_config(
    page_title="InsightGPT Lite",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightGPT Lite")
st.subheader("AI-Powered Data Analytics and RAG Platform")

# File Upload
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    st.write("### Dataset Preview")
    st.dataframe(df.head())

    st.write("### Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.write("### Column Data Types")
    st.dataframe(df.dtypes.astype(str))

    st.write("### Data Cleaning")

    if st.button("Remove Duplicates"):
        df = remove_duplicates(df)
        st.success("Duplicates removed!")

    if st.button("Fill Missing Values"):
        df = fill_missing_values(df)
        st.success("Missing values filled!")

    st.write("### Data Visualization")

    numeric_columns = df.select_dtypes(include=['number']).columns

    if len(numeric_columns) > 0:

        selected_column = st.selectbox(
            "Select column for histogram",
            numeric_columns
        )

        hist_fig = create_histogram(df, selected_column)

        st.plotly_chart(hist_fig)

    if len(numeric_columns) >= 2:

        x_col = st.selectbox("X-axis", numeric_columns)

        y_col = st.selectbox("Y-axis", numeric_columns, index=1)

        scatter_fig = create_scatter(df, x_col, y_col)

        st.plotly_chart(scatter_fig)

st.sidebar.title("InsightGPT Lite")
st.sidebar.info("AI-Powered Data Analytics Platform")