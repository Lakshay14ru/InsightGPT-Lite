# ============================================
# AI DATASET SUMMARY
# ============================================

def generate_ai_dataset_summary(
    df,
    dataset_summary,
    eda_summary
):

    dataset_preview = df.head(20).to_string(
        index=False
    )

    prompt = f"""
You are an expert Data Science assistant.

Analyze the following dataset and provide a
professional dataset summary.

DATASET STATISTICS:

Rows:
{dataset_summary["Rows"]}

Columns:
{dataset_summary["Columns"]}

Missing Values:
{dataset_summary["Missing Values"]}

Duplicate Records:
{dataset_summary["Duplicate Records"]}

Numerical Columns:
{dataset_summary["Numerical Columns"]}

Categorical Columns:
{dataset_summary["Categorical Columns"]}

AUTOMATED EDA SUMMARY:

{eda_summary}

DATASET PREVIEW:

{dataset_preview}

Provide the response using the following structure:

1. Dataset Overview
2. Key Observations
3. Data Quality Issues
4. Recommended Actions

Keep the explanation clear, professional,
and suitable for a Data Science analytics
application.

Do not invent information that is not supported
by the provided dataset information.
"""

    return prompt