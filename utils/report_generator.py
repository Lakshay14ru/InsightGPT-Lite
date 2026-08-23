from fpdf import FPDF
from datetime import datetime
import os
import re


class InsightGPTPDF(FPDF):

    def header(self):

        if self.page_no() > 1:

            self.set_font(
                "Arial",
                "B",
                9
            )

            self.cell(
                0,
                8,
                "InsightGPT Lite | Analytics Report",
                align="R",
                ln=True
            )

            self.ln(2)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Arial",
            size=8
        )

        self.cell(
            0,
            10,
            f"InsightGPT Lite | Page {self.page_no()}",
            align="C"
        )


def generate_report(
    df,
    automatic_insights=None,
    dataset_health=None,
    ai_executive_summary=None
):

    pdf = InsightGPTPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=18
    )

    pdf.add_page()

    # ============================================
    # HELPER FUNCTIONS
    # ============================================

    def clean_text(text):

        if text is None:
            return ""

        text = str(text)

        # Remove unsupported Unicode characters
        # because the default Arial font in FPDF
        # uses Latin-1 encoding.
        cleaned_text = ""

        for char in text:

            try:
                char.encode("latin-1")
                cleaned_text += char

            except UnicodeEncodeError:
                cleaned_text += " "

        return cleaned_text

    def add_heading(number, title):

        pdf.ln(4)

        pdf.set_font(
            "Arial",
            "B",
            14
        )

        pdf.cell(
            0,
            9,
            f"{number}. {clean_text(title)}",
            ln=True
        )

        pdf.ln(2)

    def add_subheading(title):

        pdf.set_font(
            "Arial",
            "B",
            11
        )

        pdf.cell(
            0,
            8,
            clean_text(title),
            ln=True
        )

    def add_text(text):

        text = clean_text(text)

        if not text.strip():
            return

        pdf.set_font(
            "Arial",
            size=10
        )

        pdf.multi_cell(
            0,
            6,
            text
        )

        pdf.ln(1)

    def add_bullet(text):

        text = clean_text(text)

        if not text.strip():
            return

        pdf.set_font(
            "Arial",
            size=10
        )

        pdf.multi_cell(
            0,
            6,
            "- " + text
        )

        pdf.ln(1)

    def add_ai_summary(text):

        """
        Converts Gemini/Markdown-style AI output
        into clean PDF formatting.
        """

        if not text:
            return

        text = str(text)

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        lines = text.split("\n")

        for raw_line in lines:

            line = raw_line.strip()

            if not line:
                pdf.ln(2)
                continue

            # ------------------------------------
            # Remove unsupported Unicode
            # ------------------------------------

            line = clean_text(line)

            # ------------------------------------
            # Markdown headings
            # ------------------------------------

            if line.startswith("### "):

                heading = line[4:].strip()

                # Remove markdown bold
                heading = heading.replace("**", "")

                pdf.ln(2)

                pdf.set_font(
                    "Arial",
                    "B",
                    11
                )

                pdf.multi_cell(
                    0,
                    7,
                    heading
                )

                pdf.ln(1)

                continue

            if line.startswith("## "):

                heading = line[3:].strip()

                heading = heading.replace("**", "")

                pdf.ln(2)

                pdf.set_font(
                    "Arial",
                    "B",
                    11
                )

                pdf.multi_cell(
                    0,
                    7,
                    heading
                )

                pdf.ln(1)

                continue

            if line.startswith("# "):

                heading = line[2:].strip()

                heading = heading.replace("**", "")

                pdf.ln(2)

                pdf.set_font(
                    "Arial",
                    "B",
                    12
                )

                pdf.multi_cell(
                    0,
                    7,
                    heading
                )

                pdf.ln(1)

                continue

            # ------------------------------------
            # Markdown bullet points
            # ------------------------------------

            if line.startswith("- "):

                bullet = line[2:].strip()

                bullet = bullet.replace(
                    "**",
                    ""
                )

                add_bullet(
                    bullet
                )

                continue

            if line.startswith("* "):

                bullet = line[2:].strip()

                bullet = bullet.replace(
                    "**",
                    ""
                )

                add_bullet(
                    bullet
                )

                continue

            # ------------------------------------
            # Numbered lists
            # ------------------------------------

            if re.match(
                r"^\d+\.\s+",
                line
            ):

                numbered_text = re.sub(
                    r"^\d+\.\s+",
                    "",
                    line
                )

                numbered_text = (
                    numbered_text
                    .replace("**", "")
                )

                pdf.set_font(
                    "Arial",
                    size=10
                )

                pdf.multi_cell(
                    0,
                    6,
                    "- " + numbered_text
                )

                pdf.ln(1)

                continue

            # ------------------------------------
            # Remove bold markdown
            # ------------------------------------

            line = line.replace(
                "**",
                ""
            )

            # ------------------------------------
            # Remove inline code markdown
            # ------------------------------------

            line = line.replace(
                "`",
                ""
            )

            # ------------------------------------
            # Normal paragraph
            # ------------------------------------

            pdf.set_font(
                "Arial",
                size=10
            )

            pdf.multi_cell(
                0,
                6,
                line
            )

            pdf.ln(1)

    # ============================================
    # COVER / TITLE
    # ============================================

    pdf.ln(18)

    pdf.set_font(
        "Arial",
        "B",
        22
    )

    pdf.cell(
        0,
        12,
        "InsightGPT Lite",
        align="C",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        0,
        10,
        "Analytics Report",
        align="C",
        ln=True
    )

    pdf.ln(8)

    pdf.set_font(
        "Arial",
        size=11
    )

    pdf.multi_cell(
        0,
        7,
        "AI-Powered Data Analytics and "
        "Retrieval-Augmented Query Platform",
        align="C"
    )

    pdf.ln(18)

    pdf.set_font(
        "Arial",
        "B",
        11
    )

    pdf.cell(
        0,
        8,
        "Internship Project - BCA Data Science",
        align="C",
        ln=True
    )

    pdf.set_font(
        "Arial",
        size=10
    )

    pdf.cell(
        0,
        7,
        "Developed by Lakshay Kundariya",
        align="C",
        ln=True
    )

    pdf.ln(15)

    pdf.set_font(
        "Arial",
        size=9
    )

    generated_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    pdf.cell(
        0,
        7,
        f"Report Generated: {generated_time}",
        align="C",
        ln=True
    )

    pdf.add_page()

    # ============================================
    # 1. PROJECT INFORMATION
    # ============================================

    add_heading(
        1,
        "Project Information"
    )

    add_text(
        "InsightGPT Lite is an AI-powered "
        "data analytics and retrieval-augmented "
        "query platform designed to analyze "
        "uploaded datasets and generate "
        "actionable insights."
    )

    # ============================================
    # 2. DATASET OVERVIEW
    # ============================================

    add_heading(
        2,
        "Dataset Overview"
    )

    numerical_columns = len(
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_columns = len(
        df.select_dtypes(
            include=[
                "object",
                "category"
            ]
        ).columns
    )

    add_text(
        f"Total Rows: {df.shape[0]:,}"
    )

    add_text(
        f"Total Columns: {df.shape[1]:,}"
    )

    add_text(
        f"Numerical Columns: "
        f"{numerical_columns}"
    )

    add_text(
        f"Categorical Columns: "
        f"{categorical_columns}"
    )

    # ============================================
    # 3. DATA QUALITY ANALYSIS
    # ============================================

    add_heading(
        3,
        "Data Quality Analysis"
    )

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_records = int(
        df.duplicated().sum()
    )

    total_cells = (
        df.shape[0] *
        df.shape[1]
    )

    missing_percentage = 0

    if total_cells > 0:

        missing_percentage = (
            missing_values /
            total_cells
        ) * 100

    add_text(
        f"Total Missing Values: "
        f"{missing_values:,}"
    )

    add_text(
        f"Overall Missing Cell Percentage: "
        f"{missing_percentage:.1f}%"
    )

    add_text(
        f"Duplicate Records: "
        f"{duplicate_records:,}"
    )

    if missing_percentage > 50:

        add_text(
            "Missing Data Status: "
            "High amount of missing data"
        )

    elif missing_percentage > 10:

        add_text(
            "Missing Data Status: "
            "Moderate amount of missing data"
        )

    else:

        add_text(
            "Missing Data Status: "
            "Low amount of missing data"
        )

    if duplicate_records > 0:

        add_text(
            "Duplicate Status: "
            "Duplicate records detected"
        )

    else:

        add_text(
            "Duplicate Status: "
            "No duplicate records detected"
        )

    # ============================================
    # 4. COLUMN INFORMATION
    # ============================================

    add_heading(
        4,
        "Column Information"
    )

    add_subheading(
        "Columns in Dataset"
    )

    for column in df.columns:

        add_bullet(
            column
        )

    pdf.ln(2)

    add_subheading(
        "Column Data Types"
    )

    for column in df.columns:

        dtype = str(
            df[column].dtype
        )

        add_text(
            f"{column}: {dtype}"
        )

    # ============================================
    # 5. STATISTICAL SUMMARY
    # ============================================

    add_heading(
        5,
        "Statistical Summary"
    )

    numerical_df = df.select_dtypes(
        include="number"
    )

    if not numerical_df.empty:

        statistics = (
            numerical_df
            .describe()
            .T
        )

        for column in statistics.index:

            add_text(
                f"{column}: "
                f"Mean={statistics.loc[column, 'mean']:.3f}, "
                f"Median={statistics.loc[column, '50%']:.3f}, "
                f"Min={statistics.loc[column, 'min']:.3f}, "
                f"Max={statistics.loc[column, 'max']:.3f}"
            )

    else:

        add_text(
            "No numerical columns are available "
            "for statistical analysis."
        )

    # ============================================
    # 6. OUTLIER ANALYSIS
    # ============================================

    add_heading(
        6,
        "Outlier Analysis"
    )

    if automatic_insights is not None:

        outlier_info = (
            automatic_insights.get(
                "outliers",
                {}
            )
        )

        outlier_column = (
            outlier_info.get(
                "column"
            )
        )

        outlier_count = (
            outlier_info.get(
                "count",
                0
            )
        )

        if outlier_column:

            add_text(
                f"Column with Most Potential "
                f"Outliers: {outlier_column}"
            )

            add_text(
                f"Potential Outliers: "
                f"{outlier_count:,}"
            )

            add_text(
                outlier_info.get(
                    "message",
                    ""
                )
            )

        else:

            add_text(
                "No significant outlier information "
                "was provided."
            )

    else:

        add_text(
            "Outlier analysis was not generated."
        )

    # ============================================
    # 7. CORRELATION ANALYSIS
    # ============================================

    add_heading(
        7,
        "Correlation Analysis"
    )

    if automatic_insights is not None:

        correlation_info = (
            automatic_insights.get(
                "correlation",
                {}
            )
        )

        column_a = (
            correlation_info.get(
                "column_a"
            )
        )

        column_b = (
            correlation_info.get(
                "column_b"
            )
        )

        correlation_value = (
            correlation_info.get(
                "value"
            )
        )

        if column_a and column_b:

            add_text(
                f"Strongest Correlation: "
                f"{column_a} and {column_b}"
            )

            add_text(
                f"Correlation Coefficient: "
                f"{correlation_value}"
            )

            add_text(
                correlation_info.get(
                    "message",
                    ""
                )
            )

        else:

            add_text(
                "No suitable correlation relationship "
                "was identified."
            )

    else:

        add_text(
            "Correlation analysis was not generated."
        )

    # ============================================
    # 8. AUTOMATIC DATASET INSIGHTS
    # ============================================

    add_heading(
        8,
        "Automatic Dataset Insights"
    )

    if automatic_insights is not None:

        dataset_info = (
            automatic_insights.get(
                "dataset",
                {}
            )
        )

        quality_info = (
            automatic_insights.get(
                "data_quality",
                {}
            )
        )

        column_info = (
            automatic_insights.get(
                "columns",
                {}
            )
        )

        outlier_info = (
            automatic_insights.get(
                "outliers",
                {}
            )
        )

        correlation_info = (
            automatic_insights.get(
                "correlation",
                {}
            )
        )

        add_text(
            f"Dataset contains "
            f"{dataset_info.get('rows', df.shape[0]):,} "
            f"rows and "
            f"{dataset_info.get('columns', df.shape[1]):,} "
            f"columns."
        )

        add_text(
            f"Numerical columns: "
            f"{column_info.get('numerical_count', numerical_columns)}"
        )

        add_text(
            f"Categorical columns: "
            f"{column_info.get('categorical_count', categorical_columns)}"
        )

        add_text(
            quality_info.get(
                "missing_message",
                ""
            )
        )

        add_text(
            quality_info.get(
                "duplicate_message",
                ""
            )
        )

        add_text(
            outlier_info.get(
                "message",
                ""
            )
        )

        add_text(
            correlation_info.get(
                "message",
                ""
            )
        )

    else:

        add_text(
            "Automatic dataset insights were not generated."
        )

    # ============================================
    # 9. DATASET HEALTH
    # ============================================

    add_heading(
        9,
        "Dataset Health"
    )

    if dataset_health is not None:

        health_score = (
            dataset_health.get(
                "score",
                0
            )
        )

        health_status = clean_text(
            dataset_health.get(
                "status",
                "N/A"
            )
        )

        add_text(
            f"Health Score: "
            f"{health_score}/100"
        )

        add_text(
            f"Overall Status: "
            f"{health_status}"
        )

        add_text(
            f"Missing Data Impact: "
            f"-{dataset_health.get('missing_penalty', 0)}"
        )

        add_text(
            f"Duplicate Impact: "
            f"-{dataset_health.get('duplicate_penalty', 0)}"
        )

        add_text(
            f"Outlier Impact: "
            f"-{dataset_health.get('outlier_penalty', 0)}"
        )

    else:

        add_text(
            "Dataset health analysis was not generated."
        )

    # ============================================
    # 10. RECOMMENDED ACTIONS
    # ============================================

    add_heading(
        10,
        "Recommended Actions"
    )

    if dataset_health is not None:

        recommendations = (
            dataset_health.get(
                "recommendations",
                []
            )
        )

        if recommendations:

            for recommendation in recommendations:

                add_bullet(
                    recommendation
                )

        else:

            add_text(
                "No major recommendations were generated."
            )

    else:

        add_text(
            "Recommendations were not generated."
        )

    # ============================================
    # 11. AI EXECUTIVE SUMMARY
    # ============================================

    add_heading(
        11,
        "AI Executive Summary"
    )

    if ai_executive_summary:

        add_ai_summary(
            ai_executive_summary
        )

    else:

        add_text(
            "AI Executive Summary was not generated "
            "for this report."
        )

    # ============================================
    # 12. REPORT DETAILS
    # ============================================

    add_heading(
        12,
        "Report Details"
    )

    current_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    add_text(
        f"Generated On: {current_time}"
    )

    add_text(
        "Generated By: InsightGPT Lite"
    )

    add_text(
        "Platform: AI-Powered Data Analytics "
        "and RAG System"
    )

    # ============================================
    # SAVE REPORT
    # ============================================

    report_directory = "reports"

    os.makedirs(
        report_directory,
        exist_ok=True
    )

    report_path = os.path.join(
        report_directory,
        "InsightGPT_Report.pdf"
    )

    pdf.output(
        report_path
    )

    return report_path