# ============================================
# AI DATASET CONTEXT GENERATOR
# ============================================


import pandas as pd


# ============================================
# BASIC DATASET INFORMATION
# ============================================


def generate_dataset_context(df):

    context = []

    # ----------------------------------------
    # Dataset Size
    # ----------------------------------------

    context.append(
        f"Dataset contains {len(df):,} rows "
        f"and {len(df.columns)} columns."
    )

    # ----------------------------------------
    # Column Information
    # ----------------------------------------

    column_information = []

    for column in df.columns:

        dtype = str(
            df[column].dtype
        )

        missing = int(
            df[column].isnull().sum()
        )

        column_information.append(
            f"{column}: type={dtype}, "
            f"missing_values={missing}"
        )

    context.append(
        "Column Information:\n"
        + "\n".join(column_information)
    )

    # ----------------------------------------
    # Missing Value Analysis
    # ----------------------------------------

    missing_values = (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )

    missing_values = missing_values[
        missing_values > 0
    ]

    if not missing_values.empty:

        context.append(
            "Missing Value Analysis:\n"
            + "\n".join(
                [
                    f"{column}: {int(count)}"
                    for column, count
                    in missing_values.items()
                ]
            )
        )

    else:

        context.append(
            "Missing Value Analysis: "
            "No missing values detected."
        )

    # ----------------------------------------
    # Duplicate Analysis
    # ----------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    context.append(
        f"Duplicate Records: "
        f"{duplicate_count}"
    )

    # ----------------------------------------
    # Numerical Statistics
    # ----------------------------------------

    numerical_df = df.select_dtypes(
        include="number"
    )

    if not numerical_df.empty:

        statistical_summary = (
            numerical_df
            .describe()
            .round(3)
            .to_string()
        )

        context.append(
            "Numerical Statistical Summary:\n"
            + statistical_summary
        )

    # ----------------------------------------
    # Correlation Analysis
    # ----------------------------------------

    if numerical_df.shape[1] >= 2:

        correlation_matrix = (
            numerical_df.corr()
            .round(3)
            .to_string()
        )

        context.append(
            "Correlation Matrix:\n"
            + correlation_matrix
        )

    # ----------------------------------------
    # Outlier Analysis using IQR
    # ----------------------------------------

    outlier_information = []

    for column in numerical_df.columns:

        series = numerical_df[column].dropna()

        if series.empty:

            continue

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )

        outliers = series[
            (series < lower_bound)
            |
            (series > upper_bound)
        ]

        outlier_count = len(
            outliers
        )

        outlier_information.append(
            f"{column}: "
            f"{outlier_count} potential outliers"
        )

    if outlier_information:

        context.append(
            "Outlier Analysis:\n"
            + "\n".join(
                outlier_information
            )
        )

    # ----------------------------------------
    # Return Context
    # ----------------------------------------

    return "\n\n".join(context)