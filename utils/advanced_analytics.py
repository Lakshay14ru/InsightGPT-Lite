# ============================================
# ADVANCED DATASET ANALYTICS
# ============================================


def get_statistical_summary(df):

    numerical_df = df.select_dtypes(
        include="number"
    )

    if numerical_df.empty:

        return None

    summary = numerical_df.describe().T

    summary["Missing"] = numerical_df.isnull().sum()

    summary["Missing %"] = (
        numerical_df.isnull().mean() * 100
    ).round(2)

    return summary


# ============================================
# CORRELATION ANALYSIS
# ============================================


def get_correlation_matrix(df):

    numerical_df = df.select_dtypes(
        include="number"
    )

    if numerical_df.shape[1] < 2:

        return None

    return numerical_df.corr()


# ============================================
# STRONGEST CORRELATIONS
# ============================================


def get_strong_correlations(df, threshold=0.5):

    correlation_matrix = get_correlation_matrix(df)

    if correlation_matrix is None:

        return []

    correlations = []

    columns = correlation_matrix.columns

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            column_1 = columns[i]

            column_2 = columns[j]

            correlation = correlation_matrix.loc[
                column_1,
                column_2
            ]

            if abs(correlation) >= threshold:

                correlations.append({

                    "Column 1": column_1,

                    "Column 2": column_2,

                    "Correlation": round(
                        correlation,
                        3
                    )

                })

    correlations.sort(
        key=lambda x: abs(
            x["Correlation"]
        ),
        reverse=True
    )

    return correlations


# ============================================
# NUMERICAL COLUMN INSIGHTS
# ============================================


def get_column_insights(df):

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    insights = []

    for column in numerical_columns:

        series = df[column].dropna()

        if series.empty:

            continue

        insights.append({

            "Column": column,

            "Mean": round(
                series.mean(),
                2
            ),

            "Median": round(
                series.median(),
                2
            ),

            "Minimum": round(
                series.min(),
                2
            ),

            "Maximum": round(
                series.max(),
                2
            ),

            "Standard Deviation": round(
                series.std(),
                2
            )

        })

    return insights

# ============================================
# AUTOMATIC ANALYTICAL INSIGHTS
# ============================================


def generate_analytical_insights(df):

    insights = []

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    # ============================================
    # DATASET OVERVIEW
    # ============================================

    total_rows = len(df)
    total_columns = len(df.columns)

    if total_rows > 0:

        insights.append(
            f"The dataset contains {total_rows:,} "
            f"records across {total_columns} columns."
        )

    # ============================================
    # MISSING VALUE ANALYSIS
    # ============================================

    missing_values = df.isnull().sum()

    total_missing = int(
        missing_values.sum()
    )

    if total_missing == 0:

        insights.append(
            "No missing values were detected "
            "in the dataset."
        )

    else:

        missing_columns = missing_values[
            missing_values > 0
        ].sort_values(
            ascending=False
        )

        highest_missing_column = (
            missing_columns.index[0]
        )

        highest_missing_count = int(
            missing_columns.iloc[0]
        )

        missing_percentage = round(
            (
                highest_missing_count /
                total_rows
            ) * 100,
            2
        )

        insights.append(
            f"'{highest_missing_column}' contains "
            f"{highest_missing_count:,} missing values "
            f"({missing_percentage}% of its records)."
        )

    # ============================================
    # DUPLICATE ANALYSIS
    # ============================================

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count == 0:

        insights.append(
            "No duplicate records were detected."
        )

    else:

        duplicate_percentage = round(
            (
                duplicate_count /
                total_rows
            ) * 100,
            2
        )

        insights.append(
            f"{duplicate_count:,} duplicate records "
            f"were detected "
            f"({duplicate_percentage}% of the dataset)."
        )

    # ============================================
    # NUMERICAL COLUMN ANALYSIS
    # ============================================

    for column in numerical_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        mean_value = series.mean()
        median_value = series.median()
        minimum_value = series.min()
        maximum_value = series.max()
        standard_deviation = series.std()

        # ----------------------------------------
        # Mean vs Median / Skewness
        # ----------------------------------------

        if mean_value > median_value * 1.15:

            insights.append(
                f"'{column}' appears to be "
                f"right-skewed because its mean "
                f"({mean_value:.2f}) is noticeably "
                f"higher than its median "
                f"({median_value:.2f})."
            )

        elif (
            median_value > 0
            and mean_value < median_value * 0.85
        ):

            insights.append(
                f"'{column}' appears to be "
                f"left-skewed because its median "
                f"({median_value:.2f}) is noticeably "
                f"higher than its mean "
                f"({mean_value:.2f})."
            )

        # ----------------------------------------
        # High Variability
        # ----------------------------------------

        if mean_value != 0:

            coefficient_of_variation = (
                abs(standard_deviation / mean_value)
            )

            if coefficient_of_variation > 1:

                insights.append(
                    f"'{column}' shows high variability "
                    f"relative to its mean."
                )

        # ----------------------------------------
        # Range
        # ----------------------------------------

        if minimum_value != maximum_value:

            insights.append(
                f"'{column}' ranges from "
                f"{minimum_value:.2f} to "
                f"{maximum_value:.2f}."
            )

    # ============================================
    # CORRELATION ANALYSIS
    # ============================================

    strong_correlations = (
        get_strong_correlations(df)
    )

    if strong_correlations:

        strongest = strong_correlations[0]

        column_1 = strongest["Column 1"]
        column_2 = strongest["Column 2"]
        correlation = strongest["Correlation"]

        if correlation >= 0:

            relationship = "positive"

        else:

            relationship = "negative"

        strength = abs(correlation)

        if strength >= 0.8:

            strength_text = "very strong"

        elif strength >= 0.6:

            strength_text = "strong"

        else:

            strength_text = "moderate"

        insights.append(
            f"'{column_1}' and '{column_2}' "
            f"show a {strength_text} "
            f"{relationship} correlation "
            f"({correlation:.3f})."
        )

    else:

        insights.append(
            "No strong correlations were detected "
            "between numerical variables."
        )

    # ============================================
    # MOST VARIABLE NUMERICAL COLUMN
    # ============================================

    if len(numerical_columns) > 0:

        standard_deviations = (
            df[numerical_columns]
            .std()
            .dropna()
        )

        if not standard_deviations.empty:

            highest_variability_column = (
                standard_deviations.idxmax()
            )

            highest_std = (
                standard_deviations.max()
            )

            insights.append(
                f"'{highest_variability_column}' "
                f"has the highest standard deviation "
                f"({highest_std:.2f}) among the "
                f"numerical columns."
            )

    # ============================================
    # FINAL DATASET MESSAGE
    # ============================================

    if len(numerical_columns) == 0:

        insights.append(
            "The dataset does not contain numerical "
            "columns, so advanced numerical analysis "
            "is limited."
        )

    else:

        insights.append(
            f"The dataset contains "
            f"{len(numerical_columns)} numerical "
            f"columns available for statistical "
            f"analysis."
        )

    return insights