import pandas as pd

def dataset_summary(df):

    summary = {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Records": int(df.duplicated().sum()),

        "Numerical Columns": len(
            df.select_dtypes(include="number").columns
        ),

        "Categorical Columns": len(
            df.select_dtypes(include="object").columns
        ),

        "Memory Usage (KB)": round(
            df.memory_usage(deep=True).sum() / 1024,
            2
        )

    }

    return summary


def dataset_health_score(df):

    total_cells = df.shape[0] * df.shape[1]

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    missing_penalty = (missing / total_cells) * 100

    duplicate_penalty = (duplicates / len(df)) * 100

    score = 100 - missing_penalty - duplicate_penalty

    score = max(0, round(score, 2))

    return score

def advanced_eda(df):

    eda = {}

    eda["Unique Values"] = df.nunique()

    eda["Missing Percentage"] = (
        df.isnull().sum() / len(df) * 100
    ).round(2)

    eda["Data Types"] = df.dtypes.astype(str)

    return eda

def detect_outliers(df):

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    outlier_results = {}

    for column in numerical_columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ]

        outlier_count = len(outliers)

        outlier_percentage = (
            outlier_count / len(df) * 100
        )

        outlier_results[column] = {
            "Q1": round(Q1, 2),
            "Q3": round(Q3, 2),
            "IQR": round(IQR, 2),
            "Outliers": outlier_count,
            "Outlier Percentage": round(
                outlier_percentage,
                2
            )
        }

    return outlier_results

def correlation_matrix(df):

    numerical_data = df.select_dtypes(
        include="number"
    )

    if numerical_data.shape[1] < 2:
        return None

    correlation = numerical_data.corr()

    return correlation

def generate_eda_summary(df, summary, health_score, outlier_results):

    rows = summary["Rows"]
    columns = summary["Columns"]
    missing_values = summary["Missing Values"]
    duplicates = summary["Duplicate Records"]
    numerical_columns = summary["Numerical Columns"]
    categorical_columns = summary["Categorical Columns"]

    summary_text = (
        f"The dataset contains {rows} rows and "
        f"{columns} columns. "
    )

    # Missing values
    if missing_values > 0:

        missing_columns = df.isnull().sum()

        missing_columns = missing_columns[
            missing_columns > 0
        ].sort_values(
            ascending=False
        )

        top_missing_column = missing_columns.index[0]

        summary_text += (
            f"It contains {missing_values} missing values "
            f"across {len(missing_columns)} columns. "
            f"The '{top_missing_column}' column has the highest "
            f"number of missing values. "
        )

    else:

        summary_text += (
            "The dataset does not contain missing values. "
        )

    # Duplicates
    if duplicates > 0:

        summary_text += (
            f"There are {duplicates} duplicate records "
            f"that should be removed. "
        )

    else:

        summary_text += (
            "No duplicate records were detected. "
        )

    # Data types
    summary_text += (
        f"The dataset contains {numerical_columns} numerical "
        f"columns and {categorical_columns} categorical columns. "
    )

    # Outliers
    outlier_columns = []

    for column, result in outlier_results.items():

        if result["Outliers"] > 0:

            outlier_columns.append(column)

    if outlier_columns:

        displayed_columns = ", ".join(
            outlier_columns[:3]
        )

        summary_text += (
            f"Potential outliers were detected in "
            f"{displayed_columns}. "
        )

    else:

        summary_text += (
            "No significant outliers were detected "
            "using the IQR method. "
        )

    # Health score
    summary_text += (
        f"Overall, the dataset has a health score of "
        f"{health_score}%. "
    )

    if health_score >= 90:

        summary_text += (
            "The dataset is in excellent condition "
            "and is ready for analysis."
        )

    elif health_score >= 75:

        summary_text += (
            "The dataset is generally suitable for analysis "
            "after addressing the identified data quality issues."
        )

    else:

        summary_text += (
            "The dataset requires significant cleaning "
            "before reliable analysis."
        )

    return summary_text