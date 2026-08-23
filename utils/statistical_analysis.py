import pandas as pd


# ============================================
# GROUP-WISE NUMERICAL ANALYSIS
# ============================================

def groupwise_analysis(df, group_column, value_column):
    """
    Calculate group-wise statistics for a numerical
    column based on a categorical/group column.
    """

    if group_column not in df.columns:
        return None

    if value_column not in df.columns:
        return None

    # Make sure the value column is numerical
    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):
        return None

    result = (
        df.groupby(group_column)[value_column]
        .agg(
            ["count", "mean", "median", "min", "max"]
        )
        .round(3)
        .reset_index()
    )

    return result


# ============================================
# CATEGORY COUNTS
# ============================================

def category_counts(df, column):
    """
    Calculate the number of records in each
    category.
    """

    if column not in df.columns:
        return None

    result = (
        df[column]
        .value_counts(dropna=False)
        .reset_index()
    )

    result.columns = [
        column,
        "Count"
    ]

    return result


# ============================================
# SURVIVAL RATE BY GROUP
# ============================================

def survival_rate_by_group(df, group_column):
    """
    Calculate survival count and survival
    percentage for each group.

    Requires a 'Survived' column where:
    1 = Survived
    0 = Did not survive
    """

    if "Survived" not in df.columns:
        return None

    if group_column not in df.columns:
        return None

    # Calculate group-wise survival statistics
    result = (
        df.groupby(group_column)["Survived"]
        .agg(
            Total="count",
            Survived="sum",
            Survival_Rate="mean"
        )
        .reset_index()
    )

    # Convert survival rate to percentage
    result["Survival_Rate"] = (
        result["Survival_Rate"] * 100
    ).round(2)

    return result


# ============================================
# NUMERICAL COLUMN SUMMARY
# ============================================

def numerical_summary(df):
    """
    Generate statistical summary for all
    numerical columns.
    """

    numerical_columns = (
        df.select_dtypes(
            include="number"
        ).columns
    )

    if len(numerical_columns) == 0:
        return None

    result = (
        df[numerical_columns]
        .describe()
        .round(3)
        .T
        .reset_index()
    )

    result.rename(
        columns={
            "index": "Column"
        },
        inplace=True
    )

    return result


# ============================================
# FIND HIGHEST GROUP VALUE
# ============================================

def highest_group_average(
    df,
    group_column,
    value_column
):
    """
    Find the group with the highest average
    value.
    """

    result = groupwise_analysis(
        df,
        group_column,
        value_column
    )

    if result is None or result.empty:
        return None

    highest_row = result.loc[
        result["mean"].idxmax()
    ]

    return {
        "group": highest_row[group_column],
        "value": highest_row["mean"],
        "table": result
    }


# ============================================
# FIND LOWEST GROUP VALUE
# ============================================

def lowest_group_average(
    df,
    group_column,
    value_column
):
    """
    Find the group with the lowest average
    value.
    """

    result = groupwise_analysis(
        df,
        group_column,
        value_column
    )

    if result is None or result.empty:
        return None

    lowest_row = result.loc[
        result["mean"].idxmin()
    ]

    return {
        "group": lowest_row[group_column],
        "value": lowest_row["mean"],
        "table": result
    }