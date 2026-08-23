# ============================================
# AI CLEANING RECOMMENDATIONS
# ============================================

def generate_cleaning_recommendations(
    df,
    dataset_summary,
    outlier_results
):

    missing_values = df.isnull().sum()

    missing_info = ""

    for column, count in missing_values.items():

        if count > 0:

            percentage = (
                count / len(df)
            ) * 100

            missing_info += (
                f"{column}: "
                f"{count} missing values "
                f"({percentage:.2f}%)\n"
            )

    if missing_info == "":

        missing_info = (
            "No missing values detected."
        )

    duplicate_count = int(
        df.duplicated().sum()
    )

    outlier_info = ""

    for column, result in outlier_results.items():

        if result["Outliers"] > 0:

            outlier_info += (
                f"{column}: "
                f"{result['Outliers']} potential "
                f"outliers detected\n"
            )

    if outlier_info == "":

        outlier_info = (
            "No potential outliers detected."
        )

    column_types = ""

    for column in df.columns:

        column_types += (
            f"{column}: "
            f"{df[column].dtype}\n"
        )

    prompt = f"""
You are an expert Data Science data-cleaning assistant.

Analyze the uploaded dataset's data-quality information
and provide practical cleaning recommendations.

DATASET INFORMATION

Rows:
{dataset_summary["Rows"]}

Columns:
{dataset_summary["Columns"]}

MISSING VALUES

{missing_info}

DUPLICATE RECORDS

{duplicate_count}

COLUMN DATA TYPES

{column_types}

POTENTIAL OUTLIERS

{outlier_info}

Provide the recommendations using this structure:

## 🧹 Data Cleaning Recommendations

### 1. Missing Values
Identify important columns with missing values
and explain an appropriate treatment.

### 2. Duplicate Records
Explain whether duplicate records need attention.

### 3. Outliers
Identify columns containing potential outliers
and explain whether they should be investigated,
removed, capped, or retained.

### 4. Data Types
Identify any columns whose data type may need
conversion or correction.

### 5. Recommended Cleaning Order
Provide a short step-by-step order for cleaning
the dataset.

Important rules:

- Do not invent missing-value counts.
- Do not invent column names.
- Use the provided statistics.
- Do not automatically recommend deleting valid
  data without explaining the reason.
- Distinguish between a recommendation and an
  action that has actually been performed.
- Keep the recommendations practical and suitable
  for a Data Science project.
"""

    return prompt