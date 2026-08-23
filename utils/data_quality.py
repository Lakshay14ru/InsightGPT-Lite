# ============================================
# DATA QUALITY ANALYSIS
# ============================================


def calculate_data_quality(df, outlier_results=None):

    total_rows = len(df)

    # --------------------------------------------
    # Missing Values
    # --------------------------------------------

    missing_values = int(
        df.isnull().sum().sum()
    )

    if total_rows > 0 and missing_values > 0:

        missing_percentage = (
            missing_values /
            (total_rows * len(df.columns))
        ) * 100

    else:

        missing_percentage = 0

    # --------------------------------------------
    # Duplicate Records
    # --------------------------------------------

    duplicate_records = int(
        df.duplicated().sum()
    )

    if total_rows > 0:

        duplicate_percentage = (
            duplicate_records /
            total_rows
        ) * 100

    else:

        duplicate_percentage = 0

    # --------------------------------------------
    # Determine Missing Value Severity
    # --------------------------------------------

    if missing_percentage == 0:

        missing_status = "Good"
        missing_severity = "🟢 Low"

    elif missing_percentage < 5:

        missing_status = "Minor Missing Data"
        missing_severity = "🟢 Low"

    elif missing_percentage < 20:

        missing_status = "Moderate Missing Data"
        missing_severity = "🟠 Medium"

    else:

        missing_status = "High Missing Data"
        missing_severity = "🔴 High"

    # --------------------------------------------
    # Determine Duplicate Severity
    # --------------------------------------------

    if duplicate_percentage == 0:

        duplicate_status = "No Duplicates"
        duplicate_severity = "🟢 Low"

    elif duplicate_percentage < 5:

        duplicate_status = "Few Duplicates"
        duplicate_severity = "🟢 Low"

    elif duplicate_percentage < 20:

        duplicate_status = "Moderate Duplicates"
        duplicate_severity = "🟠 Medium"

    else:

        duplicate_status = "High Duplicates"
        duplicate_severity = "🔴 High"

    # --------------------------------------------
    # Data Type Analysis
    # --------------------------------------------

    numerical_columns = len(
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_columns = len(
        df.select_dtypes(
            include=["object", "category"]
        ).columns
    )

    # --------------------------------------------
    # Outlier Analysis
    # --------------------------------------------

    if outlier_results is None:

        outlier_results = {}

    total_outliers = 0

    for column, result in outlier_results.items():

        total_outliers += result.get(
            "Outliers",
            0
        )

    if total_rows > 0:

        outlier_percentage = (
            total_outliers /
            total_rows
        ) * 100

    else:

        outlier_percentage = 0

    # --------------------------------------------
    # Determine Outlier Severity
    # --------------------------------------------

    if total_outliers == 0:

        outlier_status = "No Significant Outliers"
        outlier_severity = "🟢 Low"

    elif outlier_percentage < 5:

        outlier_status = "Few Potential Outliers"
        outlier_severity = "🟢 Low"

    elif outlier_percentage < 15:

        outlier_status = "Moderate Potential Outliers"
        outlier_severity = "🟠 Medium"

    else:

        outlier_status = "High Potential Outliers"
        outlier_severity = "🔴 High"

    # --------------------------------------------
    # Overall Quality Score
    # --------------------------------------------

    score = 100

    # Missing-value penalty
    score -= min(
        missing_percentage,
        40
    )

    # Duplicate penalty
    score -= min(
        duplicate_percentage,
        25
    )

    # Outlier penalty
    score -= min(
        outlier_percentage,
        20
    )

    score = max(
        0,
        round(score)
    )

    # --------------------------------------------
    # Overall Status
    # --------------------------------------------

    if score >= 90:

        overall_status = "🟢 Excellent"

    elif score >= 75:

        overall_status = "🟢 Good"

    elif score >= 50:

        overall_status = "🟠 Needs Attention"

    else:

        overall_status = "🔴 Poor"

    # --------------------------------------------
    # Return Data Quality Results
    # --------------------------------------------

    return {

        "quality_score": score,

        "overall_status": overall_status,

        # Missing values
        "missing_values": missing_values,

        "missing_percentage": round(
            missing_percentage,
            2
        ),

        "missing_status": missing_status,

        "missing_severity": missing_severity,

        # Duplicate records
        "duplicate_records": duplicate_records,

        "duplicate_percentage": round(
            duplicate_percentage,
            2
        ),

        "duplicate_status": duplicate_status,

        "duplicate_severity": duplicate_severity,

        # Outliers
        "total_outliers": total_outliers,

        "outlier_percentage": round(
            outlier_percentage,
            2
        ),

        "outlier_status": outlier_status,

        "outlier_severity": outlier_severity,

        # Data types
        "numerical_columns": numerical_columns,

        "categorical_columns": categorical_columns

    }