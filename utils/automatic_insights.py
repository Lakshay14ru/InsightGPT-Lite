import pandas as pd


def generate_automatic_insights(
    df,
    summary=None,
    outlier_results=None
):
    """
    Generate structured automatic analytical
    insights from the uploaded dataset.
    """

    # ============================================
    # BASIC DATASET INFORMATION
    # ============================================

    rows = len(df)
    columns = len(df.columns)

    dataset_insights = {
        "rows": rows,
        "columns": columns,
        "message": (
            f"The dataset contains {rows:,} rows "
            f"and {columns} columns."
        )
    }

    # ============================================
    # DATA QUALITY
    # ============================================

    missing = df.isnull().sum()

    missing_columns = (
        missing[missing > 0]
        .sort_values(ascending=False)
    )

    if not missing_columns.empty:

        missing_column = (
            missing_columns.index[0]
        )

        missing_count = int(
            missing_columns.iloc[0]
        )

        missing_percentage = round(
            (missing_count / rows) * 100,
            2
        )

        missing_message = (
            f"The column with the most missing "
            f"values is '{missing_column}', "
            f"with {missing_count:,} missing "
            f"values ({missing_percentage}%)."
        )

    else:

        missing_column = None
        missing_count = 0
        missing_percentage = 0

        missing_message = (
            "The dataset contains no missing values."
        )

    duplicates = int(
        df.duplicated().sum()
    )

    if duplicates > 0:

        duplicate_message = (
            f"The dataset contains "
            f"{duplicates:,} duplicate records."
        )

    else:

        duplicate_message = (
            "No duplicate records were detected."
        )

    data_quality = {
        "missing_column": missing_column,
        "missing_count": missing_count,
        "missing_percentage": missing_percentage,
        "missing_message": missing_message,
        "duplicates": duplicates,
        "duplicate_message": duplicate_message
    }

    # ============================================
    # NUMERICAL / CATEGORICAL COLUMNS
    # ============================================

    numerical_columns = (
        df.select_dtypes(
            include="number"
        ).columns.tolist()
    )

    categorical_columns = (
        df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
    )

    column_analysis = {
        "numerical_count": len(
            numerical_columns
        ),
        "categorical_count": len(
            categorical_columns
        ),
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns
    }

    # ============================================
    # OUTLIER ANALYSIS
    # ============================================

    outlier_column = None
    highest_outliers = 0

    if outlier_results:

        for column, result in (
            outlier_results.items()
        ):

            outlier_count = int(
                result.get(
                    "Outliers",
                    0
                )
            )

            if outlier_count > highest_outliers:

                highest_outliers = outlier_count
                outlier_column = column

    if outlier_column is not None:

        outlier_message = (
            f"The column with the highest "
            f"number of potential outliers is "
            f"'{outlier_column}', with "
            f"{highest_outliers:,} detected "
            f"outliers."
        )

    else:

        outlier_message = (
            "No potential outliers were detected."
        )

    outlier_analysis = {
        "column": outlier_column,
        "count": highest_outliers,
        "message": outlier_message
    }

    # ============================================
    # CORRELATION ANALYSIS
    # ============================================

    strongest_correlation = None

    if len(numerical_columns) >= 2:

        correlation_matrix = (
            df[numerical_columns].corr()
        )

        correlation_pairs = []

        for i in range(
            len(correlation_matrix.columns)
        ):

            for j in range(
                i + 1,
                len(correlation_matrix.columns)
            ):

                column_a = (
                    correlation_matrix.columns[i]
                )

                column_b = (
                    correlation_matrix.columns[j]
                )

                correlation_value = (
                    correlation_matrix.iloc[
                        i,
                        j
                    ]
                )

                if pd.notna(
                    correlation_value
                ):

                    correlation_pairs.append(
                        (
                            abs(
                                correlation_value
                            ),
                            column_a,
                            column_b,
                            correlation_value
                        )
                    )

        if correlation_pairs:

            correlation_pairs.sort(
                reverse=True
            )

            (
                _,
                column_a,
                column_b,
                correlation_value
            ) = correlation_pairs[0]

            strongest_correlation = {
                "column_a": column_a,
                "column_b": column_b,
                "value": round(
                    correlation_value,
                    3
                ),
                "message": (
                    f"The strongest numerical "
                    f"relationship is between "
                    f"'{column_a}' and "
                    f"'{column_b}', with a "
                    f"correlation coefficient "
                    f"of {correlation_value:.3f}."
                )
            }

    if strongest_correlation is None:

        strongest_correlation = {
            "column_a": None,
            "column_b": None,
            "value": None,
            "message": (
                "Correlation analysis requires "
                "at least two numerical columns."
            )
        }

    # ============================================
    # FINAL STRUCTURED RESULT
    # ============================================

    return {
        "dataset": dataset_insights,
        "data_quality": data_quality,
        "columns": column_analysis,
        "outliers": outlier_analysis,
        "correlation": strongest_correlation
    }

def generate_ai_executive_summary(
    df,
    automatic_insights,
    ask_gemini
):
    """
    Generate a professional AI executive summary
    using already-computed statistical insights.
    """

    dataset_info = automatic_insights["dataset"]

    quality_info = automatic_insights["data_quality"]

    column_info = automatic_insights["columns"]

    outlier_info = automatic_insights["outliers"]

    correlation_info = automatic_insights["correlation"]

    prompt = f"""
You are an expert data analytics assistant.

Create a professional executive summary of the
uploaded dataset using ONLY the computed
statistics provided below.

============================================
DATASET OVERVIEW
============================================

Rows: {dataset_info["rows"]}
Columns: {dataset_info["columns"]}

============================================
DATA QUALITY
============================================

Missing Values:
{quality_info["missing_count"]}

Most Affected Column:
{quality_info["missing_column"]}

Missing Percentage:
{quality_info["missing_percentage"]}%

Duplicate Records:
{quality_info["duplicates"]}

============================================
COLUMN ANALYSIS
============================================

Numerical Columns:
{column_info["numerical_count"]}

Categorical Columns:
{column_info["categorical_count"]}

============================================
OUTLIER ANALYSIS
============================================

Column with Most Potential Outliers:
{outlier_info["column"]}

Potential Outliers:
{outlier_info["count"]}

============================================
CORRELATION ANALYSIS
============================================

Column 1:
{correlation_info["column_a"]}

Column 2:
{correlation_info["column_b"]}

Correlation:
{correlation_info["value"]}

============================================
INSTRUCTIONS
============================================

1. Summarize the most important findings.

2. Mention important data-quality issues.

3. Mention the most significant outlier finding.

4. Mention the strongest correlation when
   available.

5. Do not invent statistics.

6. Do not calculate new statistics.

7. Do not make causal claims.

8. Do not discuss information that is not
   provided above.

9. Keep the summary concise and professional.

10. Write for a data analytics dashboard.

============================================
RESPONSE FORMAT
============================================

### 🧠 Executive Summary

Write 1 concise professional paragraph.

### 🔎 Key Observations

Provide 3–5 important observations as bullets.

### 💡 Recommended Attention

Provide 1–3 practical areas that should be
investigated further.

Do not mention these instructions.
"""

    response = ask_gemini(prompt)

    return response

def calculate_dataset_health(automatic_insights):
    """
    Calculate an overall dataset health score
    and generate actionable recommendations.
    """

    quality_info = automatic_insights[
        "data_quality"
    ]

    outlier_info = automatic_insights[
        "outliers"
    ]

    # ============================================
    # START WITH PERFECT SCORE
    # ============================================

    score = 100

    # ============================================
    # MISSING DATA PENALTY
    # ============================================

    missing_percentage = quality_info[
        "missing_percentage"
    ]

    if missing_percentage <= 5:

        missing_penalty = 5

    elif missing_percentage <= 20:

        missing_penalty = 15

    elif missing_percentage <= 40:

        missing_penalty = 25

    else:

        missing_penalty = 35

    score -= missing_penalty

    # ============================================
    # DUPLICATE PENALTY
    # ============================================

    duplicates = quality_info[
        "duplicates"
    ]

    total_rows = automatic_insights[
        "dataset"
    ]["rows"]

    if total_rows > 0:

        duplicate_percentage = (
            duplicates / total_rows
        ) * 100

    else:

        duplicate_percentage = 0

    if duplicate_percentage == 0:

        duplicate_penalty = 0

    elif duplicate_percentage <= 5:

        duplicate_penalty = 5

    elif duplicate_percentage <= 20:

        duplicate_penalty = 10

    else:

        duplicate_penalty = 20

    score -= duplicate_penalty

    # ============================================
    # OUTLIER PENALTY
    # ============================================

    outlier_count = outlier_info[
        "count"
    ]

    if outlier_count == 0:

        outlier_penalty = 0

    elif outlier_count <= 10:

        outlier_penalty = 5

    elif outlier_count <= 50:

        outlier_penalty = 10

    elif outlier_count <= 100:

        outlier_penalty = 15

    else:

        outlier_penalty = 20

    score -= outlier_penalty

    # ============================================
    # KEEP SCORE BETWEEN 0 AND 100
    # ============================================

    score = max(
        0,
        min(
            100,
            round(score)
        )
    )

    # ============================================
    # DETERMINE HEALTH STATUS
    # ============================================

    if score >= 90:

        status = "🟢 Excellent"

    elif score >= 75:

        status = "🟢 Good"

    elif score >= 50:

        status = "🟠 Needs Attention"

    else:

        status = "🔴 Poor"

    # ============================================
    # GENERATE RECOMMENDATIONS
    # ============================================

    recommendations = []

    # Missing data recommendation

    if missing_percentage > 5:

        if quality_info[
            "missing_column"
        ]:

            recommendations.append(
                f"Review missing values in "
                f"'{quality_info['missing_column']}' "
                f"and determine an appropriate "
                f"imputation or removal strategy."
            )

        else:

            recommendations.append(
                "Review the missing values and "
                "apply an appropriate handling strategy."
            )

    # Duplicate recommendation

    if duplicates > 0:

        recommendations.append(
            f"Review and remove {duplicates:,} "
            f"duplicate record(s) if they do not "
            f"represent valid repeated observations."
        )

    # Outlier recommendation

    if outlier_count > 0:

        recommendations.append(
            f"Investigate potential outliers in "
            f"'{outlier_info['column']}' before "
            f"performing advanced statistical or "
            f"machine-learning analysis."
        )

    # Correlation recommendation

    correlation_info = automatic_insights[
        "correlation"
    ]

    if (
        correlation_info["column_a"]
        and correlation_info["column_b"]
    ):

        recommendations.append(
            f"Further investigate the relationship "
            f"between '{correlation_info['column_a']}' "
            f"and '{correlation_info['column_b']}'."
        )

    # No major issues

    if not recommendations:

        recommendations.append(
            "No major data-quality issues were "
            "identified by the current automated checks."
        )

    # ============================================
    # RETURN RESULT
    # ============================================

    return {
        "score": score,
        "status": status,
        "missing_penalty": missing_penalty,
        "duplicate_penalty": duplicate_penalty,
        "outlier_penalty": outlier_penalty,
        "recommendations": recommendations
    }