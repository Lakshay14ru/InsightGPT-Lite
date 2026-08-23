import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
import re


# ============================================================
# IMPORTS
# ============================================================

from utils.question_classifier import classify_question
from utils.ai_context import generate_dataset_context
from utils.data_quality import calculate_data_quality

from utils.analytics import (
    dataset_summary,
    dataset_health_score,
    advanced_eda,
    detect_outliers,
    correlation_matrix,
    generate_eda_summary
)

from utils.report_generator import generate_report
from utils.filtering import filter_dataframe

from utils.preprocessing import (
    remove_duplicates,
    fill_missing_values
)

from utils.automatic_insights import (
    generate_automatic_insights,
    generate_ai_executive_summary,
    calculate_dataset_health
)

from utils.visualization import (
    create_histogram,
    create_scatter,
    create_box_plot,
    create_bar_chart,
    create_pie_chart,
    create_line_chart
)

from utils.ai_engine import ask_gemini

from utils.ai_analytics import (
    generate_ai_dataset_summary
)

from utils.ai_cleaning import (
    generate_cleaning_recommendations
)

from utils.rag_pipeline import (
    split_text
)

from utils.embedding_model import (
    create_embeddings
)

from utils.chroma_db import (
    store_chunks,
    search_chunks
)

from utils.advanced_analytics import (
    get_statistical_summary,
    get_correlation_matrix,
    get_strong_correlations,
    get_column_insights,
    generate_analytical_insights
)

from utils.statistical_question import (
    detect_groupwise_question,
    detect_survival_question
)

from utils.statistical_analysis import (
    groupwise_analysis,
    category_counts,
    survival_rate_by_group,
    numerical_summary,
    highest_group_average,
    lowest_group_average
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="InsightGPT Lite",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# DATASET FINGERPRINT
# ============================================================

def _dataset_fingerprint(dataframe):

    if dataframe is None:
        return None

    try:

        payload = pd.util.hash_pandas_object(
            dataframe,
            index=True
        ).values.tobytes()

        payload += "||".join(
            f"{c}:{dataframe[c].dtype}"
            for c in dataframe.columns
        ).encode(
            "utf-8",
            errors="ignore"
        )

        return hashlib.md5(
            payload
        ).hexdigest()

    except Exception:

        try:

            return hashlib.md5(
                dataframe.to_csv(
                    index=True
                ).encode(
                    "utf-8",
                    errors="ignore"
                )
            ).hexdigest()

        except Exception:

            return None


# ============================================================
# AI RESPONSE CLEANING
# ============================================================

def _clean_ai_response(text):

    if text is None:
        return ""

    cleaned = str(text)

    # Remove localhost SVG artifacts that sometimes appear
    # after Streamlit markdown rendering/copying.
    cleaned = re.sub(
        r"\[svg\]\(http://localhost:[^)]+\)",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\[svg\]\([^)]*localhost[^)]*\)",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    # Remove accidental empty markdown links
    cleaned = re.sub(
        r"\[\]\([^)]*\)",
        "",
        cleaned
    )

    # Remove excessive blank lines
    cleaned = re.sub(
        r"\n{3,}",
        "\n\n",
        cleaned
    )

    return cleaned.strip()


# ============================================================
# AI SUMMARY SANITIZATION
# ============================================================

def _sanitize_ai_executive_summary(
    text,
    dataframe
):

    if not text:
        return text

    cleaned = _clean_ai_response(
        text
    )

    if dataframe is None or dataframe.empty:
        return cleaned

    for column in dataframe.columns:

        missing = int(
            dataframe[column].isna().sum()
        )

        if missing == 0:
            continue

        total = len(dataframe)

        percentage = (
            missing / total * 100
            if total
            else 0
        )

        percentage_text = (
            f"{percentage:.1f}%"
        )

        patterns = [

            rf"{re.escape(percentage_text)}\s+of\s+the\s+(?:entire\s+)?dataset",

            rf"{re.escape(percentage_text)}\s+of\s+the\s+data"

        ]

        for pattern in patterns:

            cleaned = re.sub(
                pattern,
                f"{percentage_text} of the `{column}` column values",
                cleaned,
                flags=re.IGNORECASE
            )

    return cleaned.strip()


# ============================================================
# GROUP-WISE QUESTION FALLBACK
# ============================================================

def _detect_groupwise_question_fallback(
    question,
    dataframe
):

    q = str(question).lower().strip()

    categorical_columns = (
        dataframe
        .select_dtypes(
            include=[
                "object",
                "category"
            ]
        )
        .columns
        .tolist()
    )

    numerical_columns = (
        dataframe
        .select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    group_column = None
    value_column = None

    # ========================================================
    # GROUP COLUMN
    # ========================================================

    if (
        "gender" in q
        or "male" in q
        or "female" in q
        or "sex" in q
    ):

        for column in dataframe.columns:

            if column.lower() == "sex":

                group_column = column
                break

    if group_column is None:

        for column in categorical_columns:

            normalized_column = (
                column
                .lower()
                .replace("_", " ")
            )

            if normalized_column in q:

                group_column = column
                break

    if group_column is None:

        if (
            "school" in q
            and "school" in dataframe.columns
        ):

            group_column = "school"

    if group_column is None:

        if (
            "address" in q
            and "address" in dataframe.columns
        ):

            group_column = "address"

    if group_column is None:

        if (
            "parent job" in q
            and "Mjob" in dataframe.columns
        ):

            group_column = "Mjob"

    # ========================================================
    # VALUE COLUMN
    # ========================================================

    if (
        "final grade" in q
        or "final grades" in q
        or "final score" in q
        or "final scores" in q
        or "g3" in q
    ):

        for column in dataframe.columns:

            if column.lower() == "g3":

                value_column = column
                break

    if value_column is None:

        if (
            "grade" in q
            and "G3" in dataframe.columns
        ):

            value_column = "G3"

    if value_column is None:

        if "age" in q:

            for column in dataframe.columns:

                if column.lower() == "age":

                    value_column = column
                    break

    if value_column is None:

        if (
            "study time" in q
            and "studytime" in dataframe.columns
        ):

            value_column = "studytime"

    if value_column is None:

        if (
            "absence" in q
            and "absences" in dataframe.columns
        ):

            value_column = "absences"

    if value_column is None:

        for column in numerical_columns:

            if column.lower() in q:

                value_column = column
                break

    # ========================================================
    # GROUP-WISE DETECTION
    # ========================================================

    group_words = [

        "by",
        "among",
        "between",
        "which gender",
        "which group",
        "which category",
        "highest",
        "lowest",
        "average for",
        "average by",
        "mean by",
        "group"

    ]

    is_groupwise = (

        group_column is not None

        and

        value_column is not None

        and

        any(
            word in q
            for word in group_words
        )

    )

    return {

        "is_groupwise": is_groupwise,

        "group_column": group_column,

        "value_column": value_column

    }


# ============================================================
# QUESTION INTENT DETECTION
# ============================================================

def _detect_question_intent(
    question,
    dataframe
):

    q = str(question).lower().strip()

    intent = "general"

    # ========================================================
    # GROUP-WISE QUESTIONS
    # ========================================================

    if (
        "which gender" in q
        or "which group" in q
        or "which category" in q
        or "by gender" in q
        or "by group" in q
        or "average by" in q
        or "mean by" in q
        or "highest average" in q
        or "lowest average" in q
        or "highest mean" in q
        or "lowest mean" in q
    ):

        intent = "groupwise"

    # ========================================================
    # SURVIVAL QUESTIONS
    # ========================================================

    if (
        "survival" in q
        or "survived" in q
    ):

        intent = "survival"

    # ========================================================
    # OUTLIER QUESTIONS
    # ========================================================

    elif (
        "outlier" in q
        or "outliers" in q
        or "unusual value" in q
        or "unusual values" in q
        or "extreme value" in q
        or "extreme values" in q
        or "abnormal value" in q
        or "abnormal values" in q
    ):

        intent = "outlier"

    # ========================================================
    # CORRELATION QUESTIONS
    # ========================================================

    elif (
        "correlation" in q
        or "correlated" in q
        or "relationship between" in q
        or "relationship among" in q
    ):

        intent = "correlation"

    # ========================================================
    # MISSING VALUE QUESTIONS
    # ========================================================

    elif (
        "missing" in q
        or "null" in q
        or "nan" in q
        or "empty value" in q
        or "empty values" in q
    ):

        intent = "missing"

    # ========================================================
    # DUPLICATE QUESTIONS
    # ========================================================

    elif (
        "duplicate" in q
        or "duplicates" in q
    ):

        intent = "duplicate"

    # ========================================================
    # AGE QUESTIONS
    # ========================================================

    elif "age" in q:

        intent = "age"

    # ========================================================
    # COUNT QUESTIONS
    # ========================================================

    elif (
        "how many" in q
        or "count" in q
        or "number of" in q
    ):

        intent = "count"

    # ========================================================
    # AVERAGE / MEAN QUESTIONS
    # ========================================================

    elif (
        "average" in q
        or "mean" in q
    ):

        intent = "average"

    # ========================================================
    # MEDIAN QUESTIONS
    # ========================================================

    elif "median" in q:

        intent = "median"

    # ========================================================
    # MINIMUM QUESTIONS
    # ========================================================

    elif (
        "minimum" in q
        or "lowest value" in q
        or "smallest" in q
    ):

        intent = "minimum"

    # ========================================================
    # MAXIMUM QUESTIONS
    # ========================================================

    elif (
        "maximum" in q
        or "highest value" in q
        or "largest" in q
    ):

        intent = "maximum"

    return intent


# ============================================================
# DIRECT STATISTICAL CONTEXT
# ============================================================

def _build_relevant_statistical_context(
    question,
    dataframe,
    groupwise_info,
    survival_info,
    intent
):

    q = str(question).lower().strip()

    context_parts = []

    # ========================================================
    # GROUP-WISE
    # ========================================================

    if (
        intent == "groupwise"
        and
        groupwise_info.get(
            "is_groupwise",
            False
        )
    ):

        group_column = (
            groupwise_info.get(
                "group_column"
            )
        )

        value_column = (
            groupwise_info.get(
                "value_column"
            )
        )

        if (
            group_column in dataframe.columns
            and
            value_column in dataframe.columns
        ):

            try:

                result = groupwise_analysis(
                    dataframe,
                    group_column,
                    value_column
                )

                if (
                    result is not None
                    and
                    not result.empty
                ):

                    context_parts.append(
                        "GROUP-WISE RESULT:\n"
                        +
                        result.to_string(
                            index=False
                        )
                    )

            except Exception as e:

                context_parts.append(
                    "GROUP-WISE ANALYSIS ERROR:\n"
                    f"{e}"
                )

    # ========================================================
    # SURVIVAL
    # ========================================================

    elif intent == "survival":

        if survival_info.get(
            "is_survival",
            False
        ):

            survival_group = (
                survival_info.get(
                    "group_column"
                )
            )

            if survival_group in dataframe.columns:

                try:

                    result = (
                        survival_rate_by_group(
                            dataframe,
                            survival_group
                        )
                    )

                    if (
                        result is not None
                        and
                        not result.empty
                    ):

                        context_parts.append(
                            "SURVIVAL RATE RESULT:\n"
                            +
                            result.to_string(
                                index=False
                            )
                        )

                except Exception as e:

                    context_parts.append(
                        "SURVIVAL ANALYSIS ERROR:\n"
                        f"{e}"
                    )

    # ========================================================
    # OUTLIERS
    # ========================================================

    elif intent == "outlier":

        try:

            results = detect_outliers(
                dataframe
            )

            if results:

                outlier_rows = []

                for column, result in results.items():

                    outlier_rows.append(
                        {
                            "Column": column,
                            "Outliers": result.get(
                                "Outliers",
                                0
                            ),
                            "Outlier Percentage": result.get(
                                "Outlier Percentage",
                                0
                            )
                        }
                    )

                if outlier_rows:

                    context_parts.append(
                        "OUTLIER RESULTS:\n"
                        +
                        pd.DataFrame(
                            outlier_rows
                        ).to_string(
                            index=False
                        )
                    )

        except Exception as e:

            context_parts.append(
                "OUTLIER ANALYSIS ERROR:\n"
                f"{e}"
            )

    # ========================================================
    # CORRELATION
    # ========================================================

    elif intent == "correlation":

        try:

            corr = get_correlation_matrix(
                dataframe
            )

            if corr is not None:

                context_parts.append(
                    "CORRELATION MATRIX:\n"
                    +
                    corr.round(3).to_string()
                )

                try:

                    strong = (
                        get_strong_correlations(
                            dataframe
                        )
                    )

                    if strong:

                        context_parts.append(
                            "STRONG CORRELATIONS:\n"
                            +
                            pd.DataFrame(
                                strong
                            ).to_string(
                                index=False
                            )
                        )

                except Exception:
                    pass

        except Exception as e:

            context_parts.append(
                "CORRELATION ANALYSIS ERROR:\n"
                f"{e}"
            )

    # ========================================================
    # MISSING VALUES
    # ========================================================

    elif intent == "missing":

        total_values = (
            dataframe.shape[0]
            *
            dataframe.shape[1]
        )

        missing_values = int(
            dataframe.isna()
            .sum()
            .sum()
        )

        percentage = (
            missing_values
            /
            total_values
            *
            100
            if total_values
            else 0
        )

        context_parts.append(
            "MISSING VALUE RESULT:\n"
            f"Missing values: {missing_values}\n"
            f"Missing percentage: {percentage:.2f}%"
        )

    # ========================================================
    # DUPLICATES
    # ========================================================

    elif intent == "duplicate":

        duplicates = int(
            dataframe.duplicated()
            .sum()
        )

        context_parts.append(
            "DUPLICATE RESULT:\n"
            f"Duplicate records: {duplicates}"
        )

    # ========================================================
    # AGE
    # ========================================================

    elif intent == "age":

        age_column = None

        for column in dataframe.columns:

            if column.lower() == "age":

                age_column = column
                break

        if age_column:

            series = pd.to_numeric(
                dataframe[age_column],
                errors="coerce"
            )

            context_parts.append(
                "AGE RESULT:\n"
                f"Average age: {series.mean():.3f}\n"
                f"Minimum age: {series.min():.3f}\n"
                f"Maximum age: {series.max():.3f}"
            )

    # ========================================================
    # AVERAGE
    # ========================================================

    elif intent == "average":

        numerical_columns = (
            dataframe
            .select_dtypes(
                include=["number"]
            )
            .columns
        )

        averages = {}

        for column in numerical_columns:

            averages[column] = round(
                dataframe[column].mean(),
                3
            )

        context_parts.append(
            "AVERAGE RESULTS:\n"
            +
            "\n".join(
                f"{column}: {value}"
                for column, value
                in averages.items()
            )
        )

    # ========================================================
    # MEDIAN
    # ========================================================

    elif intent == "median":

        numerical_columns = (
            dataframe
            .select_dtypes(
                include=["number"]
            )
            .columns
        )

        medians = {}

        for column in numerical_columns:

            medians[column] = round(
                dataframe[column].median(),
                3
            )

        context_parts.append(
            "MEDIAN RESULTS:\n"
            +
            "\n".join(
                f"{column}: {value}"
                for column, value
                in medians.items()
            )
        )

    # ========================================================
    # COUNT
    # ========================================================

    elif intent == "count":

        context_parts.append(
            "COUNT RESULTS:\n"
            f"Rows: {len(dataframe)}\n"
            f"Columns: {len(dataframe.columns)}"
        )

    # ========================================================
    # MINIMUM
    # ========================================================

    elif intent == "minimum":

        numerical_columns = (
            dataframe
            .select_dtypes(
                include=["number"]
            )
            .columns
        )

        values = {}

        for column in numerical_columns:

            values[column] = dataframe[
                column
            ].min()

        context_parts.append(
            "MINIMUM RESULTS:\n"
            +
            "\n".join(
                f"{column}: {value}"
                for column, value
                in values.items()
            )
        )

    # ========================================================
    # MAXIMUM
    # ========================================================

    elif intent == "maximum":

        numerical_columns = (
            dataframe
            .select_dtypes(
                include=["number"]
            )
            .columns
        )

        values = {}

        for column in numerical_columns:

            values[column] = dataframe[
                column
            ].max()

        context_parts.append(
            "MAXIMUM RESULTS:\n"
            +
            "\n".join(
                f"{column}: {value}"
                for column, value
                in values.items()
            )
        )

    return "\n\n".join(
        context_parts
    )


# ============================================================
# BUILD STRICT AI PROMPT
# ============================================================

def _build_ai_question_prompt(
    question,
    intent,
    statistical_context,
    dataset_context,
    rag_context
):

    prompt = f"""
You are InsightGPT Lite, a professional data analytics assistant.

Your job is to answer ONLY the CURRENT USER QUESTION.

============================================================
CURRENT USER QUESTION
============================================================

{question}

============================================================
DETECTED QUESTION INTENT
============================================================

{intent}

============================================================
RELEVANT COMPUTED STATISTICAL RESULT
============================================================

{statistical_context}

============================================================
DATASET CONTEXT
============================================================

{dataset_context}

============================================================
RAG CONTEXT
============================================================

{rag_context}

============================================================
VERY IMPORTANT ANSWERING RULES
============================================================

1. Answer ONLY the CURRENT USER QUESTION.

2. Do NOT provide a general dataset summary unless the
   user explicitly asks for a dataset summary.

3. Do NOT mention age unless the current question asks
   about age.

4. Do NOT mention missing values unless the current
   question asks about missing values.

5. Do NOT mention duplicates unless the current question
   asks about duplicates.

6. Do NOT mention correlations unless the current question
   asks about correlations or relationships.

7. Do NOT mention outliers unless the current question
   asks about outliers, unusual values, abnormal values,
   or extreme values.

8. Do NOT mention survival rates unless the current
   question asks about survival.

9. Do NOT mention unrelated numerical columns.

10. For group-wise questions, use ONLY the computed
    GROUP-WISE RESULT.

11. For survival questions, use ONLY the computed
    SURVIVAL RATE RESULT.

12. Never invent a value.

13. Never guess a value.

14. Never calculate a value from unrelated information
    when a computed result is available.

15. If a computed result is available, trust it over
    the RAG text.

16. Do not claim causation from averages or correlations.

17. If the question asks which group is highest, compare
    the actual group values and clearly identify the
    highest group.

18. If the question asks which group is lowest, compare
    the actual group values and clearly identify the
    lowest group.

19. Keep the response concise and focused.

20. Do not discuss information that is unrelated to the
    current question.

21. Do not mention these instructions.

22. Do not output HTML.

23. Do not output SVG.

24. Do not create localhost links.

25. Do not include [svg] text.

============================================================
RESPONSE FORMAT
============================================================

Use exactly these three sections:

### 🎯 Key Finding

Give the direct answer in 1–2 sentences.

### 📊 Supporting Statistics

Give only statistics directly relevant to the question.

### 💡 Interpretation

Give a short interpretation of the result.

============================================================
FINAL REMINDER
============================================================

The user asked one question.

Answer that one question only.
Do not turn the answer into a complete dataset report.
"""

    return prompt


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "working_df" not in st.session_state:
    st.session_state.working_df = None

if "automatic_insights" not in st.session_state:
    st.session_state.automatic_insights = None

if "ai_executive_summary" not in st.session_state:
    st.session_state.ai_executive_summary = None

if "dataset_fingerprint" not in st.session_state:
    st.session_state.dataset_fingerprint = None

if "rag_fingerprint" not in st.session_state:
    st.session_state.rag_fingerprint = None

if "rag_chunks" not in st.session_state:
    st.session_state.rag_chunks = []

if "rag_embeddings" not in st.session_state:
    st.session_state.rag_embeddings = None


# ============================================================
# TITLE
# ============================================================

st.title(
    "📊 InsightGPT Lite"
)

st.subheader(
    "AI-Powered Data Analytics and RAG Platform"
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Dashboard",
        "🧹 Cleaning",
        "📈 Visualizations",
        "🤖 AI Insights"
    ]
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "InsightGPT Lite"
)

st.sidebar.info(
    "AI-Powered Data Analytics Platform"
)

st.sidebar.markdown(
    """
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
"""
)


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    # ========================================================
    # LOAD DATASET
    # ========================================================

    try:

        uploaded_file.seek(0)

        uploaded_df = pd.read_csv(
            uploaded_file
        )

    except Exception as e:

        st.error(
            "Unable to read the uploaded CSV file."
        )

        st.exception(e)

        st.stop()


    # ========================================================
    # BASIC VALIDATION
    # ========================================================

    if uploaded_df is None:

        st.error(
            "The uploaded dataset could not be loaded."
        )

        st.stop()


    if uploaded_df.empty:

        st.warning(
            "The uploaded CSV file is empty."
        )

        st.stop()


    current_fingerprint = (
        _dataset_fingerprint(
            uploaded_df
        )
    )


    # ========================================================
    # NEW DATASET DETECTED
    # ========================================================

    if (
        st.session_state.dataset_fingerprint
        != current_fingerprint
    ):

        st.session_state.dataset_fingerprint = (
            current_fingerprint
        )

        st.session_state.working_df = (
            uploaded_df.copy()
        )

        st.session_state.automatic_insights = None

        st.session_state.ai_executive_summary = None

        st.session_state.rag_fingerprint = None

        st.session_state.rag_chunks = []

        st.session_state.rag_embeddings = None


    # ========================================================
    # SAFE WORKING DATASET INITIALIZATION
    # ========================================================

    working_df = st.session_state.get(
        "working_df",
        None
    )


    if (
        working_df is None
        or not isinstance(
            working_df,
            pd.DataFrame
        )
    ):

        st.session_state.working_df = (
            uploaded_df.copy()
        )

        working_df = (
            st.session_state.working_df
        )


    # ========================================================
    # FINAL SAFETY CHECK
    # ========================================================

    if working_df is None:

        st.error(
            "Working dataset could not be initialized."
        )

        st.stop()


    if not isinstance(
        working_df,
        pd.DataFrame
    ):

        st.error(
            "Working dataset is not a valid pandas DataFrame."
        )

        st.stop()


    if working_df.empty:

        st.warning(
            "The current working dataset contains no rows."
        )

        st.stop()


    # ========================================================
    # SAFE COPY
    # ========================================================

    df = working_df.copy()


    # ========================================================
    # DATASET ANALYSIS
    # ========================================================

    try:

        summary = dataset_summary(
            df
        )

        outlier_results = detect_outliers(
            df
        )

        quality = calculate_data_quality(
            df,
            outlier_results
        )

        health_score = dataset_health_score(
            df
        )

        eda = advanced_eda(
            df
        )

        correlation = correlation_matrix(
            df
        )

        eda_summary = generate_eda_summary(
            df,
            summary,
            health_score,
            outlier_results
        )

    except Exception as e:

        st.error(
            "Dataset analysis failed."
        )

        st.exception(e)

        st.stop()


    st.success(
        "File uploaded successfully!"
    )


    # ========================================================
    # RAG PIPELINE
    # ========================================================

    current_working_fingerprint = (
        _dataset_fingerprint(
            df
        )
    )


    if (
        st.session_state.rag_fingerprint
        != current_working_fingerprint
    ):

        try:

            dataset_text = df.to_string(
                index=False
            )

            chunks = split_text(
                dataset_text
            )

            embeddings = None


            if chunks:

                embeddings = create_embeddings(
                    chunks[:5]
                )

                store_chunks(
                    chunks
                )


            st.session_state.rag_chunks = (
                chunks
            )

            st.session_state.rag_embeddings = (
                embeddings
            )

            st.session_state.rag_fingerprint = (
                current_working_fingerprint
            )

        except Exception as e:

            st.warning(
                "RAG processing could not be completed."
            )

            st.exception(e)

            chunks = []

            embeddings = None

    else:

        chunks = st.session_state.get(
            "rag_chunks",
            []
        )

        embeddings = st.session_state.get(
            "rag_embeddings",
            None
        )


    # ============================================================
    # TAB 1 - DASHBOARD
    # ============================================================

    with tab1:

        if chunks:

            st.success(
                "Chunks stored in ChromaDB successfully!"
            )


        # ========================================================
        # RAG STATISTICS
        # ========================================================

        st.write(
            "## 🧠 RAG Statistics"
        )

        st.write(
            f"Chunks Created: {len(chunks)}"
        )


        if embeddings is not None:

            try:

                st.write(
                    f"Embedding Shape: {embeddings.shape}"
                )

            except Exception:

                st.write(
                    "Embeddings generated successfully."
                )

        else:

            st.warning(
                "Embeddings are not available."
            )


        if chunks:

            st.write(
                "### 🧠 RAG Processing"
            )

            rag_col1, rag_col2 = st.columns(
                2
            )

            with rag_col1:

                st.metric(
                    "Text Chunks",
                    len(chunks)
                )

            with rag_col2:

                embedding_dimensions = 0

                try:

                    if embeddings is not None:

                        embedding_dimensions = (
                            embeddings.shape[1]
                        )

                except Exception:

                    embedding_dimensions = 0


                st.metric(
                    "Embedding Dimensions",
                    embedding_dimensions
                )


            with st.expander(
                "🔍 View Sample RAG Chunk"
            ):

                st.code(
                    chunks[0][:1000],
                    language="text"
                )


        # ========================================================
        # DATASET PREVIEW
        # ========================================================

        st.write(
            "### Dataset Preview"
        )

        st.dataframe(
            df.head(),
            use_container_width=True
        )


        # ========================================================
        # SMART DATASET SUMMARY
        # ========================================================

        st.write(
            "## 📈 Smart Dataset Summary"
        )

        col1, col2, col3 = st.columns(
            3
        )

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


        col4, col5, col6 = st.columns(
            3
        )

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


        # ========================================================
        # DATA QUALITY
        # ========================================================

        st.write(
            "### 🩺 Data Quality"
        )

        st.progress(
            max(
                0,
                min(
                    quality["quality_score"] / 100,
                    1
                )
            )
        )

        st.caption(
            f"Overall Data Quality Score: "
            f"{quality['quality_score']}%"
        )


        quality_col1, quality_col2, quality_col3, quality_col4 = (
            st.columns(4)
        )


        quality_col1.metric(
            "Quality Score",
            f"{quality['quality_score']}%"
        )

        quality_col2.metric(
            "Missing Values",
            quality["missing_values"]
        )

        quality_col3.metric(
            "Duplicate Records",
            quality["duplicate_records"]
        )

        quality_col4.metric(
            "Overall Status",
            quality["overall_status"]
        )


        # ========================================================
        # QUALITY DETAILS
        # ========================================================

        st.write(
            "#### 🔎 Data Quality Details"
        )

        quality_data = {

            "Data Quality Check": [

                "Missing Values",

                "Duplicate Records"

            ],

            "Status": [

                quality["missing_status"],

                quality["duplicate_status"]

            ],

            "Severity": [

                quality["missing_severity"],

                quality["duplicate_severity"]

            ],

            "Percentage": [

                f"{quality['missing_percentage']}%",

                f"{quality['duplicate_percentage']}%"

            ]

        }


        st.dataframe(
            quality_data,
            use_container_width=True,
            hide_index=True
        )


        # ========================================================
        # DATASET HEALTH SUMMARY
        # ========================================================

        st.write(
            "#### 📊 Dataset Health Summary"
        )

        summary_col1, summary_col2 = st.columns(
            2
        )


        with summary_col1:

            st.info(
                f"""
**Numerical Columns:**  
{quality['numerical_columns']}

**Categorical Columns:**  
{quality['categorical_columns']}
"""
            )


        with summary_col2:

            if quality["quality_score"] >= 90:

                st.success(
                    "The dataset has excellent overall quality."
                )

            elif quality["quality_score"] >= 75:

                st.success(
                    "The dataset has good quality with minor issues."
                )

            elif quality["quality_score"] >= 50:

                st.warning(
                    "The dataset needs cleaning before deeper analysis."
                )

            else:

                st.error(
                    "The dataset requires significant cleaning."
                )


        # ========================================================
        # DATASET HEALTH SCORE
        # ========================================================

        st.write(
            "## 💚 Dataset Health Score"
        )

        st.progress(
            max(
                0,
                min(
                    health_score / 100,
                    1
                )
            )
        )

        st.metric(
            "Health Score",
            f"{health_score}%"
        )


        if health_score >= 90:

            st.success(
                "Excellent Dataset ✅"
            )

        elif health_score >= 75:

            st.info(
                "Good Dataset 👍"
            )

        elif health_score >= 50:

            st.warning(
                "Dataset Needs Cleaning ⚠"
            )

        else:

            st.error(
                "Poor Dataset ❌"
            )


        # ========================================================
        # RECOMMENDATIONS
        # ========================================================

        st.write(
            "### 💡 Recommendations"
        )


        if summary["Missing Values"] > 0:

            st.write(
                "✔ Fill missing values."
            )


        if summary["Duplicate Records"] > 0:

            st.write(
                "✔ Remove duplicate records."
            )


        if (
            summary["Missing Values"] == 0
            and
            summary["Duplicate Records"] == 0
        ):

            st.write(
                "✔ Dataset is clean and ready for analysis."
            )


        # ========================================================
        # AUTOMATED EDA
        # ========================================================

        st.write(
            "## 🧠 Automated EDA Summary"
        )

        st.info(
            eda_summary
        )


        # ========================================================
        # AI DATASET SUMMARY
        # ========================================================

        st.write(
            "## 🤖 AI Dataset Summary"
        )


        if st.button(
            "✨ Generate AI Dataset Summary",
            key="ai_dataset_summary"
        ):

            with st.spinner(
                "AI is analyzing your dataset..."
            ):

                ai_prompt = (
                    generate_ai_dataset_summary(
                        df,
                        summary,
                        eda_summary
                    )
                )

                ai_response = ask_gemini(
                    ai_prompt
                )

            st.write(
                "### 🧠 AI Analysis"
            )

            st.success(
                _clean_ai_response(
                    ai_response
                )
            )


        # ========================================================
        # ADVANCED EDA
        # ========================================================

        st.write(
            "## 📈 Advanced EDA"
        )


        st.write(
            "### Unique Values"
        )

        st.dataframe(
            eda["Unique Values"]
        )


        st.write(
            "### Missing Percentage"
        )

        st.dataframe(
            eda["Missing Percentage"]
        )


        st.write(
            "### Data Types"
        )

        st.dataframe(
            eda["Data Types"]
        )


        # ========================================================
        # OUTLIER ANALYSIS
        # ========================================================

        st.write(
            "## 📦 Outlier Analysis"
        )


        if outlier_results:

            outlier_table = []


            for column, result in outlier_results.items():

                outlier_table.append(
                    {
                        "Column": column,

                        "Q1": result["Q1"],

                        "Q3": result["Q3"],

                        "IQR": result["IQR"],

                        "Outliers": result["Outliers"],

                        "Outlier %": result["Outlier Percentage"]
                    }
                )


            outlier_df = pd.DataFrame(
                outlier_table
            )


            st.dataframe(
                outlier_df,
                use_container_width=True
            )

        else:

            st.info(
                "No numerical columns available "
                "for outlier analysis."
            )


        # ========================================================
        # CORRELATION
        # ========================================================

        st.write(
            "## 📊 Correlation Analysis"
        )


        if correlation is not None:

            st.write(
                "The correlation matrix shows the "
                "relationship between numerical variables."
            )


            st.dataframe(
                correlation.round(2),
                use_container_width=True
            )


            st.write(
                "### 🔥 Correlation Heatmap"
            )


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


        # ========================================================
        # DATASET INFORMATION
        # ========================================================

        st.write(
            "### Dataset Information"
        )


        col1, col2, col3 = st.columns(
            3
        )


        col1.metric(
            "Rows",
            df.shape[0]
        )

        col2.metric(
            "Columns",
            df.shape[1]
        )

        col3.metric(
            "Missing Values",
            df.isnull().sum().sum()
        )


        # ========================================================
        # DATA TYPES
        # ========================================================

        st.write(
            "### Column Data Types"
        )

        st.dataframe(
            df.dtypes.astype(str)
        )


        # ========================================================
        # AUTOMATIC DATASET INSIGHTS
        # ========================================================

        st.write(
            "## 💡 Automatic Dataset Insights"
        )

        st.caption(
            "Automatically generated analytical observations "
            "from the uploaded dataset."
        )


        if st.button(
            "✨ Generate Automatic Insights",
            key="automatic_insights_button"
        ):

            with st.spinner(
                "Analyzing dataset..."
            ):

                automatic_outliers = detect_outliers(
                    df
                )

                st.session_state.automatic_insights = (
                    generate_automatic_insights(
                        df,
                        summary=summary,
                        outlier_results=automatic_outliers
                    )
                )

                st.session_state.ai_executive_summary = None


        # ========================================================
        # DISPLAY AUTOMATIC INSIGHTS
        # ========================================================

        if (
            st.session_state.automatic_insights
            is not None
        ):

            automatic_insights = (
                st.session_state.automatic_insights
            )


            dataset_health = (
                calculate_dataset_health(
                    automatic_insights
                )
            )


            st.success(
                "Automatic dataset analysis completed!"
            )


            # ====================================================
            # DATASET OVERVIEW
            # ====================================================

            st.write(
                "### 📊 Dataset Overview"
            )


            dataset_info = (
                automatic_insights[
                    "dataset"
                ]
            )


            col1, col2 = st.columns(
                2
            )


            with col1:

                st.metric(
                    "Total Rows",
                    f"{dataset_info['rows']:,}"
                )


            with col2:

                st.metric(
                    "Total Columns",
                    dataset_info["columns"]
                )


            st.info(
                dataset_info["message"]
            )


            # ====================================================
            # DATA QUALITY
            # ====================================================

            st.write(
                "### ⚠️ Data Quality"
            )


            quality_info = (
                automatic_insights[
                    "data_quality"
                ]
            )


            col1, col2 = st.columns(
                2
            )


            with col1:

                st.metric(
                    "Missing Values",
                    f"{quality_info['missing_count']:,}"
                )


            with col2:

                st.metric(
                    "Duplicate Records",
                    f"{quality_info['duplicates']:,}"
                )


            with st.container(
                border=True
            ):

                st.markdown(
                    "#### Missing Data"
                )

                st.write(
                    quality_info[
                        "missing_message"
                    ]
                )


                st.markdown(
                    "#### Duplicate Records"
                )

                st.write(
                    quality_info[
                        "duplicate_message"
                    ]
                )


            # ====================================================
            # COLUMN ANALYSIS
            # ====================================================

            st.write(
                "### 🔢 Column Analysis"
            )


            column_info = (
                automatic_insights[
                    "columns"
                ]
            )


            col1, col2 = st.columns(
                2
            )


            with col1:

                st.metric(
                    "Numerical Columns",
                    column_info[
                        "numerical_count"
                    ]
                )


            with col2:

                st.metric(
                    "Categorical Columns",
                    column_info[
                        "categorical_count"
                    ]
                )


            # ====================================================
            # OUTLIER ANALYSIS
            # ====================================================

            st.write(
                "### 🔴 Outlier Analysis"
            )


            outlier_info = (
                automatic_insights[
                    "outliers"
                ]
            )


            with st.container(
                border=True
            ):

                if outlier_info["column"]:

                    st.markdown(
                        f"**Highest Outlier Count:** "
                        f"`{outlier_info['column']}`"
                    )


                    st.metric(
                        "Potential Outliers",
                        f"{outlier_info['count']:,}"
                    )


                    st.write(
                        outlier_info["message"]
                    )

                else:

                    st.success(
                        outlier_info["message"]
                    )


            # ====================================================
            # CORRELATION
            # ====================================================

            st.write(
                "### 📈 Correlation Analysis"
            )


            correlation_info = (
                automatic_insights[
                    "correlation"
                ]
            )


            with st.container(
                border=True
            ):

                if correlation_info["column_a"]:

                    col1, col2, col3 = st.columns(
                        3
                    )


                    with col1:

                        st.metric(
                            "Column 1",
                            correlation_info[
                                "column_a"
                            ]
                        )


                    with col2:

                        st.metric(
                            "Column 2",
                            correlation_info[
                                "column_b"
                            ]
                        )


                    with col3:

                        st.metric(
                            "Correlation",
                            correlation_info[
                                "value"
                            ]
                        )


                    st.write(
                        correlation_info[
                            "message"
                        ]
                    )

                else:

                    st.info(
                        correlation_info[
                            "message"
                        ]
                    )


            # ====================================================
            # KEY FINDINGS
            # ====================================================

            st.write(
                "### 🎯 Key Findings"
            )


            with st.container(
                border=True
            ):

                st.markdown(
                    f"""
**Dataset:** {dataset_info['rows']:,} rows ×
{dataset_info['columns']} columns

**Missing Data:**  
{quality_info['missing_message']}

**Duplicates:**  
{quality_info['duplicate_message']}

**Outliers:**  
{outlier_info['message']}

**Correlation:**  
{correlation_info['message']}
"""
                )


            # ====================================================
            # AI EXECUTIVE SUMMARY
            # ====================================================

            st.write(
                "### 🧠 AI Executive Summary"
            )


            st.caption(
                "Gemini converts the computed statistical "
                "findings into a concise analytical summary."
            )


            if st.button(
                "✨ Generate AI Executive Summary",
                key="ai_executive_summary_button"
            ):

                with st.spinner(
                    "Generating AI executive summary..."
                ):

                    generated_summary = (
                        generate_ai_executive_summary(
                            df,
                            automatic_insights,
                            ask_gemini
                        )
                    )


                    st.session_state.ai_executive_summary = (
                        _sanitize_ai_executive_summary(
                            generated_summary,
                            df
                        )
                    )


            if (
                st.session_state.ai_executive_summary
                is not None
            ):

                with st.container(
                    border=True
                ):

                    st.markdown(
                        st.session_state.ai_executive_summary
                    )


            # ====================================================
            # DATASET HEALTH
            # ====================================================

            st.write(
                "### 🩺 Dataset Health"
            )


            st.caption(
                "Overall assessment based on missing data, "
                "duplicates, and potential outliers."
            )


            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    2
                )


                with col1:

                    st.metric(
                        "Health Score",
                        f"{dataset_health['score']}/100"
                    )


                with col2:

                    st.metric(
                        "Overall Status",
                        dataset_health["status"]
                    )


                st.progress(
                    max(
                        0,
                        min(
                            dataset_health["score"] / 100,
                            1
                        )
                    )
                )


                health_score_value = (
                    dataset_health["score"]
                )


                if health_score_value >= 90:

                    health_explanation = (
                        "The dataset is in excellent condition "
                        "with minimal data-quality issues. "
                        "It is generally suitable for further "
                        "analysis."
                    )

                elif health_score_value >= 75:

                    health_explanation = (
                        "The dataset is in good condition, "
                        "although some minor data-quality issues "
                        "may require attention before advanced "
                        "analysis."
                    )

                elif health_score_value >= 50:

                    health_explanation = (
                        "The dataset needs attention. One or more "
                        "data-quality issues such as missing values, "
                        "duplicates, or potential outliers should "
                        "be reviewed before advanced analysis."
                    )

                else:

                    health_explanation = (
                        "The dataset has significant data-quality "
                        "issues. Missing data, duplicates, or "
                        "potential outliers should be investigated "
                        "and handled before further analysis."
                    )


                st.markdown(
                    "#### 📝 Health Assessment"
                )


                st.info(
                    health_explanation
                )


                # =================================================
                # SCORE BREAKDOWN
                # =================================================

                st.markdown(
                    "#### 📋 Score Breakdown"
                )


                breakdown_col1, breakdown_col2, breakdown_col3 = (
                    st.columns(3)
                )


                with breakdown_col1:

                    st.metric(
                        "Missing Data Impact",
                        f"-{dataset_health['missing_penalty']}"
                    )


                with breakdown_col2:

                    st.metric(
                        "Duplicate Impact",
                        f"-{dataset_health['duplicate_penalty']}"
                    )


                with breakdown_col3:

                    st.metric(
                        "Outlier Impact",
                        f"-{dataset_health['outlier_penalty']}"
                    )


            # ====================================================
            # HEALTH RECOMMENDATIONS
            # ====================================================

            st.write(
                "### 💡 Recommended Actions"
            )


            with st.container(
                border=True
            ):

                for recommendation in (
                    dataset_health[
                        "recommendations"
                    ]
                ):

                    st.markdown(
                        f"• {recommendation}"
                    )


        # ========================================================
        # DATASET FILTERS
        # ========================================================

        st.write(
            "### Dataset Filters"
        )


        filter_columns = (
            df.columns.tolist()
        )


        if filter_columns:

            selected_filter_column = st.selectbox(
                "Select Column to Filter",
                filter_columns,
                key="filter_column"
            )


            selected_values = st.multiselect(
                "Select Values",
                df[
                    selected_filter_column
                ].dropna().unique(),
                key="filter_values"
            )


            if selected_values:

                filtered_df = filter_dataframe(
                    df,
                    selected_filter_column,
                    selected_values
                )


                st.success(
                    f"{len(filtered_df)} records found."
                )


                st.dataframe(
                    filtered_df.head(),
                    use_container_width=True
                )


    # ============================================================
    # TAB 2 - CLEANING
    # ============================================================

    with tab2:

        st.write(
            "### 🧹 Data Cleaning"
        )


        st.caption(
            "Clean the uploaded dataset and download "
            "the processed version."
        )


        # ========================================================
        # REMOVE DUPLICATES
        # ========================================================

        if st.button(
            "🗑️ Remove Duplicates",
            key="remove_duplicates_button"
        ):

            before_rows = len(df)

            try:

                cleaned_df = remove_duplicates(
                    df.copy()
                )

                if cleaned_df is None:

                    st.error(
                        "The duplicate-removal function returned no dataset."
                    )

                else:

                    st.session_state.working_df = (
                        cleaned_df.copy()
                    )

                    st.session_state.automatic_insights = None

                    st.session_state.ai_executive_summary = None

                    st.session_state.rag_fingerprint = None

                    st.session_state.rag_chunks = []

                    st.session_state.rag_embeddings = None

                    removed = (
                        before_rows
                        -
                        len(cleaned_df)
                    )

                    st.success(
                        f"✅ Duplicates removed successfully. "
                        f"{removed} duplicate record(s) removed."
                    )

                    st.rerun()

            except Exception as e:

                st.error(
                    "Duplicate removal failed."
                )

                st.exception(e)


        # ========================================================
        # FILL MISSING VALUES
        # ========================================================

        if st.button(
            "🧩 Fill Missing Values",
            key="fill_missing_values_button"
        ):

            before_missing = int(
                df.isnull().sum().sum()
            )

            try:

                cleaned_df = fill_missing_values(
                    df.copy()
                )

                if cleaned_df is None:

                    st.error(
                        "The missing-value function returned no dataset."
                    )

                else:

                    st.session_state.working_df = (
                        cleaned_df.copy()
                    )

                    st.session_state.automatic_insights = None

                    st.session_state.ai_executive_summary = None

                    st.session_state.rag_fingerprint = None

                    st.session_state.rag_chunks = []

                    st.session_state.rag_embeddings = None

                    after_missing = int(
                        cleaned_df.isnull()
                        .sum()
                        .sum()
                    )

                    filled = (
                        before_missing
                        -
                        after_missing
                    )

                    st.success(
                        f"✅ Missing values processed successfully. "
                        f"{filled} missing value(s) handled."
                    )

                    st.rerun()

            except Exception as e:

                st.error(
                    "Missing-value processing failed."
                )

                st.exception(e)


        # ========================================================
        # PROCESSED DATASET
        # ========================================================

        st.write(
            "### 📋 Processed Dataset"
        )


        st.dataframe(
            df.head(20),
            use_container_width=True
        )


        # ========================================================
        # DOWNLOAD
        # ========================================================

        csv = df.to_csv(
            index=False
        )


        st.download_button(
            label="📥 Download Processed Dataset",
            data=csv,
            file_name="processed_dataset.csv",
            mime="text/csv",
            key="download_processed_dataset"
        )


        # ========================================================
        # PDF REPORT
        # ========================================================

        st.write(
            "### 📄 Analytics Report"
        )


        st.caption(
            "Generate a comprehensive PDF report containing "
            "dataset analysis, data quality, automatic insights, "
            "dataset health, recommendations, and AI summary."
        )


        if st.button(
            "📄 Generate Complete PDF Report",
            key="generate_pdf_report"
        ):

            try:

                with st.spinner(
                    "Preparing complete analytics report..."
                ):

                    report_df = df.copy()


                    report_automatic_insights = (
                        st.session_state.get(
                            "automatic_insights",
                            None
                        )
                    )


                    if (
                        report_automatic_insights
                        is None
                    ):

                        report_outliers = (
                            detect_outliers(
                                report_df
                            )
                        )


                        report_summary = (
                            dataset_summary(
                                report_df
                            )
                        )


                        report_automatic_insights = (
                            generate_automatic_insights(
                                report_df,
                                summary=report_summary,
                                outlier_results=report_outliers
                            )
                        )


                        st.session_state.automatic_insights = (
                            report_automatic_insights
                        )


                    report_dataset_health = (
                        calculate_dataset_health(
                            report_automatic_insights
                        )
                    )


                    report_ai_summary = (
                        st.session_state.get(
                            "ai_executive_summary",
                            None
                        )
                    )


                    report_path = generate_report(
                        report_df,
                        automatic_insights=(
                            report_automatic_insights
                        ),
                        dataset_health=(
                            report_dataset_health
                        ),
                        ai_executive_summary=(
                            report_ai_summary
                        )
                    )


                st.success(
                    "✅ Complete PDF report generated successfully!"
                )


                with open(
                    report_path,
                    "rb"
                ) as file:

                    pdf_bytes = file.read()


                st.download_button(
                    label="⬇️ Download InsightGPT Report",
                    data=pdf_bytes,
                    file_name="InsightGPT_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf_report"
                )


            except Exception as e:

                st.error(
                    "❌ PDF report generation failed."
                )

                st.exception(e)


    # ============================================================
    # TAB 3 - VISUALIZATIONS
    # ============================================================

    with tab3:

        st.write(
            "### 📈 Data Visualization"
        )


        numeric_columns = (
            df.select_dtypes(
                include=["number"]
            ).columns
        )


        # ========================================================
        # HISTOGRAM
        # ========================================================

        if len(numeric_columns) > 0:

            selected_column = st.selectbox(
                "Select column for histogram",
                numeric_columns,
                key="histogram_column"
            )


            hist_fig = create_histogram(
                df,
                selected_column
            )


            st.plotly_chart(
                hist_fig,
                use_container_width=True
            )

        else:

            st.info(
                "No numerical columns available for histogram."
            )


        # ========================================================
        # SCATTER
        # ========================================================

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


            scatter_fig = create_scatter(
                df,
                x_col,
                y_col
            )


            st.plotly_chart(
                scatter_fig,
                use_container_width=True
            )


        # ========================================================
        # ADVANCED ANALYTICS
        # ========================================================

        st.write(
            "## 📊 Advanced Dataset Analytics"
        )


        # ========================================================
        # STATISTICAL SUMMARY
        # ========================================================

        st.write(
            "### 📋 Statistical Summary"
        )


        statistical_summary = (
            get_statistical_summary(
                df
            )
        )


        if statistical_summary is not None:

            st.dataframe(
                statistical_summary,
                use_container_width=True
            )

        else:

            st.info(
                "No numerical columns available "
                "for statistical analysis."
            )


        # ========================================================
        # COLUMN INSIGHTS
        # ========================================================

        st.write(
            "### 🔢 Numerical Column Insights"
        )


        column_insights = (
            get_column_insights(
                df
            )
        )


        if column_insights:

            st.dataframe(
                column_insights,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No numerical columns available."
            )


        # ========================================================
        # CORRELATION
        # ========================================================

        st.write(
            "### 🔗 Correlation Analysis"
        )


        correlation_matrix_result = (
            get_correlation_matrix(
                df
            )
        )


        if correlation_matrix_result is not None:

            st.dataframe(
                correlation_matrix_result.round(3),
                use_container_width=True
            )


            st.write(
                "#### 🔥 Strong Relationships"
            )


            strong_correlations = (
                get_strong_correlations(
                    df
                )
            )


            if strong_correlations:

                st.dataframe(
                    strong_correlations,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No strong correlations were detected."
                )

        else:

            st.info(
                "At least two numerical columns "
                "are required for correlation analysis."
            )


        # ========================================================
        # CORRELATION HEATMAP
        # ========================================================

        st.write(
            "### 🌡️ Correlation Heatmap"
        )


        if correlation_matrix_result is not None:

            heatmap_fig = px.imshow(
                correlation_matrix_result,
                text_auto=".2f",
                aspect="auto",
                title="Numerical Feature Correlation"
            )


            heatmap_fig.update_layout(
                height=600
            )


            st.plotly_chart(
                heatmap_fig,
                use_container_width=True
            )

        else:

            st.info(
                "At least two numerical columns "
                "are required to generate a correlation heatmap."
            )


        # ========================================================
        # DISTRIBUTION
        # ========================================================

        st.write(
            "### 📊 Distribution Analysis"
        )


        if len(numeric_columns) > 0:

            distribution_column = st.selectbox(
                "Select a numerical column",
                numeric_columns,
                key="distribution_column"
            )


            distribution_fig = px.histogram(
                df,
                x=distribution_column,
                marginal="box",
                title=f"Distribution of {distribution_column}",
                nbins=30
            )


            distribution_fig.update_layout(
                height=500
            )


            st.plotly_chart(
                distribution_fig,
                use_container_width=True
            )

        else:

            st.info(
                "No numerical columns available "
                "for distribution analysis."
            )


        # ========================================================
        # KEY FINDINGS
        # ========================================================

        st.write(
            "## 🧠 Key Findings"
        )


        analytical_insights = (
            generate_analytical_insights(
                df
            )
        )


        if analytical_insights:

            top_insights = (
                analytical_insights[:3]
            )


            finding_columns = st.columns(
                len(top_insights)
            )


            for i, insight in enumerate(
                top_insights
            ):

                with finding_columns[i]:

                    st.info(
                        f"📌 {insight}"
                    )


            if len(analytical_insights) > 3:

                st.write(
                    "### 📋 Additional Findings"
                )


                with st.expander(
                    "View all analytical findings"
                ):

                    for i, insight in enumerate(
                        analytical_insights[3:],
                        start=4
                    ):

                        st.markdown(
                            f"**{i}.** {insight}"
                        )

        else:

            st.info(
                "No automatic analytical insights "
                "could be generated."
            )


        # ========================================================
        # BOX PLOT
        # ========================================================

        st.write(
            "## 📦 Box Plot"
        )


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


        # ========================================================
        # CATEGORICAL COLUMNS
        # ========================================================

        categorical_columns = (
            df.select_dtypes(
                include=[
                    "object",
                    "category"
                ]
            ).columns
        )


        # ========================================================
        # BAR CHART
        # ========================================================

        st.write(
            "## 📊 Bar Chart"
        )


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


        # ========================================================
        # PIE CHART
        # ========================================================

        st.write(
            "## 🥧 Pie Chart"
        )


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


        # ========================================================
        # LINE CHART
        # ========================================================

        st.write(
            "## 📈 Line Chart"
        )


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


    # ============================================================
    # TAB 4 - AI INSIGHTS
    # ============================================================

    with tab4:

        # ========================================================
        # AI CLEANING RECOMMENDATIONS
        # ========================================================

        st.write(
            "## 🧹 AI Cleaning Recommendations"
        )


        st.caption(
            "AI analyzes missing values, duplicates, "
            "data types, and potential outliers."
        )


        if st.button(
            "✨ Generate Cleaning Recommendations",
            key="cleaning_recommendations"
        ):

            with st.spinner(
                "AI is analyzing data quality..."
            ):

                cleaning_outliers = (
                    detect_outliers(
                        df
                    )
                )


                cleaning_prompt = (
                    generate_cleaning_recommendations(
                        df,
                        summary,
                        cleaning_outliers
                    )
                )


                cleaning_response = ask_gemini(
                    cleaning_prompt
                )


            st.write(
                "### 🧠 AI Recommendations"
            )


            with st.container(
                border=True
            ):

                st.markdown(
                    _clean_ai_response(
                        cleaning_response
                    )
                )


        # ========================================================
        # ASK AI
        # ========================================================

        st.write(
            "## 🤖 Ask AI About Your Dataset"
        )


        user_question = st.text_input(
            "Enter your question about the dataset",
            key="dataset_question"
        )


        if st.button(
            "Generate AI Insight",
            key="ai_button"
        ):

            if not user_question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                # =================================================
                # QUESTION CLASSIFICATION
                # =================================================

                question_type = classify_question(
                    user_question
                )


                # =================================================
                # QUESTION INTENT
                # =================================================

                question_intent = (
                    _detect_question_intent(
                        user_question,
                        df
                    )
                )


                # =================================================
                # EXISTING GROUPWISE DETECTOR
                # =================================================

                try:

                    groupwise_info = (
                        detect_groupwise_question(
                            user_question,
                            df
                        )
                    )

                except Exception:

                    groupwise_info = {
                        "is_groupwise": False,
                        "group_column": None,
                        "value_column": None
                    }


                # =================================================
                # FALLBACK GROUPWISE DETECTOR
                # =================================================

                if not groupwise_info.get(
                    "is_groupwise",
                    False
                ):

                    fallback_groupwise = (
                        _detect_groupwise_question_fallback(
                            user_question,
                            df
                        )
                    )


                    if fallback_groupwise[
                        "is_groupwise"
                    ]:

                        groupwise_info = (
                            fallback_groupwise
                        )


                # =================================================
                # SURVIVAL DETECTION
                # =================================================

                try:

                    survival_info = (
                        detect_survival_question(
                            user_question,
                            df
                        )
                    )

                except Exception:

                    survival_info = {
                        "is_survival": False,
                        "group_column": None
                    }


                # =================================================
                # FORCE INTENT FOR DETECTED GROUPWISE QUESTION
                # =================================================

                if groupwise_info.get(
                    "is_groupwise",
                    False
                ):

                    question_intent = "groupwise"


                # =================================================
                # FORCE INTENT FOR SURVIVAL QUESTION
                # =================================================

                if survival_info.get(
                    "is_survival",
                    False
                ):

                    question_intent = "survival"


                # =================================================
                # BUILD RELEVANT STATISTICAL CONTEXT
                # =================================================

                statistical_context = (
                    _build_relevant_statistical_context(
                        user_question,
                        df,
                        groupwise_info,
                        survival_info,
                        question_intent
                    )
                )


                if not statistical_context:

                    statistical_context = (
                        "No dedicated statistical result "
                        "was generated for this question."
                    )


                # =================================================
                # QUESTION TYPE DISPLAY
                # =================================================

                if question_type == "statistical":

                    st.info(
                        "📊 Question Type: Statistical Analysis"
                    )

                elif question_type == "rag":

                    st.info(
                        "🔎 Question Type: Dataset Context / RAG"
                    )

                else:

                    st.info(
                        "🧠 Question Type: "
                        "Statistical + RAG Analysis"
                    )


                st.caption(
                    f"Detected intent: {question_intent}"
                )


                # =================================================
                # AI ANALYSIS
                # =================================================

                with st.spinner(
                    "Analyzing dataset..."
                ):

                    # =============================================
                    # RAG RETRIEVAL
                    # =============================================

                    try:

                        results = search_chunks(
                            user_question
                        )

                    except Exception:

                        results = {}


                    retrieved_documents = (
                        results.get(
                            "documents",
                            [[]]
                        )
                        if isinstance(
                            results,
                            dict
                        )
                        else [[]]
                    )


                    if (
                        retrieved_documents
                        and
                        len(
                            retrieved_documents[0]
                        ) > 0
                    ):

                        retrieved_chunks = (
                            "\n\n".join(
                                retrieved_documents[0]
                            )
                        )

                    else:

                        retrieved_chunks = (
                            "No relevant RAG context found."
                        )


                    # =============================================
                    # DATASET CONTEXT
                    # =============================================

                    try:

                        dataset_context = (
                            generate_dataset_context(
                                df
                            )
                        )

                    except Exception:

                        dataset_context = (
                            "Dataset context unavailable."
                        )


                    # =============================================
                    # LIMIT RAG CONTEXT
                    # =============================================

                    # RAG is supporting context only.
                    # It must never override computed statistics.

                    if len(
                        retrieved_chunks
                    ) > 6000:

                        retrieved_chunks = (
                            retrieved_chunks[:6000]
                            +
                            "\n[Additional RAG context omitted]"
                        )


                    # =============================================
                    # AI PROMPT
                    # =============================================

                    prompt = _build_ai_question_prompt(
                        question=user_question,
                        intent=question_intent,
                        statistical_context=statistical_context,
                        dataset_context=dataset_context,
                        rag_context=retrieved_chunks
                    )


                    # =============================================
                    # GEMINI RESPONSE
                    # =============================================

                    try:

                        response = ask_gemini(
                            prompt
                        )

                    except Exception as e:

                        response = (
                            "Unable to generate the AI response.\n\n"
                            f"Error: {e}"
                        )


                # =================================================
                # CLEAN AI RESPONSE
                # =================================================

                response = _clean_ai_response(
                    response
                )


                # =================================================
                # RAG RETRIEVAL DISPLAY
                # =================================================

                st.write(
                    "### 🔎 RAG Retrieval"
                )


                retrieved_count = (
                    len(
                        retrieved_documents[0]
                    )
                    if (
                        retrieved_documents
                        and
                        len(retrieved_documents) > 0
                    )
                    else 0
                )


                st.success(
                    f"{retrieved_count} relevant context "
                    f"chunks retrieved from ChromaDB."
                )


                with st.expander(
                    "🔍 View Retrieved Context"
                ):

                    if (
                        retrieved_documents
                        and
                        len(retrieved_documents[0]) > 0
                    ):

                        for i, chunk in enumerate(
                            retrieved_documents[0],
                            start=1
                        ):

                            st.markdown(
                                f"**Retrieved Context {i}**"
                            )


                            st.code(
                                str(chunk)[:1000],
                                language="text"
                            )

                    else:

                        st.info(
                            "No retrieved context available."
                        )


                # =================================================
                # STATISTICAL CONTEXT DISPLAY
                # =================================================

                with st.expander(
                    "📊 View Computed Statistical Result"
                ):

                    st.code(
                        statistical_context,
                        language="text"
                    )


                # =================================================
                # AI RESPONSE
                # =================================================

                st.write(
                    "### 🤖 AI Analysis"
                )


                st.caption(
                    "🧠 Generated using intelligent question "
                    "routing, statistical analysis, ChromaDB "
                    "and Gemini."
                )


                with st.container(
                    border=True
                ):

                    if response:

                        st.markdown(
                            response
                        )

                    else:

                        st.warning(
                            "No AI response was generated."
                        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "---"
)


st.markdown(
    """
### 🚀 InsightGPT Lite

AI-Powered Data Analytics and Retrieval-Augmented Query Platform

Developed by Lakshay Kundariya  
Internship Project – BCA Data Science
"""
)